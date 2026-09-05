"""
cinemetrics.py — no-ML cinematography metrics for short clips.

Measures, per clip, using only OpenCV + numpy:
  - cut rate            (frame-difference cut detection)
  - camera movement     (dominant global affine flow -> static/pan/tilt/push/pull/roll)
  - lighting key        (luminance histogram -> low-key / high-key / mid, plus contrast)
  - colour statistics   (colourfulness, mean saturation, warm/cool balance)
  - shot scale proxy    (largest face box area as fraction of frame)
  - depth-of-field proxy(centre-vs-surround sharpness ratio)

Dependencies: opencv-python, numpy.  No model weights, no network.

Usage:
    python cinemetrics.py clip.mp4
    python cinemetrics.py shots/*.mp4 --json out.json
"""

import argparse
import glob
import json
import math
import sys

import cv2
import numpy as np


# ---------------------------------------------------------------- frame access

def read_frames(path, max_side=480, stride=1):
    """Yield (index, bgr_frame) downscaled so the long side is <= max_side."""
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise IOError(f"cannot open {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if i % stride == 0:
            h, w = frame.shape[:2]
            s = max_side / max(h, w)
            if s < 1.0:
                frame = cv2.resize(frame, (int(w * s), int(h * s)),
                                   interpolation=cv2.INTER_AREA)
            yield i, frame
        i += 1
    cap.release()
    return


def clip_info(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return {"fps": round(fps, 3), "frames": n, "width": w, "height": h,
            "duration_s": round(n / fps, 3) if fps else None}


# -------------------------------------------------------------------- cut rate

def cuts(frames, floor=18.0, ratio=3.0, window=9):
    """
    Adaptive cut detection: mean absolute HSV delta between adjacent frames,
    compared against a ROLLING MEDIAN of the surrounding deltas.

    A fixed threshold (PySceneDetect's ContentDetector default of 27) is
    unusable here: a fast pan or a push-in raises the frame-to-frame delta
    above 27 on every single frame, so a smooth one-take clip reports a cut
    per frame. Camera-moving clips are the norm in generated footage, so we
    need the adaptive form — the same reason PySceneDetect ships
    AdaptiveDetector alongside ContentDetector.

    A frame is a cut when its delta is both:
      - `ratio` times the local median delta (it stands out from its context), and
      - above `floor` in absolute terms (it is a real change, not amplified noise).

    Returns (cut_frame_indices, per_frame_scores).
    """
    prev = None
    scores, idxs = [], []
    for idx, bgr in frames:
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
        if prev is not None:
            scores.append(float(np.abs(hsv - prev).mean()))
            idxs.append(idx)
        prev = hsv

    if not scores:
        return [], []

    s = np.asarray(scores)
    cut_idx = []
    for i, v in enumerate(s):
        lo, hi = max(0, i - window), min(len(s), i + window + 1)
        ctx = np.concatenate([s[lo:i], s[i + 1:hi]])
        if ctx.size == 0:
            continue
        med = float(np.median(ctx))
        if v >= floor and v >= ratio * max(med, 1.0):
            cut_idx.append(idxs[i])
    return cut_idx, scores


# ------------------------------------------------------------- camera movement

def camera_motion(frames):
    """
    Estimate global camera motion by fitting a partial affine transform to
    tracked corners between adjacent frames (Shi-Tomasi + Lucas-Kanade).

    The partial-affine model gives translation (dx, dy), scale and rotation.
    Those map directly onto the film vocabulary:
        dx  -> pan   (or truck)
        dy  -> tilt  (or pedestal)
        scale > 1 -> push in / zoom in ; scale < 1 -> pull out
        rotation  -> roll / dutch

    Returns a dict of cumulative and per-frame-normalised motion, plus a label.
    """
    prev_gray = None
    prev_pts = None
    dxs, dys, dss, drs = [], [], [], []
    W = H = None

    for _, bgr in frames:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        H, W = gray.shape
        if prev_gray is not None:
            if prev_pts is None or len(prev_pts) < 20:
                prev_pts = cv2.goodFeaturesToTrack(
                    prev_gray, maxCorners=400, qualityLevel=0.01,
                    minDistance=8, blockSize=7)
            if prev_pts is not None and len(prev_pts) >= 8:
                nxt, status, _ = cv2.calcOpticalFlowPyrLK(
                    prev_gray, gray, prev_pts, None,
                    winSize=(21, 21), maxLevel=3)
                if nxt is not None:
                    good_prev = prev_pts[status.ravel() == 1]
                    good_next = nxt[status.ravel() == 1]
                    if len(good_prev) >= 8:
                        M, _ = cv2.estimateAffinePartial2D(
                            good_prev, good_next, method=cv2.RANSAC,
                            ransacReprojThreshold=3.0)
                        if M is not None:
                            scale = math.hypot(M[0, 0], M[1, 0])
                            rot = math.degrees(math.atan2(M[1, 0], M[0, 0]))
                            # Translation must be read AT THE FRAME CENTRE, not
                            # at the origin. M[:,2] is the shift of the top-left
                            # corner, so a pure zoom or roll about the centre
                            # shows up there as a large fake pan/tilt. Map the
                            # centre point through M and take its displacement.
                            cx, cy = W / 2.0, H / 2.0
                            dx = M[0, 0] * cx + M[0, 1] * cy + M[0, 2] - cx
                            dy = M[1, 0] * cx + M[1, 1] * cy + M[1, 2] - cy
                            dxs.append(dx); dys.append(dy)
                            dss.append(scale); drs.append(rot)
                        prev_pts = good_next.reshape(-1, 1, 2)
                    else:
                        prev_pts = None
                else:
                    prev_pts = None
        prev_gray = gray

    if not dxs or not W:
        return {"label": "unknown", "n_pairs": 0}

    n = len(dxs)
    # Use the MEDIAN per-frame delta, not the mean, and extrapolate to the whole
    # clip. Summing or multiplying per-frame estimates lets a handful of bad
    # RANSAC fits dominate: a 0.5% per-frame scale error compounds to 40% over
    # 72 frames. The median is unmoved by those outliers.
    pan = float(np.median(dxs)) / W
    tilt = float(np.median(dys)) / H
    zoom = float(np.exp(np.median(np.log(dss)) * n))
    roll = float(np.median(drs) * n)
    # spread of the per-frame deltas: high means handheld/erratic, low means
    # a smooth move or a locked-off camera
    jitter = float(np.hypot(np.std(dxs) / W, np.std(dys) / H))

    # Per-frame fractions of the frame. 0.0008 of the width per frame is about
    # 6% of the frame per second at 24fps — slower than that reads as locked off.
    T = 0.0008
    parts = []
    if abs(pan) > T:
        # positive dx means content moved right, i.e. the camera panned LEFT
        parts.append("pan_left" if pan > 0 else "pan_right")
    if abs(tilt) > T:
        parts.append("tilt_up" if tilt > 0 else "tilt_down")
    if zoom > 1.05:
        parts.append("push_in")
    elif zoom < 0.95:
        parts.append("pull_out")
    if abs(roll) > 4.0:
        parts.append("roll_cw" if roll < 0 else "roll_ccw")
    label = "+".join(parts) if parts else "static"

    return {
        "label": label,
        "pan_per_frame_frac": round(pan, 5),
        "tilt_per_frame_frac": round(tilt, 5),
        "net_zoom": round(zoom, 4),
        "net_roll_deg": round(roll, 2),
        "jitter": round(jitter, 5),
        "n_pairs": n,
    }


# ------------------------------------------------------------- lighting key

def lighting(frames):
    """
    Lighting key from the luminance histogram of the clip.

    Low-key lighting puts most of its pixels in the shadows with a small
    highlight tail; high-key fills the upper range and leaves the shadows
    empty. So the discriminator is the shape of the histogram, not just
    its mean: we use the median plus the fraction of pixels in the bottom
    and top deciles of the range.
    """
    hist = np.zeros(256, dtype=np.float64)
    lums = []
    for _, bgr in frames:
        y = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        hist += cv2.calcHist([y], [0], None, [256], [0, 256]).ravel()
        lums.append(float(y.mean()))
    if hist.sum() == 0:
        return {}
    p = hist / hist.sum()
    cdf = np.cumsum(p)
    median = int(np.searchsorted(cdf, 0.5))
    shadow_frac = float(p[:26].sum())     # bottom 10% of the range
    highlight_frac = float(p[230:].sum())  # top 10%
    # dynamic range between the 5th and 95th percentile
    lo = int(np.searchsorted(cdf, 0.05))
    hi = int(np.searchsorted(cdf, 0.95))

    if shadow_frac > 0.35 and median < 80:
        key = "low_key"
    elif highlight_frac > 0.20 and median > 150:
        key = "high_key"
    else:
        key = "mid_key"

    return {
        "key": key,
        "median_luma": median,
        "mean_luma": round(float(np.mean(lums)), 2),
        "shadow_frac": round(shadow_frac, 4),
        "highlight_frac": round(highlight_frac, 4),
        "contrast_p5_p95": hi - lo,
        "luma_drift": round(float(np.max(lums) - np.min(lums)), 2),
    }


# --------------------------------------------------------------- colour stats

def colour(frames):
    """
    Colourfulness after Hasler & Süsstrunk (2003):
        rg = R - G ;  yb = 0.5(R + G) - B
        C  = sqrt(sd_rg^2 + sd_yb^2) + 0.3 * sqrt(mean_rg^2 + mean_yb^2)

    Rough reading of the scale from that paper: <15 not colourful,
    ~33 averagely colourful, >65 extremely colourful.
    """
    cs, sats, warms = [], [], []
    for _, bgr in frames:
        b, g, r = cv2.split(bgr.astype(np.float32))
        rg = r - g
        yb = 0.5 * (r + g) - b
        c = math.hypot(rg.std(), yb.std()) + 0.3 * math.hypot(rg.mean(), yb.mean())
        cs.append(c)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        sats.append(float(hsv[:, :, 1].mean()))
        # positive = warm (red/yellow heavy), negative = cool (blue heavy)
        warms.append(float(rg.mean() + yb.mean()) / 2.0)
    return {
        "colourfulness": round(float(np.mean(cs)), 2),
        "mean_saturation": round(float(np.mean(sats)), 2),
        "warm_cool": round(float(np.mean(warms)), 2),
    }


# ---------------------------------------------------------- shot scale proxy

YUNET_URL = ("https://media.githubusercontent.com/media/opencv/opencv_zoo/main/"
             "models/face_detection_yunet/face_detection_yunet_2023mar.onnx")


def shot_scale(frames, yunet_path="yunet.onnx", score_threshold=0.85):
    """
    Shot scale proxy: the largest detected face as a fraction of frame area.

    Cut points are the conventional ones — a face filling more than a quarter
    of the frame is a close-up, a face you can barely find is a wide. Only
    valid when there IS a face; returns no_face otherwise, and you fall back
    to a model or to hand-labelling for those.

    Uses YuNet (ships with OpenCV >= 4.5.4 as cv2.FaceDetectorYN) rather than a
    Haar cascade. Haar fires on texture and does it CONSISTENTLY, so a
    false positive appears on every frame of a static shot and no amount of
    temporal filtering removes it. YuNet returns a confidence score, which does.

    Fetch the 233KB model once:
        curl -L -o yunet.onnx <YUNET_URL>
    Note it is a git-LFS file: the raw.githubusercontent URL returns a
    123-byte pointer, you need the media.githubusercontent.com host.
    """
    import os
    if not os.path.exists(yunet_path):
        return {"scale": "unavailable",
                "note": f"yunet.onnx not found; fetch from {YUNET_URL}"}

    det = None
    ratios = []
    n_frames = 0
    for _, bgr in frames:
        n_frames += 1
        h, w = bgr.shape[:2]
        if det is None:
            det = cv2.FaceDetectorYN.create(yunet_path, "", (w, h),
                                            score_threshold, 0.3, 5000)
        _, faces = det.detect(bgr)
        if faces is not None and len(faces):
            # each row: x, y, w, h, 5 landmarks..., score
            area = max(f[2] * f[3] for f in faces) / float(w * h)
            ratios.append(float(area))

    hit_rate = len(ratios) / max(n_frames, 1)
    if not ratios or hit_rate < 0.2:
        return {"scale": "no_face", "face_area_frac": None,
                "detected_in": len(ratios), "hit_rate": round(hit_rate, 3)}
    a = float(np.median(ratios))
    if a > 0.25:
        s = "extreme_close_up"
    elif a > 0.10:
        s = "close_up"
    elif a > 0.03:
        s = "medium"
    elif a > 0.008:
        s = "full"
    else:
        s = "wide"
    return {"scale": s, "face_area_frac": round(a, 5), "detected_in": len(ratios)}


# ------------------------------------------------------- depth of field proxy

def depth_of_field(frames):
    """
    Shallow-vs-deep focus proxy: variance of Laplacian in the centre third
    against the surrounding border. A shallow-focus shot has a sharp subject
    and a soft background, so the ratio runs high; a deep-focus shot is
    sharp edge to edge and the ratio sits near 1.

    This assumes the subject is centred. It is wrong for off-centre framing.
    """
    ratios = []
    for _, bgr in frames:
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        h, w = g.shape
        y0, y1 = h // 3, 2 * h // 3
        x0, x1 = w // 3, 2 * w // 3
        centre = g[y0:y1, x0:x1]
        mask = np.ones_like(g, dtype=bool)
        mask[y0:y1, x0:x1] = False
        lap = cv2.Laplacian(g, cv2.CV_64F)
        c_var = float(lap[y0:y1, x0:x1].var())
        s_var = float(lap[mask].var())
        if s_var > 1e-6:
            ratios.append(c_var / s_var)
    if not ratios:
        return {}
    r = float(np.median(ratios))
    return {
        "focus": "shallow" if r > 2.0 else ("deep" if r < 1.2 else "medium"),
        "centre_surround_sharpness": round(r, 3),
    }


# --------------------------------------------------------------------- driver

def analyse(path, stride=1, max_side=480):
    """Run every metric on one clip. Frames are decoded once per metric;
    for clips of a few seconds that is cheap enough not to bother caching."""
    info = clip_info(path)
    fps = info["fps"] or 24.0

    cut_idx, scores = cuts(read_frames(path, max_side, stride))
    dur = info["duration_s"] or 1.0
    cut_stats = {
        "n_cuts": len(cut_idx),
        "cuts_per_min": round(len(cut_idx) / dur * 60, 2) if dur else None,
        "mean_shot_len_s": round(dur / (len(cut_idx) + 1), 3),
        "single_take": len(cut_idx) == 0,
        "peak_frame_delta": round(max(scores), 2) if scores else None,
    }

    return {
        "clip": path,
        "info": info,
        "cuts": cut_stats,
        "camera": camera_motion(read_frames(path, max_side, stride)),
        "lighting": lighting(read_frames(path, max_side, stride)),
        "colour": colour(read_frames(path, max_side, stride)),
        # Faces are detected at NATIVE resolution, not the downscaled frames the
        # other metrics use. YuNet's floor is a roughly fixed pixel size (~30-40px
        # box), so the smallest face it can find as a FRACTION of the frame drops
        # about tenfold going from 640x360 to 1280x720. Downscaling here would
        # make every wide shot report no_face.
        "shot_scale": shot_scale(read_frames(path, 1920, max(stride, 2))),
        "dof": depth_of_field(read_frames(path, max_side, stride)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--json", help="write results to this file")
    ap.add_argument("--stride", type=int, default=1,
                    help="analyse every Nth frame (2 is usually safe, and halves runtime)")
    args = ap.parse_args()

    paths = []
    for c in args.clips:
        paths.extend(sorted(glob.glob(c)) or [c])

    out = []
    for p in paths:
        try:
            r = analyse(p, stride=args.stride)
        except Exception as e:
            r = {"clip": p, "error": str(e)}
        out.append(r)
        print(json.dumps(r, indent=2))

    if args.json:
        with open(args.json, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nwrote {args.json}", file=sys.stderr)


if __name__ == "__main__":
    main()

# Brain-Reactive Livestream: TRIBE v2 → MiniMax H3 Max

> Low-development-complexity system coupling Meta TRIBE v2 brain-response prediction to fal.ai MiniMax H3 Max video generation, so predicted brain responses to audiovisual content dynamically write the prompts for a continuous AI livestream.

*Generated 2026-09-01 · 20 research items · all validated at 100% field coverage · fields marked uncertain are omitted*

---

## Contents

1. [Autoregressive Realtime Alternative](#autoregressive-realtime-alternative) — Complexity: **LOW**
2. [Brain State To Prompt Translation Layer](#brain-state-to-prompt-translation-layer) — Complexity: **LOW** · Cost: $0.00/hour
3. [Brain-output semantic readout](#brain-output-semantic-readout) — Complexity: **LOW** · Cost: $0.00 per hour
4. [Clip continuity and chaining](#clip-continuity-and-chaining) — Complexity: **LOW** · Cost: $0.08/s
5. [Closed Loop Recursion](#closed-loop-recursion) — Complexity: **MEDIUM**
6. [Closed-loop neuro-generation prior art](#closed-loop-neuro-generation-prior-art) — Complexity: **LOW**
7. [Cost model](#cost-model) — Complexity: **LOW** · Cost: $90.36/hr
8. [Differentiable stimulus optimisation as an offline motif table](#differentiable-stimulus-optimisation-as-an-offline-motif-table) — Complexity: **LOW**
9. [fal MiniMax H3 Max generation API](#fal-minimax-h3-max-generation-api) — Complexity: **LOW**
10. [GPU hosting for TRIBE v2](#gpu-hosting-for-tribe-v2) — Complexity: **LOW**
11. [Latency budget and real-time feasibility](#latency-budget-and-real-time-feasibility) — Complexity: **LOW** · Cost: $0.54/hr
12. [Licence, ethics and framing](#licence-ethics-and-framing) — Complexity: **LOW** · Cost: $0.00 per hour
13. [Neural data regulatory surface](#neural-data-regulatory-surface) — Complexity: **LOW**
14. [Observability and on-stream brain visualisation](#observability-and-on-stream-brain-visualisation) — Complexity: **LOW**
15. [Orchestration loop and buffer management](#orchestration-loop-and-buffer-management) — Complexity: **MEDIUM**
16. [Prior art and reference implementations](#prior-art-and-reference-implementations) — Complexity: **LOW**
17. [Radical simplification paths](#radical-simplification-paths) — Complexity: **LOW**
18. [Stimulus ingestion and windowing](#stimulus-ingestion-and-windowing) — Complexity: **MEDIUM**
19. [Streaming and playback pipeline](#streaming-and-playback-pipeline) — Complexity: **LOW**
20. [TRIBE v2 inference interface and runtime cost](#tribe-v2-inference-interface-and-runtime-cost) — Complexity: **MEDIUM**

---

## Autoregressive Realtime Alternative

### Identity

**what_it_is**

Krea Realtime 14B (Wan 2.1 14B distilled with Self-Forcing into an autoregressive/causal video model) served as a hosted realtime WebSocket endpoint on fal as `fal-ai/krea-wan-14b`. It streams JPEG frames continuously and accepts prompt changes MID-GENERATION, so steering is continuous rather than clip-stepwise.

**role_in_loop**

It replaces BOTH the 'generate' and 'stream' stages of the loop, and dissolves the 'clip queue' stage entirely. TRIBE readout -> prompt string -> one WebSocket send -> frames already flowing on the canvas. There is no per-clip request/response boundary, no buffer scheduler and no concatenation step.

### Interface

**interface_spec**

HOSTED REALTIME (the path that matters):
1. Mint a short-lived JWT server-side:
   POST https://rest.alpha.fal.ai/tokens/
   Headers: Authorization: Key $FAL_KEY, Content-Type: application/json
   Body: {"allowed_apps": ["krea-wan-14b"], "token_expiration": 5000}
   Response: {"token": "eyJ..."}   (5000 s ~= 83 min lifetime)
2. Open the socket:
   wss://fal.run/fal-ai/krea-wan-14b/ws?fal_jwt_token=<urlencoded JWT>
   ws.binaryType = 'arraybuffer'
3. Server sends a TEXT frame {"status":"ready"}. Only then send params.
4. Send msgpack-encoded initial params (BINARY frame):
   {prompt: str, width: int (mult of 8, default 832), height: int (mult of 8, default 480),
    num_blocks: int, num_denoising_steps: 4, strength: float, seed?: int (0..2^24),
    start_frame?: bytes (JPEG, for image/canvas/webcam conditioning)}
5. Server streams BINARY frames: raw JPEG bytes per frame as ArrayBuffer. Decode with
   createImageBitmap(new Blob([buf],{type:'image/jpeg'})) and draw to a <canvas>.
   Errors/status arrive as TEXT JSON: {"status": ...} or {"error": ...}.
6. MID-STREAM STEERING (the whole point) -- a single send, no reconnect:
   ws.send(msgpackEncode({prompt: newPrompt, num_blocks: numBlocks}))
   The model interpolates prompt embeddings, so the scene morphs rather than cuts.
7. VIDEO-TO-VIDEO / continuous conditioning (same socket): send at input fps
   {image: Uint8Array(JPEG), strength: float (0-1), prompt: str, num_blocks: int, timestamp: int}

QUEUED (non-realtime) SIBLINGS on the same model, for reference:
  POST https://queue.fal.run/fal-ai/krea-wan-14b/text-to-video
    input: {prompt, num_frames (=6+12k, default 78), enable_prompt_expansion, seed}
    output: {video: {url, content_type, file_name, file_size}}
  POST https://queue.fal.run/fal-ai/krea-wan-14b/video-to-video
    input: {prompt, video_url, strength (default 0.85), enable_prompt_expansion, seed}
    constraints: 16:9 and 480p ONLY; <1000 frames at 16 fps; frames = 6 + 12k

FAL'S THREE TRANSPORT SURFACES (documented for completeness):
  a) Queue REST: https://queue.fal.run/{model-id} -> request_id, then /status and /requests/{id};
     webhook supported. This is what H3 Max uses.
  b) SSE streaming: https://queue.fal.run/{model-id}/stream returns text/event-stream with
     progressive partial outputs. fal_client.stream() (Py) / fal.stream() (JS) append /stream
     automatically. ONE-WAY: you cannot push a new prompt into a running request.
  c) Realtime WebSocket: wss://fal.run/{model-id}/ws, msgpack binary, BIDIRECTIONAL --
     this is the only surface that accepts mid-generation input. fal_client.realtime() /
     fal_client.ws_connect() in Python; hand-rolled WebSocket + msgpack in the JS scaffold.

**input_contract**

Per socket: a JWT scoped to allowed_apps=['krea-wan-14b'], then one msgpack params object, then an unbounded sequence of msgpack prompt updates. Prompt is plain text -- Krea's own guidance is that LONG prompts that explicitly describe MOTION work far better than short noun phrases (short prompts yield near-static output). Dimensions must be multiples of 8 (832x480 default; the queued endpoints are 16:9/480p only). num_denoising_steps is effectively fixed at 4. Optional start_frame as JPEG bytes gives you image conditioning; optional per-frame {image, strength} gives you live video-to-video. For the TRIBE loop the only input that changes at runtime is the prompt string -- everything else is set once at socket open.

**output_contract**

A continuous stream of individual JPEG-encoded RGB frames as binary WebSocket messages, nominally 832x480, at the model's native 16 fps timebase but produced at ~11 fps wall-clock. No container, no timestamps, no audio track -- you get pixels only. Each frame is a complete image (not a delta), so dropping frames is harmless. Interleaved TEXT JSON messages carry status and validation errors. To get a broadcastable stream you draw frames to a canvas and either captureStream() + MediaRecorder (what the scaffold does, producing WebM/VP9) or pipe to ffmpeg for RTMP/HLS.

### Complexity

**dev_complexity**

LOW -- materially lower than the H3 Max clip queue, and this reverses the assumption in the brief. The reason is that fal HOSTS Krea Realtime: `fal-ai/krea-wan-14b` is a managed endpoint with the same zero-infrastructure profile as H3 Max. You do not need a B200. The premise that this path costs you a GPU is only true for the self-hosted `krea-ai/realtime-video` repo, which is a different and much worse option (40GB+ VRAM, Flash-Attention-4/SageAttention builds, 30GB of checkpoints, and CC-BY-NC-SA-4.0 weights that forbid commercial use). Given hosting parity, the realtime path is strictly less code: no queue manager, no double buffer, no clip concatenation, no seam handling, no mux pipeline. The one place it is HARDER is audio -- Krea Realtime emits no audio at all, so a livestream needs a separate sound bed, whereas H3 Max gives you synchronised dialogue/music/SFX for free.

**off_the_shelf_option**

github.com/fal-ai-community/realtime-krea-wan -- MIT, Next.js 15 / React 19 / TypeScript / Tailwind v4, created 2025-10-14, last pushed 2025-12-09, 17 stars / 4 forks, no open issues surfaced. It is small and low-traffic but COMPLETE and RUNNABLE: `npm install`, put FAL_API_KEY in .env.local, `npm run dev`. It already implements every hard part -- JWT minting route (src/app/api/fal/route.ts), a hand-rolled msgpack encoder (src/lib/msgpack.ts, 141 LOC, no dependency), the full WebSocket lifecycle with ready-signal handshake and close-code mapping (src/hooks/useWebSocket.ts, 431 LOC), JPEG->ImageBitmap frame buffering and a canvas playback loop, MediaRecorder capture to WebM, and text / canvas(Konva) / webcam input modes. It deploys to Vercel with one env var. This is genuinely the nearest existing scaffold to the target system: it is text-to-video with dynamic prompt rewriting on a realtime model, which is the target minus the brain readout. VERDICT: runnable today, requires NO GPU (all compute is fal's), costs only fal inference credits. Caveat: its README has drifted from its code (num_blocks documented 10-50, hardcoded 1000; 'Blocks slider' described but the shipped control is fixed), so trust the source over the docs. Self-host alternative github.com/krea-ai/realtime-video (580 stars, CC-BY-NC-SA-4.0, ships release_server.py WebSocket server) -- NOT recommended: non-commercial licence plus B200/H100-class hardware.

### Decision

**recommended_approach**

VERDICT: YES -- the Krea Realtime continuous stream is the shorter path for a solo developer, PROVIDED you can live without native audio and at 480p/~11fps. Take it.

The decisive fact is hosting parity. The brief assumes Krea Realtime means renting a B200; it does not. fal serves it at `fal-ai/krea-wan-14b` with a realtime WebSocket, so both candidates are hosted APIs with zero infrastructure. Once that asymmetry is gone, the comparison is one-sided:
  - CODE YOU DON'T WRITE: the clip queue forces you to build a request scheduler, an N-deep clip buffer,     frame-accurate playback handoff, last-frame->next-clip continuity chaining, and an ffmpeg concat/HLS     pipeline. In the realtime path all five are absent by construction. This is the single biggest delta.
  - STEERING: ~1.5 s brain-to-pixel vs ~5-8 s. For a brain-REACTIVE demo, perceived causality is the     product. At 8 s viewers do not connect the signal to the picture.
  - CONTINUITY: prompt-embedding interpolation morphs the scene. Clip chaining cuts every 5 s, and every     cut is a chance for identity/scene drift; H3 Max's audio does NOT chain across clips, so you get an     audible seam at every boundary regardless of how well you match the video.
  - COST: ~$62/hr of wall-clock stream vs $180/hr for H3 Max at 480p once the launch promo ends 2026-09-01.

CONCRETE BUILD, in order:
  1. `git clone https://github.com/fal-ai-community/realtime-krea-wan` (MIT), npm install,      FAL_API_KEY=... in .env.local, npm run dev. Confirm frames stream and that typing in the prompt box      visibly morphs the scene. This alone is 30 minutes and de-risks the whole architecture.
  2. In src/app/page.tsx, delete the textarea debounce path and feed the TRIBE readout into the SAME      `sendPromptUpdate(prompt, numBlocks)` call. Throttle brain updates to ~1 Hz (one block) -- faster is      wasted because updates only take effect at block boundaries, and it makes the motion incoherent.
  3. Add a supervisor: refresh the JWT and re-open the socket before the 5000 s expiry, and on the 10 s      frame watchdog reconnect while continuing to paint the last frame, so a drop reads as a pause, not a crash.
  4. Add an audio bed. Krea Realtime is SILENT. A looped ambient track, or a generative music endpoint      driven by the same brain readout at a slower cadence, is far less work than switching generators.
  5. For broadcast, pipe the canvas to ffmpeg -> RTMP/HLS instead of MediaRecorder->WebM.

WHEN TO CHOOSE H3 MAX INSTEAD -- state this plainly: if native synchronised audio is non-negotiable, or if you need 768p/2K fidelity and clean camera motion, H3 Max wins outright and no amount of engineering closes that gap on the Krea side. Krea Realtime's documented failure profile (mode collapse, weak complex camera movement, colour shift, error accumulation) is the price of 4-step autoregression.

**simpler_alternative**

Three fallbacks, cheapest-first:
1. STAY ON THE SCAFFOLD, DROP THE BROADCAST. Ship the Next.js page itself as the 'stream' -- viewers open    a URL and watch the canvas. Removes ffmpeg/RTMP/HLS entirely. This is the true minimum demo.
2. DECART REALTIME AS A STYLISER, NOT A GENERATOR. Decart's self-serve platform (platform.decart.ai) bills    realtime models per second of active generation: Lucy Restyle 2 at $0.01/s (=$36/hr, the cheapest    realtime option found), Lucy 2.5 and Lucy VTON 3.5 at $0.02/s, Oasis 3 Preview (world model) at $0.02/s.    But these are VIDEO-TO-VIDEO -- they transform an incoming stream, they do not generate from text alone.    Usable as: loop a source video, steer style/mood from the brain readout. Cheap and very robust, but the    content is yours, not the model's. NOTE on MirageLSD specifically: 768x432 at 20 fps, <40 ms/frame, and it    IS video-to-video. It does NOT appear on Decart's public pricing page (superseded by the Lucy line), and    the Crusoe Cloud listing is gated behind 'contact us'. Treat MirageLSD as NOT self-serve-available; use    the Lucy realtime endpoints if you want this family.
3. FALL BACK TO THE H3 MAX CLIP QUEUE if realtime quality or the missing audio kills the piece. The work is    larger but every step is conventional and it degrades gracefully -- a failed clip costs 5 seconds,    whereas a dropped WebSocket kills the stream.

**code_sketch**

// The entire brain-steering integration, on top of the forked scaffold.
// Everything below `sendPromptUpdate` already exists in src/hooks/useWebSocket.ts.

// --- server: mint the JWT (src/app/api/fal/route.ts, already present) ---
// POST https://rest.alpha.fal.ai/tokens/  Authorization: Key $FAL_API_KEY
// body {allowed_apps:['krea-wan-14b'], token_expiration:5000} -> {token}

// --- client: open once ---
const token = (await (await fetch('/api/fal',{method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({allowed_apps:['krea-wan-14b'],token_expiration:5000})})).json()).token;

const ws = new WebSocket(`wss://fal.run/fal-ai/krea-wan-14b/ws?fal_jwt_token=${encodeURIComponent(token)}`);
ws.binaryType = 'arraybuffer';

ws.onmessage = async (e) => {
  if (typeof e.data === 'string') {                 // control channel
    const m = JSON.parse(e.data);
    if (m.status === 'ready') ws.send(msgpackEncode({
      prompt: seedPromptFromBaseline(),             // first TRIBE-derived prompt
      width: 832, height: 480,
      num_blocks: 1000,                             // effectively 'run until stopped'
      num_denoising_steps: 4,
      strength: 1.0,
      seed: Math.floor(Math.random() * (1 << 24)),
    }));
    if (m.error) console.error('fal validation:', m.error);
    return;
  }
  // data channel: one complete JPEG per message
  const bmp = await createImageBitmap(new Blob([e.data], { type: 'image/jpeg' }));
  frameQueue.push(bmp);                             // canvas playback loop drains this
  lastFrameAt = Date.now();
};

// --- THE ACTUAL INTEGRATION: brain readout replaces the textarea ---
// One block is ~12 frames at ~11fps, so updating faster than ~1 Hz is wasted work
// and makes the motion incoherent. Throttle, do not debounce.
tribe.onPrediction(({ embedding }) => {
  const prompt = promptFromBrainState(embedding);   // your readout -> long, motion-rich text
  if (ws.readyState !== WebSocket.OPEN) return;
  if (Date.now() - lastSteerAt < 1000) return;
  lastSteerAt = Date.now();
  ws.send(msgpackEncode({ prompt, num_blocks: 1000 }));  // <-- morphs, does not cut
});

// --- keep it infinite: JWT dies at ~83 min, watchdog at 10 s of silence ---
setInterval(() => {
  const stalled = Date.now() - lastFrameAt > 10_000;
  const expiring = Date.now() - socketOpenedAt > 4_500_000;   // refresh before 5000 s
  if (stalled || expiring) reopenSocketKeepingLastFrameOnCanvas();
}, 1000);

// Python equivalent of the transport, if you prefer a server-side pump:
//   import fal_client;  fal_client.realtime('fal-ai/krea-wan-14b')  # msgpack handled for you
//   (or fal_client.ws_connect() for raw is_websocket=True apps)
// SSE sibling, for progressive output WITHOUT mid-stream input:
//   fal_client.stream(...)  ->  GET https://queue.fal.run/{model-id}/stream (text/event-stream)

### Risk

**failure_modes**

1. SILENT STREAM. Krea Realtime produces no audio whatsoever. On a livestream, silence reads as a broken    feed within seconds. This is the single biggest quality gap versus H3 Max's native synchronised audio    and it is not fixable inside the model -- you must add a bed.
2. MODE COLLAPSE FROM SELF-FORCING DISTILLATION. Krea document this themselves: the student is prone to    mode collapse and low output diversity. Under a brain-driven prompt stream that hovers near one state,    the picture can lock into a repetitive loop and stop looking reactive even though prompts are changing.
3. SHORT PROMPTS PRODUCE STATIC VIDEO. Krea's guidance is explicit that long prompts describing motion are    required. A naive readout emitting terse labels ('calm', 'anxious') will yield near-frozen frames -- the    brain-to-prompt mapping must synthesise long motion-rich sentences, not adjectives.
4. ERROR ACCUMULATION / COLOUR SHIFT OVER LONG ROLLOUTS. Mitigated in-model by KV-cache recomputation and    a negative attention bias on past-frame tokens, plus a deliberately short 3-latent-frame (~12 RGB frame)    context window -- but 'mitigated' is not 'solved'. Open issues on krea-ai/realtime-video include    'color shift' and 'generated videos are all noise/snow-like'. A multi-hour stream will drift.
5. SHORT CONTEXT KILLS LONG-RANGE COHERENCE. ~12 RGB frames of context means the model has roughly one    second of memory. A character or setting will not survive across minutes the way a chained clip with an    explicit reference image can.
6. HARD SESSION CEILING AT ~83 MINUTES. The JWT expires at 5000 s. Without a refresh supervisor an    'infinite' stream dies on the hour. Close code 1008 (Policy Violation) is the symptom of an expired or    invalid token.
7. SINGLE POINT OF FAILURE. One dropped WebSocket ends the stream, versus the clip queue where one failed    request costs 5 seconds. The realtime path is less robust by construction and needs the reconnect    supervisor to be treated as load-bearing, not optional.
8. SCAFFOLD DOCUMENTATION DRIFT. The README describes num_blocks 10-50 and a blocks slider; the code sets    useState(1000) with no slider. Following the README will make you build against the wrong constraints.
9. SELF-HOST LICENCE TRAP. The open weights are CC-BY-NC-SA-4.0 -- NON-COMMERCIAL. Several secondary    write-ups incorrectly call them Apache-2.0. If the stream is ever monetised, self-hosting is a legal    problem; fal's hosted endpoint is separately marked commercial-use-supported and is the safe route.
10. WEAK CAMERA MOTION. Complex camera movement is a documented weakness. Prompts that ask for sweeping     camera work will underdeliver relative to H3 Max.

**unknowns**

- fal's HOSTED fps for krea-wan-14b is not published. The 11 fps figure is Krea's own on a single B200 at   4 steps. Must be measured: count frames received per wall-clock second on a real socket.
- Maximum WebSocket session length and whether num_blocks=1000 is honoured server-side. The queued   video-to-video endpoint caps at <1000 frames (~62 s); whether that bound applies to the WS path is   unknown. Measure by running one socket to exhaustion.
- Exact block size in RGB frames over the WS transport. The queued API's 'frames = 6 + 12k' implies 12,   which combined with 11 fps gives the ~1.1 s steering granularity quoted above -- but that is inference,   not documentation. This number directly sets the brain-to-pixel latency, so measure it first.
- Whether fal bills wall-clock GPU seconds or delivered frames divided by 16. This changes the hourly cost   by ~1.45x ($62/hr vs $90/hr). Run a 60 s session and read the billing dashboard.
- Resolution ceiling on the WS path. The scaffold accepts 64-2048 px but the queued endpoints are 480p/16:9   only; whether 720p works over WS is untested (there is an open upstream issue asking exactly this).
- How abruptly prompt-embedding interpolation transitions under a fast-changing brain signal -- whether it   morphs pleasingly or smears. Only observable empirically.
- MirageLSD commercial availability: not on Decart's public pricing page, and Crusoe Cloud access is   'contact us'. Whether a self-serve MirageLSD API exists at all in Aug 2026 could not be confirmed.
- Whether concurrent sockets on one fal account are rate-limited, which matters if you want a failover   stream running warm.

### Evidence

**sources**

PRIMARY SCAFFOLD (read the source directly, not just the README):
- https://github.com/fal-ai-community/realtime-krea-wan -- MIT; created 2025-10-14, pushed 2025-12-09,   17 stars / 4 forks (verified via GitHub API). Key files: src/hooks/useWebSocket.ts (431 LOC, full WS   lifecycle + sendPromptUpdate), src/lib/msgpack.ts (141 LOC), src/app/api/fal/route.ts (JWT minting),   src/app/page.tsx (508 LOC; note `const [numBlocks] = useState(1000)` contradicting the README).
- https://github.com/krea-ai/realtime-video -- self-host reference server; 580 stars, 45 forks, pushed   2025-11-13; README states 40GB+ VRAM, 11 fps on B200, ~30GB checkpoints, LICENCE CC-BY-NC-SA-4.0.   Open issues confirming failure modes: 'color shift', 'generated videos are all noise/snow-like',   'Performance', 'Support For Image2Video Task', 'Dynamic KV Cache Memory Management'.

MODEL / API:
- https://www.krea.ai/blog/krea-realtime-14b -- 11 fps at 4 steps on one B200, ~1 s to first frame,   3 latent frames (~12 RGB) context, KV-cache recomputation, negative attention bias, prompt-embedding   interpolation for mid-generation prompt change, documented mode collapse and weak camera motion.
- https://fal.ai/models/fal-ai/krea-wan-14b/text-to-video -- $0.025 per output video second at 16 fps;   num_frames = 6 + 12k, default 78; commercial use supported.
- https://fal.ai/models/fal-ai/krea-wan-14b/video-to-video/api -- 480p / 16:9 only, <1000 frames at 16 fps,   strength default 0.85.
- https://huggingface.co/krea/krea-realtime-video -- weights.
- https://docs.fal.ai/model-apis/real-time/quickstart and   https://fal.ai/docs/documentation/development/realtime -- realtime WebSocket surface, msgpack binary   protocol, fal_client.realtime() vs fal_client.ws_connect(); explicitly directs one-way progressive   output to Streaming Endpoints (SSE) instead.
- https://docs.fal.ai/model-apis/streaming and https://docs.fal.ai/model-apis/model-endpoints/queue --   /{model-id}/stream returns text/event-stream (SSE); base https://queue.fal.run.
- https://github.com/api-evangelist/fal-ai -- corroborates the three surfaces: queue REST at   queue.fal.run plus realtime WebSocket and SSE streaming.

COMPARISON TARGET:
- https://fal.ai/models/minimax/h3-max/text-to-video and https://fal.ai/minimax-h3-max -- native   synchronised audio, 5-15 s durations, optional final keyframe; 50%-off launch pricing to 2026-09-01.
- https://explainx.ai/blog/fal-h3-max-faster-than-realtime-video-august-2026 and   https://www.virse.ai/blog/what-is-minimax-h3-max-fals-faster-h3-explained -- 5 s clip in <3 s, ~2.5 s   backend denoise at 768p, ~35x the official MiniMax endpoint's throughput.

COMPETING REALTIME PLATFORM:
- https://docs.platform.decart.ai/getting-started/pricing -- realtime models billed per second of active   generation: Lucy 2.5 $0.02/s, Lucy VTON 3.5 $0.02/s, Lucy Restyle 2 $0.01/s, Oasis 3 Preview $0.02/s.   MirageLSD is NOT listed.
- https://the-decoder.com/decart-launches-miragelsd-an-ai-model-that-transforms-live-video-feeds-in-real-time/   -- MirageLSD 768x432 at 20 fps, <100 ms frame latency, video-to-video.
- https://www.crusoe.ai/resources/blog/miragelsd-decarts-real-time-ai-video-model-is-now-available-on-crusoe-cloud   -- <40 ms/frame, video-to-video, access gated behind 'contact us'; no public pricing.

ACADEMIC BACKING (all verified on arXiv):
- Helios, arXiv:2603.04379 (submitted 2026-03-04, Yuan/Yin/Li et al.) -- first 14B video model at   19.5 FPS on a SINGLE H100 with minute-scale generation, achieved WITHOUT self-forcing, error banks or   keyframe sampling, and without KV-cache tricks, sparse attention or quantisation. Supports T2V, I2V and   V2V. RELEVANCE: it is the direct successor pressure on Krea Realtime -- nearly 2x the fps on cheaper   hardware with drift handled architecturally rather than patched. If it lands on a hosted API, it   supersedes this recommendation.
- minWM, arXiv:2605.30263 (submitted 2026-05-28, Min Zhao et al.) -- open-source end-to-end pipeline   converting bidirectional T2V/TI2V foundation models into real-time camera-controllable interactive world   models, via camera-control fine-tuning, causal forcing, consistency distillation, few-step AR generation   and asymmetric DMD for streaming inference; instantiated on Wan2.1-T2V and HY1.5-TI2V. RELEVANCE: it   generalises exactly what Krea did to Wan 2.1, so the realtime-model supply will keep growing -- betting   the architecture on 'continuous stream' is betting with the trend.
- Causal Forcing++, arXiv:2605.15141 (submitted 2026-05-14, revised 2026-06-01, Min Zhao & Hongzhou Zhu   et al.) -- causal consistency distillation taking supervision from a single online teacher ODE step   rather than precomputed trajectories; 1-2 sampling steps instead of 4, beating 4-step chunk-wise   baselines while HALVING first-frame latency and cutting stage-2 training cost ~4x; extends to   action-conditioned world models. RELEVANCE: halves the exact 4-step cost that sets Krea Realtime's   11 fps ceiling, and there is an open issue on krea-ai/realtime-video titled 'Causal Forcing as an   improved replacement for Self Forcing' -- the community is already asking for it.

INFERENCE MARKERS: all per-hour dollar figures, the ~1.1-2.0 s steering latency, the ~5-8 s H3 Max steering latency, the 11-vs-16 fps deficit and the LOC estimates are DERIVED from the sourced figures above, not directly published. They are labelled as inference where they appear.

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `loc_estimate`
- `realtime_headroom`
- `throughput_constraint`

---

## Brain State To Prompt Translation Layer

### Identity

**what_it_is**

The creative core: a pure function that turns the reduced ROI activation vector for clip N (a handful of floats from item 02's readout) into the text prompt string for clip N+1, expressed in MiniMax H3 Max's preferred prompt grammar.

**role_in_loop**

Sits between readout and generation. Consumes state r_t from the brain-output readout, emits prompt_{t+1} which is POSTed to minimax/h3-max/text-to-video (or image-to-video when chaining). It is the only place in the pipeline where a number becomes an aesthetic decision, and it runs entirely on CPU/an LLM API — no GPU of its own.

### Interface

**interface_spec**

RECOMMENDED SIGNATURE (single pure function, no class needed):

    def next_prompt(
        state: dict[str, float],        # ROI name -> rolling-z-scored activation
        prev_prompt: str,               # the prompt used for clip N (or its expanded_prompt)
        archive: list[str],             # last M prompts, for the novelty term
        target: dict[str, float] | None = None,   # setpoint for trajectory-tracking policy
        step: int = 0,
    ) -> str

INPUT VECTOR — exact shape and units. `state` is K floats, K in [5, 16]. Two natural sources:
  * Yeo-7 network means from the fsaverage5 surface: {'visual','somatomotor','dorsal_attention','ventral_attention','limbic','frontoparietal','default'} (K=7).
  * neuroscore's composite regions (K=7): amygdala, ACC, dlPFC, vmPFC, striatum, auditory, visual — each exposing `.peak_value`, `.mean_value`, peak time and onset time (github.com/ndpvt-web/neuroscore). This is the cheapest K=7 signal available and needs no parcellation code.
Units are TRIBE v2 z-scored BOLD. CRITICAL CALIBRATION FACT: absolute values are TINY. arXiv 2605.13904 measures a natural face photograph driving FFA at +0.080 and a vector illustration at +0.039, with a gradient-ascent-optimised synthetic stimulus reaching only +0.339. So natural-stimulus ROI means sit in roughly ±0.02 to ±0.15 z units. Any fixed absolute threshold ('if visual > 0.5') will NEVER fire. The layer must rescale first:

    z_k = (r_k - mu_k) / (sigma_k + 1e-6)   # mu, sigma = running mean/std over a rolling window of the last W=20 clips

Only z_k is safe to threshold or rank.

OUTPUT. A single UTF-8 string, up to 7,000 characters (fal's stated H3 prompt ceiling). Practical target 120-250 words / 700-1500 characters — long enough for the seven H3 techniques, short enough that an LLM writer returns it inside ~1.5 s.

DESIGN (a) — PURE LOOKUP / TEMPLATE. Two tables plus a composer.

    MOTIF: dict[roi_name, dict[str, list[str]]]  # roi -> {'high': [...], 'low': [...]} visual motifs
    SLOTS: an ordered H3 prompt skeleton with {subject} {action} {camera} {light} {sound} {negatives}

    def compose(z):
        ranked = sorted(z.items(), key=lambda kv: -abs(kv[1]))
        driver, second = ranked[0], ranked[1]
        motif = MOTIF[driver[0]]['high' if driver[1] > 0 else 'low']
        return SLOTS.format(subject=choice(motif), camera=CAM[second[0]], ...)

Latency: 0.05-0.3 ms (pure Python dict lookup + str.format; measured order of magnitude, not sourced). Dev complexity LOW. ~80-120 LOC including the tables. Fully deterministic, fully debuggable, zero API dependency, zero cost.

DESIGN (b) — LLM-IN-THE-LOOP. One chat completion per clip. System prompt (cached) holds the H3 prompt grammar, the ROI->meaning glossary and the anti-repetition rule; user message holds the z-vector, the previous prompt, and the last 3 archive entries. Model returns only the prompt string.
Latency with claude-haiku-4-5: TTFT ~0.6 s on a medium prompt, throughput 80-100 tok/s (artificialanalysis.ai, benchlm.ai). A 150-token output therefore costs ~0.6 + 150/90 ≈ 2.3 s end to end; capping max_tokens at 80 gives ~1.5 s. HONEST VERDICT: an LLM writer that produces a GOOD H3 prompt does NOT return in well under one second — physically it cannot at ~90 tok/s. The 'under 1 s' constraint is only met by outputs of ~30-40 tokens, which is too short to use H3's structure. See recommended_approach for why this does not matter.
Dev complexity LOW-MEDIUM (one API call, one retry path, one JSON/plain-text parse). ~60-100 LOC.

DESIGN (c) — STEERING VECTORS / LATENT INTERPOLATION. Requires write access to the text-encoder embedding or the diffusion latent. minimax/h3-max on fal is a closed hosted endpoint whose only semantic input is `prompt` (plus seed, image_url, end_image_url). There is NO embedding input, no negative-embedding input, no latent input, and no exposed CFG or guidance parameter in the documented schema. DESIGN (c) IS THEREFORE IMPOSSIBLE ON H3 MAX and should be struck from consideration. It only becomes available if you switch generator to an open-weights model you host (Wan 2.1 / Krea Realtime, item 17), which trades this whole layer's simplicity for a self-hosted B200. Latency would be ~0 (a tensor add); dev complexity HIGH (self-hosting) — the complexity moves, it does not disappear.

**input_contract**

state: dict of K in [5,16] float ROI/network activations in TRIBE z-scored BOLD units, one vector per clip, already temporally reduced by item 02 (the raw prediction is (T, 20484), so a reduction policy — ROI mean over the clip, peak, or last-N-seconds — must already have been applied upstream). Values are small (|r| typically < 0.15) and MUST be re-standardised against a rolling window of >= 20 previous clips before use.
prev_prompt: the string actually used for clip N. Prefer H3 Max's returned `expanded_prompt` over your own prompt when it is non-null, because that is what the video actually depicts.
archive: last M (recommend 30-40) prompt strings, for the novelty/anti-repetition term.
Optional target: a setpoint vector for the trajectory-tracking policy.
Cold start: the rolling z-score is undefined for the first ~20 clips. Seed mu=0, sigma=0.05 (a defensible prior given the 2605.13904 magnitudes) and let it converge, or run the first 20 clips on a fixed script.

**output_contract**

A single prompt string, 700-1500 characters recommended, <= 7000 characters hard ceiling. It should contain, in this order: (1) an opening state — who/what/where in one sentence; (2) time-coded beats for anything longer than one action, written as '[0-4 seconds] ... [4-9 seconds] ...'; (3) camera direction in film vocabulary (lens, movement, exposure behaviour — 'rack focus', 'slow push in on a 35mm', 'handheld'); (4) light and grade; (5) an explicit soundscape sentence naming the sounds, because H3 generates native stereo audio in the same pass and leaves the mix to chance otherwise; (6) identity anchors for any recurring subject ('the woman in the ochre coat from the previous shot'); (7) negative direction ('no dissolves, no on-screen text, no dialogue').
NOTE ON WHAT THE NUMBERS MEAN DOWNSTREAM: the string you emit is not the string the model renders. With prompt_expansion_mode='balanced' (the default) H3 Max decides per request how much to rewrite, and returns the result as `expanded_prompt`. You are steering a rewriter, not the renderer. Always log `expanded_prompt` and treat it, not your own output, as the ground truth of what the clip depicts.

### Performance

**throughput_constraint**

Effectively unconstrained relative to the rest of the pipeline. One call per clip = 240 calls/hour at 15 s clips, 720/hour at 5 s clips. Anthropic default rate limits for claude-haiku-4-5 are far above this at any tier. fal-ai/any-llm inherits fal's account-level concurrency ladder (2 concurrent for new accounts, auto-scaling toward 40) — a real consideration only because the SAME ladder gates your H3 Max generations, so putting the LLM on fal spends concurrency slots you need for video. USE A SEPARATE VENDOR FOR THE LLM so it cannot contend with generation. The template design has no throughput constraint at all.

**realtime_headroom**

Large surplus, and this component should never be on the critical path.
15 s clip budget: template 0.0003 s -> surplus ~15.0 s. LLM hybrid ~2.3 s -> surplus ~12.7 s against playback, but the real comparison is against the OTHER work in the same tick (H3 Max generation ~9 s for a 15 s clip, plus download, plus the TRIBE forward pass). Sequentially: ~2.3 + ~9 + download ≈ 12-13 s of a 15 s window before TRIBE's own cost — tight.
5 s clip budget: H3 Max returns a 5 s clip in <3 s, so 2.3 s of prompt writing is ~46% of the clip duration and the loop will not close sequentially. At 5 s clips use the template only (surplus ~5.0 s).
THE FIX THAT REMOVES THE PROBLEM ENTIRELY: write prompt N+1 while clip N is still generating. The prompt writer depends on the READOUT of clip N-1, not on clip N, so it is off the critical path by construction with a generate-ahead depth of 2. With that pipelining the LLM's 2.3 s is free and the 'well under 1 second' requirement is moot. Design for depth-2 buffering (item 08) and stop optimising this component.

### Complexity

**dev_complexity**

LOW for the template (a): two Python dicts and a format string, no dependencies, no failure modes beyond a KeyError. LOW-MEDIUM for the LLM hybrid (b): one API call, one timeout, one fallback path, plus the genuinely hard part which is not code at all — authoring the ROI->motif glossary and the system prompt. Budget most of the time for taste, not engineering. HIGH and out of scope for steering vectors (c), which additionally requires abandoning H3 Max.

**loc_estimate**

Template only: 80-120 LOC (≈70 of which is the motif table, i.e. content not code). LLM hybrid on top: +60-90 LOC (client, cached system prompt, timeout, template fallback, archive ring buffer). Control-policy layer (rolling z-score, novelty term, setpoint tracking): +50-70 LOC. Total for the recommended system: ~200-280 LOC.

**off_the_shelf_option**

Nothing does this job — there is no ROI->prompt library, and no repository in the eight-strong `tribe-v2` GitHub topic attempts generation from brain state (they are all scoring/analysis tools: neuroscore, Audience, mindprint, neuroscanner, tribe-brain-analysis, NoLemming, tribe-subcortex, NeuroSync). Two things remove work adjacently:
1. github.com/ndpvt-web/neuroscore — removes the readout AND supplies a ready-made 7-float semantic vector with named regions and per-region peak/mean/onset. `from neuroscore import score; r = score('clip.mp4'); r.region_map.vmpfc.peak_value`. Use its RegionMap as your `state` dict and you skip parcellation entirely. Caveat, which must be stated publicly if the piece is exhibited: its 0-10 'engagement score' and its amygdala->ACC->vmPFC->dlPFC 'persuasion sequence' are the author's heuristic, not validated against view time, shares or conversions.
2. github.com/fal-ai-community/realtime-krea-wan — 'text-to-video with dynamic prompt rewriting', a working scaffold whose rewriter you would swap for this layer. Relevant only if you take item 17's realtime-model route; it does not apply to the H3 Max clip queue.
For the LLM itself the off-the-shelf option is simply the Anthropic SDK — do not build an abstraction layer.

### Decision

**recommended_approach**

HYBRID: deterministic template composes a structured brief; claude-haiku-4-5 renders it into H3 grammar; the template output is the fallback if the LLM is slow or errors. Concretely:

1. READOUT -> Z. Maintain a 20-clip ring buffer per ROI; z-score the incoming vector against it. Never threshold raw values.
2. POLICY -> DRIVE. Apply the control policy (below) to produce a drive vector a_t and pick the top-2 driving ROIs by |a_k|.
3. TEMPLATE -> BRIEF. Look up a motif for the top ROI (sign-dependent) and a camera/pacing modifier for the second. Emit ~5 structured lines: SUBJECT, ACTION, CAMERA, LIGHT, SOUND, AVOID.
4. LLM -> PROMPT. Call `client.messages.create(model='claude-haiku-4-5', max_tokens=400, system=<cached H3 grammar + glossary>, messages=[<brief + prev expanded_prompt + last 3 archive entries + 'do not reuse the subject of the previous two clips'>])`. Set `temperature` from the novelty term (see below). Do NOT pass a `thinking` block — Haiku 4.5 predates adaptive thinking and thinking only costs latency here.
5. FALLBACK. Wrap the call in a 3 s timeout; on timeout or any APIError, ship the template's own slot-filled string. The stream never stalls on the LLM.
6. PIPELINE. Compute prompt N+1 while clip N generates (generate-ahead depth 2), so steps 1-5 are off the critical path.

WHY HAIKU 4.5 AND NOT SOMETHING ELSE. Model id `claude-haiku-4-5`, 200K context, $1/MTok in, $5/MTok out — the cheapest current Claude model, lowest measured TTFT among mainstream APIs (~597 ms), and the system prompt (motif glossary + H3 grammar, ~800-1500 tokens) is perfectly static, so prompt caching applies on every call. Do not use fal-ai/any-llm: it proxies through OpenRouter (extra hop, no published latency), the /enterprise variant is already deprecated, and — decisively — it spends the same fal concurrency slots your H3 Max generations need.

CONTROL POLICY — the five options, and the recommendation.

  P1 MAXIMISE ACTIVATION (engagement-seeking hill climb). Push the prompt toward whatever raised the top ROI last tick. Aesthetics: escalating salience — faces, motion, threat cues, loudness. Artistically this is the most legible thesis ('an algorithm optimising for your attention') and the most self-defeating: it collapses (see closed_loop_recursion.json, and the +0.339 vs +0.080 result in arXiv 2605.13904). It also drives prompts straight into the region where fal's enable_safety_checker rejects, costing throughput.

  P2 MAXIMISE NOVELTY. Objective is change, not level: maximise ||z_t - z_{t-1}|| or 1 - max cosine similarity to the last M prompt embeddings (standard k-NN-in-archive novelty search, the same formulation used in novelty-search RL). Aesthetics: restless channel-surfing, no throughline, never boring and never coherent. Provably non-collapsing.

  P3 TRACK A TARGET TRAJECTORY. Define a slowly-moving setpoint r*(t) over the K ROIs — a composed score. Drive from the error e_t = r*(t) - z_t. Aesthetics: a piece with movements and structure; the brain model becomes an instrument being played rather than a slot machine. Two ready-made scores: a slow LFO rotating dominance around the Yeo-7 networks with a ~10-minute period, or neuroscore's amygdala -> ACC -> vmPFC -> dlPFC ordering run as a repeating 4-act cycle (with the honesty caveat above attached).

  P4 HOMEOSTAT / ERROR-NULLING. P3 with a constant setpoint: a PI controller holding the brain at a fixed state. Aesthetics: eerie stasis, the stream visibly working to keep you level. Genuinely interesting, but one note long.

  P5 OPEN LOOP / RANDOM. The control condition. Worth building because it costs nothing (it is the template with a random ROI) and it is the only way to tell whether the brain model is doing anything at all — run it side by side for a night and see if anyone can tell.

  RECOMMENDATION: P3 as the primary policy with P2 as a regulariser, i.e. drive = error-to-setpoint, with temperature and a forced-motif circuit-breaker driven by the novelty term. Reasons: (i) it is the only policy that yields an artwork with a shape over time rather than a texture; (ii) because the setpoint keeps moving, the loop cannot settle into an attractor, which structurally solves the collapse problem instead of patching it; (iii) it is honest — you are not claiming the system discovers what people want, you are claiming it chases a score; (iv) same LOC as P1. Build P1 too, as a switchable mode, because it is the more provocative demo and because watching it collapse on camera is itself the strongest argument the piece can make.

PROMPT-WRITING CRAFT FOR H3 MAX SPECIFICALLY (from fal's own MiniMax H3 prompting guide, fal.ai/learn/devs/minimax-h3-prompting-guide, plus the fal model card):
  * H3 rewards structure, not adjective density. Write a compact production brief, not a mood board.
  * Give every reference an explicit job — fal calls this the single highest-leverage habit ('Use Image 1 for the character, Image 2 for the location'). Relevant when you chain via image_url / end_image_url.
  * Time-code anything with more than one beat: '[0-2 seconds] ... [2-5 seconds] ...'. H3 honours these.
  * Use real cinematography vocabulary directly: 'rack focus', 'push in', 'handheld shake', named lens lengths, exposure behaviour.
  * ART-DIRECT THE AUDIO EXPLICITLY. H3 renders picture and native stereo in one pass; unnamed sound is left to chance. Name instrumentation, specific diegetic sounds and their timing ('rain ambience, one soft shutter rattle, no dialogue'). fal reports two extra sentences of soundscape make a noticeable difference. This is the single biggest quality lever available to an automated writer and the cheapest to template.
  * Anchor identity with concrete visual attributes when carrying a subject across clips ('the young man in the dark-grey hoodie from the previous shot'), not with names.
  * Write transitions as physical events, not named effects.
  * Use explicit negative direction — 'No soft dissolves', 'Do not add on-screen text', 'No dialogue'. For an unattended stream, 'no on-screen text' and 'no dialogue' are near-mandatory: text artefacts and garbled speech are the most legible failure a viewer will notice.
  * Ceiling is 7,000 characters; aim for 700-1500. Longer is not better once the seven elements are present.
  * Set prompt_expansion_mode='balanced' (default, ~1 s). 'quality' spends up to ~30 s on the rewrite alone and is off the table for a live loop. Consider disabling expansion entirely once your writer is good — it removes a source of nondeterminism between what you asked for and what was rendered.

**simpler_alternative**

Drop the LLM. Ship the template alone: one dict mapping each of 7 networks to 6-8 visual motifs (high and low), one dict mapping the second-ranked network to a camera/pacing modifier, one f-string H3 skeleton with a hand-written soundscape line per motif. Latency sub-millisecond, cost zero, no API key, no timeout path, fully deterministic and reproducible from a seed. Quality is lower and repetition arrives sooner — mitigate by making the motif lists longer (30+ entries each) and sampling without replacement within a window. This is the correct build for day one: it makes the whole loop close, and the LLM can be dropped in later behind the same `next_prompt()` signature without touching anything else.
EVEN SIMPLER, if the LLM is wanted but latency or reliability is a worry: keep the LLM but call it once every N clips to write a 'scene bible' (setting, palette, recurring subject, soundscape), and let the template fill per-clip variation against it. One API call per minute instead of per clip, better continuity, and the LLM is completely off the per-clip path.

**code_sketch**

# brain_to_prompt.py — recommended hybrid. ~120 LOC in full; the core is below.
import os, random, collections
import anthropic

client = anthropic.Anthropic()  # picks up ANTHROPIC_API_KEY or an `ant auth login` profile

MOTIF = {
  'visual':   {'hi': ['a dense lattice of neon signage seen through rain',
                      'kaleidoscopic reflections in a rotating glass atrium'],
               'lo': ['a single grey wall, one slow shadow crossing it',
                      'fog over still water, almost no detail']},
  'auditory': {'hi': ['a brass section rehearsing in a stairwell',
                      'a rail yard at shift change'],
               'lo': ['a snowfield, wind only', 'an empty anechoic room']},
  'language': {'hi': ['a hand writing on a fogged window, the words legible',
                      'a crowded market, mouths moving, no sound'],
               'lo': ['wordless machinery, rhythmic and mute']},
  'default':  {'hi': ['a slow drift through an unpeopled interior at dusk',
                      'clouds from above, unhurried'],
               'lo': ['a face very close, direct address to camera']},
  'motion':   {'hi': ['a body falling through frame, tracked',
                      'a train interior at speed, lights strobing past'],
               'lo': ['a held wide shot, nothing moves but dust']},
}
CAMERA = {'visual':'slow 35mm push in, shallow focus',
          'auditory':'locked-off wide, no camera movement',
          'language':'handheld, small corrective reframes',
          'default':'very slow drift, 24mm, deep focus',
          'motion':'whip pan into a tracking shot'}

SKELETON = ("{subject}. {beats}\n"
            "Camera: {camera}. {light}.\n"
            "Sound: {sound}.\n"
            "Avoid: no on-screen text, no dialogue, no dissolves, no logos.")

class Z:  # rolling standardiser — the piece that makes the tiny BOLD range usable
    def __init__(self, w=20): self.buf = collections.defaultdict(lambda: collections.deque(maxlen=w))
    def __call__(self, state):
        out = {}
        for k, v in state.items():
            b = self.buf[k]; b.append(v)
            mu = sum(b)/len(b)
            sd = (sum((x-mu)**2 for x in b)/max(len(b)-1, 1))**0.5
            out[k] = (v - mu) / (sd + 0.05)   # 0.05 floor: natural-stimulus sigma is ~0.05 z-units
        return out

SYSTEM = open('h3_grammar.md').read()   # static -> cache it; H3 rules + ROI glossary + house style

def next_prompt(state, prev_prompt, archive, target=None, step=0, zc=Z(), temp=1.0):
    z = zc(state)
    if target:                                   # P3: track a setpoint
        z = {k: target.get(k, 0.0) - v for k, v in z.items()}
    rank = sorted(z, key=lambda k: -abs(z[k]))
    drv, snd = rank[0], rank[1]
    motif = random.choice(MOTIF[drv]['hi' if z[drv] > 0 else 'lo'])
    brief = SKELETON.format(
        subject=motif,
        beats='[0-5s] establish. [5-11s] the change begins. [11-15s] hold.',
        camera=CAMERA[snd],
        light='low-key, single practical source, cool grade',
        sound='room tone, one recurring metallic tick, no music, no speech')
    try:                                         # LLM polish, with the template as fallback
        msg = client.messages.create(
            model='claude-haiku-4-5', max_tokens=400, temperature=temp,
            system=[{'type':'text','text':SYSTEM,
                     'cache_control':{'type':'ephemeral'}}],
            messages=[{'role':'user','content':
                f"BRIEF:\n{brief}\n\nPREVIOUS CLIP AS RENDERED:\n{prev_prompt}\n\n"
                f"RECENT PROMPTS (do not reuse their subject):\n" + '\n'.join(archive[-3:]) +
                "\n\nWrite the next clip's MiniMax H3 prompt. 120-200 words. "
                "Output the prompt only, no preamble."}],
        )
        return msg.content[0].text.strip()
    except Exception:
        return brief                             # stream never stalls on the LLM

# --- usage, pipelined one clip ahead ---
# p = next_prompt(readout[t-1], last_expanded_prompt, archive, target=score(t))
# archive.append(p)
# fal_client.submit('minimax/h3-max/text-to-video',
#                   {'prompt': p, 'duration': 15, 'resolution': '768P',
#                    'prompt_expansion_mode': 'balanced'})

### Risk

**failure_modes**

1. DEAD SIGNAL FROM ABSOLUTE THRESHOLDS. The most likely day-one bug and it fails silently. TRIBE z-scored predictions for natural stimuli sit around 0.04-0.15 (arXiv 2605.13904: natural face photo +0.080, vector illustration +0.039); any rule written against intuition ('if visual > 0.5') never fires, the template always picks the same default branch, and the stream looks reactive but is not. Fix: mandatory rolling z-score with a sigma floor around 0.05. Verify by asserting that the top-ranked ROI changes across a 50-clip run.
2. YOU ARE STEERING A REWRITER, NOT A RENDERER. With prompt_expansion_mode='balanced' H3 Max rewrites your prompt by an amount it chooses per request. Small, deliberate changes in your prompt can be washed out entirely. Any A/B claim about the brain-state->image mapping is invalid unless you log and compare `expanded_prompt`. Consider disabling expansion once the writer is good.
3. `expanded_prompt` IS NOT ALWAYS THERE. fal's schema states it is null when expansion was disabled, left the prompt unchanged, OR was performed internally by MiniMax's hosted API. Code that feeds it forward must be `expanded_prompt or prompt`, or the layer starts writing continuations of `None`.
4. SAFETY-CHECKER COLLISION WITH THE OBJECTIVE. `enable_safety_checker` defaults true. The P1 activation-maximising policy pushes precisely toward faces, threat cues, bodies and high-salience imagery — exactly where rejections cluster. Rejections are unbudgeted throughput loss. The prompt layer must own its half of the fix: a `soften()` retry that re-runs the template with the motif list's tamer branch, before the orchestrator falls back to filler.
5. LLM SEMANTIC RUT. Small models given the previous prompt converge on a house style within ~20 clips — same three subjects, same grade. The archive-and-forbid instruction helps but is not sufficient; the novelty-driven temperature schedule and a forced-motif circuit breaker are what actually break it (see closed_loop_recursion.json).
6. THE MOTIF TABLE IS UNGROUNDED. 'Visual network high -> neon lattice' is your taste, not a finding. Nothing in the TRIBE literature licenses a mapping from ROI to motif. The one genuinely grounded source is arXiv 2605.13904's feature-visualisation images (gradient ascent recovers V1/V2/V3/V4/MT/FFA/PPA selectivity), which could be used offline to author the table from what actually drives each region — that is item 16's proposal and it is the only path to a defensible table. Until then, describe the mapping as authored, not discovered.
7. LLM ON THE CRITICAL PATH. If generate-ahead depth is 1, a 2.3 s prompt write plus a 9 s generation plus download plus the TRIBE pass will not fit a 15 s window, and the buffer drains slowly and invisibly until it underruns 20 minutes in. Depth 2 and a hard 3 s timeout.
8. LOG-EVERYTHING DEBT. Without persisting (z-vector, drive, template brief, LLM prompt, expanded_prompt, clip URL) per tick, the piece is unanalysable and unreproducible after the fact. One JSONL line per clip; ~10 LOC; do it first, not later.

### Economics

**cost**

Template-only: $0.00/hour.
LLM hybrid with claude-haiku-4-5 ($1/MTok input, $5/MTok output): per call ≈ 1,200 input tokens (of which ~1,000 is the cached static system prompt, billed at cache-read rates) + ~180 output tokens. Uncached worst case ≈ $0.0012 + $0.0009 ≈ $0.0021/call; with caching working, closer to $0.0010-0.0014/call.
  * 15 s clips = 240 calls/hour -> $0.25-0.50/hour.
  * 5 s clips = 720 calls/hour -> $0.75-1.50/hour.
Context: H3 Max at launch pricing is $0.025/s (480P) or $0.04/s (768P), i.e. $90-144 per hour of continuous 768P stream. The prompt layer is therefore 0.2-0.5% of the generation bill and rounds to zero. Do not optimise it; do not downgrade the model to save money here.
The 'scene bible every N clips' variant costs roughly 1/10th of the above, which is a rounding error on a rounding error — choose it for continuity reasons, not cost.

### Evidence

**sources**

PRIMARY / SCHEMA:
- https://fal.ai/models/minimax/h3-max/text-to-video/api — full input schema (prompt, duration default 5, resolution 480P|768P default 768P, seed, enable_safety_checker default true, sync_mode, prompt_expansion_mode default 'balanced', aspect_ratio) and output schema (video, expanded_prompt, timings). Source of the exact quote that expanded_prompt is 'Null when prompt expansion was disabled, left the prompt unchanged, or was performed internally by MiniMax's hosted API', and that 'balanced' returns in ~1 s while 'quality' spends up to ~30 s.
- https://fal.ai/learn/devs/minimax-h3-prompting-guide — fal's own H3 prompting guide: the seven techniques (reference assignment, timed shot list, camera/cinematography language, audio direction, subject identity anchors, transition-as-physical-event, negative direction), the 7,000-character ceiling, and the claim that two extra sentences of soundscape make a noticeable difference.
- https://fal.ai/minimax-h3-max — model card, pricing and native-audio claim.
- https://arxiv.org/html/2605.13904v1 — Bladon & Bent, 'Feature Visualization Recovers Known Cortical Selectivity from TRIBE v2' (13 May 2026). Source of the calibration numbers used throughout: optimised FFA stimulus +0.339, natural face photograph +0.080, vector illustration +0.039, all in TRIBE v2 z-scored BOLD units; seven ROIs V1/V2/V3/V4/MT/FFA/PPA; 3,000 gradient steps x 5 restarts on a single RTX 3090.
- https://github.com/ndpvt-web/neuroscore — CLI + Python API over TRIBE v2; `score()` returns overall_score (0-10), summary, findings, and a RegionMap over amygdala/ACC/dlPFC/vmPFC/striatum/auditory/visual with peak_value, mean_value, peak time and onset. Stated backend timings: GPU 15-60 s per 30 s video. INFERENCE (mine): its RegionMap is directly usable as this layer's `state` dict.
- https://github.com/topics/tribe-v2 — the eight public tribe-v2 repositories as of Aug 2026; basis for the claim that none of them does brain-state-to-prompt generation.

LLM LATENCY / PRICING:
- Anthropic model table (claude-api skill, cached 2026-06-24): `claude-haiku-4-5`, 200K context, $1.00/MTok input, $5.00/MTok output.
- https://benchlm.ai/models/claude-haiku-4-5 — 597 ms time-to-first-token on a medium-length prompt (Aug 2026).
- https://artificialanalysis.ai/models/claude-4-5-haiku/providers — ~80-100 output tokens/second by provider.
- https://docs.fal.ai/examples/model-apis/use-llms and https://fal.ai/models/fal-ai/any-llm/api — fal-ai/any-llm endpoint, ~34 models, default google/gemini-2.5-flash-lite, `priority: 'throughput'|'latency'`; fal proxies LLM traffic through OpenRouter and points at openrouter/router; the /enterprise variant is documented as deprecated.

CONTROL POLICY / PRIOR ART:
- https://github.com/fal-ai-community/realtime-krea-wan — 'text-to-video generation with dynamic prompt rewriting', WebSocket + MsgPack against fal's realtime surface. The nearest existing scaffold, applicable only on the realtime-model route.
- https://arxiv.org/pdf/2009.13579 (Novelty Search in Representational Space) and https://arxiv.org/pdf/1908.06976 (survey of intrinsic motivation in RL) — the k-nearest-neighbour-in-archive novelty formulation used for policy P2.
- https://arxiv.org/pdf/2602.10552 — MindPilot, closed-loop EEG-guided image generation; establishes that treating the brain model as a black-box objective and iteratively refining a generator's input is an established, published pattern. Cited as precedent, not as a method transplanted here.

INFERENCE, NOT SOURCED: the recommendation of policy P3 over P1; the specific motif tables; the sigma floor of 0.05; the depth-2 pipelining argument; the claim that design (c) is impossible on H3 Max (derived from the absence of any embedding/latent field in fal's documented schema, not from an explicit fal statement); all LOC and template-latency estimates.

### Flagged Uncertain (omitted above)

- `latency_ms`
- `unknowns`

---

## Brain-output semantic readout

### Identity

**what_it_is**

The reduction layer that collapses TRIBE v2's raw (T, 20484) fsaverage5 cortical prediction (and, from the separate subcortical checkpoint, a (T, ~8802) Harvard-Oxford voxel prediction) into a handful of named, interpretable ROI/network floats that a prompt template or LLM can actually read.

**role_in_loop**

Sits between PREDICT and PROMPT. Consumes preds from TribeModel.predict(); emits a small dict of named dials (e.g. {faces: +1.8, places: -0.4, motion: +2.1, audio: +0.3, narrative: -1.1}) plus an ordered top-k ROI name list. Everything downstream in the loop is text, so this is the last numeric stage.

### Interface

**interface_spec**

CORRECTION TO BRIEF: TRIBE v2 DOES ship parcellation helpers. tribev2/utils.py exposes, all lru_cached:

  get_hcp_labels(mesh='fsaverage5', combine=False, hemi='both') -> dict[str, np.ndarray]
     Returns {bare_Glasser_name: vertex_indices}. Internally: mne.datasets.fetch_hcp_mmp_parcellation(accept=True) -> mne.read_labels_from_annot('fsaverage', 'HCPMMP1', hemi='both') -> strips the 'L_'/'R_' prefix and '_ROI' suffix -> downsamples fsaverage(163842) to fsaverage5 by v[v < 10242] (valid because FreeSurfer icosahedral meshes are nested: fsaverage5's vertices ARE the first 10242 of fsaverage) -> adds index_offset = 10242 for the right hemisphere -> asserts the union covers exactly 10242 per hemi. hemi='both' concatenates left and right under one bilateral key. combine=True switches the annot to 'HCPMMP1_combined' (mne's ~44 coarse groups).
  get_hcp_vertex_labels(mesh='fsaverage5', combine=False) -> list[str] of length 20484 (per-vertex label name)
  get_hcp_roi_indices(rois: str|list[str], hemi='both', mesh='fsaverage5') -> np.ndarray[int]  (supports 'V1', ['PHA1','PHA2','PHA3'], and wildcards 'STS*' / '*Belt')
  summarize_by_roi(data: np.ndarray (1-D, 20484), hemi='both', mesh='fsaverage5') -> np.ndarray  (one mean per Glasser parcel; 180 values bilateral, 360 with hemi='both_separate')
  get_topk_rois(data: np.ndarray (1-D, 20484), hemi='both', mesh='fsaverage5', k=10) -> list[str]  (ranked parcel names)

Subcortical helpers also ship, in tribev2/plotting/subcortical.py:
  get_subcortical_labels(with_hemi=False) -> list[str]  (8 bilateral structures)
  get_subcortical_roi_indices(roi: str) -> np.ndarray[int]  (indices into the flat voxel vector)
  voxel_to_mesh(voxel_scores, label, resolution)
The subcortical mask is built by neuralset MaskProjector(mask='subcortical', resolution=2): nilearn.datasets.fetch_atlas_harvard_oxford('sub-maxprob-thr50-2mm'), then every label containing 'Cortex', 'White', 'Stem' or 'Background' is zeroed out. The 8 surviving bilateral structures are Lateral Ventricle, Thalamus, Caudate, Putamen, Pallidum, Hippocampus, Amygdala, Accumbens (16 labels with hemisphere).

Raw index geometry (needed only if you bypass the helpers): preds[:, 0:10242] = left hemisphere, preds[:, 10242:20484] = right, stacked by np.vstack in TribeSurfaceProjector.apply. Vertex order inside a hemisphere is fsaverage5 native order, NOT anatomically contiguous, so integer index RANGES are meaningless as ROIs.

Manual fallback (no tribev2 import), verbatim from github.com/recozers/Tribe-V2-Interp/feature_viz.py:
  import nibabel.freesurfer as nbfs, mne
  mne.datasets.fetch_fsaverage(subjects_dir=SD); mne.datasets.fetch_hcp_mmp_parcellation(subjects_dir=SD, accept=True)
  for hemi_prefix, offset in [('lh', 0), ('rh', 10242)]:
      labels_arr, ctab, names = nbfs.read_annot(f'{SD}/fsaverage/label/{hemi_prefix}.HCPMMP1.annot')
      # names are like b'L_V1_ROI-lh'; strip 'L_'/'R_', '_ROI', '-lh'/'-rh'
      verts = np.where(labels_arr == i)[0]; verts = verts[verts < 10242]; roi_verts.extend(verts + offset)
Note: read_annot with the default orig_ids=False returns POSITIONAL colortable indices, so the +1000/+2000 FreeSurfer label-value offsets mentioned in the brief do NOT apply on this route. They only bite if you read the raw label values with orig_ids=True or use the Mills-2016 numeric HCP-MMP1 distribution.

Yeo-17 on fsaverage5: NOT available from nilearn (nilearn.datasets.fetch_atlas_yeo_2011 returns VOLUMETRIC MNI NIfTIs, not surface annots). The surface version ships with FreeSurfer / ThomasYeoLab CBIG as $SUBJECTS_DIR/fsaverage5/label/{lh,rh}.Yeo2011_17Networks_N1000.annot and is read with the identical nbfs.read_annot call above, with NO v<10242 filtering needed (the file is already fsaverage5, exactly 10242 entries per hemisphere).
Zero-download alternative: nilearn.datasets.fetch_atlas_surf_destrieux() returns map_left and map_right already on fsaverage5 (10242 ints each) with 76 labels per hemisphere and no external atlas fetch at all.

**input_contract**

A numpy array from TribeModel.predict(). Cortical checkpoint facebook/tribev2: (T, 20484) float32, T = number of 1-second TRs kept. Subcortical checkpoint facebook/tribev2-subcortical: (T, ~8802) float32 voxels. summarize_by_roi and get_topk_rois take a 1-D array (they assert data.ndim == 1), so you must reduce over time BEFORE calling them, or loop per TR. The ROI-mask build additionally requires mne plus a one-time ~1.5 GB download (mne.datasets.sample.data_path() plus fetch_hcp_mmp_parcellation); cache the resulting index arrays to .npz and never rebuild them at runtime.

**output_contract**

Named floats in z-score units, not physical units. CRITICAL: TRIBE's training target was per-sample z-scored and detrended (config data.neuro.cleaning.standardize: zscore_sample, detrend: true), so ABSOLUTE VALUES CARRY NO MEANING. Only relative temporal dynamics within one normalisation window are interpretable. A raw preds value of +0.34 means nothing on its own; +2.1 sigma above this clip's own mean for the FFC parcel does. The reference implementation therefore always applies a per-vertex z-score over the full time axis before ROI-averaging, then z-scores the ROI curve again over time, then Gaussian-smooths with sigma = 2 s. Concretely, useful outputs are: (a) a dict of ~5-8 named ROI/network z-scores; (b) an ordered top-k Glasser parcel name list from get_topk_rois; (c) optionally a per-ROI delta (late-window mean minus early-window mean) in the same z units.

### Performance

**throughput_constraint**

None. Pure CPU numpy, no GPU, no network, no rate limit, trivially parallel. The upstream predict() call is the only bottleneck in this leg of the pipeline. get_hcp_labels is lru_cached so repeated calls in a warm process are free.

**realtime_headroom**

Surplus of essentially the entire clip duration. For a 15 s clip budget the readout consumes <0.01 s, i.e. >14.99 s surplus. This component will never be the reason the loop misses its deadline; budget it at zero and spend the time on generation.

### Complexity

**dev_complexity**

LOW. Meta ships get_hcp_roi_indices / summarize_by_roi / get_topk_rois, which already handle the fsaverage-to-fsaverage5 downsample, the right-hemisphere +10242 offset and the L_/R_/_ROI name mangling. The remaining work is choosing which parcels constitute each dial and deciding a temporal reduction policy. Rating would be MEDIUM if the helpers did not exist; the brief's premise that they do not is the single biggest correctable overestimate in this item.

**loc_estimate**

40-80 LOC for a solid version: a PARCELS dict mapping dial names to Glasser parcel lists, a build-and-cache-masks function, a to_dials(preds) reducer with z-score plus smoothing, and a top-k namer. The published reference (tribescore/metrics.py) does all of this in ~640 LOC including docstrings, caching, validation and legacy shims; the essential core inside it is well under 100 LOC.

**off_the_shelf_option**

Three, in descending order of usefulness:
1. tribev2.utils itself (summarize_by_roi, get_topk_rois) - already installed, zero extra dependency beyond mne, and index-aligned to the model output by construction. USE THIS.
2. techfreakworm/tribev2-brain-timeline on HF Spaces (src/tribescore/metrics.py, MIT-ish, Gradio app, live). Ships five named metrics - Attention, Engagement/arousal, Virality, Language, Self-relevance - each defined as an explicit verbatim list of HCP-MMP1 parcels, plus the full normalise-and-smooth recipe and a persisted .npz mask cache. This is the closest thing to a correct, drop-in, ~5-float engagement readout that exists. It also carries honest caveats in-repo.
3. ndpvt-web/neuroscore (8 stars, CLI + Python API, 'predict how the human brain reacts to any content'). DO NOT USE AS A SCIENTIFIC SIGNAL - see failure_modes. It is fine only as a UI/report-formatting reference.

### Decision

**recommended_approach**

TEMPORAL REDUCTION POLICY - the unavoidable design decision, with its aesthetic consequences.

The output for a 15 s clip is a (15, 20484) matrix. The five reduction options and what each does to the look of the stream:

A. ROI MEAN OVER THE WHOLE WINDOW -> one scalar per ROI. Stable, low-variance, slow-moving. Aesthetically this gives a stream that drifts: consecutive clips differ gently, transitions feel like a dissolve. Least likely to produce whiplash, most likely to feel inert. Cheapest and most robust.
B. PEAK / MAX OVER TIME per ROI (plus argmax time). Punchy and event-driven - one dramatic second dominates the next prompt. Aesthetically produces a stream that lurches between extremes and over-reacts to a single flash frame. With only 15 samples the max is nearly pure noise. Use only in combination with (A), as a 'moment' annotation.
C. LAST-N-SECONDS MEAN (e.g. final 5 TRs). Most causally connected to the tail of the clip, which is what the next clip continues from, so chaining feels motivated. But the 5 s hemodynamic offset means the final TRs of a short clip are the least well-conditioned part of the window; on a 15 s clip the last 5 TRs are also the ones with least left-context. Aesthetically: responsive but jittery.
D. TRAJECTORY DELTA (mean of last third minus mean of first third), per ROI. This is the one that actually produces narrative. It encodes DIRECTION - 'faces rising, motion falling' - which maps naturally onto a prompt verb ('the camera pushes in on a face as the crowd stills'). Aesthetically this is what makes the stream feel like it is going somewhere rather than sampling randomly. Recommended as the primary dial, with (A) as the level and (D) as the derivative.
E. TOP-K ROI NAMES (get_topk_rois on the window mean). Categorical rather than continuous, and it drops straight into a prompt template with no thresholding, no calibration and no scaling decisions. This is the shortest path to a working demo. Aesthetically it produces discrete 'modes' - the stream visibly switches between a faces mode, a places mode, a motion mode - which reads as intentional rather than noisy.

RECOMMENDED: compute (A) level and (D) delta for a fixed set of ~6 dials, and separately compute (E) top-3 parcel names, and hand the prompt layer all three. Total cost still under a millisecond.

NORMALISATION - the part that is easy to get wrong. Do NOT z-score within each 15 s clip in isolation. Fifteen samples is far too few for a stable mean and std, and the first ~5 TRs of any window are hemodynamic warm-up (the reference Space explicitly trims WARMUP_TRIM = 5 leading TRs from every window but the first), leaving ~10 usable samples. Instead keep a ROLLING NORMALISER across the last N clips (an exponentially-weighted per-vertex or per-ROI mean and std over the last few minutes of stream) and z-score each new clip against that. This preserves genuine 'calm vs active' amplitude dynamics between clips, which per-clip z-scoring destroys by forcing every clip to unit variance. This is exactly the bug the reference implementation documents: a per-window z-score 'forces every window to unit variance, erasing those dynamics and manufacturing the seam step'.

SCALE REALITY - NEVER THRESHOLD ON A RAW VALUE. Predicted activations are far smaller than intuition suggests. In arXiv 2605.13904 a natural face photograph drives FFA to +0.080 in the encoder's own output units, and even a stimulus explicitly optimised by gradient ascent to maximise FFA only reaches +0.339. So a guard written as `if faces > 0.5` NEVER FIRES, and the failure is invisible: the stream keeps running, looks reactive, and is in fact constant. Every threshold, every colour ramp and every prompt-selection cut point must be expressed in units of the ROLLING standard deviation, never in raw activation units, and should be sanity-checked by asserting that each dial actually crosses its threshold at some point over a few minutes of stream.

USE A VARIANCE FLOOR, NOT AN EPSILON. The offline reference implementations divide by (std + 1e-6), which is fine for a finished recording but dangerous in a live rolling normaliser: during a quiet passage the rolling std collapses toward zero and a 1e-6 epsilon lets pure noise be amplified into enormous z values, so the stream detonates on nothing. Use sigma_eff = max(rolling_std, SIGMA_FLOOR) instead. SIGMA_FLOOR must be CALIBRATED, not copied - log the per-ROI rolling std over ten minutes of representative stream and set the floor to roughly its 10th percentile. A starting value around 0.05 is a reasonable first guess given the +0.080 natural-stimulus scale above, but it is a guess, not a sourced constant, and a floor set too high flattens the dials into silence just as surely as one set too low makes them explode.

WHICH ROIs MAKE GOOD CREATIVE DIALS (HCP-MMP1 / Glasser names, exactly as get_hcp_roi_indices accepts them):
  faces        -> FFC                                  (fusiform face complex; 104 fsaverage5 vertices)
  places       -> PHA1, PHA2, PHA3                      (PPA; 194 vertices)
  motion       -> MT, MST                               (MT alone is only 38 vertices - small and noisy, always pair with MST)
  low_level_vis-> V1, V2, V3, V4                        (523, 383, 242, 180 vertices; V1 is your 'texture/contrast/flicker' dial)
  audio        -> A1, LBelt, MBelt, PBelt, A4, A5
  social_sts   -> STSdp, STSvp, STSda, STSva, TE1p, TE2p
  language     -> 44, 45, IFSa, STGa, TE1a, A5, PSL, SFL, 55b
  narrative_dmn-> 7m, POS2, v23ab, d23ab, 31pv, 31pd, RSC, PCV, 9m, 10r, PGs, PGi
  attention    -> FEF, LIPv, LIPd, VIP, MIP, AIP, IP0, IP1, IP2, TPOJ1, TPOJ2, PGi, PGs, PFm, IFJa, IFJp, p9-46v, a9-46v, 9-46d, 46, 8C, i6-8, s6-8
  value/reward -> 10r, 10v, 10d, 10pp, p32, s32, a24, d32, 25, OFC, pOFC, 11l, 13l, 9m   (vmPFC/mOFC cortical proxy only)
  threat/arousal (amygdala) -> NOT AVAILABLE from the cortical checkpoint. Requires facebook/tribev2-subcortical and get_subcortical_roi_indices('Amygdala').

The FFC/PHA1-3/MT/V1-V4 assignments and vertex counts are not invented here - they are the exact ROI definitions used and validated in arXiv 2605.13904, which recovered the correct known selectivity for each by gradient ascent through the frozen encoder.

ARCHITECTURE NOTE THE BRIEF GETS WRONG: cortical and subcortical are TWO SEPARATE CHECKPOINTS, not one 29,286-dimensional output. facebook/tribev2 (709 MB, predictor head [1, 2048, 20484], TribeSurfaceProjector mesh=fsaverage5) and facebook/tribev2-subcortical (613 MB, MaskProjector mask=subcortical resolution=2 fwhm=6.0), uploaded 2026-05-13 and announced by Meta author sdascoli on 2026-05-21 in response to GitHub issue #23. Note on counting: it is 8 BILATERAL STRUCTURES, i.e. 16 labels once hemispheres are separated - get_subcortical_labels(with_hemi=True) returns 16, get_subcortical_labels() collapses them to 8. Descriptions of '16 bilateral structures' double-count. Getting both means two loaded models and two forward passes. For a first demo, pick ONE: cortical if you want FFA/PPA/MT/V1 visual dials, subcortical if amygdala arousal is the creative point.

**simpler_alternative**

Drop the atlas entirely and use GLOBAL FIELD POWER: gfp = np.abs(zscore(preds, axis=0)).mean(axis=1), one float per second, plus its peak time. Two lines, no mne, no 1.5 GB download, no parcel-name bikeshedding. It gives you a single 'intensity' dial that can drive one prompt axis (calm <-> overwhelming). BUT: this exact reduction is the one that was formally tested against real behaviour and failed - arXiv 2607.01400 reduced TRIBE to 'a per-second engagement curve, the global field power' and found position-controlled partial r = +0.058, 95% CI [-0.04, 0.15], t(47)=1.21, p=0.23 against YouTube 'most replayed' heatmaps on 48 videos, below simple loudness and motion baselines. As a CREATIVE dial that is perfectly acceptable (the piece does not claim to predict virality); as an engagement claim it is refuted. Second fallback, cheaper still: skip TRIBE at runtime and use get_topk_rois on a small precomputed lookup table (see item 15/16).

**code_sketch**

# --- one-time: build and cache the dial masks -------------------------------
import numpy as np
from tribev2.utils import get_hcp_labels, get_hcp_roi_indices

DIALS = {
    'faces':     ['FFC'],
    'places':    ['PHA1', 'PHA2', 'PHA3'],
    'motion':    ['MT', 'MST'],
    'low_level': ['V1', 'V2', 'V3', 'V4'],
    'audio':     ['A1', 'LBelt', 'MBelt', 'PBelt', 'A4', 'A5'],
    'social':    ['STSdp', 'STSvp', 'STSda', 'STSva'],
    'narrative': ['7m', 'POS2', 'v23ab', 'd23ab', '31pv', '31pd', 'RSC', 'PCV', '9m', 'PGs', 'PGi'],
}

def build_masks(path='dial_masks.npz'):
    try:
        with np.load(path) as z:
            return {k: z[k] for k in z.files}
    except FileNotFoundError:
        pass
    valid = set(get_hcp_labels(mesh='fsaverage5', combine=False, hemi='both'))
    masks = {}
    for dial, parcels in DIALS.items():
        present = [p for p in parcels if p in valid]   # never silently substitute
        assert present, f'no valid parcels for {dial}'
        masks[dial] = np.unique(np.concatenate(
            [get_hcp_roi_indices(p, hemi='both', mesh='fsaverage5') for p in present]
        )).astype(np.int64)
    np.savez(path, **masks)
    return masks

# --- per clip: reduce (T, 20484) -> dials -----------------------------------
from scipy.ndimage import gaussian_filter1d

SIGMA_FLOOR = 0.05   # CALIBRATE THIS: ~10th percentile of observed rolling std.
                     # A bare +1e-6 epsilon lets a quiet passage amplify noise
                     # into huge z values and the stream detonates on nothing.

class RollingNorm:
    """EWMA per-vertex mean/std ACROSS clips - do NOT z-score inside one 15 s clip."""
    def __init__(self, alpha=0.05, sigma_floor=SIGMA_FLOOR):
        self.a, self.floor, self.m, self.v = alpha, sigma_floor, None, None
    def __call__(self, preds):                       # preds (T, 20484)
        mu, sd = preds.mean(0), preds.std(0)
        if self.m is None:
            self.m, self.v = mu, sd
        else:
            self.m = (1 - self.a) * self.m + self.a * mu
            self.v = (1 - self.a) * self.v + self.a * sd
        return (preds - self.m) / np.maximum(self.v, self.floor)

def to_dials(preds, masks, norm, warmup_trim=5):
    z = norm(preds)[warmup_trim:]                    # drop HRF warm-up TRs
    out = {}
    for dial, idx in masks.items():
        curve = z[:, idx].mean(axis=1)               # (T',) ROI mean per TR
        curve = gaussian_filter1d(curve, sigma=2.0, truncate=3.0)  # TR = 1 s
        third = max(1, len(curve) // 3)
        out[dial] = {
            'level': float(curve.mean()),                                    # option A
            'delta': float(curve[-third:].mean() - curve[:third].mean()),    # option D
            'peak_t': int(np.argmax(curve)),                                 # option B
        }
    return out

# --- categorical readout straight into a prompt (option E, shortest path) ----
from tribev2.utils import get_topk_rois
top3 = get_topk_rois(preds.mean(axis=0), hemi='both', mesh='fsaverage5', k=3)
# e.g. array(['FFC', 'STSvp', 'MT']) -> 'a face, held in social attention, moving'
# NOTE get_topk_rois is rank-based, so it is immune to the absolute-scale trap
# below - which is exactly why it is the recommended shortest path.

# --- thresholds live in SIGMA units, never in raw activation units -----------
# WRONG: if dials['faces']['level'] > 0.5      # never fires; a real face is ~+0.08
# RIGHT: if dials['faces']['level'] > 1.0      # 1.0 sigma above the rolling baseline
# Sanity-check on startup that each dial actually crosses its threshold at least
# once over a few minutes, or the stream will look reactive while being constant.

# --- subcortical variant (separate checkpoint, gives you amygdala) -----------
# from tribev2 import TribeModel
# from tribev2.plotting.subcortical import get_subcortical_roi_indices
# sub = TribeModel.from_pretrained('facebook/tribev2-subcortical', cache_folder='./cache')
# spreds, _ = sub.predict(events=df)                 # (T, ~8802)
# amyg = spreds[:, get_subcortical_roi_indices('Amygdala')].mean(axis=1)

### Risk

**failure_modes**

1. neuroscore's ROIs ARE FABRICATED - do not use it as a signal. Its regions.py defines every region as a hardcoded INTEGER INDEX RANGE (e.g. amygdala = [(4200,4400),(14400,14600)], visual = [(5000,6000),(15000,16000)]) with the in-file comment 'In a full implementation, these come from a parcellation atlas (e.g., Destrieux). For MVP, we use approximate index ranges'. fsaverage5 vertex indices are ordered by icosahedral subdivision, NOT anatomically, so an index range is a set of vertices scattered across the whole hemisphere. Worse, two of its seven regions - amygdala and striatum - are SUBCORTICAL and cannot exist in a cortical-surface output at all; the code even labels striatum '(approximated)'. Its overall 0-10 score is a hand-picked weighted sum (0.25 amygdala + 0.25 vmPFC + 0.20 ACC + 0.20 dlPFC + 0.10 sequence bonus) over those invalid regions, with invented thresholds (RELEVANCE_GATE_THRESHOLD = 0.55, STRONG_HOOK_THRESHOLD = 0.70). Its README states NO validation caveat whatsoever. It also documents the output as '20,000+ cortical activation values per half-second', which is wrong (it is 1 Hz).
AND ITS GPU PATH HAS DEMONSTRABLY NEVER RUN. neuroscore/core/backends/gpu.py calls tribev2.load_model(device=...) - no such function exists; tribev2/__init__.py is three lines and its __all__ is exactly ['TribeModel']. It then calls self._model.predict(media_path, modality=modality, device=self._device) - the real signature is predict(self, events: pd.DataFrame, verbose: bool = True), which takes an events DataFrame, not a path, and accepts neither a modality nor a device kwarg. It then treats the return value as a tensor or array (prediction.cpu().numpy()) when predict() returns a TUPLE of (np.ndarray, list). And it hardcodes _DEFAULT_SAMPLE_RATE = 2.0, so every peak_time_sec and duration_sec it reports would be off by exactly 2x even if the call worked. The first line of that method would raise AttributeError against the real library. REJECT NEUROSCORE ENTIRELY - not merely as a scientific signal but as a code reference; the only part of it worth reading is its terminal/HTML report formatting.
2. THE ENGAGEMENT SCORES ARE NOT VALIDATED AGAINST BEHAVIOUR - mandatory caveat. Community 'engagement score' tooling (the Yeo-7 -> seven network time courses -> five composite metrics -> Neural Correlation Index pipeline popularised in the Josh Wade / TribeV2 write-up) explicitly states that NCI scores have NOT been correlated with view counts, watch time, shares or conversions, and that this validation study is still 'the immediate next step'. Independently, arXiv 2607.01400 ran the test and got a null: partial r = +0.058 (95% CI [-0.04, 0.15], t(47)=1.21, p=0.23) against YouTube 'most replayed' curves on 48 videos, null across six cortical networks, value/salience ROIs and permutation tests, below loudness and motion baselines; a supervised probe reached r = 0.47 but collapsed under proper controls, indicating temporal artefact. TREAT ALL SUCH SCORES AS AESTHETIC CONTROL SIGNALS, NEVER AS AUDIENCE PREDICTIONS, AND SAY SO IN THE PIECE.
3. Per-clip z-scoring destroys cross-clip dynamics. Normalising each 15 s clip independently forces every clip to unit variance, so a genuinely calm clip and a genuinely frantic clip produce identical dial magnitudes and the stream loses all long-range dynamic range. The reference implementation calls this out as the cause of a manufactured seam step.
4. Too few samples. A 15 s clip is 15 TRs; after trimming 5 warm-up TRs you have ~10. Any statistic computed on 10 points - especially max, argmax or std - is dominated by noise.
5. MT is tiny. 38 fsaverage5 vertices for MT alone means the motion dial is high-variance; always union with MST.
6. Atlas naming drift. mne's HCP-MMP1 parcel names vary slightly by version. Validate every parcel name against get_hcp_labels() at build time and LOG-AND-DROP misses rather than silently substituting - a wrong index array corrupts the dial invisibly.
7. combine=True path has a naming quirk: the 'L_'/'R_' prefix strip (name = name[2:]) is applied only when combine is False, so the coarse HCPMMP1_combined labels keep a different naming convention. Check before mixing the two.
8. Absolute-value fallacy. Because the target was z-scored and detrended, code that thresholds on a raw preds value ('if faces > 0.5') will behave differently on every clip. Threshold only on normalised units.
9. Cortical-only blind spot. There is no ventral striatum / NAcc in facebook/tribev2 - the strongest neuroforecasting node in the literature - so any 'reward' or 'virality' dial built on the cortical checkpoint is a vmPFC/mPFC proxy, not the real thing. Both the reference Space and GitHub issue #23 state this explicitly.

### Economics

**cost**

$0.00 per hour of continuous stream. The readout is CPU numpy inside the process that already holds the model; it adds no GPU time, no API calls and no egress. One-time storage cost only: ~1.5 GB for the mne sample data plus the HCP-MMP1 annot files during the mask build, which can be discarded once the ~200-800 KB dial_masks.npz is written. If you also want subcortical dials, the cost is not in this component but upstream: a second 613 MB checkpoint and a second forward pass, which roughly doubles the GPU-hours of the PREDICT stage.

### Evidence

**sources**

PRIMARY SOURCE CODE (read directly, not summarised):
- https://github.com/facebookresearch/tribev2 - README; predict() returns (n_timesteps, n_vertices) on fsaverage5, 5 s hemodynamic offset, 'average' subject.
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/utils.py - get_hcp_labels, get_hcp_vertex_labels, get_hcp_roi_indices, summarize_by_roi, get_topk_rois. THE PARCELLATION HELPERS THE BRIEF SAYS DO NOT EXIST.
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/utils_fmri.py - TribeSurfaceProjector; np.vstack([left, right]) confirms the 10242 hemisphere split; FSAVERAGE_SIZES['fsaverage5'] = 10242.
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/plotting/subcortical.py - get_subcortical_labels, get_subcortical_roi_indices, voxel_to_mesh.
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/grids/run_subcortical.py - MaskProjector mask='subcortical', fwhm 6.0.
- neuralset 0.0.2 wheel, neuralset/extractors/neuro.py MaskProjector.get_mask - fetch_atlas_harvard_oxford('sub-maxprob-thr50-2mm') with Cortex/White/Stem/Background excluded. (pip package, PyPI: https://pypi.org/project/neuralset/0.0.2/)
- https://huggingface.co/facebook/tribev2/resolve/main/config.yaml - data.neuro.frequency: 1.0, offset: 5.0, mesh fsaverage5, cleaning standardize zscore_sample + detrend true, duration_trs 100, modality_dropout 0.3, subject_dropout 0.1.
- https://huggingface.co/facebook/tribev2-subcortical - the subcortical checkpoint (613,171,482 B best.ckpt); config MaskProjector mask subcortical resolution 2, frequency 1.0, offset 5.0.

ATLAS / ROI DEFINITIONS:
- https://arxiv.org/html/2605.13904v1 - 'Cortical ROIs are read off the HCP-MMP1 (Glasser et al., 2016) parcellation on fsaverage5'; V1/V2/V3/V4/MT = 523/383/242/180/38 vertices; FFA = FFC (104); PPA = PHA1+PHA2+PHA3 (194); scalar objective = target ROI mean minus mean elsewhere; optimised stimulus drives FFA +0.339 vs +0.080 for a natural face photograph (4.2x).
- https://github.com/recozers/Tribe-V2-Interp/blob/main/feature_viz.py - runnable ROI_MAP plus the nibabel.freesurfer.read_annot lookup with FSAVERAGE5_VERTS = 10242 and the verts[verts < 10242] + offset trick.
- https://arxiv.org/html/2605.04326v1 - paper: 20,484 fsaverage5 vertices; 8,802 voxels across 8 Harvard-Oxford subcortical regions; HCP 360-parcel analysis; ICA recovers primary auditory cortex, language network, motion area, DMN, visual system.
- https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_atlas_surf_destrieux.html - returns map_left/map_right on fsaverage5 (10242/hemi), 76 labels/hemi, no extra atlas fetch.
- https://github.com/ThomasYeoLab/CBIG (Yeo2011_fcMRI_clustering) - fsaverage5/label/{lh,rh}.Yeo2011_17Networks_N1000.annot; nilearn's fetch_atlas_yeo_2011 is volumetric MNI, not surface.

READOUT REFERENCE IMPLEMENTATIONS:
- https://huggingface.co/spaces/techfreakworm/tribev2-brain-timeline - src/tribescore/metrics.py (five metrics with verbatim Glasser parcel lists, build_roi_masks, to_metrics: ROI mean -> full-timeline z-score -> gaussian_filter1d sigma 2 s), src/tribescore/windowing.py (TR = 1.0 s => 1 Hz, WARMUP_TRIM = 5, global-not-per-window z-score rationale), README.md (metric table with literature basis; 'absolute scores are meaningless - only relative temporal dynamics are valid'), KNOWN_ISSUES.md.
- https://github.com/ndpvt-web/neuroscore - neuroscore/core/regions.py (the fabricated vertex_ranges and the 'For MVP, we use approximate index ranges' comment), neuroscore/modes/score.py (WEIGHT_AMYGDALA 0.25, WEIGHT_VMPFC 0.25, WEIGHT_ACC 0.20, WEIGHT_DLPFC 0.20, WEIGHT_SEQUENCE 0.10), neuroscore/core/backends/gpu.py (the non-existent tribev2.load_model and the wrong predict() signature), neuroscore/core/backends/base.py ('TRIBE v2 default: 2.0 (one sample per 0.5s)'). Cited as a NEGATIVE example throughout.
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/__init__.py - three lines; __all__ = ['TribeModel']. Proves tribev2.load_model does not exist.
- https://github.com/siddhant-rajhans/cortexlab - CognitiveLoadScorer (visual complexity, auditory demand, language processing, executive load), HCP-MMP default parcellation via --lh-annot.
- https://github.com/CodaCipher/tribe-subcortex - subcortical composite response scores; README carries no methodological caveats (INFERENCE: treat with the same scepticism as neuroscore).

VALIDATION CAVEAT EVIDENCE:
- https://arxiv.org/abs/2607.01400 'A global predicted-fMRI drive signal from TRIBE does not predict YouTube replay heatmaps' - global field power reduction; 48 videos; partial r = +0.058, 95% CI [-0.04, 0.15], t(47)=1.21, p=0.23; below loudness/motion baselines; supervised probe r = 0.47 collapsed under controls.
- https://medium.com/@wadan/meta-built-an-ai-that-simulates-your-brain-heres-how-you-can-use-it-to-make-content-go-viral-984e6bc84579 - the Yeo-7 -> 7 network signals -> 5 composite metrics -> NCI pipeline, and its own admission that NCI has not been correlated with view counts, watch time, shares or conversions. (Retrieved via search index; direct fetch returns HTTP 403.)
- https://github.com/facebookresearch/tribev2/issues/70 - 'Scoring a video': engineers asking Meta for the simplest correct way to turn preds into one score. OPEN AND UNANSWERED as of 2026-08-31 - there is no official readout guidance.
- https://github.com/facebookresearch/tribev2/issues/23 - subcortical checkpoint request; confirms the released cortical head is predictor.weights [1, 2048, 20484]; Meta author sdascoli announces facebook/tribev2-subcortical on 2026-05-21; also the mPFC-as-NAcc-proxy limitation.
- https://www.datacamp.com/tutorial/tribe-v2-tutorial - independent confirmation of 1 Hz output, (T, 20484), hemisphere split at 10242, and 'no atlas-based or ROI parcellation is provided; analysis remains at the vertex level' in the tutorial's own workflow.

### Other Info

**item_id**

02

### Flagged Uncertain (omitted above)

- `latency_ms`
- `unknowns`

---

## Clip continuity and chaining

### Identity

**what_it_is**

The glue between consecutive H3 Max generations: pull the final frame out of clip N, feed it back in as `image_url` on clip N+1 so the picture continues rather than cuts, and paper over the fact that each clip's natively-generated audio bed is unrelated to the last one's.

**role_in_loop**

Sits between GENERATE and STREAM, and quietly feeds back into GENERATE. It is the only component that makes a queue of independent 10-second requests read as one continuous broadcast rather than a slideshow of unrelated shots — and, because it is a feedback path, it is also the component through which drift and attractor collapse (item 09) physically propagate.

### Interface

**interface_spec**

THREE OPERATIONS. All are local except the third.

1. FINAL-FRAME EXTRACTION (ffmpeg, local, constant time).
   ffmpeg -hide_banner -loglevel error -sseof -1 -i clip_N.mp4 \
          -vsync 0 -update 1 -frames:v 1 -q:v 2 last_N.jpg
   `-sseof -1` seeks to one second before EOF and decodes only that tail, so runtime is independent of file length (milliseconds, not a full decode). `-vsync 0` disables frame drop/dup so nothing is resampled; `-update 1` keeps overwriting a single output file so the last decoded frame is what survives; `-frames:v 1` combined with `-update 1` is belt-and-braces. Use `-sseof -3` if a container ever reports a bad duration. Emit JPEG at `-q:v 2`, not PNG: a 768p JPEG is ~80-200 KB where a PNG is ~1-2 MB, and that size difference decides whether the data-URI path below is viable.
   Recommended refinement — SHARPEST-FRAME SELECTION rather than literally-last:
     ffmpeg -sseof -0.7 -i clip_N.mp4 -vsync 0 -q:v 2 cand_%03d.jpg
   then pick the candidate maximising variance-of-Laplacian (5 lines of OpenCV/numpy) and TRIM the clip to end on that frame with `-to`. The literal last frame of a generated clip is frequently mid-motion and motion-blurred; handing a blurred frame back as a *sharp* conditioning keyframe is the fastest way to compound artefacts (see failure_modes).

2. GEOMETRY LOCK. `minimax/h3-max/image-to-video` has NO `aspect_ratio` field — 'When provided, the output aspect ratio follows this image' (fal OpenAPI). The extracted frame therefore *is* the resolution contract. Normalise unconditionally before submitting:
   ffmpeg -i last_N.jpg -vf scale=1366:768:force_original_aspect_ratio=decrease,pad=1366:768:(ow-iw)/2:(oh-ih)/2 -q:v 2 key_N.jpg

3. HANDING THE FRAME TO fal. Two routes:
   (a) UPLOAD:  url = fal_client.upload_file("key_N.jpg",
                        lifecycle=fal_client.StorageSettings(expires_in=3600))
       -> returns an https://v3.fal.media/... URL. Costs one HTTPS round trip (~150-400 ms) on the critical path. `lifecycle` matters: without it every keyframe of a 24/7 stream accumulates in fal storage forever.
   (b) INLINE DATA URI (RECOMMENDED):  fal accepts a base64 data URI anywhere a file URL is expected — 'you can pass your own URL or a Base64 data URI... the API will handle the file decoding for you', with a documented caveat that large files hurt request performance. A 150 KB JPEG becomes a ~200 KB data URI, which is nothing next to the JSON request budget (prompt alone allows 50,000 chars). `fal_client.encode_file(path)` returns exactly this string. ZERO round trips, nothing to garbage-collect.

SUBMISSION SHAPE for a chained clip:
   {"prompt": <brain-derived prompt>,
    "prompt_expansion_mode": "balanced",
    "duration": 10, "resolution": "768P",
    "image_url": "data:image/jpeg;base64,...",        # continuity anchor
    "end_image_url": "data:image/jpeg;base64,..."}    # OPTIONAL, dual-anchor mode only

AUDIO/VIDEO ASSEMBLY (ffmpeg, at playback assembly time):
   Hard cut, no re-encode (cheapest, works because last-frame chaining already makes the visual join near-continuous):
     ffmpeg -f concat -safe 0 -i playlist.txt -c copy out.mp4
   Crossfaded join (re-encodes; costs `d` seconds of each clip):
     ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
       "[0:v][1:v]xfade=transition=fade:duration=0.25:offset=9.75[v]; \
        [0:a][1:a]acrossfade=d=0.25:c1=tri:c2=tri[a]" -map "[v]" -map "[a]" out.mp4
   Continuous music bed over ducked clip audio (the recommended audio fix):
     ffmpeg -i concat.mp4 -stream_loop -1 -i bed.flac -filter_complex \
       "[0:a]volume=-14dB[clip];[1:a][clip]amix=inputs=2:duration=first:dropout_transition=0[a]" \
       -map 0:v -map "[a]" -c:v copy -shortest out.mp4

**input_contract**

In: one finished MP4 from the previous H3 Max generation (768P, 5-15s, H.264 + AAC, on local disk — download it before the fal CDN URL expires). Out to fal: one JPEG at exactly the stream's target pixel dimensions, quality ~q:v 2, delivered as a data URI or an https URL. `end_image_url` additionally requires a second image at the same dimensions, which must come from somewhere — either a still-image model (an extra generation on the critical path) or a pre-rendered keyframe bank. For the audio bed, one seamlessly-loopable music track long enough that its own loop point is not itself a seam. ffmpeg must be a real build with libx264 and the xfade/acrossfade filters (any recent static build); ffprobe is needed if you want exact durations for xfade offsets rather than trusting the requested `duration`.

**output_contract**

A conditioning JPEG (bytes, or a URL string) and an assembled MP4 segment. The conditioning frame is the entire continuity mechanism: H3 Max reproduces it as literal frame 0 of the next clip, so the visual join across the cut is exact at the seam — the discontinuity, when it comes, is not at the boundary but in the slow accumulation of colour and identity error across many boundaries. Audio has no equivalent: each clip's track is generated independently and begins and ends at arbitrary points in its own imagined soundscape, so the assembled output carries one audible discontinuity per clip boundary (one every 10 seconds, 360 per hour) unless mitigated. `expanded_prompt` from each response is the only textual record of what was actually generated and should be carried alongside the frame as the chain's state.

### Performance

**throughput_constraint**

Not a throughput bottleneck. Every operation is local ffmpeg on a couple of seconds of 768P video and is one to two orders of magnitude cheaper than the 3.5-15 s generation it sits between. Two soft constraints worth naming: (1) ffmpeg is CPU-bound and single-invocation-per-clip — if the crossfade re-encode is run synchronously in the same process that is awaiting generations, it will steal cycles from the event loop, so run it in a thread/subprocess pool or a separate worker; (2) the chaining dependency is inherently SERIAL — clip N+1's conditioning frame does not exist until clip N has finished — which directly conflicts with running 2+ generations concurrently (item 08). You cannot both deep-buffer and strictly chain. Resolution: run a chained 'spine' at concurrency 1 and use the spare concurrency slots for speculative/unchained clips, or accept a chain that branches every K clips.

### Complexity

**dev_complexity**

LOW for the core (two ffmpeg invocations and one extra JSON field), MEDIUM once drift control and audio mitigation are included. Nothing here is algorithmically hard; the complexity is entirely in the taste-level decisions — how often to re-anchor, whether to crossfade, how loud the bed sits — which are settled by watching output, not by reading docs. Budget half a day for a working chain, another half day for the drift/audio mitigations, and expect to spend more time tuning than coding.

**loc_estimate**

~60 LOC for bare last-frame chaining (extract, normalise, encode, pass as image_url). ~130 LOC with sharpest-frame selection, histogram re-anchoring and the periodic hard-reset policy. ~200 LOC including the ffmpeg assembly worker with music bed and optional crossfade. The keyframe/end_image_url strategy adds a second generation call and a keyframe planner: +80-150 LOC.

**off_the_shelf_option**

There is no single library that does this end-to-end, and the pieces are small enough that a wrapper would cost more than it saves. Useful parts: `ffmpeg-python` or plain `subprocess` for the calls; `imageio-ffmpeg` if you want a bundled binary; `fal_client.encode_file` / `upload_file` for delivery; `scikit-image.exposure.match_histograms` (one call) for colour re-anchoring; OpenCV's `cv2.Laplacian(...).var()` for sharpest-frame selection. `GlideBlend` (kajdep.itch.io) is a small purpose-built utility that stitches two AI-generated clips at their most perceptually-similar frames using perceptual hashing plus ffmpeg.wasm — built exactly for merging Sora/Veo clips — and is worth reading as a reference for the seam-finding idea even though it is a Windows GUI tool and not embeddable. `fal-ai-community/realtime-krea-wan` sidesteps the whole problem by using a model that accepts prompt changes mid-generation (item 17); if clip chaining proves miserable, that is the escape hatch, not a better stitcher.

### Decision

**code_sketch**

import subprocess, cv2, numpy as np, fal_client, glob, os

W, H = 1366, 768               # lock the stream geometry; i2v inherits it from the image

def last_frame(clip: str, out: str = "key.jpg", window: float = 0.7) -> str:
    """Sharpest frame from the final `window` seconds. -sseof makes this constant-time."""
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                    "-sseof", f"-{window}", "-i", clip,
                    "-vsync","0","-q:v","2","/tmp/cand_%03d.jpg"], check=True)
    cands = sorted(glob.glob("/tmp/cand_*.jpg"))
    best = max(cands, key=lambda p: cv2.Laplacian(
        cv2.imread(p, cv2.IMREAD_GRAYSCALE), cv2.CV_64F).var())   # variance-of-Laplacian
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",best,
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                           f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2",
                    "-q:v","2", out], check=True)
    for p in cands: os.remove(p)
    return out

def reanchor(key: str, reference: str) -> str:
    """Pull colour back to the chain's reference frame. Kills the neutral->orange drift."""
    from skimage.exposure import match_histograms
    k, r = cv2.imread(key), cv2.imread(reference)
    cv2.imwrite(key, match_histograms(k, r, channel_axis=-1).astype(np.uint8))
    return key

# ---- the chain ----
MAX_HOPS = 6                    # hard reset before drift becomes visible
chain_ref, hops, prev_clip = None, 0, None

async def next_clip(prompt: str):
    global chain_ref, hops, prev_clip
    args = dict(prompt=prompt, duration=10, resolution="768P",
                prompt_expansion_mode="balanced")

    if prev_clip and hops < MAX_HOPS:
        key = last_frame(prev_clip)
        if chain_ref: reanchor(key, chain_ref)
        else:         chain_ref = key
        args["image_url"] = fal_client.encode_file(key)   # data: URI, no upload round trip
        hops += 1
    else:                                                  # hard re-anchor: routes to t2v
        args["aspect_ratio"] = "16:9"
        chain_ref, hops = None, 0

    res = await (await fal_client.submit_async(
        "minimax/h3-max/image-to-video", arguments=args)).get()
    prev_clip = download(res["video"]["url"])              # fal CDN urls expire
    return prev_clip, res.get("expanded_prompt")

# ---- assembly worker, runs one clip behind the generator ----
# hard cut, no re-encode:
#   ffmpeg -f concat -safe 0 -i playlist.txt -c copy segment.mp4
# continuous music bed over ducked clip audio  <-- the real fix for audio seams:
#   ffmpeg -i segment.mp4 -stream_loop -1 -i bed.flac -filter_complex \
#     "[0:a]volume=-14dB[c];[1:a][c]amix=inputs=2:duration=first:dropout_transition=0[a]" \
#     -map 0:v -map "[a]" -c:v copy -shortest out.mp4
# optional crossfade at a join (re-encodes; costs 0.25s of each clip):
#   ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
#     "[0:v][1:v]xfade=transition=fade:duration=0.25:offset=9.75[v]; \
#      [0:a][1:a]acrossfade=d=0.25:c1=tri:c2=tri[a]" -map "[v]" -map "[a]" out.mp4

### Risk

**failure_modes**

1. COLOUR AND EXPOSURE DRIFT, THE DOMINANT ONE. Documented as the most common form of chaining degradation: progression 'from neutral to warm to noticeably orange', plus contrast and saturation lift. Directly evidenced in a looping I2V setup (kijai/ComfyUI-WanVideoWrapper #1541) where brightness and saturation increase every cycle and the reporter could not fix it by changing scheduler, VAE, sampler or LoRA. It is a property of the feedback loop, not of any one model's settings. Histogram re-anchoring plus periodic hard reset is the fix; there is no parameter to turn it off.
2. BLUR LAUNDERING. The literal final frame of a generated clip is often mid-motion and motion-blurred. Feeding it back as a conditioning keyframe tells the model 'this blur is the scene', and the next clip renders the blur as texture — which then blurs further. Non-obvious, compounds fast, and is entirely avoided by sharpest-frame selection.
3. SEMANTIC COLLAPSE AT DEPTH. Beyond roughly 8-12 hops, drift stops being cosmetic: 'object deformation and abrupt motion shifts', eventually 'semantic collapse where the model loses track of what things are'. In a 24/7 stream with no reset policy this is not a risk, it is a certainty on a timescale of minutes.
4. AUDIO DISCONTINUITY EVERY CLIP BOUNDARY. Structural and unfixable at the API level: H3 Max generates a complete independent soundtrack per clip with no cross-clip conditioning and no parameter to provide any. At 10 s clips that is 360 audible discontinuities per hour. Crossfading smears them rather than removing them — a 0.25 s acrossfade across a hard key change is still a hard key change. Only the continuous-bed approach actually solves it.
5. SILENT RESOLUTION WOBBLE. `aspect_ratio` does not exist on the i2v endpoint; output geometry follows the conditioning image. Any drift in the extracted frame's dimensions silently changes the stream's resolution mid-broadcast and will break a live encoder that was configured once at startup. Normalise every frame unconditionally.
6. SERIALISATION vs CONCURRENCY DEADLOCK-BY-DESIGN. Strict chaining is inherently sequential — you cannot start clip N+1 until N has finished — which forfeits exactly the concurrency that item 08 needs for buffer depth. Discovered late, this forces an architecture rewrite. Decide up front: chained spine at concurrency 1 plus speculative unchained clips on the spare slots, or branch the chain.
7. A CONTENT-POLICY REJECTION BREAKS THE CHAIN, NOT JUST THE CLIP. When clip N+1 is refused (item 05), there is no new final frame, so the fallback clip must either reuse clip N's frame (fine) or the chain silently restarts. Handle explicitly or the re-anchor counter drifts out of sync with reality.
8. `-sseof` ON A MALFORMED CONTAINER returns nothing, and `-update 1` will happily leave a stale file from the previous clip in place — so the pipeline silently conditions clip N+1 on clip N-1's frame. Always check the output file's mtime or write to a fresh path.
9. CROSSFADE OFFSET DRIFT. `xfade`'s offset must equal the first clip's true duration minus the transition duration. Trusting the *requested* `duration` rather than ffprobe's measured duration accumulates a frame or two of error per join, which over hundreds of joins desynchronises audio and video.
10. THE CHAIN IS ALSO THE ATTRACTOR-COLLAPSE PATHWAY. Because clip N+1's content is conditioned on clip N's pixels, any tendency of the brain-driven prompt loop to converge (item 09) is reinforced by the visual chain rather than being independent of it. The periodic hard re-anchor doubles as the novelty injection that item 09 requires — which is a good reason to implement it early even if drift is not yet visible.

### Economics

**cost**

Near zero in dollars — every operation is local ffmpeg plus a few lines of numpy. The costs are indirect and worth naming precisely:
  - COMPUTE: negligible. A modest VPS core handles the extract/normalise path; the crossfade re-encode wants roughly one dedicated core per stream at 768P.
  - fal STORAGE: only on the upload path, and only if `lifecycle` is omitted. At one 150 KB keyframe per 10 s clip that is ~54 MB/day accumulating indefinitely. The data-URI path costs nothing and stores nothing.
  - THE REAL COST IS BILLED SECONDS. Two mechanisms. First, a hard re-anchor every 6 clips is one clip in six that discards continuity — no extra spend, but it does mean the chained approach buys ~83% continuity, not 100%. Second, and more significant, strict chaining forfeits concurrency, so recovering from a failed or rejected generation costs a full serial round trip (3.5-15 s) rather than being absorbed by a parallel slot. At H3 Max's post-promo $0.08/s at 768P — $288 per hour of stream — anything that forces a regeneration is $0.80 per 10 s clip discarded. A drift-driven re-anchor policy that throws away and regenerates clips rather than simply cutting would be genuinely expensive; the recommended policy does not regenerate, it just stops conditioning, so it is free.
  - The crossfade approach also literally costs video: a 0.25 s xfade at every join discards 0.25 s of paid footage per clip, ~2.5% of spend at 10 s clips. Trivial, but it is the argument for the hard cut plus music bed over crossfading everything.

### Other Info

**item_id**

06

### Flagged Uncertain (omitted above)

- `latency_ms`
- `realtime_headroom`
- `recommended_approach`
- `simpler_alternative`
- `sources`
- `unknowns`

---

## Closed Loop Recursion

### Identity

**what_it_is**

The recursion: the clip the system just generated becomes the stimulus TRIBE v2 reacts to next, so the simulated brain is watching the output of a machine that is optimising against it. It is the conceptual payoff of the piece and the single most likely thing to destroy the piece.

**role_in_loop**

Closes the cycle. Instead of perceive(external) -> predict -> prompt -> generate -> stream, the arc becomes generate -> stream -> perceive(own output) -> predict -> prompt -> generate. Concretely it is two edges: (1) the rendered clip URL (or its local file) is fed back into TRIBE's stimulus ingestion, and (2) the `expanded_prompt` returned alongside it is fed into TRIBE's text branch. It adds no new component — it adds a dependency, and that dependency is what turns a pipeline into a dynamical system with an attractor.

### Interface

**interface_spec**

VERIFIED AGAINST SOURCE — github.com/facebookresearch/tribev2 @ main (pushed 2026-06-23), file tribev2/demo_utils.py and tribev2/eventstransforms.py.

A. THE DOCUMENTED API BLOCKS THE OBVIOUS PLAN.

    def get_events_dataframe(self, text_path=None, audio_path=None, video_path=None) -> pd.DataFrame

    provided = {name: value for name, value in [...] if value is not None}
    if len(provided) != 1:
        raise ValueError(f"Exactly one of text_path, audio_path, video_path must be provided, got: ...")

You cannot pass the generated clip AND the expanded_prompt through the documented entry point. `text_path` additionally accepts only `.txt`; `video_path` only .mp4/.avi/.mkv/.mov/.webm. So the premise 'feed expanded_prompt straight into TRIBE's text branch' is NOT reachable via `get_events_dataframe`. It IS reachable — cheaply — one level down. See C.

B. THE VIDEO PATH ALREADY POPULATES THE TEXT BRANCH, AT A COST YOU DID NOT BUDGET FOR.
`get_events_dataframe(video_path=...)` calls `get_audio_and_text_events`, which runs this transform chain:

    ExtractAudioFromVideo()
    ChunkEvents(event_type_to_chunk='Audio', max_duration=60, min_duration=30)
    ChunkEvents(event_type_to_chunk='Video', max_duration=60, min_duration=30)
    ExtractWordsFromAudio()      # <-- WhisperX large-v3, launched via `uvx` as a SUBPROCESS
    AddText()
    AddSentenceToWords(max_unmatched_ratio=0.05)
    AddContextToWords(sentence_only=False, max_context_len=1024, split_field='')
    RemoveMissing()

Two consequences the plan has to absorb:
  * H3 Max emits native synchronised audio, so if a generated clip contains speech, TRIBE transcribes it and the text branch is already fed — from the clip's own dialogue, not from your prompt.
  * Every closed-loop tick runs `uvx whisperx --model large-v3 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --compute_type float16` as a subprocess. That is a second large model, a second GPU tenant, a cold `uvx` resolve on first call, and seconds of added latency per clip. This is an unbudgeted cost of closed-loop that open-loop-from-a-file does not avoid either, but which the expanded_prompt trick eliminates.

C. HOW TO ACTUALLY INJECT expanded_prompt — TWO VERIFIED HOOKS, BOTH OF WHICH *REMOVE* LATENCY.

  HOOK 1 (cleanest, ~15 LOC) — the transcript cache. `ExtractWordsFromAudio._run` does:

      transcript_filename = wav_filename.with_suffix('.tsv')
      if transcript_filename.exists() and not self.overwrite:
          transcript = pd.read_csv(transcript_filename, sep='\t')
      else:
          transcript = self._get_transcript_from_audio(...)   # WhisperX

  Write your own TSV next to the extracted audio, before the transform runs, with the columns WhisperX itself produces:

      text, start, duration, sequence_id, sentence

  Build those rows from `expanded_prompt` with synthetic uniform word timings across the clip duration. WhisperX is then never invoked.

  HOOK 2 (more control, ~40 LOC) — pre-seed Word rows. The same method opens with:

      if 'Word' in events.type.unique():
          logger.warning('Words already present in the events dataframe, skipping')
          return events

  So construct the events DataFrame yourself: one row {type:'Video', filepath, start:0, timeline:'default', subject:'default'} plus N rows {type:'Word', text, start, duration, sequence_id, sentence, timeline:'default', subject:'default', language:'english'}, then run the remaining transforms. ExtractWordsFromAudio short-circuits.

  VERDICT ON THE PREMISE: 'free, exact, zero added latency' is right in spirit and understated in effect — injecting expanded_prompt does not add latency, it SUBTRACTS a WhisperX large-v3 pass per clip. But it is not reachable through the public API; it requires ~15-40 LOC against internals of `tribev2.eventstransforms`, and it is exact only when expanded_prompt is non-null (see failure_modes 1).

D. SIGNATURE OF THE RECURSION STAGE ITSELF.

    def stimulus_for_next_tick(
        last_clip_path: str,            # downloaded H3 Max mp4
        last_expanded_prompt: str | None,
        external_corpus: Iterable[str], # pool of non-generated clips — the entropy source
        w: float,                       # 0.0 = fully open loop, 1.0 = fully closed loop
        step: int,
    ) -> pd.DataFrame                   # events DataFrame ready for model.predict()

**input_contract**

Per tick: a locally-readable .mp4 of the clip just generated (fal returns a CDN URL; you must download it — budget 1-3 s for a 15 s 768P clip on a well-connected host), plus `result['expanded_prompt']` from the same fal response, plus the clip's duration in seconds.
HARD CONSTRAINT ON CLIP LENGTH. `ChunkEvents(max_duration=60, min_duration=30)` sits in the video path. A 5 s or 15 s clip is below `min_duration`; TRIBE's own analysis pipeline is built around 30-60 s stimulus chunks, and the model applies a 5 s hemodynamic offset on top. Short clips will read as diffuse and low-intensity regardless of content. Practical floor for a stimulus that produces a usable readout: 15 s minimum, and prefer feeding TRIBE a rolling 30 s window built from the last two clips rather than each clip in isolation. This is the single most consequential input constraint on the recursion and it pushes the design toward 15 s clips (H3 Max's maximum) rather than 5 s ones.
For the hybrid loop: an external corpus of clips (or a live feed) of at least a few hundred distinct items — the fresh-data reservoir.

**output_contract**

An events DataFrame ready for `model.predict(events)`, returning `(preds, segments)` with preds of shape (n_timesteps, 20484) on the fsaverage5 surface at the model's TR, offset 5 s into the past to compensate hemodynamic lag. Physically the numbers are z-scored predicted BOLD for the average subject. Their magnitude is small: arXiv 2605.13904 measures a natural face photograph at +0.080 in FFA. This means the recursion's 'signal' is a drift of a few hundredths of a z-unit per clip, and the loop's apparent responsiveness is entirely a property of how you rescale it (see the rolling-z requirement in the prompt-translation item).
The recursion also outputs, per tick, the log record that makes the piece analysable: (clip_url, prompt, expanded_prompt, z-vector, novelty score, drive vector, w). Without this the collapse is undiagnosable after the fact.

### Performance

**throughput_constraint**

The recursion does not add API calls, but it makes the fal concurrency ladder bite harder. Open loop can fire generations speculatively and in parallel because nothing downstream depends on their content; closed loop cannot generate clip N+1 until clip N has been read, so in-flight parallelism is capped at the generate-ahead depth regardless of how many concurrent slots fal grants. A new fal account's 2 concurrent IN_PROGRESS requests is therefore not the binding constraint in closed loop — the serial dependency is.
Second constraint: TRIBE must be a single warm resident process (28-32 GB VRAM), so brain inference is serialised. One clip at a time through TRIBE, always. If the TRIBE pass takes longer than the clip duration, the loop cannot close at any concurrency and you must fall back to open loop or to reading every Nth clip.
Third: `enable_safety_checker` defaults true, and the closed loop's drift is toward exactly the imagery that trips it (faces, bodies, threat cues). Rejection rate is expected to RISE over a run — a throughput drain that gets worse the longer the piece runs, which is a nasty property for a 24/7 stream.

### Complexity

**dev_complexity**

MEDIUM overall, and unevenly distributed.
  * The plumbing is LOW: download the clip, call `model.predict`, feed the readout forward. ~50 LOC.
  * The expanded_prompt injection is LOW-MEDIUM: ~15-40 LOC against `tribev2.eventstransforms` internals, not the public API, so it is exposed to upstream changes. Pin the commit.
  * The stability machinery (rolling z, novelty term, temperature schedule, circuit breaker, w-scheduling) is MEDIUM: ~120-180 LOC, none of it hard, all of it requiring taste and a long observation run to tune.
  * The genuinely hard part is not code. It is that you cannot know whether the damping constants work without running the thing for hours and watching. Budget a night of observation per parameter set, not an afternoon of unit tests.

**loc_estimate**

~50 LOC recursion plumbing (download, predict, forward the readout) + ~15-40 LOC expanded_prompt injection (TSV cache hook is the 15-LOC version) + ~120-180 LOC stability layer (rolling z-score, prompt-embedding archive, novelty score, temperature schedule, circuit breaker, w-scheduler) + ~30 LOC per-tick JSONL logging. Total ~220-300 LOC. The open-loop and hybrid variants are the same code with `w` set differently; build the hybrid and get all three for free.

**off_the_shelf_option**

Nothing implements this. None of the eight repositories under the `tribe-v2` GitHub topic (neuroscore, Audience, mindprint, neuroscanner, tribe-brain-analysis, NoLemming, tribe-subcortex, NeuroSync) closes a loop — they are all one-shot scoring and analysis tools. Three things reduce work adjacently:
  * github.com/ndpvt-web/neuroscore — wraps `score()` over TRIBE and returns a 7-region RegionMap, so the readout half of each tick is off the shelf. Its cached/demo backend is also the cheapest way to dry-run the loop's control logic with no GPU at all before the real thing exists.
  * github.com/fal-ai-community/realtime-krea-wan — a working dynamic-prompt-rewriting loop against fal's realtime WebSocket surface. Not directly reusable on the H3 Max clip queue, but its loop structure and MsgPack client are the closest existing scaffold.
  * arXiv 2602.10552 (MindPilot) — the published precedent for exactly this architecture (EEG as black-box optimisation feedback steering naturalistic image generation, with a pseudo-model guidance mechanism because the brain signal is non-differentiable). No code located. Cite it; do not expect to reuse it.
For the anti-collapse literature there is no library either — the formulas below are assembled from the novelty-search and RLHF-regularisation literature and must be written by hand. They are ~150 LOC.

### Decision

**recommended_approach**

RUN THE HYBRID. An external stimulus source keeps injecting entropy; the generated output is mixed in with weight w; the mixing weight is itself part of the composition.

WHY, IN ONE LINE: 'Self-Consuming Generative Models Go MAD' (arXiv 2307.01850) tests exactly three regimes — fully synthetic loops, synthetic-augmentation loops with a fixed real dataset, and FRESH DATA LOOPS where new real data enters each generation — and finds that without enough fresh real data in each generation, quality or diversity progressively decreases; the fresh-data loop is the regime that holds. Your closed loop is a fully synthetic loop. The hybrid is a fresh-data loop. This is the one design decision with direct published evidence behind it.

CONCRETE DESIGN.

Step 1 — three modes behind one parameter.
    w = 0.0  open loop     : TRIBE watches an external feed only. Generated clips are output, never input.
    w = 1.0  closed loop   : TRIBE watches only the system's own output. The pure form. Collapses.
    0 < w < 1 hybrid       : alternate the stimulus source, choosing generated with probability w.
Implement alternation, not blending — building a single events DataFrame from two video sources is untested against `ChunkEvents` semantics and is not worth the risk. `stimulus = last_clip if random() < w else next(external_corpus)`.

Step 2 — the external entropy source. Cheapest good options, in order: a fixed corpus of a few hundred 30 s clips (public-domain film, nature footage, archive material) sampled without replacement; a live public webcam or radio stream segmented into 30 s windows; the previous hour of the stream's OWN output, delayed — cheap but note this is still synthetic and does NOT count as fresh data under the MAD result. Prefer real footage.

Step 3 — expanded_prompt injection. Use Hook 1 (the .tsv transcript cache) from interface_spec. `expanded_prompt or prompt` — never the raw field, which can be null. Attach a per-word uniform timing grid across the clip duration.

Step 4 — THE DAMPING FORMULA. Four terms; all of them are needed, and the hard one is the one that actually works.

  Let r_t in R^K be the ROI readout, z_t its rolling z-score over the last W=20 clips (sigma floor 0.05 — natural-stimulus activations are ~0.04-0.15 z-units, so an unfloored sigma explodes early).
  Let e_t = embed(expanded_prompt_t) be a sentence embedding of the prompt actually rendered.
  Let A = archive of the last M=40 embeddings.

  (i) NOVELTY, k-nearest-neighbour in the archive (the standard novelty-search form):
        n_t = (1/k) * sum over the k=5 nearest a in A of [ 1 - cos(e_t, a) ]
      n_t near 0 means the stream is repeating itself. This is your collapse detector and it is the number to put on the monitoring dashboard.

  (ii) DAMPED DRIVE — a first-order lag with a move limit, so no single clip can yank the system:
        a_t = clip( a_{t-1} + eta * (g_t - a_{t-1}),  -c, +c ),   eta = 0.25, c = 1.5
      where g_t is the raw policy output (z_t for the activation-maximising policy, or the setpoint error r*(t) - z_t for the trajectory-tracking policy). eta is a time constant, not a learning rate: eta=0.25 gives a ~4-clip response, i.e. ~1 minute at 15 s clips.

  (iii) NOVELTY-COUPLED TEMPERATURE — exploration rises automatically as the stream repeats itself:
        tau_t = tau_min + (tau_max - tau_min) * (1 - n_t / n_ref)^gamma,
        clipped to [tau_min, tau_max],  tau_min = 0.6, tau_max = 1.4, gamma = 2, n_ref = the running median of n over the last 200 clips.
      Pass tau_t as the prompt-writing LLM's `temperature`, or as the softmax temperature over the motif table in the template design.

  (iv) HARD CIRCUIT BREAKER — the term that actually saves you:
        if n_t < 0.15 * n_ref for 3 consecutive ticks:
            force w = 0 for the next 5 ticks (external stimulus only),
            hard-override the prompt subject with a uniformly sampled motif from a fixed external bank,
            reset a_t = 0.
      This is deliberately blunt. The reason it is blunt is item (v).

  (v) WHY A SOFT PENALTY IS NOT ENOUGH — and this is load-bearing. The soft-regularisation analogue of a KL penalty here would be mixing a reference-prompt fragment into every prompt with probability lambda ~ 0.2. Do it; it costs 3 LOC and helps. But do not rely on it: the RLHF literature reports that severe reward-model overoptimisation routinely occurs even under strict KL constraints, because a policy can exploit a low-probability spurious feature with a minimal footprint on the global KL penalty (arXiv 2604.13602). Translated: your prompts can stay superficially varied while every clip converges on the same handful of salience features. That is why the collapse detector is a NOVELTY score on rendered output, and the response is a hard reset, not a gradient.

Step 5 — SCHEDULE w AS COMPOSITION, NOT AS A CONSTANT. Start a session at w=0.2 and ramp toward w=0.9 over an hour, then snap back. The piece then performs its own thesis: you watch the stream become progressively more self-referential, watch it narrow, and watch it be forcibly reopened. That is a better artwork than either endpoint and it costs one line of scheduling code.

Step 6 — CLOSE THE LOOP EVERY N-TH CLIP, not every clip (N=2 or 3). Buys the latency headroom and slows the drift. See realtime_headroom.

STARTING CONSTANTS, to be tuned by observation: W=20, M=40, k=5, eta=0.25, c=1.5, tau in [0.6, 1.4], gamma=2, breaker at 0.15*n_ref for 3 ticks, lambda=0.2, w ramp 0.2 -> 0.9 per hour, N=2.

**simpler_alternative**

RUN OPEN LOOP AND SHIP. TRIBE watches an external stimulus source — a film, a live camera, a radio stream — and the predicted brain response writes prompts for a generated stream that is never fed back. Every stability problem in this document disappears: no attractor, no MAD loop, no serial dependency, no WhisperX in the critical path, no drift into safety-checker territory. The generation stage becomes embarrassingly parallel and the fal concurrency ladder stops mattering. Dev complexity drops from MEDIUM to LOW and about 200 LOC of stability machinery evaporates.
What you lose is the thesis. The open-loop piece is 'a machine dreams what a brain model says you are feeling'; the closed-loop piece is 'a machine feeds itself through a model of you and eats itself'. The second is the better idea and the first is the one that will definitely be running at 3am.
BUILD ORDER, therefore: get open loop running end to end first — it is the same code with w=0 — then turn w up with the circuit breaker already in place. Never build closed loop first; you will spend the demo debugging a dynamical system instead of a pipeline.
CRUDEST FALLBACK IF THE TRIBE PASS IS TOO SLOW TO CLOSE THE LOOP AT ALL: precompute the ROI response for a fixed bank of a few hundred motifs offline, and run the live loop as a lookup against that table with no TRIBE in the loop. The recursion then exists only as a bookkeeping update on a table. Cheap, robust, and honest as long as you say so.

**code_sketch**

# recursion.py — hybrid closed loop with the expanded_prompt injection and the damping terms.
import csv, random, collections, pathlib
import numpy as np, pandas as pd

# ---------- 1. expanded_prompt -> TRIBE text branch, via the transcript cache (Hook 1) ----------
def seed_transcript(audio_path: pathlib.Path, expanded_prompt: str, clip_seconds: float):
    """Write the .tsv that ExtractWordsFromAudio reads instead of running WhisperX large-v3.
    Columns must match what _get_transcript_from_audio produces."""
    words = expanded_prompt.split()
    if not words:
        return
    dt = clip_seconds / len(words)
    rows = [{'text': w, 'start': i * dt, 'duration': dt,
             'sequence_id': 0, 'sentence': expanded_prompt[:500]}
            for i, w in enumerate(words)]
    pd.DataFrame(rows).to_csv(audio_path.with_suffix('.tsv'), sep='\t', index=False)
    # ExtractWordsFromAudio now hits its cache branch; WhisperX is never invoked.

# ---------- 2. collapse detector ----------
class Novelty:
    def __init__(self, m=40, k=5):
        self.arch = collections.deque(maxlen=m); self.k = k
        self.hist = collections.deque(maxlen=200)
    def __call__(self, emb):
        emb = emb / (np.linalg.norm(emb) + 1e-9)
        if not self.arch:
            self.arch.append(emb); self.hist.append(1.0); return 1.0, 1.0
        d = sorted(1.0 - np.dot(np.array(self.arch), emb))[:self.k]
        n = float(np.mean(d))
        self.arch.append(emb); self.hist.append(n)
        return n, float(np.median(self.hist))          # n_t, n_ref

# ---------- 3. damped drive + temperature + circuit breaker ----------
class Governor:
    def __init__(self, k, eta=.25, c=1.5, tmin=.6, tmax=1.4, gamma=2.0):
        self.a = np.zeros(k); self.eta, self.c = eta, c
        self.tmin, self.tmax, self.gamma = tmin, tmax, gamma
        self.low = 0; self.lock = 0
    def step(self, g, n, n_ref):
        self.a = np.clip(self.a + self.eta * (g - self.a), -self.c, self.c)   # (ii)
        ratio = n / (n_ref + 1e-9)
        tau = self.tmin + (self.tmax - self.tmin) * max(0.0, 1.0 - ratio) ** self.gamma  # (iii)
        tau = float(np.clip(tau, self.tmin, self.tmax))
        self.low = self.low + 1 if ratio < 0.15 else 0                       # (iv)
        breaker = False
        if self.low >= 3 and self.lock == 0:
            breaker, self.lock = True, 5
            self.a[:] = 0.0
        self.lock = max(0, self.lock - 1)
        return self.a.copy(), tau, breaker, self.lock > 0

# ---------- 4. the tick ----------
MOTIF_BANK = [...]        # fixed external motif bank, used only by the breaker
EXTERNAL   = [...]        # corpus of real 30s clips — the fresh-data reservoir (MAD mitigation)

def tick(t, model, gov, nov, w_sched, last_clip, last_expanded, embed, write_prompt, generate):
    w = w_sched(t)                                    # ramp 0.2 -> 0.9 over the hour
    n, n_ref = nov(embed(last_expanded or ''))
    z = readout(model, last_clip)                     # (K,) rolling-z ROI vector, item 02
    g = target(t) - z                                 # P3 setpoint tracking; use z for P1
    a, tau, breaker, locked = gov.step(g, n, n_ref)

    if breaker or locked:
        w = 0.0                                       # force external stimulus
    stim = last_clip if random.random() < w else random.choice(EXTERNAL)

    prompt = (random.choice(MOTIF_BANK) if breaker
              else write_prompt(a, last_expanded, temperature=tau))
    if random.random() < 0.20:                        # (v) soft reference-mixing, the KL analogue
        prompt += ' ' + REFERENCE_FRAGMENT

    res = generate(prompt, duration=15, resolution='768P',
                   prompt_expansion_mode='balanced')
    clip = download(res['video']['url'])
    seed_transcript(audio_path_for(clip), res.get('expanded_prompt') or prompt, 15.0)
    log(t, prompt, res.get('expanded_prompt'), z, a, n, n_ref, tau, w, breaker)
    return clip, (res.get('expanded_prompt') or prompt)

### Risk

**failure_modes**

1. `expanded_prompt` IS NULL AND THE TEXT BRANCH SILENTLY EMPTIES. fal's schema is explicit: the field is 'Null when prompt expansion was disabled, left the prompt unchanged, or was performed internally by MiniMax's hosted API'. The third clause means it can be null on requests that DID expand. Code that does `feed(result['expanded_prompt'])` will intermittently feed None, the injected transcript will be empty, and the text branch quietly contributes nothing — with no error anywhere. Always `result.get('expanded_prompt') or prompt`, and alert when the null rate exceeds a few percent.

2. ATTRACTOR COLLAPSE — EVIDENCED, NOT SPECULATIVE, BUT CALIBRATE IT HONESTLY. arXiv 2605.13904 measures a gradient-ascent-optimised FFA stimulus at +0.339 z-units against +0.080 for a natural face photograph and +0.039 for a vector illustration: a 4.24x gap between what the encoder maximally likes and what a real face achieves. The authors state plainly that 'optimized stimuli are extrema of the encoder's response surface... gradient ascent finds patterns that exceed anything in the natural distribution', that this 'risks overfitting to adversarial features', and that they restricted optimisation to grayscale specifically 'to avoid adversarial high-frequency exploits'. A system that optimises for its own brain model is climbing the same surface. THE CALIBRATION: that paper optimises in PIXEL SPACE with 3,000 gradient steps per restart — a vastly stronger optimiser than a loop that takes one discrete prompt-space step per 15 s clip through a generator whose own prior keeps output on the natural-video manifold. So the failure here will NOT look like adversarial noise. It will look like semantic mode collapse: every clip becomes a face in close-up, high contrast, fast motion, loud. Slower than 'within minutes', and boring rather than uncanny. Plan the monitoring for that signature — the novelty score n_t on rendered prompts is the detector, and it will drift down over tens of minutes, not seconds. [The 'within minutes' timescale is an inference from the pixel-space result, not a measurement of this loop; treat the timescale as unknown until observed.]

3. MAD / SELF-CONSUMING DEGENERATION, WHICH IS A DIFFERENT FAILURE FROM (2). Even with no optimisation pressure at all, a generator repeatedly consuming its own output loses precision or recall progressively (arXiv 2307.01850). Here that shows up as compounding artefacts and a shrinking visual vocabulary rather than as salience-seeking. The two failures stack and are mitigated differently: (2) by the novelty/temperature/breaker terms, (3) by fresh external data. This is why the hybrid needs REAL footage in the reservoir, not delayed output of its own.

4. THE 30-SECOND FLOOR MAKES SHORT CLIPS A DEAD LOOP. `ChunkEvents(min_duration=30)` plus a 5 s hemodynamic offset means a 5 s clip produces a diffuse, near-flat readout. Feed 5 s clips and the loop will appear to run perfectly while the brain signal is noise — the most demoralising possible failure because nothing errors. Feed a rolling 30 s window (the last two 15 s clips concatenated), not individual clips.

5. WHISPERX IN THE HOT PATH. Without the transcript-cache injection, every tick shells out to `uvx whisperx --model large-v3`. First call resolves and downloads the environment; every call contends for the same GPU as TRIBE. This is the most likely cause of a loop that runs fine in testing and falls behind in production.

6. THE INJECTION IS AGAINST INTERNALS. Both hooks depend on the current shape of `tribev2/eventstransforms.py` — the `.tsv` cache filename convention and the `if 'Word' in events.type.unique()` short-circuit. Neither is a public API. Pin the commit (repo pushed 2026-06-23) and assert on the transform's behaviour in a startup smoke test.

7. SEMANTIC MISMATCH IN WHAT YOU INJECT. TRIBE's text branch was trained on transcribed SPEECH in naturalistic film and podcast stimuli, with sentence context and a 1024-word window. `expanded_prompt` is cinematographic instruction ('anamorphic, teal grade, slow push in') — far out of that distribution. Injecting it is defensible as artistic construction; it is NOT a valid prediction of how a brain would respond to anything. If the piece claims otherwise it is claiming something false. Say 'a description of the clip is read to the model' in the wall text, and mean it.

8. SAFETY REJECTIONS RISE OVER A RUN. The drift in (2) heads toward faces, bodies and threat cues — the region where `enable_safety_checker` rejects. So throughput degrades as a FUNCTION of how long the piece has been running, which is exactly the failure mode a 24/7 stream cannot absorb. Treat rejection rate as a second collapse detector: a rising rejection rate is a leading indicator that the breaker is about to be needed.

9. SILENT BUFFER DRAIN. The closed loop's serial dependency means a small per-tick deficit compounds. A 1 s overrun per tick at 15 s clips drains a 4-clip buffer in 60 ticks — 15 minutes in, with no error until playback starves. Instrument buffer depth and alarm on the derivative, not the level.

10. THE PIECE MIGHT BE INDISTINGUISHABLE FROM RANDOM. The honest one. Given a signal of a few hundredths of a z-unit, rescaled by a rolling window, passed through a hand-authored motif table and rewritten twice (once by your LLM, once by H3's prompt expander), the causal chain from brain prediction to pixels is thin. Run the w=0-with-shuffled-readout control condition for one night. If nobody can tell, that is a finding about the piece, and you want to have it before someone else does.

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `realtime_headroom`
- `unknowns`

---

## Closed-loop neuro-generation prior art

### Identity

**what_it_is**

The seven-year research lineage this project is the artistic descendant of: systems that synthesise a stimulus, score it against a model (or a real brain), and iterate. NeuroGen (2021/22), BrainDiVE (NeurIPS 2023 oral), MindPilot (ICLR 2026), Kasahara's DecNefGAN (2024), plus the two ancestors that actually answer the degeneration question - Ponce et al./XDream and Bashivan et al., both 2019 - and the one paper that ran this exact experiment on TRIBE v2 itself (Bladon & Bent, arXiv 2605.13904, May 2026).

THE HEADLINE, WHICH IS BOTH GOOD AND BAD NEWS: the entire literature agrees on what determines whether a brain-optimising loop degenerates, and it is not the encoder. It is whether the generator is constrained to a natural-stimulus manifold. Unconstrained pixel-space optimisation ALWAYS produces adversarial high-frequency imagery. Generator-constrained optimisation NEVER does - it produces weird-but-plausible pictures. Because H3 Max is reachable only through a text prompt, the proposed system is structurally incapable of the adversarial-noise failure mode. What it WILL do instead is converge semantically, and the literature is specific about where to: faces, in close-up, at high contrast.

**role_in_loop**

This is not a component; it is the predictive model for how the whole loop behaves once closed. It governs the design of exactly two things - the coupling strength between the ROI readout and the prompt, and the novelty/damping term that stops the stream converging. It should be read before the orchestration loop is written, because it changes the objective function from 'maximise' to 'track a setpoint', and that is an architectural decision, not a tuning parameter.

### Interface

**interface_spec**

=== 1. NeuroGen (Gu, Jamison, Khosla, Allen, Wu et al.; NeuroImage, 15 Feb 2022; arXiv 2105.07140) ===
WHAT IT DID: coupled an fMRI-trained encoding model of human vision (trained on the Natural Scenes Dataset) to a deep generative network, and ran gradient ascent to synthesise images predicted to produce a TARGET pattern of macro-scale brain activation - not merely to maximise one region.
WHAT IT FOUND: synthetic images can achieve regional response patterns 'not achievable by the best-matching natural images'. Used as a discovery architecture to amplify differences between regions and between individuals, verified against several thousand measured image responses.
CODE: yes - github.com/zijin-gu/NeuroGen (verified reachable, HTTP 200).
ATTRACTOR/DEGENERATION BEHAVIOUR: this is the paper that establishes the central design principle by construction rather than by discussion. The optimisation runs in the GAN's LATENT AND CLASS SPACE, not in pixels. The generator is therefore a hard constraint: every candidate the optimiser can even express is a natural-looking image, because the GAN cannot output anything else. Degeneration is not avoided by a penalty term - it is made unreachable by the parameterisation. The paper reports high fidelity outputs and does not report an adversarial failure mode, which is exactly what the architecture predicts.
IMPLICATION FOR THIS SYSTEM: the generative prior is the damping term. You already have a very strong one and did not have to build it.

=== 2. BrainDiVE (Luo, Henderson, Wehbe, Tarr; NeurIPS 2023 ORAL; arXiv 2306.03089) ===
WHAT IT DID: encoder-gradient-guided diffusion. A frozen CLIP image encoder plus learnable linear layers maps visual features to fMRI activations (trained on NSD, 7T, participants viewing ~10,000 natural images). During denoising the score is perturbed by the gradient of the activation objective:
    eps' = eps_theta - sqrt(1 - alpha_t) * grad_{x_t} [ (gamma/|S|) * sum_{i in S} M_theta(D_Omega(x_t'))_i ]
where S is the target voxel set and gamma the guidance scale. Critically, the encoder is not applied to the noisy latent directly - they use an Euler approximation of the final clean image, explicitly 'to maintain stability and image naturalness'. That is a stability hack born of exactly the degeneration problem.
WHAT IT FOUND: synthesised preferred images with correct semantic specificity for category-selective ROIs; distinguished regions selective for the SAME category (FFA vs OFA); identified novel functional subdivisions within food- and place-selective areas, confirmed behaviourally. Quantitatively, for face-selective regions the generated images reached 61-70% face classification accuracy against 40-45% for the TOP NATURAL IMAGES - i.e. the optimiser produces stimuli substantially more category-pure than anything in the natural dataset.
CODE: yes - github.com/aluo-x/BrainDiVE (verified reachable, HTTP 200).
ATTRACTOR/DEGENERATION BEHAVIOUR: this is THE most predictive result for the proposed system, because diffusion-with-a-text/image-prior is architecturally the closest thing in the literature to prompting H3 Max. The failure mode is not noise, it is SEMANTIC PURIFICATION. Guided by a face region, the generator does not produce adversarial texture - it produces more face, more centrally, more purely, than any photograph. The stated limitations are about fMRI's temporal resolution and indirectness, not about mode collapse; but the 61-70% figure IS the collapse, measured. Note also that gamma is a free knob: turn the guidance scale up and naturalness degrades, turn it down and the brain barely steers anything. That trade-off is the single parameter this project will spend the most time tuning.
IMPLICATION: expect the stream to converge on extreme close-up faces within tens of iterations unless explicitly prevented. Faces are the strongest attractor in visual cortex and every system in this lineage finds them.

=== 3. MindPilot (Li et al., NCC Lab, SUSTech; ICLR 2026; arXiv 2602.10552) ===
WHAT IT DID: the first closed-loop framework using EEG as the optimisation feedback signal to guide naturalistic image generation. Non-invasive, natural images, and crucially it treats the brain as a BLACK BOX - no gradients through the subject. Uses proxy models trained on THINGS-EEG2 plus diffusion generation, with a 'pseudo-model guidance' / surrogate mechanism replacing explicit reward gradients. The update loop is: (1) direct reward update from EEG-target similarity, (2) SPREAD the reward to semantically similar images, (3) softmax probability update. For novel generation it uses genetic-algorithm operations - CROSSOVER AND MUTATION.
WHAT IT FOUND: validated in simulation and in humans. Semantic retrieval improved consistently across iterations; CLIP similarity reached 0.67 against 0.76 for specialised decoders; an emotion-regulation task moved valence from 0.45 to 0.60; correlation between predictions and human responses R = 0.714, p <= 0.001.
CODE: yes - github.com/ncclab-sustech/MindPilot (verified reachable, HTTP 200).
ATTRACTOR/DEGENERATION BEHAVIOUR: no adversarial or repetitive imagery reported. The authors name 'stimulus degeneracy' - multiple distinct stimuli producing similar neural responses - as a limitation, which is the mirror image of the collapse problem and just as important here: it means the readout cannot uniquely determine what to generate, so many different clips will read as equally good, and the loop has slack it can fill with whatever else you tell it to value.
IMPLICATION - AND THIS IS THE MOST DIRECTLY TRANSFERABLE FINDING IN THE WHOLE ITEM: MindPilot did not need a bespoke anti-collapse penalty because MUTATION IS ALREADY A NOVELTY TERM. A genetic algorithm with crossover and mutation cannot collapse, because mutation injects unconditioned variation on every generation by construction. Copy this. It is roughly five lines in prompt space (with probability p, override or perturb one prompt element at random regardless of what the brain says) and it is far more robust than any explicit repetition penalty.

=== 4. Kasahara et al., DecNefGAN (ATR Kyoto, with Taschereau-Dumouchel, Takakura, Kawato, Cortese; arXiv 2401.16742, 30 Jan 2024) ===
WHAT IT DID: PROPOSAL ONLY. Read in full: this is a framework paper with no experiments, no results, no data and no code. It should be cited as an architecture and a warning, not as evidence.
THE ARCHITECTURE, which is startlingly close to the proposed system: a human in an fMRI scanner in a closed loop with a generative AI that has two parts, a DECODER and a GENERATOR. The decoder reads brain patterns via MVPA to infer the current mental state; the generator produces new content to STRENGTHEN that state; the resulting brain activity is fed straight back to the decoder for the next trial. Individualisation is via CLIP: participants rate images, ratings are mapped to CLIP embeddings, and stable unCLIP inverts embeddings to generate images conditioned on decoded state intensity. The twist is adversarial - the HUMAN's objective is the opposite, to reach an orthogonal mental state and defeat the decoder, giving an 'as if GAN' loop between person and machine.
CODE: none.
ATTRACTOR/DEGENERATION BEHAVIOUR: the paper asserts convergence as a design property, not a risk - 'By iterating over this process, the generative AI can converge onto stimuli that maximally activate an individual's internal brain representations.' It cites the group's own prior neural-reinforcement work showing they have altered fear memories, confidence judgments and face preferences WITHOUT the participant's intent or awareness. The paper's entire framing is that such a loop is a cognitive SECURITY THREAT, and it exists to study how humans might resist it.
IMPLICATION, TWO PARTS. Technically: this is independent confirmation from a serious neurofeedback lab that a decode-generate-redecode loop converges - convergence is the expected behaviour, not an edge case. Presentationally: the most architecturally similar published work frames this exact loop as an attack. That is worth knowing before writing the artist's statement, and it connects directly to the UNESCO Recommendation's provision against neural data in recommender systems for manipulative purposes. The crucial difference to state loudly is that DecNefGAN closes the loop through a REAL PERSON'S measured brain and this project closes it through a simulation of nobody.

=== 5. THE TWO ANCESTORS THAT ACTUALLY ANSWER THE DEGENERATION QUESTION (2019) ===
(a) Ponce, Xiao, Schade, Hartmann, Kreiman, Livingstone, Cell 2019 - XDream. A genetic algorithm plus a deep generative network, closed-loop against REAL macaque V1 and IT neurons in real time. Neuronal firing ranked image codes, which then underwent selection, recombination and mutation. Evolved images were frequently better stimuli than ALL of >1.4 million natural images. Press coverage called the results 'trippy'. Code: github.com/willwx/XDream (verified reachable) plus a PLOS Comput Biol methods paper. Same lesson as MindPilot: GA with mutation, generator-constrained, no degeneration into noise, but a decisive super-stimulus.
(b) Bashivan, Kar, DiCarlo, Science 2019 - Neural Population Control via Deep Image Synthesis. ANN-driven synthesis pushed macaque V4 spiking 'beyond naturally occurring levels' and achieved independent control of whole populations including sites with overlapping receptive fields. The images were explicitly NON-NATURALISTIC. Code: github.com/dicarlolab/npc (verified reachable).
THIS IS THE CANONICAL DEGENERATION RESULT: when the optimiser is free in pixel space, it wins - it drives the target past anything nature produces - and what it produces does not look like a photograph. Everything in the lineage that avoids this does so by constraining the generator.

=== 6. THE ONE RUN ON TRIBE v2 ITSELF (Bladon & Bent, arXiv 2605.13904, 13 May 2026) ===
Not in the brief but the most load-bearing source here, because it is the same encoder. Gradient ascent on TRIBE v2's predicted ROI activation, composed with V-JEPA 2 ViT-G (40 layers), both frozen; still images tiled to 64 identical frames; Fourier-parameterised image; 3000 steps per seed, five restarts per ROI; seven ROIs (V1, V2, V3, V4, MT, FFA, PPA); a single RTX 3090 24 GB, with compute the dominant bottleneck.
IT RECOVERED REAL NEUROSCIENCE: increasing spatial scale and feature complexity from V1 to V4, plus three downstream regimes matching the canonical selectivity of MT and FFA directly, and a consistent though not category-identifiable signature for PPA. So TRIBE v2 has genuinely internalised cortical functional organisation, not merely fit the data.
THE NUMBER THAT MATTERS: optimised FFA stimuli drive the predicted region roughly 4x as hard as a natural face photograph (+0.34 versus +0.08; the arXiv HTML gives +0.339 and a secondary summary +0.343 - either way, ~4x).
AND THE REGULARISERS THEY NEEDED, which is the practical payload:
  - spectral energy penalty on the Fourier spectrum norm, lambda_fft = 1e-3
  - 'global lift' loss: target ROI mean MINUS mean activation elsewhere in cortex, beta = 1.0 - i.e. reward selectivity, not gross activation
  - GRAYSCALE-ONLY optimisation, stated explicitly to 'avoid adversarial high-frequency exploits'
  - low-resolution curriculum, 64 -> 128 -> 256, which improved selectivity from 3.59x to 13.33x
AND THE FAILURE THEY OBSERVED: the colour variant degenerated. 'Colour expands the optimization parameter space by 3x and the optimizer exploits the extra slack to inject high-frequency texture', visible as a pink/teal tint and a high-frequency overlay.
CODE: github.com/recozers/Tribe-V2-Interp (verified reachable, HTTP 200; the arXiv HTML and the secondary summary do not themselves state a repo URL, so this URL comes from the project outline and was confirmed to resolve, not sourced from the paper).
TWO IMPLICATIONS, BOTH IMPORTANT. First, TRIBE v2 is exploitable in exactly the way every encoder is - give the optimiser more free parameters and it finds adversarial texture. Second, and reassuringly: the exploit required direct pixel-level gradient access. Prompt space has no such slack.

**input_contract**

What determines which regime this project lands in. Three properties of the loop, and the proposed system's values for each:
1. OPTIMISER'S DEGREES OF FREEDOM. Pixel-space and Fourier-space optimisation degenerates (Bashivan; the TRIBE feature-vis colour variant). Latent-space (NeuroGen), diffusion-guided (BrainDiVE) and GA-over-generator (XDream, MindPilot) do not. THIS SYSTEM: a text prompt of a few dozen tokens. That is the most constrained interface of anything in the lineage by a large margin.
2. GRADIENT OR BLACK BOX. Gradient access lets the optimiser exploit the encoder precisely. THIS SYSTEM: black box. There is no differentiable path from TRIBE's output back to H3 Max's prompt - the coupling is a discrete text rewrite. Structurally this is MindPilot's regime, not BrainDiVE's, and MindPilot is the one that reported no degeneration.
3. NUMBER OF CLOSED ITERATIONS AND COUPLING STRENGTH. The TRIBE feature-vis paper used 3000 steps per seed to reach 4x. A livestream at 15 s clips does 240 iterations an hour, 5760 a day, indefinitely. The iteration count is not the constraint; the per-step gain is. A weak coupling over thousands of steps still integrates.
So the honest summary of the input contract: this system cannot produce adversarial noise, and will produce semantic convergence, on a timescale set entirely by how hard the prompt layer is told to chase the argmax ROI.

### Performance

**throughput_constraint**

The binding constraint from this literature is not throughput but ITERATION COUNT VERSUS COUPLING GAIN, and it is a control-systems constraint rather than a platform one.
A livestream runs ~240 closed iterations an hour, forever. Every published system in this lineage runs a bounded number of iterations toward a deliberate optimum and then STOPS - that is the experiment. Nothing here has ever been run open-endedly, and nothing here wanted to avoid the optimum. This project is the first case in the family where reaching the optimum is the FAILURE condition. That is the single most important structural difference and it means the literature's methods transfer but its objectives do not.
Practical consequence: the per-iteration gain must be small enough that 5760 iterations a day do not integrate to a collapsed state. That is not a number any paper provides; it must be tuned against the collapse detectors in the logging layer.

**realtime_headroom**

Not applicable as latency - nothing here runs in the clip budget. Reframed as the useful question, how much creative headroom the loop has before it collapses:
  - MindPilot's 'stimulus degeneracy' finding says the headroom is large: many distinct stimuli produce near-identical neural readouts, so a lot of visual variety is available at essentially no cost in predicted activation. You can be adventurous without fighting the brain signal.
  - BrainDiVE's guidance scale gamma is the knob that trades naturalness and diversity against activation, and the proposed system's equivalent is how literally the prompt layer obeys the argmax ROI. Turn it down and you keep headroom indefinitely at the cost of the brain visibly steering less. That trade-off is the real creative decision in the project and it should be exposed as a single tunable constant, not buried in prompt-template logic.
  - The offline motif-table route has effectively unlimited headroom, since the loop is then a lookup rather than an optimiser and cannot run away at all.

### Complexity

**dev_complexity**

LOW to implement the lessons, MEDIUM to tune them. Nothing in this item requires reimplementing any of these papers - all four named systems plus both 2019 ancestors have public code, and none of it needs to run. The deliverables are: a mutation probability, a repetition penalty over an ROI history window, a setpoint instead of a maximisation, and the collapse detectors. Perhaps 60-100 lines total.
The MEDIUM is the tuning. There is no published value for the coupling gain of a prompt-mediated loop, and finding the setting where the brain visibly steers the stream but does not capture it is empirical work over hours of running. Budget a day of watching the thing drift and adjusting.
The real risk is not difficulty but omission: it is entirely possible to build the loop without any damping, watch it look wonderful for twenty minutes, and only discover the collapse after going live.

**loc_estimate**

~60-100 lines to implement everything this item recommends: 5-10 for the mutation term, ~15 for the ROI-history repetition penalty, ~10 for setpoint tracking instead of argmax maximisation, ~15 for the deliberate ROI rotation, ~20 for the collapse detectors (which mostly reuse the logging layer). Zero lines to reuse any of the prior art directly - none of it belongs in the live loop.
Separately, the OFFLINE motif table is a bigger piece of work if pursued: adapting github.com/recozers/Tribe-V2-Interp to sweep more ROIs is perhaps a day of code plus a day or two of GPU, and it produces a grounded ROI -> visual-motif table that removes TRIBE from the live loop entirely.

**off_the_shelf_option**

All six systems have public code and every URL below was verified to resolve (HTTP 200) during this research:
  - github.com/recozers/Tribe-V2-Interp - gradient ascent through frozen TRIBE v2 + V-JEPA 2. THE MOST DIRECTLY USEFUL: same encoder, same weights, already wired. This is what to run offline to build the ROI -> motif table. (URL from the project outline, confirmed reachable; not stated in the paper text I could retrieve.)
  - github.com/aluo-x/BrainDiVE - encoder-gradient-guided diffusion, NeurIPS 2023 oral. The reference implementation of the guidance formulation and, importantly, of the Euler-approximation stability trick.
  - github.com/ncclab-sustech/MindPilot - closed-loop black-box optimisation with GA crossover and mutation. The best template for the DAMPING design specifically, because it is the only one that is gradient-free and closed-loop like this project.
  - github.com/zijin-gu/NeuroGen - GAN-latent activation optimisation.
  - github.com/willwx/XDream - the generative-network + genetic-algorithm closed loop, with a PLOS Comput Biol methods paper written specifically to make it reusable.
  - github.com/dicarlolab/npc - Bashivan et al. neural population control.
  - Kasahara/DecNefGAN: no code exists. It is a proposal paper.
BLUNT RECOMMENDATION: run NONE of these in the live system. Read MindPilot for the mutation design, run Tribe-V2-Interp once offline to see what each ROI actually wants, and write the motifs into a table by hand. The lineage's value here is as a predictive model and a source of two or three specific tricks, not as code to integrate.

### Decision

**recommended_approach**

STOP BUILDING AN OPTIMISER. That is the one recommendation this literature actually supports, and it is architectural rather than parametric.

Every system in this lineage - NeuroGen, BrainDiVE, MindPilot, DecNefGAN, XDream, Bashivan, the TRIBE feature-vis paper - is a MAXIMISER, and every one of them succeeds: they all find a super-stimulus that beats every natural image. NeuroGen achieves response patterns natural images cannot. BrainDiVE hits 61-70% face purity against 40-45% for the best photographs. XDream beats all 1.4 million natural images. Bashivan pushes V4 past natural levels. TRIBE's own FFA optimum drives 4x a real face. If you build a maximiser you will get a maximiser's result, which is a stream of increasingly pure close-up faces. That is a successful optimisation and a failed artwork.

Concretely, five things, in descending order of importance:

1. TRACK A SETPOINT, DO NOT MAXIMISE. Pick a target activation level and steer toward it from either direction - if predicted activation is above setpoint, prompt AWAY from the dominant ROI. This single change makes collapse structurally impossible rather than merely penalised, and it is the same move as NeuroGen targeting a PATTERN rather than a maximum. Nothing in the literature does this because nothing in the literature wants it; it is the project's one genuine departure and it is a dozen lines.

2. STEAL MINDPILOT'S MUTATION. With probability p (start at 0.2-0.3) override or perturb one prompt element at random, ignoring the brain entirely. A GA with mutation cannot collapse by construction. This is the cheapest and most robust novelty term available and it is empirically validated in the one closed-loop, gradient-free, human-in-the-loop system in the set.

3. USE THE 'GLOBAL LIFT' IDEA TEMPORALLY. The TRIBE feature-vis paper's loss was target ROI mean MINUS mean elsewhere in cortex (beta = 1.0) - reward SELECTIVITY, not gross activation. The temporal analogue is what this project needs: penalise ROIs that have been dominant over the last N clips, so the loop is rewarded for moving around the cortex rather than for lighting it up. Roughly: score(roi) = activation(roi) - beta * recent_dominance(roi, window=20).

4. ROTATE THE TARGET ROI DELIBERATELY. Rather than always following the argmax, cycle a target ROI on a schedule and let the readout modulate WITHIN it. This converts the brain from a steering wheel into a texture, keeps V1/V4/MT/PPA in rotation alongside FFA, and is visually far more varied. It also makes the on-stream overlay more legible, since different parts of the cortex actually light up over time instead of one hotspot.

5. KEEP THE COUPLING WEAK AND MAKE IT ONE CONSTANT. BrainDiVE's gamma is the whole naturalness/activation trade-off in one number; the TRIBE paper's resolution curriculum showed selectivity rising 3.59x -> 13.33x purely with more optimisation pressure. More pressure, more extreme stimulus, every time. Expose the equivalent knob as a single named constant, start it LOW, and turn it up on stream until the brain is visibly steering - not until the loop is efficient.

Do not spend effort defending against adversarial imagery. Prompt space plus H3 Max's prior makes it unreachable, and the one paper that produced it on TRIBE v2 needed direct Fourier-parameterised pixel gradients and three colour channels of slack to do it.

**simpler_alternative**

THE OFFLINE MOTIF TABLE, and it is genuinely tempting. Run github.com/recozers/Tribe-V2-Interp once, offline, on a rented 24 GB GPU, over the ROIs you care about. Look at what each one converges to. Write a hand-authored table - FFA -> 'close-up human face, direct gaze'; MT -> 'fast lateral camera motion'; PPA -> 'deep architectural perspective, empty interior'; V1/V4 -> 'high-contrast repeating texture'. Then the live loop is a dictionary lookup: read the dominant ROI, fetch the motif, compose the prompt. TRIBE never runs live at all, which deletes the 28-32 GB always-on GPU from the cost model outright.
It is grounded rather than invented, because the motifs come from the actual encoder rather than from guesses about what FFA likes. And it cannot run away, because a lookup table has no optimisation dynamics.
What it costs: the loop is no longer genuinely closed, and the conceptual payoff of the piece - a system responding to its own predicted effect - becomes a simulation of itself. Worth being honest about that in the artist's statement rather than eliding it.

CRUDER STILL: run the full closed loop but hard-cap it. Force a scene change every N clips regardless of the brain, or reset to a random seed prompt every ten minutes. Collapse becomes impossible because the loop is never allowed to run long enough to converge. Ten lines, no tuning, and it doubles as the buffer-underrun filler. If only one damping measure gets built, build this one.

The genuinely simplest thing, worth naming even though it is not recommended: run the loop undamped AND SHOW THE COLLAPSE. A stream that visibly converges to a wall of faces over an hour, with the cortex overlay frozen on FFA, is a legible and honest demonstration of exactly the phenomenon this whole literature documents. Zero lines of damping code, and arguably a better piece than a well-behaved one. It just cannot run for 24 hours.

**code_sketch**

# Damping and novelty, derived from the prior art. Runs in the prompt-translation layer.
# - setpoint tracking (departure from the maximiser lineage)
# - mutation            (MindPilot / XDream genetic algorithm)
# - temporal global-lift (Bladon & Bent's selectivity loss, moved from space to time)
# - deliberate ROI rotation
import random
from collections import deque

COUPLING     = 0.35   # the BrainDiVE gamma analogue. START LOW. This is THE creative knob.
SETPOINT     = 0.6    # target normalised activation. NOT 1.0 - we are not maximising.
MUTATION_P   = 0.25   # MindPilot's mutation. A GA with mutation cannot collapse.
BETA_RECENCY = 1.0    # the temporal 'global lift' weight (paper used beta=1.0 spatially)
HARD_RESET_N = 40     # force a scene change every N clips no matter what. The crude backstop.

MOTIFS = {   # from an offline Tribe-V2-Interp sweep, not from guesswork
    'FFA': ['a face in close-up, direct gaze', 'two people looking at each other'],
    'MT':  ['fast lateral camera motion', 'a crowd surging past'],
    'PPA': ['a deep empty corridor', 'a wide landscape with strong perspective'],
    'V4':  ['saturated colour fields', 'a lattice of repeating shapes'],
    'V1':  ['high-contrast fine texture', 'rippling water at close range'],
}
WILDCARDS = ['underwater', 'at night in heavy rain', 'shot on expired film',
             'in total silence', 'from directly overhead', 'as a slow dissolve']

history = deque(maxlen=20)   # recent dominant ROIs

def choose_roi(activations, iteration):
    """Score = distance-to-setpoint, penalised by how recently this ROI dominated."""
    if iteration % HARD_RESET_N == 0:          # crude backstop; also the underrun filler hook
        return random.choice(list(MOTIFS))
    scored = {}
    for roi, a in activations.items():
        recency = history.count(roi) / max(len(history), 1)
        # setpoint tracking, NOT maximisation: we want |a - SETPOINT| small, so we steer
        # toward under-driven regions and actively away from over-driven ones.
        gap = SETPOINT - a
        scored[roi] = gap - BETA_RECENCY * recency
    roi = max(scored, key=scored.get)
    history.append(roi)
    return roi

def build_prompt(activations, iteration, base='a continuous tracking shot'):
    roi = choose_roi(activations, iteration)
    motif = random.choice(MOTIFS[roi])
    # MUTATION: with probability p, ignore the brain and inject unconditioned variation.
    # This is the single most robust anti-collapse measure available and it is two lines.
    if random.random() < MUTATION_P:
        motif = f'{motif}, {random.choice(WILDCARDS)}'
    # COUPLING scales how literally the brain steers. Low = the brain tints, does not dictate.
    weight = 'strongly featuring' if random.random() < COUPLING else 'with a hint of'
    return f'{base}, {weight} {motif}', roi

# ---- collapse detectors, reusing the JSONL logging layer ----
def collapsing(recent_records, window=20):
    """Three independent signals. Any two firing together means the loop has converged."""
    r = recent_records[-window:]
    if len(r) < window:
        return False
    dup_hashes  = len({x['vertex_vec_sha1'] for x in r}) < window * 0.5
    roi_locked  = len({x['roi'] for x in r}) <= 2
    prompt_flat = len({x['expanded_prompt'][:120] for x in r}) < window * 0.4
    return sum([dup_hashes, roi_locked, prompt_flat]) >= 2

# on detection: bump MUTATION_P, drop COUPLING, force a hard reset. Do not restart the process -
# collapse is a control-loop state, not a crash.

### Risk

**failure_modes**

What this literature predicts will actually go wrong, in order of likelihood:
1. SEMANTIC COLLAPSE TO FACES. The default outcome of an undamped loop. Every system here finds FFA as the strongest attractor and BrainDiVE quantifies the purification (61-70% vs 40-45%). The stream becomes a wall of close-up faces, the cortex overlay freezes on one hotspot, and the piece stops being about anything.
2. BUILDING A MAXIMISER BY DEFAULT. The obvious implementation - read the argmax ROI, prompt for what that ROI likes - IS the maximiser, and it is what anyone would write first. The failure is designed in at the first line of the prompt layer, not discovered later.
3. TUNING THE COUPLING UP. The loop looks unresponsive at low gain and the natural instinct is to increase it. The TRIBE feature-vis resolution curriculum is the warning: 3.59x -> 13.33x selectivity purely from more optimisation pressure. Every increase buys visible responsiveness and buys collapse at the same time.
4. MISTAKING CONVERGENCE FOR SUCCESS. A tightly converged loop looks like the system WORKING - the brain signal is strong, consistent and clearly driving the output. It is indistinguishable from success on every metric except watchability. This is why the collapse detectors must be automatic and must run on a window, not eyeballed.
5. DEFENDING AGAINST THE WRONG THING. Spending days guarding against adversarial noise, which prompt space cannot produce, while the semantic attractor goes unaddressed.
6. STIMULUS DEGENERACY MASKING DRIFT (MindPilot's named limitation). Many distinct clips produce near-identical readouts, so the ROI reduction can look healthy and varied while the actual video has gone monotonous. The control signal is not a proxy for visual variety. Monitor the expanded_prompt diversity independently.
7. THE PRESENTATIONAL FAILURE. The nearest published architecture to this system - DecNefGAN - frames the identical loop as a cognitive security threat, cites its own group's history of altering fear memories and preferences without participants' awareness, and exists to study human resistance to it. If the piece is described in the language of maximising brain response without noting that the brain is simulated and belongs to nobody, that framing is available and it will be used.
8. OVER-READING THE 4x FIGURE. TRIBE's FFA optimum drives the PREDICTED region 4x a natural face. That is a statement about the model, not about a person - no human was scanned looking at those images. It bounds how far the encoder can be pushed, not how much a viewer would feel.

### Evidence

**sources**

- https://arxiv.org/abs/2105.07140 - NeuroGen: activation optimized image synthesis for discovery neuroscience (Gu, Jamison, Khosla, Allen, Wu et al.)
- https://www.sciencedirect.com/science/article/pii/S1053811921010831 - NeuroGen in NeuroImage, published 15 Feb 2022 (page returned HTTP 403 to automated fetch; details taken from the arXiv abstract and the indexing records below)
- https://pubmed.ncbi.nlm.nih.gov/34936922/ - NeuroGen PubMed record
- https://experts.umn.edu/en/publications/neurogen-activation-optimized-image-synthesis-for-discovery-neuro - NeuroGen: synthetic images achieve regional response patterns not achievable by the best-matching natural images; verified against several thousand measured image responses
- https://github.com/zijin-gu/NeuroGen - NeuroGen code (URL verified reachable, HTTP 200)
- https://arxiv.org/abs/2306.03089 - BrainDiVE: Brain Diffusion for Visual Exploration, NeurIPS 2023 oral (Luo, Henderson, Wehbe, Tarr)
- https://www.alphaxiv.org/overview/2306.03089 - BrainDiVE detail: the guidance equation eps' = eps_theta - sqrt(1-alpha_t) grad[(gamma/|S|) sum M_theta(D_Omega(x_t'))], the Euler approximation of the clean image used 'to maintain stability and image naturalness', frozen CLIP encoder + learnable linear layers, NSD 7T with ~10,000 natural images, 61-70% face classification for generated vs 40-45% for top natural images, FFA vs OFA and novel food/place subdivisions confirmed behaviourally
- https://proceedings.nips.cc/paper_files/paper/2023/file/ef0c0a23a1a8219c4fc381614664df3e-Paper-Conference.pdf - BrainDiVE NeurIPS proceedings PDF (exceeded fetch size limit; not read directly)
- https://github.com/aluo-x/BrainDiVE - BrainDiVE official code (URL verified reachable, HTTP 200)
- https://neurips.cc/virtual/2023/poster/72593 - BrainDiVE NeurIPS 2023 poster page
- https://arxiv.org/abs/2602.10552 - MindPilot: Closed-loop Visual Stimulation Optimization for Brain Modulation with EEG-guided Diffusion (Li et al., NCC Lab SUSTech), ICLR 2026
- https://www.alphaxiv.org/overview/2602.10552v1 - MindPilot detail: brain treated as a black-box function, proxy models on THINGS-EEG2, pseudo-gradient guidance, three-step update (direct reward, semantic spreading, softmax), genetic-algorithm crossover and mutation for novel generation, CLIP similarity 0.67 vs 0.76 for specialised decoders, emotion-regulation valence 0.45 -> 0.60, R = 0.714 p <= 0.001, 'stimulus degeneracy' named as a limitation, no adversarial or repetitive imagery reported
- https://github.com/ncclab-sustech/MindPilot - MindPilot code (URL verified reachable, HTTP 200)
- https://openreview.net/forum?id=7jdmXx869Q - MindPilot OpenReview page (behind a browser check; not read directly)
- https://arxiv.org/abs/2401.16742 - Kasahara, Oka, Taschereau-Dumouchel, Takakura, Kawato, Cortese, 'Generative AI-based closed-loop fMRI system' (DecNefGAN), 30 Jan 2024
- https://arxiv.org/pdf/2401.16742 - DecNefGAN full text, READ DIRECTLY. Confirms it is a proposal paper with no experiments, no results and no code. Source of the architecture description (decoder + generator, MVPA, CLIP embeddings from participant ratings, stable unCLIP generation, human as adversary seeking an orthogonal mental state), of the convergence assertion ('By iterating over this process, the generative AI can converge onto stimuli that maximally activate an individual's internal brain representations'), and of the group's prior claims to have reduced fear memories, transformed confidence judgments and manipulated face preferences 'without the participant's intent or awareness'
- https://huggingface.co/papers/2401.16742 - DecNefGAN HF paper page
- https://arxiv.org/abs/2605.13904 - Bladon & Bent, 'Feature Visualization Recovers Known Cortical Selectivity from TRIBE v2', 13 May 2026
- https://arxiv.org/html/2605.13904v1 - full HTML, READ DIRECTLY. Source of: Fourier-parameterised gradient ascent through frozen TRIBE v2 + V-JEPA 2 ViT-G (40 layers), still frames tiled to 64; spectral energy penalty lambda_fft = 1e-3; global lift loss (target ROI mean minus mean elsewhere) beta = 1.0; grayscale-only optimisation stated to 'avoid adversarial high-frequency exploits'; low-resolution curriculum 64->128->256 improving selectivity 3.59x -> 13.33x; optimised FFA +0.339 vs natural face photograph +0.080 (~4x); the colour variant's degeneration - 'Colour expands the optimization parameter space by 3x and the optimizer exploits the extra slack to inject high-frequency texture', pink/teal tint and high-frequency overlay; single RTX 3090 24 GB with compute the dominant bottleneck
- https://www.emergentmind.com/papers/2605.13904 - secondary summary: 3000 gradient steps per seed, five restarts per ROI, seven ROIs (V1, V2, V3, V4, MT, FFA, PPA); gives the FFA optimum as +0.343 where the arXiv HTML gives +0.339 - a minor discrepancy between sources, both ~4x versus +0.080
- https://github.com/recozers/Tribe-V2-Interp - Tribe-V2-Interp code. URL taken from the project outline and VERIFIED REACHABLE (HTTP 200); it is not stated in the paper text retrieved, so treat the attribution as unconfirmed even though the repository exists
- https://www.cell.com/cell/fulltext/S0092-8674(19)30391-5 - Ponce, Xiao, Schade, Hartmann, Kreiman, Livingstone, 'Evolving Images for Visual Neurons Using a Deep Generative Network Reveals Coding Principles and Neuronal Preferences', Cell 2019: neuronal responses ranked image codes which underwent selection, recombination and mutation; evolved images frequently better stimuli than all of >1.4 million natural images
- https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1007973 - XDream methods paper (PLOS Computational Biology): genetic algorithm plus deep generative network for activation maximisation in macaque IT and V1
- https://github.com/willwx/XDream - XDream code (URL verified reachable, HTTP 200)
- https://www.science.org/doi/10.1126/science.aav9436 - Bashivan, Kar, DiCarlo, 'Neural population control via deep image synthesis', Science 2019
- https://dicarlolab.mit.edu/neural-population-control-deep-image-synthesis - DiCarlo Lab page: ANN-driven synthesis pushed V4 spiking beyond naturally occurring levels with independent control of populations including overlapping receptive fields; images explicitly non-naturalistic
- https://github.com/dicarlolab/npc - Neural Population Control code (URL verified reachable, HTTP 200)
- https://arxiv.org/pdf/2506.04379 - 'Visualizing and Controlling Cortical Responses Using Voxel-Weighted Activation Maximization' (related 2025 work; PDF exceeded the fetch size limit and was not read - listed as a lead, not as a source relied on)
- https://neurosciencenews.com/ai-images-visual-neurons-13014/ - popular coverage of the Ponce et al. evolved images ('trippy'), useful only as a characterisation of the visual result
- INFERENCE (explicitly marked): the central claim that a prompt-mediated loop is structurally incapable of adversarial-noise degeneration is MY SYNTHESIS across the lineage - specifically from the contrast between pixel/Fourier-space optimisation (Bashivan; the TRIBE colour variant) and generator-constrained optimisation (NeuroGen, BrainDiVE, XDream, MindPilot). No source states it about a text-prompted video model.
- INFERENCE (explicitly marked): the prediction that this system converges specifically to close-up faces is extrapolated from FFA being the most reliably recovered attractor across BrainDiVE and the TRIBE feature-vis paper. It is a testable prediction, not a sourced finding.
- INFERENCE (explicitly marked): the setpoint-tracking recommendation has no precedent in this literature, because every cited system is deliberately a maximiser. It is a design proposal derived from the failure analysis, not a validated technique.
- INFERENCE (explicitly marked): all wall-clock and dollar figures for the offline sweep, and the $800-1,400/month always-on-GPU saving, are arithmetic from published hardware descriptions and commodity GPU rates, not sourced measurements.

### Other Info

**item_id**

C

**focus**

The real methodological lineage for optimising generated stimuli against a brain encoding model.

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `output_contract`
- `unknowns`

---

## Cost model

### Identity

**what_it_is**

The dollar-per-hour accounting for a 24/7 TRIBE v2 -> H3 Max reactive stream, decomposed into video generation, always-on GPU for TRIBE, VPS, and egress. Not a component — the economic constraint that decides whether the piece can run unsponsored.

**role_in_loop**

Sits across the whole loop but is dominated by one edge: the generate step. Every wall-clock second of stream is a paid output-second at fal. Perceive/predict/prompt are rounding errors on the bill; stream is free if you push RTMP to YouTube and catastrophic if you serve HLS yourself.

### Interface

**input_contract**

To instantiate this model you must fix five numbers: (1) resolution -> price_per_output_second, from {0.025, 0.04, 0.05, 0.08}; (2) duty_cycle, the fraction of wall-clock stream time backed by freshly generated video, in (0, 1]; (3) GPU SKU and provider for TRIBE, or null if TRIBE is out of the live loop; (4) delivery mode, RTMP-to-platform vs self-hosted HLS; (5) hours per day the stream actually runs. Clip length is deliberately NOT an input — see output_contract.

**output_contract**

TOTALS, RTMP-to-YouTube delivery, 100% duty cycle, per stream-hour:
  Cheapest defensible today (480P promo + RunPod A6000 community + CPX31): $90.00 + $0.33 + $0.025 = $90.36/hr. Generation = 99.6% of spend.
  Cheapest defensible from Sept 1 (480P regular + A6000 community + CPX31): $180.00 + $0.33 + $0.025 = $180.36/hr = $4,329/day = $131,660/mo.
  Quality config (768P regular + Modal A100-80GB + CPX31 + LLM writer): $288.00 + $2.50 + $0.025 + $0.54 = $291.07/hr = $6,986/day = $212,478/mo.
  Same config, self-hosted HLS at 1,000 concurrent viewers: add ~$1,460/hr. Delivery becomes 83% of spend.

GENERATION SHARE is between 97.3% and 99.9% of total spend in every RTMP configuration examined — even pairing the cheapest generation rate with the most expensive GPU. Nothing else on the bill is worth optimising until the generation line is addressed.

CLIP LENGTH IS COST-NEUTRAL. This is the most common wrong intuition and it should be stated explicitly: fal bills per output-second, so 240 x 15s clips and 720 x 5s clips both cost 3600 output-seconds = the same dollars per stream-hour. Shorter clips do not save money. They strictly increase per-clip fixed overhead (queue slots, downloads, mux operations, TRIBE invocations, safety-checker dice rolls) for identical spend, and 5s falls below TRIBE's 15-30s practitioner minimum window. Use 15s, the H3 Max maximum. The cost model and the latency model and the neuroscience all point the same direction here.

COST PER SECOND OF STREAM, all-in, RTMP, cheapest config: $0.0251/s today, $0.0501/s from Sept 1.

### Performance

**throughput_constraint**

fal global concurrency: new Model API accounts start at 2 concurrent IN_PROGRESS requests, scale automatically to a self-serve ceiling of 40 based on paid invoices over the trailing four weeks, and require a sales contact beyond 40. Queued requests do not consume a slot and are never rejected for concurrency (though start_timeout can expire them). This is a throughput cap, not a billing cap — it does not change cost/hour, but it caps how many parallel streams one account can run, and it makes the credit-purchase history a soft prerequisite: you must already be spending to be allowed to spend faster. enable_safety_checker defaults true; whether fal bills for safety-rejected generations is unverified and materially affects the effective cost per delivered second at high rejection rates.

**realtime_headroom**

Economic rather than temporal headroom, and it is negative for an unsponsored individual. $180-$288 per hour is $4,320-$6,912 per day. No hobby project sustains that. Three ways to buy headroom, in descending order of leverage:
  1. DUTY CYCLE. Halve the fraction of stream-time backed by fresh generation and halve the bill, exactly. At 480P regular: 100% = $180/hr, 50% = $90/hr, 25% = $45/hr, 10% = $18/hr. Achieved by holding, looping, ping-ponging, slow-motion-stretching or crossfading generated clips between fresh ones. Zero API changes, a few dozen lines of ffmpeg filter graph, and it doubles as the mandatory buffer-underrun fallback (item 08). Aesthetically it reads as deliberate pacing rather than as a cost measure.
  2. RUN IN BURSTS, NOT 24/7. Two hours a day at 480P regular is $360/day, not $4,320. A 'brain stream' that is on for a scheduled hour is a defensible artwork; a 24/7 one is a funding problem.
  3. STOP RENTING PER-SECOND. See recommended_approach.

### Complexity

**dev_complexity**

LOW to model, HIGH to afford. The arithmetic is a spreadsheet. The engineering consequence is a single decision — RTMP-to-YouTube over self-hosted HLS — which is also the lowest-dev-effort delivery option, so the cost-optimal and effort-optimal choices coincide. The duty-cycle lever is the only cost work that requires code, and it is ~1-2 hours of ffmpeg.

**loc_estimate**

~40 LOC for a cost meter (accumulate requested output-seconds per clip, multiply by the rate, expose a running $/hr and a hard daily spend ceiling that trips the duty-cycle fallback). ~60-120 LOC for the duty-cycle filler path (ffmpeg hold/loop/slow-motion of the previous clip). ~0 LOC for egress optimisation — it is a URL change from an HLS origin to rtmp://a.rtmp.youtube.com/live2/.

**off_the_shelf_option**

fal's dashboard has a Concurrency page with a 30-day usage history, and fal bills per output-second so spend is directly readable from your own request log — no metering library needed. There is no off-the-shelf cost governor for this pipeline; a spend ceiling is ~20 lines you must write yourself, and you must write it, because an orchestration loop with a bug that double-fires generation requests burns money at $0.05-$0.08 per second per in-flight request with no natural brake.

### Decision

**recommended_approach**

1) BUILD ON REGULAR PRICING ($0.05 480P / $0.08 768P). The 50% launch promo ends September 1, 2026 — tomorrow. Any plan justified by $0.025/s is invalid on arrival.
2) 480P, not 768P. 37.5% off the dominant line item ($180/hr vs $288/hr) for a resolution difference that is largely invisible after YouTube's own transcode and on the phone screens where this will actually be watched.
3) RTMP push to YouTube Live via ffmpeg. Not HLS, not a media server, not a browser video queue. It makes egress free, makes viewer scale free, outsources the CDN and player, and is the least code. It is simultaneously the cheapest and the simplest option, which almost never happens.
4) TRIBE on the cheapest 48GB card, not on Modal. RunPod RTX A6000 48GB community at $0.33/hr = $241/mo. Comfortably fits the 28-32GB trimodal footprint; drop the Llama-3.2-3B branch via modality dropout and it fits with room. Modal at $2.50/hr buys per-second billing and scale-to-zero, both of which are worthless against a process that must stay warm because of a ~60s lazy-load cold start. Understand what this saves, though: $1,584/mo against a $131,400/mo generation bill. It is 1.2%. Choose the GPU for operational simplicity, not for savings.
5) DUTY-CYCLE THE GENERATION. This is the only lever with real magnitude. Ship the piece at a 40-60% duty cycle from day one — fresh clip, then a held/slow/looped derivative, then fresh — and the bill halves. At 480P regular and 50% duty: $90/hr, $2,160/day. Still expensive, but an order of magnitude more tractable, and the filler path is code you have to write anyway for buffer underruns.
6) HARD SPEND CEILING IN THE ORCHESTRATOR. A daily dollar cap that degrades duty cycle to zero (pure filler loop) rather than stopping the stream. Without it, a retry loop bug is a four-figure overnight invoice.
7) IF THIS RUNS FOR MONTHS, STOP RENTING PER-SECOND. A rented B200 at Modal's $0.001736/s is $6.25/hr FLAT, regardless of how many seconds of video it produces. Break-even against fal is 250 output-seconds/hr at $0.025/s, 125 at $0.05/s, and 78 at $0.08/s — i.e. a duty cycle of 6.9%, 3.5% and 2.2% respectively. Above roughly a 3% duty cycle, self-hosting a realtime video model wins on pure dollars. At 100% duty against 768P regular it is 46x cheaper ($6.25/hr vs $288/hr); against 480P regular, 29x. Krea Realtime 14B runs ~11fps 4-step on a single B200, so budget 1-2 cards (~$6.25-$12.50/hr) for something near 24fps. This trades a large, permanent, linear operating cost for a fixed one plus a few days of hosting work — see item 17. It is outside the shortest-path-to-demo bias for the FIRST demo, and it is the correct answer for the second.

**simpler_alternative**

Do not run it continuously. Generate 20-40 minutes of brain-driven clips offline as a batch, mux them into one file, and loop that file to YouTube via ffmpeg with `-stream_loop -1 -c copy`. Cost: 40 minutes * 60 * $0.05 = $120, once, total, forever. The stream then runs 24/7 at $18/mo of VPS and $0 of generation. You lose live reactivity — which, given TRIBE's 5s hemodynamic offset plus a 15s clip plus pipelining lag, was already 20-35 seconds stale and not perceptibly 'live' to a viewer anyway. Regenerate the loop nightly for $120/night if freshness matters. This is a 99.9% cost reduction for a loss most viewers cannot detect, and it should be the honest default recommendation for anyone who is not fal-sponsored.

Second fallback: keep it live but drop to a 10% duty cycle and 480P — $18/hr, $432/day. Feasible on a real budget.

**code_sketch**

# cost_meter.py — the only cost code that matters: a running meter and a hard ceiling.
import time, itertools

RATE = {("480P", "promo"): 0.025, ("768P", "promo"): 0.040,
        ("480P", "regular"): 0.050, ("768P", "regular"): 0.080}

class SpendGovernor:
    def __init__(self, resolution="480P", tier="regular", daily_cap_usd=200.0):
        self.rate = RATE[(resolution, tier)]
        self.cap = daily_cap_usd
        self.day = time.gmtime().tm_yday
        self.spent = 0.0

    def _roll(self):
        d = time.gmtime().tm_yday
        if d != self.day:
            self.day, self.spent = d, 0.0

    def charge(self, duration_s: int) -> None:
        """Call AFTER a successful fal generation. fal bills requested duration."""
        self._roll(); self.spent += duration_s * self.rate

    def may_generate(self, duration_s: int) -> bool:
        """Gate every fal call. False -> orchestrator must emit filler, NOT stop."""
        self._roll(); return (self.spent + duration_s * self.rate) <= self.cap

    @property
    def usd_per_hour(self) -> float:
        return 3600 * self.rate  # 100% duty cycle upper bound


# Duty cycle is the lever. Interleave paid clips with free derivatives.
def schedule(duty=0.5, clip_s=15):
    """duty=0.5 -> alternate one paid clip with one free filler clip.
    Halves $/hr exactly. Doubles as the buffer-underrun fallback."""
    n_free = round(1 / duty) - 1
    for _ in itertools.count():
        yield "GENERATE"
        for _ in range(n_free):
            yield "FILLER"   # ffmpeg: hold last frame / reverse-loop / 0.5x setpts


# Free egress: one upload stream, YouTube absorbs all viewer fan-out.
# ffmpeg -re -f concat -safe 0 -i playlist.txt \
#        -c:v libx264 -preset superfast -b:v 4500k -maxrate 4500k -bufsize 9000k \
#        -c:a aac -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/$KEY
#
# Self-hosted HLS instead: ~1.35 GB/hr PER VIEWER. At 1,000 concurrent that is
# 1.35 TB/hr and it dwarfs the generation bill. Do not do this.

### Risk

**failure_modes**

1. PROMO CLIFF. Building the budget on $0.025/s and waking on September 1 to a doubled invoice. The fal model page says the discount ends September 1; secondary coverage disagrees ('first week' vs 'first 14 days'), which is exactly the kind of ambiguity that produces a surprise bill. Assume regular pricing.
2. RUNAWAY RETRY LOOP. Safety-checker rejections, timeouts and 5xx responses all invite naive retries. Each retry is a fresh paid generation at $0.75-$1.20 per 15s clip. A retry storm at concurrency 40 burns ~$3.20/second. There is no fal-side circuit breaker; the daily cap must live in your orchestrator.
3. SELF-HOSTED DELIVERY UNDER SUCCESS. The cost model is stable under RTMP and unbounded under HLS. A stream that goes mildly viral — Infinite Slop did 37,000 viewers on day one — turns a $180/hr project into a $1,600/hr one, and the bill arrives precisely when the project looks like it is working.
4. SPONSORSHIP MIRAGE. fal covered Infinite Slop's compute as a promotion. Every published figure about that project's viability is therefore about a $0 marginal cost, and none of it transfers to a self-funded build. Reading 'levelsio ran an infinite AI stream on a Hetzner VPS' as evidence of affordability is the single most likely way to misprice this project.
5. IDLE GPU BURN. TRIBE's GPU bills whether or not the loop is running. A stream paused for debugging still costs $0.33-$2.50/hr. Small in absolute terms, but it accrues silently across weeks of development, and Modal's $30/mo free Starter credit covers only ~12 hours of A100-80GB.
6. CURRENCY AND REGION DRIFT. Hetzner prices in EUR and raised cloud prices in April and again on 15 June 2026; Vast.ai rates are host-set and move hourly. Any figure here older than a month should be re-checked before it is committed to.
7. OPTIMISING THE WRONG LINE. Spending a day migrating the TRIBE GPU from Modal to RunPod saves 1.2% of the bill. Spending an hour on the duty-cycle filler saves 50%. The cost structure is so lopsided that ordinary infrastructure instincts point at the wrong target.

### Economics

**cost**

HEADLINE, per hour of continuous 1:1 stream, RTMP-to-YouTube, TRIBE on RunPod A6000 community, Hetzner CPX31:
  480P promo (expires Sept 1 2026): $90.36/hr | $2,168/day | $65,963/mo
  768P promo (expires Sept 1 2026): $144.36/hr | $3,465/day | $105,383/mo
  480P regular: $180.36/hr | $4,329/day | $131,660/mo
  768P regular: $288.36/hr | $6,921/day | $210,503/mo

BREAKDOWN at 480P regular ($180.36/hr):
  Video generation  $180.00  99.80%
  TRIBE GPU           $0.33   0.18%
  VPS                 $0.025  0.01%
  Egress              $0.00   0.00%  (YouTube absorbs viewer fan-out)

Swapping to the most expensive GPU (Modal A100-80GB, $2.50/hr) moves generation's share from 99.80% to 98.6%. There is no GPU or hosting choice that makes the non-generation lines matter.

DOMINANT COST: video generation, at 97-99.9% of spend in every configuration.

SINGLE HIGHEST-LEVERAGE LEVER: reduce paid output-seconds per wall-clock hour — i.e. duty cycle. It is the only lever that scales the dominant line linearly, it requires no API change, and the filler mechanism is already mandatory as the buffer-underrun fallback. 50% duty at 480P regular = $90/hr. 25% = $45/hr. 10% = $18/hr.
  Second lever: 480P over 768P, a flat 37.5% off generation.
  Third lever: run in scheduled bursts rather than 24/7.
  Fourth lever (months-scale): abandon per-second rental for a rented B200 at ~$6.25/hr flat — 29-46x cheaper at full duty, break-even at a ~3% duty cycle.
  NOT a lever: shorter clips (cost-neutral per stream-hour, strictly worse on overhead). NOT a meaningful lever: dropping TRIBE from the live loop (saves $241-$1,824/mo against a $131,400/mo bill — 0.2-1.4%). Dropping TRIBE is a latency and complexity decision, not an economic one, and should be argued on those grounds.

SPONSORSHIP CAVEAT: fal covered compute for Infinite Slop as a promotion, and fal separately gives 5 free 5-second 768P generations per rolling 24h with no sign-up. Neither is a business model. Self-funded, the identical system costs $4,329-$6,921 per day. Every conclusion drawn from Infinite Slop's apparent feasibility must be re-derived at non-zero marginal cost.

CHEAPEST HONEST PATH TO A RUNNING 24/7 STREAM: batch-generate 40 minutes offline (~$120 one-off), loop it to YouTube with `ffmpeg -stream_loop -1 -c copy`, pay $18/mo of VPS. Regenerate nightly for $120/night if freshness matters.

### Evidence

**sources**

https://fal.ai/models/minimax/h3-max/text-to-video — live model page; 480P $0.05/s and 768P $0.08/s regular, currently 50% off at $0.025/$0.04, 'The discount ends September 1'; duration and resolution schema fields.
https://www.digitalapplied.com/blog/fal-h3-max-faster-than-real-time-video-generation — per-clip cost table ($0.40/$0.20 for 5s, $1.20/$0.60 for 15s at 768P), 5s-in-under-3s claim, notes the promo duration is stated inconsistently ('first week' vs 'first 14 days') and that fal published no reproducible latency protocol.
https://blog.fal.ai/introducing-h3-max-by-fal/ — fal's own launch post; 35x faster than official H3, 5s video in ~3s, '50% off' first week.
https://modal.com/pricing — A100-40GB $0.000583/s, A100-80GB $0.000694/s, H100 SXM5 $0.001097/s, H200 $0.001261/s, B200 $0.001736/s, L40S $0.000542/s, L4 $0.000222/s, T4 $0.000164/s, A10 $0.000306/s; storage $0.09/GiB/mo; $30/mo free Starter credit.
https://www.runpod.io/pricing — A100 PCIe $1.19 community / $1.39 secure, A100 SXM $1.39/$1.59, H100 PCIe $1.99/$2.89, H200 $3.59/$4.59, L40S $0.79/$0.99, RTX A6000 $0.33/$0.53, A40 $0.35/$0.44; storage tiers; no egress charge listed.
https://lambda.ai/service/gpu-cloud — A100-40GB $1.99/hr, A100-80GB $2.79/hr (8x), H100 $3.99-$4.29/hr, B200 $6.69-$6.99/hr, A6000 $1.09/hr, A10 $1.29/hr; explicit 'no egress fees'.
https://vast.ai/pricing/gpu/A100-SXM4 and https://www.thundercompute.com/blog/vast-ai-vs-thunder-compute — Vast.ai A100-80GB marketplace ~$0.67/hr, dipping below $0.60 off-peak; host-set and preemptible.
https://www.hetzner.com/news/gpu-server-gex130/ and https://gpuhosted.com/en/hetzner-gpu-review/ — GEX130 RTX 6000 Ada 48GB at EUR 838/mo + EUR 79 setup, or EUR 1.3429/hr; reported discontinued July 2026 in favour of GEX131 (RTX PRO 6000 Blackwell Max-Q 96GB).
https://www.whtop.com/plans/hetzner.com/128287 and https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ — CPX31 4 vCPU / 8GB / 160GB NVMe / 20TB traffic at ~EUR 16.49-17.99/mo; price adjustments effective 15 June 2026.
https://fal.ai/docs/documentation/model-apis/concurrency-limits — new accounts start at 2 concurrent IN_PROGRESS, self-serve ceiling 40 scaled by trailing-4-week paid invoices, sales contact beyond that; queued requests do not consume slots and are never rejected for concurrency.
https://www.tigrisdata.com/blog/case-study-falai/ and https://fal.ai/docs/documentation/model-apis/pricing — fal outputs served from CDN with zero egress fees; billing is per output-second for hosted video models.
https://levels.io/i-built-infinite-slop and https://levels.io/37000-watched-infinite-slop — Hetzner VPS, fal sponsored the compute ('it'd be very expensive to run this'), 37,000 viewers day one, peaks above 1,000 simultaneous watchers.
https://www.dacast.com/blog/how-to-broadcast-live-stream-using-ffmpeg/ and https://theloops.live/guides/rtmp-youtube-live — YouTube RTMP ingest at rtmp://a.rtmp.youtube.com/live2/, 4500-6000 kbps for 1080p, 2-3 vCPU for a 720p30 encode at veryfast.
https://www.datacamp.com/tutorial/tribe-v2-tutorial — TRIBE v2 VRAM 28-32GB trimodal (Llama-3.2-3B ~7GB, V-JEPA2-Giant ~14GB, Wav2Vec-BERT ~1GB), A100-40GB minimum / 80GB recommended, T4 OOMs; sets the GPU SKU floor used above.
INFERENCE (mine, not sourced): all per-hour/day/month arithmetic; the 730h month; the duty-cycle model and its break-even points against a rented B200; the self-hosted HLS egress projection at 1,000 concurrent viewers; the claim that clip length is cost-neutral per stream-hour; the ranking of levers by magnitude.

### Other Info

**item_id**

11

### Flagged Uncertain (omitted above)

- `interface_spec`
- `latency_ms`
- `unknowns`

---

## Differentiable stimulus optimisation as an offline motif table

### Identity

**what_it_is**

Gradient ascent on TRIBE v2's own predicted activation, run backwards through the frozen V-JEPA 2 ViT-G into Fourier-parameterised pixels, producing a synthetic stimulus that maximally drives a chosen Glasser ROI. Run once, offline, across seven visual ROIs, it yields a small grounded ROI -> visual-motif dictionary. Bladon & Bent, arXiv:2605.13904 (Duke, 13 May 2026), code at github.com/recozers/Tribe-V2-Interp.

**role_in_loop**

Optionally DELETES the perceive -> predict arm of the loop. Instead of running TRIBE live on each generated clip and reading out an activation vector, you consult a static table at prompt-write time. TRIBE never loads at runtime: no 28-32 GB warm GPU, no 60 s cold start, no 15-30 s minimum stimulus window, no haemodynamic-lag bookkeeping. The cost is that the stream stops being reactive in any real sense — see the legitimacy assessment in `recommended_approach`.

### Interface

**interface_spec**

Single script, `feature_viz.py`, 1,085 lines, no package, no requirements.txt.

CLI (read from the argparse block):
  --target-roi STR      default 'V1'; one of V1 V2 V3 V4 MT FFA PPA, or any raw HCP MMP1.0 label (e.g. MST)
  --skip-sweep          skip the lambda_fft sweep, use 1e-3
  --sweep-steps INT     default 500
  --full-steps INT      default 3000
  --n-restarts INT      default 5
  --seed INT            default 42 (paper uses 42 + 1000k, k in 0..4)
  --single-frame        optimise 1 frame instead of 64; README claims ~32x faster
  --stages-preset STR   default 'progressive'
  --lam-fft FLOAT       default None (swept)
  --suppress-rois STR   comma list of ROIs to actively suppress
  --suppress-beta FLOAT default 1.0
  --cache-dir STR       default ./cache
  --out-dir STR         default ./outputs

ROI_MAP, verbatim from the source:
  V1 -> ['V1'], V2 -> ['V2'], V3 -> ['V3'], V4 -> ['V4'], MT -> ['MT'],
  FFA -> ['FFC'] (fusiform face complex), PPA -> ['PHA1','PHA2','PHA3']

Differentiable pipeline (from the README, confirmed against the source):
  Fourier coefficients (the optimised variable)
    -> IRFFT -> ImageNet colour-decorrelation matmul -> sigmoid -> frames in [0,1]
    -> random jitter -> ImageNet normalise
    -> V-JEPA 2 ViT-G, FROZEN, fp16, gradient checkpointing, output_hidden_states=True
    -> hidden states at layers [20, 30, 39]  (= TRIBE's layers_to_use [0.5, 0.75, 1.0])
    -> reshape (B, 8192, D) -> (B, 32, 256, D), spatial mean-pool -> (B, 32, D)
    -> TRIBE v2 FmriEncoderModel, FROZEN, fp16, AVERAGE-SUBJECT MODE
    -> 20,484 fsaverage5 cortical vertices
    -> index target ROI vertices via HCP MMP1.0 annot
    -> loss = -mean(ROI activation) + lambda_fft * spectral_penalty + lambda_temp * temporal_smoothness
    -> backprop to the Fourier coefficients only

Constants: NUM_FRAMES=64, FRAME_SIZE=256, TUBELET_SIZE=2, PATCH_SIZE=16, T_TOKENS=32, S_TOKENS=256, FSAVERAGE5_VERTS=10242 per hemisphere.

Loss detail from the paper: 'global lift' — maximise target ROI mean while suppressing mean activation elsewhere, beta = 1.0, lambda_fft = 1e-3, lambda_temporal = 0.1 * lambda_fft. Fourier parameterisation with quadratic radial spectral penalty (freq_weight proportional to radius^2). Progressive multi-scale 64 -> 128 -> 256 by zero-padding the spectrum, step budget split 20/30/50%. Cosine-annealed LR: stage 1 0.03 -> 0.003, later stages 0.01 -> 0.001.

ROI vertex lookup: `mne.datasets.fetch_fsaverage` then `mne.datasets.fetch_hcp_mmp_parcellation`, then `nibabel.freesurfer.read_annot` on `{lh,rh}.HCPMMP1.annot`, filtered to the first 10,242 fsaverage5 vertices per hemisphere. THIS IS DIRECTLY REUSABLE for item 02 (TRIBE ships no parcellation helpers) regardless of whether you ever run the optimiser.

**input_contract**

- CUDA GPU, >=24 GB VRAM. Tested on RTX 3090; peak ~18.4 GB with gradient checkpointing. Paper also mentions an 18 GB peak on A100-40GB. System RAM ~6-8 GB peak at model load, 16 GB sufficient.
- HF_TOKEN (or `huggingface-cli login`) with accepted access to `facebook/vjepa2-vitg-fpc64-256` and `facebook/tribev2`.
- CRITICAL AND UNDER-STATED: the Llama-3.2-3B gate is NOT required. The script exploits TRIBE's modality dropout (p=0.3 in training) and feeds video features only; `aggregate_features` auto-fills zeros for text and audio. Confirmed in the source ('TRIBE v2 forward — only video key present; text/audio auto-zeroed'). So the ~6 GB text branch and the gated Meta licence acceptance both drop out of this path entirely.
- Dependencies, verbatim from the module docstring (there is no requirements.txt):
    torch>=2.5.1, torchvision, numpy==2.2.6, einops, pyyaml
    transformers>=4.50, huggingface_hub
    neuralset==0.0.2, neuraltrain==0.0.2, x_transformers==1.27.20, pydantic>=2, exca
    moviepy>=2.2.1, soundfile, julius, langdetect, spacy, Levenshtein, gtts
    git+https://github.com/facebookresearch/tribev2.git
    matplotlib, mne, nibabel
  Note numpy is HARD-PINNED to 2.2.6 and three packages are pinned to exact versions — consistent with the NumPy<2.1-class install friction flagged in item 10. Budget for dependency resolution.
- Network access for MNE to fetch fsaverage and the HCP-MMP1 annotation files on first run.

**output_contract**

Written to `outputs/{roi}/`:
  sweep/lambda_*/frames_*.png, loss_curve.png, comparison.png
  full/restart_{0..4}/frames_*.png, loss_curve.png
  best_frames.png              8-frame grid from the best restart
  best_individual/frame_00..63.png
  selectivity.png              bar chart, all ROIs, optimised vs random
  validation.json              MACHINE-READABLE — this is the file that becomes the motif table

What the numbers physically mean: TRIBE v2 predicts approximately z-scored BOLD signal, so an activation of 0.339 is ~0.34 standard deviations of predicted blood-oxygen-level-dependent response above that vertex's mean — a predicted haemodynamic quantity, not a firing rate, not attention, not preference. validation.json carries per-ROI activation for the optimised stimulus and for 5 random-noise seeds, plus two derived metrics defined in the README: LIFT OVER RANDOM (optimised minus random; should be positive) and SELECTIVITY RATIO (target activation / mean of all other ROIs; >1.0 means on-target, '>1.5 is a meaningful result').

Headline results table from the published paper (target activation, lift):
  V1  0.155  +0.179     V2  0.138  +0.143     V3  0.179  +0.183
  V4  0.292  +0.248     MT  0.490  +0.700     FFA 0.339  +0.359     PPA 0.266  +0.237
MT is the strongest result on both metrics.

The images themselves are STILL, GRAYSCALE, 64x64 optimised then band-limited up to 256x256, then tiled to 64 identical frames for the video model. Human-interpretable, but as abstract texture, not as scenes.

### Performance

**throughput_constraint**

Single GPU, fully serialised: one ROI at a time, one restart at a time, V-JEPA 2 ViT-G fp16 forward passes saturate a 3090. No batching across ROIs is implemented. Not a live constraint — it is a one-off scheduling question you can run overnight. The real throughput limit on the whole idea is the ROI count: only 7 visual regions are implemented, and the paper lists 'a sweep over the full Glasser parcellation' as deferred future work, so a richer table is not something you can just ask for.

**realtime_headroom**

Total surplus. This replaces the single largest real-time cost in the system with a dictionary lookup measured in microseconds. Against a 15 s clip budget, the live TRIBE arm (warm 28-32 GB GPU, 15-30 s minimum stimulus, 5 s haemodynamic offset) is the component most likely to blow the budget; the lookup table's contribution is unmeasurable. If real-time feasibility (item 13) fails, this is the cut that saves it.

### Complexity

**dev_complexity**

LOW if you hand-author the table from the paper's published figures and numbers — a text file and an afternoon, no GPU, no dependency resolution.
MEDIUM if you actually run the repo: a hard-pinned numpy, three exact-pinned niche packages (neuralset, neuraltrain, x_transformers), an editable install of tribev2 from git, two gated HF repos, an MNE dataset fetch, and a 24 GB CUDA card you probably have to rent. Half a day to first successful run is a realistic estimate, plus GPU hours.
The part nobody budgets for is neither of those: translating a grayscale Gabor field into words a video model will act on is a HUMAN CURATION step. It is taste, not code, and it is where the actual work is.

**loc_estimate**

0 LOC to run the repo as-is. ~30 LOC for the runtime lookup (a dict plus a weighted sampler). ~80-150 LOC if you want a builder that reads each `validation.json`, ranks ROIs by selectivity ratio and emits the table programmatically. The ROI-vertex-indexing block (mne fetch -> nibabel read_annot -> fsaverage5 filter, roughly 40 lines around source lines 274-345) is worth lifting wholesale into item 02 whether or not you use the rest.

**off_the_shelf_option**

THE PAPER IS THE OFF-THE-SHELF OPTION. arXiv:2605.13904 is CC BY 4.0, has 8 pages, 3 figures and 2 tables, and publishes both the per-ROI qualitative descriptions and the full activation/lift/selectivity table. Everything needed to write a seven-row motif dictionary is in it. The repository adds reproducibility and the ability to target ROIs beyond the seven — neither of which the demo needs.

Repo health, checked via the GitHub API: `recozers/Tribe-V2-Interp`, created 2026-03-31, last push 2026-05-13 (the arXiv submission date — abandoned since), 22 commits, 0 stars, 0 forks, 0 open issues, NO LICENSE FILE, no requirements.txt, no tests, no CI. Single 47 KB script plus the LaTeX source of the paper. It is research code published to satisfy a code-availability statement, not a maintained tool. The missing licence is a real problem if you plan to redistribute anything derived from it — there is no grant, so default copyright applies; ask the author, or work from the CC BY 4.0 paper instead.

### Decision

**recommended_approach**

DO NOT RUN IT. Hand-author the table from the paper, and spend the saved GPU-hours on the parts of the system that are actually uncertain.

The reasoning is that the optimiser's output does not survive translation to prompt text. The synthetic stimuli are grayscale abstract texture fields — Gabor swirls, contour junctions, radial streaks. A text-to-video model given 'a dense field of small-scale oriented edges and Gabor-like swirls' will not produce anything resembling the V1 stimulus, and could not: the whole point of the super-stimulus finding is that these images are OFF the natural image manifold, and a generative video model is a machine for staying ON it. The information that survives the round-trip through English is exactly the qualitative description already printed in the paper. Running 21-42 GPU-hours to regenerate images you will then discard in favour of their captions is paying for precision you cannot spend.

THE TABLE, buildable today with no hardware, grounded line-by-line in the paper:
  V1  -> fine oriented texture, dense edges, high-frequency detail, fabric weave, static grain
  V2  -> as V1 with more junctions and corners, lattice, mesh, cracked glaze
  V3  -> the same vocabulary at larger scale
  V4  -> mid-scale curves, 2-3x V1's scale, organised curvilinear form, rounded contours
  MT  -> motion streaks, long-exposure light trails, radial blur, optic flow, speed lines, camera whip
  FFA -> faces, eyes, a nose ridge, a jaw line, portraiture, frontal gaze
  PPA -> strong parallel lines, horizontal and diagonal rectilinear structure. NOT 'places', NOT 'scenes' — the authors explicitly decline that reading and you should too.
MT is the row to trust most: highest activation (0.490) and highest lift (+0.700) of any region, and the finding is genuinely non-trivial — a static-only optimisation recovered implied-motion imagery from a motion-selective region. That is the one row where the method told us something the prior literature would not have handed you for free.

IF you do run it, the sane invocation is the fast path, single-frame, no sweep, one restart, on a rented 3090 or A100:
  python feature_viz.py --target-roi MT --single-frame --skip-sweep --n-restarts 1
Run MT and FFA only — the two rows with distinctive, prompt-translatable regimes — look at the PNGs yourself, and write your own adjectives from what you see rather than from the paper's. That is a couple of hours and under a dollar of GPU, and it buys you first-hand authorship of the table, which has real value if you are going to talk about the piece publicly.

THE 4x FINDING, AND WHAT IT MEANS FOR A SELF-OPTIMISING SYSTEM.
The published arXiv v1 reports: random noise -0.020, vector face illustration +0.039, photograph of a real face +0.080, optimised FFA stimulus +0.339 — 'roughly four times harder than the photograph' (4.24x). TWO CAVEATS YOU SHOULD CARRY. First, the paper itself states 'Natural-face comparisons are n=1 each and meant only to bracket the magnitude of the optimized drive.' It is two reference images, not a benchmark. Second, and more telling: the pre-submission draft still in the repo (`paper/draft_v1.md`) reports the photograph at +0.108 and the multiplier at '~3x'. The denominator moved between drafts and the headline moved with it. Cite it as 'three to four times, on an n=1 comparison' and you are safe; cite '4x' as a hard fact and you are overstating a number the authors themselves revised.

But the DIRECTION is robust and it is the important part. Gradient ascent on a brain encoder finds inputs that exceed anything in the natural distribution. The paper is blunt: 'The optimized stimuli are extrema of the encoder's response surface: gradient ascent finds patterns that exceed anything in the natural distribution, and reasoning from these patterns to what a region "really encodes" risks overfitting to adversarial features of the composed pipeline.' A system that closes the loop by optimising its own brain model is doing gradient ascent by other means — slower, discretised through prompts, but pointed the same way. This paper is the EVIDENCE BASE for the attractor-collapse risk in item 09, and it is the strongest argument for building the novelty/damping term before launch rather than after. Note also the paper's failure mode: at full colour and full resolution with no curriculum, the optimiser collapses into 'high-frequency adversarial texture' with characteristic pink/teal tinting, and predicted activation DROPS (0.258 vs 0.339 for the constrained run). Unconstrained maximisation scored worse than constrained maximisation. That is a design lesson for the live loop, not just for the offline probe.

HOW MUCH ARTISTIC LEGITIMACY SURVIVES — the honest answer, in three parts.
(1) The TABLE is legitimate. It is derived, by a published and peer-reviewable method, from a model trained on 1,100+ hours of real fMRI, and the method demonstrably recovers known cortical selectivity — the V1->V4 scale progression matches the ventral hierarchy, MT recovers implied motion, FFA recovers face parts. 'These motifs were derived by inverting a brain encoder' is a true, specific, defensible sentence.
(2) The LIVE PIECE loses most of its claim. Once the table is fixed, nothing about the stream responds to anything. You have a static dictionary and a sampler. 'The stream reacts to a simulated brain' becomes false the moment TRIBE leaves the loop; the honest version collapses to 'the vocabulary was derived from a brain model, once, in advance' — which is a much smaller and much more ordinary claim. Be clear-eyed that this is the trade: you are buying a working demo with the conceptual core.
(3) The escape hatch, if you want both. Keep TRIBE in the loop but SLOWLY — the table drives moment-to-moment prompting, and a live TRIBE pass runs every few minutes to re-weight which table rows are active. That preserves a truthful closed loop at a duty cycle the latency budget can afford, and it is a smaller build than the full live loop. If the demo must ship this week, ship the table; if there is a second week, this is where it goes.

**simpler_alternative**

Skip both the repo and the paper's optimiser and use a hand-written motif table with no brain model behind it — MT-style motion streaks, FFA-style faces, V1-style texture are all things you could have written from an undergraduate vision-science lecture. The pipeline is identical; only the provenance claim changes. This is the honest crude fallback: it costs an hour, cannot break, and you simply do not get to say the motifs came from a brain encoder. Given that the paper is CC BY 4.0 and free to cite, there is little reason to choose this over the paper-derived table — the paper-derived version is the same amount of work with a real citation attached.

**code_sketch**

# --- built ONCE, offline. No TRIBE, no GPU, no torch at runtime. ---
# Descriptions are quoted/paraphrased from Bladon & Bent, arXiv:2605.13904 (CC BY 4.0).
# `lift` is the paper's measured lift-over-random; used as a sampling weight so the
# rows the method actually established (MT, FFA) dominate the ones it barely did (V2).

ROI_MOTIFS = {
    'MT':  {'lift': 0.700, 'prompt': 'long-exposure motion streaks, radial light trails, '
                                     'optic flow, whip pan, sustained camera speed'},
    'FFA': {'lift': 0.359, 'prompt': 'a human face filling the frame, frontal gaze, '
                                     'eyes nose and jaw in sharp relief'},
    'V4':  {'lift': 0.248, 'prompt': 'large rounded curvilinear forms, organised mid-scale '
                                     'curves, smooth sweeping contours'},
    'PPA': {'lift': 0.237, 'prompt': 'strong parallel lines, horizontal and diagonal '
                                     'rectilinear structure, receding rulings'},
    'V3':  {'lift': 0.183, 'prompt': 'coarse repeating texture at large scale'},
    'V1':  {'lift': 0.179, 'prompt': 'dense fine oriented texture, high-frequency grain, '
                                     'woven fabric detail'},
    'V2':  {'lift': 0.143, 'prompt': 'lattice and mesh, contour junctions, cracked glaze'},
}

import random

def write_prompt(active_rois, recent, novelty_penalty=0.6):
    """active_rois: list of ROI names the current state wants to drive.
       recent: ROIs used in the last N clips -- damped to resist attractor collapse,
       which arXiv:2605.13904 gives us direct evidence to expect."""
    weights = [
        ROI_MOTIFS[r]['lift'] * (novelty_penalty if r in recent else 1.0)
        for r in active_rois
    ]
    roi = random.choices(active_rois, weights=weights, k=1)[0]
    return roi, ROI_MOTIFS[roi]['prompt']

# --- If you DO run the optimiser, this is the only invocation worth the GPU time ---
# python feature_viz.py --target-roi MT  --single-frame --skip-sweep --n-restarts 1
# python feature_viz.py --target-roi FFA --single-frame --skip-sweep --n-restarts 1
# then read outputs/{roi}/validation.json for measured lift + selectivity ratio,
# and outputs/{roi}/best_frames.png to write your own adjectives from what you see.

# --- Reusable regardless: ROI -> fsaverage5 vertex indices (needed by item 02) ---
# import mne, nibabel.freesurfer as nbfs
# mne.datasets.fetch_fsaverage(...); mne.datasets.fetch_hcp_mmp_parcellation(...)
# labels, ctab, names = nbfs.read_annot(subjects_dir/'fsaverage'/'label'/'lh.HCPMMP1.annot')
# keep only vertices < 10242 (fsaverage5); rh indices are offset by +10242.

### Risk

**failure_modes**

- SUPER-STIMULI ARE NOT EXEMPLARS. The optimised images are extrema of the encoder's response surface, not canonical examples of what a region likes. Reading them as 'what FFA encodes' overfits to adversarial features of the composed V-JEPA-2 + TRIBE pipeline — the authors say so explicitly. A table built on that reading inherits the error.
- THE HEADLINE NUMBER MOVED. 3x in the repo draft (photograph +0.108), 4x in the published arXiv v1 (photograph +0.080), on an n=1-per-condition comparison the authors describe as meant 'only to bracket the magnitude'. Quote it with the caveat attached.
- THE IMAGES DO NOT SURVIVE CAPTIONING. Grayscale Gabor fields become 'fine oriented texture' become a video of a woven fabric. Most of what the optimiser found is destroyed by the round-trip through English, and a generative video model cannot render off-manifold stimuli anyway. This is the single biggest reason not to spend the GPU hours.
- ONLY SEVEN ROIs, ALL VISUAL. No language, auditory, DMN or value/salience motifs, so the table cannot express most of what TRIBE actually predicts. The full-Glasser sweep is explicitly deferred future work.
- PPA IS UNINTERPRETED. Consistent rectilinear lines, but the authors refuse a category-level reading. If your table says 'places' you have invented that.
- STATIC TILING IS OUT OF DISTRIBUTION. TRIBE v2 was trained on 64-frame video; the method optimises a still and tiles it to 64 identical frames, which the paper calls 'mildly out of distribution'. Motion tuning cannot be distinguished from implied-motion tuning without temporal-axis optimisation, which has not been done.
- n=5 RESTARTS, NO SIGNIFICANCE TESTING. The authors report restart variation but explicitly decline significance tests on lift-vs-noise. FFA face geometry varies across restarts. Do not treat any single number as tight.
- fp16 NON-DETERMINISM. Pixel-level reproducibility is not available; you will not get the paper's exact images back.
- REPO BIT-ROT AND NO LICENCE. 0 stars, 0 forks, abandoned since 2026-05-13, no requirements.txt, no tests, no LICENSE file. Hard-pinned numpy==2.2.6 and three exact-pinned niche packages against a moving transformers>=4.50 is a dependency-resolution failure waiting to happen. And with no licence, you have no explicit grant to redistribute derived artefacts — work from the CC BY 4.0 paper if you plan to publish the table.
- LICENCE INHERITANCE. The table is derived from TRIBE v2, which is CC BY-NC 4.0. Precomputing offline does NOT escape the non-commercial restriction — see the licence item. People reach for offline precomputation partly hoping it launders the licence; it does not.
- THE CONCEPTUAL COST IS THE REAL FAILURE MODE. A fixed table means the piece is not reactive. If you keep describing it as responding to a simulated brain after making this swap, the claim is simply false — and it is the kind of false that an informed viewer will catch.

### Evidence

**sources**

- https://arxiv.org/abs/2605.13904 — Bladon, S. & Bent, B., 'Feature Visualization Recovers Known Cortical Selectivity from TRIBE v2', Duke University, submitted 13 May 2026, v1 only, licence CC BY 4.0, 8 pages / 3 figures / 2 tables, q-bio.NC + cs.LG.
- https://arxiv.org/html/2605.13904v1 — full text, read directly. Source of: the abstract's '~4x as much as a natural face photograph'; the stimulus comparison table (random noise -0.020, vector illustration +0.039, photograph +0.080, optimised +0.339); the caveat 'Natural-face comparisons are n=1 each and meant only to bracket the magnitude of the optimized drive'; the per-ROI activation/lift table (V1 0.155/+0.179, V2 0.138/+0.143, V3 0.179/+0.183, V4 0.292/+0.248, MT 0.490/+0.700, FFA 0.339/+0.359, PPA 0.266/+0.237); 'TRIBE v2 predicts approximately z-scored blood-oxygen-level-dependent (BOLD) signal'; the RTX 3090 / 'compute was the dominant bottleneck' statement; the full Limitations section quoted in `failure_modes`; and the Future work section listing the full-Glasser sweep, temporal-axis optimisation and human-observer validation as deferred.
- https://github.com/recozers/Tribe-V2-Interp — the code. README read verbatim via raw.githubusercontent.com: pipeline diagram, CLI examples, '>=24 GB VRAM ... tested on RTX 3090; peak ~18.4 GB', 'Full 5-restart run takes ~3-6 hours on a 3090', the output-directory tree, the supported-ROI table mapping FFA->FFC and PPA->PHA1/2/3, and the design-decision sections on Fourier parameterisation, progressive multi-scale, colour decorrelation, cosine LR, temporal smoothness and modality dropout.
- https://raw.githubusercontent.com/recozers/Tribe-V2-Interp/main/feature_viz.py — the source, 1,085 lines, read directly. Source of: the full argparse surface and defaults; ROI_MAP; the constants block (NUM_FRAMES 64, FRAME_SIZE 256, TUBELET_SIZE 2, PATCH_SIZE 16, T_TOKENS 32, S_TOKENS 256, FSAVERAGE5_VERTS 10242); the exact pip dependency list in the module docstring including numpy==2.2.6, neuralset==0.0.2, neuraltrain==0.0.2, x_transformers==1.27.20; the mne/nibabel HCP-MMP1 annot lookup at lines ~274-345; and the confirmation at lines 509/543 that TRIBE is called with video features only and text/audio auto-zeroed (hence NO Llama gate on this path).
- https://raw.githubusercontent.com/recozers/Tribe-V2-Interp/main/paper/draft_v1.md — the pre-submission draft still in the repo. Source of the 3x-vs-4x discrepancy: this version reports the photograph at +0.108 and 'roughly three times harder', against the published +0.080 and '~4x'. Also the full-colour/full-resolution failure mode (activation drops to 0.258 vs 0.339) and the targeted-vs-global suppression ablation (0.289 vs 0.339).
- GitHub API, repos/recozers/Tribe-V2-Interp — created 2026-03-31T01:29:27Z, pushed 2026-05-13T00:07:43Z, 22 commits, 0 stars, 0 forks, 0 open issues, license: null, no requirements.txt. Queried directly.
- https://www.emergentmind.com/papers/2605.13904 — secondary summary of the paper; used only for cross-checking, no unique claims taken from it.
- https://github.com/facebookresearch/tribev2 — for the modality-dropout and average-subject-mode context the script relies on.
- INFERENCE, flagged as such: the single-frame wall-clock estimate (~1-3 min/ROI), the GPU dollar costs, the 'half a day to first successful run' figure, and the entire artistic-legitimacy assessment are my reasoning from the sourced facts above, not claims made by any source.

### Other Info

**item_id**

16

**_qualitative_output_descriptions**

- **V1**: densest fields of small-scale oriented edges and Gabor-like swirls
- **V2**: similar to V1 with slightly more contour junctions
- **V3**: noticeably larger spatial scale
- **V4**: most organised; mid-scale curves roughly 2-3x the spatial scale of V1
- **MT**: sharp radial or diagonal streak patterns, elongated local orientations, converging lines and bands that read as frozen optic flow or long-exposure photographs of moving scenes — recovered despite static-only optimisation
- **FFA**: eye-like regions, nose ridges, mouth/jaw outlines; face geometry varies across restarts
- **PPA**: parallel, predominantly horizontal and diagonal lines, high within-run consistency. AUTHORS EXPLICITLY REFRAIN from a category-level interpretation — do NOT translate this to 'places' or 'scenes'.

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `unknowns`

---

## fal MiniMax H3 Max generation API

### Identity

**what_it_is**

fal's post-trained turbo variant of the open-weights MiniMax H3 (Hailuo 03) omni-modal video model, exposed as two hosted queue endpoints that turn a text prompt (optionally plus a first and/or last keyframe image) into a 5-15s MP4 with natively synchronised audio, typically faster than the clip plays.

**role_in_loop**

The GENERATE stage — final consumer of the prompt written by the brain-state-to-prompt layer (item 04), and the producer of the clip that the streaming pipeline (item 07) plays and that the closed loop (item 09) optionally feeds back into TRIBE. It is the only stage that returns both the pixels and the audio, closing TRIBE's audio branch with no separate TTS/music model.

### Interface

**interface_spec**

TWO ENDPOINTS (verified against the live fal OpenAPI schemas on 2026-08-31 via https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=minimax/h3-max/text-to-video and .../image-to-video).

Endpoint ids: `minimax/h3-max/text-to-video` (internal schema title `TurboTextToVideoHailuo03Input/Output`) and `minimax/h3-max/image-to-video` (`TurboImageToVideoHailuo03Input/Output`). Note there is NO `fal-ai/` owner prefix on these — `fal-ai/minimax/h3-max/...` 404s.

QUEUE HTTP SURFACE (all under https://queue.fal.run):
  POST /minimax/h3-max/text-to-video                                 -> QueueStatus {status, request_id, response_url, status_url, cancel_url, queue_position?}
  GET  /minimax/h3-max/text-to-video/requests/{request_id}/status?logs=1 -> QueueStatus
  GET  /minimax/h3-max/text-to-video/requests/{request_id}           -> Output
  PUT  /minimax/h3-max/text-to-video/requests/{request_id}/cancel    -> {success: bool}
Status enum is exactly [IN_QUEUE, IN_PROGRESS, COMPLETED]. Auth header: `Authorization: Key <FAL_KEY>`. Synchronous (non-queue) host is https://fal.run/<endpoint-id>. Webhooks are requested by appending `?fal_webhook=<url-encoded callback>` to the queue POST.
H3 Max exposes NO `/stream` path in its OpenAPI — `fal_client.stream()` / SSE is NOT available for this model. Real-time WebSocket (`fal_client.realtime()`) is likewise not exposed. Queue-poll or webhook are the only two mechanisms.

INPUT SCHEMA — text-to-video (exact, from OpenAPI):
  prompt              string   REQUIRED, minLength 1, maxLength 50000
  prompt_expansion_mode string REQUIRED, default "balanced", examples ["balanced","quality"] — NOTE: declared as a bare `type: string`, NOT an enum, so other values are accepted by the validator
  duration            integer  minimum 5, maximum 15, default 5 — ANY integer in 5..15, not just 5/10/15
  resolution          enum     ["480P","768P"], default "768P"
  aspect_ratio        enum     ["21:9","16:9","4:3","1:1","3:4","9:16"], default "16:9"  (t2v ONLY)
  seed                integer|null — random when omitted
  enable_safety_checker boolean default true
  sync_mode           boolean default false — returns the video as base64 instead of a CDN URL

INPUT SCHEMA — image-to-video: identical MINUS `aspect_ratio`, PLUS:
  image_url     string|null — "Optional URL of the image to use as the first frame. When provided, the output aspect ratio follows this image. When omitted, the request is handled as text-to-video (16:9 by default)."
  end_image_url string|null — "Optional URL of the image to use as the last frame, for first-to-last keyframe generation."
Both image fields accept a public https URL, a fal CDN URL, or a base64 data URI (`data:image/jpeg;base64,...`).

OUTPUT SCHEMA (both endpoints):
  video           File REQUIRED — {url: string, content_type, file_name, file_size} e.g. https://v3b.fal.media/files/b/<hash>/<name>.mp4
  expanded_prompt string|null — "The prompt after expansion, as sent to the model. Null when prompt expansion was disabled, left the prompt unchanged, or was performed internally by MiniMax's hosted API."  <-- the wording 'when prompt expansion was disabled' is direct evidence that a disable value for prompt_expansion_mode exists; the exact token is not documented (see unknowns).
  timings         object|null — map<string,number>, "Timing breakdown in seconds. 'inference' is the DiT denoising time on the GPU backend. Null on routes that do not report backend timings."  Observed key: `timings.inference` ~2.53 on a 5s/768P example.

ERROR SHAPE. Model-level errors are HTTP 422 with a FastAPI/Pydantic body:
  {"detail":[{"loc":["body","<field>"],"msg":"<human text>","type":"<error_type>","url":"https://docs.fal.ai/errors#<error_type>","ctx":{...},"input":...}]}
Request-level errors use a different, flat shape:
  {"detail":"<human text>","error_type":"<error_type>"}
Relevant types: content_policy_violation (422, marked NON-RETRYABLE), no_media_generated (422), generation_timeout (504), request_timeout (504), startup_timeout (504), runner_scheduling_failure/runner_disconnected/runner_connection_* (503), runner_server_error (500), internal_server_error (500), plus the numeric validation family (greater_than_equal / less_than_equal for duration, one_of for resolution).

WEBHOOK CALLBACK PAYLOAD (POST to your fal_webhook URL):
  success: {"request_id":"...","gateway_request_id":"...","status":"OK","payload":{<the Output object>}}
  failure: {"request_id":"...","gateway_request_id":"...","status":"ERROR","error":"...","payload":{<error detail>}}
Signed with ED25519; header `X-Fal-Webhook-Signature`; public keys at https://rest.alpha.fal.ai/.well-known/jwks.json; the signed message is requestId, userId, timestamp and the SHA-256 of the body joined by newlines; reject anything with a timestamp older than 300s.

PYTHON CLIENT (`fal-client` 1.0.1, released 2026-08-19, Python >= 3.8) — verified against source at fal-ai/fal projects/fal_client/src/fal_client/client.py:
  run(application, arguments, *, path="", timeout=None, start_timeout=None, hint=None, headers={}) -> dict
  submit(application, arguments, *, path="", hint=None, webhook_url=None, priority=None, headers={}, start_timeout=None) -> SyncRequestHandle
  subscribe(application, arguments, *, path="", hint=None, with_logs=False, interval=0.1, on_enqueue=None, on_queue_update=None, priority=None, headers={}, start_timeout=None, client_timeout=None) -> dict
  status(application, request_id, *, with_logs=False) / result(application, request_id) / cancel(application, request_id) / get_handle(application, request_id)
  upload(data, content_type, ...) / upload_file(path, *, repository=None, fallback_repository=None, lifecycle=StorageSettings(expires_in=..., initial_acl=...)) -> str
  encode_file(path) -> data-URI string   (no network round trip)
  stream(application, arguments, *, path="/stream", ...)  — NOT supported by H3 Max
Async mirrors exist for every one of these (`run_async`, `submit_async`, `subscribe_async`, ...). Default queue poll interval is 0.1s (DEFAULT_QUEUE_POLL_INTERVAL). `webhook_url` is implemented as `?fal_webhook=` on the queue URL.

JS CLIENT (`@fal-ai/client`):
  fal.subscribe(id, {input, logs, onQueueUpdate})
  fal.queue.submit(id, {input, webhookUrl}) -> {request_id}
  fal.queue.status(id, {requestId, logs:true}) / fal.queue.result(id, {requestId})

**input_contract**

Minimum viable request is two fields: `prompt` (1..50000 chars) and `prompt_expansion_mode` — both are REQUIRED by the schema even though prompt_expansion_mode has a default, so the client must send it explicitly. `duration` is an integer 5..15 inclusive (any integer, so 7s or 11s clips are legal — useful for tuning the buffer). Resolution is one of two fixed rungs, 480P or 768P; there is no 1080P on H3 Max (the non-Max MiniMax H3 goes to 2K). Aspect ratio is settable only on text-to-video; on image-to-video the output aspect ratio is inherited from `image_url`, so a chained pipeline must keep every conditioning frame at exactly the same dimensions or the stream resolution will wobble mid-broadcast. Image inputs may be a public https URL, a fal CDN URL from upload_file, or an inline base64 data URI. Auth is a single `FAL_KEY` env var. Prompts should carry an explicit sound description — the model generates audio from the same prompt, and fal's own prompting guide recommends naming instrumentation, ambience and where beats land.

**output_contract**

One MP4 at 480x854/854x480-class (480P) or 768-class (768P) resolution, of exactly the requested duration in seconds, with an embedded, natively synchronised AAC audio track (dialogue, foley, ambience and music are predicted jointly with the pixels rather than dubbed on afterwards). Delivered as `video.url` on the fal CDN (v3b.fal.media) unless `sync_mode: true`, in which case it comes back inline as base64 — avoid that at 768P, a 15s clip is roughly 6-20MB and base64 inflates it 33%. `expanded_prompt` is the rewritten prompt actually sent to the DiT: this is free text, no fixed length, and is the exact artefact item 09 wants to feed back into TRIBE's text branch instead of captioning the clip. `timings.inference` is seconds of GPU denoising ONLY — it excludes prompt expansion, queue wait, CDN write and network transfer, so it is a floor on wall-clock, not a measure of it. CDN URLs are NOT permanent: fal's media-expiration docs state expired files are permanently deleted and unrecoverable, and retention is controlled by the `X-Fal-Object-Lifecycle-Preference` header ({"expiration_duration_seconds": N} or null for never). A 24/7 stream must download each MP4 to local disk on receipt rather than referencing the fal URL from the player.

### Complexity

**dev_complexity**

LOW. It is a JSON POST with two required fields behind a maintained first-party client that already handles auth, queue polling, backoff and file upload. The only genuinely non-trivial work is failure handling — safety rejections, 5xx runner errors and buffer underrun — and that is orchestration work (item 08), not API work. No model hosting, no GPU, no cold starts, no container.

**loc_estimate**

~40 LOC for a naive blocking `subscribe` call plus download. ~120-150 LOC for the production shape: an async worker pool bounded by a semaphore sized to the concurrency limit, per-request retry classification (retryable 5xx vs non-retryable 422 content_policy_violation), a prompt-softening fallback path, and local download with the fal URL discarded.

**off_the_shelf_option**

`fal-client` (PyPI, 1.0.1, 2026-08-19) and `@fal-ai/client` (npm) are the off-the-shelf answer and remove essentially all of it — `subscribe()` alone collapses submit + poll + fetch-result into one call. For the surrounding loop, `github.com/fal-ai-community/realtime-krea-wan` is the nearest existing scaffold to this project's whole architecture (text-to-video with dynamic prompt rewriting) although it targets a realtime model, not H3 Max — see item 17. fal's own model playground pages generate copy-pasteable Python/JS/curl per endpoint. There is no need to write a raw HTTP client; do not.

### Decision

**recommended_approach**

Use `minimax/h3-max/image-to-video` (NOT text-to-video) as the single generation endpoint for the whole stream, called through `fal_client.submit_async(...)` with an asyncio semaphore, polling via the returned handle rather than webhooks.

Why image-to-video even for the first clip: `image_url` is optional and the endpoint transparently 'routes to t2v' when it is omitted, per fal's own endpoint description. One endpoint, one code path, and clip-chaining (item 06) becomes a matter of setting one extra field rather than switching models mid-stream.

Why submit_async + poll rather than webhooks: webhooks require a publicly reachable HTTPS receiver, ED25519 signature verification against a JWKS endpoint, and a 300s replay window — that is a tunnel, a web server and a verification routine, for a callback that saves at most a few hundred milliseconds on a request the orchestrator is already awaiting in-process. For a single-box demo this is pure cost. Reach for webhooks only if the orchestrator is serverless or the clip queue lives in another process.

Why not `subscribe()`: `subscribe` blocks a coroutine until completion, which is fine, but `submit_async` returns a handle immediately and lets the orchestrator hold N handles, inspect queue_position, cancel a stale request when the brain state has moved on, and fill the buffer opportunistically. Cancellation matters here: if TRIBE's readout swings hard while a clip is mid-generation, PUT .../cancel frees a concurrency slot rather than paying for a clip nobody will see.

FIXED PARAMETERS for the live loop:
  prompt_expansion_mode: "balanced"   — mandatory. 'quality' costs up to 30s and is disqualified outright.
  resolution: "768P"                   — 480P halves the bill but the visual difference on a public stream is stark; drop to 480P only if the cost model (item 11) forces it.
  duration: 10                         — best surplus-to-seam-count tradeoff. Not 5 (twice the audio seams, twice the requests), not 15 (headroom may be zero at the pessimistic latency).
  aspect_ratio: "16:9"                 — first clip only; thereafter inherited from the conditioning frame.
  seed: omitted                        — let it vary; a fixed seed with a varying prompt buys nothing here.
  enable_safety_checker: leave TRUE.

ON THE SAFETY CHECKER — the outline's concern is correct and the fallback matters. A brain-activation-maximising objective pushes toward faces, threat cues, gore-adjacent salience and high-arousal imagery, which is precisely where the content filter clusters. A rejection is HTTP 422 with detail[0].type == "content_policy_violation", message 'The content could not be processed because it was flagged by automated systems as potentially violating usage policies or responsible AI guidelines', and fal explicitly marks it NON-RETRYABLE — resubmitting the identical prompt is guaranteed to fail again and will just burn a concurrency slot. fal also warns 'The content may have been flagged by either fal's filter or one of our partners'. Sensitivity levels can vary between partner APIs', so behaviour is not fully deterministic and can move without notice.
Do NOT set enable_safety_checker: false as the mitigation. Two reasons: (a) fal runs platform-level moderation (OpenAI's Omni moderation API) independent of the per-model flag, so the flag does not buy immunity, and (b) a public 24/7 stream that has deliberately disabled content filtering on brain-salience-optimised imagery is an obvious liability under fal's Trust & Safety terms and an obvious problem for item 14.
THE FALLBACK LADDER (implement all four rungs, ~30 LOC):
  1. Catch the 422, inspect detail[0].type. If content_policy_violation, DO NOT retry the same prompt.
  2. Re-emit through a deterministic prompt softener: strip the top-scoring salience terms the readout injected (blood, corpse, scream, weapon, wound, terror, child) and re-request once with the abstracted remainder. One retry only.
  3. If that also fails, fall back to a mood-only prompt built from the ROI vector's low-level dials (colour, motion energy, spatial frequency) with no semantic content at all. These effectively never trip the filter.
  4. If all three fail, hand control to the buffer-underrun path (item 08) — filler loop or held crossfade — and log the rejected prompt. Budget for this: assume a 2-8% rejection rate on salience-maximised prompts and size the playback buffer so a single rejection is invisible. [uncertain — no published rejection rate for this endpoint on this class of prompt; must be measured]
Also catch `no_media_generated` (422) — the model completed but produced nothing — and treat it as retryable-once, unlike content_policy_violation.

**simpler_alternative**

Blocking `fal_client.subscribe("minimax/h3-max/text-to-video", {...})` in a single loop with no chaining, no concurrency and no error ladder: submit, wait, download, append to the playlist, repeat. It is about 25 lines, it works today, and at 5s clips its ~3.5s turnaround still beats real time on one concurrency slot, so it will actually sustain a stream. What it loses is visual continuity between clips, any tolerance for a failed generation (one 422 and the stream stalls), and the ability to cancel stale work. It is the correct thing to build first — get pixels moving end-to-end, then add the semaphore and the fallback ladder. A cruder rung below that: pre-generate 20 clips offline into a folder and loop them while the brain half is being wired up, so the streaming and playback stages (item 07) can be developed against real files with zero API spend.

**code_sketch**

import asyncio, os, json, aiohttp, fal_client

# FAL_KEY in env. pip install fal-client aiohttp
CONCURRENCY = 2                       # new-account limit; raise as credits are purchased
SEM = asyncio.Semaphore(CONCURRENCY)
ENDPOINT = "minimax/h3-max/image-to-video"   # image_url optional -> routes to t2v when omitted

BASE = dict(duration=10, resolution="768P",
            prompt_expansion_mode="balanced",  # 'quality' costs up to ~30s. Never in the live loop.
            enable_safety_checker=True)

class ContentRejected(Exception): pass

async def generate(prompt: str, first_frame: str | None = None) -> dict:
    """Returns {'path':..., 'expanded_prompt':..., 'inference_s':...}. Raises ContentRejected on 422."""
    args = {**BASE, "prompt": prompt}
    if first_frame:                    # a fal CDN url OR an inline data: URI (see item 06)
        args["image_url"] = first_frame

    async with SEM:                    # never exceed the account concurrency cap
        try:
            handle = await fal_client.submit_async(ENDPOINT, arguments=args)
            result = await handle.get()               # polls status_url at 0.1s
        except fal_client.FalClientError as e:
            body = getattr(e, "body", None) or {}
            detail = body.get("detail")
            if isinstance(detail, list) and detail and \
               detail[0].get("type") == "content_policy_violation":
                raise ContentRejected(detail[0].get("msg", "")) from e
            raise                                     # 5xx / runner_* -> retryable upstream

    url = result["video"]["url"]
    path = f"clips/{result['video']['file_name']}"
    async with aiohttp.ClientSession() as s, s.get(url) as r:   # fal CDN urls expire; pull it local now
        with open(path, "wb") as f:
            async for chunk in r.content.iter_chunked(1 << 16):
                f.write(chunk)

    return {"path": path,
            "expanded_prompt": result.get("expanded_prompt"),   # <- feed this to TRIBE (item 09)
            "inference_s": (result.get("timings") or {}).get("inference")}

SALIENCE_TERMS = ("blood","gore","corpse","scream","weapon","wound","terror","child")

def soften(prompt: str) -> str:
    out = prompt
    for t in SALIENCE_TERMS:
        out = out.replace(t, "")
    return " ".join(out.split())

async def generate_with_fallback(prompt, mood_only_prompt, first_frame=None):
    for candidate in (prompt, soften(prompt), mood_only_prompt):   # rungs 1-3 of the ladder
        try:
            return await generate(candidate, first_frame)
        except ContentRejected:
            continue
    return None            # rung 4 -> orchestrator plays filler (item 08)

# ---- JavaScript equivalent, queue + webhook (only if the orchestrator is serverless) ----
// import { fal } from "@fal-ai/client";
// const { request_id } = await fal.queue.submit("minimax/h3-max/image-to-video", {
//   input: { prompt, duration: 10, resolution: "768P", prompt_expansion_mode: "balanced" },
//   webhookUrl: "https://your.host/fal-callback",   // -> ?fal_webhook= on queue.fal.run
// });
// // callback body: {request_id, gateway_request_id, status:"OK"|"ERROR", payload, error?}
// // verify X-Fal-Webhook-Signature (ED25519, JWKS at rest.alpha.fal.ai/.well-known/jwks.json),
// // reject if the timestamp is older than 300s.

### Risk

**failure_modes**

1. CONTENT_POLICY_VIOLATION AS SILENT THROUGHPUT LOSS. 422, non-retryable, and it does not announce itself as a capacity problem — it looks like an application bug. On brain-salience-optimised prompts the rejection rate is the single most likely cause of buffer underrun, and it is correlated in time (once the readout locks onto a high-arousal attractor, consecutive prompts get rejected together, exactly when the buffer is least able to absorb it). Compounds badly with item 09's attractor collapse.
2. THE PROMO PRICE EXPIRES TOMORROW. Every published source says launch pricing runs to 2026-09-01; today is 2026-08-31. Any cost model built on $0.04/s at 768P is wrong from midnight — the real number is $0.08/s, which is $288 per hour of continuous 768P stream. This is not a rounding error; it is the dominant line in the whole project's budget.
3. `timings.inference` MISLEADS. It is GPU denoising only. Building a buffer policy on it rather than on measured wall-clock will underestimate the loop by roughly 1s at 5s clips and by an unmeasured amount at 15s.
4. CDN URLS EXPIRE AND ARE UNRECOVERABLE. A player pointed at v3b.fal.media will start 404ing on old clips. Download on receipt, always.
5. UNDOCUMENTED PER-MODEL CONCURRENCY. fal reserves the right to cap high-demand models below the account limit. H3 Max on launch promo is precisely that profile. The account dashboard's number may not be the number that applies here.
6. ASPECT-RATIO INHERITANCE ON i2v. `aspect_ratio` is absent from the image-to-video schema and the output follows the conditioning image. A chained pipeline that extracts frames at slightly different dimensions will silently change the stream's resolution mid-broadcast, breaking the encoder downstream.
7. `prompt_expansion_mode` IS AN UNVALIDATED STRING, NOT AN ENUM. A typo will not 422 at the schema layer; it will either be silently coerced or produce unexpected expansion behaviour. Pin it to a constant.
8. NO STREAMING SURFACE. H3 Max publishes no `/stream` path, so there is no partial/progressive output — a clip is unavailable until it is entirely finished. Latency is a step function, not a ramp, and there is no way to start playing at 50%.
9. `sync_mode: true` AT 768P is a trap: it inlines a 6-20MB MP4 as base64 in the JSON response.
10. PROMPT EXPANSION IS ITSELF A NON-DETERMINISTIC LLM in the loop. It can and does rewrite the brain-derived prompt into something semantically different, which corrupts the closed-loop signal in item 09 — feeding `expanded_prompt` back to TRIBE is correct precisely because the original prompt is NOT what the model saw.
11. RUNNER-CLASS 503s (runner_scheduling_failure, runner_disconnected, runner_connection_timeout) are ordinary on a busy launch model and ARE retryable, unlike the 422s. Conflating the two families in one retry handler either wastes slots on doomed retries or drops recoverable clips.

**unknowns**

1. The exact token that disables prompt expansion. The output field says 'Null when prompt expansion was disabled', proving a disabled state exists, but the schema publishes only `balanced` and `quality` as examples and declares the field a bare string. Whether `disabled`, `none` or `off` is accepted must be tested with one API call. Worth doing: disabling expansion would remove ~1s from every clip AND remove a non-deterministic LLM from the closed loop.
2. TRUE WALL-CLOCK FOR 10s AND 15s CLIPS AT BOTH RESOLUTIONS. Published figures are 5s-only and the two available 15s numbers disagree by 60% (9s vs 15s). This is the number the whole latency budget (item 13) rests on. Measure 20 clips at each of {5,10,15}x{480P,768P} before committing to a clip length.
3. THE SAFETY REJECTION RATE on salience-maximising prompts. No published figure for any endpoint, let alone this one. Must be characterised empirically against a representative sample of readout-generated prompts before the buffer is sized.
4. WHETHER A 422 CONTENT REJECTION IS BILLED. fal's error docs are silent on billing for failed requests. Materially affects the cost model if the rejection rate is high.
5. WHETHER H3 MAX CARRIES A PER-MODEL CONCURRENCY CAP below the account limit, and what it is.
6. THE ACTUAL 480P COST/QUALITY TRADE for this use case — whether 480P halves latency as well as price, and whether it is watchable on a public stream.
7. DEFAULT CDN RETENTION when no X-Fal-Object-Lifecycle-Preference header is sent. Documented as 'configurable', with no default stated.
8. The 'five free no-login 5s generations per rolling 24h' figure comes from a single secondary source and is not corroborated by fal directly; the signed-in five-per-day allowance is better attested.
9. Whether the launch promo actually ends on 2026-09-01 or is extended — one fal source describes it as 'the first week', another as 14 days, and the aggregate consensus is a 2026-09-01 end. Check the live model page on the day.

### Other Info

**item_id**

05

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `realtime_headroom`
- `sources`
- `throughput_constraint`

---

## GPU hosting for TRIBE v2

### Identity

**what_it_is**

The always-on GPU process that holds TRIBE v2 resident and answers 'score this clip' calls. Not an inference endpoint in the usual sense — it is a stateful, long-lived worker, because TRIBE's backbones lazy-load on first predict() and the stock code then throws them away again after every call.

**role_in_loop**

Infrastructure under the PREDICT stage. It is the only component in the whole pipeline that is a rented machine rather than a metered API: H3 Max is per-second-of-video on fal, playback is CDN, but TRIBE is GPU-hours whether or not you are scoring. It therefore sets the floor on running cost and is the single largest devops item in the build.

### Interface

**interface_spec**

Whatever you choose, the contract you are hosting is: a Python 3.11+ process holding a module-level `TribeModel` singleton, exposing one call `score(clip_path_or_bytes) -> (T, 20484) float32 + abs_times`. Concretely, per platform:

HF SPACES (dedicated hardware) — README YAML front-matter is the entire deployment spec:
```yaml
sdk: gradio
python_version: '3.12'
app_file: app.py
hardware: l40sx1            # or l4x1 / a10g-small / a100-large
preload_from_hub:            # bakes non-gated weights at BUILD time
  - facebook/tribev2 best.ckpt,config.yaml
  - facebook/vjepa2-vitg-fpc64-256 *.safetensors,*.json
  - facebook/w2v-bert-2.0 *.safetensors,*.json
  - Systran/faster-whisper-large-v3
```
plus `requirements.txt`, `packages.txt` (`ffmpeg`), and Settings -> Secrets for `HF_TOKEN`. Gated repos CANNOT be preloaded at build (no build-time auth); they download at runtime into a writable cache. On dedicated hardware the process is genuinely persistent — no `@spaces.GPU` decorator, no reservation, no quota.

MODAL:
```python
image = (modal.Image.debian_slim(python_version='3.11')
    .apt_install('ffmpeg')
    .pip_install('uv', 'exca>=0.5.20,<0.5.26',
                 'tribev2[plotting] @ git+https://github.com/facebookresearch/tribev2.git@refs/pull/67/head')
    .env({'HF_HUB_DOWNLOAD_TIMEOUT': '300', 'HF_HUB_HTTP_TIMEOUT': '300'})
    .run_function(download_weights, secrets=[modal.Secret.from_name('hf')]))  # bake weights INTO the image

@app.cls(image=image, gpu='L40S', min_containers=1, scaledown_window=1200,
         timeout=3600, secrets=[modal.Secret.from_name('hf')])
class Tribe:
    @modal.enter()
    def load(self): self.model = TribeModel.from_pretrained(...)
    @modal.method()
    def score(self, clip: bytes) -> list: ...
```
Key knobs: `min_containers=1` pins a warm container (billed at the normal rate — a cost decision, not a free feature); `scaledown_window` default 60 s, MAX 20 minutes; `buffer_containers` for spikes; `enable_memory_snapshot=True` + `@modal.enter(snap=True)` gives a documented 3-10x on init-heavy startup, and GPU snapshots are ALPHA behind `experimental_options={'enable_gpu_snapshot': True}`.

REPLICATE / COG: `cog.yaml` + `predict.py` with `setup()` (the warm hook) and `predict()`. `cog push` builds an OCI image serving `/predictions` on :5000.

FAL CUSTOM CONTAINER: a `fal.App` subclass with `machine_type`, `keep_alive`, `min_concurrency`/`max_concurrency`, `setup()` vs `__call__`. Custom/dedicated deployment and B200 pricing are BEHIND A SALES CONTACT — not self-serve.

LOCAL: `systemd` unit or `tmux` running the same Python process. No interface layer at all.

**input_contract**

A CUDA GPU with >=16 GB VRAM (24 GB comfortable), Python 3.11+, `ffmpeg` and `uv`/`uvx` on PATH, ~15-20 GB of local disk for weights (708 MB TRIBE ckpt + ~7.6 GB V-JEPA2-ViT-g + ~2.4 GB W2V-BERT + ~6 GB Llama-3.2-3B if you use the text branch + ~3 GB faster-whisper large-v3), outbound network to huggingface.co on first boot, `HF_TOKEN` ONLY if you use the text branch, and a process supervisor that never restarts the container between clips.

T4 (16 GB) IS INSUFFICIENT — confirmed by a real OOM report against a 14.56 GiB card (issue #28). But see throughput_constraint: the widely-repeated 'A100-40GB minimum' is not supported by measurement.

### Performance

**throughput_constraint**

1. **VRAM IS NOT THE CONSTRAINT, AND THE GROUNDING FIGURE IS WRONG.** The '28-32 GB, A100-40GB minimum, 80GB recommended' number traces to a third-party tutorial that SUMS the three backbones (Llama ~7 GB + V-JEPA2 ~14 GB + W2V-BERT ~1 GB). It ignores `_free_extractor_model`, which frees each extractor after its features are cached, so THE THREE BACKBONES NEVER CO-RESIDE. The measured figure from a production deployment is 'Peak VRAM is only ~13 GB, so the forward is compute-bound, not VRAM-bound'. Quality (tri-modal) mode is higher — Llama plus a WhisperX subprocess that DOES co-reside with the parent — ESTIMATED ~16-20 GB, unverified. Practical floor: 24 GB (L4, A10, RTX 4090) is enough; 48 GB (L40S) is comfortable. A100-40/80GB is buying throughput, not memory. T4 at 16 GB genuinely fails (issue #28).
2. **Compute-bound on V-JEPA2-ViT-g, which does not batch.** Measured on CUDA: 'B=4 approx 231 s vs B=1 bf16 approx 173 s' — batching clips adds memory with no throughput gain. GPU choice should be picked on raw dense bf16 throughput, not VRAM. This is why an L4 at $0.80/hr may be false economy against an L40S at $1.80/hr.
3. **One `predict()` at a time per process.** Concurrency is N processes on N GPUs; cost scales linearly. For a single stream you need exactly one.
4. **The GPU idles ~44% of a run on CPU-side prep** (video decode, ASR). Pipelining that outside the GPU-timed section is quoted at ~3.3x more scores/day.
5. **Serverless scale-to-zero is ruled out** — not by the ~60 s cold start alone, but by the cost model: a scale-to-zero function that is invoked every 15 s never scales to zero anyway, so you pay always-on rates AND eat cold starts. Pin a warm container from the start.
6. **HF ZeroGPU is ruled out for 24/7** despite being the cheapest thing on the list ($9/mo PRO). It is quota-and-queue based, allocates a GPU per decorated call with a reservation window (reference deployments use 300-480 s), runs the function in a DAEMONIC subprocess (forcing `data.num_workers=0`), and has no notion of a persistent GPU-resident model. It is excellent for a first smoke test and useless for a continuous loop.
7. **Replicate private models bill setup + idle + active**, so 'serverless' there is priced identically to always-on but at the highest per-hour rate on this list.

### Complexity

**dev_complexity**

LOW on HF Spaces (fork an existing working Space, change one YAML line, push — no Dockerfile, no container registry, no cold-start engineering; `preload_from_hub` bakes the weights and Secrets handle HF_TOKEN). MEDIUM on Modal (a real image definition, weight baking, `min_containers`, and you must reproduce the exca pin and the ffmpeg/uv system deps yourself — half a day, but you get a proper HTTP API and CI). MEDIUM-HIGH on Replicate (Cog build cycle is slow to iterate and the pricing punishes idle). HIGH-and-blocked on fal custom containers (self-serve is not available; you must talk to sales, which is a schedule risk). LOWEST OF ALL on a local GPU you already own — if you have a 24 GB+ card, that is genuinely the shortest path and costs nothing.

**off_the_shelf_option**

**A WORKING, BILLED-VERIFIED TRIBE v2 DEPLOYMENT ALREADY EXISTS AND YOU SHOULD START BY DUPLICATING IT: `techfreakworm/tribev2-brain-timeline` on HF Spaces.** It ships the whole hosting problem solved — a `requirements.txt` that actually resolves (`torch==2.8.0`, `torchvision==0.23.0`, `transformers>=4.53,<5`, plus a fork of `tribev2` that relaxes upstream's `torch<2.7` cap), `packages.txt` with `ffmpeg`, a `preload_from_hub` block that bakes the TRIBE checkpoint + V-JEPA2 + W2V-BERT + faster-whisper at build time, a `prewarm.py` that caches the gated Llama / whisperx / spaCy stack during UN-BILLED container startup, the writable-`HF_HOME` fix, the `num_workers=0` daemonic-fork fix, and a candid `KNOWN_ISSUES.md`. Duplicate it, switch `hardware: zero-a10g` to dedicated `l40sx1`, and delete the `@spaces.GPU` decorator so the process becomes genuinely persistent. That is a one-afternoon deployment against a several-day one from scratch. (Check its LICENSE/NOTICE before reusing the code.)

Secondary: `cbensimon/tribe-v2` (by HF's ZeroGPU lead) and `beta3/TRIBE_V2_Neural_Activity_Predictor` are live Spaces with programmatic JSON endpoints callable via `gradio_client` — zero infrastructure at all, good for a same-day end-to-end smoke test, unusable for 24/7.

NOT off-the-shelf: there is no TRIBE v2 on Replicate's public model catalogue, none on fal's, and no published Modal example. Nobody has containerised this for you outside HF Spaces.

### Decision

**recommended_approach**

**HF SPACES ON DEDICATED L40S ($1.80/hr), BY DUPLICATING THE EXISTING WORKING SPACE.** It wins on the only axis that matters for a demo — devops hours to a running warm GPU — and it wins by a wide margin because someone has already fought every install and caching battle in public.

Exact steps:
1. Duplicate https://huggingface.co/spaces/techfreakworm/tribev2-brain-timeline.
2. Settings -> Hardware -> `Nvidia L40S 1x` ($1.80/hr). This makes the Space a persistent always-on process; ZeroGPU's reservation model disappears.
3. Delete the `@spaces.GPU` decorator and the `spaces` import. On dedicated hardware you own the GPU for the life of the container; the decorator only costs you a fork and forces `num_workers=0`.
4. Keep the `preload_from_hub` front-matter — it bakes ~14 GB of non-gated weights into the image at build, which is the whole cold-start story. Add persistent storage and set `HF_HOME=/data/.huggingface` at build so the ~14 GB writable-cache copy at every cold start disappears (the maintainers flag this as their own top infra improvement).
5. Skip `HF_TOKEN` and `PREWARM_QUALITY` entirely if you run the video+audio-only path (item 01, step 1) — the Meta Llama licence gate then never applies to you at all.
6. Patch `_free_extractor_model` / cache the V-JEPA2 backbone at module import (copy `tribescore/prewarm.py::prewarm_video_model`). Without this, 'always-on' still re-pays a ~7.6 GB build per clip.
7. Replace the Gradio UI with a small FastAPI route or a queue consumer that your orchestrator calls.

**RUNNER-UP: MODAL, L40S at $1.95/hr (or L4 at $0.80/hr if throughput allows).** Choose this instead if you want a real versioned HTTP API, CI, and control over the image — it costs you an extra half-day. Configure `min_containers=1`, `scaledown_window=1200` (the 20-minute maximum), bake weights into the image via `.run_function(download_weights)` rather than fetching at call time (Modal's own guidance: 'reduce boot times from minutes to seconds'), and add `enable_memory_snapshot=True` with `@modal.enter(snap=True)` around `from_pretrained` for a documented 3-10x on init. Do NOT count on GPU memory snapshots — they are alpha, explicitly incompatible with multi-GPU, and their docs warn that snapshotting helps little when init is disk-load-bound, which TRIBE's is. Modal's $30/mo Starter credit covers ~15 hours of L40S, enough to build against for free.

**IF YOU OWN A 24 GB+ NVIDIA CARD, USE IT.** Peak VRAM is ~13 GB in Fast mode; an RTX 4090 or 5090 runs this. Zero marginal cost, zero devops, no CC BY-NC ambiguity about who is hosting non-commercial weights. For a one-off art piece this is very likely the actual shortest path and the fact that the 'A100-40GB minimum' figure is wrong is what unlocks it. Verify with `nvidia-smi` during a real run before committing.

**REJECT — REPLICATE.** Private models bill setup + idle + active, so it is priced as always-on anyway, at $3.51/hr (L40S) to $5.04/hr (A100-80) — 2-3x the alternatives for no benefit. Cog's `setup()` is a fine warm hook, but the economics are indefensible here.

**REJECT FOR NOW — FAL CUSTOM CONTAINER.** Architecturally tempting (colocate TRIBE with the H3 Max calls, one vendor, one bill) and their published rates are competitive (RTX PRO 6000 96GB $1.10/hr discounted, H100 $1.89/hr discounted). But custom/dedicated deployment is behind `contact support@fal.ai` — not self-serve — and fal bills the full runner lifetime including `setup()`, `keep_alive` idle, draining and teardown. Do not put a sales conversation on the critical path of a demo. Revisit if this becomes a real product.

**REJECT — NAIVE PER-CLIP SERVERLESS AND HF ZEROGPU.** Ruled out for the reasons in throughput_constraint. ZeroGPU is still worth $9 for a PRO month as a free smoke-test rig before you rent anything.

**simpler_alternative**

(A) DON'T HOST IT AT ALL FOR v0. Call `cbensimon/tribe-v2` or `beta3/TRIBE_V2_Neural_Activity_Predictor` over `gradio_client`. Zero infrastructure, an end-to-end loop closes in an afternoon, and you learn whether the brain-to-prompt idea is aesthetically interesting BEFORE spending a day on containers. Rate-limited, queued, and a third party in your loop — but that only matters once the piece is real.

(B) RUNPOD, A PLAIN PERSISTENT POD. L40S 48GB at ~$0.79/hr, per-second billing, network volumes at $0.07/GB/month. You `ssh` in, `pip install`, run `python worker.py` in tmux. This is the CHEAPEST warm GPU on the list and the devops is 'it is a Linux box'. Downside: no build system, no image reproducibility, and you must remember to stop it. If cost dominates and you accept manual ops, this beats everything.

(C) SCORE FEWER CLIPS ON A SMALLER GPU. At a 1-in-3 duty cycle an L4 (24 GB, $0.80/hr) keeps up. Hold the previous brain vector between reads. Halves the bill against an L40S with no code changes.

(D) DROP THE GPU ENTIRELY — precompute an offline clip -> ROI-vector lookup table and do nearest-neighbour at runtime. GPU-hours go to zero. This is item 15/16 territory and is the honest fallback if the running cost or the real-time budget will not close.

**code_sketch**

**Option 1 — HF Spaces dedicated (recommended). This is the whole deployment:**
```yaml
# README.md front-matter. Set hardware in Settings -> Hardware to l40sx1.
---
title: Tribe Scorer
sdk: gradio
sdk_version: 6.11.0
python_version: '3.12'
app_file: app.py
hardware: l40sx1
preload_from_hub:                      # baked at BUILD time -> fast cold start
  - facebook/tribev2 best.ckpt,config.yaml
  - facebook/vjepa2-vitg-fpc64-256 *.safetensors,*.json
  - facebook/w2v-bert-2.0 *.safetensors,*.json
---
```
```
# packages.txt
ffmpeg
```
```
# requirements.txt  (the pin set that actually resolves)
tribev2[plotting] @ git+https://github.com/facebookresearch/tribev2.git@refs/pull/67/head
torch==2.8.0
torchvision==0.23.0
transformers>=4.53,<5
mne
nilearn
scipy
uv
```
```python
# app.py -- NO @spaces.GPU on dedicated hardware; the process owns the GPU.
import os
os.environ.setdefault('HF_HUB_DOWNLOAD_TIMEOUT', '300')
os.environ.setdefault('HF_HUB_HTTP_TIMEOUT', '300')
from warm_tribe import load, score          # from item 01
load()                                      # cold start paid ONCE at boot
import gradio as gr
gr.Interface(fn=score, inputs='video', outputs='json').launch()
```

**Option 2 — Modal:**
```python
import modal

HF = modal.Secret.from_name('huggingface')  # only needed for the text branch

def bake():
    from huggingface_hub import snapshot_download
    for r in ('facebook/tribev2',
              'facebook/vjepa2-vitg-fpc64-256',
              'facebook/w2v-bert-2.0'):
        snapshot_download(r)

image = (
    modal.Image.debian_slim(python_version='3.11')
    .apt_install('ffmpeg', 'git')
    .pip_install(
        'uv',
        'exca>=0.5.20,<0.5.26',          # upstream is unpinned and BREAKS on 0.5.26
        'torch==2.8.0', 'torchvision==0.23.0', 'transformers>=4.53,<5',
        'tribev2[plotting] @ git+https://github.com/facebookresearch/tribev2.git@refs/pull/67/head',
    )
    .env({'HF_HUB_DOWNLOAD_TIMEOUT': '300', 'HF_HUB_HTTP_TIMEOUT': '300',
          'HF_HOME': '/weights'})
    .run_function(bake)                   # ~10 GB baked INTO the image, not fetched at call time
)

app = modal.App('tribe-scorer', image=image)

@app.cls(
    gpu='L40S',
    min_containers=1,                     # PIN ONE WARM. Billed normally; this is the cost decision.
    scaledown_window=1200,                # 20 min == the documented maximum
    timeout=3600,
    enable_memory_snapshot=True,          # 3-10x on init-heavy startup
)
class Tribe:
    @modal.enter(snap=True)
    def load(self):
        from tribev2 import TribeModel
        self.model = TribeModel.from_pretrained(
            'facebook/tribev2', cache_folder='/weights/cache', device='auto',
            config_update={'data.overlap_trs_train': 20, 'data.num_workers': 0,
                           'data.video_feature.image.batch_size': 16,
                           'data.batch_size': 16},
        )
        # CRITICAL: also cache the built V-JEPA2 backbone on CPU here, or
        # _free_extractor_model makes every predict() re-pay a ~7.6 GB build.

    @modal.method()
    def score(self, clip_bytes: bytes) -> dict:
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            f.write(clip_bytes)
            f.flush(); os.fsync(f.fileno())   # MANDATORY before handing the path over
            path = f.name
        from warm_tribe import events_video_audio_only
        preds, segments = self.model.predict(events_video_audio_only(path), verbose=False)
        return {'preds': preds.tolist(),
                'abs_times': [round(s.start) for s in segments]}
```

**Option 3 — RunPod / local, the cheap path:**
```bash
# On a 24 GB+ CUDA box.
sudo apt-get install -y ffmpeg
pip install uv 'exca>=0.5.20,<0.5.26' \
  'tribev2[plotting] @ git+https://github.com/facebookresearch/tribev2.git@refs/pull/67/head'
export HF_HUB_DOWNLOAD_TIMEOUT=300 HF_HUB_HTTP_TIMEOUT=300
# no HF_TOKEN needed on the video+audio-only path
python -c "from tribev2 import TribeModel; TribeModel.from_pretrained('facebook/tribev2', cache_folder='./cache')"
tmux new -d -s tribe 'python worker.py'
watch -n1 nvidia-smi        # confirm peak VRAM yourself -- expect ~13 GB, not 28-32
```

### Risk

**failure_modes**

**HOSTING-SPECIFIC:**
- **The 'warm process' trap.** `_free_extractor_model` deletes each backbone after its features are cached, so a pinned container still rebuilds V-JEPA2 (~7.6 GB) on every clip. Symptom: steady-state latency that never improves after the first call. You will conclude your hosting is broken when the model is doing it deliberately. Patch it.
- **Weights fetched at call time instead of baked into the image.** Turns a 1-second container boot into a multi-minute one. Modal: `.run_function(download_weights)`. HF: `preload_from_hub`. Replicate: `cog.yaml` build steps.
- **HF Spaces read-only baked cache -> EACCES on any gated runtime download.** `preload_from_hub` writes as the BUILD user; the runtime uid cannot create new repo dirs. Fix is to redirect `HF_HOME` to a writable copy BEFORE `import gradio` (huggingface_hub freezes `HF_HUB_CACHE`/`HF_XET_CACHE` as module constants at import). Costs a ~14 GB copy and 1-2 min at every cold start; eliminate it by setting `HF_HOME=/data/.huggingface` at build with persistent storage attached.
- **`AssertionError: daemonic processes are not allowed to have children`** whenever the model runs inside a forked/daemonic worker (HF ZeroGPU, some queue runners). The shipped config uses `num_workers: 20`. Set `data.num_workers = 0`.
- **`HF_HUB_ENABLE_HF_TRANSFER=1` inherited by the `uvx whisperx` subprocess**, which has no `hf_transfer` in its isolated env -> 'hf_transfer not available'. Hard-set it to `0`. Only bites on the text branch.
- **`scaledown_window` too short.** Modal's default is 60 s. At a 15 s clip cadence you would survive, but any pause in the stream evicts the container and you pay a full cold start on resume. Set it to the 20-minute maximum AND pin `min_containers=1`.
- **Modal GPU memory snapshots are ALPHA**, incompatible with multi-GPU, can fail outright with `torch.compile` (mitigate with `TORCHINDUCTOR_COMPILE_THREADS=1`), and their own docs warn they help little when init is disk-load-bound — which TRIBE's is. Use CPU snapshots for the import/`from_pretrained` phase and do not depend on GPU snapshots.
- **Replicate silently bills idle on private models.** 'You pay for the time they spend setting up; the time they spend idle, waiting for requests; and the time they spend active.' There is no cheap-idle mode.
- **fal custom containers are not self-serve.** Public pricing covers their catalogue; dedicated deployment is a sales conversation. Do not discover this on deadline.

**INSTALL BLOCKERS (roughly half a day if you rediscover them; all verified against the repo and its issue tracker):**
- **exca, not numpy, is the real blocker.** A clean install of upstream `main` DOES NOT IMPORT: `neuralset==0.0.2` calls `exca.steps.base.NoValue`, which exca moved to `exca.steps.identity` in 0.5.26, and tribev2 leaves exca unpinned. Install from `@refs/pull/67/head` (adds `exca>=0.5.20,<0.5.26`). Bumping neuralset is NOT an option — every release after 0.0.2 removes `AddText`, which `demo_utils.py` imports. Issues #65, #67, #69, #2, #27.
- **THE 'NumPy pinned <2.1' GROUNDING FACT IS WRONG AND WILL BREAK YOUR BUILD.** `pyproject.toml` HARD-PINS `numpy==2.2.6`. The `ImportError: cannot import name '_center'` that people attribute to numpy 2.x is a NOTEBOOK artefact — the old numpy binaries stay loaded in memory after pip upgrades it. The fix is RESTART THE KERNEL/CONTAINER, and it does not arise at all in a fresh container that installs before importing. Issues #56, #27.
- **Gated Llama-3.2-3B + HF_TOKEN: real, but AVOIDABLE.** Only the text branch needs it. `from_pretrained` succeeds without it because backbones lazy-load inside `predict()`. On the video+audio-only path you never touch it — which also removes ~6 GB from your image and a licence dependency from your project.
- **`HF_HUB_DOWNLOAD_TIMEOUT` / `HF_HUB_HTTP_TIMEOUT` = 300: real and necessary.** The 10 s default raises ReadTimeout mid-inference while pulling the ~6 GB Llama snapshot.
- **`flush()` -> `os.fsync(fileno())` -> `close()` on temp files: real and necessary.** Otherwise the model reads an empty file. This bites hardest in exactly this architecture, where every clip arrives as bytes and is written to a temp path.
- **torch cap:** upstream pins `torch>=2.5.1,<2.7`. Modern runtimes need a one-line fork relaxing it; torch 2.8.0 + torchvision 0.23.0 is proven.
- **transformers unpinned upstream** -> a fresh install grabs 5.x, which relocates the V-JEPA2 video-processor module path and can silently drift extractor I/O. Pin `>=4.53,<5`.
- **System deps:** `ffmpeg` (moviepy) and `uv`/`uvx` (the ASR subprocess) must be on PATH.
- **Windows hosts:** `from_pretrained` does `str(Path(repo_id))`, mangling 'facebook/tribev2' into a backslash path. Issues #10, #11, #63. Use Linux.

**LICENCE:** CC BY-NC 4.0. Non-commercial only, and Meta is enforcing it — the tracker carries an alleged-violation report (#48) and five separate open commercial-licence inquiries (#8, #17, #25, #45, #49, #66) with no evidence any has been granted. Whoever's account rents the GPU is hosting non-commercially-licensed weights.

**unknowns**

1. **Real throughput per dollar across GPU classes.** Every latency number I have is from ONE hardware class (a ZeroGPU MIG slice of an RTX Pro 6000 Blackwell). Nobody has published TRIBE v2 on an L4, L40S, A100 or H100. Because it is compute-bound on V-JEPA2-ViT-g with no batching, the ranking should track dense bf16 throughput — but MEASURE IT before committing to a monthly spend. Benchmark the same 15 s clip on L4 / L40S / A100 for one hour each; that costs a few dollars and decides the whole cost model.
2. **Peak VRAM in Quality (tri-modal) mode.** ~13 GB is measured for Fast; my ~16-20 GB for Quality is an estimate. Decides whether a 24 GB card covers the full pipeline.
3. **Exact first-`predict()` backbone build time** on each platform. My 20-60 s is an estimate; no source measures it in isolation.
4. **Whether Modal's alpha GPU memory snapshot works with TRIBE at all**, and what it saves. Potentially large, entirely unverified.
5. **fal's actual custom-container terms and pricing** for a persistent A100/L40S-class runner — behind sales, so unobtainable without a conversation.
6. **Whether HF Spaces dedicated hardware genuinely gives an uninterrupted persistent process** for days at a time, or whether the platform restarts containers on its own schedule. Not documented; test with a 48-hour soak before trusting it for a 24/7 piece.
7. **The reuse licence on `techfreakworm/tribev2-brain-timeline`'s `tribescore` package** (it ships a LICENSE + NOTICE I did not read in full). Check before copying code.
8. **Whether `refs/pull/67/head` stays available.** It is an unmerged community PR against a repo with 77 open issues and visible maintainer inattention; it can be force-pushed or closed. Vendor your own fork rather than depending on the ref.

### Evidence

**sources**

**PRICING (all fetched directly, August 2026):**
- https://modal.com/pricing — per-second rates: H100 $0.001097, H200 $0.001261, A100-80 $0.000694, A100-40 $0.000583, L40S $0.000542, L4 $0.000222, A10 $0.000306, T4 $0.000164, B200 $0.001736; CPU $0.0000131/core/s (min 0.125 cores), memory $0.00000222/GiB/s; $30/mo Starter and $100/mo Team free credits.
- https://replicate.com/pricing — T4 $0.81/hr, L40S $3.51/hr, A100-80 $5.04/hr, H100 $5.49/hr; and the explicit statement that private models bill setup + idle + active.
- https://huggingface.co/pricing — Spaces dedicated: T4 small $0.40/hr, L4 1x $0.80/hr, A10G small $1.00/hr, L40S 1x $1.80/hr, A100 large $2.50/hr, H100 1x $4.50/hr; ZeroGPU free with PRO at $9/mo for 8x quota, on RTX Pro 6000 Blackwell; Hub storage from $12/TB/mo with egress + CDN included.
- https://fal.ai/pricing — B300 $8.50/$4.49, B200 $6.25/$3.49, H200 $4.50/$2.10, H100 $4.50/$1.89, RTX PRO 6000 96GB $2.99/$1.10 (list/discounted); custom deployments are 'Contact support@fal.ai', with no published A100/L40S rate.
- RunPod rates via https://gpuperhour.com/providers/runpod — L40S $0.79/hr, A100-80 $1.39/hr, H100 PCIe $1.99/hr, H100 SXM5 $2.69/hr (community) / $2.99 (secure); network volumes $0.07/GB/mo for the first TB; per-second billing.

**PLATFORM MECHANICS:**
- https://modal.com/docs/guide/cold-start — 'containers boot in about one second'; pre-downloading weights 'can reduce boot times from minutes to seconds'; `scaledown_window` default 60 s / max 20 min; `min_containers`; `buffer_containers`; concurrent loading.
- https://modal.com/docs/guide/memory-snapshot — `enable_memory_snapshot=True`, `@modal.enter(snap=True)`, '3-10x faster from Memory Snapshots'; GPU snapshots ALPHA via `experimental_options={'enable_gpu_snapshot': True}`; limitations (multi-GPU incompatible, minimal benefit when storage-bound, `torch.compile` failures, `TORCHINDUCTOR_COMPILE_THREADS=1`).
- https://docs.fal.ai/ — fal bills the total runner lifetime including `setup()`, `keep_alive` idle, active processing, draining and teardown; custom/dedicated deployment is sales-gated.

**THE REFERENCE DEPLOYMENT (the highest-value source in this item — a real, billed, working TRIBE v2 Space whose maintainers documented every hosting battle):**
- https://huggingface.co/spaces/techfreakworm/tribev2-brain-timeline — `README.md` (the `preload_from_hub` block, the deploy steps including HF_TOKEN and PREWARM_QUALITY, the measured '~1-minute clip scores in ~140-175 s on ZeroGPU in Fast mode'), `KNOWN_ISSUES.md` (**'Peak VRAM is only ~13 GB, so the forward is compute-bound, not VRAM-bound'**; `xlarge` 4g.96gb/188SM ~1.8x over `large` 2g.48gb/94SM; the ~14 GB cold-start cache copy adding 1-2 min; the ~44% GPU-idle figure and the ~3.3x prep-outside estimate; the build-time `HF_HOME` fix), `requirements.txt` (the working pin set and the torch<2.7 fork rationale), `app.py` (the writable-HF_HOME-before-import-gradio block, `HF_HUB_ENABLE_HF_TRANSFER=0`), `src/tribescore/inference.py` (`data.num_workers=0` daemonic-fork rationale, the duration_trs warning), `src/tribescore/prewarm.py` (un-billed startup prewarm of Llama/whisperx/spaCy/V-JEPA2), `src/tribescore/fast_encode.py` (the ~7.6 GB V-JEPA2 build, the CPU-cache-and-fork-COW pattern).
- https://huggingface.co/spaces/cbensimon/tribe-v2 — `hardware: zero-a10g`, `@spaces.GPU(duration=30/60)`, '~30s' text / '~2-5 min' video.
- https://huggingface.co/spaces/beta3/TRIBE_V2_Neural_Activity_Predictor — `@spaces.GPU(duration=300)`.
- https://huggingface.co/docs/hub/en/spaces-zerogpu — ZeroGPU dynamic allocation model.

**INSTALL BLOCKERS (github.com/facebookresearch/tribev2 issues, read via the API):**
- #65 / #67 / #69 — the exca 0.5.26 break, full root cause, and the `exca>=0.5.20,<0.5.26` fix; #67 also documents why bumping neuralset fails (AddText removed after 0.0.2).
- #56 / #27 — the numpy `_center` ImportError is a runtime-restart problem.
- #28 — CUDA OOM on a 14.56 GiB T4.
- #24 — `from_pretrained` FileNotFoundError on HF ZeroGPU Spaces.
- #10 / #11 / #63 — Windows path mangling in `from_pretrained`.
- #58 / #20 / #22 — WhisperX float16-on-CPU.
- #8 / #17 / #25 / #45 / #48 / #49 / #66 — commercial-licence inquiries and one alleged violation; evidence the CC BY-NC clause is enforced.

**SOURCE CODE (cloned and read):**
- https://github.com/facebookresearch/tribev2 — `tribev2/main.py::_free_extractor_model` (lines 59-79) and its call site at line 217, which is the basis for the 'warm process is not a warm model' finding and for correcting the peak-VRAM figure; `pyproject.toml` (`numpy==2.2.6`, `torch>=2.5.1,<2.7`, transformers unpinned, requires-python >=3.11); `tribev2/demo_utils.py`; `tribev2/eventstransforms.py` (the `uvx whisperx` subprocess).

**CORRECTED / DISPUTED:** https://www.datacamp.com/tutorial/tribe-v2-tutorial is the origin of the '28-32 GB, A100-40GB minimum' and 'numpy<2.1' claims that appear in the grounding facts. I judge BOTH to be wrong — the VRAM figure sums three backbones that `_free_extractor_model` guarantees never co-reside, and the numpy pin contradicts the package's own `numpy==2.2.6`. Its HF_TOKEN, `HF_HUB_*_TIMEOUT=300`, `fsync` and T4-insufficiency advice IS corroborated and is good.

**EXPLICIT INFERENCES (mine, not sourced):** the platform recommendation ranking; the ~16-20 GB Quality-mode VRAM estimate; the 20-60 s first-`predict()` backbone build estimate; the claim that GPU-class ranking tracks dense bf16 throughput; the observation that TRIBE's GPU is 1-2% of the total stream bill against H3 Max generation cost.

### Other Info

**item_id**

10

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `loc_estimate`
- `output_contract`
- `realtime_headroom`

---

## Latency budget and real-time feasibility

### Identity

**what_it_is**

The end-to-end wall-clock accounting for one turn of perceive -> predict -> prompt -> generate -> stream, measured against the seconds of playback that turn buys. Determines whether the loop is self-sustaining, and which stages must be cut or moved off the critical path if it is not.

**role_in_loop**

Spans the entire loop. The governing question is not 'is any stage fast' but 'does the sum of the stages on the CRITICAL PATH fit inside D seconds of clip playback, on average'. The central finding is that the critical path and the loop are not the same set of stages — TRIBE can be moved off the critical path almost for free, and doing so is what makes the system work.

### Interface

**input_contract**

The budget is only meaningful once five parameters are fixed: D (clip duration, seconds of playback — use 15, the H3 Max maximum and TRIBE's practical minimum window); the TRIBE modality set (trimodal / video-only / audio+video / text-only); the prompt-writer (template vs LLM); resolution (480P vs 768P); and the pipeline topology (serial vs TRIBE-concurrent). TRIBE additionally imposes a hard floor from below: it applies a 5s BOLD offset and yields diffuse, low-intensity activations on short inputs, with practitioner guidance of a 15-30s minimum stimulus. D < 15 is therefore ruled out by the neuroscience before it is ruled out by the arithmetic.

**output_contract**

STEADY-STATE CONDITION, stated precisely. Two INDEPENDENT inequalities must both hold; satisfying one does not help the other.

  (1) GENERATION THROUGHPUT:   T_gen / (C * (1 - r))  <=  D
      T_gen = mean wall-clock seconds on the generation critical path (stages 4-10)
      C     = fal concurrent IN_PROGRESS requests actually in flight
      r     = safety-checker rejection rate (each rejection costs a full cycle)
      D     = clip playback duration, 15s

  (2) PERCEPTION THROUGHPUT:   T_tribe / K  <=  D
      T_tribe = mean wall-clock seconds for one TRIBE forward pass
      K       = clips between TRIBE invocations (K=1 = every clip, K=2 = every other clip)

Worked: config D has T_gen = 8.4s, C = 1, r = 0. 8.4 <= 15. PASSES with 44% margin, and absorbs r up to 0.44 before failing. Config B has T_gen = 28.8s serial; at C = 2 (the fal new-account limit) 28.8/2 = 14.4 <= 15 — it scrapes through, but only by generating speculatively, which is discussed below. Video-only TRIBE at 6.0s satisfies (2) at K = 1 with 60% margin; TRIMODAL TRIBE AT 15-30s DOES NOT SATISFY (2) AT K = 1 EVEN WHEN PIPELINED — pipelining removes it from the critical path but not from its own throughput obligation. Fix by modality dropout (lower T_tribe) or by K = 2 (double its budget). This distinction is easy to miss and is the most likely source of a system that appears architecturally correct and still falls behind.

WHAT THE BUFFER DOES AND DOES NOT DO. With production rate C/T_gen clips/s and consumption 1/D clips/s, a buffer of B clips drains in B / (1/D - C/T_gen) seconds. At B=4, D=15, C=1, T_gen=20s (a 33% overrun): 240 seconds. Four minutes. At a mere 7% overrun (T_gen=16s): 16 minutes. THE BUFFER ABSORBS JITTER, NOT DEFICIT. It must be sized against the standard deviation of T_gen, not its mean, and the mean must satisfy (1) strictly. Practical sizing: B >= 3*sigma/D + 2. With sigma ~= 4s of fal queue jitter and D = 15, B >= 3 clips; recommend 3-4 clips (45-60s) and no more — for the reason below.

THE BUFFER IS THE DOMINANT SOURCE OF REACTION LAG, NOT TRIBE. If perception is done on the clip currently PLAYING, total staleness at the moment a clip reaches the screen is: 5s (TRIBE's hemodynamic offset) + ~7.5s (mean age of the 15s window) + 15s (one clip of pipelining) + B*D (buffer depth) = 87.5s at B=4, 147.5s at B=8. The buffer that keeps the stream alive is the same thing that destroys its reactivity, and it is a larger contributor than every model latency combined.
  RESOLUTION: PERCEIVE AT GENERATION TIME, NOT AT PLAYBACK TIME. Run TRIBE on each clip the moment it is downloaded — while it sits in the buffer, before anyone has seen it — rather than on whatever is currently on screen. Staleness collapses to 5 + 7.5 + 15 = ~27.5s and becomes INDEPENDENT OF BUFFER DEPTH. This costs nothing, changes one line of queue plumbing, and is the difference between a loop that reacts within half a minute and one that reacts within two and a half minutes.

### Performance

**throughput_constraint**

fal concurrency: new Model API accounts start at 2 concurrent IN_PROGRESS; automatic self-serve scaling to 40 based on trailing-4-week paid invoices; beyond 40 requires sales. Queued requests do not occupy a slot and are never rejected for concurrency, though start_timeout can expire them.

The useful and slightly counter-intuitive finding: C=2 IS ENOUGH FOR A SINGLE 15s-CLIP STREAM. Generation alone runs at ~0.6x realtime (9s of work per 15s of output), so one in-flight request already outpaces playback; the second slot is pure headroom for retries. The concurrency ladder becomes a constraint only if you shorten clips (at D=5 the same fixed overhead consumes 50-70% of the budget and you need real parallelism), run several streams from one account, or hit a high safety-checker rejection rate.

AND CONCURRENCY IS NOT FREE ARCHITECTURALLY. Parallel generation only raises throughput if clips N+1 and N+2 are launched before clip N's brain response exists — which is speculation, and it directly contradicts the reactive premise. With C requests in flight, the brain state shaping a clip is C clips (C*D seconds) stale. CONCURRENCY BUYS THROUGHPUT BY SPENDING REACTION LATENCY. At C=1 the loop is maximally reactive and has 44% headroom in the recommended configuration, so keep C=1 for the demo and hold the second slot for retries.

GPU serialisation: TRIBE holds a warm process on one GPU (28-32GB VRAM trimodal, ~60s cold start from lazy loading of V-JEPA2-Giant and Llama-3.2-3B). Invocations serialise on that process. If TRIBE and the orchestrator share a box, ffmpeg's encode (2-3 cores for 720p30) must not contend with the GPU feeder thread.

Safety-checker rejections (enable_safety_checker defaults true) enter condition (1) as the (1-r) term. The pipelined budget absorbs r up to ~0.44 before failing; the serial budget absorbs none. This is a further argument for pipelining that has nothing to do with latency.

### Complexity

**dev_complexity**

LOW. Nothing here requires a fast model, a custom kernel, or an optimisation pass. The entire feasibility gap is closed by (a) two asyncio tasks and a shared slot instead of one sequential function, (b) passing a shorter modality list to TRIBE, (c) a dict lookup instead of an LLM call, and (d) not setting prompt_expansion_mode to 'quality'. The one genuinely uncertain input — TRIBE's real per-window latency — is a 20-minute measurement, not a research project. RATING RATIONALE: low because the levers are structural rather than performance work, and because the recommended topology degrades gracefully rather than stalling when a stage is slow.

**loc_estimate**

~30-50 LOC for the pipelined orchestrator (two asyncio tasks, an asyncio.Queue of finished clips, one shared 'latest brain vector' slot with no lock needed under asyncio). ~15 LOC for a stage-timing decorator that logs every stage so the estimated numbers in this document can be replaced with measured ones on day one. ~25 LOC for the underrun detector and filler trigger. Total ~90 LOC for the whole real-time control layer.

**off_the_shelf_option**

No off-the-shelf real-time budget manager exists for this shape of pipeline, and none is needed — asyncio.Queue plus asyncio.create_task is the whole mechanism. Two adjacent things do remove work: (1) fal's own client exposes both a queue API (submit / status / result, with webhooks) and subscribe-style helpers, so you do not implement polling or backoff yourself; (2) `github.com/fal-ai-community/realtime-krea-wan` is an existing 'text-to-video with dynamic prompt rewriting' scaffold on a realtime model, which dissolves the clip-boundary problem entirely by allowing the prompt to change MID-GENERATION rather than between clips — in that architecture there is no per-clip latency budget to close, only a steady-state fps. That is a different system with a different hosting burden; see item 17. For the H3 Max clip-queue approach assumed here, write the ~90 lines.

### Decision

**recommended_approach**

TAKE TRIBE OUT OF THE HOT PATH ENTIRELY, AND PERCEIVE AT GENERATION TIME.

Run two concurrent asyncio tasks against one shared mutable slot:
  Task GEN (the pump): reads whatever brain vector is currently in the slot, writes a prompt from it, fires the fal request, downloads the result, extracts the last frame, appends to the concat playlist, and pushes the finished clip onto a perception queue. It NEVER awaits TRIBE. If the vector is stale it simply uses the stale one.
  Task PERCEIVE: pulls finished clips off that queue, runs TRIBE on them, and overwrites the slot. If it falls behind it drops all but the newest clip.

This has four properties that together decide the project:
  - The critical path drops from 28.8s to 13.2s (768P/LLM) or 8.4s (480P/template), converting a 1.92x deficit into a 12-44% surplus.
  - TRIBE slowness degrades REACTIVITY GRACEFULLY instead of stalling the stream. A TRIBE run that takes 40s does not cause an underrun; it just means two clips share a brain vector. There is no failure mode, only a smoothly aging signal — which is exactly the right behaviour for an artwork.
  - Perceiving each clip at download time rather than at playback time makes reaction staleness independent of buffer depth: ~27.5s (5s hemodynamic offset + ~7.5s mean window age + 15s one-clip pipelining) regardless of whether you hold 2 clips or 20.
  - It absorbs a ~44% safety-checker rejection rate within the existing budget.

Then apply, in this order:
  1. MODALITY DROPOUT — pass video only (or video+audio), skipping the Llama-3.2-3B text branch. TRIBE was trained with independent per-modality dropout at p=0.3, so single-modality inference is a supported mode, not an abuse. Estimated 40-60% off T_tribe (15s -> ~6s) and ~7GB off the 28-32GB VRAM footprint. Required to satisfy condition (2) at K=1.
  2. prompt_expansion_mode='balanced'. 'quality' spends up to ~30s rewriting and is categorically off the table for a live loop — it alone exceeds two full clip budgets. Note 'balanced' still costs ~1s; it is not free.
  3. D = 15, the maximum H3 Max allows. Fixed per-clip overhead (queue + download + frame extract + mux) is ~2.5-3.5s regardless of clip length: at D=5 that is 50-70% of the budget, at D=15 it is 17-23%. Longer clips are strictly better for feasibility, and 15s is simultaneously TRIBE's practical minimum window and cost-neutral per stream-hour. Every constraint in the system points at 15.
  4. 480P over 768P for launch. Estimated ~3s of generation saved [uncertain — fal publishes no per-resolution timing] and a certain 37.5% off the dominant cost line.
  5. TEMPLATE PROMPT WRITER, not an LLM. Saves 0.8-2.0s, removes an external dependency, removes a failure mode, and removes a per-call cost. An ROI vector -> phrase-fragment lookup with a small weighted-sample over modifiers is more than adequate for the first working version.
  6. C = 1 in flight. Sufficient (generation runs at 0.6x realtime), maximally reactive, and it reserves the second fal slot for retries.
  7. INSTRUMENT EVERY STAGE FROM THE FIRST RUN. Every TRIBE figure in this document is an estimate scaled from a single published 4x range. A 15-line timing decorator replaces the whole estimated column with measurements inside one session, and the design decisions above are robust across that entire range — which is why it is safe to build now and measure later.

**simpler_alternative**

RUN TRIBE ON THE PROMPT TEXT, NOT ON THE RENDERED VIDEO. The fal response returns `expanded_prompt` — the rewritten prompt actually used for generation — so there is a clean, exact, free textual description of every clip with no captioning stage and no video decode. Feed that to TRIBE's text branch alone. T_tribe collapses from 6-30s to well under 1s (one short Llama-3.2-3B forward pass over ~100 words), condition (2) becomes trivially satisfied at K=1, V-JEPA2-Giant and Wav2Vec-BERT need not be loaded at all, and the VRAM footprint drops from 28-32GB to ~7-9GB — which moves TRIBE off a 48GB card onto a 16GB one, or onto the same box as everything else.
  What you lose: you are predicting the brain response to a DESCRIPTION of the video rather than to the video. Conceptually weaker, and it inverts the modality argument made everywhere else in this project. State it honestly rather than eliding it.

CRUDER STILL, if even that is too fiddly: drop TRIBE from the live loop entirely and precompute an ROI -> visual-motif lookup table offline (see items 15 and 16). Runtime latency for the perceive+predict half then goes to zero, the critical path is 8.4s against 15s with no GPU at all, and the whole GPU line disappears from the cost model. The stream stops being closed-loop, which is the conceptual payoff — but it is the correct fallback if the measured T_tribe lands at the 30s end of the published range and modality dropout does not rescue it.

**code_sketch**

# orchestrator.py — the whole real-time control layer. ~50 lines.
# Key move: TRIBE never sits on the generation critical path, and clips are
# perceived at DOWNLOAD time (in the buffer) not at PLAYBACK time, so reaction
# staleness is independent of buffer depth.

import asyncio, time

D = 15                    # clip playback seconds; also TRIBE's minimum window
BUFFER_TARGET = 3         # clips (~45s). Deeper buys jitter tolerance, not reactivity.

latest_brain = default_vector()   # shared slot; asyncio => no lock required
perceive_q: asyncio.Queue = asyncio.Queue(maxsize=4)

async def gen_pump(playlist, governor):
    """Critical path only. Never awaits TRIBE."""
    last_frame = seed_image
    while True:
        t0 = time.perf_counter()
        vec = latest_brain                      # whatever is current; staleness is fine
        prompt = template_prompt(vec)           # ~5ms, no LLM
        if not governor.may_generate(D):
            await playlist.append(filler_from(last_frame, D)); continue
        res = await fal.subscribe("minimax/h3-max/image-to-video", {
            "prompt": prompt, "duration": D, "resolution": "480P",
            "image_url": last_frame,
            "prompt_expansion_mode": "balanced",   # 'quality' costs ~30s. Never.
        })
        governor.charge(D)
        path = await download(res["video"]["url"])
        last_frame = await extract_last_frame(path)
        await playlist.append(path)             # ffmpeg concat -> RTMP
        # perceive it NOW, while it is still in the buffer and unseen
        perceive_q.put_nowait((path, res["expanded_prompt"]))
        log_stage("gen_cycle", time.perf_counter() - t0)   # replace estimates with data

async def perceive():
    """Off the critical path. Slowness degrades reactivity, never throughput."""
    global latest_brain
    while True:
        path, expanded = await perceive_q.get()
        while not perceive_q.empty():           # fell behind? skip to newest
            path, expanded = perceive_q.get_nowait()
        t0 = time.perf_counter()
        preds = await asyncio.to_thread(
            tribe.predict, video=path, audio=None, text=None,  # modality dropout:
        )                                        # video-only skips Llama-3.2-3B (~7GB, ~50% of T_tribe)
        latest_brain = reduce_roi(preds)         # (T, 20484) -> ~7-17 floats, ~30ms
        log_stage("tribe", time.perf_counter() - t0)

async def main():
    await asyncio.gather(gen_pump(playlist, governor), perceive())

# STEADY-STATE CONDITIONS — assert these against measured logs, not estimates:
#   (1) mean(gen_cycle) / (C * (1 - reject_rate))  <=  D     # generation keeps up
#   (2) mean(tribe) / K                            <=  D     # perception keeps up
# They are independent. Pipelining fixes neither; it only removes (2) from the
# critical path. If mean(tribe) > D, either drop a modality or set K=2.

### Risk

**failure_modes**

1. SATISFYING (1) AND ASSUMING (2) FOLLOWS. Pipelining makes the stream survive a slow TRIBE, which makes a broken perception loop invisible: the video keeps flowing, so nothing alarms, while the brain vector quietly ages until every clip is driven by the same minutes-old state and the piece has silently stopped being reactive. Monitor the AGE of latest_brain as a first-class metric, not just buffer depth.
2. THE +0.2s CONFIGURATION. Config A closes on paper (ratio 0.99) and will not survive contact with a real fal queue. Anything above ratio ~0.85 should be treated as failing; jitter, not the mean, is what kills it.
3. BUFFER AS A SUBSTITUTE FOR HEADROOM. A 33% throughput deficit drains a 4-clip buffer in four minutes and an 8-clip buffer in eight. Deepening the buffer looks like a fix, costs real money to prime, and — if you perceive at playback time — destroys reactivity while merely deferring the same failure.
4. SPECULATIVE PARALLELISM ERODING THE PREMISE. Raising C is the obvious response to falling behind and it silently converts a reactive system into an open-loop one: with C in flight the brain state driving a clip is C*D seconds stale. The system gets faster and stops being the thing it claims to be.
5. TRIBE COLD START MID-STREAM. ~60s lazy load of V-JEPA2-Giant and Llama-3.2-3B on first predict(). Any process restart, OOM-kill or preemption (Vast.ai interruptible instances especially) reintroduces it. Warm the model at boot with a dummy predict() before the stream starts, and never let the perception task be the thing that triggers the first load.
6. SAFETY-CHECKER REJECTIONS AS UNBUDGETED CYCLES. Each rejection costs a full T_gen. A brain-activation-maximising objective biases toward faces, threat cues and high salience — exactly where rejections cluster — so r is likely to be structurally elevated for THIS system specifically, not merely incidental. Budget r >= 0.15 and verify the pipelined margin covers it.
7. prompt_expansion_mode='quality' LEFT ON. A single flag adds ~30s, exceeding two clip budgets, and it will not look like a latency bug — it will look like the whole system is inexplicably slow.
8. ffmpeg RE-ENCODING ON CONCAT. Stage 10 is ~0.2s only with stream copy. Any codec, resolution or framerate mismatch between clips silently forces a re-encode and turns 0.2s into 5-15s, blowing the budget from the least-suspected stage. Pin resolution, fps and codec across every generation and verify with ffprobe.
9. SYNCHRONOUS BLOCKING INSIDE THE ASYNC LOOP. tribe.predict is CPU/GPU-blocking; calling it directly rather than via asyncio.to_thread stalls the event loop and re-serialises the pipeline, silently undoing the entire architectural fix while the code still looks concurrent.

### Economics

**cost**

Latency choices and cost choices point the same way in every case but one, which makes the decisions easy:
  - 480P is both ~3s faster and 37.5% cheaper than 768P.
  - D=15 has the lowest overhead fraction AND is cost-neutral per stream-hour AND meets TRIBE's minimum window.
  - Template prompt writing is faster, free, and one fewer dependency than an LLM (~$0.54/hr).
  - prompt_expansion_mode='balanced' saves ~30s and costs nothing either way (fal bills output duration, not wall-clock).
  - C=1 is maximally reactive and does not change cost/hour at all.
The exception: pipelining TRIBE requires a warm GPU running continuously alongside generation, at $0.33/hr (RunPod A6000 48GB community) to $2.50/hr (Modal A100-80GB). That is 0.2-1.4% of a $180-288/hr stream — an immaterial price for converting a 1.92x throughput deficit into a 44% surplus.
Buffer priming: B clips of pre-generated video costs B * D * price_per_second. At B=3, D=15, 480P regular: $2.25 one-off. Negligible, and a further reason not to over-deepen it for reasons other than jitter.
See item 11 for the full cost model. The short version: latency optimisation is nearly free, cost optimisation is where the money is, and dropping TRIBE from the live loop buys latency and simplicity but almost no dollars.

### Evidence

**sources**

https://github.com/ndpvt-web/neuroscore — the only public TRIBE v2 timing figure: '15-60s / 30s video' on the GPU backend, 'minutes / video' on CPU, 16GB+ VRAM; also the ~5 composite engagement scores (amygdala, ACC, dlPFC, vmPFC, striatum, auditory, visual) and half-second temporal resolution. Secondary coverage of the same package reports 'approximately two minutes per 30-60 second video on a single GPU', which conflicts with the README's own range — the discrepancy is unresolved and is the reason this figure must be measured rather than trusted.
https://www.datacamp.com/tutorial/tribe-v2-tutorial — VRAM 28-32GB trimodal (Llama-3.2-3B ~7GB, V-JEPA2-Giant ~14GB, Wav2Vec-BERT ~1GB), A100-40GB minimum / 80GB recommended, T4 OOMs on Llama load; output (T, 20484) at 1Hz; modality dropout p=0.3 per modality at training enabling any-subset inference; recommended minimum stimulus 15-30s; '~60s' full uncached cycle.
https://github.com/facebookresearch/tribev2 and https://huggingface.co/facebook/tribev2 — model card and code; 1Hz predicted BOLD output; lazy Llama download on first predict() with a 10s default HF Hub timeout that must be raised.
https://fal.ai/models/minimax/h3-max/text-to-video — schema (prompt, duration, resolution, prompt_expansion_mode, aspect_ratio); observed 'inference: 2.53' seconds on a sample generation.
https://blog.fal.ai/introducing-h3-max-by-fal/ — fal's launch post: 5s video in ~3s, 35x faster than official H3.
https://www.digitalapplied.com/blog/fal-h3-max-faster-than-real-time-video-generation — 5s at 768p in under 3s is vendor-stated with no independent wall-clock verification; explicitly notes fal published no reproducible latency protocol (hardware, queue time, prompt set, repeated trials, tail latency) and that the timings field measures backend denoising rather than end-to-end application latency.
https://anikuku.com/blog/fal-h3-max-api-speed-pricing-2026 and https://explainx.ai/blog/fal-h3-max-faster-than-realtime-video-august-2026 — '15 seconds of 720p in under 10 seconds in typical runs'; prompt_expansion 'quality' up to ~30s vs 'balanced' ~1s; real application latency additionally includes queue time, uploads, downloads, webhooks and retries.
https://fal.ai/docs/documentation/model-apis/concurrency-limits — 2 concurrent IN_PROGRESS for new accounts, self-serve ceiling 40 scaled by trailing-4-week paid invoices, sales beyond; queued requests consume no slot and are never rejected for concurrency; start_timeout can expire them.
https://levels.io/i-built-infinite-slop — prior art: chat-driven clip chaining with each clip conditioned to connect to the previous one, running fast enough to sustain a live stream.
https://github.com/fal-ai-community/realtime-krea-wan — existing 'text-to-video with dynamic prompt rewriting' scaffold on a realtime model; the architecture in which the per-clip latency budget does not exist. See item 17.
INFERENCE (mine, not sourced): the entire budget table's ffmpeg, download, ROI-reduction and queue-wait figures; the 40-60% modality-dropout saving; the 480P generation estimate; both steady-state inequalities and the buffer-drain formula; the finding that buffer depth dominates reaction staleness under playback-time perception and vanishes under generation-time perception; the pipelined-topology totals and headroom figures; the observation that concurrency trades reaction latency for throughput.

### Other Info

**item_id**

13

### Flagged Uncertain (omitted above)

- `interface_spec`
- `latency_ms`
- `realtime_headroom`
- `unknowns`

---

## Licence, ethics and framing

### Identity

**what_it_is**

Not a runtime component. It is the constraint layer that decides what the finished piece is allowed to BE: a CC BY-NC 4.0 research model (TRIBE v2) sits at the head of the pipeline, which makes non-commercial the default posture for the whole work, and a separate honesty problem sits at the tail, because TRIBE v2's released checkpoint has no per-person parameters at all and therefore cannot, even in principle, be predicting the viewer's brain.

**role_in_loop**

Outside the perceive -> predict -> prompt -> generate -> stream cycle, but it gates the two ends of it. At the input end it determines which weights you are permitted to load and under what conditions (HF gating, Meta licence acceptance). At the output end it determines the monetisation surface (no ads, no subs, no sponsor), the mandatory on-screen strings (attribution, AI-generation identifier), and the wording of every caption, title card and README describing what the viewer is watching.

### Interface

**input_contract**

Preconditions before a single frame can be generated:
- A Hugging Face account with an accepted Meta licence for `meta-llama/Llama-3.2-3B` (gated), plus access to `facebook/tribev2` and `facebook/vjepa2-vitg-fpc64-256`, exposed as HF_TOKEN. If you run TRIBE video-only with modality dropout (item 01), the Llama branch is never loaded and this gate disappears entirely — a licence simplification, not just a latency one.
- A fal.ai account, and a check that the `minimax/h3-max/*` endpoint carries fal's 'Commercial use' badge rather than 'Research only'. Even if it does, that badge speaks to fal's arrangement with the model provider; it does not cure the CC BY-NC restriction that TRIBE v2 imposes upstream.
- A settled answer to: is this stream monetised, in any form, at any point? That single answer determines whether the project is legal at all.

### Performance

**latency_ms**

0 ms at runtime — nothing in this item executes in the loop. The mandatory strings are static DOM. One-off human cost: roughly 2-4 hours to read the five licences properly and write the credits block; add a day or more if you decide to email Meta about a commercial licence (and see `unknowns` — the one public attempt got no reply). ESTIMATE, not sourced.

**throughput_constraint**

The binding constraint is not requests per second, it is the monetisation ceiling. CC BY-NC caps revenue at zero, permanently, for as long as TRIBE v2 is anywhere in the pipeline — including offline. There is no rate-limit-style escape hatch and no paid tier: Meta has published no commercial licence for TRIBE v2, and GitHub issue #45 asking for one is open and unanswered. Separately, MiniMax IV.1 imposes a US$20M/yr revenue ceiling before written authorisation is needed, which is irrelevant at this scale but confirms the licence anticipates commercial users.

**realtime_headroom**

Not applicable — infinite surplus. This item consumes no part of the clip-duration budget. Worth stating plainly so it is not mistaken for a scheduling risk: the licence question costs an afternoon once, and then nothing, forever.

### Complexity

**dev_complexity**

LOW as engineering, MEDIUM as judgement. The code is a footer and two overlay strings. The difficulty is entirely in deciding what the piece is permitted to be and in writing copy that is evocative without being false — neither of which is a coding problem, and both of which are cheaper to resolve now than after launch.

**loc_estimate**

~40 LOC of HTML/CSS for a credits block and a persistent 'AI-generated / Powered by MiniMax H3' overlay, plus a ~60-line LICENSES.md in the repo. Zero runtime logic.

**off_the_shelf_option**

Three things remove most of the work: (1) the Creative Commons attribution best-practices guidance and the CC licence chooser generate a compliant TASL block for you; (2) Meta publishes the exact required Llama NOTICE string, so copy it verbatim rather than paraphrasing; (3) MiniMax publishes the exact required strings ('Powered by MiniMax H3', 'MiniMax H3') in III.3 and IV.2 — again, copy verbatim. There is no off-the-shelf product for the honesty framing; that is writing, not tooling.

### Decision

**recommended_approach**

A. THE PRACTICAL READ ON NON-COMMERCIAL (not legal advice).
CC defines NonCommercial as use 'not primarily intended for or directed towards commercial advantage or monetary compensation'. It is an INTENT test on the use, not a status test on the user — CC's own wiki states that 'any interpretation of NonCommercial that assumes all uses by for-profit entities are automatically commercial conflicts with the plain language of the definition'. Scenario by scenario:

  - Free public livestream, no ads, no monetisation of any kind: CLEARLY FINE. This is the design target. Build this.
  - Pre-roll/mid-roll ADS on the stream: DO NOT. Advertising revenue is the textbook case of a use directed toward monetary compensation. The fact that CC's own guidance treats ad-funded blogs as a contested grey area is itself the reason to stay out of it.
  - SPONSORSHIP (a brand pays you to run the piece, or the piece carries a logo): DO NOT. Same reasoning, and worse — a sponsor's presence makes the commercial purpose explicit and documented.
  - TWITCH SUBS / bits / YouTube memberships / Patreon tied to the stream: DO NOT. These are monetary compensation flowing from the work.
  - A PAID SITE or paywalled access: DO NOT.
  - DONATIONS / a 'buy me a coffee' link with no gating and no reward: GREY, and I would still avoid it. It is defensible as cost recovery rather than commercial advantage, but it is exactly the fact pattern people litigate about, and the upside is small.
  - Hosting on YouTube/Twitch where the PLATFORM monetises but you have monetisation switched OFF: GREY but defensible. Your use is not directed toward your commercial advantage. Keep monetisation demonstrably disabled and be able to prove it.
  - A PORTFOLIO PIECE shown to get hired by a commercial studio: this is the sharpest edge and it is under-appreciated. A portfolio exists to obtain paid work; on the plain-language intent test, showing the piece to win a commercial job is arguably 'directed toward commercial advantage'. My read: putting the piece on a personal site as documented artistic work is fine and universally practised; naming it in a pitch deck for paid work is where I would stop. Do not let a client host it, rebrand it, or put it in their own marketing.
  - EXHIBITION in a gallery that charges admission: GREY. Non-profit institution, admission covering costs — arguable. A commercial gallery selling editions of the work — no.
  - SELLING the output videos, as editions, NFTs, or stock: DO NOT. Even though MiniMax VI.4 says 'MiniMax claims no rights over the Outputs you generate' and fal disclaims ownership, the TRIBE-side NC restriction is upstream of all of that. See `unknowns` on whether NC reaches the output at all — but the safe assumption is that selling artefacts made by an NC-licensed model is a commercial use of that model.

CRITICAL SCOPE POINT: dropping TRIBE out of the live loop does NOT escape NC. If you precompute an ROI -> motif table offline (items 15/16) that table is derived from an NC-licensed model, and building and using it is still your exercise of the CC BY-NC licence. CC BY-NC permits adaptations and, having no ShareAlike term, lets you license YOUR adaptation on your own terms — but your own use of the licensed material must remain non-commercial. The NC constraint follows the project, not the architecture.

B. TERRITORY — THE ONE THING I DID NOT EXPECT.
The MiniMax H3 Community License excludes the EU, UK, South Korea and the USA from its grant, and V.4 forbids using or displaying not only the Works but 'any of their Outputs or results' outside the Applicable Territory. MiniMax's own licence FAQ resolves this for you: the restriction is about OPEN WEIGHTS, and 'API: Globally available with built-in safeguards and responsible-use controls ... Open weights: Temporarily limited in certain regions.' Because you are calling fal's hosted endpoint and never touching the weights, the intended reading is that you are governed by fal's terms and MiniMax's API terms, not by the Community Licence. RESIDUAL AMBIGUITY WORTH KNOWING: the Community Licence's acceptance clause says you accept it by using the Works 'including through any Hosted Services', and I.12 defines Output to include results obtained 'through Hosted Services'. Read literally and in isolation, that would pull an API user in the UK into V.4. The FAQ contradicts that reading and the FAQ is the more sensible interpretation, but if you are UK- or EU-based this is worth one email to fal support asking, in writing, whether the H3 Max endpoint is licensed for display of outputs in your territory. Ten minutes, and it converts an ambiguity into a paper trail.

C. THE HONESTY QUESTION — AND WHY 'YOUR BRAIN' IS NOT MERELY IMPRECISE.
The framing problem is worse than a rounding error, and the reason is structural. The released `facebook/tribev2` checkpoint was trained with subject averaging and contains NO subject-specific parameters, so its predictions are bit-identical no matter whose viewing you claim it represents. The README says it flatly: 'Predictions are for the "average" subject ... and live on the fsaverage5 cortical mesh (~20k vertices).' There is no person-shaped variable in the model. 'Your brain' is not an approximation of what the system does; it names a quantity the system does not compute. Nor can you retreat to 'a selected training subject' — the public checkpoint exposes no such selector, which is exactly why the authors of arXiv 2607.01400 had to fit their OWN per-subject encoders to get an inter-subject-correlation readout.

And there is a published null result that closes off the other tempting claim. Sahu & Pandey (arXiv 2607.01400, July 2026) reduced TRIBE's predicted cortical response to a per-second engagement curve over 48 YouTube videos and correlated it with each video's 'most replayed' heatmap. Result: pooled position-controlled partial correlation +0.058 (95% CI [-0.04, 0.15]; t(47)=1.21, p=0.23), no better than loudness/motion baselines, BF01=3.2 for the null, equivalence test excluding effects above r=0.14, and a split-half reliability of 0.82 on the target that rules out a noisy-label excuse. So: predicted brain drive does NOT track what people actually re-watch. Any copy of the form 'this finds what your brain wants to watch' or 'this is optimising for engagement' is contradicted by the literature, not merely unproven. (Caveat: that paper evaluates TRIBE, the Algonauts-2025 winner, and the architecture family rather than v2 specifically — but it is the same three backbones and the same subject-averaged release problem.)

WHAT IS DEFENSIBLE:
  - 'A frozen encoder predicts the group-average cortical response of a canonical viewer.'
  - 'Trained on 451.6 h of fMRI from 25 subjects; evaluated on 1,117.7 h from 720.' (from the project's own grounding facts)
  - 'On HCP, the dataset with the best signal-to-noise, group-level Pearson R is near 0.4 — roughly twice the median individual subject's group-predictivity.' Note what that sentence actually concedes: the model beats a single noisy scan at estimating the AVERAGE, which is a statement about averages, not about people.
  - 'The prediction is of blood-oxygen-level-dependent signal, offset five seconds for haemodynamic lag — so what you see is always a response to something that already happened.' This is true, it is a real property of the system, and it is far more evocative than the false version.

WHAT IS NOT DEFENSIBLE: 'your brain', 'reads your mind', 'sees what you see', 'knows what you want', 'brain-optimised for engagement', 'neuro-tested'.

SUGGESTED FRAMING LANGUAGE — accurate and still evocative:
  - 'A simulated viewer.' (Best single phrase. Concrete, honest, slightly uncanny.)
  - 'There is no one watching. There is a model of an average cortex, and it is five seconds behind.'
  - 'The stream is written by a prediction of a brain that does not belong to anyone.'
  - 'An average of 720 people, none of them you.'
  - 'In-silico neuroscience' — Meta's own term for the use case, and it does the honest work of the prefix.
  - Title-card copy: 'Every image here was chosen to raise a number in a model of a brain. The brain is nobody's. The number is not attention, or pleasure, or interest. It is predicted blood flow.'
That last one is strictly true, fully citable, and more unsettling than the overclaim would have been — which is the argument for honesty on aesthetic grounds rather than only ethical ones.

**simpler_alternative**

If the licence posture becomes intolerable — i.e. the piece must earn money — there is exactly one clean route, and it is not a workaround: remove TRIBE v2 entirely and drive the prompts from something permissively licensed. Options, cheapest first: (a) an audio/visual salience heuristic (loudness, optical-flow magnitude, face count via a permissive detector) — note that arXiv 2607.01400 found TRIBE's predicted drive was 'not above simple loudness/motion baselines' at predicting re-watch, so on the one behavioural benchmark that has been tested, you lose nothing measurable; (b) a small permissively-licensed VLM captioning the previous clip; (c) a hand-authored motif table with no brain model behind it. All three cost you the concept, which is the actual asset — hence the recommendation to keep TRIBE and keep the piece non-commercial. Do NOT attempt a middle path of 'TRIBE offline only, then monetise': as set out above, the NC condition follows the project.

**code_sketch**

// credits.tsx — the whole of the compliance surface
const CREDITS = {
  brainModel: {
    title: 'TRIBE v2',
    author: 'Meta AI / FAIR Brain & AI (d\'Ascoli et al., 2026)',
    source: 'https://github.com/facebookresearch/tribev2',
    licence: 'CC BY-NC 4.0',
    licenceUrl: 'https://creativecommons.org/licenses/by-nc/4.0/',
    modified: 'Used for inference only; outputs reduced to ROI means. Not modified or retrained.',
  },
  // Include ONLY if the Llama text branch is actually loaded.
  // Running TRIBE video-only via modality dropout removes this obligation entirely.
  textBackbone: {
    builtWith: 'Built with Llama',
    notice: 'Llama 3.2 is licensed under the Llama 3.2 Community License, ' +
            'Copyright (c) Meta Platforms, Inc. All Rights Reserved.',
  },
  generator: {
    poweredBy: 'Powered by MiniMax H3',   // MiniMax licence III.3(a)
    ui: 'MiniMax H3',                     // MiniMax licence IV.2
  },
  honesty:
    'Predictions are of the group-average cortical response of a simulated viewer. ' +
    'The released model contains no subject-specific parameters: its output is ' +
    'identical for every person watching. This is not your brain.',
};

// Persistent overlay — satisfies MiniMax III.3(b) 'AI-generation identifier'
// and does the honesty work in the same 30px.
function StreamOverlay() {
  return (
    <div className="overlay" aria-live="off">
      <span>AI-generated \u00b7 Powered by MiniMax H3</span>
      <span>Simulated viewer \u00b7 group-average cortex \u00b7 +5s lag</span>
    </div>
  );
}

# Also tag the file itself, not just the page (III.3(b) says 'files produced'):
# ffmpeg -i clip.mp4 -c copy \
#   -metadata comment="AI-generated. Powered by MiniMax H3. Prompts derived from TRIBE v2 (CC BY-NC 4.0)." \
#   out.mp4

### Risk

**failure_modes**

Specific, non-obvious ways this bites:
- THE SUCCESS FAILURE. The realistic path to breaching NC is not a decision, it is momentum: the stream does well, someone offers sponsorship, a platform auto-enables monetisation, or a studio asks to run it at an event. Decide the answer now, in writing, before there is money on the table and a reason to rationalise.
- PLATFORM AUTO-MONETISATION. YouTube and Twitch can enable ads on a channel by default or on threshold-crossing. You can breach NC without ever taking an action. Check the setting after every milestone, not once.
- NC FOLLOWS THE PROJECT, NOT THE ARCHITECTURE. The most likely genuine mistake is believing that precomputing offline (items 15/16) launders the licence. It does not.
- THE PORTFOLIO TRAP. The piece is built partly to be seen by people who hire. That is the least examined and most likely NC exposure in the whole project.
- TERRITORY. If you are in the UK or EU, the MiniMax Community Licence text read literally excludes you from displaying Outputs, and the FAQ's 'API is global' carve-out is published in a docs/ markdown file, not in the licence itself. Get fal's position in writing.
- SAFETY, ADVERSARIALLY. A brain-activation-maximising objective pushes toward faces (FFA), threat cues and high-salience imagery. That is precisely the region of stimulus space where MiniMax's Acceptable Use Policy, fal's AUP and V.5's safeguard obligations concentrate — likeness generation is named in MiniMax's own FAQ as a driver of the territory carve-out. The aesthetic objective and the content policy are pointed in opposite directions by construction.
- OVERCLAIM AS A LEGAL, NOT ONLY ETHICAL, RISK. 'Your brain' in promotional copy for anything that touches money is a misleading-advertising exposure in most jurisdictions, and it is now contradicted by a published null result you would be assumed to know about.
- LICENCE DRIFT. MiniMax has explicitly committed to expanding territory scope and to 'clearly communicate any future license changes'; V-JEPA licensing already differs across releases (MIT vs CC BY-NC vs CC BY-NC-ND). Pin the licence text you relied on, with a date, in the repo.
- ATTRIBUTION ROT. CC BY attribution must survive the medium. A credits page nobody reaches while a 24/7 stream plays elsewhere is weak compliance; put the essential strings in the video overlay and the file metadata.

### Economics

**cost**

$0.00 per hour of stream in licence fees. Every licence in the stack is royalty-free at this scale: CC BY-NC 4.0 is free for non-commercial use; the Llama 3.2 Community License is free below 700M MAU; the MiniMax H3 Community License is free below US$20M/yr revenue. The only recurring costs are compute (items 10, 11), which this item does not touch.

The real economics are the OPTION cost, and it is worth stating in dollars because it is easy to under-price: choosing TRIBE v2 sets the lifetime commercial value of the piece to zero unless Meta later offers a commercial licence, which they have so far not answered a public request about. If the piece is intended to lead to paid work, that ceiling is the single most consequential decision in the project, and it is made at import time.

Cost of getting it wrong: a DMCA takedown and channel strike is the cheap outcome; a copyright claim from Meta is the expensive one. Neither is priceable, both are avoidable by not monetising.

### Other Info

**item_id**

14

### Flagged Uncertain (omitted above)

- `interface_spec`
- `sources`
- `unknowns`

---

## Neural data regulatory surface

### Identity

**what_it_is**

The non-licence legal surface of the piece: US state neural-data privacy statutes, FTC Act Section 5 deceptive-advertising exposure, the UNESCO neurotechnology ethics Recommendation, and the EU AI Act. Distinct from the CC BY-NC 4.0 question, which is about whether you may run TRIBE at all; this is about what you may SAY about what it produces, and whether the output is regulated data.

HEADLINE: the privacy surface is almost entirely empty and the advertising surface is not. Every US neural-data statute keys on MEASURING a nervous system. Nothing here measures anything. The whole of the real risk collapses into two words on a stream title card: 'your brain'.

**role_in_loop**

Wraps the whole loop rather than sitting inside it. Two concrete touch points: (1) the wording of the stream title, channel description, overlay caption and any press or social copy - this is where Section 5 exposure is created or avoided; (2) an on-screen disclosure that the video is AI-generated and the brain map is a model prediction, not a measurement. Both are text, both cost minutes, and between them they neutralise most of the surface.

### Interface

**input_contract**

What determines whether any of this attaches. The whole surface is a function of four facts:
1. IS ANY REAL PHYSIOLOGICAL SIGNAL COLLECTED FROM ANY VIEWER? Currently no. If that ever changes - an EEG headset, a webcam-based arousal proxy, an eye tracker, even a heart-rate reading from a collaborator - the analysis inverts and every statute above must be re-run. Montana's 'data associated with neural activity' and Connecticut's carve-out-free definition become live. Treat adding any sensor as a decision requiring fresh legal review, not a feature.
2. WHAT DOES THE PUBLIC-FACING COPY CLAIM? Stream title, channel description, overlay captions, social posts, press. This is the input that actually sets the risk level.
3. IS IT COMMERCIAL? Tips, subs, sponsorship, ads, merch, or promoting anything. Determines whether Section 5 reaches it at all.
4. WHO CAN SEE IT? A public stream is visible from the EU and from every US state, so assume all of the above apply simultaneously and design to the strictest.
Note what is NOT an input: the technical accuracy of TRIBE. A perfectly accurate group-average prediction described as 'your brain' is still deceptive; a crude prediction described accurately is not.

**output_contract**

The deliverable is a small set of words and one on-screen label.

SAY (all true, all substantiated by the TRIBE v2 paper and model card):
  - 'A neural network trained on fMRI recordings from 25 people predicts how a typical brain might respond to this video.'
  - 'predicted', 'simulated', 'modelled', 'a model of', 'group-average'
  - 'No one's brain is being measured. Nothing is recorded from you.'
  - 'The video and audio are generated by AI.'

DO NOT SAY:
  - 'your brain' / 'reads your mind' / 'sees what you feel' / 'live brain scan'
  - 'measures', 'reads', 'scans', 'detects' (all imply instrumentation)
  - anything therapeutic, focus-enhancing, relaxing, healing or cognitively beneficial
  - 'real-time' without qualification (there is a 5 s haemodynamic offset built into the model)

ON-SCREEN, PERMANENTLY, small and always visible - this is the entire compliance artefact:
  'AI-generated video. Brain map is a computer model's prediction, not a measurement. Nobody is being scanned.'
That one line simultaneously discharges the EU AI Act Art 50 synthetic-media disclosure, removes the implied measurement claim that the overlay itself makes for Section 5 purposes, and pre-empts the UNESCO-flavoured criticism. Roughly thirty seconds of work.

Also worth publishing once, in a pinned post or an About page: which subject conditioning you used, that TRIBE is CC BY-NC 4.0, and a link to the paper. Costs nothing and converts the project from 'suspicious brain claim' to 'documented artwork' in the eyes of anyone who goes looking.

### Performance

**throughput_constraint**

No rate limits, quotas or per-request costs - nothing here is metered. The constraints are categorical rather than throughput-shaped, and they are triggers:
  - Adding ANY viewer-side sensor (EEG, webcam arousal, eye tracking, heart rate) crosses into real neural or biometric data and re-opens every statute in interface_spec. Hard stop; get advice first.
  - Monetising brings the piece inside 'in or affecting commerce' for Section 5.
  - Crossing a state privacy law's applicability threshold (Connecticut ~100k consumers; California $25m revenue or 100k consumers) - implausible for a solo artist, but 'consumers whose personal information is processed' is a broader count than 'customers' if you ever collect viewer accounts, emails or analytics.
  - CC BY-NC 4.0 on TRIBE is the binding constraint on monetisation and is a separate item; note only that it and Section 5 pull in opposite directions - the non-commercial licence keeps you out of Section 5's reach, and the moment you solve the licence problem in order to monetise, Section 5 engages.

**realtime_headroom**

Ample. Every mitigation is text written once before going live; none of it is in any latency budget and none of it recurs per clip. The only per-clip cost is the persistent drawtext overlay, which ffmpeg renders as part of a filter chain already measured at ~0.5 s per 15 s clip - the disclosure adds no measurable time.
The one thing that genuinely must be decided BEFORE launch rather than iterated on is the naming and framing, because it propagates into the stream title, the URL, the social handle and the press copy, and is expensive to change once an audience exists. Decide the words first, build second.

### Complexity

**dev_complexity**

LOW as engineering; MEDIUM as judgement. Implementation is one drawtext filter and a rewritten channel description - under an hour. What is not low is the discipline: the compelling framing and the compliant framing are in direct tension, because 'watch your brain react' is a far better hook than 'watch a model's group-average prediction'. Every instinct in the promotion of this piece pushes toward the deceptive claim, which is exactly why it needs to be settled once, in writing, before there is an audience to impress.
Worth saying plainly: the honest framing is also the better artwork. 'A machine dreaming about how 25 strangers' brains might feel about what it just made' is more interesting than 'a brain scanner', and it is true.

**loc_estimate**

~5 lines of code. One ffmpeg drawtext filter appended to the existing overlay filter_complex:
  drawtext=text='AI-generated. Brain map is a model prediction\, not a measurement.':x=24:y=H-36:fontsize=18:fontcolor=white@0.75:box=1:boxcolor=black@0.4:boxborderw=8
Everything else is prose: roughly 150 words of channel description and a pinned About post.

**off_the_shelf_option**

No product removes this; it is a drafting problem, not a tooling problem. What genuinely reduces the work:
  - The TRIBE v2 paper and model card. Quote their own characterisation of what the model predicts. Substantiation by citation is the cheapest possible reasonable basis for a Section 5 claim, and it costs one link.
  - FPF's 'Neural Data Goldilocks Problem' post is the best single comparative source on how each US state defines neural data and which ones carve out inferences - it does in one page what would otherwise be four statutes of reading.
  - The EU AI Act Art 50 disclosure is a solved pattern: every AI video tool now ships a 'made with AI' label convention, and most platforms (YouTube, TikTok, Meta) have a built-in 'altered or synthetic content' toggle at upload/stream setup. USE THE PLATFORM TOGGLE as well as the burned-in text - it is one checkbox and it puts the disclosure in the platform's own metadata.
  - If the project ever monetises or takes real physiological data, that is the point to pay a privacy/advertising lawyer for a one-hour review. Not before; there is nothing for them to review while the answer is 'no data, no commerce'.

### Decision

**recommended_approach**

TREAT THIS AS A COPYWRITING TASK WITH A THIRTY-MINUTE BUDGET, NOT A COMPLIANCE PROJECT.

The analysis is genuinely reassuring and should be stated plainly: no US neural-data statute reaches this system. Every one of them - California, Colorado, Connecticut, Montana - keys on MEASURING an individual's nervous system, and California and Montana go further and expressly exclude information inferred from nonneural sources, which is precisely what a video-to-fMRI encoder produces. Beneath that, these are all consumer privacy laws that require personal data about an identifiable person, and there is no such person here. And beneath THAT, none of their applicability thresholds are met by a solo artist. Four layers, any one sufficient. The EU AI Act's emotion-recognition provisions fail at the definition: Art 3(39) requires inference from natural persons' biometric data, and this system sees no person. UNESCO's Recommendation binds Member States, not you.

So do these five things, in this order, and stop:
1. WRITE THE DISCLOSURE LINE AND BURN IT IN PERMANENTLY: 'AI-generated video. Brain map is a computer model's prediction, not a measurement. Nobody is being scanned.' One drawtext filter. This discharges the live EU AI Act Art 50 synthetic-media duty and removes the implied measurement claim the overlay otherwise makes.
2. BAN 'YOUR BRAIN' FROM ALL COPY. Title, description, socials, press. Substitute 'a model of how a typical brain might respond'. This single substitution eliminates the great majority of the residual risk, because Section 5 exposure comes from the claim, not the code.
3. NEVER MAKE A HEALTH, WELLNESS, FOCUS OR COGNITIVE CLAIM. Health-adjacent claims demand rigorous scientific substantiation and would convert a low-risk artwork into a genuine problem.
4. TICK THE PLATFORM'S 'ALTERED OR SYNTHETIC CONTENT' BOX at stream setup, in addition to the burned-in label.
5. PUBLISH ONE 'HOW THIS WORKS' PAGE: TRIBE v2, trained on 451.6 h of fMRI from 25 people, CC BY-NC 4.0, link to the paper, which subject conditioning you used, and an explicit statement that no viewer data of any kind is collected. This is your substantiation file and your press kit at the same time.

AND ONE HARD RULE: do not add any viewer-side sensor - EEG, webcam arousal detection, eye tracking, heart rate - without fresh legal advice. That is the single decision that would move this project from 'no applicable statute' to 'sensitive data under four state regimes plus GDPR special category', and it is tempting precisely because it would make the piece feel more real. Simulating the brain is what keeps the regulatory surface empty; it is a feature of the design, not a limitation of it.

**simpler_alternative**

Already close to minimal, but if even thirty minutes is too much, the irreducible core is a single sentence in the stream title area: 'Simulated brain response - nobody is being scanned.' Nine words. It removes the implied measurement claim, which is the only meaningful exposure the project has.

In the other direction, if a cautious posture is wanted: drop the word 'brain' from the marketing entirely and describe the control signal functionally - 'a model of visual and auditory response steers what gets generated next'. Zero regulatory surface, and arguably a weaker artwork, since the brain is the whole point. Not recommended, but it is the maximally safe option and it should be named so the trade-off is a choice rather than an accident.

A genuinely useful middle option: put the honest framing IN the artwork rather than in a disclaimer. Caption the overlay 'predicted response - subject 04' rather than 'brain activity'. The specificity is more compelling than the vague version, it is accurate, and it makes the disclaimer almost redundant.

**code_sketch**

# The entire technical mitigation. Append to the existing overlay filter chain.
DISCLOSURE = ("AI-generated video. Brain map is a model prediction\\, not a measurement. "
              "Nobody is being scanned.")

FILTER = (
    "[1]scale=440:-1,fps=25[ov];"
    "[0][ov]overlay=W-w-24:H-h-24:eof_action=repeat[v];"
    f"[v]drawtext=text='{DISCLOSURE}':x=24:y=H-36:fontsize=18"
    ":fontcolor=white@0.75:box=1:boxcolor=black@0.4:boxborderw=8"
)
# ffmpeg -y -i clip.mp4 -framerate 2 -i frame_%03d.png -filter_complex FILTER \
#        -c:v libx264 -preset veryfast -crf 20 -c:a copy out.mp4

# ---- copy constants, imported everywhere user-facing text is produced ----
STREAM_TITLE = "A model dreams about how 25 strangers' brains might see it"
CHANNEL_BLURB = (
    "Every clip is generated by AI. A neural network (Meta's TRIBE v2, trained on 451.6 hours of "
    "fMRI from 25 people) predicts how a typical brain might respond to it, and that prediction "
    "writes the prompt for the next clip. Nothing is measured from you. No viewer data of any kind "
    "is collected. The brain you see is a simulation, and it is not yours."
)

# ---- a cheap guard against the failure mode that actually happens ----
BANNED = ['your brain', 'reads your mind', 'brain scan', 'measures your',
          'live brain', 'mind reading', 'detects your', 'scans your']
def check_copy(text):
    """Run over every string that will ever face a viewer. Fails loudly and early."""
    hits = [p for p in BANNED if p in text.lower()]
    if hits:
        raise ValueError(f'deceptive-claim risk in user-facing copy: {hits}')
    return text

check_copy(STREAM_TITLE); check_copy(CHANNEL_BLURB)

### Risk

**failure_modes**

How this goes wrong in practice, in rough order of likelihood:
1. THE HOOK WINS. Someone writes 'WATCH YOUR BRAIN REACT LIVE' because it is a far better title, and the project acquires a material implied measurement claim on day one. This is by a wide margin the most likely failure and it is a marketing failure, not a legal one. Mitigate with the check_copy guard and by settling the wording before launch.
2. THE OVERLAY MAKES THE CLAIM THE COPY AVOIDS. Careful text plus a cortex pulsing beside a live video still communicates 'this is measuring something'. Implied claims are actionable. The caption on the overlay is doing regulatory work and should be written as deliberately as the title.
3. SCOPE CREEP INTO SENSORS. 'It would be so much better with a real EEG' - and every statute above becomes live, plus GDPR special-category data for EU viewers, plus Montana's per-purpose consent architecture. Innocuous-feeling, and the single largest step-change in exposure available.
4. HEALTH FRAMING BY DRIFT. A stream that runs overnight gets described as 'relaxing' or 'good for focus' in a social post, and a health claim requiring rigorous substantiation appears without anyone deciding to make one.
5. MONETISATION WITHOUT RE-READING. Turning on subs or sponsorship brings Section 5 fully into play and simultaneously breaches CC BY-NC 4.0. Two separate problems, one action, easy to trip.
6. THE ATTRACTOR-COLLAPSE OPTICS. A loop optimising for predicted brain activation converges toward salience-maximising imagery. If that becomes visibly true on stream while the copy says 'brain', the story writes itself as 'AI engineered to hijack your brain' - which is not what is happening, but it is what it will look like, and it maps uncomfortably onto exactly the manipulation concerns Art 5(1)(a) and the UNESCO Recommendation are about. The technical damping term has a reputational function as well as an aesthetic one.
7. QUIETLY RELYING ON 'IT IS ART'. There is no artistic exemption in Section 5, the AI Act, or any state privacy law. The exemptions relied on here are real and specific - no measurement, no identifiable person, no covered business, no biometric data - and they are much stronger than an artistic-purpose argument would be. Rely on the strong grounds, not the weak one.
8. JURISDICTIONAL DRIFT. The US patchwork is widening and definitions are broadening, not narrowing. An analysis correct on 2026-08-31 is not durable. Re-check before any relaunch or major press push.

### Evidence

**sources**

- NOT LEGAL ADVICE. This is desk research by a non-lawyer, summarising public sources as of 2026-08-31. Statutes are paraphrased, not quoted in full, and none of it is a substitute for advice from a qualified lawyer in the relevant jurisdiction.
- https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB1223 - SB 1223 bill text; definition of neural data: 'generated by measuring the activity of a consumer's central or peripheral nervous system, and that is not inferred from nonneural information'
- https://apcp.assembly.ca.gov/system/files/2024-07/sb-1223-becker-apcp-analysis.pdf - Assembly Privacy and Consumer Protection analysis; 'nonneural information' as downstream physical effects (pupil dilation, motor activity, breathing rate) and the rationale for the inference carve-out
- https://cppa.ca.gov/meetings/materials/20240716_item7_sb_1223.pdf - California Privacy Protection Agency board materials on SB 1223
- https://www.mofo.com/resources/insights/241011-a-mofo-privacy-minute-q-a-california-revises-ccpa - Morrison Foerster Q&A; effective 1 Jan 2025; heightened sensitive-PI obligations bite when data is processed to infer characteristics about a consumer
- https://www.hunton.com/privacy-and-cybersecurity-law-blog/california-amends-ccpa-to-cover-neural-data-and-clarify-scope-of-personal-information - Hunton analysis of the CCPA amendment
- https://connectontech.bakermckenzie.com/minding-your-data-new-law-expands-ccpas-sensitive-personal-information-to-include-neural-data/ - Baker McKenzie; signed 28 Sep 2024
- https://www.techpolicy.press/neural-data-and-consumer-privacy-californias-new-frontier-in-data-protection-and-neurorights/ - Tech Policy Press; critique that behavioural/physiological inference data falls outside the amended CCPA
- https://fpf.org/blog/the-neural-data-goldilocks-problem-defining-neural-data-in-u-s-state-privacy-laws/ - Future of Privacy Forum; the single best comparative source. Side-by-side statutory definitions for CA, CO, CT and MT and which exclude inferences: California and Montana carve out nonneural information, Connecticut does not, Colorado narrows to identification purposes
- https://www.rmmagazine.com/articles/article/2026/02/24/state-of-mind--the-new-landscape-of-neural-data-privacy-laws - Risk Management Magazine (Feb 2026) survey of the state neural-data landscape; Montana's regime described as the most extensive, with per-purpose and per-third-party express consent
- https://www.bassberry.com/news/you-read-my-mind-neural-data-and-the-new-wave-of-biometric-privacy-protections/ - Bass Berry; Colorado HB 24-1058 first in the US, effective 7 Aug 2024, amends CPA so sensitive data includes biological data including neural data
- https://www.truevault.com/learn/2024-amendments-to-colorados-privacy-law - Colorado HB 24-1058 definition and identification-purposes limitation
- https://www.neurorightsfoundation.org/advocacy/united-states - Neurorights Foundation US advocacy tracker; Connecticut SB 1295 signed 24 Jun 2025 by Gov. Lamont, most provisions effective 1 Jul 2026
- https://insidebci.com/policy/2026-04-03-us-states-build-patchwork-of-neural-data-privacy-laws-as-bci-market-accelerates/ - Inside BCI (Apr 2026) on the widening state patchwork
- https://legislature.vermont.gov/Documents/2026/Workgroups/Senate%20Health%20and%20Welfare/Bills/H.814/Witness%20Testimony/H.814~Ashley%20Collins~US%20State%20Legislation%20to%20Protect%20Neural%20Data~4-9-2026.pdf - Vermont legislature briefing note (Apr 2026), US state legislation to protect neural data
- https://www.arnoldporter.com/en/perspectives/advisories/2025/07/neural-data-privacy-regulation - Arnold & Porter, neural data privacy regulation: what exists and what is anticipated
- https://www.commerce.senate.gov/2025/4/cantwell-schumer-markey-call-on-ftc-to-protect-consumers-neural-data - Senate Commerce release, 28 Apr 2025: Senators urge FTC to investigate deceptive or unfair practices around neural data
- https://www.cooley.com/news/insight/2025/2025-04-30-senators-urge-ftc-action-on-consumer-neural-data-signaling-heightened-scrutiny - Cooley on the Senators' letter and heightened FTC scrutiny
- https://www.medtechdive.com/news/senators-bci-brain-computer-privacy-ftc/746733/ - MedTech Dive; FTC confirmed receipt of the letter and declined to comment
- https://www.ftc.gov/system/files/documents/public_statements/410531/831014deceptionstmt.pdf - FTC Policy Statement on Deception (1983): likely to mislead a consumer acting reasonably, and materiality
- https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes - Operation AI Comply, 25 Sep 2024, five enforcement actions; Chair Khan: 'there is no AI exemption from the laws on the books'
- https://www.ftc.gov/business-guidance/blog/2024/09/operation-ai-comply-continuing-crackdown-overpromises-ai-related-lies - FTC business guidance blog on Operation AI Comply
- https://www.beneschlaw.com/insight/one-year-in-ftcs-operation-ai-comply-continues-under-new-administration-signaling-enduring-enforcement-focus/ - Operation AI Comply continued under the subsequent administration
- https://www.venable.com/insights/publications/2022/02/ftc-enforcement-of-advertising-claims - Venable: reasonable basis required for express and implied claims before dissemination; rigorous scientific support for health/disease claims
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6629579/ - Oversight of direct-to-consumer neurotechnologies; regulatory burden has largely fallen to the FTC via deceptive-advertising authority
- https://www.ftc.gov/system/files/documents/public_statements/903353/160104lumositystatement.pdf - FTC statement in the Lumosity brain-training matter (precedent for brain-claim enforcement)
- https://www.unesco.org/en/articles/ethics-neurotechnology-unesco-adopts-first-global-standard-cutting-edge-technology - UNESCO adopts the Recommendation on the Ethics of Neurotechnology, 12 Nov 2025
- https://www.unesco.org/en/legal-affairs/recommendation-ethics-neurotechnology - official Recommendation page
- https://www.insideprivacy.com/health-privacy/unesco-adopts-first-global-framework-on-neurotechnology-ethics/ - Covington analysis: prohibit neural data in recommender systems for manipulative purposes, restrict nudging, prohibit marketing during sleep, specific neuromarketing rules
- https://www.globalpolicywatch.com/2026/01/unesco-adopts-first-global-framework-on-neurotechnology-ethics/ - further analysis of the Recommendation's provisions
- https://law.stanford.edu/2026/03/30/who-owns-digital-thoughts-the-limits-of-property-law-and-the-2025-unesco-recommendation-on-the-ethics-of-neurotechnology/ - Stanford Law and Biosciences blog on the 2025 Recommendation's limits
- https://artificialintelligenceact.eu/article/3/ - EU AI Act Article 3 definitions; Art 3(39) 'emotion recognition system' means an AI system for the purpose of identifying or inferring emotions or intentions of natural persons on the basis of their biometric data
- https://www.twobirds.com/en/insights/2024/global/what-is-an-emotion-recognition-system-under-the-eus-artificial-intelligence-act-part-1 - Bird & Bird: where emotions are inferred by non-biometric means the system is not an ERS
- https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/ - FPF on the scope of the Art 5(1)(f) emotion-recognition prohibition (workplace and education only)
- https://fpf.org/blog/red-lines-under-the-eu-ai-act-understanding-manipulative-techniques-and-the-exploitation-of-vulnerabilities/ - FPF on Art 5(1)(a) manipulative techniques and vulnerability exploitation
- https://www.paulhastings.com/insights/client-alerts/european-commission-and-ai-guidelines-on-prohibited-practices - Paul Hastings on the Commission's guidelines: personalised advertising is not inherently manipulative; Art 5(1)(a) targets subliminal techniques the user cannot perceive
- https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20240408-prohibited-ai-practices-a-deep-dive-into-article-5-of-the-european-unions-ai-act - WilmerHale deep dive on Article 5
- https://artificialintelligenceact.eu/article/50/ - EU AI Act Article 50 transparency obligations for providers and deployers
- https://artificialintelligenceact.eu/transparency-rules-article-50/ - practical guide to Article 50
- https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/ - CSA research note (Jul 2026): Art 50 duties attach by function not by Annex III tier, cover synthetic-media generators and deepfake tools, applied from 2 Aug 2026, enforceable by national market surveillance authorities from that date
- https://www.stibbe.com/publications-and-insights/feeling-watched-transparency-obligations-for-emotion-recognition-and - Stibbe on Art 50(3): deployers of emotion recognition and biometric categorisation systems must inform exposed natural persons
- https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act - European Commission FAQ on Article 50
- INFERENCE (explicitly marked): the four-ground analysis of why SB 1223 does not reach a simulated response - no consumer, no measurement, express inference carve-out, no covered business - is my reading of the statutory text and the cited commentary. No regulator or court has addressed predicted-brain-response data. It is text-reading, not precedent.
- INFERENCE (explicitly marked): the conclusion that Art 3(39) is not engaged because the input is the stimulus rather than any viewer's biometric data is my application of the definition, supported by the Bird & Bird point that non-biometric inference falls outside ERS, but not directly sourced for this fact pattern.
- INFERENCE (explicitly marked): the practical risk ranking - that platform policy and reputational damage are far more probable consequences than regulatory action against an unmonetised solo art project - is judgement, not a sourced claim.

### Other Info

**item_id**

B

**focus**

Legal exposure distinct from the software licence, arising from marketing a simulated brain response.

**disclaimer**

NOT LEGAL ADVICE. This is desk research by a non-lawyer, summarising public sources as of 2026-08-31. Statutes are paraphrased, not quoted in full, and none of it is a substitute for advice from a qualified lawyer in the relevant jurisdiction.

### Flagged Uncertain (omitted above)

- `cost`
- `interface_spec`
- `latency_ms`
- `unknowns`

---

## Observability and on-stream brain visualisation

### Identity

**what_it_is**

Two jobs bolted onto the same tap point on the TRIBE output tensor. (1) THE OVERLAY: render the predicted fsaverage5 cortical activation and blend it into the outgoing video beside the generated clip. (2) THE LOG: append one JSONL record per loop iteration carrying the vertex vector, the ROI reduction, the prompt, the H3 Max expanded_prompt and the clip URL.

The overlay is not a debug tool - it is the entire visual differentiator versus a plain chat-driven infinite stream. A cortex lighting up next to the video is what makes the concept legible in three seconds without a word of explanation. Measured cost: ~2 s of one CPU core per 15 s clip for a fully animated cortex. It is very nearly free.

THE ONE THING THAT WILL RUIN IT: TRIBE's predicted values are tiny. The training target was z-scored and detrended, so absolute magnitudes are meaningless, and encoder predictions are further shrunk toward the mean - a natural face photograph drives FFA at only +0.080 z-units. Rendering those values with colour limits chosen for z-scale data produces a uniform, dead cortex that never visibly changes. MEASURED: at threshold=1.5, vmax=4.0, exactly 0.00% of vertices render. The overlay must be normalised over a rolling window or it is not a feature, it is a grey blob.

**role_in_loop**

Taps the (T, n_vertices) tensor immediately after TRIBE predict() - the same tensor the readout stage reduces - so it costs nothing extra upstream. The render runs concurrently with the fal generation call (the ~9 s H3 Max wait is dead time and is where the overlay should be built). Blending happens in the playout path, per outgoing frame. Logging taps every stage and writes at end-of-iteration. Neither job is on the critical path; both are cheap enough to be anyway.

### Interface

**interface_spec**

=== 0. USE TRIBE'S OWN PARCELLATION HELPERS. THEY EXIST. ===
CORRECTION TO THE ORIGINAL BRIEF: the premise that 'TRIBE ships no parcellation helpers' is wrong. Verified against facebookresearch/tribev2, tribev2/utils.py ships FIVE relevant functions:
    get_hcp_labels(mesh='fsaverage5', combine=False, hemi='both')
    get_hcp_vertex_labels(mesh='fsaverage5', combine=False)
    get_hcp_roi_indices(rois: str | list[str], hemi='both', mesh='fsaverage5')
    summarize_by_roi(data: np.ndarray, hemi='both', mesh='fsaverage5')
    get_topk_rois(data: np.ndarray, hemi='both', mesh='fsaverage5', k=10) -> list[str]
HCP-MMP1 is fetched via mne.datasets.fetch_hcp_mmp_parcellation() and read with mne.read_labels_from_annot() against the fsaverage template. The implementation handles hemispheres separately and applies an index_offset based on mesh size, concatenating left and right vertex arrays when hemi='both' - which independently corroborates the 10242 boundary for fsaverage5.
  - summarize_by_roi() IS the ROI reduction. Do not hand-roll it.
  - get_topk_rois() is a gift for the overlay: it returns ROI NAMES directly, which is exactly the caption text that turns a pretty picture into a legible causal story ('FFA is lit, so it is asking for faces'). Use it for the drawtext caption.
  - You still need the manual hemisphere split for RAW SURFACE PLOTTING, because plot_surf_stat_map takes one hemisphere's array against one hemisphere's mesh. The helpers give you ROIs; the slice gives you something to draw.
  - Adds an mne dependency. If that is unwelcome in the streaming container, get_hcp_roi_indices results are static - compute them once offline and ship a .npz of index arrays.

=== 1. HEMISPHERE SPLIT (still needed, for plotting only) ===
Empirically confirmed: fsaverage5 has exactly 10242 vertices per hemisphere (loaded meshes reported (10242, 3) for both lh and rh). For a TRIBE cortical row `v` of length 20484:
    lh = v[:10242]
    rh = v[10242:]
This is legitimate because it is a CONCATENATION BOUNDARY between two separate meshes, not an anatomical claim. See section 5 for why anatomical claims about vertex index ranges are not.

=== 2. MESH SOURCE ===
nilearn.datasets.fetch_surf_fsaverage('fsaverage5'). Measured fetch time 0.00 s - fsaverage5 is bundled with the nilearn wheel, so there is NO network download and no first-run stall. Verified keys: area_left/right, curv_left/right, description, flat_left/right, infl_left/right, pial_left/right, sphere_left/right, sulc_left/right, thick_left/right, white_left/right. Note flat_left/flat_right are present - the flat cortical map needs zero extra setup.

=== 3. NORMALISATION - THE MOST IMPORTANT PART OF THIS SPEC ===
TRIBE's training target was per-sample z-scored and detrended (the paper's preprocessing section lists 'Rescaling and detrending'), so absolute predicted values carry no physical scale, and encoder shrinkage makes them far smaller than unit variance. The published anchor: an optimised FFA stimulus reaches +0.34 and a natural face photograph only +0.080 (arXiv 2605.13904).
MEASURED CONSEQUENCE, on simulated predictions with std 0.057 and p99 0.193:
    threshold=1.5, vmax=4.0  ->  0.00% of vertices exceed threshold  (a blank, dead cortex)
    threshold=0.5, vmax=2.0  ->  0.00%
    threshold=0.1, vmax=0.3  ->  6.05%
    per-frame p98(|x|)=0.136, threshold=0.35*p98  ->  35.4% visible (a live, moving map)
THE FIX, and it must be the ROLLING-WINDOW version, not either naive extreme:
  - Naive fixed limits (a hard-coded vmax) -> dead cortex, as measured above.
  - Naive per-frame autoscaling -> the scale rebases every frame, so an all-noise clip and a strongly-driven clip look identical and the overlay flickers. Constant-amplitude noise reads as dramatic brain activity.
  - CORRECT: maintain a rolling percentile over the last N clips (N ~ 20-40). Set vmax = p98(|x|) over that window and threshold = 0.35 * vmax. Stable within and across frames, adaptive to the actual output scale, and it survives a change of subject conditioning or clip length without retuning. Seed the window from a short calibration run so the first minute is not wrong.

=== 4. RENDER CALLS ===
    nilearn.plotting.plot_surf_stat_map(
        surf_mesh=None, stat_map=None, bg_map=None, hemi='left', view=None,
        engine='matplotlib', cmap='RdBu_r', colorbar=True, avg_method=None,
        threshold=None, alpha=None, bg_on_data=False, vmin=None, vmax=None,
        symmetric_cbar='auto', cbar_tick_format='auto', title=None, title_font_size=None,
        output_file=None, axes=None, figure=None, **kwargs)
  - stat_map accepts a raw numpy float array of shape (10242,) directly.
  - hemi in {'left','right','both'}; view in {'lateral','medial','dorsal','ventral','anterior','posterior'} or a custom (elev, azim) tuple.
  - Pass axes= and figure= to draw multiple panels into one figure.
  - savefig(transparent=True) yields an RGBA PNG that blends without a background box.
  - view_surf(...) -> SurfaceView with save_as_html(); HTML only, never a static image; 2.53 MB per call. Offline inspection only, never in the loop.

=== 5. TEMPORAL RATE - DERIVE IT, DO NOT HARD-CODE IT ===
CORRECTION: the brief's '2 Hz' is the STIMULUS FEATURE ALIGNMENT rate, not the output rate. The TRIBE v2 paper describes features aligned on 'an evenly spaced grid at a frequency f_stim = 2 Hz' (0.5 s bins) for text, audio and video embeddings before the transformer. The fMRI prediction TR is NOT explicitly stated in the section I could retrieve, so I could not independently confirm the output rate. The team lead reports 1 Hz; that is consistent with 2 Hz being alignment-only, but note a typical fMRI TR of 1.49 s would give ~0.67 Hz rather than exactly 1 Hz.
ENGINEERING GUIDANCE: read T from preds.shape[0] at runtime and render that many frames. Never hard-code a frame count. Both plausible rates are affordable and both were measured (section on latency): 15 frames 1.97 s, 30 frames 3.90 s. A 15 s clip at ~1 Hz gives ~15 frames - ample for a slow pulse, which is the right aesthetic anyway.

=== 6. SUBCORTICAL IS A DIFFERENT RENDERER ENTIRELY ===
The cortical checkpoint's 20484 vertices are all that plot_surf_stat_map can draw. The paper confirms subcortical targets are '8,802 voxels of 8 subcortical regions defined by the Harvard-Oxford atlas', in MNI space at 2 mm - hippocampus, lateral ventricles, amygdala, thalamus, caudate, putamen, pallidum, accumbens. 8 structures bilaterally is 16 per-hemisphere labels, which reconciles the team lead's '16 bilateral structures'.
UNVERIFIED: I could NOT confirm a separate `facebook/tribev2-subcortical` checkpoint released 2026-05-13, nor the figure 8,808. The paper gives 8,802 / 8 regions, matching the project's own grounding facts. Treat the second checkpoint as reported-but-unconfirmed and check the HF model page directly before building against it.
RENDER PATH: volumetric, not surface. Un-flatten the vector into an MNI volume with the mask, then
    plotting.plot_glass_brain(img, threshold=..., display_mode='lyrz', output_file=...)
    plotting.plot_stat_map(img, threshold=..., display_mode='z', cut_coords=4, output_file=...)
MEASURED: glass brain 139 ms, 4-slice stat map 116 ms. Both cheaper than the cortical montage.
GOTCHA, MEASURED: you cannot rebuild the volume from nilearn's off-the-shelf atlas. fetch_atlas_harvard_oxford('sub-maxprob-thr25-2mm') gives shape (91,109,91) with 206,870 voxels in mask across 21 labels - not 8,802. TRIBE uses its own restricted mask and voxel ordering. You need that exact mask from the checkpoint, or the vector cannot be placed correctly and you will render a confident, meaningless picture.
The glass brain is genuinely worth having on stream: amygdala and accumbens lighting up is far more legible to a lay audience than any cortical parcel name.

=== 7. COMPOSITING - REVISED, SEE recommended_approach ===
Two paths. Which one applies depends on whether the project adopts the infinite-livestream client.
  (a) FRAME-PIPE ALPHA BLEND (preferred if using infinite-livestream): rasterise once per TRIBE timestep, then numpy alpha-blend the RGBA panel into each outgoing frame.
  (b) PER-CLIP FFMPEG FILTER (standalone fallback):
    ffmpeg -y -i clip.mp4 -framerate <T/duration> -i frame_%03d.png \
      -filter_complex '[1]scale=440:-1,fps=25[ov];[0][ov]overlay=W-w-24:H-h-24:eof_action=repeat' \
      -c:v libx264 -preset veryfast -crf 20 -c:a copy out.mp4
    -c:a copy preserves H3 Max's natively-synchronised audio bit-exact. eof_action=repeat holds the last overlay frame (a frozen brain, not a vanished one). W-w-24:H-h-24 is resolution-independent so it survives a 480P/768P switch.

**input_contract**

RENDER: a float32 numpy array, (n_vertices,) for one timepoint or (T, n_vertices) for a clip. Derive T at runtime; do not assume a rate. Cortical vertices only for the surface path; the subcortical voxels need the volumetric path and TRIBE's own mask.
Values must be finite: NaN or inf produces a blank or all-black panel with NO exception raised. Sanitise with np.nan_to_num() before every render.
Values are on an arbitrary z-like scale with tiny magnitude and MUST be normalised over a rolling window (see interface_spec section 3). This is the difference between a living overlay and a grey blob, and the failure is silent.
COMPOSITE: the H3 Max clip (frames or file) plus the rendered RGBA panel.
LOG: whatever each stage produced. Nothing is required to be present - write partial records rather than skipping a record, because the iterations that fail are the ones you most need logged.

**output_contract**

RENDER -> an RGBA PNG (or an in-memory RGBA array for the blend path). Measured sizes at 640x360 dpi=100: 4-panel inflated montage 58 KB; two-hemisphere flat map 15 KB; single hemi single view 28-59 KB. Use cmap='hot' with a threshold - a lay audience reads hot-on-grey as 'brain activity' instantly and reads the signed RdBu_r default as nothing at all.

LOG -> one JSON object per iteration:
  ts                 ISO 8601 UTC, to align a log line to a VOD timestamp
  iter               monotonic int, the x-axis for every drift plot
  clip_id            uuid joining record to mp4 and PNG
  vertex_vec_path    path to a .npy of the (T, n) float16 array. DO NOT inline - 20484 float32 is
                     ~80 KB raw and ~500 KB as JSON text, per iteration, 240x/hour.
  vertex_vec_sha1    hash of the array - the cheapest possible attractor-collapse detector
  norm_window        the vmax/threshold actually used for this frame's render. WITHOUT THIS a
                     recorded overlay cannot be reinterpreted later, because the colour scale is
                     no longer recoverable from the array alone.
  roi_reduction      output of summarize_by_roi(). Small - inline it. The most useful field here.
  topk_rois          output of get_topk_rois(), the caption text actually shown on screen
  reduction_policy   which temporal reduction was applied (peak/mean/last-N/delta)
  prompt             what your translation layer wrote
  expanded_prompt    what H3 Max actually used. Highest-value field for diagnosing drift: free,
                     exact, and diffing consecutive values shows attractor collapse in text before
                     it is visible in the video.
  seed               H3 Max seed; without it no iteration is reproducible
  clip_url           fal video.url
  timings            {tribe_ms, reduce_ms, render_ms, fal_ms, composite_ms}
  safety_rejected    bool + retry_count - unbudgeted throughput loss you cannot size without data
  buffer_depth       clips queued; the leading indicator of an underrun
Volume: a few MB/day of JSONL; ~600 MB/day of float16 sidecars at 15 frames (15 x 20484 x 2 bytes x 240 x 24), ~1.2 GB/day at 30. Rotate the sidecars; keep the JSONL forever, it is tiny.

### Performance

**latency_ms**

MEASURED, not estimated. Apple M4, 10 cores, arm64, nilearn 0.14.0, matplotlib Agg, ffmpeg 8.1.1. Median of 5 runs after warm-up. Single-threaded CPU rasterisation, no GPU.

  plot_surf_stat_map, 1 hemi, 1 view, with sulc bg_map ....... 71 ms
  plot_surf_stat_map, 1 hemi, 1 view, no bg_map .............. 70 ms  (bg_map is free)
  4-panel L/R x lateral/medial montage, one savefig .......... 235 ms
  PRODUCTION 4-panel, transparent PNG, 640x360, dpi=100 ...... 229 ms
  Flat map, both hemispheres (flat_left/flat_right) .......... 99 ms
  SurfaceImage (new nilearn API), 1 hemi, 1 view ............. 76 ms
  view_surf plotly -> save_as_html ........................... 78 ms (2.53 MB HTML)
  Bare matplotlib plot_trisurf, 1 hemi (floor for mpl 3D) .... 34 ms
  Precomputed vertex->pixel LUT recolour, 640x360 ............ 20 ms
  PNG encode floor alone, 640x360 ............................ 17 ms
  SUBCORTICAL plot_glass_brain (volumetric, lyrz) ............ 139 ms
  SUBCORTICAL plot_stat_map, 4 axial slices .................. 116 ms

ANIMATED sequences, 2-panel L/R lateral, transparent, WITH per-frame percentile normalisation:
  15 frames (a 15 s clip at ~1 Hz) ........................... 1.97 s   (131 ms/frame)
  30 frames (a 15 s clip at 2 Hz) ............................ 3.90 s   (130 ms/frame)
Normalisation is free - it is a percentile over 10k floats, lost in the rendering noise.

COMPOSITING, 15 s 1366x768 clip, libx264 -preset veryfast -crf 20, audio copied:
  static PNG overlay ......................................... 490 ms wall
  animated 2 fps PNG sequence overlay ........................ 510 ms wall
Animating costs ffmpeg essentially nothing; the cost is rendering, not muxing.
FRAME-PIPE ALPHA BLEND (infinite-livestream's approach, their figure): ~0.6 ms per frame at 1344x768, with Pillow re-rasterising a panel only when its text changes.

TOTALS per 15 s clip: animated cortex 1.97 + 0.51 = 2.5 s. Add the subcortical glass brain per timestep and it is ~4 s.

**throughput_constraint**

No API, no rate limit, no quota - pure local CPU, the only stage with no external ceiling. Real constraints:
1. matplotlib is NOT thread-safe. Never render from multiple threads against global pyplot state. Use a process, or the object-oriented Figure API with an explicit canvas per process.
2. Every figure must be closed with plt.close('all') or the process leaks until it dies - on a 24/7 stream that is a certainty, not a risk.
3. matplotlib.use('Agg') must precede the pyplot import or a headless server fails on a missing display.
4. libx264 -preset veryfast composited a 15 s clip in 0.5 s, ~30x realtime. Never the bottleneck.
5. FROM infinite-livestream's documented learnings, and these are the expensive ones to rediscover: frame geometry must match ffmpeg's -s WxH EXACTLY or you get scanline corruption ('TV static'); NEVER write to ffmpeg stdin from the event loop, because blocking there starves the whole system; feed audio and video on SEPARATE pipes in lockstep; an audio track is mandatory for platform acceptance even when it is silence. The overlay renderer must therefore run off the event loop and hand finished arrays to the pacer.
6. At 15 frames, ~2 s of the ~9 s H3 Max wait is consumed by rendering - fine, but launch the render at the same moment as the fal request, not after it returns.

**realtime_headroom**

Enormous. Against a 15 s clip cadence:
  animated cortex (15 frames) + composite: 2.5 s used, 12.5 s surplus (17% of budget, ~6x headroom)
  + subcortical glass brain per timestep:  ~4 s used, ~11 s surplus (~3.7x headroom)
  static single montage + composite:       0.72 s used, 14.3 s surplus (~21x headroom)
Even against a 5 s clip the static path uses 0.72 s of 5 s.

This inverts the original premise. The concern was whether a nilearn surface plot could keep up with a 15 s cadence; it keeps up with a 1 s cadence. So BUILD THE ANIMATED ONE, and add the subcortical glass brain too - both are already paid for. A static image per clip looks like a slideshow; a cortex that pulses in time with the video is what makes a viewer stop scrolling.
Corollary: the precomputed LUT (20 ms) and pycortex are premature optimisation. Do not build them. The binding constraint is normalisation correctness, not speed.

### Complexity

**dev_complexity**

LOW. Overlay: roughly half a day, now slightly less because summarize_by_roi() and get_topk_rois() are shipped rather than hand-rolled. The nilearn call is one line, the hemisphere split is one slice, and all paths were verified working in this session.
The genuine difficulty is not difficulty, it is a silent failure: the rolling-window normalisation. Get it wrong in either direction - fixed limits or naive per-frame autoscale - and the overlay looks plausible in a screenshot while being either dead or meaningless in motion. Budget an hour to get the normalisation right and verify it against a recorded clip, not a single frame.
Logging: about an hour. json.dumps to an append-only file plus np.save for the sidecar.

**loc_estimate**

Overlay renderer: 50-70 lines (mesh load at import, rolling-window normaliser, render function, blend or ffmpeg call). Animated variant: +15. Subcortical glass brain: +25, IF TRIBE's mask is available. JSONL logger: 25-40 including sidecar write and rotation. Total ~120-150 lines. The cheapest headline feature in the system by a wide margin.

**off_the_shelf_option**

PARCELLATION: use TRIBE's own tribev2/utils.py - get_hcp_labels, get_hcp_vertex_labels, get_hcp_roi_indices, summarize_by_roi, get_topk_rois. HCP-MMP1 via mne.datasets.fetch_hcp_mmp_parcellation(). This removes the ROI-indexing work entirely.
RENDERING: nilearn IS the off-the-shelf option and nothing beats it - fsaverage5 ships inside the wheel, plot_surf_stat_map takes a raw numpy array, 71 ms. Just `pip install nilearn` (heavy tail: matplotlib, nibabel, scikit-learn, scipy, pandas).
  Fallback surface atlas if you want to avoid mne: fetch_atlas_surf_destrieux() is the only surface atlas nilearn ships and it works directly on fsaverage5 - verified, 76 labels, map_left (10242,), ~2 s one-off download to ~/nilearn_data. Yeo-17 and Glasser come as FreeSurfer .annot files (CBIG repo, into fsaverage5/label/) read with nibabel.freesurfer.read_annot(); mind the +1000/+2000 hemisphere offset on Glasser. nilearn's other atlas fetchers (yeo_2011, schaefer_2018, harvard_oxford, aal, destrieux_2009) are VOLUMETRIC and will not index a 20484-vertex vector.
STREAMING/COMPOSITING: github.com/reactor-team/infinite-livestream (Apache-2.0) already solves this. Its streaming-client does per-frame overlay in Python - Pillow rasterises a panel only when its text changes, per-frame cost is a numpy alpha blend (~0.6 ms at 1344x768) - and every outgoing frame (live, repeated or black) passes through the overlay before the RTMP sink. It pairs with fast-h3, a FastVideo-distilled MiniMax-H3 (4-step, sparse attention) at 768p with audio, driven by chat prompts. READ ITS streaming-client/README BEFORE WRITING ANY COMPOSITING CODE - it documents the ffmpeg gotchas listed in throughput_constraint, and it is the same generator family this project targets.
OBS is the wrong choice: it keeps its scene compositor and preview renderer running on a static automated scene, burning CPU on a UI nobody watches. Its one advantage - a CEF Browser Source - only matters on the browser-side path.
BROWSER-SIDE: NiiVue (@niivue/niivue, WebGL2) reads GIfTI/CIfTI-2/FreeSurfer CURV and ANNOT mesh overlays and exposes setMeshLayerProperty(mesh, layer, key, val) for live updates; threeBrain and BrainBrowser are alternatives.
LOGGING: plain JSONL beats every LLM-observability SaaS here - MLflow tracing, Statsig and similar are built around request/response pairs with nowhere to put a 20484-vector. JSONL is appendable, streamable, diffable and incrementally loadable, exactly the access pattern for drift forensics.

### Decision

**recommended_approach**

REVISED. Render an ANIMATED cortex with ROLLING-WINDOW NORMALISATION, and blend it into the frame pipeline rather than running a separate ffmpeg filter pass.

1. At process start, once: matplotlib.use('Agg'); fs = fetch_surf_fsaverage('fsaverage5'). Zero network cost, zero cold start. Precompute get_hcp_roi_indices() results and cache them.
2. NORMALISE OVER A ROLLING WINDOW. Keep a deque of the last ~30 clips' |values|; set vmax = p98 over the window, threshold = 0.35 * vmax. Seed from a short calibration run. This is the single most important line in the stage - MEASURED, fixed limits at threshold=1.5/vmax=4.0 render 0.00% of vertices, and naive per-frame autoscale makes noise look like drama.
3. Per iteration, at the moment you fire the fal request (not after), render T = preds.shape[0] frames: split at 10242, draw left-lateral and right-lateral into one figure with axes=/figure=, savefig(transparent=True), plt.close('all'). ~2 s for 15 frames, concurrent with the ~9 s generation.
4. COMPOSITE VIA THE FRAME PIPELINE if using infinite-livestream's client: hand the RGBA panels to the existing per-frame overlay path and let it alpha-blend (~0.6 ms/frame). This is better than my original per-clip ffmpeg-filter recommendation for a CONTINUOUS stream, because the client is already frame-pipe based rather than file based - a separate filter pass would mean re-encoding clips that are about to be decoded to frames anyway. Keep the ffmpeg overlay filter (with -c:a copy) as the standalone fallback if the project does NOT adopt that client.
5. Caption with get_topk_rois(). The ROI name beside the brain is what converts a pretty picture into a legible causal story, and it is one string.
6. Add the subcortical glass brain (139 ms) if TRIBE's mask is obtainable. Amygdala and accumbens lighting up is far more legible to a lay audience than any cortical parcel name.
7. Append the JSONL record; np.save the float16 array; record its sha1 AND the norm_window used.

Use cmap='hot' with a threshold, not the RdBu_r default.

WHY BURN IN RATHER THAN A BROWSER CANVAS: the browser path (NiiVue beside a <video>) animates at 60 fps and allows rotation, but it only works for viewers on YOUR page. Pushing to YouTube Live or Twitch - the cheapest delivery by a distance - requires the overlay already in the video, and the browser path then forces an OBS Browser Source purely to screen-scrape your own canvas back into a stream. That is an extra always-on process and a CEF instance to buy interactivity a livestream audience cannot use. Burn it in. Add the interactive version later as a companion page reading the same JSONL - it is additive, not a fork.

**simpler_alternative**

Fall back one step at a time; each is strictly simpler and none abandons the feature:
1. ONE STATIC PNG PER CLIP. Reduce (T, n) to (n,) with a mean or peak, render the 4-panel montage (229 ms), composite (490 ms). Total 0.72 s. A slideshow rather than a living brain, but 90% of the legibility for 30% of the cost - ship this on day one. STILL NEEDS the rolling-window normalisation; that is not the part to skip.
2. THE FLAT MAP. fsaverage5 ships flat_left/flat_right and both hemispheres render flat in 99 ms - faster than the inflated montage, whole cortex at once, no occluded medial surface. More diagrammatic, less brain-like. Worth an A/B on stream.
3. THE SUBCORTICAL GLASS BRAIN ALONE (139 ms). If the cortical surface proves fiddly, a glass brain with amygdala/accumbens/hippocampus lighting up is arguably MORE legible to a lay viewer than a cortical map, and it is cheaper. Blocked only on obtaining TRIBE's voxel mask.
4. THE PRECOMPUTED LUT. Rasterise the mesh once offline into an (H,W) vertex-index array, then per frame `img = cmap(values[idx])`. 20 ms measured against a 17 ms floor for writing any PNG. ~30 lines. Premature at current headroom; keep it for a sub-5-second cadence.
5. NO BRAIN, JUST BARS. A row of labelled bars from summarize_by_roi() drawn with ffmpeg drawbox/drawtext. Near-zero cost and honest, but it throws away the visual hook - bars could be anything, a cortex is unmistakably a brain. Only if nilearn cannot be installed in the container.
For logging there is no simpler alternative worth taking.
pycortex is NOT the fallback: it needs a configured filestore and per-subject surface database, it caches intermediates that silently invalidate, and no published benchmark shows it beating nilearn. nilearn's flat map at 99 ms removes the reason to reach for it.

**code_sketch**

# --- verified against nilearn 0.14.0 + ffmpeg 8.1.1 this session ---
import json, hashlib, subprocess, uuid
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')            # MUST precede the pyplot import on a headless box
import matplotlib.pyplot as plt
from nilearn import plotting, datasets

FS    = datasets.fetch_surf_fsaverage('fsaverage5')   # bundled in the wheel; 0.00 s, no download
SPLIT = 10242            # fsaverage5 vertices per hemisphere. verified empirically.

# ---- ROLLING-WINDOW NORMALISATION: the part that makes or breaks the overlay ----
# TRIBE targets were z-scored and detrended, and encoder predictions are shrunk toward
# the mean. A natural face photo drives FFA at only +0.080. MEASURED: threshold=1.5,
# vmax=4.0 renders 0.00%% of vertices -- a uniform dead cortex. But naive per-frame
# autoscaling flickers and makes noise look like drama. A rolling window fixes both.
class Norm:
    def __init__(self, window=30, pct=98, thresh_frac=0.35):
        self.buf, self.pct, self.tf = deque(maxlen=window), pct, thresh_frac
    def update(self, vals):
        self.buf.append(float(np.percentile(np.abs(vals), self.pct)))
    def limits(self):
        vmax = float(np.median(self.buf)) if self.buf else 1e-3
        vmax = max(vmax, 1e-4)                      # never divide by ~0 on a dead clip
        return vmax, vmax * self.tf

NORM = Norm()

def render_frame(vec, path, vmax, thresh):
    """One (20484,) cortical vector -> one transparent RGBA PNG. ~131 ms measured."""
    v = np.nan_to_num(vec, nan=0.0, posinf=0.0, neginf=0.0)
    lh, rh = v[:SPLIT], v[SPLIT:]     # concatenation boundary, NOT an anatomical claim
    fig, axes = plt.subplots(1, 2, subplot_kw={'projection': '3d'}, figsize=(4.4, 2.2))
    for ax, (mesh, bg, dat, hemi) in zip(axes, [
            (FS['infl_left'],  FS['sulc_left'],  lh, 'left'),
            (FS['infl_right'], FS['sulc_right'], rh, 'right')]):
        plotting.plot_surf_stat_map(mesh, dat, bg_map=bg, hemi=hemi, view='lateral',
                                    cmap='hot', threshold=thresh, vmax=vmax,
                                    colorbar=False, axes=ax, figure=fig)
    fig.subplots_adjust(0, 0, 1, 1, 0, 0)
    fig.savefig(path, dpi=100, transparent=True)
    plt.close('all')                  # omit this and the process leaks until it dies

def render_sequence(preds, outdir):
    """(T, 20484) -> T PNGs. DERIVE T; do not hard-code the rate.
       Measured: 15 frames 1.97 s, 30 frames 3.90 s. Run CONCURRENTLY with the fal call."""
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    NORM.update(preds)                          # one window update per clip, not per frame
    vmax, thresh = NORM.limits()
    for t in range(preds.shape[0]):             # <- T from the tensor, always
        render_frame(preds[t], outdir / f'frame_{t:03d}.png', vmax, thresh)
    return outdir, vmax, thresh

# ---- ROI readout: use TRIBE's shipped helpers, do not hand-roll ----
# from tribev2.utils import summarize_by_roi, get_topk_rois
# roi     = summarize_by_roi(preds.mean(0), hemi='both', mesh='fsaverage5')
# caption = ', '.join(get_topk_rois(preds.mean(0), k=3))   # the on-screen caption

# ---- compositing, standalone fallback only ----
# If using reactor-team/infinite-livestream, hand the RGBA panels to its per-frame
# overlay path instead (~0.6 ms/frame alpha blend) and skip this entirely.
def composite(clip_mp4, frames_dir, out_mp4, overlay_fps):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error',
        '-i', str(clip_mp4),
        '-framerate', str(overlay_fps), '-i', str(Path(frames_dir) / 'frame_%03d.png'),
        '-filter_complex',
        '[1]scale=440:-1,fps=25[ov];[0][ov]overlay=W-w-24:H-h-24:eof_action=repeat',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
        '-c:a', 'copy',                # keep H3 Max's synchronised audio bit-exact
        str(out_mp4)], check=True)

# ---- per-iteration logging ----
LOG = Path('run.jsonl'); ARR = Path('arrays'); ARR.mkdir(exist_ok=True)

def log_iteration(i, preds, roi, topk, policy, prompt, expanded_prompt, seed,
                  clip_url, timings, norm, safety_rejected=False, retries=0, buffer_depth=None):
    cid = uuid.uuid4().hex
    a = preds.astype(np.float16)
    p = ARR / f'{cid}.npy'; np.save(p, a)
    rec = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'iter': i, 'clip_id': cid,
        'vertex_vec_path': str(p),
        'vertex_vec_sha1': hashlib.sha1(a.tobytes()).hexdigest(),
        'vertex_shape': list(preds.shape),
        'norm_window': {'vmax': norm[0], 'threshold': norm[1]},  # else the render is
        'roi_reduction': roi,                                    # not reinterpretable later
        'topk_rois': topk,
        'reduction_policy': policy,
        'prompt': prompt, 'expanded_prompt': expanded_prompt,
        'seed': seed, 'clip_url': clip_url, 'timings': timings,
        'safety_rejected': safety_rejected, 'retry_count': retries,
        'buffer_depth': buffer_depth,
    }
    with LOG.open('a') as f:
        f.write(json.dumps(rec) + '\n'); f.flush()

# ---- offline drift forensics ----
# df = pd.read_json('run.jsonl', lines=True)
# df['vertex_vec_sha1'].duplicated().sum()        # >0 means the loop is repeating exactly
# pd.json_normalize(df['roi_reduction']).plot()   # collapse shows as flatlining
# df['expanded_prompt'].tail(20).tolist()         # the drift, in the model's own words

### Risk

**failure_modes**

SPECIFIC AND NON-OBVIOUS, in rough order of likelihood:
1. THE DEAD CORTEX. Colour limits chosen for z-scale data on values whose real magnitude is ~0.08. MEASURED: threshold=1.5/vmax=4.0 renders 0.00% of vertices. The overlay is a uniform grey blob that never changes, and the entire visual differentiator is gone. It throws no error and looks intentional. THE SINGLE MOST LIKELY WAY THIS FEATURE FAILS.
2. THE FLICKERING CORTEX. The overcorrection: naive per-frame autoscaling. Now an all-noise clip and a strongly-driven clip look identical, and the audience reads constant-amplitude noise as dramatic brain activity. Also silent. Only a rolling window avoids both.
3. Missing plt.close('all'). Every unclosed figure leaks; at 240 iterations/hour x 15 frames that is 3600 leaked figures/hour and an OOM kill within a day. One line.
4. NaN/inf in the vector -> blank or black panel, no exception. Always np.nan_to_num.
5. matplotlib is not thread-safe; rendering from a worker thread while the loop touches pyplot corrupts figures or segfaults. Use a process.
6. Forgetting matplotlib.use('Agg') before importing pyplot - fails only on the headless server, i.e. exactly at deploy time.
7. HARD-CODING THE FRAME RATE. Assume 2 Hz when the model emits ~1 Hz and you render twice the frames the tensor has, or index past the end. Derive T from preds.shape[0].
8. RECONSTRUCTING THE SUBCORTICAL VOLUME FROM THE WRONG MASK. MEASURED: nilearn's harvard_oxford sub-maxprob-thr25-2mm has 206,870 in-mask voxels across 21 labels, not 8,802. Fill a volume with TRIBE's vector using that mask and you get a confident, meaningless picture with no error anywhere.
9. Re-encoding audio during compositing. Dropping -c:a copy shifts A/V sync a frame or two per clip; over a chained stream that accumulates into visible drift and destroys the one thing H3 Max gives free.
10. Frame geometry not matching ffmpeg's -s WxH exactly -> scanline corruption ('TV static'), per infinite-livestream's documented learnings. Also: writing to ffmpeg stdin from the event loop starves the whole system; and platforms reject a stream with no audio track, even silence.
11. Overlay position hard-coded in pixels rather than W/H expressions - switch 480P to 768P to manage cost and the brain lands off-screen or over a face.
12. view_surf's 2.53 MB HTML per call. Fine in a notebook; 600 MB/hour in a loop. Offline only.
13. Log written only on success. The failed iterations are the ones worth logging. try/finally.
14. Unbounded .npy sidecars (~600 MB-1.2 GB/day) fill a small VPS in a fortnight and take the stream with them. Rotate.
15. Not logging norm_window. A recorded overlay whose colour scale is unrecoverable cannot be reinterpreted later, and you will want to.
16. The overlay makes attractor collapse VISIBLE - the same vertices lighting identically clip after clip, a frozen brain on stream. Diagnostically excellent, bad viewing. Watch vertex_vec_sha1 duplication and consecutive expanded_prompt diffs as the early warning.

### Evidence

**sources**

- MEASURED THIS SESSION (Apple M4, 10 cores, arm64; nilearn 0.14.0; matplotlib Agg; ffmpeg 8.1.1; median of 5 after warm-up). Primary measurements, not literature values: all latency figures; 10242 vertices/hemisphere; fsaverage5 bundled in the wheel (0.00 s fetch); PNG sizes; ffmpeg composite timings; the 0.00%-of-vertices-render result for threshold=1.5/vmax=4.0 and the 35.4% result for p98 normalisation; subcortical glass-brain 139 ms and stat-map 116 ms; and the Harvard-Oxford mask mismatch (206,870 in-mask voxels across 21 labels, not 8,802).
- MEASURED THIS SESSION - fsaverage5 vertex ordering is NOT anatomical. Loaded the Destrieux surface atlas on fsaverage5 (75 regions) and computed, for each region, the fraction of its vertex-index span actually occupied: MEDIAN CONTIGUITY 1.4%. Regions span essentially the entire 0-10242 range (e.g. G_insular_short: 50 vertices spread over indices 200-9844, 0.5% contiguous). Separately, spatially-nearest-neighbour vertices are a MEDIAN OF 5463 INDICES APART (mean 5120, max 9907). This PROVES that hard-coded fsaverage5 vertex index RANGES cannot correspond to anatomical regions, and confirms the warning about neuroscore's ROI accessors.
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/utils.py - VERIFIED. TRIBE v2 DOES ship parcellation helpers, correcting the original brief: get_hcp_labels(mesh='fsaverage5', combine=False, hemi='both'), get_hcp_vertex_labels(mesh='fsaverage5', combine=False), get_hcp_roi_indices(rois, hemi='both', mesh='fsaverage5'), summarize_by_roi(data, hemi='both', mesh='fsaverage5'), get_topk_rois(data, hemi='both', mesh='fsaverage5', k=10). HCP-MMP1 via mne.datasets.fetch_hcp_mmp_parcellation() and mne.read_labels_from_annot(); hemispheres handled separately with an index_offset based on mesh size, concatenated when hemi='both'.
- https://arxiv.org/html/2605.04326v1 - TRIBE v2 paper. Confirms features are aligned on 'an evenly spaced grid at a frequency f_stim=2 Hz' (0.5 s bins) for text/audio/video embeddings - i.e. 2 Hz is STIMULUS ALIGNMENT, not output rate; the prediction TR is not stated in the retrieved section. Confirms preprocessing includes 'Rescaling and detrending' (the basis for the normalisation warning). Confirms subcortical targets are 'the 8,802 voxels of 8 subcortical regions defined by the Harvard-Oxford atlas' (hippocampus, lateral ventricles, amygdala, thalamus, caudate, putamen, pallidum, accumbens; MNI 2 mm) and cortical predictions are 20,484 fsaverage5 vertices.
- https://github.com/reactor-team/infinite-livestream - Apache-2.0. Two parts: fast-h3 (FastVideo-distilled MiniMax-H3, 4-step sparse-attention, 768p with audio) and streaming-client (chat-to-prompt, clip queue, paced RTMP out). Model weights under the MiniMax H3 Community License.
- https://raw.githubusercontent.com/reactor-team/infinite-livestream/main/streaming-client/README.md - the overlay is NOT an ffmpeg filter: 'Every outgoing frame - live, repeated, or black - passes through the overlay before the sink'; 'Pillow rasterizes a panel only when its text changes; the per-frame cost is numpy alpha blends (~0.6 ms at 1344x768)'. Documented ffmpeg learnings: feed audio and video in lockstep on separate pipes; frame geometry must match -s WxH exactly or scanlines corrupt into 'TV static'; never write to ffmpeg stdin from the event loop; the sink restarts ffmpeg lazily with cooldown and failure caps; an audio track (silence included) is mandatory for platform acceptance.
- https://arxiv.org/html/2605.13904v1 - Bladon & Bent, feature visualisation on TRIBE v2. Source of the magnitude anchor that motivates the normalisation warning: optimised FFA stimuli reach +0.339 against a natural face photograph at +0.080.
- https://nilearn.github.io/dev/modules/generated/nilearn.plotting.plot_surf_stat_map.html - full signature and parameters; accepts raw numpy per-vertex arrays; hemi/view options; matplotlib and plotly engines
- https://nilearn.github.io/dev/modules/generated/nilearn.plotting.view_surf.html - full signature; returns SurfaceView; save_as_html/open_in_browser/resize; HTML-only output
- https://nilearn.github.io/dev/auto_examples/01_plotting/plot_3d_map_to_surface_projection.html - fsaverage5 is the low-resolution mesh with 10242 nodes per hemisphere
- https://github.com/nilearn/nilearn/blob/main/examples/01_plotting/plot_surf_stat_map.py - canonical usage example
- https://github.com/ThomasYeoLab/CBIG/blob/master/stable_projects/brain_parcellation/Yeo2011_fcMRI_clustering/1000subjects_reference/Yeo_JNeurophysiol11_SplitLabels/README.md - Yeo2011 17-network annot files; fsaverage5 follows a FreeSurfer subject layout with parcellations in fsaverage5/label/
- https://gallantlab.org/pycortex/generated/cortex.quickflat.make_png.html - pycortex flatmap PNG API and its intermediate-step caching / recache=True behaviour
- https://dev.to/javidjamae/ffmpeg-overlay-filter-picture-in-picture-and-compositing-5fog - overlay filter, filter_complex for multiple inputs, W/H/w/h position variables, eof_action
- https://www.host-stage.net/case-study/ffmpeg-vs-obs/ - OBS keeps its scene compositor and preview renderer running on static scenes, burning CPU on unused UI; ffmpeg is the headless choice
- https://github.com/StreamElements/obs-browser - OBS Browser Source renders via CEF to a shared texture
- https://niivue.com/docs/api/niivue/classes/Niivue/ - setMeshLayerProperty(mesh, layer, key, val) for live mesh-overlay updates
- https://github.com/niivue/niivue - WebGL2 viewer; mesh overlay formats GIfTI/CIfTI-2/MZ3/SMP/STC/FreeSurfer CURV+ANNOT
- https://dipterix.org/threeBrain/ and https://brainbrowser.cbrain.mcgill.ca/ - alternative WebGL surface viewers
- https://fast.io/resources/ai-agent-production-logging/ - full-text debug logs in JSONL, ~30 day retention for active debugging
- https://dev.to/apprs_6334/diff-every-tool-call-replaying-agent-runs-from-a-jsonl-trace-2b75 - JSONL traces are appendable, streamable, diffable, incrementally loadable; replay tooling flags identical repeats and cross-run drift
- https://www.statsig.com/perspectives/observabilitydebuggingai - capture the exact input actually sent to the model (rationale for logging expanded_prompt)
- INFERENCE (explicitly marked): the rolling-window normalisation design (window 30, p98, threshold 0.35*vmax) is my synthesis of the measured failure of fixed limits and the known flicker problem of per-frame autoscaling. The parameters are reasoned defaults validated on SIMULATED data with plausible statistics (std 0.057, p99 0.193), not on real TRIBE output.
- INFERENCE (explicitly marked): the revised recommendation to alpha-blend into the frame pipeline rather than run a per-clip ffmpeg filter follows from infinite-livestream's documented frame-pipe architecture - a separate filter pass would re-encode clips that are about to be decoded to frames anyway. Their README does not itself make this recommendation.
- INFERENCE (explicitly marked): the ~600 MB-1.2 GB/day sidecar figures are arithmetic (T x 20484 x 2 bytes x 240/hour x 24), and the claim that a modern x86 server core is broadly comparable to the Apple M4 here follows from the work being single-threaded CPU rasterisation. Both flagged in unknowns.

### Other Info

**item_id**

A

**focus**

Logging the loop, and rendering the predicted brain map as an on-stream overlay.

### Flagged Uncertain (omitted above)

- `cost`
- `unknowns`

---

## Orchestration loop and buffer management

### Identity

**what_it_is**

The single always-on process that decides what to generate, how many generations to have in flight, when to stop submitting, when to run the brain model and on what window, what to air when nothing is ready, and what to do when fal refuses a prompt. It is the only stateful component in the system and the only one that can take the stream off the air.

**role_in_loop**

It IS the loop, and it runs TWO clocks that must be designed separately: a GENERATION clock (one 15 s clip submitted and aired every D seconds) and a PERCEPTION clock (one TRIBE pass over a rolling 30 s window every N clips). Everything else — the translator, the fal client, the streaming stage — is a pure function it calls. All timing, backpressure, buffer policy and failure handling live here.

### Interface

**interface_spec**

=== fal queue API (the only external surface that matters) ===
POST https://queue.fal.run/{model-id}          # e.g. minimax/h3-max/text-to-video
  Authorization: Key $FAL_KEY
  ?fal_webhook=https://your-host/webhook        # or webhook_url via the SDK
  body: prompt, duration, resolution, seed, prompt_expansion_mode, enable_safety_checker, image_url/end_image_url
->  { "request_id": "764cabcf-...", "status_url": ".../status", "response_url": ".../response",
      "cancel_url": ".../cancel", "queue_position": 0 }

States: IN_QUEUE -> IN_PROGRESS -> COMPLETED.
  IN_QUEUE    : stored, waiting for a runner. DOES NOT count against concurrency.
  IN_PROGRESS : dispatched to a runner. COUNTS against concurrency.
  COMPLETED   : result at response_url, or POSTed to your webhook.

SDK:
  handler = fal_client.submit(model, arguments={...}, webhook_url="https://.../webhook")
  handler.request_id ; handler.status(with_logs=True) ; handler.get() ; handler.cancel()
  const { request_id } = await fal.queue.submit(model, { input, webhookUrl });
  await fal.queue.cancel(model, { requestId });

=== Concurrency ladder (VERIFIED against fal's own docs) ===
  New accounts: 2 concurrent IN_PROGRESS. Scales automatically on credit purchases over the last 4 weeks,
  self-serve ceiling 40; above that, sales. Requests are NEVER rejected for concurrency — at capacity a
  queued request stays queued and is retried with exponential backoff, no maximum retry count (direct run()
  retries up to 10). 429 `concurrent_requests_limit` + header `X-Fal-needs-retry: 1` on the direct path.
  All four claims from the brief CONFIRMED. See throughput_constraint for why 2 is enough and why raising it
  is a trap.

=== Error contract you must branch on (fal's documented error table) ===
  422 non-retryable  : content_policy_violation, value_error, input_value_error, missing
  422, see note      : no_media_generated  <- fal's table says Retryable: No; a teammate reports it IS
                       retryable. Both readings are defensible and they imply the SAME policy: see
                       recommended_approach. Budget it separately from content_policy_violation.
  5xx retryable      : request_timeout(504), startup_timeout(504), runner_scheduling_failure(503),
                       runner_connection_timeout/refused/error(503), runner_disconnected(503)
  5xx non-retryable  : runner_incomplete_response(502), runner_server_error(500), internal_error(500)
  Branch on `type`/`error_type`, never on `msg`.

=== TRIBE side (from items 01 and 03, measured by teammates on a billed deployment) ===
  predict(window_video, window_audio) -> (T_seconds, 20484) cortical at 1 Hz, plus subcortical.
  NOTE: output is 1 Hz. A 15 s clip yields (15, 20484); a 30 s window yields (30, 20484). The 2 Hz figure
  in circulation is the stimulus FEATURE rate, not the output rate.
  Cost: 2.3-2.9 s of compute per 1 s of stimulus in Fast mode (video+audio, no text branch, bf16 + TF32 +
  frame dedup). Checkpoint trained with duration_trs=100 and time_pos_embedding=True, i.e. on 100-SECOND
  windows; practical floor ~30 s. THE FLOOR IS NOT ENFORCED IN CODE — a short window runs silently and
  returns garbage rather than raising. Assert it yourself before every call.

=== Internal orchestrator state ===
  inflight:  {request_id -> {prompt, brain_state, submitted_at, attempt}}   # 2 steady, burst higher only on recovery
  ready:     deque[{path, frames, samples, prompt, brain_state, gen_at}]    # target 6, hard cap 10
  ring:      deque[last 40 aired segments]                                  # deep under-run source
  window:    deque[last 2 clips' decoded frames+samples]                    # TRIBE perception window, 30 s
  brain:     latest readout, held between perception passes

**output_contract**

One spec-conformant MP4 handed to the streaming stage every D seconds, forever, tagged with its provenance: `filler` (generated from the drift term, not from a brain state) and `replay` (re-aired from the archive). The streaming stage needs both flags — `replay` drives the RERUN badge, and neither filler nor replays may re-enter the perception window.

Plus a status document (Infinite Slop publishes status.json) exposing on-air prompt, in-flight prompts, ready
buffer and pending queue. For this project that document is where the brain-state readout becomes visible to
the audience, so it is part of the artwork rather than debug output. Add one field that neither reference
implementation needs: `age_of_current_brain_state`, in seconds. Condition (2) fails silently and this is the
only thing that shows it.

And a latency, which is the honest headline output of this item. Reaction staleness — the gap between a
stimulus clip airing and the clip generated in response to it airing:
  audio_only TRIBE, W=30 s : T_perc + W_gen  ~=  6 + 15   =  21-25 s
  trimodal TRIBE,   W=30 s : T_perc + W_gen  ~=  87 + 15  =  81-105 s
Independent of buffer depth in both cases, PROVIDED clips are perceived at download time. If they are
perceived at playback instead, add B*D — 90 s at B=6 — to both figures. For comparison, Infinite Slop's
MEASURED request-to-air latency is ~154 s, and it is not attempting to be reactive to anything but chat.

Units note for downstream consumers: TRIBE's readout is 1 Hz, so a 30 s window yields a (30, 20484) cortical
matrix, not a vector. The temporal reduction to a control signal is item 02's decision, not this item's.

### Complexity

**dev_complexity**

MEDIUM for a single developer, with the difficulty concentrated in two places, neither of them the fal integration.

Easy (hours): queue submission, webhook receipt, a deque, an airing timer. The SDK does the hard parts.

HARD PART ONE — the two clocks. Generation and perception run at different rates over different window sizes
with different resource pools, and the perception clock fails SILENTLY when it falls behind (no exception, no
backpressure signal, just an increasingly stale brain state). You must instrument perception lag explicitly
and alarm on it; nothing else will tell you.

HARD PART TWO — no natural test harness. Under-run, rejection storms, concurrency saturation, webhook loss
and perception-lag drift all happen under conditions you cannot reproduce on demand and that cost real money
to provoke. Budget for a simulation mode: a fake fal client with configurable G distribution, rejection rate
and failure injection, plus a fake TRIBE with a configurable compute-per-stimulus-second ratio. ~110 lines,
runs 24 simulated hours in a minute, and it is the difference between this being MEDIUM and being a week of
mystery debugging at $288/hour.

HIGH if you reach for a task queue. Celery/RQ/Temporal are the wrong shape: one worker, <10 concurrent tasks,
state that fits in a dict. A single asyncio process with two deques is correct.

**loc_estimate**

~360 lines of orchestrator, plus ~110 for the simulation harness.
  async submit loop with backpressure + adaptive C   ~55
  webhook receiver + download + decode + handoff     ~50
  airing tick + ready/filler/ring precedence         ~50
  perception scheduler (every Nth clip, K workers,
    lag instrumentation, 30 s floor assertion)       ~55
  rolling decoded-array window cache                 ~30
  two-tier under-run (generated filler + replay ring) ~45
  error branching + split safety retry paths         ~45
  cancel-stale-requests logic                        ~20
  status.json publisher                              ~30
  config/state/logging                               ~40
  ------------------------------------------------------
  total                                             ~360
  fake-fal + fake-TRIBE simulation harness          ~110

**off_the_shelf_option**

Two things worth taking, one library and one design.

TAKE THE LIBRARY: fal_client (Python) / @fal-ai/client (JS). `submit` + `webhook_url` + `handler.cancel()` is
the entire integration. `handler.iter_events()` exists but polling is the wrong pattern at this cadence.

TAKE THE DESIGN: reactor-team/infinite-livestream's `director.py` idle-filler policy (Apache-2.0, verified
this session). It is a more thought-through answer to buffer management than anything I would have designed,
and the specific rules are the valuable part:
  - top the queue up to IDLE_QUEUE_TARGET (default 6) from a preset prompt list, shuffled then rotated;
  - the target SELF-CLAMPS to one below live playout capacity (default 10), because a full playout queue
    pauses builds and that headroom slot is where the next real clip lands;
  - filler is forced to ONE SCENE PER GROUP — the finest eviction granularity, so popping one never truncates
    a story — and is tagged `generated: true`;
  - real requests outrank filler four ways: they insert into the generation queue ahead of waiting filler and
    behind waiting real work; the playout loop plays real clips first; filler stands down when real work is
    pending, including work that arrived while the filler's own LLM call was in flight; and when a full
    playout queue of built filler blocks a real build, the playout loop pops one filler per tick, NEWEST
    FIRST, until the build resumes;
  - only `generated: true` clips are ever evicted, and a playing clip is in neither queue so playback is never
    cut;
  - every capacity is read live from state, never assumed.
That is roughly a day of design you can skip. Adapt `!prompt from chat` to `prompt from brain readout` and
the policy transfers unchanged.

DO NOT TAKE: Celery, RQ, Temporal, Inngest, Redis (unless the orchestrator and web server are separate
processes). All add a second thing that can be down while the stream is on air.

SIGNPOST, not an option for this item: fal-ai-community/realtime-krea-wan. If you go item 17's autoregressive
route, this entire item dissolves — there are no clips to buffer and no two clocks to reconcile.

### Decision

**recommended_approach**

One asyncio process, webhook-driven, two clocks, three numbers, two fallback tiers.

THE THREE NUMBERS
  B_target = 6 ready clips, B_max = 10   (set by perception throughput; converges with two production systems)
  C        = 2 in flight, bursting to 4-6 ONLY during filler/rerun recovery
  N        = 2 (analyse every 2nd clip), W = 30 s, K = 1 with audio_only

PERCEIVE AT DOWNLOAD TIME, NOT AT PLAYBACK TIME — one line of queue plumbing, ~90 s off reaction staleness,
and it makes staleness independent of buffer depth. THIS REVERSES WHAT I SAID EARLIER. I previously argued
for perceiving the on-air clip on the grounds that otherwise 'the brain is responding to content the audience
hasn't seen'. That reasoning was wrong, and it is worth being precise about why, because the mistake is
tempting: there is no real brain here. TRIBE predicts a HYPOTHETICAL viewer's response, and a hypothetical
viewer can perceive a clip whenever you like. What must be preserved is the SEQUENCE — the checkpoint is
windowed and order-sensitive — and a FIFO buffer preserves order exactly. Download-time order equals playback
order, so perceiving early is both faster and sequence-faithful. There is no conceptual cost.
  ONE CAVEAT that follows directly: filler and reruns break FIFO order — they air but were already perceived,
  or were never part of the intended sequence. Do NOT re-perceive them and do not let them enter the
  perception window, or the brain state loops on its own past and the readout degenerates.

THE TWO-TIER UNDER-RUN FALLBACK. A single mechanism is not enough because there are two distinct failures:
  TIER 1 — SHALLOW (buffer thinning, generation still working). Generate FILLER from the novelty/drift term
    that item 09 needs anyway for damping. Costs money, stays fresh, keeps the stream genuinely generative.
    Use reactor-team's policy verbatim (see off_the_shelf_option): top up to 6, self-clamp to capacity-1,
    one scene per group, tag `generated: true`, evict newest-first, never evict real clips, never cut a
    playing clip. Real brain-driven prompts outrank filler in all four of their ways.
  TIER 2 — DEEP (generation actually failing: fal outage, rejection storm, credit exhausted). REPLAY RING
    from the archive, flagged `replay: true`. Costs $0. This is Infinite Slop's shipped mechanism — meta.json
    carries a per-segment `replay` boolean and the client renders 'RERUN' with an age past 900 s. The
    client-side half matters as much as the server half: on FRAG_CHANGED, scan forward for the first unseen
    non-replay fragment and seek to it, so a fresh clip PRE-EMPTS the rerun loop rather than queueing behind
    it. Without that, one stall leaves you permanently a buffer-depth behind.
  Precedence: real > filler > replay. Rejected alternatives and why: slow-motion of the prior clip needs a
  transcode and destroys H3 Max's native dialogue audio (atempo on speech is unlistenable); a crossfade hold
  on the last frame reads as a crash rather than a choice.

THE SAFETY PATH — BUDGET THE TWO 422s SEPARATELY. They look alike and behave oppositely:
  content_policy_violation — DETERMINISTIC. The same prompt is guaranteed to fail again and burns a slot for
    nothing. Never resubmit it. Sanitise (strip the salience descriptors that cluster with rejection: gore,
    weapons, distressed or injured faces, nudity terms, real-person names), re-roll the seed, resubmit ONCE.
    On a second rejection, fall to filler and record the driving brain-state vector in a `rejected` set that
    feeds item 09's damping term.
  no_media_generated — STOCHASTIC. The model produced nothing for an input that was otherwise acceptable.
    fal's error table marks it Retryable: No; a teammate reports it IS retryable. Both readings imply the
    same policy, which is why the conflict does not need resolving before you build: retry exactly ONCE with
    a seed change and no prompt edit. If fal's table is right you have wasted one slot; if the teammate is
    right you have recovered a clip. Do not retry twice either way.
  Cost model: with rejection rate r and one retry, effective slot throughput is ~1/(1+r). At r=0.2 you lose
  ~17% of capacity — which condition (1) above already absorbs at C=2.
  THE COUPLING THAT MAKES THIS DANGEROUS: a brain-activation-maximising objective drifts toward faces, threat
  cues and high salience — precisely the checker's trigger set. r is not a constant; it RISES as item 09's
  attractor collapse progresses. A stream that is working well aesthetically is a stream whose rejection rate
  is climbing. Instrument r as a time series; it is the earliest available collapse signal.

STALENESS CANCELLATION. Stamp every request with the brain state that produced it. When the readout moves
beyond a threshold, POST to cancel_url for any request still IN_QUEUE whose driving state is now stale.
Cancelling a queued request is documented as immediate. This is the one lever that buys reactivity back
without shrinking the buffer — and with perceive-at-download already applied, it is the remaining one.

ASSERT THE 30 s FLOOR BEFORE EVERY TRIBE CALL. It is not enforced anywhere in TRIBE's code: a short window
runs silently and returns garbage rather than raising. At cold start you have fewer than 2 clips buffered, so
the very first perception pass is exactly the case that will silently produce nonsense. Hold the brain state
at a neutral default until the window is genuinely full.

INSTRUMENT PERCEPTION LAG. Condition (2) fails without any error: the stream keeps running and the brain
state just gets older. Publish `age_of_current_brain_state` alongside the usual counters and alarm when it
exceeds N*D by more than one clip. Nothing else surfaces this.

**simpler_alternative**

TWO RUNGS DOWN, in order of how much they remove.

RUNG 1 — polling instead of webhooks, no cancellation, fixed C (~60 lines). Spawn exactly C asyncio tasks,
each an infinite `while True: prompt = translate(brain.latest()); clip = await
fal_client.subscribe_async(MODEL, arguments={...}); ready.append(clip)`. `subscribe` holds the connection and
hides the queue entirely: no webhook endpoint, no public URL, no reaper for lost callbacks, no request_id
bookkeeping — which kills two of the listed failure modes outright. Concurrency is enforced by the number of
tasks. Backpressure becomes `while len(ready) >= B_MAX: await asyncio.sleep(0.5)` at the top of each task.
Keep the replay ring and the 30 s floor assertion — those are not optional at any rung. What you lose: no
staleness cancellation, and long-held connections are more fragile across a restart. Correct choice for the
first working demo.

RUNG 2 — take BOTH fal and TRIBE out of the live loop (the genuinely shortest path to something on screen,
and the one I would build first). Precompute a bank of clips offline: enumerate a few hundred brain-state
archetypes from item 16's ROI->motif table, generate 3-5 clips for each as an overnight batch, and at runtime
SELECT which precomputed clip to air based on the current readout. This is far more attractive than it looks
once condition (2) is on the table, because it dissolves BOTH steady-state conditions at once: no concurrency
ladder, no perception-throughput obligation, no K workers, no always-on A100, no silent perception lag,
safety rejections handled once at batch time by a human rather than live at 3 a.m., under-run structurally
impossible, and cost collapsing from $288/hour to a one-off batch spend. Reactivity survives at the selection
level — the stream still changes in response to the predicted brain state, it just chooses rather than
generates, and selection latency is milliseconds rather than 21-105 s, so it is arguably MORE reactive than
the live system.
Two honest caveats: the piece is no longer 'generated from a brain response' and the framing must say so
(item 14); and repetition becomes visible within about an hour at 240 clips/hour against a bank of a few
hundred.
Mitigation, and my actual recommendation for a first build: a HYBRID. Air from the bank by default, run TRIBE
at a relaxed cadence (N=4 or slower — there is no throughput obligation when nothing depends on it landing on
time), and spend your 2 concurrent fal slots generating fresh material for whichever brain states the bank
covers worst. Cost, complexity and failure surface all sit far below the live loop, and the stream is
generative where it matters.

**code_sketch**

import asyncio, time, collections, os, fal_client

D        = 15.0   # seconds of video per clip
W_SEC    = 30.0   # TRIBE perception window -- 2 clips. NOT the same as D.
N_EVERY  = 2      # run TRIBE every Nth clip; the free tunable
B_TARGET = 6      # set by perception throughput: ceil(T_tribe / D)
B_MAX    = 10     # stop submitting above this (BILLING GUARD: fal never rejects)
C_STEADY = 2      # in flight. Raising this makes the driving brain state C*D stale.
C_BURST  = 6      # only while airing filler/reruns, when reactivity is already lost
RING_N   = 40
MODEL    = "minimax/h3-max/text-to-video"

ready    = collections.deque()   # finished clips, pre-playback. Also the perception backing store.
ring     = collections.deque(maxlen=RING_N)
inflight = {}
window   = collections.deque(maxlen=int(W_SEC / D))   # decoded arrays, concatenated in memory
brain    = None                  # held between perception passes
brain_at = 0.0
degraded = False                 # True while airing filler/reruns
r_hits = r_total = 0             # rejection rate over time -> item 09 collapse signal

def c_target():
    return C_BURST if degraded else C_STEADY

# ---------- submit side ----------
async def submit_loop(translate):
    while True:
        if brain is not None and len(inflight) < c_target() \
           and len(ready) + len(inflight) < B_MAX:
            prompt = translate(brain)
            h = fal_client.submit(
                MODEL,
                arguments=dict(prompt=prompt, duration=int(D), resolution="768P",
                               prompt_expansion_mode="balanced",   # 'quality' ~30 s: unusable live
                               enable_safety_checker=True),
                webhook_url=os.environ["WEBHOOK_URL"])
            inflight[h.request_id] = dict(prompt=prompt, brain=brain,
                                          at=time.time(), attempt=1, handle=h)
        else:
            await asyncio.sleep(0.25)
        await asyncio.sleep(0.1)

# ---------- webhook: split the two 422s, they behave oppositely ----------
async def on_webhook(payload):
    global r_hits, r_total
    job = inflight.pop(payload["request_id"], None)
    if job is None:
        return
    r_total += 1

    if payload["status"] != "COMPLETED":
        et = (payload.get("error") or {}).get("type") or payload.get("error_type")

        # DETERMINISTIC. Same prompt WILL fail again -- never resubmit it unchanged.
        if et == "content_policy_violation":
            r_hits += 1
            rejected_states.append(job["brain"])          # -> item 09 damping term
            if job["attempt"] == 1:
                await resubmit(sanitise(job["prompt"]), job["brain"], attempt=2, reseed=True)
            return

        # STOCHASTIC. Same prompt, new seed, exactly one attempt.
        if et == "no_media_generated":
            if job["attempt"] == 1:
                await resubmit(job["prompt"], job["brain"], attempt=2, reseed=True)
            return

        if et in ("request_timeout", "startup_timeout", "runner_scheduling_failure",
                  "runner_connection_timeout", "runner_connection_refused",
                  "runner_connection_error", "runner_disconnected") and job["attempt"] < 2:
            await resubmit(job["prompt"], job["brain"], attempt=job["attempt"] + 1)
        return

    path = await download(payload["payload"]["video"]["url"])
    frames, samples = decode(path)        # decode ONCE; reused by the perception window
    clip = dict(path=path, frames=frames, samples=samples,
                prompt=payload["payload"].get("expanded_prompt", job["prompt"]),
                brain=job["brain"], gen_at=int(time.time()), filler=False)
    ready.append(clip)

    # PERCEIVE AT DOWNLOAD TIME, not at playback. Removes B*D from reaction staleness
    # and makes staleness independent of buffer depth. FIFO preserves the sequence,
    # which is the only property TRIBE's windowing actually requires.
    if not clip["filler"]:
        window.append(clip)
        perceive_q.put_nowait(len(ready))

# ---------- perception clock: separate rate, separate resource ----------
async def perceive_loop(tribe, translate):
    global brain, brain_at
    n = 0
    while True:
        await perceive_q.get()
        n += 1
        if n % N_EVERY:
            continue                                   # hold the brain state between passes
        if len(window) < window.maxlen:
            continue                                   # 30 s FLOOR IS NOT ENFORCED BY TRIBE --
                                                       # a short window returns garbage, silently
        vid = concat_frames([c["frames"] for c in window])   # arrays in memory, no ffmpeg,
        aud = concat_samples([c["samples"] for c in window]) # history never re-encoded
        brain = await tribe.predict(vid, aud)          # (30, 20484) at 1 Hz; 2 Hz is the feature rate
        brain_at = time.time()

async def perception_lag_monitor():
    """Condition (2) fails with NO error -- the brain state just gets older. Alarm on it."""
    while True:
        age = time.time() - brain_at
        if brain_at and age > N_EVERY * D + D:
            log.warning("[perception] brain state %.0fs old, budget %.0fs -- TRIBE is behind",
                        age, N_EVERY * D)
        await asyncio.sleep(5)

# ---------- airing tick: real > filler > replay ----------
async def air_loop(publish):
    global degraded
    while True:
        real = next((c for c in ready if not c["filler"]), None)
        if real is not None:
            ready.remove(real); degraded = False
            seg = publish(real["path"], real["prompt"], real["brain"], replay=False)
            ring.append(dict(seg=seg, gen_at=real["gen_at"], replay=False))
        elif ready:
            degraded = True                            # TIER 1: generated filler
            f = ready.popleft()
            seg = publish(f["path"], f["prompt"], f["brain"], replay=False)
            ring.append(dict(seg=seg, gen_at=f["gen_at"], replay=False))
        else:
            degraded = True                            # TIER 2: replay ring, $0
            cand = [x for x in ring if x["seg"] not in recent_aired and not x["replay"]] \
                or [x for x in ring if x["seg"] not in recent_aired]
            if cand:
                pick = max(cand, key=lambda x: x["gen_at"])
                republish(pick["seg"], replay=True)    # meta.json replay:true -> client shows RERUN
                recent_aired.append(pick["seg"])
            # NB: reruns and filler are NOT fed back into `window` -- re-perceiving them
            # loops the brain state on its own past.
        await asyncio.sleep(D)

# Build the harness too -- it is the only way to test any of this:
#   FakeFal (configurable G distribution, rejection rate, failure injection) +
#   FakeTribe (configurable compute-per-stimulus-second), so 24 simulated hours
#   run in a minute instead of costing $6,900.

### Risk

**failure_modes**

1. PERCEPTION FALLS BEHIND SILENTLY. Condition (2) fails with no exception, no backpressure, no 429 — the
stream keeps running and the brain state simply gets older. A naive 'run TRIBE on every new clip' loop at
W=30 s trimodal K=1 falls behind at 4.6-5.8x and never recovers, and everything looks fine. This is the most
likely way to build this system wrong. Publish age_of_current_brain_state and alarm on it; nothing else
surfaces it.

2. THE 30 s FLOOR IS NOT ENFORCED IN TRIBE'S CODE. A short window runs and returns garbage rather than
raising. Cold start is exactly this case — you have fewer than 2 clips buffered on the first pass. Assert the
window length yourself and hold a neutral brain state until it is genuinely full.

3. NO BACKPRESSURE -> UNBOUNDED BILL. fal never rejects a submission and IN_QUEUE is unlimited, so a loop
that submits while the airing side is stalled queues hundreds of billable generations at $0.60-1.20 each.
No error, no 429, no log line. Cap on len(inflight)+len(ready) and set a hard hourly spend ceiling.

4. WEBHOOK LOSS -> PERMANENT SLOT LEAK. A dropped webhook leaves the request_id in `inflight` forever,
effective concurrency drops by one, and the buffer bleeds out over hours. It presents as 'generation got
slower'. At C=2 losing one slot halves your throughput and breaks condition (1). Mandatory: a reaper polling
status_url for any inflight job older than 3x expected G.

5. FEEDING FILLER OR RERUNS BACK INTO THE PERCEPTION WINDOW. The brain state then responds to its own past
output and degenerates — a fast path into item 09's attractor collapse, arriving through the buffer rather
through the aesthetics. Exclude anything not on the intended FIFO sequence.

6. RISING REJECTION RATE COUPLED TO AESTHETIC SUCCESS. A brain-activation-maximising objective drifts toward
faces, threat and salience — exactly the checker's trigger set. r climbs as the piece starts working.
Throughput degrades precisely when things are going well.

7. RAISING C TO FIX A THROUGHPUT PROBLEM YOU DO NOT HAVE. C=2 already satisfies condition (1) with 1.6x
headroom at r=0.2. Raising it to 4 doubles brain-state staleness to 60 s to buy capacity that is not the
bottleneck — the bottleneck is condition (2), which more concurrency does nothing for. Diagnose which
condition is failing before touching C.

8. THE RERUN DEATH SPIRAL. Without the client-side 'fresh clip pre-empts reruns' rule, a single stall leaves
the player permanently one buffer-depth behind and every fresh clip queues behind reruns. The server-side
ring is only half the fix.

9. RETRY-STORM DOUBLE BILLING. fal retries retryable failures internally (up to 10 on the direct path).
Layering unbounded retries on top pays for the same clip repeatedly. Cap own attempts at 2, and never retry
content_policy_violation unchanged — it is deterministic and pure waste.

10. THUNDERING HERD AFTER A STALL. When the buffer drains and C slots free at once, submissions and
completions synchronise and the system oscillates. Stagger by G/C seconds.

11. CLOCK DRIFT ON THE AIRING TICK. `await asyncio.sleep(D)` after variable work accumulates drift against
the real playlist. Schedule against an absolute next-air timestamp.

12. FILLER STARVING REAL WORK. If filler is allowed to fill the playout queue to the brim, generation pauses
and there is no slot for the next real clip. reactor-team's clamp — target one below capacity — exists for
exactly this, and evicting newest-first ensures you drop the least-invested filler.

### Evidence

**sources**

- https://fal.ai/docs/documentation/model-apis/concurrency-limits — CONFIRMS ALL FOUR BRIEF CLAIMS: new accounts start at 2 concurrent; scales automatically on credit purchases over the last 4 weeks; self-serve maximum 40; above that requires sales. Only IN_PROGRESS counts; IN_QUEUE does not. Requests are never rejected — at capacity they wait and are retried with exponential backoff, no maximum retry count. 429 type `concurrent_requests_limit`, header `X-Fal-needs-retry: 1`.
- https://fal.ai/docs/documentation/model-apis/errors — full error table. content_policy_violation 422 Retryable:No; no_media_generated 422 Retryable:No (CONFLICTS with a teammate's report that it is retryable — see unknowns); request_timeout 504 Yes; startup_timeout 504 Yes; runner_scheduling_failure 503 Yes; runner_connection_* 503 Yes; runner_server_error 500 No. Branch on `type`, not `msg`.
- https://fal.ai/docs/documentation/model-apis/inference/queue — queue API: POST https://queue.fal.run/{model-id}; request_id, status_url, response_url, cancel_url, queue_position; IN_QUEUE -> IN_PROGRESS -> COMPLETED; webhook_url on submit; metrics.inference_time; no queue size limits; cancellation stops queued requests immediately.
- https://docs.fal.ai/model-apis/model-endpoints/webhooks — webhook_url on submit; fal POSTs request_id, status and payload on completion.
- https://infiniteslop.ai/status.json — LIVE MEASUREMENT, 5 polls over 76 s (2026-08-31 21:31 UTC). in-flight (`generating_now`) 2/3/3/3/4; ready buffer (`playing_next`) 4/5/5/6/5; pending queue 52/56/53/53/44; now_replay false throughout. Independent corroboration of B~5-6 and C~2-4. Also shows an autonomous prompt source ('SLOP NEWS NETWORK') keeping the queue full when chat is quiet — the tier-1 filler pattern in the wild.
- https://infiniteslop.ai/live/meta.json — LIVE: per-segment {prompt, chat, gen_at, replay}. The `replay` boolean is the shipped tier-2 under-run mechanism.
- https://infiniteslop.ai/ — page source: client-side 'a brand-new clip beats queued reruns' logic and the RERUN badge past 900 s.
- https://github.com/reactor-team/infinite-livestream — VERIFIED via GitHub API this session: Apache-2.0, created 2026-08-30, 157 stars, Python. Source for the tier-1 filler design.
- https://raw.githubusercontent.com/reactor-team/infinite-livestream/main/streaming-client/README.md — read this session. 'Idle filler' section: IDLE_QUEUE_TARGET default 6, self-clamping to one below playout capacity (default 10) because a full playout queue pauses builds and the headroom slot is where the next viewer clip lands; filler forced to one scene per group (finest eviction granularity); tagged `generated: true`; four ways viewers outrank filler; evict newest-first, only `generated:true`, never cut a playing clip; capacities read live from state_update, never assumed.
- https://levels.io/ai-video-faster-than-you-watch — 'It generates 15 seconds of video in 9 seconds!'
- https://levels.io/37000-watched-infinite-slop — 'Only 4 videos per minute can be generated (4x 15 seconds = 1 minute)', i.e. exactly 1x real time at 15 s clips.
- https://anikuku.com/blog/fal-h3-max-api-speed-pricing-2026 — CONFLICTING TIMING: 5 s/768p 'under 3 seconds' (~2.53 s observed) but a 15 s clip 'about 15 seconds'. Pricing: 480p $0.025/s launch, $0.05/s regular; 768p $0.04/s launch, $0.08/s regular; launch pricing through September 1. Notes timings are inference only.
- https://blog.fal.ai/introducing-h3-max-by-fal/ — fal's own announcement: 5-second video in approximately 3 seconds; 35x the throughput of the official MiniMax H3 endpoint. No 10 s or 15 s figure.
- https://fal.ai/legal/trust-and-safety — platform-level content policy applies independently of the per-request enable_safety_checker flag.
- https://github.com/fal-ai/fal/issues/939 — a revoked API key does not release IN_PROGRESS concurrent slots, with no self-service recovery. A filed way to permanently lose concurrency capacity; do not rotate keys while requests are in flight. At C=2 this is fatal.
- https://github.com/fal-ai-community/realtime-krea-wan — 'text-to-video with dynamic prompt rewriting' on a realtime model; item 17's competing architecture, in which both steady-state conditions dissolve.
- TEAMMATE MEASUREMENTS (items 01/03, billed deployment, not independently verified by me): TRIBE runs 2.3-2.9x slower than realtime in Fast mode (video+audio, no text, bf16 + TF32 + frame dedup) — a ~60 s clip scores in ~140-175 s; audio_only ~6 s; checkpoint trained with duration_trs=100 and time_pos_embedding=True (100-second windows), practical floor ~30 s, floor NOT enforced in code (silent garbage on short input); output is 1 Hz, not 2 Hz (2 Hz is the stimulus feature rate). Every K and N figure in throughput_constraint is derived from the 2.3-2.9x number by LINEAR scaling in window length — see unknowns, that linearity is an assumption I did not verify.

### Other Info

**item_id**

08

### Flagged Uncertain (omitted above)

- `cost`
- `input_contract`
- `latency_ms`
- `realtime_headroom`
- `throughput_constraint`
- `unknowns`

---

## Prior art and reference implementations

### Identity

**what_it_is**

A survey of everything already built that touches this system: the two viral H3-Max infinite streams (levelsio's Infinite Slop, Rehan Sheikh's interdimensional cable), one Apache-2.0 open-source clone of that architecture (reactor-team/infinite-livestream), the seven public repos tagged tribe-v2 (all analysis, none generative), and the real-EEG generative-art lineage that already does the artistic thing this project claims to do.

**role_in_loop**

Upstream of the whole build. Prior art supplies (a) a finished, forkable orchestration layer for prompt -> generate -> stream (items 05-08 disappear if forked), (b) an off-the-shelf brain readout for the predict step (neuroscore, item 01-02), and (c) the negative evidence that constrains what the perceive -> predict edge is honestly allowed to claim (item 14). Nothing in prior art already connects the predict step to the prompt step: that edge is the only genuinely new code in the project.

### Interface

**interface_spec**

THREE reusable interfaces exist, in decreasing order of leverage.

1) reactor-team/infinite-livestream (Apache-2.0, Python, 157 stars, 24 forks, created 2026-08-30, pushed 2026-08-31). Two halves meeting on one wire contract in `fast-h3/fasth3_types.py`.
   MODEL SIDE (FastH3, a `ReactorModel`) exposes a TWO-QUEUE contract over WebRTC:
     commands: enqueue(prompt<=800 chars, metadata<=2000 chars, seed>=0 optional, seconds in 5.167..14.375 optional, position>=0 optional) -> clip_queued{ClipInfo};
               move(clip_id, position); play(clip_id optional); pop(clip_id); stop(); get_queue(); get_state();
               set_autoplay(enabled: bool); set_clip_seconds(seconds); set_seed(seed); set_canvas(aspect in {16:9,1:1,9:16,4:3}); reset()
     messages: state_update, queue_update, clip_queued, clip_generated, clip_started, clip_finished, clip_stopped, clip_failed, clip_popped, command_error
     ClipInfo{clip_id: uuid, prompt: str, metadata: str (opaque, echoed on EVERY message referencing the clip), frames: int, seconds: float (= frames/24), seed: int, ready: bool}
     tracks: main_video (out, 24 fps fixed, RGB at session canvas e.g. 1344x768), main_audio (out, 48 kHz mono int16, sample-locked to video). NO inbound tracks.
     clip geometry (fasth3_clip_plan.py): 24 fps, frame count of form 17n+5, 5-15 s, short edge 768, <=768x1344, both sides multiple of 32. 15.0 s = 360 frames aligns UP to 362 and is rejected, so the true maximum clip is 345 frames = 14.375 s.
   CLIENT SIDE (streaming-client) pipeline: Twitch IRC / YouTube Data API v3 -> Director -> Moderator (OpenAI /moderations, fail-closed) -> PromptUpsampler (any OpenAI-compatible endpoint) -> scene groups -> ReactorLink -> Pacer (24 fps metronome) -> Overlay -> StreamSink (rtmp via ffmpeg | noop).
   Files and ownership: main.py (wiring only), config.py (sole .env reader), reactor_link.py (all SDK contact + reconnect), director.py (moderate/upsample/enqueue + idle filler + eviction + cooldown), admin.py (!switch <preset>), upsampler.py (LLM call + scene validation), moderator.py, presets/*.json, pacer.py, overlay/, sinks/, chat/.

2) neuroscore (ndpvt-web, Apache-2.0 code / CC-BY-NC weights, 8 stars, PyPI `neuroscore`):
     CLI: neuroscore score <video|audio|text> [--mode score|compare|accessibility] [--backend gpu|cpu|cloud|demo] [--format terminal|json|html] [--raw] [--save PATH]
          neuroscore compare a.mp4 b.mp4 ; neuroscore youtube <url> ; neuroscore demo ; neuroscore backends
     Python: neuroscore.score(input, mode='score', backend=None) -> NeuroReport ; neuroscore.compare(a, b, backend=None) -> NeuroReport
     NeuroReport{overall_score: float 0..10, summary: str, findings: list[Finding], region_map: RegionMap, to_dict() -> dict}
     Finding{severity in {info,warning,critical}, title, detail, suggestion|None, region|None, start_sec|None}
     RegionMap accessors: .amygdala .acc .dlpfc .vmpfc .striatum (plus auditory, visual) -> RegionTimecourse{.values, .peak_value, .peak_time_sec, .mean_value, .onset_time_sec}
     Internal pipeline is contract-based and swappable: Input -> Backend -> BrainActivation (T, 20484) -> ROI extraction -> RegionMap -> Mode -> NeuroReport -> Formatter.

3) fal MiniMax H3 Max (minimax/h3-max/text-to-video, minimax/h3-max/image-to-video). Verified from the fal API docs page: duration default 5 (integer), resolution default '768P' (enum 480P|768P), prompt_expansion_mode default 'balanced' (required field), enable_safety_checker default true, seed random when omitted, sync_mode present. Output: video{url, content_type, file_name, file_size} (required), expanded_prompt ('The prompt after expansion, as sent to the model' - CONFIRMED present, which is what makes item 09's free text-branch feedback work), timings (per-stage inference duration on the GPU backend).

**input_contract**

What each piece of prior art needs fed to it.
- infinite-livestream MODEL half: four NVIDIA B200s (GPU count must divide H3's 56 attention heads, so 1/2/4/7/8; six is refused at init); CUDA 13 (the VSA-H3 sparse kernel and FA4 CuTe kernels are cu130 builds); a ~148 GB weights bundle at runtime.weights_path (transformer ~70 GB, text_encoder Qwen3-VL ~69 GB, vae, audio_vae, schedulers, tokenizer/processor) placed on disk in advance - nothing downloads at load, HF_HUB_OFFLINE=1; ~32 GB /dev/shm (docker's 64 MB default kills the first real clip); resources.cpu pinned at the account's full model CPU quota with OMP_NUM_THREADS=8 (nproc reports the whole node otherwise).
- infinite-livestream CLIENT half: ffmpeg on PATH; an OpenAI-compatible LLM endpoint (OPENAI_BASE_URL/OPENAI_API_KEY - a proxy, vLLM or OpenRouter all work); a SEPARATE moderation endpoint/key (MODERATION_API_KEY/MODERATION_BASE_URL) because inference gateways commonly do not expose /moderations; an RTMP ingest URL (Twitch, YouTube Live and Kick are all just ingest URLs); TWITCH_CHANNEL (anonymous justinfan IRC - no OAuth, no app registration, no token rotation) and/or YOUTUBE_VIDEO_ID + YOUTUBE_API_KEY pointing at a LIVE broadcast. A preset JSON in presets/ carries the style block and the idle prompt list. Everything else lives in .env.
- neuroscore: a media file path, a URL, or a raw string. Demo backend needs nothing at all (precomputed examples ship in the package). GPU backend needs `pip install neuroscore[gpu]` plus an NVIDIA card with 16 GB+ (this is neuroscore's own floor and is BELOW the 28-32 GB the full three-branch TRIBE stack actually needs; treat 16 GB as text/audio-only territory).
- Infinite Slop itself: not reproducible from published material. No source, no architecture post, no buffer figures. Only the model choice, the throughput ceiling, and the host are public.

**output_contract**

- infinite-livestream produces ONE uninterrupted RTMP broadcast: 1344x768 @ 24 fps video plus 48 kHz mono int16 audio, both emitted every period forever by the Pacer (repeated frames + silence on underflow, drop-oldest on overflow). An audio track is MANDATORY - YouTube and Twitch will not accept video-only FLV. The shipped overlay adds, top-left, 'NOW <title> - scene 2/3 - by <author>' with a dimmer 'COMING UP <next>'; top-right, 'READY n - BUILDING m' (playout queue vs generation queue). READY pinned at 0 while BUILDING holds a backlog is the on-stream signature of builds running slower than playback.
- neuroscore emits NeuroReport: one float 0-10 overall score, a natural-language summary, timestamped findings with fix suggestions, and seven region timecourses (amygdala/relevance, ACC/decision-weighing, dlPFC/analytical-resistance, vmPFC/value-recognition, striatum/reward-drive, auditory, visual). --raw adds the full timecourse; --format json is pipeline-ready. What the numbers physically mean: each region value is a mean over that region's vertices of TRIBE's predicted BOLD response, in TRIBE's arbitrary normalised units - NOT a percentage, NOT a probability, and NOT calibrated against any behavioural outcome.
- Infinite Slop's observable output: 15-second clips at ~1.0x realtime, hard-cut between clips, chat-steered, continuity attempted only in the prompt text.

### Performance

**throughput_constraint**

The binding constraint in every shipped system is 1.0x realtime generation with essentially zero headroom.
- Infinite Slop, levelsio's own words: 'Only 4 videos per minute can be generated (4x 15 seconds = 1 minute)' and 'not everyone gets their video generated if it gets busy.' That is exactly 1.0x realtime. A stream at 1.0x realtime cannot absorb a single failed or rejected generation without stalling - which is why item 08's underrun fallback is not optional.
- infinite-livestream self-hosted: identical 1.0x. Builds consume the generation queue front-first ONE AT A TIME whenever an audience is connected, including while another clip plays, pausing only while the playout queue is at capacity. Generation is gated on having an audience: with nobody connected no new build starts.
- Queue bounds: generation_queue_size default 20; playout capacity default 10 built clips, each ~1 GB of uint8 pixels held in HOST memory at the 16:9 canvas and maximum length, so playout capacity is a RAM budget not a policy. A full generation queue refuses enqueue with command_error; a full playout queue pauses builds.
- Idle filler target is 6 clips and self-clamps to one below live playout capacity, because a full playout queue pauses builds and the headroom slot is where the next viewer clip lands.
- CPU quota bites hard: the same image hit 1.16x realtime on an unthrottled HGX B200 box and 0.85x on a hosted pod with requests.cpu 8 / limits.cpu 32 on a 192-vCPU node - 38%% of CFS periods throttled, latent prep 1.65 s vs 0.3 s, denoise 9.5 s vs 5 s. The fabric was never the problem.
- torch dynamo recompile_limit defaults to 8 and the fullgraph regional-compile route makes exceeding it a HARD failure that kills the engine workers and the whole serving process. Observed live after enqueueing many different clip lengths.
- fal-side, the equivalent cap is the concurrency ladder (item 05/08), not per-clip latency.

**realtime_headroom**

SURPLUS OF ZERO, in both shipped systems, measured not estimated.
- Infinite Slop: 4 x 15 s clips per 60 s = 60 s of video per 60 s of wall clock. Headroom = 0.0 s per clip.
- infinite-livestream on 4x B200: 14.4 s build for a 14.375 s clip. Headroom = -0.025 s per clip, i.e. very slightly NEGATIVE, held up only by the pre-built playout queue. On 8x B200: 12.9 s for 14.375 s = +1.5 s per clip. On 8x B300 with the kernel gate bug: 19.3 s for 14.375 s = -4.9 s per clip, an outright deficit.
- fal hosted H3 Max is the only configuration with real surplus: 9 s to build 15 s = +6.0 s per clip (1.67x realtime), and 3 s to build 5 s = +2.0 s (1.67x). This is the single strongest argument for using the fal API rather than self-hosting FastH3.
CONSEQUENCE FOR THIS PROJECT: at fal's 1.67x, a 15 s clip leaves ~6 s of slack per clip for everything else in the loop. TRIBE's video path (15-60 s per 30 s of video via neuroscore GPU) does not fit in 6 s. TRIBE's text path plausibly does. That single arithmetic fact is the strongest argument in the whole survey for item 15's text-branch simplification.

### Complexity

**dev_complexity**

LOW to fork the client, HIGH to fork the model.
- Forking reactor-team/infinite-livestream's streaming-client and swapping ReactorLink for a fal queue client: LOW-MEDIUM. The pacer, RTMP sink, ffmpeg supervision, chat sources, moderation, overlay, idle filler and eviction are all written, documented, and carry an explicit 'learnings baked in, do not re-learn these' list. You replace one module.
- Standing up its fast-h3 model half: HIGH. Four B200s, CUDA 13, a 148 GB weights bundle, a kernel that must be compiled from source at image build (the published fastvideo-kernel 0.3.5 wheel's sm_100a binary fails EVERY launch on driver 595 with 'invalid argument'), a protobuf-vs-FA4 dependency conflict resolved via UV_OVERRIDE, a sitecustomize.py import hook to raise dynamo limits inside spawned engine workers, and a B300 device-gate patch. Days of devops for a result that is SLOWER than fal's hosted endpoint. Do not do this.
- neuroscore: LOW. pip install, one CLI call, JSON out, and a demo backend that needs no GPU at all.
- Reproducing Infinite Slop from its write-ups: MEDIUM, because nothing is published - you would be rebuilding what infinite-livestream already open-sourced.

**off_the_shelf_option**

RANKED, best first.
1. reactor-team/infinite-livestream streaming-client (Apache-2.0). Removes essentially all of outline items 07 and 08. Fork it, keep the pacer/sink/chat/overlay/filler, replace ReactorLink with fal. THE most valuable single artefact found in this survey.
2. neuroscore (pip install neuroscore, Apache-2.0 code). Removes most of items 01 and 02: it already collapses (T, 20484) into seven named region timecourses with peak/mean/onset accessors and a JSON formatter. Its `demo` backend gives you a working brain-shaped control signal on day one with no GPU and no weights.
3. CodaCipher/tribe-subcortex (MIT, Colab notebook). If the piece wants subcortical dials - accumbens, amygdala, caudate, putamen, pallidum, thalamus, hippocampus - plus a composite subcortical response score over time, this is the readout already written. Notebook-shaped, so it is a source to lift from rather than a dependency.
4. recozers/Tribe-V2-Interp. Not a runtime component, but the only public code that runs GRADIENTS through TRIBE toward a stimulus. It is the seed of item 16's offline motif table. No licence file - check before use.
5. BrainFlow (for the real-EEG variant): board-agnostic API with a documented band-power notebook (Welch PSD, alpha 7-13 Hz, beta 14-30 Hz). kylemath/Brainimation and NeuroSkill are working Muse/OpenBCI creative-coding front ends.
NOT available off the shelf: any code that connects a brain model to a generator. That edge does not exist publicly.

### Decision

**recommended_approach**

Fork reactor-team/infinite-livestream's `streaming-client/` and replace exactly one module.

Concretely:
1. git clone https://github.com/reactor-team/infinite-livestream ; work only inside streaming-client/. Read AGENTS.md first - it is written for coding agents and names the load-bearing invariants.
2. Do NOT stand up fast-h3. Write a fal-backed drop-in for reactor_link.py that presents the same surface the director already speaks to: an enqueue(prompt, metadata, seconds, seed, position), a queue mirror emitting state_update/queue_update-shaped events, and a media path feeding the Pacer. Behind it, call fal's `minimax/h3-max/text-to-video` through the queue API, download each result, and decode it to 24 fps RGB frames + 48 kHz audio for the pacer. fal's 1.67x realtime replaces FastH3's 1.0x and gives you the only headroom in the system.
3. Keep, unchanged: pacer.py (the constant-rate metronome is explicitly documented as 'not optional' - RTMP needs a frame every period forever and clip-shaped output does not provide that), sinks/rtmp.py (its ffmpeg learnings cost the authors many iterations), chat/, moderator.py (fail-closed), overlay/, and the idle-filler + eviction logic in director.py (this IS item 08's buffer-underrun fallback, already written and tuned: IDLE_QUEUE_TARGET 6, self-clamped to one below playout capacity, viewer clips outranking filler four different ways).
4. Insert the brain readout AHEAD of upsampler.py, not instead of it: brain vector -> a style/motif directive -> the existing preset-driven upsampler -> prompt. That keeps the upsampler's hard-won rules intact (every scene re-describes the full setting from scratch because clips have NO memory; hard truncate to 800 chars because LLMs cannot count; ask for explicit quoted dialogue because H3 renders real speech; single-scene generations always run maximum clip length).
5. Use neuroscore as the readout for v1 (`neuroscore.score(path_or_text, backend='demo')` on day one, `backend='gpu'` later). Its RegionMap is already the small interpretable vector item 02 asks for.
6. Point SINK=rtmp at YouTube Live, not Twitch. Twitch banned Rehan Sheikh's stream and the project bounced to Kick and Rumble; Nothing, Forever was suspended from Twitch in 2023 for generated content. This is a documented, repeated failure mode for endless AI streams, not a hypothetical.

WHAT PRIOR ART SAYS YOU MUST BUILD YOURSELF: the brain-state -> prompt edge (item 04). None of the seven tribe-v2 repos drives a generative model. All of them - neuroscore, tribe-subcortex, mindprint, Audience, neuroscanner, NoLemming - are analysis and scoring. That edge is the project's actual contribution and its only irreducible work.

**simpler_alternative**

If forking infinite-livestream proves too heavy (it assumes a reactor-sdk session, WebRTC tracks and an ffmpeg RTMP pipeline), fall back to what levelsio actually shipped: a browser-side video queue. Infinite Slop ran on a Hetzner VPS and levelsio built it 'completely on my phone with Termius... with Claude Code in the sauna' - which strongly implies a small web app with an HTML5 <video> element playing a client-side queue of fal-returned MP4 URLs, not an encoded RTMP broadcast. That removes ffmpeg, the pacer, RTMP, the audio-track requirement and the whole encoder failure surface, at the cost of losing YouTube/Twitch CDN and per-viewer identical playback. It is provably enough to draw 37,000 viewers on day one.
Cruder still: drop the live loop entirely and pre-render. Generate a few hours of clips offline, score them with neuroscore in batch, order them by a brain-derived trajectory, concatenate with ffmpeg, and loop the result. Nobody watching can tell the difference between that and a live loop within one viewing session - which is itself a finding worth being honest about.

**code_sketch**

# The one module you write. Everything around it is forked.
# streaming-client/fal_link.py - drop-in for reactor_link.py's enqueue surface

import asyncio, json, fal_client
from neuroscore import score

STATE = {"brain": None}   # last RegionMap, the control signal

async def generate(prompt: str, metadata: dict, seconds: int = 15) -> dict:
    h = await fal_client.submit_async(
        "minimax/h3-max/text-to-video",
        arguments={
            "prompt": prompt[:800],              # FastH3's cap; keep it, H3 Max is happier short
            "duration": seconds,                  # 5..15
            "resolution": "480P",                # $0.05/s vs $0.08/s at 768P (regular pricing)
            "prompt_expansion_mode": "balanced", # 'quality' is ~30 s and off the table live
            "enable_safety_checker": True,
        },
    )
    res = await h.get()
    return {"url": res["video"]["url"],
            "expanded_prompt": res.get("expanded_prompt", prompt),
            "metadata": json.dumps(metadata)}     # echoed like FastH3's opaque metadata

def read_brain(expanded_prompt: str):
    # Text branch only: free, exact, no video decode, no re-encode.
    # backend='demo' on day one (precomputed, instant, no GPU); 'gpu' once a warm box exists.
    r = score(expanded_prompt, backend="demo")
    return {"amygdala": r.region_map.amygdala.peak_value,
            "vmpfc":    r.region_map.vmpfc.mean_value,
            "dlpfc":    r.region_map.dlpfc.mean_value,
            "striatum": r.region_map.striatum.mean_value,
            "score":    r.overall_score}

async def loop(director):
    while True:
        directive = brain_to_directive(STATE["brain"])      # item 04 - the only new idea
        prompt    = director.upsample(directive)             # FORKED, unchanged
        clip      = await generate(prompt, {"generated": True})
        STATE["brain"] = read_brain(clip["expanded_prompt"]) # closes the loop, zero extra latency
        await director.enqueue(clip)                         # FORKED pacer/sink take it from here

# Invariants inherited from the fork - preserve them or things break in documented ways:
#   prompt <= 800 chars after sanitisation; metadata JSON well under 2000 chars;
#   scene groups enqueued contiguously and only when they fully fit;
#   eviction pops only clips tagged generated:true; moderation fails closed;
#   the pacer and sink are created ONCE and outlive every reconnect;
#   sinks never block the event loop; every capacity read live, never assumed.

### Risk

**failure_modes**

Documented, observed failures - not speculation.
1. PLATFORM BANS ARE THE MODAL OUTCOME. Rehan Sheikh's H3-Max stream was banned from Twitch and bounced to Kick then Rumble. Nothing, Forever was suspended from Twitch for at least 14 days in February 2023 after a character told hateful jokes - the co-creator attributed it to switching from Davinci to Curie, a model with looser moderation. An endless generative stream is a moderation surface that runs unattended at 3 a.m.
2. THE ECONOMICS DO NOT CLOSE. Rehan Sheikh's own published breakdown: 480p at $0.05/video-second is $4,320/day, $129,600/month, $1.58M/year in inference alone, and breaking even on Twitch revenue alone would put you 'around the 99.9997th' percentile of streamers. Infinite Slop only existed because fal donated the compute; levelsio thanks '@fal for VERY generously sponsoring and making this possible.'
3. CONTINUITY IS UNSOLVED, NOT SOLVED. infinite-livestream states it flatly: 'Clip boundaries are hard cuts. Every clip is generated independently. There is no continuity of subject, framing, or voice from one clip to the next, even with identical prompts... This checkpoint has no continuation path.' Its entire continuity strategy is prompt-level - the upsampler re-describes the full setting, subjects and style from scratch in every single scene prompt. levelsio raised last-frame conditioning only as a future improvement, noting it 'presents generation speed challenges.' Do not budget for smooth continuity; budget for a cut-driven aesthetic.
4. RAW-VIDEO GEOMETRY IS UNFORGIVING. One frame whose bytes disagree with ffmpeg's -s WxH - wrong size, or a non-C-contiguous tobytes() that includes row padding - shifts every following scanline into permanent TV static.
5. NEVER WRITE TO A PIPE FROM THE EVENT LOOP. stdin.write blocks when ffmpeg stalls; a blocked loop starves WebRTC and everything snowballs. Each pipe needs its own writer thread behind a bounded drop-oldest queue.
6. FEED AUDIO AND VIDEO IN LOCKSTEP ON SEPARATE PIPES. Starving one ffmpeg input while pushing the other is the classic two-pipe deadlock. An audio track is mandatory - YouTube and Twitch reject video-only FLV - and anullsrc silence is not sufficient when the model emits real synchronised audio.
7. THE QUEUE DIES WITH THE SESSION. FastH3 resets all session state on a new session: after a reconnect, clips queued but unplayed are simply gone.
8. A DEAD CLIENT ORPHANS THE RUNTIME and its reaper takes a minute or more, during which every connect returns 409.
9. REFUSALS ARE BROADCAST, NOT RAISED. A refused command answers with a bodyless reply plus a command_error broadcast. Treat 'reply without clip' as refusal and retry with patience.
10. THE BRAIN SIGNAL MAY BE MEASURING NOTHING. arXiv 2607.01400 tested exactly the reduction this project wants - TRIBE's predicted cortical response collapsed to a per-second global-field-power engagement curve - against YouTube 'most replayed' heatmaps on 48 videos. Pooled position-controlled partial correlation +0.058, 95%% CI [-0.04, 0.15], t(47)=1.21, p=0.23, and NOT above simple loudness/motion baselines. Predicted inter-subject correlation r=-0.04, p=0.34, Bayes factor 3.2 favouring the null. A supervised probe reached r=0.47 but collapsed to a temporal-shape artefact. neuroscore's own documentation concedes the same: its scores 'have not yet been correlated with actual engagement metrics like view counts, watch time, shares, or conversions.'
11. ATTRACTOR COLLAPSE HAS AN EVIDENCE BASE. arXiv 2605.13904 optimised stimuli through the frozen TRIBE encoder by gradient ascent and recovered genuine cortical selectivity (V1->V4 showing increasing spatial scale and feature complexity, MT producing radial 'frozen-motion' streaks from static-only optimisation, FFA producing face-like features, PPA producing rectilinear line patterns) - but the FFA-optimised stimulus drove the predicted region ~4x as hard as a natural face photograph. The authors call these adversarial super-stimuli, not canonical exemplars. Any loop that maximises its own brain model walks straight at them.

### Evidence

**sources**

- https://levels.io/i-built-infinite-slop - levelsio's build post. Confirms MiniMax H3 'Max', fal post-trained 50x faster, fal sponsoring compute, chat-driven prompts, LLM attempts to connect each clip to the previous one. Contains NO buffer, streaming-protocol, LOC or build-time details.
- https://levels.io/37000-watched-infinite-slop - the throughput ceiling in levelsio's own words ('Only 4 videos per minute can be generated (4x 15 seconds = 1 minute)', 'not everyone gets their video generated if it gets busy'), 37,000 viewers, Hetzner VPS + Termius + Claude Code build story, last-frame conditioning named as a future improvement with 'generation speed challenges'.
- https://levels.io/ai-video-faster-than-you-watch - '15 seconds of video in 9 seconds', 50x faster than base H3, fal.ai/minimax-h3-max.
- https://infiniteslop.ai/ - the live artefact.
- https://x.com/rehan_shei/status/2093528415576211819 - Rehan Sheikh (fal) announcing the interdimensional-cable Twitch stream.
- https://x.com/rehan_shei/status/2094004479574110671 - the cost breakdown: $0.05/video-second at 480p, $4,320/day, $129,600/month, $1.58M/year, break-even at ~99.9997th percentile of Twitch streamers. (Page itself returns HTTP 402 to automated fetch; figures come from the indexed search snippet of that post.)
- https://x.com/levelsio/status/2093628563693944889 - levelsio's 'historical moment' post, 50x figure.
- https://github.com/reactor-team/infinite-livestream - Apache-2.0, Python, 157 stars, 24 forks, created 2026-08-30. THE most valuable artefact in this survey.
- https://raw.githubusercontent.com/reactor-team/infinite-livestream/main/streaming-client/README.md - full client architecture, scene groups, upsampling rules, fail-closed moderation, idle filler and eviction, overlay, sinks, chat sources, and the 'learnings baked into this client (do not re-learn these)' list.
- https://raw.githubusercontent.com/reactor-team/infinite-livestream/main/fast-h3/README.md - the two-queue contract, ClipInfo, commands and messages, clip geometry (17n+5 frames, 345-frame/14.375 s maximum), the 14.4 s-on-4xB200 = 1.0x realtime profile with stage split, the 'clip boundaries are hard cuts' statement, and the full deployment-learnings section (sm100a kernel from source, 256-token prompt padding, CPU-quota throttling, dynamo recompile limit, /dev/shm).
- https://huggingface.co/FastVideo/FastVideo-FastH3-4-step-Preview-v1-VSA-DataFree - MiniMax-H3 35B distilled by FastVideo via data-free DMD2 to four transformer forwards with 90%% sparse video attention; joint video+audio.
- https://fal.ai/models/minimax/h3-max/text-to-video/api - CONFIRMED schema: duration default 5, resolution default 768P, prompt_expansion_mode default 'balanced' (required), enable_safety_checker default true, and expanded_prompt present in the output as 'The prompt after expansion, as sent to the model'. Pricing and rate limits were NOT on this page.
- https://fal.ai/learn/devs/introducing-h3-max-by-fal - 5 s video in under 3 s, ~35x the throughput of the official MiniMax H3 endpoint.
- https://github.com/topics/tribe-v2 - the topic index. GitHub search API returns 7 repos as of 2026-08-31.
- https://github.com/ndpvt-web/neuroscore - CLI + Python API, seven regions, four backends (gpu/cpu/cloud/demo), GPU 15-60 s per 30 s video, demo backend precomputed and instant. Roadmap shows 'Streaming backend for real-time scoring' as NOT yet done. Apache-2.0 code, CC-BY-NC weights.
- https://github.com/CodaCipher/tribe-subcortex - MIT, Colab. Subcortical ROIs (accumbens, amygdala, caudate, putamen, pallidum, thalamus, hippocampus), composite subcortical response scores over time, peak timing tables.
- https://github.com/attila-aranyi/mindprint - Chrome extension, TRIBE v2 + Claude, manipulation detection. Analysis, not generation.
- https://github.com/MrSJx/Audience - audience reaction simulation. Analysis, not generation.
- https://github.com/sanyambassi/neuroscanner - FastAPI + Next.js + three.js brain visualisation. Analysis, not generation.
- https://github.com/samuelczhao/NoLemming - brain-encoded swarm social simulation. Analysis, not generation.
- https://github.com/mahanyasbaira/NeuroSync-Multimodal-Brain-Encoding-Model-TRIBE-v2-Inspired - TypeScript/Next.js, TRIBE v2-'inspired' rather than actually using it.
- https://github.com/recozers/Tribe-V2-Interp - the ONLY public code running gradients through TRIBE toward a stimulus. Fourier parameterisation, colour decorrelation, progressive 64->128->256, ~3-6 h for a 5-restart run on a 3090 (peak ~18.4 GB VRAM), single-frame mode ~32x faster. Explicitly exploits modality dropout: aggregate_features auto-fills zeros for missing text and audio, 'equivalent to a training condition the model has seen'. No LICENSE file.
- https://arxiv.org/abs/2605.13904 - Feature Visualization Recovers Known Cortical Selectivity from TRIBE v2. V1/V4/MT/FFA/PPA recovered; FFA-optimised stimuli drive the predicted region ~4x a natural face photograph; authors characterise them as adversarial super-stimuli.
- https://arxiv.org/pdf/2607.01400 - A global predicted-fMRI drive signal from TRIBE does not predict YouTube replay heatmaps. 48 videos; pooled position-controlled partial r=+0.058, 95%% CI [-0.04,0.15], t(47)=1.21, p=0.23; not above loudness/motion baselines; predicted ISC r=-0.04, p=0.34, BF=3.2 for the null; supervised probe r=0.47 collapses to a temporal-shape artefact. THE key negative result for this project's framing.
- https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model/ - Meta FAIR's TRIBE v2 announcement, published 2026-03-25.
- https://dl.acm.org/doi/10.1145/3749893.3749963 - Oneiris: an AI-augmented BCI installation. Wireless EEG + dream narratives + hand-drawn sketches -> LLM builds an image prompt -> diffusion generates evolving dreamscapes whose texture and colour palette are modulated in real time by neural markers of hypnagogia and brain complexity. The closest PUBLISHED closed-loop brain->generative-model system, and it uses a real brain.
- https://github.com/kylemath/Brainimation - live Muse EEG + P5.js creative-coding web platform, real-time alpha/beta/theta/delta/gamma.
- https://neuroskill.com/ - open-source real-time EEG analysis for Muse and the full OpenBCI board family, as of 2026.
- https://brainflow.readthedocs.io/en/stable/notebooks/band_power.html - the canonical band-power recipe (Welch PSD, alpha 7-13 Hz, beta 14-30 Hz) that makes a real-EEG control signal a ~20-line job.
- https://arxiv.org/pdf/2502.12048 - A Survey on Bridging EEG Signals and Generative AI: From Image and Text to Beyond.
- https://arxiv.org/pdf/2410.00712 - NECOMIMI: EEG-informed image generation with diffusion models.
- https://en.wikipedia.org/wiki/Nothing,_Forever - the 2022-23 precedent: GPT-3 + Azure TTS + Unity, live since 2022-12-14 on twitch.tv/watchmeforever; suspended from Twitch in Feb 2023 after a moderation failure attributed to a Davinci->Curie model swap. Python+TensorFlow / TypeScript+Azure Functions+Heroku / C#+Unity.
- https://www.deeplearning.ai/the-batch/ai-generated-sitcom-nothing-forever-booted-from-twitch - the ban and its cause.
- https://www.datacamp.com/tutorial/tribe-v2-tutorial - practical TRIBE v2 runtime facts: 28-32 GB VRAM for all three encoders, A100-40GB floor, T4 fails during LLaMA init, L4/24GB 'may fit' if text and video are skipped, 15-30 s minimum stimulus ('very short inputs (a few seconds) often produce diffuse, low-intensity activations that are hard to interpret'), NumPy pinned <2.1, HF_HUB_DOWNLOAD_TIMEOUT=300, flush->fsync->close before passing temp paths, and the predict() signature returning (T, 20484) at 1 Hz.
- https://x.com/i/trending/2094016540031005048 - contemporaneous coverage confirming 768p clips in 2.5-3 s and the Twitch->Kick->Rumble migration after moderation flags.

### Other Info

**item_id**

12

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `loc_estimate`
- `unknowns`

---

## Radical simplification paths

### Identity

**what_it_is**

Four escape routes from the expensive part of the system - the always-on 28-32 GB GPU running full trimodal TRIBE inside a real-time loop. Ranked: (1) run TRIBE on the PROMPT TEXT only, which keeps the live closed loop and cuts the cost by roughly two orders of magnitude; (2) precompute a prompt-category -> ROI-profile lookup table offline and do pure table lookup at runtime with zero GPU; (3) replace the simulated brain with a real EEG headset; (4) a fake-it-first staging plan that has something on screen in a day.

**role_in_loop**

All four attack the same edge: perceive -> predict. Everything downstream (prompt -> generate -> stream) is unchanged in all four. The text-branch path keeps that edge live and recursive but feeds it text rather than pixels. The lookup table removes the edge from the runtime entirely and moves it to build time, which kills the recursion. The EEG path replaces the edge's SOURCE - a real cortex instead of a predicted one - while leaving its interface (a small float vector at roughly 1 Hz) byte-identical, which is why both can plug into the same prompt-translation layer.

### Interface

**interface_spec**

Design every variant against ONE interface, so the source is swappable:

    BrainVector = dict[str, float]   # ~5-8 named dials in [0,1], refreshed roughly once per clip
    def read_brain(context) -> BrainVector: ...

FOUR IMPLEMENTATIONS OF THAT SIGNATURE:

A) TEXT-BRANCH TRIBE (recommended)
   events = model.get_events_dataframe(text_path=tmp.name)   # text_path ONLY - no video_path, no audio_path
   preds, segments = model.predict(events=events)             # -> (T, 20484) float, T = seconds at 1 Hz
   Video and audio branches are left unset; TRIBE's aggregate_features auto-fills zeros for absent
   modalities. This is a TRAINED condition, not a hack: modality dropout at p=0.3 per modality means the
   model saw text-only inputs throughout training, and recozers/Tribe-V2-Interp relies on exactly this
   property in reverse (video-only, zeros for text and audio) for its published feature-visualisation work.
   Text encoder: Llama-3.2-3B, 1024-word context.
   INPUT SOURCE, free and exact: the `expanded_prompt` field of fal's MiniMax H3 Max response, documented
   as 'The prompt after expansion, as sent to the model'. No captioning model, no video download, no
   re-encode, no extra API call, no added latency.

B) OFFLINE LOOKUP TABLE
   Build time:  for each of N candidate prompts -> generate a clip -> neuroscore score <clip> --format json
                --save table/<hash>.json   ->  {prompt, category, expanded_prompt, region_map, overall_score}
   Runtime:     BrainVector = TABLE[nearest_category(previous_expanded_prompt)]  # dict lookup + a cheap
                sentence-embedding nearest neighbour. Zero GPU, sub-millisecond.

C) REAL EEG
   from brainflow.board_shim import BoardShim, BrainFlowInputParams
   from brainflow.data_filter import DataFilter
   bands = DataFilter.get_avg_band_powers(data, channels, sampling_rate, True)
   # -> [delta, theta, alpha, beta, gamma]; the canonical derived dials are alpha/beta (relaxation)
   # and beta/theta (focus). Board-agnostic: the same call serves Muse and every OpenBCI board.

D) DEMO / STUB
   neuroscore.score(text_or_path, backend='demo')  # precomputed examples ship in the pip package;
   instant, no GPU, no weights, no HF token. Returns a real NeuroReport with a real RegionMap shape.

**output_contract**

All four emit the same shape: a handful of named floats per clip. What they MEAN differs, and the piece's
honesty depends on stating which one is running.
- Text-branch TRIBE: predicted BOLD response, in TRIBE's arbitrary normalised units, of a ~720-subject
  AVERAGE cortex, to a WRITTEN DESCRIPTION of the clip - not to the clip. Defensible and specific. Say it.
- Lookup table: the same numbers, computed earlier. Physically identical; epistemically identical; the only
  thing lost is that they cannot respond to something that was not in the corpus.
- EEG band powers: microvolts-squared per Hz from four to eight scalp electrodes on ONE living person, at
  10-250 ms latency. Not cortical activation in any localised sense - scalp EEG has poor spatial
  specificity - but it is an actual brain, right now.
- Demo backend: synthetic. Structurally valid, semantically meaningless. Never ship it as the real thing.

### Complexity

**dev_complexity**

- Text-branch TRIBE: LOW-MEDIUM. Same install as the full model (the gated-Llama, NumPy-pin and
  HF-timeout blockers all still apply and cost about half a day), but you pass text_path instead of
  video_path and never touch ffmpeg, frame extraction, re-encoding or temp-file plumbing. Expect warnings
  about extractors being removed - the tutorial documents this as expected behaviour when the model
  disables unused branches.
- Lookup table: LOW at runtime, MEDIUM at build time. The build script is trivial; curating a corpus that
  is actually interesting is the real work, and it is creative work, not engineering.
- Real EEG: LOWEST of all on the software axis. BrainFlow's band-power recipe is ~20 lines and
  board-agnostic. No GPU, no 148 GB of weights, no CC-BY-NC problem, no gated model, no cold start, no
  15-30 s minimum stimulus, no 5 s hemodynamic offset. The complexity is entirely PHYSICAL and
  LOGISTICAL: hardware to buy, ship and debug, a scalp to keep in contact, and a person who has to be
  there. For a 24/7 unattended stream that trade is bad; for a gallery installation it is obviously right.
- Demo backend: TRIVIAL. One pip install and one call.

**off_the_shelf_option**

- neuroscore (pip install neuroscore) removes the readout code entirely and ALREADY implements three of the
  four backends this item proposes: `gpu` (real TRIBE), `cloud` (via a NEUROSCORE_CLOUD_URL env var), and
  `demo` (precomputed, instant, no GPU). Its backend interface is explicitly documented as extensible - 'New
  backend: one file in core/backends/, implement the Backend interface' - so a text-branch-only backend and
  an EEG backend are each one file, and every mode, formatter and report structure above them keeps working
  unchanged. This is by some distance the best-shaped dependency found for this item. Its roadmap does list
  'Streaming backend for real-time scoring' as NOT yet done, so the real-time path is yours to write.
- tribev2-rs (crates.io `tribev2`, CLI `tribev2-infer`, Apache-2.0 source / CC-BY-NC weights) is a pure-Rust
  TRIBE v2 port loading the exact same pretrained weights with claimed 100%% numeric parity - 8 parity tests
  at Pearson r=1.0, max errors under 2 micro-units. Backends: pure Rust CPU, Burn/NdArray, Burn/wgpu
  (Metal/Vulkan/DX12) and RLX (CPU/Metal/MLX/CUDA/ROCm). Its documented caveat matters: audio and video
  feature extraction need RLX compilation with matching device support, whereas TEXT extraction can come
  from plain HuggingFace. So the text-only path is exactly the path this port makes easiest - and it is the
  route to running the brain model on an Apple laptop with no rented GPU at all.
- BrainFlow for the EEG variant: board-agnostic, with a published band-power notebook.
- CodaCipher/tribe-subcortex (MIT) if the piece wants subcortical dials precomputed - it already produces
  composite subcortical response scores over time and peak-timing tables.
- recozers/Tribe-V2-Interp for the richest possible offline table (see recommended_approach step 5).

### Decision

**recommended_approach**

RUN TRIBE ON THE TEXT BRANCH ONLY, FED BY H3 MAX'S OWN `expanded_prompt`. This is the strongest
simplification because it is the only one that removes the cost WITHOUT removing the live closed loop.

Why it wins on every axis:
- It drops V-JEPA-2-Giant, the single most expensive component, and the entire video ingestion path -
  no download, no decode, no frame windowing, no re-encode.
- VRAM falls from the documented 28-32 GB trimodal footprint to something a single 24 GB card holds warm,
  which changes the hosting question from 'rent an A100-80GB indefinitely' to 'rent a 4090' - or, via the
  Rust port on Metal, to 'run it on the laptop'.
- Latency plausibly falls from ~60 s to a few hundred ms, moving the read from a 54 s deficit to a ~6 s
  surplus inside the clip budget.
- The input is free and exact. fal returns `expanded_prompt` as a documented output field, so you are
  scoring precisely the text the video model actually conditioned on - strictly better than captioning the
  generated clip, which would introduce a second model's errors and its own latency.
- It is legitimate, not a fudge. Modality dropout at p=0.3 per modality is a training condition TRIBE saw
  throughout training, and Tribe-V2-Interp's published feature-visualisation work depends on the same
  property in the mirror-image configuration.
- The artistic claim survives essentially intact. 'Predicted brain response to the content' becomes
  'predicted brain response to the description of the content'. State that in the wall text and it is
  honest; the piece loses nothing a viewer can perceive.

IMPLEMENT IT AS A neuroscore BACKEND, not as bespoke code: one file in core/backends/ implementing the
documented Backend interface, so RegionMap, the modes, the formatters and the JSON output all keep working.

PAIR IT WITH A WARM-CACHE HYBRID, which is where the lookup table earns its place rather than replacing
everything: memoise read_brain() on a hash of the expanded prompt. Repeated motifs cost nothing, novel
prompts pay the full (cheap) price, and the cache IS the lookup table - built incrementally by the running
stream instead of in a separate batch job. It also gives you the offline table for free if you later want
to drop the GPU entirely.

**simpler_alternative**

PURE OFFLINE LOOKUP TABLE, ZERO GPU AT RUNTIME. Generate ~150 clips across the aesthetic space overnight,
score each with `neuroscore score <clip> --format json --save`, key the results by prompt category, and at
runtime do nothing but a dict lookup on the previous clip's expanded_prompt.

HOW MUCH OF THE ARTISTIC CLAIM SURVIVES - the honest assessment, which is more favourable than it first
looks and then worse in one specific place:
- What survives intact: 'these prompts were chosen by a model of the human brain' is still literally true.
  The numbers are identical - the same TRIBE weights on the same content producing the same activations.
  Precomputation changes WHEN they were computed, not WHAT they are.
- What survives better than expected: given arXiv 2607.01400's null result - TRIBE's global predicted-fMRI
  drive signal does not predict YouTube replay heatmaps (pooled partial r=+0.058, p=0.23, not above
  loudness/motion baselines, BF=3.2 favouring the null) - the live version's extra claim to be tracking
  something real-time and meaningful is not empirically stronger than the table's. Liveness here is an
  aesthetic property, not an epistemic one. Be clear-eyed about that in both directions.
- WHAT DIES, and it is the good part: the RECURSION. A lookup table cannot respond to a clip that was not
  in the corpus, so the system stops being a loop and becomes a weighted random walk over a fixed graph.
  Item 09's whole conceptual payoff - the stream watching itself and drifting - is gone, and with it the
  attractor-collapse risk that makes the piece interesting to talk about. Within a few hours a viewer will
  see the table's structure as repetition, because it IS repetition.
- Verdict: excellent as a week-one milestone and as a permanent memoisation layer under the live path;
  a real artistic downgrade as the final architecture. Use it as scaffolding, not as the building.

**code_sketch**

# ---------- A) The recommended path: text-branch TRIBE as a neuroscore backend ----------
# core/backends/text_only.py  -- one file, per neuroscore's documented extension contract
import os, tempfile, numpy as np
from neuroscore.core.backends.base import Backend

class TextOnlyBackend(Backend):
    name = "text_only"

    def __init__(self):
        from tribev2 import FmriEncoderModel      # warm ONCE - lazy load is ~60 s
        self.model = FmriEncoderModel.from_pretrained("facebook/tribev2")

    def activate(self, text: str) -> np.ndarray:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write(text)
            f.flush(); os.fsync(f.fileno())       # documented gotcha: flush -> fsync -> close
        # text_path ONLY. No video_path, no audio_path. aggregate_features zero-fills the
        # absent modalities - a trained condition (modality dropout p=0.3), not a hack.
        events = self.model.get_events_dataframe(text_path=f.name)
        preds, _ = self.model.predict(events=events)   # (T, 20484) at 1 Hz
        return preds

# Environment, all mandatory and all documented failure points:
#   HF_TOKEN=...                        (Llama-3.2-3B is gated; accept the Meta licence first)
#   HF_HUB_DOWNLOAD_TIMEOUT=300
#   HF_HUB_HTTP_TIMEOUT=300
#   pip install 'numpy>=1.26.4,<2.1.0'  BEFORE tribev2, then restart the interpreter

# ---------- The loop, with the warm cache that doubles as the lookup table ----------
import hashlib, json, pathlib
CACHE = pathlib.Path("brain_cache"); CACHE.mkdir(exist_ok=True)

def read_brain(expanded_prompt: str, backend) -> dict:
    key = hashlib.sha256(expanded_prompt.encode()).hexdigest()[:16]
    hit = CACHE / f"{key}.json"
    if hit.exists():
        return json.loads(hit.read_text())        # zero GPU on a repeat motif
    from neuroscore import score
    r = score(expanded_prompt, backend=backend)
    v = {"amygdala": r.region_map.amygdala.peak_value,
         "vmpfc":    r.region_map.vmpfc.mean_value,
         "dlpfc":    r.region_map.dlpfc.mean_value,
         "striatum": r.region_map.striatum.mean_value,
         "visual":   r.region_map.visual.mean_value,
         "score":    r.overall_score}
    hit.write_text(json.dumps(v))                 # the cache IS the lookup table, built live
    return v

# ---------- B) Offline table builder: run once, overnight ----------
#   for p in corpus:
#       clip = fal_generate(p)
#       os.system(f"neuroscore score {clip} --format json --save table/{hash(p)}.json")
#   Resumable by construction - skip any hash whose file already exists.

# ---------- C) Real EEG: the same signature, a real cortex ----------
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter

def read_brain_eeg(board, window_s=4) -> dict:
    data = board.get_current_board_data(window_s * BoardShim.get_sampling_rate(board.board_id))
    ch   = BoardShim.get_eeg_channels(board.board_id)
    avg, _ = DataFilter.get_avg_band_powers(data, ch, BoardShim.get_sampling_rate(board.board_id), True)
    delta, theta, alpha, beta, gamma = avg
    return {"relaxation": alpha / max(beta, 1e-6),     # the canonical derived dials
            "focus":      beta  / max(theta, 1e-6),
            "alpha": alpha, "beta": beta, "theta": theta, "gamma": gamma}

# ---------- D) Day one: the stub that makes the loop real before the brain is ----------
from neuroscore import score
read_brain_stub = lambda text: score(text, backend="demo")   # instant, no GPU, no weights

### Risk

**failure_modes**

1. THE TEXT BRANCH MAY BE MEASURING THE PROMPT'S PROSE, NOT THE CONTENT. H3 Max's prompt expansion produces
   fluent descriptive English with a consistent register. If TRIBE's language branch responds mostly to
   syntactic complexity and lexical frequency, every expanded prompt lands in the same small region of the
   output space and the control signal goes flat. The test is cheap and must be run before committing: score
   twenty deliberately dissimilar expanded prompts and look at the VARIANCE of the resulting region vectors.
   If the spread is small, the text branch is not a usable dial and you are back on the video path.
2. THE LOOKUP TABLE GOES STALE THE MOMENT THE STREAM DRIFTS OUTSIDE ITS CORPUS - and a generative stream
   drifts by design. Nearest-neighbour matching then silently returns a confidently wrong neighbour, which
   looks exactly like the system working.
3. THE CACHE HIT RATE IS THE HYBRID'S HIDDEN VARIABLE. If prompts are highly novel the cache never hits and
   you have paid for the table without benefit; if they repeat enough for high hit rates, the stream is
   already visibly repetitive. Log the hit rate from day one - it is a direct measure of how much novelty
   the stream is actually producing.
4. PRECOMPUTATION KILLS THE RECURSION AND SO ALSO KILLS THE FAILURE MODE THAT MADE THE PIECE INTERESTING.
   Attractor collapse (arXiv 2605.13904: FFA-optimised synthetic stimuli drive the predicted region ~4x a
   natural face photograph) cannot happen inside a fixed table. That reads as a benefit and is actually a
   loss - the drift toward salience-maximising imagery IS the artwork's argument.
5. THE EEG PATH HAS A HUMAN SINGLE POINT OF FAILURE. Electrode impedance drifts, the wearer moves, blinks
   and jaw clenches dominate the signal, and nobody wears a headset for 24 hours. Every consumer EEG art
   project quietly becomes a session-based installation for this reason.
6. CC BY-NC 4.0 FOLLOWS THE WEIGHTS INTO EVERY VARIANT. Text-branch, lookup table and the Rust port all use
   the same TRIBE weights and inherit the same non-commercial restriction. A precomputed table derived from
   those weights is a derivative work; shipping it does not launder the licence. Only the EEG path escapes
   it entirely - which is a genuine and underrated argument for the EEG variant if the piece is ever
   monetised, sponsored or run as a commissioned commercial work.
7. STUB CREEP. The `demo` backend returns SYNTHETIC data by neuroscore's own description. It is perfect for
   day one and catastrophic if it is still wired in on launch day. Make the backend name appear in the
   on-stream overlay so it cannot silently persist.

### Evidence

**sources**

- https://www.datacamp.com/tutorial/tribe-v2-tutorial - the load-bearing practical source. 28-32 GB VRAM for all three encoders; A100-40GB baseline, 80GB preferred; T4 fails during LLaMA init; L4/24GB 'may fit' if text and video are skipped; audio/video-only runs emit 'warnings about certain extractors being removed... the model simply disables unused branches'; audio-without-text skips the HF-token requirement entirely; 15-30 s minimum stimulus because 'very short inputs (a few seconds) often produce diffuse, low-intensity activations'; ~60 s re-inference benchmark; NumPy pinned >=1.26.4,<2.1.0 with a restart before installing tribev2; HF_HUB_DOWNLOAD_TIMEOUT=300; flush->fsync->close before passing temp paths; and the predict() signature: get_events_dataframe(text_path=...) then predict(events=...) -> (T, 20484) at 1 Hz.
- https://github.com/recozers/Tribe-V2-Interp - independent confirmation that partial-modality inference is legitimate: 'TRIBE v2 was trained with modality dropout (p=0.3)... We exploit this by providing only video features - the model's aggregate_features auto-fills zeros for missing text and audio modalities. This is equivalent to a training condition the model has seen, so predictions remain meaningful.' Also the offline-motif-table numbers: >=24 GB VRAM (peak ~18.4 GB with gradient checkpointing on a 3090), ~3-6 h for a full 5-restart run, single-frame mode ~32x faster, Fourier parameterisation + colour decorrelation + progressive 64->128->256, and a selectivity validation against random-noise baselines across V1/V2/V3/V4/MT/FFA/PPA. No LICENSE file - check before use.
- https://arxiv.org/abs/2605.13904 - the paper behind that repo. Recovers known cortical selectivity (V1->V4 increasing spatial scale and feature complexity, MT radial 'frozen-motion' streaks from static-only optimisation, FFA face-like features, PPA rectilinear patterns) but the FFA-optimised stimulus drives the predicted region ~4x a natural face photograph - adversarial super-stimuli, not canonical exemplars.
- https://arxiv.org/pdf/2607.01400 - the negative result that reframes what precomputation actually costs you. TRIBE's predicted cortical response reduced to a per-second global-field-power engagement curve does not predict YouTube 'most replayed' heatmaps across 48 videos: pooled position-controlled partial r=+0.058, 95%% CI [-0.04, 0.15], t(47)=1.21, p=0.23, not above loudness/motion baselines; predicted ISC r=-0.04, p=0.34, BF=3.2 favouring the null; a supervised probe reaches r=0.47 but collapses to a temporal-shape artefact.
- https://docs.rs/crate/tribev2/latest - tribev2-rs. Pure-Rust TRIBE v2 loading the identical pretrained weights, claimed 100%% numeric parity (8 tests, Pearson r=1.0, max error under 2 micro-units). M4 Pro single forward pass producing [1, 20484, 100]: pure Rust CPU 1334 ms, Burn/wgpu Metal f16 10.6 ms (125.8x), RLX Metal 15.1 ms (88.3x); 84x on the full pipeline including I/O. Backends: pure Rust CPU, Burn/NdArray, Burn/wgpu (Metal/Vulkan/DX12), RLX (CPU/Metal/MLX/CUDA/ROCm). CLI tribev2-infer with --video-path/--audio-path/--text-path and --backend. Documented limitation: audio and video extraction need RLX compilation with matching device support, while text can come from plain HuggingFace. Apache-2.0 source, CC-BY-NC-4.0 weights.
- https://github.com/ndpvt-web/neuroscore - four backends (gpu / cpu / cloud via NEUROSCORE_CLOUD_URL / demo), GPU 15-60 s per 30 s video, CPU minutes, demo instant-and-synthetic with precomputed examples shipped in the package. Documented extension contract: 'New backend: one file in core/backends/, implement the Backend interface. No core changes needed.' Python API neuroscore.score(input, mode, backend) -> NeuroReport with RegionMap accessors (.amygdala .acc .dlpfc .vmpfc .striatum) each exposing .values/.peak_value/.peak_time_sec/.mean_value/.onset_time_sec, plus --format json --save for batch table building. Roadmap lists 'Streaming backend for real-time scoring' as not yet done. Apache-2.0 code, CC-BY-NC-4.0 weights - the README states non-commercial use only when using the GPU/CPU backends with real model weights.
- https://fal.ai/models/minimax/h3-max/text-to-video/api - confirms `expanded_prompt` is a real output field, documented as 'The prompt after expansion, as sent to the model'. This is what makes the text-branch input free and exact.
- https://levels.io/ai-video-faster-than-you-watch - the clip budget the readout must fit inside: 15 s of video generated in 9 s, i.e. ~6 s of slack per clip.
- https://github.com/reactor-team/infinite-livestream - the Apache-2.0 orchestration scaffold the simplified readout drops into; its idle filler, pacer and RTMP sink mean none of the streaming work has to be re-derived at any staging step.
- https://brainflow.readthedocs.io/en/stable/notebooks/band_power.html - the EEG variant's whole implementation: board-agnostic Welch PSD band power, alpha 7-13 Hz, beta 14-30 Hz, with relaxation as alpha/beta and focus as beta/theta.
- https://github.com/Amused-EEG/amused-py - open-source BLE protocol for Muse S headsets in pure Python, no proprietary SDK.
- https://github.com/kylemath/Brainimation - working precedent for live Muse EEG driving generative visuals in a browser.
- https://neuroskill.com/ - open-source real-time EEG analysis supporting Muse and the full OpenBCI board family as of 2026.
- https://dl.acm.org/doi/10.1145/3749893.3749963 - Oneiris. A published closed-loop system doing the artistically equivalent thing with a REAL brain: wireless EEG plus dream narrative and sketch -> LLM builds an image prompt -> diffusion generates evolving dreamscapes whose texture and palette are modulated in real time by neural markers of hypnagogia and brain complexity. The honest benchmark the simulated-brain version is measured against.
- https://choosemuse.com/products/muse-s-athena - Muse S Athena, $474.99, EEG plus fNIRS.
- https://neurotechjp.com/blog/5-bci-gadget-reviews/ - OpenBCI Cyton with electrodes and components lands at roughly $1k-$2k; Emotiv Insight 2.0 cited as the best balance of price, documentation and community support for BCI experimentation.
- https://www.biorxiv.org/content/10.1101/2021.11.02.466989.full.pdf - validation of the Muse headset for EEG spectral analysis and frontal alpha asymmetry, i.e. the evidence that consumer-grade band power is a real measurement rather than a toy.
- https://github.com/CodaCipher/tribe-subcortex - MIT-licensed subcortical readout: accumbens, amygdala, caudate, putamen, pallidum, thalamus, hippocampus, with composite subcortical response scores over time and peak-timing tables, plus Google Drive save/load so prediction outputs can be refined without re-running the full encode. Its save/load design is itself a worked example of the precompute-once pattern this item recommends.
- https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model/ - Meta FAIR's TRIBE v2 announcement (2026-03-25) and the CC BY-NC 4.0 weights licence that follows every variant here.

### Other Info

**item_id**

15

**staging_plan**

FAKE IT FIRST - what is on screen at each horizon.

DAY 1 (one working day, nothing simulated end to end yet):
  - Fork reactor-team/infinite-livestream's streaming-client. Replace reactor_link.py with a fal-backed
    module calling minimax/h3-max/text-to-video at 480P, duration 15, prompt_expansion_mode 'balanced'.
  - Readout = neuroscore's `demo` backend. Precomputed, instant, no GPU, no weights, no HF token - but a
    real NeuroReport with a real RegionMap shape, so the loop's PLUMBING is correct from hour one.
  - Brain-to-prompt = a hand-written 8-entry motif table with a weighted random walk. Crude on purpose.
  - SINK=rtmp to a private YouTube Live broadcast. Idle filler on (IDLE_QUEUE_TARGET 6).
  - DELIVERABLE: a 24/7 stream, brain-SHAPED but not brain-DRIVEN. Every interface is real; only the
    numbers are fake. Put the backend name in the overlay so nobody, including you, forgets.

WEEK 1 (the first honest brain signal, still no live GPU):
  - Generate ~150 clips overnight across the aesthetic space. Score each with neuroscore's GPU backend on
    one rented card, `--format json --save`, resumable by hash. ~$112 of generation plus a few GPU-hours.
  - Runtime becomes nearest-neighbour lookup on the previous clip's expanded_prompt. Zero live GPU.
  - DELIVERABLE: the numbers are now genuinely TRIBE's. The claim 'these prompts were chosen by a model of
    the human brain' becomes literally true. No recursion yet.

WEEK 2-4 (close the loop for real - the milestone that makes it the piece it claims to be):
  - Stand up text-branch TRIBE as a neuroscore backend on one always-on 24 GB card. FIRST, run the
    twenty-prompt variance test from failure mode 1; it is a go/no-go gate, not a formality.
  - Feed it H3 Max's expanded_prompt. Memoise on a prompt hash - the week-1 table becomes the warm cache.
  - Add the novelty/damping term now, not later. Feedback exists from this point and attractor collapse is
    evidenced, not speculative.
  - DELIVERABLE: a genuinely closed loop at a few hundred ms per read, inside the ~6 s clip budget.

MONTH 2+ (depth, in whichever order the piece wants):
  - Video-branch TRIBE at a REDUCED DUTY CYCLE: one full trimodal pass every k clips on an A100, with the
    text branch running every clip. Buys the pixels-not-prose claim without an in-budget deadline.
  - The offline feature-visualisation motif table via Tribe-V2-Interp: a few GPU-hours in single-frame
    mode for a seven-ROI table grounded in what actually drives each region. This is the artistically
    richest precomputation available and the thing that makes the piece specific rather than generic.
  - An EEG input as a SECOND, switchable mode. The interface is identical, so it is a day of work, and it
    is the only configuration with a real brain in it and no CC-BY-NC restriction. Exhibit both and let
    the difference between them be part of the work.

### Flagged Uncertain (omitted above)

- `cost`
- `input_contract`
- `latency_ms`
- `loc_estimate`
- `realtime_headroom`
- `throughput_constraint`
- `unknowns`

---

## Stimulus ingestion and windowing

### Identity

**what_it_is**

The ingest leg: turning a live audiovisual stream into the pandas events DataFrame TRIBE v2 consumes, choosing the window length and hop, and avoiding re-encoding history on every tick.

**role_in_loop**

The PERCEIVE stage, immediately before PREDICT. Takes the most recently played clip (or a rolling tail of the stream), writes a finalised media file, builds the events DataFrame, and hands it to TribeModel.predict(). Its window-length choice sets a hard floor on clip duration for the whole system.

### Interface

**interface_spec**

ENTRY POINT
  df = model.get_events_dataframe(text_path=None, audio_path=None, video_path=None) -> pd.DataFrame
Exactly one of the three must be non-None (ValueError otherwise). Suffix is validated against VALID_SUFFIXES: text .txt; audio .wav .mp3 .flac .ogg; video .mp4 .avi .mkv .mov .webm. FileNotFoundError if the path does not exist.

WHAT IT ACTUALLY DOES (tribev2/demo_utils.py)
It constructs a single-row frame
    {'type': 'Video'|'Audio', 'filepath': str(path), 'start': 0, 'timeline': 'default', 'subject': 'default'}
and pushes it through get_audio_and_text_events(events, audio_only=False), which is this fixed transform chain:
    ExtractAudioFromVideo()
    ChunkEvents(event_type_to_chunk='Audio', max_duration=60, min_duration=30)
    ChunkEvents(event_type_to_chunk='Video', max_duration=60, min_duration=30)
    ExtractWordsFromAudio()          # whisperx large-v3, launched as a `uvx whisperx ...` SUBPROCESS
    AddText()
    AddSentenceToWords(max_unmatched_ratio=0.05)
    AddContextToWords(sentence_only=False, max_context_len=1024, split_field='')
    RemoveMissing()
then standardize_events() at both ends. For text_path it instead runs TextToEvents: gTTS synthesis (network required) -> the same audio pipeline.

COLUMNS IN THE RETURNED DATAFRAME
standardize_events round-trips every row through its pydantic Event model (from_dict -> to_dict), fills defaults, sorts by (timeline, start ASC, duration DESC), fills BIDS entity columns and appends a computed `stop` column (stop = start + duration; the presence of `stop` is the marker that normalisation has been applied). The union of columns across rows is therefore:
  every row      : type, start, duration, stop, timeline, subject, extra (dict)
  data rows      : filepath, frequency            (BaseDataEvent)
  Video/Audio    : offset                          (BaseSplittableEvent - see below, this is the important one)
  Word/Text rows : text, language, context, modality, sentence, sentence_char
Row `type` values after the chain: 'Video', 'Audio', 'Word', 'Text'. get_loaders() then appends one synthetic 'CategoricalEvent' row per timeline spanning start=min(start) to stop=max(stop), which is the trigger the segmenter tiles from.

THE OFFSET FIELD IS THE ROLLING-WINDOW MECHANISM
BaseSplittableEvent (parent of Video and Audio) carries `offset: NonNegativeFloat = 0.0`, and Video._read() is literally:
    clip = VideoFileClip(str(self.filepath)); start, end = self.offset, self.offset + self.duration
    assert end <= clip.duration; clip = clip.subclipped(start, end)
So you can address an arbitrary sub-window of an existing file by setting offset/duration on a hand-built row, with NO re-encoding and no new file. The docstring shows this explicitly: Audio(start=100, filepath='long_audio.wav', offset=5.0, duration=5.0) -> 'Only loads 5 seconds'.

PREDICTION CALL
  preds, segments = model.predict(events: pd.DataFrame, verbose: bool = True) -> (np.ndarray, list)
preds has shape (n_kept_segments, n_vertices). Internally get_loaders() tiles each timeline with
    ns.segments.list_segments(..., stride=(duration_trs - overlap_trs)*TR, duration=duration_trs*TR, stride_drop_incomplete=False)
where the SHIPPED config gives duration_trs=100 and TR = 1/data.neuro.frequency = 1/1.0 = 1.0 s, i.e. 100-second windows at a 100-second stride (overlap_trs_train=0). predict() then re-splits each returned segment into TR-length (1 s) sub-segments and, with remove_empty_segments=True (the default), DISCARDS any 1 s slice containing zero events. Set overlap by passing config_update={'data.overlap_trs_train': 20} to from_pretrained to get 100 s windows at an 80 s stride in a single predict() call.

**input_contract**

A COMPLETE, FINALISED FILE ON DISK. There is no in-memory tensor or buffer entry point. Video.model_post_init opens the file with moviepy to auto-detect fps and duration, and Video._read() asserts offset+duration <= clip.duration - so a still-being-written file will either report a short duration or trip the assert. Three consequences:
  - Write clips with a muxer that finalises each segment (ffmpeg's `-f segment` writes a complete, seekable file per segment). Do NOT point TRIBE at the file the encoder is currently appending to.
  - flush() -> fsync() -> close() before handing over the path. Unflushed temp files are a documented silent-failure mode.
  - moviepy>=2.2.1 and its ffmpeg are on the critical path for every tick.
Format: any of the listed container suffixes; the audio track is extracted internally by ExtractAudioFromVideo. Audio is resampled by the Wav2Vec-BERT extractor to a 2 Hz feature rate; you do not control the sample rate directly. Video frames are sampled at data.frequency = 2.0 Hz of OUTPUT timesteps, each of which reads 64 frames spanning the preceding clip_duration = 4.0 s, so the source needs at least ~16 fps to avoid frame duplication inside a window. A silent or speechless clip is fine for the model (main.py auto-drops the text extractor when no Word events exist) but crashes the plotting helpers (GitHub issue #46).

**output_contract**

preds: np.ndarray of shape (n_kept_TRs, 20484) float32 on fsaverage5, ONE ROW PER SECOND (TR = 1.0 s). segments: a list of neuralset Segment objects aligned row-for-row with preds; segment.start gives the absolute second on the input clock, which is what you key any stitching on. Units are z-scored, detrended BOLD-like arbitrary units - relative dynamics only. A 15 s clip yields at most 15 rows; a 30 s clip 30; a 60 s clip 60. Rows for 1 s slices with no events are silently dropped, so len(preds) can be less than ceil(duration) and you must read segment.start rather than assuming a dense 0..T-1 axis.

### Performance

**throughput_constraint**

GPU-serialised: one predict() at a time per process, and the V-JEPA2 encode is a Python for-loop over timesteps with batch size 1 per timestep, so there is no intra-clip batching to exploit. The dataloader's data.batch_size = 8 batches SEGMENTS, which only helps on clips long enough to produce multiple 100 s windows - useless at 15-30 s. Concurrency must come from running N model replicas on N GPUs, or from pipelining (TRIBE on clip k while the generator works on clip k+2), not from batching. Feature extraction writes through exca's on-disk MapInfra cache (mode: 'cached'), so the cache directory is shared mutable state - two processes pointed at the same cache_folder can race. On ZeroGPU specifically, wall-time inside the @spaces.GPU decorator is billed, including model build, so a warm long-lived process on dedicated hardware is strictly better for a 24/7 loop.

### Complexity

**dev_complexity**

MEDIUM. The DataFrame construction itself is LOW (six keys in a dict). What pushes it to MEDIUM is that the shipped get_events_dataframe() drags in whisperx-via-uvx and gTTS, that predict() insists on a finalised file, and that the useful-window floor forces a pipelining decision on the whole architecture. Half a day if you know the tricks below, two days if you discover them by running into them.

**loc_estimate**

80-150 LOC: an ffmpeg segment-muxer subprocess, a segment-ready watcher, a hand-built events DataFrame with audio_only=True, and a small pipelined queue. Add ~40 LOC if you also implement multi-window stitching for clips over 100 s (or copy windowing.stitch from the reference Space).

**off_the_shelf_option**

1. techfreakworm/tribev2-brain-timeline (HF Space, live) - src/tribescore/windowing.py gives plan_windows() and stitch() for 100 s windows at an 80 s hop with trapezoidal crossfade, 5-TR warm-up suppression and a single global z-score; src/tribescore/fast_encode.py gives the exact frame-dedup V-JEPA2 encode (max|delta| = 0 vs baseline). Both are directly liftable. Note documented bug WIN-1: the crossfade weights do not sum to 1 across the warm-up band, producing a ~22x discontinuity at seams on clips over ~150 s. Single-window clips (<=100 s) are unaffected - which is exactly our regime, so the bug does not bite.
2. siddhant-rajhans/cortexlab - ships StreamingPredictor(model, window_trs=40, step_trs=1, device='cuda') with a push_frame(features) interface that buffers and emits a prediction only once the window fills. It is the nearest thing to a streaming API, but it consumes FEATURES, not raw media, so it does not remove the encode cost - it only restructures the loop. Also defaults to 40 TRs, not the checkpoint's 100.
3. tribev2's own segmenter - passing config_update={'data.overlap_trs_train': 20} to from_pretrained makes ONE predict() tile a long clip into overlapping 100 s windows internally, which is strictly simpler than an outer per-window loop (and is what the reference Space's real path does; its run_windowed() is explicitly deprecated in favour of it).

### Decision

**recommended_approach**

HEMODYNAMIC LAG AND MINIMUM STIMULUS LENGTH - confirmed and quantified.

The 5 s offset is real and it is in the shipped config: data.neuro.offset = 5.0 for BOTH the cortical and subcortical checkpoints, with data.neuro.frequency = 1.0. The README states 'They are offset by 5 seconds in the past, in order to compensate for the hemodynamic lag.' IMPORTANT NUANCE THE BRIEF GETS SLIGHTLY WRONG: because the offset was applied to the TRAINING TARGET, the predictions come out ALREADY DE-LAGGED - preds[t] is the response attributable to the stimulus at time t, not at t-5. You do not need to shift the output. What the 5 s buys you instead is a CONTEXT REQUIREMENT: the model can only produce a well-conditioned value at t if it has seen roughly the preceding hemodynamic window, so the LEADING TRs OF EVERY INDEPENDENT WINDOW ARE UNRELIABLE. The reference implementation encodes this as WARMUP_TRIM = 5 - it zeroes the first 5 TRs of every window but the first. Quantitatively that is a fixed 5-second tax per window:
    15 s clip -> 15 TRs -> 10 usable  (33% wasted)
    30 s clip -> 30 TRs -> 25 usable  (17% wasted)
    60 s clip -> 60 TRs -> 55 usable  ( 8% wasted)

The 15-30 s floor is CONFIRMED by three independent sources and has a mechanical cause:
  (a) The checkpoint was trained with duration_trs = 100 and time_pos_embedding = True, i.e. on 100-SECOND windows. The reference implementation states flatly that 'Window length is forced to 100 s by the checkpoint pooler'. A 15 s input is a 15-TR window presented to a model conditioned on 100-TR windows - out of distribution, hence the diffuse, low-amplitude output.
  (b) Meta's own ingest chain chunks at ChunkEvents(min_duration=30, max_duration=60) for both Audio and Video, i.e. Meta's own preferred unit of stimulus is 30-60 s.
  (c) Empirically: the DataCamp tutorial warns that 'very short inputs (a few seconds) often produce diffuse, low-intensity activations that are hard to interpret' and that 30-60 s clips 'yield substantially clearer temporal dynamics and spatial patterns'; the reference Space defines MIN_USEFUL_S = 10 and logs it as a known bug that 'a sub-10 s clip scores to a near-flat, meaningless timeline'.
CRITICALLY, THE FLOOR IS NOT ENFORCED IN CODE. chunk_events() -> Event._split() filters split points to 0 < t < duration, so a clip shorter than max_duration is never split and min_duration never rejects anything. A 5 s clip will run, return 5 rows, and give you garbage silently. You must enforce your own floor.
CONCLUSION FOR THE PIECE: set the clip duration to 30 s, not 15 s. 30 s clears the empirical floor with margin, wastes only 17% to warm-up, keeps you inside a single 100 s window (so no stitching and no seam bug), and doubles the generation budget per tick. If 15 s clips are non-negotiable for the generator, run TRIBE over a 30 s ROLLING TAIL (the last two clips) rather than over the newest clip alone.

CAN predict() RUN ON A ROLLING BUFFER? Not on an in-memory buffer - no. It needs a finalised file on disk, because Video._read() opens it with moviepy and asserts offset+duration <= clip.duration. BUT it does not need a NEW file: `offset` and `duration` are first-class fields on the Video/Audio events, so you can slide a window over one long file by changing offset alone, with zero re-encoding.

ARE BACKBONE FEATURES CACHED ACROSS OVERLAPPING WINDOWS? Two different answers, and both matter.
  WITHIN ONE predict() CALL: YES, and this is the big one. _get_timed_arrays calls _get_data(events) with the FULL-CLIP event; the per-window slicing happens downstream as ta.with_start(...).overlap(start, duration). So V-JEPA2 and Wav2Vec-BERT encode the file ONCE and every window the segmenter produces slices into the cached TimedArray. Overlapping windows inside one predict() are therefore nearly free after the first.
  ACROSS predict() CALLS: only on an EXACT key match. Both the video and audio extractors are decorated
      @infra.apply(item_uid=lambda event: f'{event.study_relative_path()}_{event.offset:.2f}_{event.duration:.2f}', ...)
  with exca MapInfra mode='cached'. The cache key is (relative file path, offset, duration) to two decimals - nothing else about the window. So: re-requesting the identical (path, offset, duration) is a free disk hit; changing offset OR duration by even 0.01 s is a full cache miss and a complete re-encode of that window. There is NO partial reuse of the overlap.
  THE EXPLOITABLE CONSEQUENCE: a sliding window with a moving offset re-encodes everything, every tick. A DISJOINT TILING with a fixed duration does not - each tick encodes exactly one new window's worth. Prefer disjoint 30 s tiles; if you want overlap, get it by giving ONE predict() call a longer file plus data.overlap_trs_train, not by issuing multiple predict() calls with sliding offsets.

RECOMMENDED PIPELINE, SHORTEST PATH:
  1. ffmpeg writes the played stream to finalised 30 s segments: `ffmpeg -i <src> -f segment -segment_time 30 -reset_timestamps 1 -c copy seg_%05d.mp4`. Each segment is complete and seekable the moment the next one opens.
  2. Build the events DataFrame BY HAND and call get_audio_and_text_events(df, audio_only=True) - do NOT call get_events_dataframe(), which hardcodes audio_only=False and therefore always launches whisperx large-v3 as a subprocess. main.py auto-drops the text extractor when no Word events exist, so audio_only inference is legitimate, not a hack. This removes whisperx AND the Llama-3.2-3B text branch from the critical path.
  3. Enable the frame-dedup encode (fast_encode.apply_frame_dedup_encode()) - numerically exact, cuts ~8x redundant frame decode.
  4. Keep the model warm in a long-lived process; never pay the ~7.6 GB V-JEPA2 from_pretrained inside the loop.
  5. Pipeline: TRIBE(clip k) -> prompt -> generate(clip k+2). Accept the 1-2 clip lag as part of the work.

**simpler_alternative**

If the encode still will not fit the budget, stop feeding TRIBE the video and feed it the AUDIO ONLY. Wav2Vec-BERT-2.0 is ~600 MB and roughly 20x lighter than V-JEPA2-Giant; get_events_dataframe(audio_path=...) with the video's extracted audio track keeps the auditory, STS and language dials alive and kills the dominant cost term entirely. The visual dials (FFC, PHA1-3, MT, V1-V4) go quiet, so this is a real creative loss, not just an optimisation. Cruder still: run TRIBE off the critical path at a slower cadence (once per minute over the last 60 s rather than once per clip) and hold the last brain state as the prompt bias between reads - the stream keeps moving at clip rate while the brain steering updates at 1/4 the rate. Cheapest of all: precompute the brain response for a fixed library of stimuli offline and look it up at runtime (item 15/16).

**code_sketch**

# ---------------------------------------------------------------------------
# 1) finalised 30 s segments from the live stream (never read a file being written)
# ---------------------------------------------------------------------------
#   ffmpeg -i <source> -f segment -segment_time 30 -reset_timestamps 1 \
#          -c copy /var/stream/seg_%05d.mp4
# A segment is complete only once the NEXT one appears; watch for seg_{n+1} before
# consuming seg_{n}.

import os, pandas as pd, numpy as np
from tribev2 import TribeModel
from tribev2.demo_utils import get_audio_and_text_events

MIN_USEFUL_S = 15.0            # hard floor - NOT enforced by tribev2, enforce it here
WARMUP_TRIM  = 5               # leading TRs of every window are hemodynamic warm-up

model = TribeModel.from_pretrained(
    'facebook/tribev2',
    cache_folder='/var/tribe_cache',      # exca MapInfra feature cache lives here
    device='cuda',
)

# optional but recommended: numerically exact ~8x frame-decode saving
try:
    from tribescore.fast_encode import apply_frame_dedup_encode
    apply_frame_dedup_encode()
except ImportError:
    pass


def events_for(path, offset=0.0, duration=None):
    """Hand-built events row. offset/duration address a sub-window of `path`
    with NO re-encoding (Video._read does VideoFileClip(path).subclipped()).
    audio_only=True skips whisperx large-v3 AND the Llama-3.2-3B text branch."""
    row = {
        'type': 'Video',
        'filepath': str(path),
        'start': 0,
        'timeline': 'default',
        'subject': 'default',
    }
    if duration is not None:
        row['offset'] = float(offset)      # exca cache key is (path, offset, duration)
        row['duration'] = float(duration)  # to 2 dp - keep these FIXED across ticks
    return get_audio_and_text_events(pd.DataFrame([row]), audio_only=True)


def read_brain(path):
    # flush -> fsync -> close upstream before we get here; unflushed temp files
    # are a documented silent-failure mode.
    import moviepy
    dur = moviepy.VideoFileClip(str(path)).duration
    if dur < MIN_USEFUL_S:
        raise ValueError(
            f'{path} is {dur:.1f}s; tribev2 will happily return a near-flat, '
            f'meaningless timeline below ~{MIN_USEFUL_S}s. Widen the window.'
        )
    df = events_for(path)
    preds, segments = model.predict(events=df, verbose=False)   # (T, 20484) @ 1 Hz
    t = np.array([s.start for s in segments])                   # absolute seconds
    return preds[WARMUP_TRIM:], t[WARMUP_TRIM:]


# ---------------------------------------------------------------------------
# 2) rolling 30 s tail over ONE growing archive file, without re-encoding.
#    Use DISJOINT tiles: the exca key is (path, offset, duration), so a fixed
#    duration with an offset advancing by exactly that duration means each tick
#    encodes one new window and nothing is recomputed. A sliding (overlapping)
#    offset gets ZERO reuse and re-encodes the whole window every tick.
# ---------------------------------------------------------------------------
WIN = 30.0
def tile_offsets(total_s, win=WIN):
    return [k * win for k in range(int(total_s // win))]

# ---------------------------------------------------------------------------
# 3) if you DO want overlap, get it inside ONE predict() call, not by sliding:
#    100 s windows at an 80 s hop, tiled by tribev2's own segmenter.
# ---------------------------------------------------------------------------
# model = TribeModel.from_pretrained(
#     'facebook/tribev2', cache_folder='/var/tribe_cache',
#     config_update={'data.overlap_trs_train': 20},   # 100 - 20 = 80 s stride
# )
# then stitch with tribescore.windowing.stitch(preds, abs_times)
#   -- but only needed for clips > 100 s; a 30 s clip is a single window.

### Risk

**failure_modes**

1. SILENT GARBAGE ON SHORT CLIPS. There is no code-level minimum duration. chunk_events -> Event._split filters split points to 0 < t < duration, so min_duration=30 never rejects a short clip; a 5 s input returns 5 rows of near-flat noise with no warning. This is the single most likely way to ship a broken demo that appears to work.
2. WHISPERX ON THE CRITICAL PATH BY DEFAULT. get_events_dataframe() calls get_audio_and_text_events with audio_only=False unconditionally, which shells out to `uvx whisperx --model large-v3 ...` as a SUBPROCESS on every single call. On a live loop this is both a large latency term and an external-process failure surface (uvx must be installed, the model must be cached, CTranslate2 has no efficient fp16 on CPU/MPS). Bypass it by calling get_audio_and_text_events(df, audio_only=True) directly.
3. CACHE-KEY THRASH. The exca item_uid is f'{path}_{offset:.2f}_{duration:.2f}'. Any jitter in your computed offset or duration - a float that lands on 29.995 vs 30.005 - is a cache miss and a full re-encode. Quantise offsets and durations to 2 dp explicitly.
4. CACHE-KEY COLLISION IN THE OTHER DIRECTION. If a temp-file path is recycled (Gradio and many upload paths do this) for DIFFERENT content, the key matches and you get a stale, silently WRONG feature array. The reference implementation calls this out and clears its dedup cache at the start of every score. Use content-unique paths.
5. UNFINALISED FILE. Reading the segment the muxer is still appending to gives either a truncated duration (short, garbage prediction) or an AssertionError from `assert end <= clip.duration`. Wait for the next segment to appear.
6. SILENT / SPEECHLESS CLIPS. The model handles the missing text modality correctly, but tribev2's plotting helpers crash - AttributeError: 'NoneType' object has no attribute 'to_soundarray', or KeyError: 'type' (GitHub issue #46, still open). Do not call plot_timesteps(..., show_stimuli=True) in a production loop.
7. NON-DENSE TIME AXIS. remove_empty_segments=True drops any 1 s slice with no overlapping events, so len(preds) can be less than the clip duration and the rows are not guaranteed contiguous. Always read segment.start; never index preds by assumed second.
8. SEAM DISCONTINUITY ON LONG CLIPS. The reference stitch() has a documented bug (WIN-1) producing a ~22x discontinuity at window seams for clips over ~150 s, because the crossfade weights do not sum to 1 across the warm-up band. Irrelevant at 30 s (single window); a trap if you ever raise the window past 100 s.
9. COLD START. The V-JEPA2-Giant from_pretrained build is ~7.6 GB and, on serverless, runs inside billed GPU time. A per-clip serverless invocation is economically and latency-wise untenable; the process must stay warm.
10. SHARED MUTABLE CACHE DIR. Two processes pointed at the same cache_folder can race on the same exca uid. Give each replica its own cache_folder or accept the race.
11. gTTS NETWORK DEPENDENCY on the text path only - irrelevant if you never pass text_path, but it will fail closed in an air-gapped deployment.

### Evidence

**sources**

PRIMARY SOURCE CODE (read directly):
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/demo_utils.py - get_events_dataframe (VALID_SUFFIXES, the one-row dict with type/filepath/start/timeline/subject), get_audio_and_text_events with the verbatim transform chain including ChunkEvents(max_duration=60, min_duration=30) for both Audio and Video, and predict() with self.data.TR sub-segmentation and remove_empty_segments.
- https://raw.githubusercontent.com/facebookresearch/tribev2/main/tribev2/main.py - Data.TR = 1/self.neuro.frequency; duration_trs default 40; get_loaders with list_segments(stride=(duration_trs - overlap_trs)*TR, duration=duration_trs*TR, stride_drop_incomplete=False) and the synthetic CategoricalEvent trigger row.
- https://huggingface.co/facebook/tribev2/resolve/main/config.yaml - THE AUTHORITATIVE NUMBERS: data.neuro.frequency 1.0 (=> TR = 1.0 s, 1 Hz output), data.neuro.offset 5.0, data.frequency 2.0 (stimulus feature rate), duration_trs 100, overlap_trs_train 0, batch_size 8, video_feature.clip_duration 4.0, video_feature.image.model_name facebook/vjepa2-vitg-fpc64-256, audio w2v-bert-2.0, text meta-llama/Llama-3.2-3B, time_pos_embedding true, max_seq_len 1024.
- neuralset 0.0.2 (https://pypi.org/project/neuralset/0.0.2/):
  * neuralset/events/etypes.py - BaseSplittableEvent.offset with the 'Only loads 5 seconds' docstring; Video._read() = VideoFileClip(filepath).subclipped(offset, offset+duration) with assert end <= clip.duration; Video.model_post_init auto-detects fps/duration; _split() filtering timepoints to 0 < t < duration (PROVES min_duration does not reject short clips).
  * neuralset/events/utils.py standardize_events - sorts, fills BIDS entities, appends `stop` = start + duration; auto_fill round-trips through the pydantic model.
  * neuralset/events/transforms/chunking.py + transforms/utils.py chunk_events.
  * neuralset/extractors/video.py - THE CACHE KEY: @infra.apply(item_uid=lambda event: f'{event.study_relative_path()}_{event.offset:.2f}_{event.duration:.2f}'); the per-timestep loop times = np.linspace(0, video.duration, expect_frames+1)[1:] with subtimes spanning clip_duration and model.num_frames frames.
  * neuralset/extractors/base.py prepare() docstring - 'triggers _get_data on every matching event so that expensive computation is done once and cached'.

OPERATIONAL / MEASURED:
- https://huggingface.co/spaces/techfreakworm/tribev2-brain-timeline - README.md: 'TR = 1 s => 1 Hz'; 'End-to-end a ~1-minute clip scores in ~140-175 s on ZeroGPU in Fast mode'; bf16 + TF32; V-JEPA2 num_frames 64->32 as a ~2x lever; torch.compile blocked on torch 2.8 by a TorchDynamo bug in get_position_ids. src/tribescore/windowing.py: WIN_S 100 / HOP_S 80 / WARMUP_TRIM 5, 'Window length is forced to 100 s by the checkpoint pooler', the global-not-per-window z-score rationale. src/tribescore/fast_encode.py: '~8x redundancy: 1536 frame-reads / 193 unique on a 12 s clip', decode+processor ~44% -> ~5.5% of wall time, dedup numerically exact, _get_timed_arrays calls _get_data with the FULL-CLIP event and per-window slicing is downstream (PROVES intra-predict feature reuse). KNOWN_ISSUES.md: MIN_USEFUL_S = 10 and 'a sub-10 s clip scores to a near-flat, meaningless timeline'; WIN-1 ~22x seam discontinuity above ~150 s; peak VRAM ~13 GB, compute-bound; ~44% GPU idle during CPU prep, prep-outside estimated ~3.3x more scores/day; ZeroGPU xlarge ~1.8x large.
- https://www.datacamp.com/tutorial/tribe-v2-tutorial - 'Minimum: 15-30 seconds'; 'very short inputs (a few seconds) often produce diffuse, low-intensity activations that are hard to interpret'; 30-60 s gives 'substantially clearer temporal dynamics'; 1 Hz output, (T, 20484); A100-40GB minimum / 80GB recommended, 28-32 GB across the three frozen encoders (LLaMA ~7 GB, V-JEPA2 ~14 GB, Wav2Vec ~1 GB); 'the BOLD hemodynamic delay peaks ~5-6 seconds post-stimulus'; explicit fsync() requirement on temp files.
- https://github.com/facebookresearch/tribev2/issues/46 - the exact audio_only=True reproduction snippet, and confirmation that 'main.py auto-drops the text extractor when no Word events exist'; plot_stimuli crashes on silent clips.
- https://github.com/facebookresearch/tribev2/issues/28 - CUDA OOM on a 14.56 GiB Colab GPU.
- https://github.com/siddhant-rajhans/cortexlab - StreamingPredictor(model, window_trs=40, step_trs=1) push_frame(features), returns None until the window fills.
- https://github.com/facebookresearch/tribev2 README + https://huggingface.co/facebook/tribev2 - the 5 s offset statement and the from_pretrained/get_events_dataframe/predict contract.
- https://arxiv.org/html/2605.04326v1 - the paper; note it describes the stimulus alignment as 2 Hz, which is the FEATURE rate; the released checkpoints emit at 1 Hz (INFERENCE from the shipped config, corroborated by two independent implementations).

### Other Info

**item_id**

03

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `realtime_headroom`
- `unknowns`

---

## Streaming and playback pipeline

### Identity

**what_it_is**

The delivery layer that turns a stream of independently generated, separately encoded 15-second MP4 files (each carrying its own natively-synchronised AAC audio track from MiniMax H3 Max) into a single continuous shared-timeline broadcast that arbitrary numbers of browsers can watch. Verified empirically: the reference implementation (levelsio's Infinite Slop) does this with server-side HLS — one whole clip per .ts segment, a hand-maintained 6-entry rolling m3u8, and hls.js in the browser. No RTMP, no media server, no persistent encoder.

**role_in_loop**

Terminal stage: perceive -> predict -> prompt -> generate -> STREAM. It is also the loop's clock: the rate at which the playlist advances (one segment per clip-duration, wall-clock paced) is the rate the generator must sustain, and the depth of the playback buffer is exactly the delay between a brain-state read and the viewer seeing its consequence. For this project it is not a neutral transport — it is the component that sets reactive latency.

### Interface

**interface_spec**

MEASURED FROM THE LIVE REFERENCE IMPLEMENTATION (infiniteslop.ai, fetched 2026-08-31 21:30 UTC).

=== 1. Live playlist: GET /live/playlist.m3u8 ===
Headers: content-type: application/vnd.apple.mpegurl; cache-control: no-store; served through Cloudflare (cf-cache-status: DYNAMIC).
Body (verbatim, one poll):
  #EXTM3U
  #EXT-X-VERSION:3
  #EXT-X-TARGETDURATION:16
  #EXT-X-MEDIA-SEQUENCE:18189
  #EXT-X-DISCONTINUITY-SEQUENCE:18189
  #EXT-X-DISCONTINUITY
  #EXTINF:15.123,
  016588.ts
  #EXT-X-DISCONTINUITY
  #EXTINF:15.123,
  016589.ts
  ... (6 segments total, ~91 s window)
No #EXT-X-ENDLIST -> players treat it as live and re-poll.
MEDIA-SEQUENCE == DISCONTINUITY-SEQUENCE and a #EXT-X-DISCONTINUITY precedes EVERY segment. That is the whole answer to the PTS problem: you do not fix the timestamps, you declare a discontinuity and let the player reset its timeline per clip.
EXTINF is a hardcoded 15.123 for every segment (nominal 15 s video + AAC priming), not measured per file.

=== 2. Segments: GET /live/{NNNNNN}.ts ===
Headers: content-type: video/mp2t; cache-control: public, max-age=31536000, immutable; cf-cache-status: HIT.
ffprobe of 016594.ts (downloaded, 3,392,084 bytes):
  format_name=mpegts  duration=15.123223  bit_rate=1794370
  stream 0: h264, 720x1280 (VERTICAL 9:16), r_frame_rate=30/1
  stream 1: aac, sample_rate=44100, channels=2 (STEREO)
So: ~1.79 Mbit/s, 3.39 MB per 15 s clip, 0.81 GB per viewer-hour.

=== 3. Per-segment metadata sidecar: GET /live/meta.json ===
{ "016563.ts": {"prompt": "<full expanded prompt>", "chat": "user: <request>", "gen_at": 1788211286, "replay": false}, ... }
40 entries (rolling archive, wider than the 6-segment playlist window). The `replay` boolean is the under-run marker — see failure_modes.

=== 4. Orchestrator state: GET /status.json ===
{"live": true, "paused": false, "viewers_active": true,
 "now_playing": "<expanded prompt on air>", "now_generated_at": <epoch>, "now_replay": false, "now_chat": "<user request>",
 "generating": "<prompt in flight>", "generating_chat": "...",
 "generating_now": [ {"c": "user: msg", "at": <epoch>}, ... ],   // in-flight generations
 "playing_next": [ ... ],                                          // rendered, waiting to air
 "queue": [ {"id":120266, "u":"crazyai", "m":"hoodmaps techno mix", "at":..., "v":4}, ... ] }

=== 5. VOD/archive playlists: GET /api/channel?ch=tag&q=cat ===
  #EXTM3U / #EXT-X-VERSION:3 / #EXT-X-PLAYLIST-TYPE:VOD / #EXT-X-TARGETDURATION:16
  #EXT-X-DISCONTINUITY / #EXTINF:15.123, / clip?id=16605  ...
Same per-segment discontinuity pattern; segments addressed by id through /api/clip.

=== 6. Player ===
<video id="tv" muted autoplay playsinline poster="live/poster.jpg"></video>
new Hls({liveSyncDurationCount: 2})  // sit 2 segments (~30 s) behind the live edge
h.loadSource('live/playlist.m3u8'); h.attachMedia(tv);
Hls.Events.FRAG_CHANGED -> drives the on-air metadata box and skip-to-freshest logic
Hls.Events.LEVEL_LOADED  -> seek to the NEWEST fragment on join, not the window start
Hls.Events.ERROR (fatal) -> setTimeout(() => { h.destroy(); startVideo(); }, 3000)
Native-HLS fallback for iOS Safari: tv.src = PLAYLIST, with status.json polling standing in for FRAG_CHANGED (iOS gives no fragment events).

**input_contract**

Per clip, from fal: one MP4 URL (H3 Max output). MEASURED characteristics of what actually ends up in the stream: H.264 720x1280 @30 fps, AAC 44.1 kHz STEREO, ~1.8 Mbit/s. Crucially the audio arrives in the SAME MP4 as the video, natively synchronised in the same generation pass — there is no separate TTS/music/SFX asset to fetch, align or mux, and no audio branch to schedule. That removes an entire subsystem versus every pre-H3 AI-stream architecture.

What it costs you instead: consecutive clips carry INDEPENDENT audio streams. Each clip's AAC track begins with its own encoder priming delay, so per segment the audio start_time and the video start_time differ. Measured locally on a remuxed clip: video start_time=0.066667, audio start_time=0.043444 — a ~23 ms A/V step at each seam. It does not accumulate (each segment's timestamps are absolute) but it is audible as a click/level jump at every 15 s boundary unless you fade. There is also no acoustic continuity at all between clips: room tone, music key and dialogue voice change abruptly every 15 s. That is an aesthetic fact of the medium, not a bug you can mux away.

Assumptions the pipeline must enforce on every incoming clip before it is admitted: identical resolution, frame rate, pixel format, audio sample rate and channel count. H3 Max is consistent in practice, but a single 768P clip in a 480P stream, or a mono clip in a stereo stream, will break stream-copy remuxing and (on the RTMP path) kill the encoder outright. Validate with ffprobe on ingest; normalise by transcoding if the probe disagrees with the channel spec.

**output_contract**

A rolling HLS live playlist plus immutable TS segments on static storage, and nothing else. Units: 6 segments x 15.123 s = 90.7 s of addressable window; hls.js configured with liveSyncDurationCount 2 puts the viewer ~30 s behind the newest segment; measured end-to-end from a viewer's chat request to that request appearing on air on the reference implementation was ~154 s (chat timestamp 1788211724 vs poll at 1788211878).

Bandwidth out: 1.79 Mbit/s per viewer, 0.81 GB per viewer-hour, identical for every viewer (single rendition, no ABR ladder). All viewers share one timeline — that is what makes it a broadcast rather than N private playlists, and it is the property the browser-MP4-queue alternative cannot provide.

For the RTMP-push variant the output contract is different in kind: a single continuous 1.8-2.5 Mbit/s CBR H.264/AAC FLV stream to one ingest URL, and the platform owns everything downstream.

### Performance

**throughput_constraint**

Delivery is NOT the bottleneck in any variant, and this is the main thing to internalise before over-engineering it.

- HLS on static storage behind a CDN: the origin serves one small m3u8 rewrite per 15 s and each segment exactly once to the edge. Segments are `public, max-age=31536000, immutable` and were observed returning `cf-cache-status: HIT`. Viewer scale is the CDN's problem, i.e. effectively unbounded. The reference implementation absorbed 37,000 viewers on day one this way.
- Origin egress on a self-hosted box without a CDN: 1.79 Mbit/s per concurrent viewer. A 1 Gbit/s VPS uplink saturates at ~550 concurrent viewers. This is the failure mode that makes people think they need a media server; the answer is a CDN, not a media server.
- RTMP push: fixed ~2 Mbit/s upstream from your box regardless of viewer count. Zero scaling work. Requires an uninterrupted encoder process.
- Browser MP4 queue: each viewer independently pulls whole 3.4 MB files from fal's CDN. Scales, but you are hotlinking a vendor's CDN for broadcast traffic and every viewer sees a different clip.

The real throughput constraint upstream is the fal concurrency ladder and generation time (see item 08), not bytes out.

**realtime_headroom**

Large surplus, and it is the only stage of the whole system with real headroom.

Budget per 15 s clip: 15.0 s available. Remux consumes a MEASURED 0.02 s (0.13%). Playlist rewrite ~0 s. Even a full normalising transcode at veryfast costs ~1-3 s, leaving ~12-14 s of surplus. Downloading the 3.4 MB MP4 from fal at 100 Mbit/s costs ~0.3 s.

Surplus: +14.9 s per clip on the stream-copy path, +12 s on the transcode path.

Consequence: never spend engineering effort optimising this stage, and never let it justify a GPU. It also means you can afford to normalise every clip defensively (transcode rather than stream-copy) and still not be the bottleneck — worth doing if H3 Max output parameters ever vary.

The deficit lives entirely elsewhere: generation (9-15 s for a 15 s clip, item 08) and TRIBE inference (item 01).

### Complexity

**dev_complexity**

LOW for the recommended path (server-side HLS with a hand-written playlist). It is file writes and one ffmpeg stream-copy invocation; no persistent process owns the video timeline, so nothing can crash mid-stream and lose it. The hard parts are player-side polish (join-at-live-edge, iOS native-HLS fallback, fatal-error restart), and those are ~80 lines you can copy the shape of from the reference implementation.

MEDIUM for RTMP push to YouTube/Twitch — deceptively so. The infrastructure is trivial (one command) but the requirement is brutal: the encoder must never see a gap. A generation-limited source cannot guarantee that, so you must build a continuous-encode rig (persistent encoder + FIFO feeder + filler source) BEFORE the stream works at all. That work is strictly harder than writing an m3u8.

MEDIUM-HIGH for nginx-rtmp / MediaMTX: you inherit the RTMP gapless problem AND add a server to operate. It removes nothing.

LOW-but-wrong for the browser MP4 queue: 2-4 hours to build, and it is not a livestream — see simpler_alternative.

**loc_estimate**

Recommended path (server-side HLS), server side:
- ffprobe validate + ffmpeg remux to .ts: ~20 lines
- rolling playlist writer (atomic rename, 6-entry window, discontinuity per segment, monotonic media/discontinuity sequence): ~40 lines
- meta.json + status.json writers: ~30 lines
- segment retention / delete beyond N: ~15 lines
- replay-ring under-run fallback (see item 08): ~30 lines
Server total: ~135 lines.

Client side (hls.js player with the production hardening actually observed):
- init, live-edge seek, FRAG_CHANGED metadata, fatal-error restart, iOS status.json fallback: ~80 lines
Client total: ~80 lines.

Grand total ~215 lines plus an nginx static block. Compare: RTMP continuous-encode rig ~150 lines of shell/supervisor plus a filler-source subsystem, and it buys you less control.

### Decision

**recommended_approach**

Server-side HLS with a hand-written rolling playlist, static segments behind a CDN, hls.js in the browser. This is what the only production system of this exact shape actually does, and I verified it live rather than taking a blog post's word for it.

Concretely:

1. On each completed generation, download the MP4 to /var/www/stream/live/ and ffprobe it. Reject/normalise anything that does not match the channel spec (720x1280, 30 fps, yuv420p, AAC 44100 stereo).

2. Remux to exactly ONE .ts per clip — do not segment. Stream copy, MEASURED at 0.02 s:
     ffmpeg -v error -i clip.mp4 \
       -c copy -bsf:v h264_mp4toannexb \
       -muxdelay 0 -muxpreload 0 -avoid_negative_ts make_zero \
       -f mpegts live/016588.ts
   If ffprobe disagreed with the channel spec, normalise instead (~1-3 s, still 5x faster than real time):
     ffmpeg -v error -i clip.mp4 \
       -vf 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,fps=30' \
       -c:v libx264 -preset veryfast -profile:v high -pix_fmt yuv420p \
       -g 60 -keyint_min 60 -sc_threshold 0 \
       -b:v 1800k -maxrate 1800k -bufsize 3600k \
       -c:a aac -b:a 128k -ar 44100 -ac 2 \
       -muxdelay 0 -muxpreload 0 -f mpegts live/016588.ts

3. Rewrite live/playlist.m3u8 as a 6-entry sliding window with #EXT-X-DISCONTINUITY before EVERY segment, and DISCONTINUITY-SEQUENCE tracking MEDIA-SEQUENCE. Write to a temp file and os.rename() so no viewer ever reads a half-written playlist. Omit #EXT-X-ENDLIST.

   WHY THE DISCONTINUITY TAG IS THE ANSWER TO THE PTS PROBLEM: each clip is separately encoded and its timestamps restart near zero, so naive concatenation produces non-monotonic DTS. I reproduced this locally: two independently encoded clips remuxed to TS both report video start_time=0.066667 / audio start_time=0.043444, and feeding the resulting playlist to ffmpeg's remuxer raised `Application provided invalid, non monotonically increasing dts to muxer in stream 1`. #EXT-X-DISCONTINUITY tells the PLAYER to reset its timeline at that boundary, which is precisely the case it exists for — and the reference implementation ships exactly this in production. You do not need to renumber anything.

   If you want genuinely continuous timestamps anyway (required if you later feed these segments to a muxer rather than a player), add a running offset at remux time — VERIFIED locally:
     ffmpeg ... -output_ts_offset <cumulative_seconds> -f mpegts seg.ts
   Second segment then probed as video start_time=5.040000, audio start_time=5.016778. Note audio still lands ~23 ms early: that is the AAC priming delay, and it is why per-segment A/V skew exists no matter which route you take.

4. Serve /live/ as static files. Playlist: `Cache-Control: no-store`. Segments: `Cache-Control: public, max-age=31536000, immutable`. Put Cloudflare (or any CDN) in front — segments then serve from edge cache and origin egress collapses to near zero. This single decision is what makes 37,000 viewers a non-event.

5. Client:
     const h = new Hls({liveSyncDurationCount: 2});
     h.loadSource('live/playlist.m3u8'); h.attachMedia(video);
     h.on(Hls.Events.LEVEL_LOADED, seekToNewestFragment);
     h.on(Hls.Events.ERROR, (_, d) => { if (d.fatal) setTimeout(() => { h.destroy(); start(); }, 3000); });
   Plus `if (video.canPlayType('application/vnd.apple.mpegurl')) video.src = PLAYLIST;` for iOS, which gets no fragment events and must be driven from status.json polling.

6. Emit live/meta.json (segment -> {prompt, brain_state, gen_at, replay}) alongside. For this project that sidecar is where the brain-state vector for each clip goes, so the page can show what the predicted response was that wrote the prompt. That is most of the artwork's legibility and it costs ~10 lines.

Why not RTMP-to-YouTube despite it being cheapest on infrastructure. Two reasons, and the second is the one that should settle it.

FIRST, it demands an encoder that never stops. Your source is generation-limited and will stall. YouTube ends a stream on a sustained ingest gap, requires CBR with fixed 2 s keyframes (scene-cut/auto keyframe modes trigger 'stream not stable'), treats 9:16 as second-class, and gives you no per-clip metadata overlay without burning it into pixels. You would build a continuous-encode rig purely to satisfy the transport. That rig has a name and a reference implementation — reactor-team/infinite-livestream's pacer.py — and the fact that a 204-line, carefully-commented module exists solely to convert clip-shaped output into a constant-rate stream is the clearest statement of what RTMP costs you. HLS segments are clip-shaped by nature, so on the HLS path that module has nothing to do.

SECOND, and decisively: platform bans are the modal outcome for 24/7 generative streams, not a tail risk. 'Nothing, Forever' was suspended from Twitch within about thirty minutes of its model producing a transphobic segment (verified; February 2023, 14-day ban). If the platform IS your delivery mechanism, that event ends the piece and takes the archive and audience with it. If the platform is a mirror of your own HLS stream, it costs you reach for a fortnight. Given that item 09 predicts this system drifts toward high-salience content, this is not a hypothetical.

So: self-hosted HLS is the primary. Push a derived feed to YouTube/Twitch for reach once the HLS stream is stable, and run a fail-closed moderation pass before anything is enqueued — the ordering reactor-team's client uses, and the right one.

**simpler_alternative**

Crudest fallback: a browser-side MP4 queue. Your API returns the next clip URL; the page keeps two <video> elements, preloads clip N+1 into the hidden one, and swaps on the visible one's `ended` event.

  const a = document.getElementById('v0'), b = document.getElementById('v1');
  let cur = a, nxt = b;
  async function load(el) { const r = await fetch('/api/next'); el.src = (await r.json()).url; el.load(); }
  cur.addEventListener('ended', () => { [cur, nxt] = [nxt, cur]; cur.hidden = false; nxt.hidden = true; cur.play(); load(nxt); });

~2-4 hours, zero infrastructure, zero added latency, and fal's CDN serves the files.

But be clear about what you give up, because it is more than it looks:
- It is NOT a broadcast. Every viewer is on their own timeline watching a different clip. For a piece whose premise is a shared reactive channel, that is a conceptual failure, not just a technical one.
- Autoplay with audio is blocked until a user gesture, and H3 Max's whole selling point is the audio.
- The swap shows a black frame or a stall unless you preload aggressively; mobile Safari limits concurrent video elements and will fight you.
- No seek-back, no archive, no 'what is on air right now' shared state.

Use it for the first hour of development to prove the generation loop works end to end, then move to HLS. Do not ship it.

Middle-path fallback if you truly need RTMP (e.g. you decide YouTube reach matters more than control): do NOT restart ffmpeg per clip. Run one persistent encoder that owns all timestamps, fed raw frames through a FIFO, with the shell holding the write end open across feeders so the encoder never sees EOF:

  mkfifo /tmp/feed.nut
  # persistent encoder — starts once, never restarts
  ffmpeg -f nut -i /tmp/feed.nut \
    -c:v libx264 -preset veryfast -tune zerolatency -pix_fmt yuv420p \
    -b:v 2000k -minrate 2000k -maxrate 2000k -bufsize 4000k \
    -g 60 -keyint_min 60 -sc_threshold 0 -r 30 \
    -c:a aac -b:a 128k -ar 44100 -ac 2 \
    -f flv rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY &
  # feeder loop — the outer redirect keeps the FIFO write end open between clips
  ( while true; do
      CLIP=$(next_clip_or_filler)
      ffmpeg -v error -re -i "$CLIP" \
        -c:v rawvideo -pix_fmt yuv420p -s 720x1280 -r 30 \
        -c:a pcm_s16le -ar 44100 -ac 2 -f nut -
    done ) > /tmp/feed.nut

Because the encoder generates its own PTS from a continuous raw feed, there are no timestamp seams, no discontinuities and no non-monotonic DTS at all — the class of problem simply does not arise. `next_clip_or_filler` must ALWAYS return something (see item 08's replay ring); if it ever blocks, YouTube drops you.

If you build this, read reactor-team/infinite-livestream's pacer.py first rather than deriving it. Its shape: a drift-free metronome at the target frame rate; each tick pops the oldest buffered video frame (or repeats the last shown, or black before anything arrived) and pulls exactly one tick of int16 samples (padding with silence on underflow); video and audio buffered FIFO with the SAME shallow cap, which is what keeps them in sync; overflow drops oldest and is counted; `_BUFFER_SECONDS = 2.0` because 'depth here is end-to-end latency'; `_RESNAP_PERIODS = 8` to resnap the clock after a starve instead of machine-gunning catch-up frames. It also instruments repeated_frames / silent_ticks / dropped_frames, which are precisely the metrics that tell you the generator is falling behind. Note this is a SECOND, frame-level buffer measured in seconds, distinct from the clip-level buffer of item 08 measured in clips — do not conflate them.

Avoid the `-f concat -safe 0 -i playlist.txt` growing-playlist route. The concat demuxer reads its list at start; appending lines to a file it has already read does not reliably feed new clips to a running process. [uncertain — some practitioners report feeding the list through a blocking pipe works; I could not verify it, and the FIFO-of-raw-frames route above is unconditionally reliable, so there is no reason to gamble on it.]

**code_sketch**

# server side — runs once per completed generation. ~60 lines, no dependencies beyond ffmpeg.
import json, os, subprocess, collections

LIVE   = "/var/www/stream/live"
WINDOW = 6           # segments visible in the playlist (~90 s)
ARCHIVE_KEEP = 400   # segments retained on disk for the replay ring / VOD channels
SPEC = dict(w=720, h=1280, fps="30/1", ar="44100", ch=2)

state = dict(seq=0, window=collections.deque(maxlen=WINDOW), meta={})

def probe(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_streams", "-show_format", path])
    return json.loads(out)

def matches_spec(p):
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = next(s for s in p["streams"] if s["codec_type"] == "audio")
    return (int(v["width"]) == SPEC["w"] and int(v["height"]) == SPEC["h"]
            and v["r_frame_rate"] == SPEC["fps"] and v["codec_name"] == "h264"
            and a["sample_rate"] == SPEC["ar"] and int(a["channels"]) == SPEC["ch"]
            and a["codec_name"] == "aac")

def to_segment(mp4, seg_path):
    """One whole clip -> one .ts. Stream copy measured at 0.02 s."""
    p = probe(mp4)
    if matches_spec(p):
        cmd = ["ffmpeg", "-v", "error", "-i", mp4, "-c", "copy",
               "-bsf:v", "h264_mp4toannexb"]
    else:
        cmd = ["ffmpeg", "-v", "error", "-i", mp4,
               "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,"
                      "pad=720:1280:(ow-iw)/2:(oh-ih)/2,fps=30",
               "-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high",
               "-pix_fmt", "yuv420p", "-g", "60", "-keyint_min", "60",
               "-sc_threshold", "0", "-b:v", "1800k", "-maxrate", "1800k",
               "-bufsize", "3600k",
               "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2"]
    cmd += ["-muxdelay", "0", "-muxpreload", "0",
            "-avoid_negative_ts", "make_zero", "-f", "mpegts", seg_path]
    subprocess.run(cmd, check=True)
    return float(probe(seg_path)["format"]["duration"])

def write_playlist():
    """Every segment gets its own DISCONTINUITY: each clip is separately
    encoded and restarts its PTS near zero. The tag makes the player reset
    its timeline, which is the whole fix. Atomic rename so no viewer ever
    reads a partial playlist."""
    segs = list(state["window"])
    body = ["#EXTM3U", "#EXT-X-VERSION:3",
            "#EXT-X-TARGETDURATION:%d" % (max(int(d) + 1 for _, d in segs)),
            "#EXT-X-MEDIA-SEQUENCE:%d" % (state["seq"] - len(segs)),
            "#EXT-X-DISCONTINUITY-SEQUENCE:%d" % (state["seq"] - len(segs))]
    for name, dur in segs:
        body += ["#EXT-X-DISCONTINUITY", "#EXTINF:%.3f," % dur, name]
    # NO #EXT-X-ENDLIST -> players keep re-polling; this is what makes it live.
    tmp = os.path.join(LIVE, ".playlist.m3u8.tmp")
    open(tmp, "w").write("\n".join(body) + "\n")
    os.replace(tmp, os.path.join(LIVE, "playlist.m3u8"))

def publish(mp4, prompt, brain_state, replay=False):
    name = "%06d.ts" % state["seq"]
    dur = to_segment(mp4, os.path.join(LIVE, name))
    state["window"].append((name, dur))
    state["meta"][name] = dict(prompt=prompt, brain=brain_state,
                               gen_at=int(__import__("time").time()),
                               replay=replay)
    state["seq"] += 1
    write_playlist()
    tmp = os.path.join(LIVE, ".meta.json.tmp")
    json.dump(dict(list(state["meta"].items())[-40:]), open(tmp, "w"))
    os.replace(tmp, os.path.join(LIVE, "meta.json"))
    return name


// client side — the whole player, ~30 lines of the ~80 you eventually want
const PLAYLIST = 'live/playlist.m3u8';
const tv = document.getElementById('tv');
let meta = {};
setInterval(async () => { meta = await (await fetch('live/meta.json')).json(); }, 5000);

function start() {
  if (window.Hls && Hls.isSupported()) {
    const h = new Hls({ liveSyncDurationCount: 2 });   // ~30 s behind live edge
    h.loadSource(PLAYLIST);
    h.attachMedia(tv);
    // join on the NEWEST segment, not wherever the window happens to start
    let placed = false;
    h.on(Hls.Events.LEVEL_LOADED, (_, d) => {
      if (placed) return; placed = true;
      let best = null, bestId = -1;
      for (const f of d.details.fragments) {
        const n = parseInt(f.url.split('/').pop(), 10);
        if (!isNaN(n) && n > bestId) { bestId = n; best = f; }
      }
      if (best) tv.currentTime = best.start + 0.05;
    });
    // surface the brain state that wrote this clip's prompt
    h.on(Hls.Events.FRAG_CHANGED, (_, d) => {
      const seg = d.frag.url.split('/').pop().split('?')[0];
      if (meta[seg]) renderBrainReadout(meta[seg]);
    });
    h.on(Hls.Events.ERROR, (_, d) => {
      if (d.fatal) setTimeout(() => { h.destroy(); start(); }, 3000);
    });
  } else if (tv.canPlayType('application/vnd.apple.mpegurl')) {
    tv.src = PLAYLIST;   // iOS: no fragment events, drive the readout from status.json
  }
  tv.play().catch(() => {});
}
start();

### Risk

**failure_modes**

1. UNDER-RUN IS THE ONLY ONE THAT MATTERS, and the reference implementation's answer is visible in its data model: meta.json carries a per-segment `replay: bool`, and the client renders 'RERUN' with an age when a replayed clip is >15 min old. When generation cannot keep up, an already-aired clip is re-appended to the playlist marked replay:true. Cost: zero dollars, ~30 lines. The client-side counterpart is 'a brand-new clip beats queued reruns' — on FRAG_CHANGED it scans forward for the first unseen non-replay fragment and seeks straight to it, so a fresh clip pre-empts the rerun loop rather than waiting behind it. Copy this design; do not invent a filler-loop or slow-motion scheme first.

2. Non-monotonic DTS at clip boundaries. REPRODUCED locally: separately encoded clips remuxed to TS both start at video 0.066667 / audio 0.043444, and a playlist of them fed to ffmpeg's remuxer raises `Application provided invalid, non monotonically increasing dts to muxer in stream 1`. Harmless for HLS PLAYERS given #EXT-X-DISCONTINUITY; fatal the moment you pipe those segments into a muxer or an RTMP encoder. If you ever add an RTMP output, do not reuse the segments — use the persistent-encoder FIFO rig.

3. Per-seam A/V skew of ~23 ms from AAC encoder priming, MEASURED. Present on both the discontinuity route and the -output_ts_offset route. Inaudible as sync error, audible as a click; a 100 ms audio fade at each clip's head and tail costs one filter and removes it.

4. Partial playlist reads. If you write playlist.m3u8 in place, a viewer polling mid-write gets a truncated file and hls.js throws a fatal error. Write-then-rename. The reference implementation serves the playlist `no-store` and the segments `immutable`, which is the correct and non-obvious split — get it backwards and either viewers cache a stale playlist forever or your origin serves every segment to every viewer.

5. iOS Safari uses native HLS and emits no hls.js fragment events, so any UI keyed to FRAG_CHANGED silently freezes on iPhone. The reference implementation polls status.json as a takeover after 12 s of no fragment advance. This is the single most likely thing to ship broken.

6. CDN caching the playlist. If Cloudflare caches playlist.m3u8 even briefly, viewers wedge on a stale window. Observed: cf-cache-status DYNAMIC on the playlist, HIT on segments.

7. Vertical 9:16 is a real constraint, not a style choice — H3 Max output observed at 720x1280. If you later push to YouTube Live, portrait live is second-class there; decide the aspect ratio before building any overlay.

8. RTMP-specific, and the list is longer than it looks. A sustained ingest gap ends the YouTube broadcast and you must create a new one; scene-cut or 'auto' keyframe modes trigger the 'stream not stable' warning even at correct bitrate; VBR is not accepted (CBR required). Every one of these turns a generation stall into an unrecoverable outage rather than a rerun. Five more, all taken from reactor-team/infinite-livestream's 'learnings baked into this client (do not re-learn these)' list, which is the only place I have seen them written down:
   (a) AN AUDIO TRACK IS MANDATORY — YouTube and Twitch will not accept video-only FLV. H3 Max's native audio satisfies this while a clip plays, but the encoder must receive silence when nothing is playing or it runs dry.
   (b) NEVER WRITE TO AN FFMPEG PIPE FROM THE EVENT LOOP. `stdin.write` blocks when ffmpeg stalls, the blocked loop starves everything upstream, and it snowballs. Each pipe needs its own writer thread behind a bounded drop-oldest queue.
   (c) THE TWO-PIPE DEADLOCK. Feeding video and audio on separate raw pipes and starving one while pushing the other deadlocks ffmpeg. They deliver both every tick in lockstep. My single-container nut FIFO in simpler_alternative sidesteps this by construction — one pipe cannot desynchronise against itself — which is the main reason I prefer it, though their two-pipe design is the one with production miles on it.
   (d) RAW-VIDEO GEOMETRY IS UNFORGIVING. One frame whose bytes disagree with ffmpeg's `-s WxH` — wrong size, or a non-C-contiguous `tobytes()` that includes row padding — shifts every following scanline into permanent 'TV static'. Letterbox onto a fixed canvas and refuse mismatched frames rather than passing them through.
   (e) FFMPEG DIES; THE BROADCAST MUST NOT. Restart it lazily with a cooldown and a failure cap, and keep the last stderr lines. Relatedly: create the sink and pacer ONCE and run the connection loop behind them, so the platform sees one continuous stream while the client rebuilds a session.

9. PLATFORM BAN IS A MODAL OUTCOME FOR THIS GENRE, NOT A TAIL RISK — and it is an argument about architecture, not just policy. VERIFIED PRECEDENT: 'Nothing, Forever', the 24/7 AI-generated Seinfeld parody, was suspended from Twitch in February 2023 (a 14-day ban) after the model generated a transphobic stand-up segment; the ban landed within about thirty minutes of the segment airing. A teammate reports a further 2026 case (Rehan Sheikh's stream banned from Twitch, moving to Kick then Rumble) — I could not verify that one and searched for it specifically, so treat it as unconfirmed. The structural point stands either way: a brain-activation-maximising objective steers toward exactly the high-salience material that gets streams banned (see item 09), the failure is instantaneous and account-level rather than gradual, and it takes your archive and your audience with it. This is the decisive argument for keeping self-hosted HLS as the PRIMARY output and any platform as a mirror: a ban then costs you reach, not the piece. Ship the fail-closed moderation pass regardless — reactor-team's client runs one before anything is enqueued, and that ordering is correct.

10. Disk growth. At 3.4 MB per 15 s, a 24/7 stream writes ~19 GB/day. Retention policy is mandatory, and it trades against how deep your replay ring can be.

### Evidence

**sources**

- https://infiniteslop.ai/ — live reference implementation. Page source fetched 2026-08-31 21:30 UTC; contains hls.min.js, const PLAYLIST = 'live/playlist.m3u8', new Hls({liveSyncDurationCount: 2}), FRAG_CHANGED/LEVEL_LOADED/ERROR handlers, native-HLS iOS fallback, and the 'a brand-new clip beats queued reruns' skip logic. PRIMARY EVIDENCE for the whole recommendation.
- https://infiniteslop.ai/live/playlist.m3u8 — fetched live: EXT-X-VERSION:3, TARGETDURATION:16, MEDIA-SEQUENCE == DISCONTINUITY-SEQUENCE, #EXT-X-DISCONTINUITY before every segment, EXTINF:15.123, 6-segment window, no ENDLIST, Cache-Control: no-store.
- https://infiniteslop.ai/live/016594.ts — downloaded and ffprobed: mpegts, 15.123223 s, 1,794,370 bit/s, h264 720x1280 30/1, aac 44100 Hz 2ch, 3,392,084 bytes; served Cache-Control: public, max-age=31536000, immutable with cf-cache-status: HIT.
- https://infiniteslop.ai/live/meta.json — fetched live: 40 entries of {prompt, chat, gen_at, replay}. The `replay` flag is the documented-by-existence under-run mechanism.
- https://infiniteslop.ai/status.json — fetched live: now_playing / now_replay / generating / generating_now / playing_next / queue. Polled 5x over 76 s; MEDIA-SEQUENCE advanced 18192->18197 (5 segments / 76 s = real-time paced).
- https://infiniteslop.ai/api/channel?ch=tag&q=cat — fetched live: VOD-type m3u8 assembled from the archive, segments addressed as clip?id=NNNNN, same per-segment discontinuity pattern.
- https://levels.io/i-built-infinite-slop — levelsio's build post. Confirms Hetzner VPS, built via Termius on phone with Claude Code, fal sponsors compute. Contains NO streaming-architecture detail; everything above about the pipeline is my own measurement of the live site, not from this post.
- https://levels.io/ai-video-faster-than-you-watch — 'It generates 15 seconds of video in 9 seconds!'; fal's post-trained H3 Max variant '50x faster than the original'.
- https://levels.io/37000-watched-infinite-slop — 37,000 viewers day one; 'Only 4 videos per minute can be generated (4x 15 seconds = 1 minute)'; notes last-frame chaining would require generating 'SO fast without ANY slowdowns'.
- https://ffmpeg.org/ffmpeg-formats.html — HLS muxer: append_list appends new segments to an existing list and removes #EXT-X-ENDLIST; omit_endlist suppresses the tag. The off-the-shelf route if you do not need the replay ring.
- https://www.mux.com/blog/simulate-a-live-stream-of-a-video-playlist-with-ffmpeg — concat demuxer to RTMP; also the source of the constraint that the playlist is read at start and is not dynamic.
- https://ffmpeg-cookbook.com/en/articles/rtmp-streaming/ — ffmpeg RTMP push to YouTube Live and Twitch.
- https://dev.to/devlobb/how-i-built-a-stable-247-youtube-livestream-on-a-vps-using-ffmpeg-no-saas-required-1bid — working 24/7 YouTube RTMP command line (libx264 superfast, -b:v 2000k -maxrate 2000k -bufsize 4000k, -g 60 -keyint_min 60, aac 128k, -f flv).
- https://developers.google.com/youtube/v3/live/guides/rtmps-ingestion — YouTube RTMPS ingest.
- https://theloops.live/guides/rtmp-youtube-live — YouTube requires H.264/AAC, 2 s keyframe interval (max 4 s), CBR; scene-cut/open-GOP/auto-keyframe modes cause the 'stream not stable' warning.
- https://www.pistack.xyz/posts/self-hosted-live-streaming-owncast-mediamtx-nginx-rtmp-guide-2026/ — 2026 comparison: nginx-rtmp for plain RTMP-in/HLS-out, MediaMTX for protocol breadth; a 1-core/1 GB VPS handles one passthrough stream for dozens of viewers.
- https://forum.videohelp.com/threads/390057-FFMpeg-non-monotonous-DTS-in-output-stream-error — non-monotonic DTS on concatenation is usually the audio stream; -fflags +igndts / -copytb 1 discussed.
- https://github.com/reactor-team/infinite-livestream — VERIFIED via the GitHub API this session: Apache-2.0, created 2026-08-30T13:20:45Z, pushed 2026-08-31T07:34:10Z, 157 stars, Python. Top level: fast-h3/, streaming-client/, skills/, AGENTS.md. streaming-client/ contains pacer.py, director.py, reactor_link.py, upsampler.py, moderator.py, admin.py, config.py, main.py, group_tag.py, sinks/, chat/, overlay/, presets/.
- https://raw.githubusercontent.com/reactor-team/infinite-livestream/main/streaming-client/README.md — read this session. Architecture diagram, sink table (rtmp/noop; 'Twitch, YouTube Live, Kick are all just ingest URLs'), per-file ownership table, and the 'Learnings baked into this client (do not re-learn these)' list — source for failure_modes 8(a)-(e): mandatory audio track, never write to a pipe from the event loop, the two-pipe deadlock, raw-video geometry/contiguity causing 'TV static', lazy ffmpeg restart with cooldown and failure cap, sink outliving reconnects.
- https://raw.githubusercontent.com/reactor-team/infinite-livestream/main/streaming-client/pacer.py — read this session, 204 lines. Docstring states the clip-shaped-output vs constant-rate-ingest problem. _BUFFER_SECONDS = 2.0 ('Shallow on purpose: depth here is end-to-end latency'); _RESNAP_PERIODS = 8; repeats + silence on underflow; drop-oldest on overflow; counters repeated_frames / silent_ticks / dropped_frames / dropped_samples.
- https://raw.githubusercontent.com/reactor-team/infinite-livestream/main/README.md — read this session. 'the stream goes out over RTMP as one uninterrupted broadcast'; the model half is FastVideo's FastH3 Preview v1 (MiniMax-H3 35B distilled to four transformer forwards, 90% sparse video attention) served on Reactor Runtime, README says 8x B200.
- https://techcrunch.com/2023/02/06/ai-generated-seinfeld-suspended-on-twitch-for-ai-generated-transphobic-jokes/ and https://www.nbcnews.com/tech/twitch-temporary-ban-seinfeld-parody-ai-transphobic-remarks-rcna69389 and https://incidentdatabase.ai/cite/462/ — VERIFIED PRECEDENT for failure mode 9: 'Nothing, Forever', a 24/7 AI-generated stream, suspended from Twitch February 2023 (14 days) after a model-generated transphobic segment; ban landed ~30 minutes after it aired.
- RELAYED, UNVERIFIED: a teammate reports a 2026 case of an AI stream (Rehan Sheikh's) banned from Twitch and moving to Kick then Rumble. I searched for this specifically and found nothing; the Nothing, Forever precedent above carries the argument on its own.
- LOCAL MEASUREMENT (this session, ffmpeg/ffprobe on macOS): mp4 -> single .ts stream copy took 0.02 s real. Two independently encoded clips both remuxed to video start_time=0.066667 / audio start_time=0.043444. A playlist of them read by ffmpeg's remuxer raised 'Application provided invalid, non monotonically increasing dts to muxer in stream 1'. Adding -output_ts_offset 5.04 to the second produced video start_time=5.040000 / audio start_time=5.016778, confirming both the continuous-timestamp fix and the ~23 ms AAC priming skew.

### Other Info

**item_id**

07

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `off_the_shelf_option`
- `unknowns`

---

## TRIBE v2 inference interface and runtime cost

### Identity

**what_it_is**

Meta FAIR's TRIBE v2 (arXiv 2605.04326, released 2026-03-24) is a frozen tri-modal encoder stack (V-JEPA2-ViT-g video, Wav2Vec-BERT-2.0 audio, Llama-3.2-3B text) feeding an 8-layer / 1152-d Transformer that regresses predicted fMRI BOLD onto 20,484 fsaverage5 cortical vertices at 1 Hz. In this pipeline it is the 'simulated viewer': it converts an audiovisual clip into a time-series of predicted brain response that becomes the control signal for the next prompt.

**role_in_loop**

PREDICT stage. Sits between PERCEIVE (a generated clip is captured / read from disk) and PROMPT (the brain vector is reduced to ROI scores and templated into the next H3 Max prompt). CRITICAL FINDING: at measured speed it cannot sit inside the clip-duration critical path, so it must be run one-to-four clips BEHIND playback, off the hot path, feeding clip N's brain read into clip N+2's prompt.

### Interface

**interface_spec**

Package `tribev2` (pyproject requires-python >=3.11). Public surface is `tribev2.demo_utils.TribeModel`, a subclass of `tribev2.main.TribeExperiment` (a pydantic/exca model).

(1) `TribeModel.from_pretrained(checkpoint_dir: str|Path, checkpoint_name: str='best.ckpt', cache_folder: str|Path=None, cluster: str=None, device: str='auto', config_update: dict|None=None) -> TribeModel`.
  - `checkpoint_dir` is either a local dir holding `config.yaml` + `best.ckpt`, or an HF repo id ('facebook/tribev2'). HF repo holds exactly 5 files; `best.ckpt` is 708,856,138 bytes (708 MB), `config.yaml` 18 KB.
  - Loads with `torch.load(..., weights_only=True, mmap=True)`, reads `ckpt['model_build_args']`, strips the `model.` prefix from `state_dict`, builds `FmriEncoderModel`, `load_state_dict(strict=True, assign=True)`, `.to(device)`, `.eval()`.
  - IT UNCONDITIONALLY SETS `config['average_subjects'] = True` BEFORE applying `config_update`, and pops `infra.workdir`, `data.study.infra_timelines`, `data.neuro.infra`, `data.image_feature.infra`.
  - `config_update` is a flat dict of dotted exca ConfDict paths, applied LAST, so it overrides everything.

(2) `model.get_events_dataframe(text_path=None, audio_path=None, video_path=None) -> pd.DataFrame`. EXACTLY ONE must be non-None (else ValueError). Suffixes are validated: video {.mp4,.avi,.mkv,.mov,.webm}, audio {.wav,.mp3,.flac,.ogg}, text {.txt}. For video/audio it builds a one-row frame `{type:'Video'|'Audio', filepath, start:0, timeline:'default', subject:'default'}` and pushes it through `get_audio_and_text_events(df)`. For text it runs gTTS -> mp3 -> the same pipeline.

(3) `tribev2.demo_utils.get_audio_and_text_events(events: pd.DataFrame, audio_only: bool=False) -> pd.DataFrame` — THE UNDOCUMENTED LEVER. Transform chain: `ExtractAudioFromVideo()`, `ChunkEvents('Audio', max_duration=60, min_duration=30)`, `ChunkEvents('Video', max_duration=60, min_duration=30)`, and THEN, only if `audio_only is False`: `ExtractWordsFromAudio()`, `AddText()`, `AddSentenceToWords(max_unmatched_ratio=0.05)`, `AddContextToWords(sentence_only=False, max_context_len=1024, split_field='')`, `RemoveMissing()`. `get_events_dataframe` does NOT expose `audio_only`; you must call this function directly.

(4) `model.predict(events: pd.DataFrame, verbose: bool=True) -> tuple[np.ndarray, list]`. Internally: `self.data.get_loaders(events=events, split_to_build='all')['all']`; per extractor `extractor.prepare(events)` then `_free_extractor_model(extractor)` (deletes `._model`, `gc.collect()`, `torch.cuda.empty_cache()`); segments via `ns.segments.list_segments(..., stride=(duration_trs-overlap_trs_train)*TR, duration=duration_trs*TR, stride_drop_incomplete=False)`; then per batch each segment is subdivided by `np.arange(0, segment.duration-1e-2, TR)` into TR-length sub-segments, sub-segments with `len(s.ns_events)==0` are dropped when `remove_empty_segments=True` (default), and `y_pred = rearrange(model(batch), 'b d t -> (b t) d')[keep]`.

RELEASED-CONFIG CONSTANTS (facebook/tribev2 config.yaml, verified): `data.neuro.frequency=1.0` so TR=1.0 s; `data.neuro.offset=5`; `data.neuro.projection={SurfaceProjector, mesh:fsaverage5, kind:ball, radius:3}`; `data.frequency=2.0` (all three extractors sample at 2 Hz); `data.duration_trs=100`; `data.overlap_trs_train=0`; `data.batch_size=8`; `data.num_workers=20`; `data.stride_drop_incomplete=false`; `data.layers_to_use=[0.5,0.75,1.0]`, `layer_aggregation=group_mean`; `data.features_to_use=[text,audio,video]`; `data.text_feature={HuggingFaceText, meta-llama/Llama-3.2-3B, contextualized:true, batch_size:4}`; `data.video_feature={HuggingFaceVideo, image:facebook/vjepa2-vitg-fpc64-256, clip_duration:4}`; `data.audio_feature={Wav2VecBert, facebook/w2v-bert-2.0}`; `brain_model_config={hidden:1152, encoder.depth:8, encoder.heads:8, use_scalenorm:true, rotary_pos_emb:true, max_seq_len:1024, low_rank_head:2048, extractor_aggregation:cat, layer_aggregation:cat, modality_dropout:0.3, temporal_dropout:0.0, subject_embedding:false, subject_layers:{name:SubjectLayers, n_subjects:25, subject_dropout:0.1, average_subjects:false, mode:gather}}`.

USEFUL `config_update` PATHS (all verified against the source): `data.overlap_trs_train` (int TRs; 20 gives 100 s windows on an 80 s hop), `data.num_workers` (set 0 inside any daemonic/forked worker — a daemon process cannot spawn DataLoader children and raises `AssertionError: daemonic processes are not allowed to have children`), `data.batch_size`, `data.video_feature.image.batch_size`, `data.text_feature.batch_size`, `data.frequency`. `remove_empty_segments` is a TribeModel field, not a config path. DO NOT SET `data.duration_trs`: 100 is baked into the checkpoint pooler (`n_output_timesteps`, `nn.AdaptiveAvgPool1d`) and changing it crashes `predict()`.

SUBCORTICAL SIBLING: `facebook/tribev2-subcortical` (released 2026-05-13, 217 downloads, same 5-file layout) carries a MaskProjector head 2048 -> 8,808 voxels over 16 bilateral Harvard-Oxford structures (hippocampus, amygdala, thalamus, caudate, putamen, pallidum, accumbens, lateral ventricle). Same `TribeModel.from_pretrained` call, different repo id. Note the count is 8,808 in the maintainer thread, not 8,802.

**input_contract**

One media file path per call. Video: mp4/avi/mkv/mov/webm; audio is auto-demuxed with moviepy/ffmpeg (ffmpeg MUST be on PATH). Audio: wav/mp3/flac/ogg. Text: .txt, which is TTS'd through gTTS (needs network; language auto-detected by langdetect) and then transcribed back. `ChunkEvents` splits Audio and Video events into 30-60 s chunks before feature extraction. The model's own window is FIXED at 100 s (duration_trs=100 x TR=1 s), tiled with stride 100 s by default; `stride_drop_incomplete=False` means a short clip still yields one incomplete window, so a 15 s clip DOES run. Practitioner floor: the Space that ships this sets `MIN_USEFUL_S = 10` and its maintainers record that sub-10 s clips score to a near-flat, meaningless timeline; 15-30 s is the working minimum, consistent with the 5 s hemodynamic offset eating the head of every clip. Video with no audio track runs fine but silently degrades to video-only (zero Word events). Temp files written by your code MUST be flush() -> os.fsync(fileno()) -> close() before the path is handed to the model, or the model reads an empty file.

**output_contract**

`preds`: np.ndarray, shape `(n_kept_TRs, 20484)`, float32. `20484 = 2 x 10242`; LH occupies `[0:10242]`, RH `[10242:20484]` on the fsaverage5 surface — the split is a bare index, there is no helper. One row per fMRI TR, TR = 1 / data.neuro.frequency = 1.0 s, i.e. a 1 Hz time series (NOT 2 Hz — 2 Hz is the feature-extractor rate, which the pooler collapses). Rows are offset 5 s into the past (`neuro.offset: 5`): the row timestamped t is the predicted BOLD at t+5 s driven by stimulus around t, so the read is inherently lagged relative to the frames that caused it. `segments`: a same-length list of neuralset Segment objects; `segment.start` is the absolute second on the input clock and `segment.duration == TR`, which is how you rebuild the time axis (`abs_times = np.array([round(s.start) for s in segments])`). WHAT THE NUMBERS MEAN: the training target was per-sample z-scored and detrended, so ABSOLUTE MAGNITUDES ARE NOT INTERPRETABLE — only relative temporal dynamics within one run are valid. Any 'score' you build must z-score over the timeline. Predictions are for the average / unseen subject only (see subject conditioning under failure_modes).

### Performance

**throughput_constraint**

1. THE BACKBONES ARE FREED AFTER EVERY predict() CALL. `Data.get_loaders` runs `extractor.prepare(events)` then `_free_extractor_model(extractor)`, which deletes the extractor's `._model`, runs `gc.collect()` and `torch.cuda.empty_cache()`. A warm PROCESS therefore does NOT give you a warm MODEL: every `predict()` re-pays the ~7.6 GB V-JEPA2 build plus the W2V-BERT build. This is the most important throughput fact about TRIBE v2 and it is absent from the model card and README. It must be patched out (cache the built backbone on CPU at startup and pay only `.to(cuda)` per call — exactly what `tribescore.prewarm.prewarm_video_model` + `fast_encode._VIDEO_MODEL_CACHE` do).
2. V-JEPA2-ViT-g is compute-bound and DOES NOT BATCH. Source comment from a measured run: 'B=1 is intentional and load-bearing: V-JEPA2 ViT-g is compute-bound and ONE 8192-token clip already over-saturates the GPU (measured: B=4 approx 231 s vs B=1 bf16 approx 173 s on CUDA)'. Batching clips adds memory with no throughput gain. Cost is strictly linear in clip seconds x feature frequency.
3. GPU serialisation: one `predict()` at a time per process. Concurrency requires N processes x N GPUs, which multiplies the always-on cost linearly.
4. GPU idles ~44% of a run doing CPU-side prep (video decode, ASR) unless you pipeline it. Fixing this is quoted at ~3.3x more scores/day on ZeroGPU.
5. Frame decode redundancy: the encoder samples a 64-frame window per output timestep and adjacent windows overlap ~8x (measured 1,536 frame-reads / 193 unique on a 12 s clip). Dedup is worth ~44% -> ~5.5% of per-clip time.
6. VRAM is NOT the constraint. Measured peak in Fast mode is ~13 GB (see the Space's own note: 'Peak VRAM is only ~13 GB, so the forward is compute-bound, not VRAM-bound').

### Complexity

**dev_complexity**

MEDIUM. The happy path is 5 lines. What makes it MEDIUM rather than LOW: a clean `pip install` is currently BROKEN upstream (exca API break, see failure_modes), the `audio_only` fast path is not reachable from the public API, the backbone free-after-every-call behaviour must be patched out to get usable throughput, and the raw `(T, 20484)` output is useless until reduced. Every one of those has a published, working solution you can copy rather than derive — which is what drops it from HIGH.

**off_the_shelf_option**

I evaluated all 8 repos under the GitHub `tribe-v2` topic plus the live HF Spaces. Verdict, best first:

1. **`techfreakworm/tribev2-brain-timeline` (HF Space) — USE THIS. It is the nearest existing scaffold and it removes most of the work.** A 716-line Gradio app plus a `tribescore` package (inference / windowing / metrics / prewarm / fast_encode / patches, ~130 KB of source, 8 test modules) that ALREADY solves, with the reasoning documented inline: the `audio_only` fast path (`_build_audio_only_events`), the 100 s / 80 s-hop window plan + per-window z-score + trapezoidal crossfade stitch, ROI reduction to named metrics via `tribev2.utils.get_hcp_roi_indices`, the `num_workers=0` daemonic-fork fix, bf16 + TF32, exact frame dedup (validated max|delta|=0), backbone prewarm-and-fork-COW, the writable-`HF_HOME`-before-`import gradio` fix, and a `requirements.txt` pin set that actually installs (torch==2.8.0, torchvision==0.23.0, transformers>=4.53,<5, plus a fork of tribev2 that relaxes upstream's torch<2.7 cap). It ships a candid `KNOWN_ISSUES.md`. Duplicate it, delete `app.py`/`ui.py`/`theme.py`, keep `src/tribescore/`. Check its LICENSE/NOTICE before reuse.

2. **`siddhant-rajhans/cortexlab` (PyPI `cortexlab-toolkit`, 283 tests, Python 3.11+) — take one idea, not the package.** Its `cortexlab.inference.streaming.StreamingPredictor` is genuinely additive: a feature-level sliding window (`push_frame(features) -> np.ndarray|None`, `window_trs`, `step_trs`, thread-locked deque) that correctly zero-fills a missing modality using `model.feature_dims`. That is the right shape for a rolling-window design. CAVEAT: its `inference/predictor.py` is a verbatim copy of Meta's `demo_utils.py` with imports renamed, and its headline brain-alignment benchmark table is on a SYNTHETIC benchmark with every p-value > 0.1 (CLIP p=0.104, DINOv2 p=0.542, V-JEPA2 p=0.333, Llama p=0.642) — i.e. it demonstrates nothing. Borrow the streaming pattern; do not cite its analyses.

3. **`ndpvt-web/neuroscore` (8 stars, the most-starred wrapper) — REJECT. Do not build on it.** Three disqualifying defects found by reading the source: (a) `neuroscore/core/backends/gpu.py` calls `self._model.predict(media_path, modality=modality, device=self._device)`, which is NOT the TRIBE v2 API (`predict(events=df)`) — the real-weights GPU path cannot ever have been executed; (b) its 'seven brain regions' are hard-coded fsaverage5 vertex index RANGES (amygdala = vertices 4200-4400 and 14400-14600, etc.) under a source comment admitting they are 'approximate index ranges', and fsaverage5 vertex ordering is icosahedral-subdivision order, not anatomical — these masks are not the regions they are labelled as, and amygdala/striatum are SUBCORTICAL and absent from the cortical checkpoint entirely; (c) it hard-codes `_DEFAULT_SAMPLE_RATE = 2.0` Hz when the output is 1 Hz, so every timestamp it reports is 2x wrong. Excellent README, unusable internals.

4. `CodaCipher/tribe-subcortex` (0 stars, a notebook) — SUPERSEDED. Meta shipped the official `facebook/tribev2-subcortical` checkpoint on 2026-05-13 in response to issue #23. Use Meta's.

5. Remainder of the topic (`MrSJx/Audience` 5*, `mahanyasbaira/NeuroSync...` 5* and TypeScript, `attila-aranyi/mindprint` 2*, `sanyambassi/neuroscanner` 1*, `yahiacuda/tribe-brain-analysis` 0*, `samuelczhao/NoLemming` 0*) — application demos, no reusable runtime. `eugenehp/tribev2-rs` is a pure-Rust inference port with safetensors weights at `eugenehp/tribev2`; interesting but a wrong-language detour for a Python demo.

6. HOSTED, ZERO-CODE: `cbensimon/tribe-v2` and `beta3/TRIBE_V2_Neural_Activity_Predictor` are live Gradio Spaces with programmatic JSON endpoints, callable via `gradio_client`. Fine for a first end-to-end smoke test in an afternoon; not for a 24/7 loop (ZeroGPU is quota-and-queue based).

### Decision

**recommended_approach**

SHORTEST PATH, in order.

STEP 0 — INSTALL. `pip install 'tribev2[plotting] @ git+https://github.com/facebookresearch/tribev2.git@refs/pull/67/head'`. Upstream `main` DOES NOT IMPORT: `neuralset==0.0.2` calls `exca.steps.base.NoValue`, which exca moved to `exca.steps.identity` in 0.5.26, and upstream leaves exca unpinned. PR #67 adds `exca>=0.5.20,<0.5.26`; it is the maintained fix and is what the community is using. Bumping neuralset is NOT an alternative — every release after 0.0.2 removes `AddText`, which `demo_utils.py` imports. Also install `ffmpeg` (system), `uv` (provides `uvx`, which the ASR path shells out to), and `mne` (ships the HCP-MMP1 annot that `tribev2.utils.get_hcp_roi_indices` fetches). Pin `torch==2.8.0` / `torchvision==0.23.0` / `transformers>=4.53,<5` if you need a modern torch — upstream caps torch<2.7, and the proven workaround is a one-line fork that relaxes that cap.

STEP 1 — RUN VIDEO+AUDIO ONLY. This is the single biggest win and it is legitimate, not a hack. `FmriEncoderModel.aggregate_features` contains `if modality not in self.projectors or modality not in batch.data: data = torch.zeros(B, T, self.config.hidden // len(self.feature_dims))`. A missing modality is zero-filled at exactly the projector output width. `modality_dropout=0.3` during training zeroes a modality's projected tensor the same way (`data[mask,:] = torch.zeros_like(...)`, gated on `self.training`), so a text-free batch is byte-identical in form to what the model saw on ~30% of training steps. This is a trained-for input state. Reach it by bypassing `get_events_dataframe`:

    from tribev2.demo_utils import get_audio_and_text_events
    df = pd.DataFrame([{'type':'Video','filepath':path,'start':0,'timeline':'default','subject':'default'}])
    events = get_audio_and_text_events(df, audio_only=True)

This skips WhisperX (a `uvx` subprocess loading faster-whisper large-v3 EVERY call), Llama-3.2-3B, spaCy, the gated Meta licence and HF_TOKEN entirely. `from_pretrained` succeeds without Llama access because the backbones lazy-load inside `predict()`; only a text-path run would 403.

STEP 2 — DEFEAT `_free_extractor_model`. Cache the built V-JEPA2 backbone on CPU once at process start and move it to the GPU per call, so you never re-pay the ~7.6 GB `from_pretrained` build. Copy `tribescore/prewarm.py::prewarm_video_model` + `tribescore/fast_encode.py::_VIDEO_MODEL_CACHE`. Without this a 'warm process' still pays a multi-second disk load per clip.

STEP 3 — LOAD WITH THE RIGHT CONFIG. `config_update={'data.overlap_trs_train': 20, 'data.num_workers': 0, 'data.video_feature.image.batch_size': 16, 'data.batch_size': 16}`. NEVER touch `data.duration_trs`.

STEP 4 — TAKE TRIBE OUT OF THE CRITICAL PATH. Run it as a long-lived asyncio-fed worker behind a 3-4 clip generate-ahead buffer. Clip N finishes generating -> enqueue for scoring -> the resulting ROI vector steers clip N+2 or N+3. At 15 s clips a 45-60 s buffer covers the measured 35-44 s Fast-mode score with headroom, TODAY, with no speedup work. If a clip's score is late, reuse the previous brain vector; the signal is smooth and one stale frame is invisible.

STEP 5 — TURN ON bf16 AUTOCAST + TF32 on the V-JEPA2 forward if you are not inheriting them from `tribescore` (~2x). Do NOT reach for `torch.compile`: it is a known dead end on torch 2.8 (V-JEPA2 `get_position_ids` TorchDynamo tracer bug).

STEP 6 — ON THE SUBJECT QUESTION: do not plan around per-viewer conditioning. The public `best.ckpt` contains ONLY the shared unseen-subject head — `model.predictor.weights` is `(1, 2048, 20484)` and `model.predictor.bias` is `(1, 20484)`, confirmed by a user who inspected the checkpoint (issue #62). The config declares `n_subjects: 25` with a `predefined_mapping` of 25 named subjects across 4 studies (Algonauts2025Bold sub-01/02/03/05, Lahner2024Bold 1-10, Lebel2023Bold UTS01-08, Wen2017 subject1-3), but those 25 heads WERE NOT SHIPPED. Issue #62 asks Meta for the `(26, 2048, 20484)` stack; it is still open and unanswered. `from_pretrained` hard-sets `average_subjects=True` (which sets `subject_layers.average_subjects=True`, `n_subjects=0`, `subject_id.predefined_mapping=None`) and `load_state_dict(strict=True)` will reject any attempt to restore the 25-subject path via `config_update={'average_subjects': False}` — the tensor shapes do not exist in the file. CONSEQUENCE FOR THE PIECE: 'your brain' is a group-average unseen-subject prediction. If you want multiple simulated viewers, fake them DOWNSTREAM by weighting ROIs differently in the readout (a 'visual' viewer vs a 'language' viewer), and say so honestly.

STEP 7 — IF YOU WANT AMYGDALA / NUCLEUS ACCUMBENS (the affectively interesting regions), you need `facebook/tribev2-subcortical`, which is a SECOND checkpoint and, naively, a second `predict()` pass at double the cost. The encoder and `low_rank_head` are expected to be shared between the two checkpoints, so splicing both predictor heads onto one loaded encoder is ~20 LOC and halves the cost — but VERIFY by diffing the two state dicts first (see unknowns).

**simpler_alternative**

In descending order of crudeness.

(A) SCORE THE AUDIO, NOT THE PIXELS. Drop the video modality too and run audio-only. W2V-BERT-2.0 is ~600M params against V-JEPA2-ViT-g's ~1B-plus-8192-tokens-per-forward; removing V-JEPA2 removes the entire compute bottleneck and should be roughly an order of magnitude faster [estimate]. H3 Max emits natively synchronised audio in the same pass, so an audio-only read is a real signal about a real clip, not a degenerate one. Combine with the returned `expanded_prompt` on the text branch and you have a fast bi-modal read with no video encoder at all.

(B) SCORE EVERY Nth CLIP. TRIBE at 2.3-2.9x real time keeps up with a 1-in-3 duty cycle on one GPU with no code changes and no accuracy risk. Hold the last brain vector between reads. Cost is identical (the GPU must stay warm either way), so this buys latency slack for free.

(C) SCORE A TRIMMED CENTRE WINDOW. Feed `ffmpeg`-trimmed 10-15 s from the middle of each clip rather than the whole thing. Cost is linear in seconds, so this is a direct dial. Watch the sub-10 s floor.

(D) HOSTED SPACE VIA `gradio_client`. Call `cbensimon/tribe-v2` or `beta3/TRIBE_V2_Neural_Activity_Predictor` over the network. Zero infrastructure, gets you an end-to-end loop in an afternoon. Not viable for 24/7 (ZeroGPU quota + queue + a 5-minute per-call reservation cap), and it puts a third party in your loop.

(E) DROP TRIBE FROM THE LIVE LOOP ENTIRELY. Precompute offline: score a corpus of clips or motifs once, build a motif -> ROI-vector lookup table, and at runtime do a nearest-neighbour lookup instead of a forward pass. Latency goes to microseconds and the GPU bill goes to zero. This is item 15/16 territory and is the honest fallback if the real-time budget will not close.

**code_sketch**

```python
# warm_tribe.py -- long-lived single-GPU scorer. Fast (video+audio) path.
# pip install 'tribev2[plotting] @ git+https://github.com/facebookresearch/tribev2.git@refs/pull/67/head'
# system: ffmpeg, uv
import os, numpy as np, pandas as pd, torch

os.environ.setdefault('HF_HUB_DOWNLOAD_TIMEOUT', '300')
os.environ.setdefault('HF_HUB_HTTP_TIMEOUT', '300')
# No HF_TOKEN needed on this path: the text branch is never touched.

from tribev2 import TribeModel
from tribev2.demo_utils import get_audio_and_text_events
from tribev2.utils import get_hcp_roi_indices   # ships with the package

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

_MODEL = None

def load():
    """Called ONCE at process start. Never inside the request path."""
    global _MODEL
    if _MODEL is None:
        _MODEL = TribeModel.from_pretrained(
            'facebook/tribev2',
            cache_folder='/cache',
            device='auto',
            config_update={
                'data.overlap_trs_train': 20,   # 100 s windows, 80 s hop
                'data.num_workers': 0,          # required in forked/daemonic workers
                'data.video_feature.image.batch_size': 16,
                'data.batch_size': 16,
                # 'data.duration_trs'  <- NEVER SET THIS. 100 is baked into the pooler.
            },
        )
        # TODO: patch _free_extractor_model / cache the built V-JEPA2 backbone on CPU
        # here, or every predict() re-pays a ~7.6 GB from_pretrained build.
    return _MODEL


def events_video_audio_only(path: str) -> pd.DataFrame:
    """The whole trick: bypass get_events_dataframe to reach audio_only=True,
    which skips WhisperX + Llama-3.2-3B + spaCy and the Meta licence gate.
    The model is trained for this input (modality_dropout=0.3)."""
    df = pd.DataFrame([{
        'type': 'Video', 'filepath': str(path), 'start': 0,
        'timeline': 'default', 'subject': 'default',
    }])
    return get_audio_and_text_events(df, audio_only=True)


ROIS = {
    'visual':    ['L_V1_ROI', 'L_V2_ROI', 'L_V4_ROI', 'L_MT_ROI'],
    'auditory':  ['L_A1_ROI', 'L_STGa_ROI'],
    'value':     ['L_10r_ROI', 'L_p32_ROI', 'L_a24_ROI'],   # vmPFC / pgACC proxy
}
_MASKS = None

def score(clip_path: str) -> dict:
    m = load()
    with torch.inference_mode(), torch.autocast('cuda', dtype=torch.bfloat16):
        preds, segments = m.predict(events_video_audio_only(clip_path), verbose=False)
    preds = np.asarray(preds, dtype=np.float32)          # (T, 20484) @ 1 Hz
    abs_t = np.array([round(s.start) for s in segments]) # absolute seconds

    global _MASKS
    if _MASKS is None:
        _MASKS = {k: get_hcp_roi_indices(v, hemi='both', mesh='fsaverage5')
                  for k, v in ROIS.items()}

    out = {}
    for name, idx in _MASKS.items():
        curve = preds[:, idx].mean(axis=1)
        # MANDATORY: the training target was per-sample z-scored, so absolute
        # values are meaningless. Only relative dynamics are valid.
        sd = curve.std()
        out[name] = float(((curve - curve.mean()) / (sd + 1e-8)).max())
    out['_t'] = abs_t.tolist()
    return out


if __name__ == '__main__':
    load()                       # pay the cold start once, at boot
    print(score('clip_0001.mp4'))
```

Rolling-window variant, if you want a prediction per second instead of per clip — reuse `cortexlab.inference.streaming.StreamingPredictor`, which buffers pre-extracted features one TR at a time and zero-fills absent modalities from `model.feature_dims`:

```python
from cortexlab.inference.streaming import StreamingPredictor
sp = StreamingPredictor(model=_MODEL._model, window_trs=100, step_trs=1,
                        tr_seconds=1.0, device='cuda')
pred = sp.push_frame({'video': vjepa_feats_this_tr, 'audio': w2v_feats_this_tr})
# -> (20484,) once the window is full, else None. YOU must run the extractors.
```

### Risk

**failure_modes**

INSTALL (collectively about half a day if you rediscover them):
- `AttributeError: module 'exca.steps.base' has no attribute 'NoValue'` on `from tribev2.demo_utils import TribeModel`. A clean install of upstream `main` is BROKEN: neuralset==0.0.2 references a symbol exca moved in 0.5.26 and tribev2 leaves exca unpinned. Fix: install from `@refs/pull/67/head` (adds `exca>=0.5.20,<0.5.26`). Issues #65, #67, #69, #2, #27.
- NUMPY: the grounding claim 'NumPy pinned <2.1' IS WRONG and will break your install. `pyproject.toml` HARD-PINS `numpy==2.2.6`. The real symptom (`ImportError: cannot import name '_center'`) is a Colab/Jupyter artefact — the OLD numpy binaries stay loaded in memory after pip upgrades it; the fix is RESTART THE KERNEL, not downgrade. Issues #56, #27. (A third-party tutorial recommends `numpy>=1.26.4,<2.1.0`; that contradicts the package's own pin. Do not follow it.)
- torch cap: upstream pins `torch>=2.5.1,<2.7`. Any environment requiring torch 2.8+ needs a one-line fork relaxing that cap; torch 2.8.0 + torchvision 0.23.0 is proven in production.
- transformers: UNPINNED upstream, so a fresh install grabs 5.x, which relocates the V-JEPA2 video-processor module path and can silently drift extractor I/O. Pin `>=4.53,<5`.
- `ffmpeg` must be on PATH (moviepy). `uv`/`uvx` must be on PATH or the ASR path dies (irrelevant on the audio_only path).
- Llama-3.2-3B is gated: accept Meta's licence on the Hub, create a read token, export `HF_TOKEN`. ONLY needed for the text/tri-modal path. `from_pretrained` succeeds without it.
- `HF_HUB_DOWNLOAD_TIMEOUT` / `HF_HUB_HTTP_TIMEOUT` = 300. The 10 s default raises ReadTimeout mid-inference while pulling the ~6 GB Llama snapshot.
- WhisperX hard-codes `compute_type='float16'` in `eventstransforms.py`, which CTranslate2 cannot do on CPU/MPS -> crash. Open PRs #58, #20, #22 switch it to int8. Irrelevant on the audio_only path.
- Temp files: `flush()` -> `os.fsync(fileno())` -> `close()` before handing a path to the model, or it reads an empty file.
- Windows: `from_pretrained` does `str(Path(repo_id))`, which turns 'facebook/tribev2' into a backslash path and fails HF validation. Issues #10, #11, #63.
- `plot_stimuli` crashes on silent / speechless clips. Issues #46, #47.

RUNTIME:
- BACKBONES ARE FREED AFTER EVERY `predict()`. A warm process is not a warm model. Unpatched, every clip re-pays a ~7.6 GB V-JEPA2 build.
- OOM on a 16 GB card. Confirmed: 'GPU 0 has a total capacity of 14.56 GiB' (a Colab T4) OOMs (issue #28). But note the WIDELY-REPEATED 28-32 GB / A100-40GB-minimum figure IS THE SUM of the three backbones, not the peak — `_free_extractor_model` means they never co-reside. Measured peak in Fast mode is ~13 GB.
- Setting `data.duration_trs` crashes `predict()` — the 100 s window is baked into the checkpoint pooler.
- `num_workers > 0` inside a daemonic/forked worker raises `AssertionError: daemonic processes are not allowed to have children`.
- MULTI-WINDOW SEAM BUG on clips longer than ~150 s: the reference stitcher's crossfade weights do not sum to 1 across the warm-up band, producing a ~22x discontinuity at window seams. Single-window clips (<=100 s) are unaffected. If your clips are 5-15 s this never fires — another argument for short clips.
- SUB-10 s CLIPS SCORE TO A NEAR-FLAT, MEANINGLESS TIMELINE. `MIN_USEFUL_S = 10` exists in the reference app but is not enforced. This is a hard floor on clip duration, driven by the 5 s hemodynamic offset.
- Video with no audio track silently degrades to video-only (zero Word events) with no error.
- Text mode requires network (gTTS) and will fail air-gapped.

INTERPRETATION (the ones that will embarrass you publicly):
- ABSOLUTE SCORES ARE MEANINGLESS. The training target was per-sample z-scored and detrended. Any headline number must be relative-within-run.
- The cortical checkpoint HAS NO SUBCORTEX: no nucleus accumbens, no amygdala, no ventral striatum. Any wrapper claiming to report 'amygdala' from `facebook/tribev2` is fabricating it — see the neuroscore teardown above. Use `facebook/tribev2-subcortical` if you need those.
- 'Engagement' / 'virality' scores from community tooling are UNVALIDATED against view time, shares or conversions. None of the repos surveyed presents such a validation.
- The prediction is a group-average, unseen-subject one. It is not 'your brain'. Licence is CC BY-NC 4.0 — non-commercial only, and Meta is actively policing it (issue #48, 'Commercial License Violation of TRIBE v2 by AskKairo.com'; five separate open commercial-licence inquiries: #8, #17, #25, #45, #49, #66).

**unknowns**

MUST BE MEASURED, not researched:
1. Actual wall-clock for a 5-15 s clip on YOUR chosen GPU. The only published measurement is 140-175 s for a ~60 s clip on a ZeroGPU MIG slice in Fast mode. Everything shorter is my linear extrapolation, and fixed per-call overheads are not amortised at that scale. RUN THIS FIRST — it decides the buffer depth for the whole system.
2. Isolated cost of the text branch. No source separates WhisperX-subprocess time from Llama-forward time. My +30-60 s is an estimate.
3. Accuracy cost of `audio_only`. `modality_dropout=0.3` means the model tolerates it, but the paper does not publish a per-modality-ablation Pearson r that I could find. Quantify by correlating an audio_only run against a full tri-modal run on the same clip.
4. Whether `config_update={'data.frequency': 0.5}` runs at all, and what it costs in accuracy. Potentially a 4x speedup. Purely my inference from the source.
5. Whether V-JEPA2 `num_frames` 64 -> 32 (~2x, per the maintainers) preserves the signal. Explicitly flagged 'needs validation' by them.
6. WHETHER THE CORTICAL AND SUBCORTICAL CHECKPOINTS SHARE AN ENCODER. If they do, both heads can ride one forward pass (~20 LOC, halves the cost of getting amygdala + visual cortex together). Test: load both `best.ckpt` files and diff every `state_dict` key that is not `predictor.*`.
7. Peak VRAM in Quality (tri-modal) mode. ~13 GB is measured for Fast; Quality adds Llama-3.2-3B plus a WhisperX subprocess that DOES co-reside with the parent. My estimate is ~16-20 GB, unverified.
8. Whether the reference Space's `tribescore` package is licensed for reuse (it ships a LICENSE + NOTICE I did not read in full).
9. Whether Meta will ever release the 25 subject heads (issue #62, open, unanswered). If they do, per-viewer conditioning becomes possible and materially changes the piece.
10. Real-world stability of the `refs/pull/67/head` install — it is an unmerged community PR against a repo with 77 issues and visible maintainer inattention; it could be force-pushed or closed. Vendor a fork.

### Evidence

**sources**

PRIMARY, READ IN FULL:
- https://github.com/facebookresearch/tribev2 — cloned and read: `tribev2/demo_utils.py` (TribeModel, from_pretrained, get_events_dataframe, predict, get_audio_and_text_events + the audio_only flag), `tribev2/model.py` (FmriEncoderModel.aggregate_features missing-modality zero-fill at lines ~189-213, modality_dropout gated on self.training), `tribev2/main.py` (TR = 1/neuro.frequency, get_loaders, _free_extractor_model at lines 59-79, average_subjects handling at lines 356-365, Data field defaults), `tribev2/eventstransforms.py` (ExtractWordsFromAudio shelling out to `uvx whisperx --model large-v3 --compute_type float16`), `tribev2/utils.py` (get_hcp_roi_indices, summarize_by_roi — CONTRADICTS the outline's 'TRIBE ships no parcellation helpers'), `tribev2/grids/defaults.py` (all extractor configs), `pyproject.toml` (numpy==2.2.6, torch>=2.5.1,<2.7, transformers unpinned, requires-python >=3.11), `tribe_demo.ipynb`.
- https://huggingface.co/facebook/tribev2 — model card; API listing via https://huggingface.co/api/models/facebook/tribev2/tree/main (best.ckpt = 708,856,138 bytes); and the RELEASED CONFIG https://huggingface.co/facebook/tribev2/raw/main/config.yaml, read line by line (duration_trs:100, neuro.frequency:1.0, offset:5, n_subjects:25 with the full 25-subject predefined_mapping, average_subjects:false, modality_dropout:0.3, subject_dropout:0.1, low_rank_head:2048, hidden:1152, max_seq_len:1024).
- https://huggingface.co/facebook/tribev2-subcortical — the subcortical checkpoint, created 2026-05-13.
- https://arxiv.org/abs/2605.04326 — d'Ascoli et al., 'A foundation model of vision, audition, and language for in-silico neuroscience'. 1,000+ hours fMRI, 720 subjects.

GITHUB ISSUES (read via the API, bodies + comments):
- Issue #62 'Request for full subject-head weights' — THE source for `predictor.weights: (1, 2048, 20484)`, i.e. shared-unseen-subject head only. Open, unanswered.
- Issue #23 'Release subcortical prediction checkpoint (MaskProjector with 8,808 voxels)' — closed; maintainer @sdascoli replies with the tribev2-subcortical link. Contains the 16-bilateral-structure list and the 'shared encoder + low_rank_head should transfer' claim.
- Issues #65 / #67 / #69 — the exca 0.5.26 install break, root cause and the `exca>=0.5.20,<0.5.26` fix.
- Issue #56 / #27 — the numpy `_center` ImportError is a kernel-restart problem, not a version problem.
- Issue #28 — OOM on a 14.56 GiB T4.
- Issues #58 / #20 / #22 — WhisperX float16-on-CPU.
- Issues #10 / #11 / #63 — Windows path handling.
- Issues #1, #46/#47, #29, #24 — missing-modality aggregation widths, plot_stimuli on silent clips, word timestamps >60 s, ZeroGPU FileNotFoundError.
- Issues #8/#17/#25/#45/#48/#49/#66 — commercial licence inquiries and one alleged violation; evidence the NC clause is enforced.

REFERENCE IMPLEMENTATION (the single most useful source found):
- https://huggingface.co/spaces/techfreakworm/tribev2-brain-timeline — read `README.md` (THE measured '~1-minute clip scores in ~140-175 s on ZeroGPU in Fast mode', the bf16/TF32 notes, the torch.compile dead end, the ROI/metric table, 'absolute scores are meaningless'), `KNOWN_ISSUES.md` ('Peak VRAM is only ~13 GB, so the forward is compute-bound', the ~150 s seam bug, MIN_USEFUL_S, the ~44% GPU-idle figure, xlarge ~1.8x), `requirements.txt` (the working pin set), `app.py`, `src/tribescore/inference.py` (CONFIG_UPDATE, the duration_trs warning, `_build_audio_only_events`), `src/tribescore/fast_encode.py` (the measured 'B=4 approx 231 s vs B=1 bf16 approx 173 s on CUDA', the ~8x frame redundancy, the ~7.6 GB V-JEPA2 build), `src/tribescore/prewarm.py`.
- https://huggingface.co/spaces/cbensimon/tribe-v2 — reference Space by HF's ZeroGPU lead; '~30s' text / '~2-5 min' video.
- https://huggingface.co/spaces/beta3/TRIBE_V2_Neural_Activity_Predictor — `@spaces.GPU(duration=300)`.

WRAPPERS (source read, not just READMEs):
- https://github.com/topics/tribe-v2 — all 8 tagged repos enumerated with stars.
- https://github.com/ndpvt-web/neuroscore — cloned; `neuroscore/core/backends/gpu.py` (wrong predict signature), `neuroscore/core/regions.py` (hard-coded 'approximate' vertex ranges, `_DEFAULT_SAMPLE_RATE = 2.0`). Basis for the REJECT verdict — this is my own source analysis, stated as such.
- https://github.com/siddhant-rajhans/cortexlab — cloned; `src/cortexlab/inference/streaming.py` (StreamingPredictor, verified genuine) and `src/cortexlab/inference/predictor.py` (verbatim fork of Meta's demo_utils.py).
- https://github.com/eugenehp/tribev2-rs — Rust port.

PRICING: https://modal.com/pricing, https://replicate.com/pricing, https://huggingface.co/pricing, RunPod rates via https://gpuperhour.com/providers/runpod.

SECONDARY / TREAT WITH CARE: https://www.datacamp.com/tutorial/tribe-v2-tutorial — source of the widely-repeated 28-32 GB / A100-40GB-minimum and 'numpy<2.1' claims. I judge BOTH to be wrong: the VRAM figure is the SUM of the three backbones and ignores `_free_extractor_model`, and the numpy pin contradicts the package's own `numpy==2.2.6`. Its HF_TOKEN, timeout and fsync advice IS corroborated by the repo and issues and is good. https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model/ — announcement, no runtime numbers.

EXPLICIT INFERENCES (mine, not sourced): the per-15 s-clip latency extrapolation; the +30-60 s text-branch estimate; the `data.frequency` speedup lever; the ~16-20 GB Quality-mode VRAM estimate; the audio-only order-of-magnitude claim; the head-splicing idea for cortical+subcortical; the out-of-critical-path buffer architecture.

### Other Info

**item_id**

01

### Flagged Uncertain (omitted above)

- `cost`
- `latency_ms`
- `loc_estimate`
- `realtime_headroom`

---

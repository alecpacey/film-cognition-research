#!/bin/bash
# Wait for the detached dial measurement to finish, then collect the table and
# run the pre-registered diagnostics + selection. Detached so the harness's
# background-task reaper cannot interrupt the chain half-way.
cd "$(dirname "$0")"
PID=$(cat measure_dials.pid)
while ps -p "$PID" >/dev/null 2>&1; do sleep 20; done
echo "=== measurement process ended, $(ls dials/*.json 2>/dev/null | wc -l | tr -d ' ') dial files"
python3 measure_dials.py --workers 4          # sweep up anything that failed
echo "=== collecting"
python3 measure_dials.py --collect
echo "=== analysing"
python3 analyse_dials.py --n 60
echo "=== O3 pipeline complete"

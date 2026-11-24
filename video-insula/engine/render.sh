#!/bin/bash
# render one video: tools/render.sh <name> [engine flags...]
set -e
cd "$(dirname "$0")/.."
python3 tools/engine.py "$@"
npx hyperframes render -q standard -w 4 -o "out/$1_raw.mp4" 2>&1 | tail -3
tools/finish.sh "out/$1_raw.mp4" "out/$1.mp4"

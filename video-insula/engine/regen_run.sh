#!/bin/bash
cd "$(dirname "$0")/.."
for seed in 101 202; do for v in sito brand; do
  K=$(python3 -c "import json;print(','.join(json.load(open('cache/regen_keys.json'))['$v']))")
  HF_HUB_OFFLINE=1 /root/cbx/bin/python tools/clone_voice.py $v --keys $K --seed $seed 2>&1 | grep -E "^[0-9]+/"
done; done

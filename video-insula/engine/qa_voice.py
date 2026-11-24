"""Transcribe every cloned beat and flag the ones that don't match the script."""
import json, hashlib, os, re, subprocess, sys, difflib
from pywhispercpp.model import Model
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = Model('small', n_threads=os.cpu_count(), language='it', print_progress=False, print_realtime=False)
norm = lambda s: re.sub(r'[^a-zàèéìòù0-9 ]', '', s.lower().replace("'", ' ')).split()
bad = []
for v in sys.argv[1:]:
    for t in json.load(open(f'{ROOT}/cache/{v}_beats.json')):
        p = f'{ROOT}/cache/cbx/' + hashlib.md5(t.encode()).hexdigest()[:16] + '.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-ar', '16000', '-ac', '1', '/tmp/qa.wav'], check=True)
        got = ' '.join(s.text for s in m.transcribe('/tmp/qa.wav'))
        r = difflib.SequenceMatcher(a=norm(t), b=norm(got)).ratio()
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
        wps = len(t.split()) / max(dur, .1)
        flag = r < 0.8 or wps < 1.6 or wps > 4.2
        print(f'{"BAD " if flag else "ok  "}{r:.2f} {wps:.1f}w/s | {t[:55]} | {got[:70]}', flush=True)
        if flag: bad.append(t)
json.dump(bad, open(f'{ROOT}/cache/qa_bad.json', 'w'), ensure_ascii=False, indent=1)
print('BAD:', len(bad))

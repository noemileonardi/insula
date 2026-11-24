"""For every regenerated beat pick the best take (whisper similarity to the script, sane speed, no repeated tail)."""
import difflib, hashlib, json, os, re, shutil, subprocess
from pywhispercpp.model import Model

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'cache', 'cbx_clean')
m = Model('small', n_threads=os.cpu_count(), language='it', print_progress=False, print_realtime=False)
norm = lambda s: re.sub(r'[^a-zàèéìòù0-9 ]', '', s.lower().replace("'", ' ').replace('dr.', 'doctor')).split()
keys = json.load(open(os.path.join(ROOT, 'cache', 'regen_keys.json')))
texts = {}
for v in keys:
    for t in json.load(open(os.path.join(ROOT, 'cache', f'{v}_beats.json'))):
        texts[hashlib.md5(t.encode()).hexdigest()[:16]] = t

def score(p, t):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-ar', '16000', '-ac', '1', '/tmp/pk.wav'], check=True)
    got = ' '.join(s.text for s in m.transcribe('/tmp/pk.wav'))
    r = difflib.SequenceMatcher(a=norm(t), b=norm(got)).ratio()
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
    wps = len(t.split()) / max(dur, .1)
    pen = 0.25 if (wps < 1.5 and len(t.split()) > 5) or wps > 4.3 else 0
    return r - pen, got

for v, ks in keys.items():
    for k in ks:
        t = texts[k]
        base = os.path.join(D, f'{k}.wav')
        orig = os.path.join(D, f'{k}_s7.wav')
        if not os.path.exists(orig): shutil.copy(base, orig)
        best = None
        for s in (7, 101, 202):
            p = os.path.join(D, f'{k}_s{s}.wav')
            if not os.path.exists(p): continue
            sc, got = score(p, t)
            print(f'  s{s} {sc:.2f} {got[:70]}', flush=True)
            if best is None or sc > best[0]: best = (sc, s)
        shutil.copy(os.path.join(D, f'{k}_s{best[1]}.wav'), base)
        print(f'{v}: s{best[1]} ({best[0]:.2f}) <- {t[:60]}', flush=True)

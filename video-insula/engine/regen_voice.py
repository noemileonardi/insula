"""Regenerate flagged beats: phonetic spelling for the TTS only, N seeds each -> cache/cbx_cand/<key>_<seed>.wav
Run: /root/cbx/bin/python tools/regen_voice.py
"""
import hashlib, json, os, sys, time, torch, torchaudio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clone_voice import load, REF, ROOT
SAY = [("Mikhail Varshavski", "Mikaìl Varsciàvski"), ("Grey's Anatomy", "Greis Anàtomi"), ("Doctor Mike", "Dòctor Maik"),
       ("Dr. House", "Dottor Haus"), ("di brand", "di brend"), ("Il suo brand", "Il suo brend"), ("2017", "duemila diciassette"),
       ("glamour", "glàmur"), ("«cardiologo Palermo»", "cardiologo Palermo"), ("curriculum", "curricùlum"),
       ("«Chi sono»", "chi sono"), ("«il dottore bello»", "il dottore bello,"), ("«il dottore di cui mi fido»", "il dottore di cui mi fido"),
       ("Smonta i miti", "Smonta, i miti"), ("Lui però", "Lui, però,")]
def say(t):
    for a, b in SAY: t = t.replace(a, b)
    return t.replace('«', '').replace('»', '')
bad = json.load(open(os.path.join(ROOT, 'cache', 'qa_bad.json')))
out = os.path.join(ROOT, 'cache', 'cbx_cand'); os.makedirs(out, exist_ok=True)
torch.set_num_threads(os.cpu_count())
m = load()
for t in bad:
    k = hashlib.md5(t.encode()).hexdigest()[:16]
    for seed in (101, 202, 303):
        p = os.path.join(out, f'{k}_{seed}.wav')
        if os.path.exists(p): continue
        torch.manual_seed(seed); s = time.time()
        wav = m.generate(say(t), language_id='it', audio_prompt_path=REF, exaggeration=0.45, cfg_weight=0.5, temperature=0.65)
        torchaudio.save(p, wav.cpu(), m.sr)
        print(f'{time.time()-s:.0f}s {seed} {say(t)[:60]}', flush=True)

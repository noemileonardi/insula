"""Generate the voice-over with the client's cloned voice (Chatterbox Multilingual, MIT licence).
Run with the dedicated venv:  /root/cbx/bin/python tools/clone_voice.py <video> [--only N]
Reads cache/<video>_beats.json (written by engine.py --dump) and writes cache/cbx/<md5>.wav per beat.
"""
import hashlib, json, os, sys, time
import torch, torchaudio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, 'voice', 'ref_clean.wav')     # 11 s of the client's AI-restored voice (no room echo)
OUT = os.path.join(ROOT, 'cache', 'cbx_clean')
SAY = [("Mikhail Varshavski", "Mikaìl Varsciàvski"), ("Grey's Anatomy", "Greis Anàtomi"), ("Doctor Mike", "Dòctor Maik"),
       ("Dr. House", "Dottor Haus"), ("di brand", "di brend"), ("Il suo brand", "Il suo brend"), ("costruiamo brand", "costruiamo brend"),
       ("2017", "duemila diciassette"), ("2015", "duemila quindici"), ("2014", "duemila quattordici"), ("2009", "duemila nove"),
       ("glamour", "glàmur"), ("curriculum", "curricùlum"), ("YouTube", "Iutùb"), ("Instagram", "Ìnstagram"),
       ("Smonta i miti", "Smonta, i miti"), ("Lui però", "Lui, però,"), ("New Jersey", "Niu Gèrsi")]
def say(t):
    for a, b in SAY: t = t.replace(a, b)
    return t.replace('«', '').replace('»', '').replace('…', '.')

def load():
    import chatterbox.mtl_tts as M
    class _NoWM:                     # optional watermark module is broken in this env
        def apply_watermark(self, wav, sample_rate=None): return wav
    M.perth.PerthImplicitWatermarker = _NoWM
    return M.ChatterboxMultilingualTTS.from_pretrained(device='cpu')

def key(text):
    return hashlib.md5(text.encode()).hexdigest()[:16]

def main():
    name = sys.argv[1]
    beats = json.load(open(os.path.join(ROOT, 'cache', f'{name}_beats.json')))
    os.makedirs(OUT, exist_ok=True)
    seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 7
    sub = sys.argv[sys.argv.index('--keys') + 1].split(',') if '--keys' in sys.argv else None
    torch.set_num_threads(os.cpu_count())
    m = load()
    only = int(sys.argv[sys.argv.index('--only') + 1]) if '--only' in sys.argv else None
    todo = beats[:only] if only else beats
    for i, text in enumerate(todo):
        if sub and key(text) not in sub: continue
        p = os.path.join(OUT, key(text) + ('.wav' if not sub else f'_s{seed}.wav'))
        if os.path.exists(p): continue
        t = time.time(); torch.manual_seed(seed)
        wav = m.generate(say(text), language_id='it', audio_prompt_path=REF, exaggeration=0.45, cfg_weight=0.5, temperature=0.7)
        torchaudio.save(p, wav.cpu(), m.sr)
        print(f'{i + 1}/{len(todo)} {time.time() - t:.0f}s  {text[:60]}', flush=True)

if __name__ == '__main__':
    main()

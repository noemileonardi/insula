"""Generate the voice-over with the client's cloned voice (Chatterbox Multilingual, MIT licence).
Run with the dedicated venv:  /root/cbx/bin/python tools/clone_voice.py <video> [--only N]
Reads cache/<video>_beats.json (written by engine.py --dump) and writes cache/cbx/<md5>.wav per beat.
"""
import hashlib, json, os, sys, time
import torch, torchaudio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, 'voice', 'ref.wav')
OUT = os.path.join(ROOT, 'cache', 'cbx')

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
    torch.set_num_threads(os.cpu_count()); torch.manual_seed(7)
    m = load()
    only = int(sys.argv[sys.argv.index('--only') + 1]) if '--only' in sys.argv else None
    todo = beats[:only] if only else beats
    for i, text in enumerate(todo):
        p = os.path.join(OUT, key(text) + '.wav')
        if os.path.exists(p): continue
        t = time.time()
        wav = m.generate(text, language_id='it', audio_prompt_path=REF, exaggeration=0.45, cfg_weight=0.5, temperature=0.7)
        torchaudio.save(p, wav.cpu(), m.sr)
        print(f'{i + 1}/{len(todo)} {time.time() - t:.0f}s  {text[:60]}', flush=True)

if __name__ == '__main__':
    main()

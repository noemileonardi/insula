"""AI voice restoration (Resemble Enhance, MIT): de-reverb, denoise, bandwidth extension to 44.1 kHz.
Run: PYTHONPATH=/root/stubs HF_HUB_DISABLE_XET=1 /root/cbx/bin/python tools/enhance_voice.py in.wav out.wav [nfe] [lambd]
"""
import sys, time, torch, torchaudio
from resemble_enhance.enhancer.inference import enhance
src, dst = sys.argv[1], sys.argv[2]
nfe = int(sys.argv[3]) if len(sys.argv) > 3 else 48
lambd = float(sys.argv[4]) if len(sys.argv) > 4 else 0.9
torch.set_num_threads(torch.get_num_threads())
wav, sr = torchaudio.load(src)
wav = wav.mean(0)
t = time.time()
out, osr = enhance(wav, sr, 'cpu', nfe=nfe, solver='midpoint', lambd=lambd, tau=0.5)
torchaudio.save(dst, out.unsqueeze(0).cpu(), osr)
print('enhanced', f'{time.time() - t:.0f}s', osr)

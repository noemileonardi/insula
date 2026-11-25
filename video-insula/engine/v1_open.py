import os, sys, torch, torchaudio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clone_voice import load, REF, say
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = ["Questo è un dermatologo con quindici anni di carriera.", "E anche questo è un dermatologo con quindici anni di carriera."]
m = load(); torch.set_num_threads(os.cpu_count())
for i, t in enumerate(T):
    for s in (7, 101, 202, 303):
        torch.manual_seed(s)
        w = m.generate(say(t), language_id='it', audio_prompt_path=REF, exaggeration=0.5, cfg_weight=0.5, temperature=0.7)
        torchaudio.save(f'{ROOT}/cache/v1_open/l{i}_s{s}.wav', w.cpu(), m.sr); print(i, s, flush=True)

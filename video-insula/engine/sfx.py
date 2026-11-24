"""Synthesised sound-design kit (no samples, no licences needed). All sounds are mono float32 at SR."""
import numpy as np

def _env(n, a, d, sr):
    t = np.arange(n) / sr
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(d, 1e-4))

def _bp(x, sr, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / sr)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))

def _norm(x, peak):
    m = np.max(np.abs(x)) or 1
    return (x / m * peak).astype(np.float32)

def kit(sr):
    rng = np.random.default_rng(11)
    S = {}
    # pop: soft bubbly blip (item appears)
    n = int(sr * .12); t = np.arange(n) / sr
    S['pop'] = _norm(np.sin(2 * np.pi * (520 + 900 * np.exp(-t * 40)) * t) * _env(n, .004, .035, sr), .5)
    # click: crisp UI tap (chips, tags, buttons)
    n = int(sr * .05); t = np.arange(n) / sr
    S['click'] = _norm((np.sin(2 * np.pi * 2400 * t) * .6 + _bp(rng.standard_normal(n), sr, 2000, 7000) * .5) * _env(n, .001, .008, sr), .38)
    # key: typing keystroke
    n = int(sr * .04)
    S['key'] = _norm(_bp(rng.standard_normal(n), sr, 1500, 6000) * _env(n, .001, .006, sr), .22)
    # ding: notification / message bubble (two-tone bell)
    n = int(sr * .7); t = np.arange(n) / sr
    bell = sum(np.sin(2 * np.pi * f * t) * w for f, w in ((1318.5, 1), (2637, .35), (3955, .12)))
    bell2 = np.concatenate([np.zeros(int(sr * .09)), sum(np.sin(2 * np.pi * f * t) * w for f, w in ((1760, 1), (3520, .3)))[:n - int(sr * .09)]])
    S['ding'] = _norm(bell * _env(n, .002, .18, sr) + bell2 * _env(n, .09, .25, sr) * .8, .32)
    # stamp: punchy thud + paper slap
    n = int(sr * .25); t = np.arange(n) / sr
    S['stamp'] = _norm(np.sin(2 * np.pi * (60 + 120 * np.exp(-t * 30)) * t) * _env(n, .002, .08, sr) + _bp(rng.standard_normal(n), sr, 300, 4000) * _env(n, .001, .02, sr) * .7, .7)
    # whoosh: band-passed noise sweep (scene transition)
    n = int(sr * .45); x = rng.standard_normal(n); out = np.zeros(n)
    for k in range(8):
        a, b = k * n // 8, (k + 1) * n // 8
        c = 400 + 3200 * (k / 7)
        out[a:b] = _bp(x, sr, c * .6, c * 1.6)[a:b]
    S['whoosh'] = _norm(out * np.sin(np.pi * np.linspace(0, 1, n)) ** 2, .35)
    # swipe: short airy swish (strike-through, slides)
    n = int(sr * .2)
    S['swipe'] = _norm(_bp(rng.standard_normal(n), sr, 2500, 9000) * np.sin(np.pi * np.linspace(0, 1, n)) ** 3, .22)
    # riser: counter going up
    n = int(sr * 1.0); t = np.arange(n) / sr
    S['riser'] = _norm((np.sin(2 * np.pi * (300 * t + 500 * t * t)) * .5 + _bp(rng.standard_normal(n), sr, 3000, 9000) * .2) * (t / t[-1]) ** 2, .22)
    # sparkle: positive "done" accent (counter end, CTA)
    n = int(sr * .5); t = np.arange(n) / sr; sp = np.zeros(n)
    for i, f in enumerate((1568, 2093, 2637, 3136)):
        s = int(i * sr * .045)
        sp[s:] += np.sin(2 * np.pi * f * t[:n - s]) * _env(n - s, .002, .12, sr)
    S['sparkle'] = _norm(sp, .26)
    # step: soft footstep (characters walking in)
    n = int(sr * .09); t = np.arange(n) / sr
    S['step'] = _norm(np.sin(2 * np.pi * 110 * t) * _env(n, .003, .03, sr) + _bp(rng.standard_normal(n), sr, 200, 1200) * _env(n, .002, .015, sr) * .5, .3)
    # boom: deep impact for big numbers / section titles
    n = int(sr * .8); t = np.arange(n) / sr
    S['boom'] = _norm(np.sin(2 * np.pi * (45 + 80 * np.exp(-t * 12)) * t) * _env(n, .003, .3, sr), .55)
    return S

# relative mix levels (voice peaks around 0.9)
LEVEL = dict(pop=.55, click=.6, key=.5, ding=.55, stamp=.75, whoosh=.7, swipe=.6, riser=.55, sparkle=.55, step=.5, boom=.7)

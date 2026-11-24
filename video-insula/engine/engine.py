"""Insula reels engine: script beats -> voice (guide TTS or real recording) -> HyperFrames HTML.

Usage:
  python3 tools/engine.py <video> [--voice path/to/recording.wav]
"""
import hashlib, html, json, os, re, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'cache')
SR = 48000
VOICE_MODEL = '/tmp/claude-0/-home-user-insula/d5eedac9-3835-54e3-916a-789adeb7f8d4/scratchpad/voices/it_IT-paola-medium.onnx'
W, H = 1080, 1920
CAP_Y = 1360

def clean(t):
    return re.sub(r'\s+', ' ', t.replace('*', '').replace(' / ', ' ').replace('/', ' '))

def words_of(t):
    """[(word, emphasized)] - '/' pause marks are not words; *a b* marks emphasis"""
    res, on = [], False
    for tok in t.split():
        if tok == '/': continue
        s_ = tok.startswith('*') or tok.startswith('«*'); e = tok.rstrip('.,;:!?"»').endswith('*')
        if s_: on = True
        res.append((tok.replace('*', ''), on))
        if e: on = False
    return res

# ---------------------------------------------------------------- audio
def read_audio(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def compress_silence(a, max_gap=0.20, keep=0.085, rel_db=-32):
    """Shorten every pause longer than max_gap to `keep` seconds (podcast-tight edit).
    Returns (new_audio, src_times, dst_times) for remapping timestamps with np.interp."""
    hop = int(SR * 0.01)
    n = len(a) // hop
    if n < 10: return a, np.array([0, len(a) / SR]), np.array([0, len(a) / SR])
    rms = np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    thr = np.percentile(rms, 95) * 10 ** (rel_db / 20)
    sil = rms < thr
    out, src, dst = [], [0.0], [0.0]
    i, pos, cur = 0, 0, 0
    fade = int(SR * 0.008)
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if (j - i) * 0.01 > max_gap:
                a0, a1 = i * hop, j * hop
                k = int(keep * SR / 2)
                seg = a[pos:a0 + k].copy()
                if out and len(seg) > fade: seg[:fade] *= np.linspace(0, 1, fade)
                if len(seg) > fade: seg[-fade:] *= np.linspace(1, 0, fade)
                out.append(seg); cur += len(seg)
                src.append((a0 + k) / SR); dst.append(cur / SR)
                pos = a1 - k
                src.append(pos / SR); dst.append(cur / SR)
            i = j
        else:
            i += 1
    seg = a[pos:].copy()
    if out and len(seg) > fade: seg[:fade] *= np.linspace(0, 1, fade)
    out.append(seg); cur += len(seg)
    src.append(len(a) / SR); dst.append(cur / SR)
    return np.concatenate(out).astype(np.float32), np.array(src), np.array(dst)

# podcast-style chain: rumble cut, gentle denoise, warmth/presence EQ, de-ess, 2-stage compression, loudness -16 LUFS
MASTER = ('highpass=f=75,lowpass=f=16000,afftdn=nf=-28:tn=1,'
          'equalizer=f=180:t=q:w=1.2:g=1.5,equalizer=f=350:t=q:w=1.5:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=11000:t=h:w=0.7:g=1.5,'
          'deesser=i=0.35,acompressor=threshold=-21dB:ratio=3:attack=4:release=90:makeup=3,'
          'acompressor=threshold=-12dB:ratio=6:attack=1:release=40,alimiter=limit=0.89,loudnorm=I=-16:TP=-1.5:LRA=8')

MASTER_LIGHT = ('highpass=f=70,equalizer=f=200:t=q:w=1.2:g=1,equalizer=f=3000:t=q:w=1.2:g=1.5,deesser=i=0.3,'
                'acompressor=threshold=-20dB:ratio=2.5:attack=5:release=100:makeup=2,acompressor=threshold=-10dB:ratio=5:attack=1:release=40,alimiter=limit=0.89')

def master(audio, chain=None):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, 'a.wav'), os.path.join(d, 'b.wav')
        with wave.open(a, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a, '-af', chain or MASTER, '-ar', str(SR), b], check=True)
        # second pass: exact -16 LUFS integrated loudness, true-peak safe
        r = subprocess.run(['ffmpeg', '-i', b, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
        I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
        c = os.path.join(d, 'c.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', b, '-af', f'volume={-16 - I:.2f}dB,alimiter=limit=0.84:level=false', '-ar', str(SR), c], check=True)
        out = read_audio(c)
    return out[:len(audio)] if len(out) >= len(audio) else np.concatenate([out, np.zeros(len(audio) - len(out), np.float32)])

_voice = None
def tts(text, speed=0.9):
    global _voice
    os.makedirs(CACHE, exist_ok=True)
    cb = os.path.join(CACHE, 'cbx_clean', hashlib.md5(text.encode()).hexdigest()[:16] + '.wav')
    if os.path.exists(cb):
        a = read_audio(cb)
        env = np.convolve(np.abs(a), np.ones(1024) / 1024, mode='same')
        idx = np.where(env > 0.008)[0]
        return a[max(0, idx[0] - 1200): idx[-1] + 2400] if len(idx) else a
    key = hashlib.md5((text + str(speed)).encode()).hexdigest()[:16]
    p = os.path.join(CACHE, key + '.wav')
    if not os.path.exists(p):
        if _voice is None:
            from piper import PiperVoice
            _voice = PiperVoice.load(VOICE_MODEL)
        from piper.config import SynthesisConfig
        with wave.open(p, 'wb') as w:
            _voice.synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=speed))
    a = read_audio(p)
    # trim silence
    env = np.convolve(np.abs(a), np.ones(512) / 512, mode='same')
    idx = np.where(env > 0.01)[0]
    if len(idx):
        a = a[max(0, idx[0] - 900): idx[-1] + 1300]
    return a

def synth_sfx():
    rng = np.random.default_rng(7)
    t = np.arange(int(SR * 0.09)) / SR
    pop = np.sin(2 * np.pi * (900 - 5000 * t) * t) * np.exp(-t * 55) * 0.35
    n = int(SR * 0.38); t2 = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # crude band-pass sweep via moving average differences
    k = np.linspace(40, 6, n).astype(int)
    cs = np.cumsum(noise)
    sm = np.array([(cs[i] - cs[max(0, i - k[i])]) / k[i] for i in range(n)])
    env = np.sin(np.pi * np.clip(t2 / 0.38, 0, 1)) ** 2
    whoosh = sm * env * 0.12
    return pop.astype(np.float32), whoosh.astype(np.float32)

def word_times(beat_words, start, dur):
    """distribute words over [start, start+dur] by char weight"""
    wts = [len(w) + 2.5 for w, _ in beat_words]
    tot = sum(wts); out = []; c = start
    for (w, e), x in zip(beat_words, wts):
        d = dur * x / tot
        out.append([c, c + d]); c += d
    return out

def build_timeline(beats, voice_path=None):
    """returns (timeline list, audio array)"""
    tl = []
    if voice_path is None:
        chunks, t = [], 0.35
        chunks.append(np.zeros(int(SR * 0.35), np.float32))
        for b in beats:
            a = compress_silence(tts(clean(b['t']), b.get('speed', 0.9)), max_gap=0.16, keep=0.07)[0]
            d = len(a) / SR
            ws = words_of(b['t'])
            tl.append(dict(beat=b, start=t, end=t + d, words=ws, wt=word_times(ws, t, d)))
            pause = min(b.get('p', 0.12), 0.16) * 0.75
            chunks += [a, np.zeros(int(SR * pause), np.float32)]
            t += d + pause
        audio = np.concatenate(chunks)
    else:
        audio, tl = align_real_voice(beats, voice_path)
    return tl, audio

def align_real_voice(beats, path):
    import difflib
    from pywhispercpp.model import Model
    tmp = os.path.join(CACHE, 'voice16k.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-ar', '16000', '-ac', '1', tmp], check=True)
    ck = os.path.join(CACHE, 'align_' + hashlib.md5(open(path, 'rb').read()).hexdigest()[:12] + '.json')
    if os.path.exists(ck):
        hw = [tuple(x) for x in json.load(open(ck))]
    else:
        m = Model('small', n_threads=os.cpu_count(), language='it', print_progress=False,
                  token_timestamps=True, max_len=1, split_on_word=True)
        segs = m.transcribe(tmp)
        hw = [(re.sub(r'[^\wàèéìòù]', '', s.text.lower()), s.t0 / 100, s.t1 / 100) for s in segs if s.text.strip()]
        json.dump(hw, open(ck, 'w'))
    sw = []
    for bi, b in enumerate(beats):
        for wi, (w, e) in enumerate(words_of(b['t'])):
            sw.append((re.sub(r'[^\wàèéìòù]', '', w.lower()), bi, wi))
    sm = difflib.SequenceMatcher(a=[x[0] for x in sw], b=[x[0] for x in hw], autojunk=False)
    times = [None] * len(sw)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = hw[blk.b + k][1:]
    # interpolate gaps
    known = [i for i, x in enumerate(times) if x]
    for i in range(len(times)):
        if times[i] is None:
            prev = max([k for k in known if k < i], default=None)
            nxt = min([k for k in known if k > i], default=None)
            a0 = times[prev][1] if prev is not None else 0
            a1 = times[nxt][0] if nxt is not None else a0 + 0.4
            span = [k for k in range(len(times)) if (prev is None or k > prev) and (nxt is None or k < nxt)]
            j = span.index(i); n = len(span)
            times[i] = (a0 + (a1 - a0) * j / n, a0 + (a1 - a0) * (j + 1) / n)
    tl = []
    for bi, b in enumerate(beats):
        ws = words_of(b['t'])
        idx = [k for k, x in enumerate(sw) if x[1] == bi]
        wt = [list(times[k]) for k in idx]
        tl.append(dict(beat=b, start=wt[0][0], end=wt[-1][1], words=ws, wt=wt))
    alt = sys.argv[sys.argv.index('--voice-audio') + 1] if '--voice-audio' in sys.argv else path
    audio, s_src, s_dst = compress_silence(read_audio(alt))
    remap = lambda x: float(np.interp(x, s_src, s_dst))
    for b in tl:
        b['wt'] = [[remap(a0), remap(a1)] for a0, a1 in b['wt']]
        b['start'], b['end'] = b['wt'][0][0], b['wt'][-1][1]
    return audio, tl

# ---------------------------------------------------------------- 3D icons
ICON_SRC = '/tmp/claude-0/-home-user-insula/d5eedac9-3835-54e3-916a-789adeb7f8d4/scratchpad/icons/lobehub-fluent-emoji-3d-1.1.0/package/assets'
_icon_files = set(os.listdir(ICON_SRC)) if os.path.isdir(ICON_SRC) else set()
def icon(ch):
    """emoji char -> assets/icons/<code>.png (Fluent 3D, upscaled 512px)"""
    cps = [f'{ord(c):x}' for c in ch]
    # realistic light skin tone on people/hands when the toned 3D asset exists
    if len(cps) > 0 and not any(c.startswith('1f3f') for c in cps):
        toned = [cps[0], '1f3fc'] + cps[1:]
        for c in ('-'.join(toned), '-'.join(x for x in toned if x != 'fe0f'), '-'.join(toned + ['fe0f'])):
            if c + '.webp' in _icon_files:
                cps = c.split('-'); break
    cands = ['-'.join(cps), '-'.join(c for c in cps if c != 'fe0f'), '-'.join(cps + ['fe0f']) if 'fe0f' not in cps else '']
    if len(cps) == 1: cands.append(cps[0] + '-fe0f')
    for c in cands:
        if c and c + '.webp' in _icon_files:
            out = os.path.join(ROOT, 'assets', 'icons', c + '.png')
            if not os.path.exists(out):
                from PIL import Image, ImageFilter
                im = Image.open(os.path.join(ICON_SRC, c + '.webp')).convert('RGBA').resize((512, 512), Image.LANCZOS)
                im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
                im.save(out)
            return f'assets/icons/{c}.png'
    print('WARN no 3D icon for', ch, cands)
    return None

def emojify(text):
    import emoji as _em
    def rep(ch, data):
        p = icon(ch)
        return f'<img class="ei" src="{p}">' if p else ch
    return _em.replace_emoji(text, replace=rep)

# ---------------------------------------------------------------- html
ACC = dict(green='#1E3A2F', violet='#5B3A66', lilac='#CDB8D8', gold='#B39874', red='#D7192B',
           blue='#2747F5', lime='#39E75F', orange='#E8901C', ink='#111111', grey='#8A8A8A')

def esc(s):
    return html.escape(s)

class Doc:
    def __init__(self):
        self.html = []; self.js = []; self.n = 0; self.sfx = []
    def id(self, p='e'):
        self.n += 1; return f'{p}{self.n}'

def anim(doc, eid, kind, t, extra=None):
    """3D entrance animation at absolute time t"""
    e = f'"#{eid}"'
    F = lambda frm, to, d, ease: doc.js.append(f'tl.fromTo({e},{frm},{to[:-1]},duration:{d},ease:"{ease}"}},{t:.3f});')
    if kind == 'pop':
        F('{scale:0.2,opacity:0,rotationY:-110,z:-300}', '{scale:1,opacity:1,rotationY:0,z:0}', 0.6, 'back.out(1.7)'); doc.sfx.append(('pop', t))
    elif kind == 'stamp':
        F('{scale:2.6,opacity:0,rotation:-14,z:500}', '{scale:1,opacity:1,rotation:-4,z:0}', 0.32, 'power4.in'); doc.sfx.append(('stamp', t + 0.3))
    elif kind == 'up':
        F('{y:160,opacity:0,rotationX:-70,z:-200}', '{y:0,opacity:1,rotationX:0,z:0}', 0.6, 'power3.out')
    elif kind == 'down':
        F('{y:-160,opacity:0,rotationX:70,z:-200}', '{y:0,opacity:1,rotationX:0,z:0}', 0.6, 'power3.out')
    elif kind == 'left':
        F('{x:-1100,rotationY:-80,z:-300}', '{x:0,rotationY:0,z:0}', 0.8, 'power3.out'); doc.sfx.append(('swipe', t))
    elif kind == 'right':
        F('{x:1100,rotationY:80,z:-300}', '{x:0,rotationY:0,z:0}', 0.8, 'power3.out'); doc.sfx.append(('swipe', t))
    elif kind in ('walkl', 'walkr'):
        sg = -1 if kind == 'walkl' else 1
        doc.js.append(f'tl.fromTo({e},{{x:{sg*900},opacity:1}},{{x:0,duration:1.1,ease:"power1.out"}},{t:.3f});')
        doc.js.append(f'tl.fromTo({e},{{y:0}},{{y:-34,duration:0.14,yoyo:true,repeat:7,ease:"sine.out"}},{t:.3f});')
        doc.js.append(f'tl.fromTo({e},{{rotation:{-6*sg}}},{{rotation:{6*sg},duration:0.14,yoyo:true,repeat:7,ease:"sine.inOut"}},{t:.3f});')
        doc.js.append(f'tl.to({e},{{rotation:0,duration:0.2}},{t + 1.12:.3f});')
        for k in range(4): doc.sfx.append(('step', t + 0.14 + k * 0.28))
    elif kind == 'fade':
        F('{opacity:0,z:-150}', '{opacity:1,z:0}', 0.5, 'power2.out')
    elif kind == 'zoom':
        F('{z:-1400,opacity:0,rotationX:25}', '{z:0,opacity:1,rotationX:0}', 0.8, 'power3.out'); doc.sfx.append(('swipe', t))
    elif kind == 'spin':
        F('{rotationY:-540,scale:0.3,opacity:0,z:-400}', '{rotationY:0,scale:1,opacity:1,z:0}', 1.0, 'power3.out'); doc.sfx.append(('boom', t + 0.25))
    elif kind == 'flip':
        F('{rotationX:-180,opacity:0}', '{rotationX:0,opacity:1}', 0.7, 'back.out(1.4)'); doc.sfx.append(('pop', t))
    elif kind == 'grow':
        F('{scaleY:0}', '{scaleY:1}', 0.9, 'power2.out')
    elif kind == 'growx':
        F('{scaleX:0}', '{scaleX:1}', 0.6, 'power2.out')

def _wi(at, words):
    if isinstance(at, int): return at
    key, _, occ = at.partition('#'); occ = int(occ or 1)
    norm = lambda x: re.sub(r'[^\wàèéìòù]', '', x.lower())
    for i, (w, e) in enumerate(words):
        if norm(w) == norm(key):
            occ -= 1
            if occ == 0: return i
    raise KeyError(f'word {at!r} not in {[w for w,_ in words]}')

def render_item(doc, it, t0, tl_words, scene_end, words=()):
    k = it['k']; eid = doc.id()
    for key in ('at', 'out', 'strike'):
        if isinstance(it.get(key), str): it = dict(it); it[key] = _wi(it[key], words)
    if 'stg' in it:
        it = dict(it); it['stg'] = [dict(sg, at=_wi(sg['at'], words)) if isinstance(sg.get('at'), str) else sg for sg in it['stg']]
    # time resolution
    if 'at' in it:
        wi = it['at']
        t = tl_words[min(wi, len(tl_words) - 1)][0] if isinstance(wi, int) else t0 + float(wi)
    else:
        t = t0 + it.get('dt', 0)
    x, y = it.get('x', 540), it.get('y', 760)
    style = f'left:{x}px;top:{y}px;'
    if 'w' in it: style += f'width:{it["w"]}px;'
    if 'h' in it: style += f'height:{it["h"]}px;'
    if 'z' in it: style += f'z-index:{it["z"]};'
    if 'rot' in it: style += f'rotate:{it["rot"]}deg;'
    if 'style' in it: style += it['style']
    cls = 'it'
    if k == 'emoji':
        sz = it.get("size", 260) * 1.15
        p = icon(it['ch'])
        inner = f'<img src="{p}" style="width:{sz}px;height:{sz}px;display:block">' if p else esc(it['ch']); cls += ' ico'
    elif k == 'text':
        f = it.get('font', 'sans')
        style += f'font-size:{it.get("size",64)}px;color:{ACC.get(it.get("c","ink"), it.get("c","ink"))};'
        cls += ' serif' if f == 'serif' else ' sans'
        if it.get('i'): style += 'font-style:italic;'
        if 'wt' in it: style += f'font-weight:{it["wt"]};'
        if 'w' in it: style += 'text-align:center;white-space:normal;'
        inner = emojify(it['s'])
    elif k == 'chip':
        bg = ACC.get(it.get('bg', 'blue'), it.get('bg', 'blue'))
        style += f'background:{bg};color:{it.get("c","#fff")};font-size:{it.get("size",46)}px;'
        cls += ' chip serif'; inner = emojify(esc(it['s']))
    elif k == 'tag':
        bg = ACC.get(it.get('bg', 'lime'), it.get('bg', 'lime'))
        style += f'background:{bg};color:{it.get("c","#0b2a12")};font-size:{it.get("size",50)}px;'
        cls += ' tag serif'; inner = emojify(esc(it['s']))
    elif k == 'box':
        style += f'border-color:{ACC.get(it.get("c","violet"), it.get("c","violet"))};'
        cls += ' dbox'; inner = ''
    elif k == 'img':
        style += f'border-radius:{it.get("r",28)}px;overflow:hidden;'
        inner = f'<img src="{it["src"]}" style="width:100%;height:100%;object-fit:{it.get("fit","cover")};object-position:{it.get("pos","center")}">'
    elif k == 'video':
        style += 'overflow:hidden;'
        vst = it.get('vstart', t); vdu = it.get('vdur', scene_end - t + 0.6)
        inner = (f'<video class="clip" src="{it["src"]}" muted playsinline data-start="{vst:.3f}" data-duration="{vdu:.3f}" '
                 f'data-track-index="2" style="width:100%;height:100%;object-fit:cover"></video>')
    elif k == 'html':
        inner = emojify(it['html'])
        if '{{TYPE:' in inner:
            tt = t + 0.5
            if 'type_at' in it:
                ta = it['type_at']
                ta = _wi(ta, words) if isinstance(ta, str) else ta
                tt = tl_words[ta][0] if isinstance(ta, int) else t + float(ta)
            rate = it.get('rate', 0.11)
            def _typ(m):
                txt = m.group(1); out = ''
                for i, ch in enumerate(txt):
                    out += f'<span id="{eid}t{i}" style="display:none">{esc(ch)}</span>'
                    doc.js.append(f'tl.set("#{eid}t{i}",{{display:"inline"}},{tt + i * rate:.3f});')
                    if ch != ' ': doc.sfx.append(('key', tt + i * rate))
                return out + f'<span class="caret" id="{eid}k">|</span>'
            inner = re.sub(r'\{\{TYPE:(.*?)\}\}', _typ, inner)
            n = int(max(1, (scene_end - tt) / 0.5))
            doc.js.append(f'tl.to("#{eid}k",{{opacity:0,duration:0.25,yoyo:true,repeat:{n},ease:"steps(1)"}},{tt:.3f});')
        if it.get('cls'): cls += ' ' + it['cls']
    elif k == 'count':
        style += f'font-size:{it.get("size",200)}px;color:{ACC.get(it.get("c","ink"), it.get("c","ink"))};'
        cls += ' sans count'; inner = f'{it.get("pre","")}<span id="{eid}n">0</span>{it.get("suf","")}'
        dec = it.get('dec', 0)
        doc.js.append(f'(function(){{var o={{v:{it.get("frm",0)}}};var n=document.getElementById("{eid}n");'
                      f'tl.to(o,{{v:{it["to"]},duration:{it.get("dur",1.2)},ease:"power2.out",onUpdate:function(){{n.textContent=o.v.toFixed({dec}).replace(".",",").replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,".");}}}},{t:.3f});'
                      f'tl.set(o,{{v:{it.get("frm",0)}}},0);n.textContent="{it.get("frm",0)}";}})();')
    elif k == 'type':
        style += f'font-size:{it.get("size",48)}px;color:{ACC.get(it.get("c","ink"), it.get("c","ink"))};'
        cls += ' sans'; chars = it['s']
        spans = ''.join(f'<span id="{eid}c{i}" style="opacity:0">{esc(ch)}</span>' for i, ch in enumerate(chars))
        inner = spans + (f'<span class="caret" id="{eid}k">|</span>' if it.get('caret', True) else '')
        rate = it.get('rate', 0.055)
        for i in range(len(chars)):
            doc.js.append(f'tl.set("#{eid}c{i}",{{opacity:1}},{t + i * rate:.3f});')
    else:
        raise ValueError(k)
    doc.html.append(f'<div id="{eid}" class="{cls}" style="{style}"><div class="in3d" id="{eid}i">{inner}</div></div>')
    depth = it.get('depth', {'emoji': 160, 'text': 70, 'chip': 110, 'tag': 110, 'count': 90}.get(k, 0))
    doc.js.append(f'gsap.set("#{eid}",{{xPercent:-50,yPercent:-50,z:{depth}}});')
    # idle 3D motion on the inner wrapper (never conflicts with the entrance on the outer)
    life = max(0.6, scene_end - t - 0.6)
    if it.get('idle', True) and k not in ('type',):
        if k == 'emoji':
            per = 1.1; n = max(0, int(life / per) - 1)
            doc.js.append(f'tl.to("#{eid}i",{{y:-30,rotationY:22,rotation:4,scaleY:1.03,duration:{per},yoyo:true,repeat:{n},ease:"sine.inOut"}},{t + 0.6:.3f});')
        elif k in ('html', 'img'):
            sgn = 1 if (doc.n % 2) else -1
            doc.js.append(f'tl.fromTo("#{eid}i",{{rotationY:{-15*sgn},rotationX:8}},{{rotationY:{15*sgn},rotationX:-4,duration:{life + 0.6:.2f},ease:"sine.inOut"}},{t:.3f});')
        else:
            doc.js.append(f'tl.to("#{eid}i",{{y:-14,duration:{life:.2f},ease:"sine.inOut"}},{t + 0.5:.3f});')
    anim(doc, eid, it.get('in', 'pop'), t)
    if it.get('in', 'pop') == 'pop' and doc.sfx and doc.sfx[-1] == ('pop', t):
        if k in ('chip', 'tag'): doc.sfx[-1] = ('click', t)
        elif k == 'html' and ('bubble' in it['html'] or 'Nuova prenotazione' in it['html']): doc.sfx[-1] = ('ding', t)
    elif k == 'html' and ('bubble' in it['html'] or 'Nuova prenotazione' in it['html']):
        doc.sfx.append(('ding', t))
    if k == 'count':
        doc.sfx.append(('riser', t)); doc.sfx.append(('sparkle', t + it.get('dur', 1.2) - 0.05))
    # optional exit / emphasis
    if 'out' in it:
        ot = tl_words[it['out']][0] if isinstance(it['out'], int) else t0 + float(it['out'])
        doc.js.append(f'tl.to("#{eid}",{{opacity:0,scale:0.8,duration:0.3}},{ot:.3f});')
    if 'shake' in it:
        st = t + float(it['shake'])
        doc.js.append(f'tl.to("#{eid}",{{rotation:9,duration:0.06,yoyo:true,repeat:11,ease:"none"}},{st:.3f});')
    def _tat(at):
        at = _wi(at, words) if isinstance(at, str) else at
        return tl_words[min(at, len(tl_words) - 1)][0] if isinstance(at, int) else t + float(at)
    for at, js in it.get('fx', []):
        doc.js.append(js.replace('#ID', '#' + eid).replace('@T', f'{_tat(at):.3f}').replace('@END', f'{scene_end:.3f}'))
    for at, kind in it.get('sfxs', []):
        doc.sfx.append((kind, _tat(at)))
    for sg in it.get('stg', []):
        st = tl_words[sg['at']][0] if isinstance(sg.get('at'), int) else t + float(sg.get('dt', 0))
        doc.js.append(f'tl.fromTo("#{eid} {sg["sel"]}",{json.dumps(sg.get("frm",{"opacity":0,"scale":0.3}))},'
                      f'Object.assign({json.dumps(sg.get("to",{"opacity":1,"scale":1}))},{{duration:{sg.get("d",0.35)},stagger:{sg.get("each",0.05)},ease:"{sg.get("ease","back.out(1.8)")}"}}),{st:.3f});')
        if sg.get('sfx'):
            for q in range(8): doc.sfx.append(('click', st + q * sg.get('each', 0.05) * 1.6))
    if 'strike' in it:
        sid = doc.id(); st = tl_words[it['strike']][0] if isinstance(it['strike'], int) else t0 + float(it['strike'])
        doc.html[-1] = doc.html[-1][:-12] + f'<div id="{sid}" class="strike"></div></div></div>'
        doc.js.append(f'tl.fromTo("#{sid}",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power2.out"}},{st:.3f});')
        doc.sfx.append(('swipe', st))
    return eid

CSS = open(os.path.join(ROOT, 'tools', 'style.css')).read() if os.path.exists(os.path.join(ROOT, 'tools', 'style.css')) else ''

def build_html(name, tl, total):
    doc = Doc()
    # group beats into scenes
    scenes = []
    for i, b in enumerate(tl):
        v = b['beat'].get('v')
        if v is not None:
            scenes.append(dict(v=v, start=b['start'] if i else 0.0, beats=[b]))
        else:
            scenes[-1]['beats'].append(b)
    for si, sc in enumerate(scenes):
        sc['end'] = scenes[si + 1]['start'] if si + 1 < len(scenes) else total
        # AI 3D scene available? swap in the full-bleed image version of this scene
        alt = sc['v'].get('ai')
        if alt:
            for ext in ('mp4', 'png', 'jpg'):
                p = os.path.join(ROOT, 'assets', 'scenes', f"{alt['id']}.{ext}")
                if os.path.exists(p):
                    img = dict(k='video' if ext == 'mp4' else 'img', src=f"assets/scenes/{alt['id']}.{ext}", x=540, y=960, w=1240, h=2204, r=0, depth=-120, idle=False,
                               vstart=max(0, sc['start'] - 0.12), vdur=sc['end'] - sc['start'] + 0.6)
                    img['in'] = 'fade'
                    shade = dict(k='html', html='<div style="width:1240px;height:2204px;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.45) 85%)"></div>', x=540, y=960, idle=False, depth=-110)
                    shade['in'] = 'none'
                    sc['v'] = dict(items=[img, shade] + alt.get('items', []), dark=True, bg='#111', capy=alt.get('capy', 1300), cam=1.14)
                    break
    TR = [('{rotationY:-55,x:760,z:-500,opacity:0}', '{rotationY:55,x:-760,z:-500,opacity:0}'),
          ('{rotationX:50,y:-900,z:-400,opacity:0}', '{rotationX:-50,y:900,z:-400,opacity:0}'),
          ('{rotationY:55,x:-760,z:-500,opacity:0}', '{rotationY:-55,x:760,z:-500,opacity:0}'),
          ('{z:-1600,opacity:0,rotationX:20}', '{z:900,opacity:0}')]
    OV = 0.42   # overlap between scenes for the 3D transition
    for si, sc in enumerate(scenes):
        v = sc['v']; sid = f's{si}'
        start, end = sc['start'], sc['end']
        vs = max(0, start - 0.12)
        last = si + 1 == len(scenes)
        ve = end if last else end + OV - 0.12
        bg = v.get('bg', '#FFFFFF'); dark = v.get('dark', False)
        doc.html.append(f'<div id="{sid}" class="clip scene{" dark" if dark else ""}" data-start="{vs:.3f}" data-duration="{ve - vs:.3f}" data-track-index="1" style="background:{bg};z-index:{si + 1}"><div class="punch" id="{sid}p"><div class="cam" id="{sid}cam"><div class="blob b1" id="{sid}b1"></div><div class="blob b2" id="{sid}b2"></div><div class="floorwrap"><div class="floor"></div></div>')
        frm, to = TR[si % len(TR)]
        if si > 0:
            doc.js.append(f'tl.fromTo("#{sid}",{frm[:-1]},filter:"blur(14px)"}},{{rotationY:0,rotationX:0,x:0,y:0,z:0,opacity:1,filter:"blur(0px)",duration:{OV + 0.05},ease:"power3.out"}},{vs:.3f});')
            doc.sfx.append(('whoosh', vs - 0.05))
        if not last:
            nfrm, nto = TR[(si + 1) % len(TR)]
            doc.js.append(f'tl.to("#{sid}",{nto[:-1]},filter:"blur(14px)",duration:{OV},ease:"power3.in"}},{end - 0.12:.3f});')
        # camera: slow 3D orbit + push-in; captions live inside it, so they move with the scene
        sg = 1 if si % 2 == 0 else -1
        z = v.get('cam', 1.08)
        doc.js.append(f'tl.fromTo("#{sid}cam",{{rotationY:{7*sg},rotationX:5,scale:1,x:{-30*sg}}},{{rotationY:{-7*sg},rotationX:-3,scale:{z},x:{30*sg},duration:{ve - vs:.2f},ease:"sine.inOut"}},{vs:.3f});')
        allw = [w for b in sc['beats'] for w in b['wt']]
        for it in v.get('items', []):
            if it.get('beat') is not None:
                bw = sc['beats'][it['beat']]['wt']
                render_item(doc, it, sc['beats'][it['beat']]['start'], bw, end, sc['beats'][it['beat']]['words'])
            else:
                render_item(doc, it, start, allw, end, [w for b in sc['beats'] for w in b['words']])
        # captions (one word at a time) inside the camera
        if not v.get('nocap'):
            cy = v.get('capy', CAP_Y)
            ws = [(w, e, a, z2) for b in sc['beats'] for (w, e), (a, z2) in zip(b['words'], b['wt'])]
            dark_t = None
            if v.get('dark_from'):
                aw = [w for b in sc['beats'] for w in b['words']]
                dark_t = ws[_wi(v['dark_from'], aw)][2] - 0.05
            for i, (w, e, a, z2) in enumerate(ws):
                nxt = ws[i + 1][2] if i + 1 < len(ws) else min(end, z2 + 0.5)
                d = min(nxt, z2 + 0.6) - a
                if d < 0.04: continue
                cid = doc.id('c')
                cl = 'cap' + (' dark' if dark or (dark_t is not None and a >= dark_t) else '') + (' em' if e else '')
                doc.html.append(f'<div id="{cid}" class="clip {cl}" data-start="{a:.3f}" data-duration="{d:.3f}" data-track-index="3" style="top:{cy}px"><span>{esc(w)}</span></div>')
                doc.js.append(f'gsap.set("#{cid}",{{yPercent:-50,z:220}});')
                doc.js.append(f'tl.fromTo("#{cid}",{{scale:0.7,rotationX:-55,y:30}},{{scale:1,rotationX:0,y:0,duration:0.16,ease:"back.out(2)"}},{a:.3f});')
                # punch-in on emphasised words (first word of each emphasis run)
                if e and (i == 0 or not ws[i - 1][1]):
                    doc.js.append(f'tl.fromTo("#{sid}p",{{scale:1}},{{scale:1.045,duration:0.11,yoyo:true,repeat:1,ease:"power2.out"}},{a:.3f});')
        # living background: soft brand-colour blobs drifting
        if not dark and not v.get('ai'):
            doc.js.append(f'tl.fromTo("#{sid}b1",{{x:-120,y:-60,scale:1}},{{x:160,y:120,scale:1.25,duration:{ve - vs:.2f},ease:"sine.inOut"}},{vs:.3f});')
            doc.js.append(f'tl.fromTo("#{sid}b2",{{x:140,y:80,scale:1.2}},{{x:-150,y:-100,scale:0.95,duration:{ve - vs:.2f},ease:"sine.inOut"}},{vs:.3f});')
        doc.html.append('</div></div></div>')
    body = '\n'.join(doc.html)
    js = '\n'.join(doc.js)
    page = f'''<!doctype html>
<html lang="it" data-resolution="portrait">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="assets/js/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="1080" data-height="1920">
{body}
<div class="wm clip" data-start="0" data-duration="{total:.3f}" data-track-index="5"><svg viewBox="0 0 24 24" width="34" height="34"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor"/></svg><span>@INSULAMEDICALAGENCY</span></div>
<audio id="vo" class="clip" src="assets/audio/{name}.wav" data-start="0" data-duration="{total:.3f}" data-track-index="0" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>'''
    return page, doc.sfx

def mix(audio, sfx):
    from sfx import kit, LEVEL
    K = kit(SR)
    out = audio.copy()
    last = {}
    for kind, t in sorted(sfx, key=lambda x: x[1]):
        if t < 0 or kind not in K: continue
        gap = 0.03 if kind in ('key', 'step', 'click') else 0.2
        if t - last.get(kind, -9) < gap: continue
        last[kind] = t
        s = K[kind] * LEVEL[kind]
        i = int(t * SR)
        if i + len(s) > len(out):
            out = np.concatenate([out, np.zeros(i + len(s) - len(out), np.float32)])
        out[i:i + len(s)] += s
    return np.clip(out, -1, 1)

def main():
    name = sys.argv[1]
    voice = sys.argv[sys.argv.index('--voice') + 1] if '--voice' in sys.argv else None
    sys.path.insert(0, os.path.join(ROOT, 'tools'))
    import specs
    beats = specs.VIDEOS[name]
    if '--dump' in sys.argv:
        json.dump([clean(b['t']) for b in beats], open(os.path.join(CACHE, f'{name}_beats.json'), 'w'), ensure_ascii=False, indent=1)
        print('dumped', len(beats)); return
    tl, audio = build_timeline(beats, voice)
    if '--novoice' in sys.argv:
        audio = np.zeros_like(audio)
    elif '--no-master' not in sys.argv:
        audio = master(audio, MASTER_LIGHT if '--light' in sys.argv else None)
    total = max(len(audio) / SR, tl[-1]['end'] + specs.TAIL.get(name, 2.5))
    audio = np.concatenate([audio, np.zeros(int(total * SR) - len(audio) + 10, np.float32)])
    page, sfx = build_html(name, tl, total)
    audio = mix(audio, sfx)
    os.makedirs(os.path.join(ROOT, 'assets', 'audio'), exist_ok=True)
    with wave.open(os.path.join(ROOT, 'assets', 'audio', f'{name}.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    open(os.path.join(ROOT, 'cache', f'{name}.html'), 'w').write(page)
    open(os.path.join(ROOT, 'index.html'), 'w').write(page)
    json.dump([dict(t=b['beat']['t'], start=round(b['start'], 2), end=round(b['end'], 2)) for b in tl],
              open(os.path.join(ROOT, 'cache', f'{name}_timeline.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'{name}: {total:.1f}s, {len(tl)} beats')

if __name__ == '__main__':
    main()

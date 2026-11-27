"""VIDEO 3 – Doctor Mike, v4: montage language copied from the client's reference reel (case study 'Massaro'),
re-skinned with the Insula aesthetic (cream bokeh, deep green, gold, lilac, Cormorant Garamond + Jost).
Reference vocabulary reproduced: giant number behind cut-out + profile card, full clip shrinking into a 3D reel wall,
phone + circle + big number + script word with reflection, phrase captions with highlight boxes, portrait with
diagonal panels and giant layered words, b/w photo + white flash, orbit rings with particles, giant rotating arc,
3D coin with ghost numeral, floating tilted video cards on dark, icon timeline with progress line, kinetic giant
letters, ring of avatars, notes-app list with strike-throughs, name lower-third over scrolling outlined names,
Instagram logo outro."""
import random
from widgets import E, T, HT, chip, tag, counter, phone
from brand3 import BRAND3, CUT, NUMBER, o, CREAM, GREEN, GOLD, LIL, VIOLET, INK, M3, CSS as CSS3

M4 = 'assets/mike_v4/'
DARK = '#0F1E17'
BOKEH = ('radial-gradient(55% 32% at 18% 14%,#EDE3F1 0%,rgba(237,227,241,0) 70%),'
         'radial-gradient(48% 30% at 86% 38%,#F2E7D4 0%,rgba(242,231,212,0) 70%),'
         'radial-gradient(60% 34% at 30% 78%,#E8E0EC 0%,rgba(232,224,236,0) 70%),'
         'radial-gradient(40% 26% at 80% 92%,#EFE4D2 0%,rgba(239,228,210,0) 70%),#F8F4EE')
DARKBG = f'radial-gradient(70% 45% at 50% 40%,#1C3528 0%,{DARK} 75%)'
FULL = dict(x=540, y=960, w=1240, h=2204)

def S(*items, **kw):
    out = []
    for i in items:
        out += i if isinstance(i, list) else [i]
    d = dict(items=out, bg=BOKEH); d.update(kw)
    if d.get('dark'): d.setdefault('bg', DARKBG); d['bg'] = DARKBG if d['bg'] == BOKEH else d['bg']
    return d

def H(html, x=540, y=960, **k):
    d = HT(html, x, y); d.update({'idle': False, 'in': 'none'}); d.update(k)
    if 'in_' in d: d['in'] = d.pop('in_')
    return d

def FLASH(dt=0.0):
    return H('<div class="fl" style="width:1500px;height:2600px;background:radial-gradient(circle at 50% 45%,#fff 0%,#FFFDF8 45%,rgba(255,253,248,.9) 100%)"></div>',
             depth=300, z=50, fx=[(dt, 'tl.fromTo("#ID .fl",{opacity:1},{opacity:0,duration:0.55,ease:"power2.out"},@T);')], sfxs=[(dt, 'sparkle')])

def GIANT(txt, x, y, size, c=GREEN, op=1.0, at=0, it=False, w=500, track=-0.02, font="'Cormorant Garamond'", extra=''):
    return H(f'<div class="gw" style="font:{"italic " if it else ""}{w} {size}px {font};color:{c};opacity:{op};letter-spacing:{track}em;white-space:nowrap;line-height:.82;{extra}">{txt}</div>',
             x, y, fx=[(at, f'tl.fromTo("#ID .gw",{{opacity:0,scale:1.3,filter:"blur(26px)"}},{{opacity:{op},scale:1,filter:"blur(0px)",duration:0.9,ease:"power3.out"}},@T);')],
             sfxs=[(at, 'whoosh')])

def SCRIPT(txt, x, y, size=130, c=VIOLET, at=0):
    """handwritten-like word with a soft reflection (reference: 'Richieste')"""
    return H(f'<div class="sw" style="font:italic 500 {size}px \'Cormorant Garamond\';color:{c};-webkit-box-reflect:below -18px linear-gradient(transparent 35%,rgba(255,255,255,.35))">{txt}</div>',
             x, y, fx=[(at, 'tl.fromTo("#ID .sw",{opacity:0,x:-60,filter:"blur(14px)",clipPath:"inset(0 100% 0 0)"},{opacity:1,x:0,filter:"blur(0px)",clipPath:"inset(0 0% 0 0)",duration:0.8,ease:"power2.out"},@T);')],
             sfxs=[(at, 'swipe')])

def CARD(title, sub, x, y, at=0, w=640, blur=0, depth=0, icon=''):
    """frosted notification card floating around a phone"""
    ic = f'<div style="width:62px;height:62px;border-radius:16px;background:{GREEN};display:flex;align-items:center;justify-content:center;font-size:34px">{icon}</div>' if icon else ''
    d = HT(f'<div style="width:{w}px;display:flex;gap:20px;align-items:center;padding:22px 26px;border-radius:26px;background:rgba(255,255,255,.82);box-shadow:0 24px 50px rgba(30,42,36,.16);text-align:left;white-space:normal;filter:blur({blur}px)">{ic}<div><div style="font:500 30px Jost;color:{INK}">{title}</div><div style="font:300 25px Jost;color:#5B6760">{sub}</div></div></div>', x, y)
    d.update({'in': 'blur', 'at': at, 'depth': depth}); return d

def LOWER3(name, sub, x=540, y=1330, at=0, pre=''):
    pre_h = f'<span style="font-weight:300">{pre} </span>' if pre else ''
    d = HT(f'<div style="padding:24px 54px 20px;border-radius:30px;background:rgba(255,255,255,.94);border:3px solid {LIL};box-shadow:0 30px 70px rgba(30,42,36,.22);text-align:center">'
           f'<div style="font:600 62px Jost;color:{INK};letter-spacing:-.01em">{pre_h}{name}</div><div style="font:400 24px Jost;letter-spacing:.24em;color:{GREEN};margin-top:4px">{sub}</div></div>', x, y)
    d.update({'in': 'blur', 'at': at, 'depth': 160, 'sfxs': [(at, 'pop')]}); return d

def ROWS(txt, at=0, switch=None, txt2=None, op=0.22):
    """giant outlined names scrolling in alternate directions behind the subject (reference lower-third scene)"""
    def rows(t, cls):
        r = ''
        for i in range(6):
            r += (f'<div class="{cls}r{i}" style="position:absolute;left:-600px;top:{i * 330}px;white-space:nowrap;font:600 300px Jost;letter-spacing:-.02em;'
                  f'color:transparent;-webkit-text-stroke:3px {GREEN if i % 2 else GOLD};opacity:{op}">{(t + " · ") * 4}</div>')
        return r
    html = f'<div style="position:relative;width:1300px;height:2000px;overflow:hidden"><div class="A">{rows(txt, "a")}</div>' + (f'<div class="B" style="opacity:0">{rows(txt2, "b")}</div>' if txt2 else '') + '</div>'
    js = ''.join(f'tl.fromTo("#ID .ar{i},#ID .br{i}",{{x:{-500 if i % 2 else 0}}},{{x:{0 if i % 2 else -500},duration:@DUR,ease:"none"}},@T);' for i in range(6))
    fx = [(at, js.replace('@DUR', '9'))]
    if switch is not None:
        fx.append((switch, 'tl.to("#ID .A",{opacity:0,filter:"blur(12px)",duration:0.35},@T);tl.fromTo("#ID .B",{opacity:0,filter:"blur(12px)"},{opacity:1,filter:"blur(0px)",duration:0.45},@T);'))
    return H(html, 540, 1000, depth=-200, fx=fx, sfxs=[(switch, 'whoosh')] if switch is not None else [])

def COIN(n):
    """3D coin flipping in with a giant ghost numeral behind (reference '2')"""
    ghost = H(f'<div class="gh" style="font:600 1150px \'Cormorant Garamond\';line-height:.8;color:transparent;-webkit-text-stroke:4px rgba(30,58,47,.13)">{n}</div>', 540, 820, depth=-250,
              fx=[(0, 'tl.fromTo("#ID .gh",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:1.2,ease:"power2.out"},@T);')])
    coin = H(f'''<div class="cn" style="position:relative;width:420px;height:420px;transform-style:preserve-3d">
<div style="position:absolute;inset:0;border-radius:50%;background:#14271F;transform:translateZ(-22px)"></div>
<div style="position:absolute;inset:0;border-radius:50%;background:#18301F;transform:translateZ(-11px)"></div>
<div style="position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 35% 30%,#2E5443 0%,{GREEN} 55%,#132A20 100%);border:12px solid {GOLD};box-shadow:inset 0 0 0 6px rgba(255,255,255,.12),0 40px 80px rgba(30,42,36,.35);display:flex;align-items:center;justify-content:center;font:italic 600 250px 'Cormorant Garamond';color:#F4EEE3">{n}</div></div>''',
             540, 760, depth=120,
             fx=[(0.1, 'tl.fromTo("#ID .cn",{rotationY:-900,rotationX:50,y:-900,scale:.6},{rotationY:0,rotationX:14,y:0,scale:1,duration:1.25,ease:"power3.out"},@T);'
                       'tl.to("#ID .cn",{rotationY:-24,rotationX:4,duration:2.2,yoyo:true,repeat:3,ease:"sine.inOut"},@T+1.25);')],
             sfxs=[(0.1, 'whoosh'), (1.15, 'stamp')])
    kick = H(f'<div style="display:flex;align-items:center;gap:20px;font:400 32px Jost;letter-spacing:.34em;color:{GOLD}"><i style="display:block;width:80px;height:2px;background:{GOLD}"></i>LEVA 0{n}<i style="display:block;width:80px;height:2px;background:{GOLD}"></i></div>', 540, 1120, in_='blur', dt=0.9)
    return [ghost, coin, kick]

def ORBIT(at_more, center):
    rnd = random.Random(5)
    rings = ''
    for ri, r in enumerate((170, 290, 410)):
        dots = ''
        for k in range(3 + ri * 2):
            a = rnd.uniform(0, 6.283); s = rnd.choice([34, 40, 48])
            import math
            dots += f'<i class="d{ri}" style="position:absolute;left:{r + r * math.cos(a) - s / 2:.0f}px;top:{r + r * math.sin(a) - s / 2:.0f}px;width:{s}px;height:{s}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0%,{LIL} 40%,{VIOLET} 100%);box-shadow:0 0 24px rgba(205,184,216,.9)"></i>'
        rings += f'<div class="rg{ri}" style="position:absolute;left:{450 - r}px;top:{450 - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;border:2px solid rgba(30,42,36,.22)">{dots}</div>'
    html = f'<div style="position:relative;width:900px;height:900px">{rings}</div>'
    js = ''.join(f'tl.fromTo("#ID .rg{ri}",{{rotation:0,scale:.4,opacity:0}},{{rotation:{(-1) ** ri * 140},scale:1,opacity:1,duration:7,ease:"power1.out"}},@T);' for ri in range(3))
    js += 'tl.fromTo("#ID i",{scale:0},{scale:1,duration:0.4,stagger:0.06,ease:"back.out(3)"},@T+0.3);'
    js2 = 'tl.to("#ID i",{background:"radial-gradient(circle at 35% 30%,#fff 0%,#E4CFA6 40%,#B39874 100%)",boxShadow:"0 0 30px rgba(228,207,166,1)",duration:0.3,stagger:0.04},@T);'
    return [H(html, 540, 760, depth=0, fx=[(0, js), (at_more, js2)], sfxs=[(0.3, 'sparkle'), (at_more, 'riser')])] + center

def ARC(x=840, y=820, r=760, c='rgba(30,42,36,.16)', at=0, sw=90):
    svg = f'<svg width="{2 * r + sw}" height="{2 * r + sw}"><circle class="ac" cx="{r + sw / 2}" cy="{r + sw / 2}" r="{r}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="{int(3.1416 * r * 0.9)} 99999"/></svg>'
    return H(f'<div class="aw">{svg}</div>', x, y, depth=-120,
             fx=[(at, 'tl.fromTo("#ID .aw",{rotation:-160,opacity:0},{rotation:40,opacity:1,duration:5,ease:"power2.out"},@T);'
                      'tl.fromTo("#ID .ac",{strokeDashoffset:900},{strokeDashoffset:0,duration:1.4,ease:"power3.out"},@T);')], sfxs=[(at, 'whoosh')])

def LINES(at=0):
    """two long hairlines slowly rotating across the frame (reference 'una tecnica che porta la sua firma')"""
    return H('<div style="position:relative;width:1600px;height:1600px"><i class="l1" style="position:absolute;left:0;top:800px;width:1600px;height:2px;background:rgba(30,42,36,.25)"></i><i class="l2" style="position:absolute;left:0;top:800px;width:1600px;height:2px;background:rgba(179,152,116,.5)"></i></div>',
             540, 900, depth=-80, fx=[(at, 'tl.fromTo("#ID .l1",{rotation:-35},{rotation:-8,duration:6,ease:"sine.out"},@T);tl.fromTo("#ID .l2",{rotation:28},{rotation:12,duration:6,ease:"sine.out"},@T);')])

def WALL(imgs, badges, cols=4, rows=6, tw=300, th=400, rotx=24, rotz=-12, blur=0, op=1.0, at=0):
    cells = ''
    for i in range(cols * rows):
        src = imgs[i % len(imgs)]; b = badges[i % len(badges)]
        cells += (f'<div class="wt" style="position:relative;width:{tw}px;height:{th}px;border-radius:26px;overflow:hidden;box-shadow:0 20px 40px rgba(30,42,36,.28);background:#ddd">'
                  f'<img src="{src}" style="width:100%;height:100%;object-fit:cover"><div style="position:absolute;left:14px;bottom:12px;font:500 26px Jost;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.7)">▶ {b}</div></div>')
    html = (f'<div class="wl" style="display:grid;grid-template-columns:repeat({cols},{tw}px);gap:30px;transform:rotateX({rotx}deg) rotateZ({rotz}deg);filter:blur({blur}px);opacity:{op}">{cells}</div>')
    return H(html, 540, 960, depth=-300,
             fx=[(at, 'tl.fromTo("#ID .wl",{scale:1.5,opacity:0},{scale:1,opacity:%s,duration:1.1,ease:"power3.out"},@T);tl.to("#ID .wl",{y:-260,duration:6,ease:"none"},@T);' % op),
                 (at, 'tl.fromTo("#ID .wt",{z:-300},{z:0,duration:0.9,stagger:0.03,ease:"power2.out"},@T);')], sfxs=[(at, 'whoosh')])

def SHRINK_CLIP(src, at=0.9, to_scale=0.34, rotz=-12, rotx=24, x=540, y=960):
    """full-screen clip that shrinks into the wall (reference 0:05)"""
    d = dict(k='video', src=src, x=x, y=y, w=1240, h=2204, depth=200, idle=False, style='border-radius:0;box-shadow:0 40px 90px rgba(0,0,0,.35)')
    d['in'] = 'none'
    d['fx'] = [(at, f'tl.to("#ID",{{scale:{to_scale},rotation:{rotz},rotationX:{rotx},borderRadius:"70px",duration:1.0,ease:"power3.inOut"}},@T);tl.to("#ID",{{y:-220,duration:5,ease:"none"}},@T+1);')]
    d['sfxs'] = [(at, 'whoosh')]
    return d

def VCARD(src, x, y, w, h, rot, at=0, k='video', depth=60, label=None):
    it = dict(k=k, src=src, x=x, y=y, w=w, h=h, depth=depth, rot=rot, r=34,
              style='border-radius:34px;border:6px solid rgba(255,255,255,.9);box-shadow:0 40px 90px rgba(0,0,0,.45);background:#111;')
    it['in'] = 'blur'; it['at'] = at
    it['fx'] = [(at, 'tl.fromTo("#ID",{y:"+=0"},{y:"-=70",duration:5,ease:"sine.inOut"},@T);')]
    return it

def PANELS(at, word, size=360):
    """two diagonal Insula-green panels slicing in + giant faded word on the lower one (reference 'ORTOPEDICO')"""
    up = H(f'<div class="pu" style="width:2000px;height:520px;background:{GREEN};transform:rotate(-16deg)"></div>', 540, 240, depth=-150,
           fx=[(at, 'tl.fromTo("#ID .pu",{x:-1800},{x:0,duration:0.55,ease:"power4.out"},@T);')], sfxs=[(at, 'swipe')])
    dn = H(f'<div class="pd" style="position:relative;width:2000px;height:820px;background:{GREEN};transform:rotate(-16deg)">'
           f'<div style="position:absolute;left:560px;top:240px;font:600 {size}px Jost;letter-spacing:-.03em;color:rgba(244,238,227,.10);white-space:nowrap">{word}</div></div>', 540, 1760, depth=-150,
           fx=[(at, 'tl.fromTo("#ID .pd",{x:1800},{x:0,duration:0.6,ease:"power4.out"},@T+0.08);')])
    return [up, dn]

def NOTES(title, lines, x=540, y=820, at=0):
    """iOS-Notes-like list (reference 'il risultato'): lines = [(text, at, kind)] kind: '', 'strike', 'gold'"""
    rows = ''
    for i, (t, _, kd) in enumerate(lines):
        col = '#B08A3E' if kd == 'gold' else INK
        st = f'<i class="sk{i}" style="position:absolute;left:-6px;right:-6px;top:54%;height:5px;background:#C98A2B;transform:scaleX(0);transform-origin:left"></i>' if kd == 'strike' else ''
        rows += (f'<div class="nl{i}" style="display:flex;gap:22px;align-items:baseline;margin-top:30px;opacity:0"><span style="font:600 46px Jost;color:{col}">•</span>'
                 f'<span style="position:relative;font:{"600" if kd == "gold" else "500"} 50px Jost;color:{col};line-height:1.15">{t}{st}</span></div>')
    html = (f'<div style="width:900px;padding:46px 56px 60px;border-radius:44px;background:linear-gradient(180deg,#FFFDF8,#F6EFE3);box-shadow:0 40px 100px rgba(30,42,36,.20);text-align:left;white-space:normal">'
            f'<div style="display:flex;justify-content:space-between;font:400 32px Jost;color:#C09A55"><span>‹ Note</span><span>Fine</span></div>'
            f'<div style="font:600 64px \'Cormorant Garamond\';color:{INK};margin-top:24px">{title}</div>{rows}</div>')
    fx = []; sf = []
    for i, (t, a, kd) in enumerate(lines):
        fx.append((a, f'tl.fromTo("#ID .nl{i}",{{opacity:0,x:-30,filter:"blur(8px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:0.35,ease:"power2.out"}},@T);'))
        sf.append((a, 'key'))
        if kd == 'strike':
            fx.append((a, f'tl.to("#ID .sk{i}",{{scaleX:1,duration:0.4,ease:"power2.inOut"}},@T+0.55);')); sf.append((a, 'swipe'))
    return H(html, x, y, in_='blur', dt=0, depth=40, fx=fx, sfxs=sf)

def TIMELINE(steps, y=760, gap=380):
    """icons in circles joined by a progress line that fills node by node; camera pans then zooms out"""
    n = len(steps); W = (n - 1) * gap + 240
    nodes = ''
    for i, (ico, lab, _) in enumerate(steps):
        nodes += (f'<div class="nd{i}" style="position:absolute;left:{i * gap}px;top:0;width:240px;text-align:center">'
                  f'<div class="cc{i}" style="width:200px;height:200px;margin:0 auto;border-radius:50%;background:#EDE6DA;display:flex;align-items:center;justify-content:center;box-shadow:0 24px 50px rgba(30,42,36,.18)">'
                  f'<span style="font-size:96px;filter:grayscale(1);opacity:.5" class="ic{i}">{ico}</span></div>'
                  f'<div style="font:500 40px Jost;color:{INK};margin-top:26px;white-space:nowrap">{lab}</div></div>')
    line = (f'<div style="position:absolute;left:120px;top:96px;width:{W - 240}px;height:10px;border-radius:5px;background:#E6DED1"></div>'
            f'<div class="pl" style="position:absolute;left:120px;top:96px;width:{W - 240}px;height:10px;border-radius:5px;background:{GOLD};transform:scaleX(0);transform-origin:left"></div>')
    html = f'<div class="mv" style="position:relative;width:{W}px;height:320px">{line}{nodes}</div>'
    fx = []; sf = []
    for i, (_, _, a) in enumerate(steps):
        cx = -(i * gap + 120 - W / 2)
        js = (f'tl.to("#ID .mv",{{x:{cx if n > 2 else 0},scale:1.15,duration:0.6,ease:"power3.inOut"}},@T);' if n > 2 else '')
        js += (f'tl.to("#ID .pl",{{scaleX:{i / (n - 1):.3f},duration:0.5,ease:"power2.out"}},@T);'
               f'tl.to("#ID .cc{i}",{{background:"{GREEN}",scale:1.12,duration:0.35,ease:"back.out(2)"}},@T+0.1);'
               f'tl.to("#ID .ic{i}",{{filter:"grayscale(0)",opacity:1,duration:0.3}},@T+0.1);')
        fx.append((a, js)); sf.append((a, 'pop'))
    last = steps[-1][2]
    fx.append((last, f'tl.to("#ID .mv",{{x:0,scale:{min(1.0, 980 / W):.3f},duration:0.9,ease:"power3.inOut"}},@T+0.9);'))
    first_x = W / 2 - 120 if n > 2 else 0
    fx.insert(0, (0, f'gsap.set("#ID .mv",{{x:{first_x}}});tl.fromTo("#ID .mv",{{opacity:0,filter:"blur(16px)"}},{{opacity:1,filter:"blur(0px)",duration:0.5}},@T);'))
    return H(html, 540, y, depth=60, fx=fx, sfxs=sf)

def AVATARS(at_one, at_all, n=10, R=330):
    import math
    av = ''
    for i in range(n):
        a = i / n * 6.283
        av += (f'<div class="av av{i}" style="position:absolute;left:{R + 110 + R * math.cos(a) - 70:.0f}px;top:{R + 110 + R * math.sin(a) - 70:.0f}px;width:140px;height:140px;border-radius:50%;background:#2A3B33;overflow:hidden;box-shadow:0 14px 30px rgba(0,0,0,.4)">'
               f'<svg viewBox="0 0 100 100" width="140" height="140"><circle cx="50" cy="38" r="17" fill="#5E7067"/><path d="M18,96 C20,66 80,66 82,96Z" fill="#5E7067"/></svg></div>')
    html = f'<div class="rgA" style="position:relative;width:{2 * R + 220}px;height:{2 * R + 220}px">{av}</div>'
    fx = [(0, 'tl.fromTo("#ID .rgA",{rotation:-30,scale:.6,opacity:0},{rotation:40,scale:1,opacity:1,duration:6,ease:"power1.out"},@T);tl.fromTo("#ID .av",{scale:0},{scale:1,duration:0.4,stagger:0.05,ease:"back.out(2)"},@T+0.2);'),
          (at_one, f'tl.to("#ID .av0",{{background:"{GOLD}",scale:1.25,duration:0.35,ease:"back.out(3)"}},@T);tl.to("#ID .av0 path,#ID .av0 circle",{{fill:"#FFF6E6",duration:0.3}},@T);'),
          (at_all, f'tl.to("#ID .av",{{background:"{LIL}",duration:0.3,stagger:0.06}},@T);tl.to("#ID .av path,#ID .av circle",{{fill:"#FFFFFF",duration:0.3,stagger:0.06}},@T);')]
    return H(html, 540, 860, depth=0, fx=fx, sfxs=[(at_one, 'ding'), (at_all, 'sparkle')])

def KINETIC(word, at=0, y=900):
    sp = ''.join(f'<span class="k{i}" style="display:inline-block">{ch}</span>' for i, ch in enumerate(word))
    html = f'<div class="kw" style="font:300 330px Jost;letter-spacing:-.04em;color:#F4EEE3;white-space:nowrap">{sp}</div>'
    js = 'tl.fromTo("#ID .kw",{x:700},{x:-700,duration:3.2,ease:"power1.inOut"},@T);'
    js += ''.join(f'tl.fromTo("#ID .k{i}",{{rotationY:-95,z:-600,opacity:0}},{{rotationY:0,z:0,opacity:1,duration:0.5,ease:"power3.out"}},@T+{i * 0.07:.2f});' for i in range(len(word)))
    return H(html, 540, y, depth=80, fx=[(at, js)], sfxs=[(at, 'whoosh'), (at, 'riser')])

def IGOUT(at):
    svg = ('<svg viewBox="0 0 24 24" width="300" height="300"><defs><linearGradient id="igg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#F9CE34"/><stop offset=".5" stop-color="#EE2A7B"/><stop offset="1" stop-color="#6228D7"/></linearGradient></defs>'
           '<rect x="2.5" y="2.5" width="19" height="19" rx="5.5" fill="none" stroke="url(#igg)" stroke-width="2"/><circle cx="12" cy="12" r="4.3" fill="none" stroke="url(#igg)" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.2" fill="#EE2A7B"/></svg>')
    html = (f'<div style="text-align:center"><div class="ig" style="display:inline-block">{svg}</div>'
            f'<div class="hd" style="font:500 40px Jost;letter-spacing:.12em;color:#F4EEE3;margin-top:20px">@INSULAMEDICALAGENCY</div></div>')
    return H(html, 540, 1060, depth=200, fx=[(at, 'tl.fromTo("#ID .ig",{scale:0,rotation:-120},{scale:1,rotation:0,duration:0.7,ease:"back.out(2)"},@T);'
                                                   'tl.fromTo("#ID .ig",{filter:"hue-rotate(0deg)"},{filter:"hue-rotate(300deg)",duration:3,ease:"none"},@T+0.7);'
                                                   'tl.fromTo("#ID .hd",{opacity:0,y:30},{opacity:1,y:0,duration:0.5},@T+0.4);')], sfxs=[(at, 'pop'), (at, 'sparkle')])

def RIBBON(at=0, c='rgba(205,184,216,.35)'):
    return H(f'<svg width="1200" height="2000"><path class="rb" d="M-50,1700 C300,1500 200,1100 600,1000 S1000,500 700,100" fill="none" stroke="{c}" stroke-width="70" stroke-linecap="round" stroke-dasharray="2600" stroke-dashoffset="2600"/></svg>',
             540, 960, depth=-200, fx=[(at, 'tl.to("#ID .rb",{strokeDashoffset:0,duration:2.2,ease:"power2.inOut"},@T);')])

def BADGE(txt, x, y, at, size=54, bg=GREEN, c='#F4EEE3'):
    d = HT(f'<div style="padding:16px 34px;border-radius:999px;background:{bg};color:{c};font:500 {size}px Jost;box-shadow:0 20px 40px rgba(30,42,36,.25)">{txt}</div>', x, y)
    d.update({'in': 'pop', 'at': at, 'depth': 180}); return d

def PROFILE(at=0):
    return H(f'''<div style="width:900px;display:flex;align-items:center;gap:26px;padding:26px 30px;border-radius:32px;background:rgba(255,255,255,.9);box-shadow:0 30px 70px rgba(30,42,36,.18);text-align:left">
<img src="{M3}i0630.png" style="width:110px;height:110px;border-radius:50%;object-fit:cover;object-position:50% 18%">
<div style="flex:1"><div style="font:600 36px Jost;color:{INK}">Doctor Mike <span style="color:#3897F0">✓</span></div><div style="font:300 24px Jost;color:#5B6760">Medico di famiglia · YouTube</div>
<div style="display:flex;gap:38px;margin-top:10px;font:400 24px Jost;color:#5B6760"><span><b style="font-weight:600;color:{INK}">15,1 Mln</b> iscritti</span><span><b style="font-weight:600;color:{INK}">1,3K</b> video</span><span><b style="font-weight:600;color:{INK}">5,6 Mld</b> views</span></div></div></div>''',
             540, 250, depth=120, in_='down', at=at, sfxs=[(at, 'swipe')])

def COLLAGE(imgs, at=0):
    rnd = random.Random(11); out = []
    spots = [(250, 420, -6), (720, 360, 5), (470, 640, 2), (860, 700, -4), (200, 860, 7), (620, 960, -3), (330, 1170, 4), (850, 1120, 6), (560, 1320, -5), (180, 1400, -2)]
    for i, (x, y, r) in enumerate(spots):
        src = imgs[i % len(imgs)]; bw = 'grayscale(1)' if i % 3 == 0 else 'none'
        it = dict(k='img', src=src, x=x, y=y, w=330, h=230 if i % 2 else 400, r=18, rot=r, depth=20 + i * 8, idle=False,
                  style=f'box-shadow:0 30px 60px rgba(30,42,36,.30);border:6px solid #fff;filter:{bw};')
        it['in'] = 'none'
        dx, dy = rnd.choice([-900, 900]), rnd.uniform(-600, 600)
        it['fx'] = [(at, f'tl.fromTo("#ID",{{x:{dx},y:{dy:.0f},rotation:{r * 6},opacity:0}},{{x:0,y:0,rotation:{r},opacity:1,duration:0.7,ease:"power3.out"}},@T+{i * 0.12:.2f});')]
        it['sfxs'] = [(at + i * 0.12 if isinstance(at, (int, float)) else at, 'click')]
        out.append(it)
    return out

THUMBS = [M4 + 'th_good.jpg', M4 + 'th_greys.jpg', M4 + 'th_tiktok.jpg', M4 + 'th_jelly.jpg', 'assets/img/mike_tile1.jpg', 'assets/img/mike_tile2.jpg',
          M4 + 'mike_dieta_f2.jpg', 'assets/img/mike_tile3.jpg', M4 + 'mike_podcast_f1.jpg', 'assets/img/mike_tile4.jpg', M4 + 'ospite_f1.jpg', 'assets/img/mike_tile5.jpg']
VIEWS = ['44 Mln', '33 Mln', '32 Mln', '30 Mln', '12 Mln', '8,4 Mln', '5,1 Mln', '27 Mln', '3,2 Mln', '9,8 Mln']

# --------------------------------------------------------------------------------------------- scenes
V = [
 # 1 giant number behind the cut-out + profile card from the top
 S(NUMBER(5.6, 540, 560, 400, suf='', dec=1, c=GREEN, at=0.1, dur=1.6),
   H(f'<div style="font:400 44px Jost;letter-spacing:.3em;color:{GOLD}">MILIARDI</div>', 540, 400, in_='blur', dt=0.4),
   CUT(M3 + 'i0630_cut.png', 540, 1400, 1150, (1206, 1500), in_='up', idle=False),
   PROFILE(at='visualizzazioni'), capy=1660, capbox=True, capsize=54),
 # 2 full clip shrinks into a 3D wall of reels
 S(WALL(THUMBS, VIEWS, at=0.9), SHRINK_CLIP('assets/mike_clips/mike_dieta.mp4', at=0.9),
   BADGE('15,1 Mln iscritti', 540, 1480, at='YouTube', size=60), capy=1640, capbox=True),
 # 3 phone + green circle + big number + script word with reflection; swaps to TikTok
 S(H(f'<div class="cr" style="width:700px;height:700px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#2E5443,{GREEN} 70%)"></div>', 540, 740, depth=-200,
     fx=[(0, 'tl.fromTo("#ID .cr",{scale:0},{scale:1,duration:0.8,ease:"back.out(1.6)"},@T);')]),
   CARD('doctor.mike', 'ha iniziato a seguirti', 290, 380, at=0.3, w=420, blur=2, depth=-60, icon='♥'),
   CARD('Nuovo commento', '"Finalmente chiaro!"', 790, 560, at=0.6, w=400, blur=1, depth=-40, icon='💬'),
   o(phone(f'<img src="assets/img/mike_ig_full.jpg" style="position:absolute;left:0;top:0;width:100%"><img class="tk" src="{M4}tiktok_clean.png" style="position:absolute;left:0;top:0;width:100%;opacity:0;background:#fff">', 540, 740, 0.7),
     **{'in': 'up', 'idle': True, 'fx': [('TikTok', 'tl.fromTo("#ID .tk",{opacity:0,filter:"blur(14px)",scale:1.08},{opacity:1,filter:"blur(0px)",scale:1,duration:0.45,ease:"power2.out"},@T);')], 'sfxs': [('TikTok', 'swipe')]}),
   H(f'<div class="n1" style="font:300 190px Jost;letter-spacing:-.03em;color:{INK}">5,6 Mln</div>', 540, 1250, depth=220,
     fx=[(0.4, 'tl.fromTo("#ID .n1",{opacity:0,filter:"blur(20px)",scale:1.2},{opacity:1,filter:"blur(0px)",scale:1,duration:0.6},@T);'),
         ('Tre', 'tl.to("#ID .n1",{opacity:0,filter:"blur(20px)",duration:0.3},@T-0.3);')]),
   H(f'<div class="n2" style="font:300 190px Jost;letter-spacing:-.03em;color:{INK};opacity:0">3,1 Mln</div>', 540, 1250, depth=220,
     fx=[('Tre', 'tl.fromTo("#ID .n2",{opacity:0,filter:"blur(20px)",scale:1.2},{opacity:1,filter:"blur(0px)",scale:1,duration:0.6},@T);')]),
   SCRIPT('follower', 540, 1450, 110, at=0.8), capy=1640),
 # 4 phrase builder with highlight boxes + ghost word
 S(LINES(0), capy=900, capsize=74, capmax=4),
 # 5 portrait + diagonal green panels + layered giant words
 S(PANELS(0.2, 'MEDICO'),
   CUT('assets/img/mike_palco_cut.png', 560, 1150, 1250, (1206, 1481), in_='blur', idle=False),
   GIANT('Doctor', 540, 930, 210, c='#F4EEE3', op=1, at=0.1, it=True, extra='text-shadow:0 8px 34px rgba(15,30,23,.55),0 2px 6px rgba(15,30,23,.45);'),
   H(f'<div class="mf" style="font:600 92px Jost;letter-spacing:-.02em;color:#F4EEE3;white-space:nowrap">medico di famiglia</div>', 540, 1580, depth=240,
     fx=[('medico', 'tl.fromTo("#ID .mf",{scaleX:2.4,opacity:0,filter:"blur(16px)"},{scaleX:1,opacity:1,filter:"blur(0px)",duration:0.6,ease:"power4.out"},@T);')], sfxs=[('medico', 'boom')]),
   BADGE('New Jersey, USA', 540, 1440, at='Jersey', size=46, bg=GOLD), capy=300, capbox=True),
 # 6 b/w full-bleed magazine page + white flash
 S(dict(k='img', src=M3 + 'i0632.jpg', **FULL, r=0, depth=-150, idle=False, pos='top', style='filter:grayscale(1) contrast(1.05) brightness(.8);',
        fx=[(0, 'tl.fromTo("#ID",{scale:1.25},{scale:1.05,duration:5,ease:"none"},@T);')], **{'in': 'none'}),
   H('<div style="width:1400px;height:2400px;background:linear-gradient(180deg,rgba(15,30,23,.2) 0%,rgba(15,30,23,.55) 45%,rgba(15,30,23,.92) 62%)"></div>', depth=-140),
   BADGE('People · 2015', 540, 380, at='rivista', size=48, bg=GOLD, c=INK), FLASH(0), dark=True, bg='#111', capy=1250, capsize=64),
 # 7 orbit rings with particles + centre number
 S(ORBIT('follower', NUMBER(1, 540, 760, 230, suf=' Mln', c=VIOLET, at='milione', dur=1.0)), capy=1400),
 # 8 giant rotating arc + rising / crashing line
 S(ARC(820, 900, 700), H(f'''<svg width="900" height="520"><path class="up" d="M20,480 C200,470 300,440 380,380 S470,60 520,40" fill="none" stroke="{GREEN}" stroke-width="12" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200"/>
<path class="dn" d="M520,40 C560,120 600,420 880,490" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-dasharray="900" stroke-dashoffset="900"/></svg>''', 540, 720, depth=60,
     fx=[('altro', 'tl.to("#ID .up",{strokeDashoffset:0,duration:1.1,ease:"power2.out"},@T);'), ('poi', 'tl.to("#ID .dn",{strokeDashoffset:0,duration:0.8,ease:"power2.in"},@T);')],
     sfxs=[('altro', 'riser'), ('poi', 'swipe')]), capy=1250, capsize=66),
 # 9 phrase with highlight boxes + hairlines (reference 'porta la sua firma')
 S(LINES(0), capy=900, capsize=68, capmax=5),
 # 10 coin I
 S(COIN(1), FLASH(0), capy=1400),
 # 11 scrolling outlined names switch + lower-third
 S(ROWS('MIKHAIL VARSHAVSKI', at=0, switch='Doctor', txt2='DOCTOR MIKE'),
   CUT(M3 + 'i0630_cut.png', 540, 1100, 1300, (1206, 1500), in_='blur', idle=False),
   LOWER3('Mike', 'MIKHAIL VARSHAVSKI · MEDICO', y=1390, at='Doctor', pre='Doctor'), capy=1600, capbox=True),
 # 12 icon timeline
 S(TIMELINE([('🩺', 'cosa fa', 'Due'), ('🙂', 'chi è', 'chi'), ('🧠', 'lo ricordi', 'ricordi')]), capy=1300),
 # 13 coin II
 S(COIN(2), capy=1400),
 # 14 dark: floating tilted video cards
 S(VCARD(M4 + 'th_greys.jpg', 300, 520, 500, 290, -8, at=0, k='img'),
   VCARD(M4 + 'th_good.jpg', 780, 820, 500, 290, 7, at='House', k='img'),
   VCARD('assets/mike_clips/mike_dieta.mp4', 360, 1180, 380, 540, -5, at='bufale'),
   H('<svg width="900" height="900" viewBox="0 0 100 100"><path d="M25,12 L88,50 L25,88Z" fill="none" stroke="rgba(244,238,227,.06)" stroke-width="3" stroke-linejoin="round"/></svg>', 540, 900, depth=-300),
   RIBBON(0, 'rgba(179,152,116,.18)'), dark=True, capy=1600),
 # 15 notes list
 S(NOTES('In corsia', [('«Questo succede davvero?»', 0.15, ''), ('Questo sì', 'davvero', 'gold'), ('Questo no.', 'no', 'strike')], y=780),
   VCARD('assets/mike_clips/mike_chirurgo.mp4', 790, 1250, 300, 430, 6, at='davvero'), capy=1560, capbox=True),
 # 16 wall behind + two featured thumbnails with counting views
 S(WALL(THUMBS[2:], VIEWS[2:], blur=5, op=0.45, at=0),
   o(VCARD(M4 + 'th_greys.jpg', 540, 560, 760, 430, -4, at=0, k='img'), depth=120),
   BADGE('<span>▶ </span>33 Mln', 780, 820, at='33', size=58, bg=VIOLET),
   o(VCARD(M4 + 'th_good.jpg', 540, 1090, 760, 430, 3, at='Quella', k='img'), depth=140),
   BADGE('<span>▶ </span>44 Mln', 300, 1400, at='44', size=58, bg=GREEN), capy=1620, capbox=True),
 # 17 giant arc around the key word (reference 'quella competenza')
 S(ARC(300, 980, 620, c='rgba(30,58,47,.22)'), FLASH(0), capy=930, capsize=72, capmax=4),
 # 18 coin III
 S(COIN(3), capy=1400),
 # 19 collage of thumbnails + counter
 S(COLLAGE(THUMBS, at=0.1), H('<div style="width:1300px;height:900px;background:radial-gradient(closest-side,rgba(248,244,238,.95),rgba(248,244,238,0))"></div>', 540, 1500, depth=150),
   NUMBER(1300, 540, 1480, 210, suf='+', c=GREEN, at='milletrecento', dur=1.2), capy=1720, capbox=True),
 # 20 dark: ring of avatars lighting up
 S(AVATARS('montatore', 'squadra'), dark=True, capy=860, capsize=62),
 # 21 dark: podcast cards
 S(VCARD(M3 + 'podcast_ospite.mp4', 330, 640, 430, 600, -7, at=0),
   VCARD(M4 + 'podcast_clean.mp4', 760, 960, 440, 404, 6, at='podcast'),
   VCARD(M3 + 'i0627.png', 330, 1330, 380, 420, 4, at='Checkup', k='img'),
   BADGE('★ 4,9 su Spotify', 760, 1420, at='Checkup', size=44, bg=GOLD, c=INK), RIBBON(0, 'rgba(205,184,216,.15)'), dark=True, capy=1680),
 # 22 dark: giant kinetic word + ghost 'hobby'
 S(H(f'<div style="font:600 260px Jost;color:rgba(205,184,216,.08);writing-mode:vertical-rl;letter-spacing:.1em">HOBBY</div>', 860, 900, depth=-200, in_='fade'),
   KINETIC('ambulatorio', at='organizzato', y=980), dark=True, capy=560, capsize=60),
 # 23 coin IV
 S(COIN(4), FLASH(0), capy=1400),
 # 24 portrait + panels
 S(PANELS(0.15, 'MEDICO'), GIANT('medico', 540, 640, 210, c=GREEN, it=True, at=0.1),
   CUT(M3 + 'i0631_cut.png', 540, 1200, 1100, (1206, 1487), in_='blur', idle=False),
   BADGE('in attività', 540, 1620, at='medico', size=52, bg=GOLD, c=INK), capy=1760),
 # 25 notes: correction
 S(NOTES('Il video', [('Un\'affermazione imprecisa', 0.1, 'strike'), ('Correzione pubblica ✓', 'corregge', 'gold')], y=700),
   VCARD('assets/mike_clips/mike_chirurgo.mp4', 540, 1260, 330, 470, -4, at='sbaglia'), capy=1640, capbox=True),
 # 26 phone + circle + big number + script word (charity)
 S(H(f'<div class="cr" style="width:700px;height:700px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#D9C6E3,{LIL} 70%)"></div>', 540, 700, depth=-200,
     fx=[(0, 'tl.fromTo("#ID .cr",{scale:0},{scale:1,duration:0.8,ease:"back.out(1.6)"},@T);')]),
   CARD('Borse di studio', 'Limitless Tomorrow', 250, 360, at='borse', w=440, depth=-40, icon='🎓'),
   o(phone(f'<img src="{M3}i0626.png" style="position:absolute;left:0;top:0;width:100%">', 540, 680, 0.62), **{'in': 'up'}),
   NUMBER(1, 540, 1200, 180, suf=' Mln $+', c=GREEN, at='oltre', dur=1.0),
   SCRIPT('beneficenza', 540, 1360, 105, at='beneficenza'), capy=1600),
 # 27 names rows + portrait + lower-third
 S(ROWS('DOCTOR MIKE', at=0), CUT('assets/img/mike_ritratto_cut.png', 540, 1000, 860, (1206, 863), in_='blur', idle=False),
   LOWER3('Mike', 'IL VOLTO DEI BRAND DELLA SALUTE', y=1300, at='brand', pre='Doctor'), capy=1580, capbox=True),
 # 28 flash + phrase + struck ghost
 S(GIANT('Doctor Mike', 540, 700, 210, c=LIL, op=0.6, it=True, at=0), FLASH(0), LINES(0), capy=1000, capsize=70, capmax=5),
 # 29 four-step timeline with pan + zoom out
 S(TIMELINE([('🏷️', 'un nome', 'nome'), ('🎬', 'contenuti', 'contenuti'), ('📅', 'costanza', 'costanza'), ('🛡️', 'credibilità', 'credibilità')], y=760), capy=1300),
 # 30 Insula rows + logo + lower-third + code badge
 S(ROWS('INSULA', at=0), o(dict(k='img', src='assets/img/insula-logo.webp', x=540, y=720, w=440, h=440, r=220, depth=120), **{'in': 'blur'}),
   LOWER3('Medical Agency', 'COMUNICAZIONE MEDICA · PALERMO', y=1080, at='Insula', pre='Insula'),
   BADGE('✓ codice deontologico', 540, 1260, at='codice', size=48, bg=LIL, c=INK), capy=1520, capbox=True),
 # 31 dark outro: comment field + Instagram logo + ribbon
 S(RIBBON(0, 'rgba(205,184,216,.20)'),
   H(f'<div style="display:flex;align-items:center;gap:22px;padding:22px 30px;border-radius:999px;background:rgba(255,255,255,.95);width:760px;box-shadow:0 30px 70px rgba(0,0,0,.4)">'
     f'<div style="width:66px;height:66px;border-radius:50%;background:{GOLD}"></div><div style="flex:1;text-align:left;font:600 54px Jost;color:{INK}">{{{{TYPE:BRAND}}}}</div><div style="font:600 34px Jost;color:#3897F0">Pubblica</div></div>',
     540, 640, depth=160, in_='blur', type_at='BRAND', rate=0.16),
   IGOUT('privato'), dark=True, capy=900, capsize=60),
]

EMPH = {
    "E non è un attore, / non è un influencer.": "E non è un *attore*, / non è un *influencer*.",
    "Mikhail Varshavski diventa *Doctor Mike*.": "*Mikhail Varshavski* diventa *Doctor Mike*.",
    "Tu non devi diventare Doctor Mike.": "Tu *non* devi diventare *Doctor Mike*.",
    "Il suo canale non è un hobby: / è organizzato come un ambulatorio.": "Il suo canale non è un *hobby*: / è organizzato come un *ambulatorio*.",
    "Se vuoi capire quale potrebbe essere il tuo, / commentami *BRAND* / e ti scrivo in privato.": "Se vuoi capire quale potrebbe essere il tuo, / commentami *BRAND* / e ti scrivo in privato.",
}
BRAND4 = []
for b, v in zip(BRAND3, V):
    t = EMPH.get(b['t'], b['t'])
    BRAND4.append(dict(t=t, v=v))
assert len(BRAND4) == 31

TRANS = [('{z:-700,opacity:0}', '{z:700,opacity:0}'),
         ('{x:900,opacity:0}', '{x:-900,opacity:0}'),
         ('{scale:1.5,opacity:0}', '{scale:0.7,opacity:0}'),
         ('{y:-700,opacity:0}', '{y:700,opacity:0}')]

CSS = CSS3 + f"""
.floorwrap{{display:none}}
.b1{{background:radial-gradient(circle,#E2D3EA 0%,rgba(226,211,234,0) 70%)}}
.b2{{background:radial-gradient(circle,#F0E2CB 0%,rgba(240,226,203,0) 70%)}}
.pcap{{position:absolute;left:150px;width:780px;text-align:center;font-family:Jost,sans-serif;font-weight:300;color:{INK};line-height:1.22;letter-spacing:-.005em;white-space:normal}}
.pcap .pin{{display:inline-block;white-space:normal}}
.pcap.box .pin{{background:rgba(255,253,248,.88);padding:14px 30px 18px;border-radius:26px;box-shadow:0 20px 50px rgba(30,42,36,.15)}}
.pcap .pw{{display:inline-block;margin:0 .1em}}
.pcap .emw{{padding:0 .16em .06em;margin:0 .02em;border-radius:12px;font-weight:500;color:#F4EEE3;background:linear-gradient({GREEN},{GREEN}) no-repeat left center/0% 100%}}
.pcap.dark{{color:#F4EEE3;text-shadow:0 4px 24px rgba(0,0,0,.45)}}
.pcap.dark .emw{{color:{INK};text-shadow:none;background-image:linear-gradient({GOLD},{GOLD})}}
.pcap.dark.box .pin{{background:rgba(15,30,23,.6)}}
"""

"""VIDEO 2 – SITO, v3: own visual identity ('night & screens'): dark scenes, neon accents, UI that moves."""
import random
from widgets import E, T, HT, chip, tag, counter, phone, cta
from sito_fx import desk_new, desk_old, macbook, glow, time_picker, darkness, spotlight, worried_guy, google_scroll, booking, confetti

NIGHT = '#0B1120'
NEON = '#39E75F'
LIL = '#CDB8D8'

def o(it, **kw):
    if 'in_' in kw: kw['in'] = kw.pop('in_')
    d = dict(it); d.update(kw); return d

def S(*items, **kw):
    d = dict(items=[i for i in items if i], bg=NIGHT, dark=True); d.update(kw); return d

def flat(*xs):
    out = []
    for x in xs:
        out += x if isinstance(x, list) else [x]
    return out

GLASS = 'background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.14);box-shadow:0 30px 80px rgba(0,0,0,.45);backdrop-filter:blur(20px);'

# ------------------------------------------------------------------ HUD section title (replaces the big 1-2-3)
def hud(n, label, icon, at=0):
    bars = ''.join(f'<i style="display:block;flex:1;height:10px;border-radius:5px;background:{NEON if i < n else "rgba(255,255,255,.15)"};box-shadow:{"0 0 14px " + NEON if i < n else "none"}"></i>' for i in range(3))
    panel = HT(f'''<div style="width:860px;padding:44px 50px;border-radius:40px;{GLASS}text-align:left;white-space:normal;font-family:Inter;color:#fff">
<div style="font-size:28px;letter-spacing:.32em;font-weight:800;color:{NEON}">DETTAGLIO 0{n}</div>
<div class="serif" style="font-size:110px;font-style:italic;line-height:1;margin-top:18px">{label}</div>
<div style="display:flex;gap:12px;margin-top:34px">{bars}</div></div>''', 540, 760)
    panel.update({'in': 'zoom', 'at': at, 'sfxs': [(at, 'boom')]})
    return [panel, o(E(icon, 860, 470, 200), in_='spin', at=at)]

# ------------------------------------------------------------------ comparison board with 3D flip tiles
def board():
    head = HT(f'''<div style="width:900px;display:flex;justify-content:space-around;font-family:Inter;font-weight:800;font-size:34px;color:#fff">
<div>Dott. Bianchi</div><div>Dott. Neri</div></div>''', 540, 360)
    items = [o(head, in_='down', at=0), o(E('👩‍⚕️', 315, 200, 120), in_='pop', at=0), o(E('👨‍⚕️', 765, 200, 120), in_='pop', at=0)]
    rows = [
        ('stesso', 560, '<div style="font-size:70px;line-height:1">📜</div><div style="font-size:30px;font-weight:800;margin-top:8px">Laurea + Specializzazione</div>', 'curriculum'),
        ('stessa', 800, '<div class="map" style="width:100%;height:150px;border-radius:18px;background:linear-gradient(135deg,#1c2a44,#24365a);position:relative;overflow:hidden"><div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.08) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.08) 2px,transparent 2px);background-size:34px 34px"></div><div class="pin" style="position:absolute;left:50%;top:18px;margin-left:-30px;font-size:60px">📍</div></div><div style="font-size:30px;font-weight:800;margin-top:8px">Palermo</div>', 'città'),
        ('stesso#2', 1040, '<div style="font-size:84px;font-weight:900;color:#39E75F;text-shadow:0 0 20px rgba(57,231,95,.6)">€ <span class="pr">120</span></div><div style="font-size:30px;font-weight:800">la visita</div>', 'prezzo'),
    ]
    for at, y, inner, word in rows:
        for x in (315, 765):
            tile = HT(f'<div style="width:370px;height:220px;border-radius:30px;{GLASS}display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-family:Inter;text-align:center;white-space:normal;padding:16px">{inner}</div>', x, y)
            tile.update({'in': 'flip', 'at': at, 'idle': False})
            fx = []
            if word == 'città': fx.append((at, 'tl.fromTo("#ID .pin",{y:-160,opacity:0},{y:0,opacity:1,duration:0.5,ease:"bounce.out",immediateRender:false},@T+0.25);'))
            if word == 'prezzo': fx.append((at, '(function(){var o={v:40},n=document.querySelector("#ID .pr");tl.to(o,{v:120,duration:0.9,ease:"power3.out",onUpdate:function(){n.textContent=Math.round(o.v/5)*5;}},@T+0.1);tl.set(o,{v:40},0);})();'))
            tile['fx'] = fx
            items.append(tile)
        eq = HT(f'<div style="width:90px;height:90px;border-radius:50%;background:{NEON};color:#0B1120;font:900 60px Inter;display:flex;align-items:center;justify-content:center;box-shadow:0 0 30px {NEON}">=</div>', 540, y)
        eq.update({'in': 'pop', 'at': word, 'sfxs': [(word, 'ding')]})
        items.append(eq)
    return items

# ------------------------------------------------------------------ lock screen with booking notifications
def lockscreen(ats):
    notes = ''.join(f'''<div class="nt{i}" style="margin:14px 18px;padding:18px 20px;border-radius:26px;background:rgba(255,255,255,.88);display:flex;gap:16px;align-items:center;text-align:left;opacity:0">
<div style="width:62px;height:62px;border-radius:16px;background:#1E3A2F;color:#fff;font-size:34px;display:flex;align-items:center;justify-content:center">📅</div>
<div><div style="font-weight:800;font-size:24px;color:#111">Nuova prenotazione</div><div style="font-size:21px;color:#555">{s}</div></div></div>''' for i, s in enumerate(['Visita cardiologica · 23:14', 'Holter 24h · 23:41', 'ECG · 00:07']))
    screen = f'''<div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#3b2b5c,#0b1120 70%);font-family:Inter;color:#fff;text-align:center;white-space:normal">
<div style="margin-top:120px;font-size:30px;opacity:.8">martedì 24 novembre</div><div style="font-size:150px;font-weight:700;letter-spacing:-.04em;line-height:1">23:14</div>
<div style="margin-top:40px">{notes}</div></div>'''
    ph = phone(screen, 540, 820, 0.92)
    ph['in'] = 'up'
    ph['fx'] = []
    for i, at in enumerate(ats):
        ph['fx'].append((at, f'tl.fromTo("#ID .nt{i}",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"back.out(2)",immediateRender:false}},@T);tl.to("#ID",{{x:8,duration:0.05,yoyo:true,repeat:7}},@T);'))
    ph['sfxs'] = [(at, 'ding') for at in ats]
    return [ph, o(T('🌙', 880, 300, 110), in_='fade', at=0)]

# ------------------------------------------------------------------ analytics dashboard flat at zero
def dead_dashboard():
    pts = ' '.join(f'{x},{200 - (2 if x % 120 else 4)}' for x in range(0, 801, 40))
    card = HT(f'''<div style="width:900px;padding:40px;border-radius:36px;{GLASS}color:#fff;font-family:Inter;text-align:left;white-space:normal">
<div style="font-size:26px;color:#9aa;font-weight:700">STATISTICHE · dottneri.it</div>
<div style="display:flex;gap:40px;margin:16px 0 20px"><div><div style="font-size:24px;color:#9aa">Visite oggi</div><div style="font-size:110px;font-weight:900;color:#D7192B">0</div></div>
<div><div style="font-size:24px;color:#9aa">Prenotazioni</div><div style="font-size:110px;font-weight:900;color:#D7192B">0</div></div></div>
<svg width="820" height="220" viewBox="0 0 800 220"><polyline class="ln" points="{pts}" fill="none" stroke="#D7192B" stroke-width="6" stroke-dasharray="1200" stroke-dashoffset="1200"/></svg></div>''', 540, 760)
    card['in'] = 'up'
    card['fx'] = [(0.3, 'tl.to("#ID .ln",{strokeDashoffset:0,duration:1.6,ease:"none"},@T);')]
    return [card, o(E('🕸️', 880, 420, 190), in_='fade', at='nessuno'), o(E('🦗', 250, 1180, 120), in_='walkr', at='apre')]

# ------------------------------------------------------------------ browser tabs + toggle
def tabs_toggle():
    tabs = ''.join(f'<div class="tb{i}" style="padding:16px 30px;border-radius:18px 18px 0 0;background:{["#1E3A2F", "#5B3A66", "#B39874"][i]};color:#fff;font:800 26px Inter;opacity:0">Dettaglio {i + 1}</div>' for i in range(3))
    win = HT(f'''<div style="width:900px;border-radius:30px;overflow:hidden;{GLASS}text-align:left">
<div style="display:flex;gap:10px;align-items:flex-end;padding:18px 20px 0;background:rgba(0,0,0,.35)"><span style="color:#f55;font-size:26px">●</span><span style="color:#fb3;font-size:26px">●</span><span style="color:#3c5;font-size:26px;margin-right:16px">●</span>{tabs}</div>
<div style="height:300px;display:flex;align-items:center;justify-content:space-between;padding:0 70px;font:800 44px Inter;color:#fff">
<span class="lv" style="opacity:.9">vetrina</span>
<div class="sw" style="width:220px;height:110px;border-radius:999px;background:#444;position:relative"><div class="kn" style="position:absolute;top:10px;left:10px;width:90px;height:90px;border-radius:50%;background:#fff;box-shadow:0 6px 16px rgba(0,0,0,.4)"></div></div>
<span class="lw" style="opacity:.4">lavora per te</span></div></div>''', 540, 700)
    win['in'] = 'up'
    win['fx'] = [(f'tre', 'tl.to("#ID .tb0",{opacity:1,duration:0.2},@T);tl.to("#ID .tb1",{opacity:1,duration:0.2},@T+0.2);tl.to("#ID .tb2",{opacity:1,duration:0.2},@T+0.4);'),
                 ('lavora', 'tl.to("#ID .kn",{x:110,duration:0.35,ease:"back.out(2)"},@T);tl.to("#ID .sw",{backgroundColor:"#39E75F",boxShadow:"0 0 40px #39E75F",duration:0.3},@T);tl.to("#ID .lw",{opacity:1,color:"#39E75F",duration:0.3},@T);tl.to("#ID .lv",{opacity:.35,duration:0.3},@T);')]
    win['sfxs'] = [('tre', 'click'), ('lavora', 'click')]
    return [win, o(E('🖼️', 240, 1080, 170), at='vetrina', in_='pop'), o(E('⚙️', 840, 1080, 190), at='lavora', in_='spin')]

# ------------------------------------------------------------------ night skyline, zoom into the lit window
def skyline():
    rnd = random.Random(5)
    blds = ''
    xs = 0
    for i in range(9):
        w = rnd.randint(100, 150); h = rnd.randint(500, 1000)
        wins = ''.join(f'<i style="display:block;width:16px;height:22px;background:{"#FFD66B" if rnd.random() < .18 else "#1b2438"};box-shadow:{"0 0 10px #FFD66B" if rnd.random() < .1 else "none"}"></i>' for _ in range((w // 30) * (h // 48)))
        blds += f'<div style="position:absolute;left:{xs}px;bottom:0;width:{w}px;height:{h}px;background:#121a2c;border-top:3px solid #1f2a44;display:grid;grid-template-columns:repeat({w // 30},16px);gap:26px 14px;padding:20px 10px;align-content:start;justify-content:center">{wins}</div>'
        xs += w + 6
    target = '<div class="tw" style="position:absolute;left:575px;bottom:620px;width:60px;height:80px;background:#FFE08A;box-shadow:0 0 40px #FFD66B;border-radius:4px"></div>'
    city = HT(f'<div class="city" style="width:1200px;height:1300px;position:relative;transform-origin:605px 640px">{blds}{target}<div style="position:absolute;left:880px;top:40px;width:120px;height:120px;border-radius:50%;background:#F4EEE3;box-shadow:0 0 60px #F4EEE3"></div></div>', 540, 980, idle=False)
    city['in'] = 'fade'
    city['fx'] = [('paziente', 'tl.to("#ID .city",{scale:9,duration:1.4,ease:"power2.in"},@T-0.3);')]
    return [city]

# ------------------------------------------------------------------ irregular ECG trace
def ecg(y, at):
    pts, x = [], 0
    pattern = [0, 0, -10, 0, 0, 30, -170, 120, -20, 0, 0, -25, 0]
    seq = []
    for k in range(5):
        seq += pattern + [0] * (2 + (k % 3) * 3)
    for v in seq:
        pts.append(f'{x},{110 + v}'); x += 900 / len(seq)
    svg = f'<svg width="900" height="240" viewBox="0 0 900 240" style="filter:drop-shadow(0 0 8px #ff4d6d)"><polyline class="ek" points="{" ".join(pts)}" fill="none" stroke="#ff4d6d" stroke-width="6" stroke-linejoin="round" stroke-dasharray="3000" stroke-dashoffset="3000"/></svg>'
    it = HT(svg, 540, y, idle=False)
    it.update({'in': 'fade', 'at': at, 'fx': [(at, 'tl.to("#ID .ek",{strokeDashoffset:0,duration:2.6,ease:"none"},@T);')]})
    return it

def red_pulse(ats):
    it = HT('<div style="width:1300px;height:2300px;background:radial-gradient(circle,rgba(255,0,60,0) 45%,rgba(255,0,60,.38))"></div>', 540, 960, idle=False, depth=150)
    it.update({'in': 'none', 'style': 'opacity:0;'})
    it['fx'] = [(a, 'tl.to("#ID",{opacity:1,duration:0.08,yoyo:true,repeat:1},@T);') for a in ats]
    return it

# ------------------------------------------------------------------ phone with mobile site (fast load / sticky button)
MSITE = '''<div class="ms" style="position:absolute;left:0;right:0;top:0;font-family:Inter;text-align:left;white-space:normal">
<div style="background:#1E3A2F;color:#F4EEE3;padding:90px 30px 40px"><div style="font-size:18px;letter-spacing:.2em;opacity:.7">DOTT. M. BIANCHI</div><div class="serif" style="font-size:62px;line-height:.95;margin-top:16px;font-style:italic">Il tuo cuore,<br>in buone mani.</div></div>
''' + ''.join(f'<div style="margin:18px 22px;padding:22px;border-radius:22px;background:{c};font-weight:800;font-size:26px">{t}<div style="font-weight:400;font-size:19px;color:#666;margin-top:8px">Risposta del cardiologo →</div></div>' for t, c in [('Palpitazioni: quando preoccuparsi', '#F1ECF4'), ('Holter: come funziona', '#F8F3EA'), ('Pressione alta', '#E6EEE9'), ('ECG sotto sforzo', '#F1ECF4'), ('Colesterolo: i valori', '#F8F3EA'), ('Dopo un infarto', '#E6EEE9')]) + '</div>'

def fast_phone(x, y, at_load, at_scroll, sticky=False, scale=0.9):
    btn = '<div class="stk" style="position:absolute;left:22px;right:22px;bottom:26px;border-radius:999px;background:#39E75F;color:#0B1120;text-align:center;padding:24px;font:900 30px Inter;box-shadow:0 0 34px rgba(57,231,95,.8)">Prenota una visita</div>' if sticky else ''
    bar = '<div class="lb" style="position:absolute;left:0;top:64px;height:6px;width:100%;background:#39E75F;transform-origin:0 0;transform:scaleX(0);z-index:4"></div>'
    screen = f'<div style="position:absolute;inset:0;background:#fff;overflow:hidden">{bar}<div class="cv" style="position:absolute;inset:0;opacity:0">{MSITE}</div>{btn}</div>'
    ph = phone(screen, x, y, scale)
    ph['fx'] = [(at_load, 'tl.to("#ID .lb",{scaleX:1,duration:0.6,ease:"power2.out"},@T);tl.to("#ID .lb",{opacity:0,duration:0.2},@T+0.6);tl.to("#ID .cv",{opacity:1,duration:0.25},@T+0.55);'),
                (at_scroll, 'tl.to("#ID .ms",{y:-620,duration:2.2,ease:"power2.inOut"},@T);')]
    if sticky:
        ph['fx'].append((at_load, 'tl.to("#ID .stk",{scale:1.06,duration:0.45,yoyo:true,repeat:7,ease:"sine.inOut"},@T+0.8);'))
    return ph

# ------------------------------------------------------------------ the scenes (beat texts must stay identical: the voice is cached per text)
SITO2 = [
 dict(t="Questo è il sito di un cardiologo.", v=S(
        o(glow(540, 760, 860, 700), in_='fade', at=0, fx=[(0, 'tl.to("#ID",{opacity:.75,scale:1.05,duration:0.9,yoyo:true,repeat:5,ease:"sine.inOut"},@T+0.7);'), ('E', 'tl.to("#ID",{x:1200,duration:0.8,ease:"power3.inOut"},@T);')]),
        o(macbook(desk_new(), 540, 760, 680), in_='down', at=0, fx=[('E', 'tl.to("#ID",{x:1250,rotationY:35,duration:0.8,ease:"power3.inOut"},@T);')]),
        o(glow(540, 760, 860, 700, color='205,184,216'), in_='fade', beat=1, at=1),
        o(macbook(desk_old(), 540, 760, 680), in_='left', beat=1, at=0), capy=1400)),
 dict(t="E anche questo è il sito di un cardiologo."),
 dict(t="Stesso curriculum, / stessa città, / stesso prezzo della visita.", v=S(*board(), capy=1450)),
 dict(t="Ma uno riceve prenotazioni *anche di notte*,", v=S(*lockscreen([1, 'anche', 'notte']))),
 dict(t="l'altro ha un sito che nessuno apre.", v=S(*dead_dashboard()), p=0.1),
 dict(t="Il motivo sono *tre dettagli* / che fanno la differenza tra un sito vetrina / e un sito che lavora per te.", v=S(*tabs_toggle())),
 dict(t="Immagina un paziente.", v=S(*skyline(), nocap=False)),
 dict(t="Sono le undici di sera, / sente il cuore che batte strano.", v=S(
        o(time_picker(540, 420, 0.1), in_='zoom'),
        o(E('❤️', 540, 830, 230), at='cuore', idle=False, fx=[(0.0, 'tl.to("#ID",{keyframes:[{scale:1.3,duration:.07},{scale:1,duration:.1},{scale:1.18,duration:.07},{scale:1,duration:.3}]},@T);'),
                                                            (0.75, 'tl.to("#ID",{keyframes:[{scale:1.3,duration:.07},{scale:1,duration:.1},{scale:1.18,duration:.07},{scale:1,duration:.3}]},@T);'),
                                                            (1.2, 'tl.to("#ID",{keyframes:[{scale:1.3,duration:.07},{scale:1,duration:.1},{scale:1.18,duration:.07},{scale:1,duration:.3}]},@T);')],
          sfxs=[(0.0, 'heart'), (0.75, 'heart'), (1.2, 'heart')]),
        ecg(1100, 'cuore'), red_pulse(['cuore', 'batte', 'strano']))),
 dict(t="Prende il telefono / e scrive: «cardiologo Palermo».", v=S(
        o(phone('<div style="padding:150px 26px 0;background:#fff;position:absolute;inset:0"><div style="font-size:56px;font-weight:800;text-align:center;margin-bottom:34px"><span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span></div><div style="border:3px solid #ddd;border-radius:999px;padding:22px 26px;font-size:33px;font-weight:600;color:#111;min-height:92px;text-align:left;white-space:nowrap">🔍 {{TYPE:cardiologo Palermo}}</div></div>', 540, 760, 0.95), in_='up', type_at='scrive', rate=0.12),
        o(E('🫵', 820, 1150, 150), in_='pop', at='scrive')), p=0.9),
 dict(t="*Primo dettaglio:* il pollice.", v=S(*hud(1, 'il pollice', '👍')), p=0.25),
 dict(t="Quel paziente non è al computer. / È sul divano, / col telefono in mano.", v=S(
        o(E('💻', 540, 560, 260), in_='pop', out='divano'), o(T('✕', 540, 560, 320, c='red'), at='computer', out='divano'),
        darkness('divano'), spotlight(540, 'divano'), *worried_guy(540, 860, 'divano'), bg='#1a2133', dark_from=None)),
 dict(t="Il sito del primo si apre in un attimo / e si legge con un dito.", v=S(
        fast_phone(540, 790, 'apre', 'dito'), o(tag('⚡ 0,8 secondi', 830, 330, size=50), at='attimo'), o(E('👆', 760, 1050, 160), at='dito', in_='up', fx=[('dito', 'tl.to("#ID",{y:-260,duration:0.9,yoyo:true,repeat:1,ease:"sine.inOut"},@T+0.3);')]))),
 dict(t="Quello del secondo è stato fatto nel 2014: / testo minuscolo, / foto che non caricano, / un menu che non si apre.", v=S(
        o(phone('<div style="position:absolute;inset:0;background:#c9c9c9;overflow:hidden"><div style="position:absolute;left:0;top:70px;transform-origin:0 0;transform:scale(.38)">' + desk_old() + '</div></div>', 540, 780, 0.95), in_='up'),
        o(chip('2014', 830, 300, bg='#6b6b6b', size=56), at='2014'),
        o(E('🔍', 400, 560, 200), at='testo', in_='pop', fx=[('testo', 'tl.to("#ID",{x:180,y:40,duration:1,ease:"sine.inOut",yoyo:true,repeat:1},@T+0.3);')]),
        o(tag('testo minuscolo', 300, 430, bg='#FFD2D6', c='#9a0f1c'), at='testo'), o(tag('foto ✕', 800, 720, bg='#FFD2D6', c='#9a0f1c'), at='foto', shake=0.2),
        o(tag('menu ✕', 300, 1000, bg='#FFD2D6', c='#9a0f1c'), at='menu', shake=0.2))),
 dict(t="Secondo Google, / se una pagina da mobile ci mette più di tre secondi, / più della metà delle persone *se ne va*.", v=S(
        *google_scroll(540, 790, 0, 'pagina'),
        o(HT('<div style="width:660px;height:300px;border-radius:40px;background:rgba(11,17,32,.92);border:2px solid #D7192B;box-shadow:0 0 50px rgba(215,25,43,.5)"></div>', 540, 1120), at='metà'),
        counter(53, 540, 1080, 150, suf='%', c='#ff4d6d', at='metà', dur=0.8), o(T('se ne va', 540, 1185, 44, c='#fff'), at='va'),
        o(E('🏃', 900, 1180, 150), at='va', in_='walkr'))),
 dict(t="Il paziente torna indietro. / E clicca sul prossimo.", v=S(
        o(phone('''<div style="position:absolute;inset:0;background:#fff;font-family:Inter;text-align:left;white-space:normal;padding:90px 0 0">''' + ''.join(f'<div class="r{i}" style="padding:24px 26px;border-bottom:1px solid #eee"><div style="font-size:19px;color:#3c8a46">{u}</div><div style="font-size:28px;color:#1a0dab;font-weight:700">{t}</div><div style="font-size:21px;color:#E8901C">{s}</div></div>' for i, (u, t, s) in enumerate([('dottneri.it', 'Dott. Neri – Cardiologia', '★★★☆☆ 3 recensioni'), ('dottbianchi.it', 'Dott. M. Bianchi – Cardiologo', '★★★★★ 4,9 · 212'), ('centrocuore.it', 'Centro Cuore', '★★★★☆ 4,2')])) + '</div>', 540, 780, 0.95), in_='up',
          fx=[('indietro', 'tl.fromTo("#ID .r0",{opacity:1},{opacity:.25,duration:0.3},@T);'), ('prossimo', 'tl.to("#ID .r1",{backgroundColor:"#E6F9EA",scale:1.04,duration:0.25},@T);')]),
        o(HT('<div style="width:140px;height:140px;border-radius:50%;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.3);color:#fff;font:900 80px Inter;display:flex;align-items:center;justify-content:center">←</div>', 200, 330), at='indietro', in_='left'),
        o(E('👆', 780, 640, 150), at='clicca', in_='up', sfxs=[('prossimo', 'click')]))),
 dict(t="*Secondo dettaglio:* prenota in due tocchi.", v=S(*hud(2, 'due tocchi', '✌️')), p=0.25),
 dict(t="Sul sito del primo c'è un solo bottone, / grande, / sempre visibile: «Prenota una visita».", v=S(
        fast_phone(540, 790, 0, 'sempre', sticky=True), o(chip('sempre visibile', 540, 280, bg='#5B3A66'), at='visibile'))),
 dict(t="Due tocchi / e l'appuntamento è fissato.", v=S(*booking(540, 840, 0, 'tocchi', "l'appuntamento", 'fissato', 0.9))),
 dict(t="Sul sito del secondo c'è scritto: / «telefonare dal lunedì al venerdì, / dalle nove alle dodici».", v=S(
        o(HT('<div style="width:820px;background:#f3f0e6;border:3px solid #bbb;padding:36px;font-family:Times New Roman,serif;font-size:44px;text-align:center;white-space:normal;color:#222">Per appuntamenti telefonare<br>dal <b>lunedì</b> al <b>venerdì</b><br>dalle <b>9:00</b> alle <b>12:00</b></div>', 540, 420), in_='down'),
        o(phone('<div class="cl" style="position:absolute;inset:0;background:linear-gradient(180deg,#2c3e50,#0b1120);color:#fff;font-family:Inter;text-align:center;padding-top:200px"><div style="font-size:30px;opacity:.7">Studio Dott. Neri</div><div class="st" style="font-size:44px;font-weight:800;margin-top:14px">Chiamata…</div><div style="margin:120px auto 0;width:130px;height:130px;border-radius:50%;background:#D7192B;font-size:60px;display:flex;align-items:center;justify-content:center">📞</div></div>', 540, 1000, 0.62), in_='up', at='telefonare',
          fx=[('dodici', 'tl.to("#ID .st",{color:"#ff4d6d",duration:0.2},@T);tl.set("#ID .st",{textContent:"Nessuna risposta"},@T);tl.to("#ID",{x:10,duration:0.05,yoyo:true,repeat:5},@T);')], sfxs=[('telefonare', 'ding'), ('dodici', 'stamp')]))),
 dict(t="Alle undici di sera, / il paziente sceglie chi gli permette di prenotare *adesso*.", v=S(
        o(chip('🌙 23:00', 540, 300, bg='#2b2f45', size=44), at=0),
        *booking(540, 840, 'paziente', 'sceglie', 'prenotare', 'adesso', 0.9))),
 dict(t="*Terzo dettaglio,* / il più sottovalutato: / parlare la lingua di Google.", v=S(*hud(3, 'la lingua di Google', '🔍')), p=0.25),
 dict(t="Il primo ha una pagina per ogni domanda che i pazienti si fanno davvero: / «Palpitazioni: quando preoccuparsi». / «Holter: come funziona».", v=S(
        o(HT(f'<div style="width:900px;border-radius:999px;background:#fff;padding:26px 36px;font:600 34px Inter;color:#111;text-align:left;white-space:nowrap">🔍 {{{{TYPE:palpitazioni quando preoccuparsi}}}}</div>', 540, 330), in_='down', type_at='domanda', rate=0.06),
        o(HT(f'<div style="width:820px;border-radius:28px;background:#fff;padding:30px 36px;text-align:left;white-space:normal;border-left:14px solid {NEON}"><div style="font:600 22px Inter;color:#2a7f3f">dottbianchi.it › palpitazioni</div><div style="font:800 40px Inter;color:#1a0dab;margin-top:6px">Palpitazioni: quando preoccuparsi</div></div>', 540, 640), in_='left', at='Palpitazioni'),
        o(HT(f'<div style="width:820px;border-radius:28px;background:#fff;padding:30px 36px;text-align:left;white-space:normal;border-left:14px solid {LIL}"><div style="font:600 22px Inter;color:#2a7f3f">dottbianchi.it › holter</div><div style="font:800 40px Inter;color:#1a0dab;margin-top:6px">Holter: come funziona</div></div>', 540, 900), in_='right', at='Holter'),
        o(tag('1ª posizione', 820, 520, size=40), at='preoccuparsi'))),
 dict(t="E una scheda Google con foto, / orari aggiornati / e *recensioni* a cui risponde.", v=S(
        o(HT('''<div style="width:900px;border-radius:34px;background:#fff;overflow:hidden;font-family:Inter;text-align:left;white-space:normal">
<div class="ph" style="display:flex;gap:8px;height:220px;opacity:0"><div style="flex:2;background:linear-gradient(135deg,#1E3A2F,#7FA992)"></div><div style="flex:1;background:linear-gradient(135deg,#CDB8D8,#5B3A66)"></div><div style="flex:1;background:linear-gradient(135deg,#F8F3EA,#B39874)"></div></div>
<div style="padding:28px 34px"><div style="font-size:40px;font-weight:800">Dott. M. Bianchi – Cardiologo</div>
<div style="font-size:30px;margin-top:8px"><span class="st" style="color:#ddd">★★★★★</span> <b class="rv">0,0</b> <span style="color:#777">· 212 recensioni</span></div>
<div class="op" style="font-size:28px;margin-top:12px;opacity:0"><b style="color:#1E9E52">Aperto</b> · Chiude alle 19:30</div>
<div class="rp" style="margin-top:18px;padding:18px 22px;border-radius:18px;background:#F1ECF4;font-size:24px;opacity:0"><b>Risposta del titolare:</b> Grazie per la fiducia, a presto!</div></div></div>''', 540, 760), in_='up',
          fx=[('foto', 'tl.fromTo("#ID .ph",{opacity:0,y:-30},{opacity:1,y:0,duration:0.4,immediateRender:false},@T);'),
              ('orari', 'tl.to("#ID .op",{opacity:1,duration:0.3},@T);'),
              ('recensioni', 'tl.to("#ID .st",{color:"#E8901C",duration:0.6},@T);(function(){var o={v:0},n=document.querySelector("#ID .rv");tl.to(o,{v:4.9,duration:0.8,onUpdate:function(){n.textContent=o.v.toFixed(1).replace(".",",");}},@T);tl.set(o,{v:0},0);})();'),
              ('risponde', 'tl.fromTo("#ID .rp",{opacity:0,y:20},{opacity:1,y:0,duration:0.35,immediateRender:false},@T);')],
          sfxs=[('foto', 'click'), ('orari', 'click'), ('recensioni', 'sparkle'), ('risponde', 'ding')]))),
 dict(t="Il secondo ha una pagina sola: / «Chi sono». / Con l'elenco dei congressi del 2009.", v=S(
        o(HT('<div style="width:800px;height:720px;overflow:hidden;background:#fff;border:3px solid #bbb;font-family:Times New Roman,serif;font-size:36px;text-align:left;white-space:normal;color:#222;position:relative"><div class="ls" style="padding:40px"><div style="font-size:60px;font-weight:bold;margin-bottom:20px;color:#003399">Chi sono</div>Congressi:<br>' + '<br>'.join(f'• {c}, {y}' for c, y in [('Roma', 2006), ('Milano', 2007), ('Napoli', 2009), ('Bologna', 2009), ('Torino', 2009), ('Bari', 2009), ('Firenze', 2009), ('Genova', 2009), ('Verona', 2009)]) + '</div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,0) 60%,#fff)"></div></div>', 540, 760), in_='up',
          fx=[('elenco', 'tl.to("#ID .ls",{y:-260,duration:2,ease:"none"},@T);')]),
        o(chip('2009', 840, 330, bg='#6b6b6b', size=56), at='2009'), o(E('🕸️', 230, 1130, 170), at='congressi', in_='fade'))),
 dict(t="Google non può consigliare / quello che non riesce a capire.", v=S(
        o(HT('<div style="width:760px;height:760px;background:#fff;border-radius:20px;position:relative;overflow:hidden;font-family:Times New Roman,serif;font-size:30px;padding:40px;text-align:left;white-space:normal;color:#444">Benvenuti nel sito del Dott. Neri. Il Dott. Neri si è laureato nel 1998 con il massimo dei voti. Congressi: Roma 2006, Milano 2007, Napoli 2009, Bologna 2009… Per appuntamenti telefonare… Clicca qui… Visitatori: 000418…<div class="scan" style="position:absolute;left:0;right:0;top:0;height:14px;background:#39E75F;box-shadow:0 0 40px 10px rgba(57,231,95,.7)"></div></div>', 540, 760), in_='zoom',
          fx=[(0.2, 'tl.fromTo("#ID .scan",{y:0},{y:740,duration:1.2,yoyo:true,repeat:1,ease:"sine.inOut"},@T);')]),
        o(E('🤖', 850, 380, 220), in_='walkr', at=0), *[o(T('?', 300 + 180 * i, 1080 + (i % 2) * 60, 140, c='#ff4d6d', font='serif', i=True), at='capire', in_='pop', dt=0) for i in range(3)])),
 dict(t="E guarda il risultato.", v=dict(items=[], capy=900, bg=NIGHT, dark=True), p=0.1),
 dict(t="Il primo dorme / e il suo sito continua a riempirgli l'agenda.", v=S(
        o(E('😴', 870, 300, 170), in_='pop', fx=[(0.3, 'tl.to("#ID",{y:-14,duration:1.1,yoyo:true,repeat:3,ease:"sine.inOut"},@T);')]),
        *lockscreen(['sito', 'riempirgli', 'agenda'])[:1])),
 dict(t="Il secondo paga un sito / che fa da *biglietto da visita* / in un cassetto.", v=S(
        o(E('🗄️', 540, 880, 420), in_='up'),
        o(HT('<div style="width:440px;height:250px;background:#fff;border-radius:10px;box-shadow:0 20px 40px rgba(0,0,0,.4);font-family:Times New Roman,serif;display:flex;flex-direction:column;justify-content:center;align-items:center;font-size:36px;color:#222">Dott. Neri<br><span style="font-size:24px;color:#666">www.dottneri.it</span></div>', 540, 420), at='biglietto', in_='pop',
          fx=[('cassetto', 'tl.to("#ID",{y:460,scale:0.4,opacity:0,duration:0.6,ease:"power2.in"},@T);')]),
        o(E('🔒', 760, 760, 150), at='cassetto', in_='stamp', dt=0))),
 dict(t="Noi di Insula costruiamo siti per medici / pensati per il telefono, / per la prenotazione / e per Google.", v=S(
        *confetti(0.2, n=110), o(dict(k='img', src='assets/img/insula-logo.webp', x=540, y=230, w=170, h=170, r=85), in_='spin'),
        o(macbook(desk_new(long=True), 540, 650, 880, scroll=(0.6, 1300)), in_='zoom', at=0),
        o(chip('📱 telefono', 220, 1110, bg='#1E3A2F', size=38), at='telefono'), o(chip('📅 prenotazione', 540, 1110, bg='#5B3A66', size=38), at='prenotazione'), o(chip('🔍 Google', 870, 1110, bg='#B39874', size=38), at='Google'))),
 dict(t="Testi scritti da chi conosce la comunicazione sanitaria, / non da chi vende siti a tutti.", v=S(
        o(HT(f'<div style="width:900px;border-radius:30px;{GLASS}padding:40px;font:500 38px Inter;color:#fff;text-align:left;white-space:normal;min-height:420px"><div style="font:800 22px Inter;color:{NEON};letter-spacing:.2em;margin-bottom:20px">EDITOR · TESTI SANITARI</div>{{{{TYPE:Le palpitazioni sono spesso innocue, ma tre segnali richiedono una visita entro 48 ore.}}}}</div>', 540, 700), in_='up', type_at='Testi', rate=0.035),
        o(tag('✓ comunicazione sanitaria', 540, 1040, size=48), at='comunicazione'), o(T('siti per tutti', 540, 1170, 56, c='#8a93a6'), at='vende', strike='tutti'))),
 dict(t="Se vuoi sapere cosa cambierei nel tuo sito, / commentami *SITO* / e ti scrivo in privato.", v=S(
        o(cta('SITO', 540, 760), in_='up'),
        o(HT('<div class="bubble me">Ciao! Ti scrivo in privato 👋</div>'), y=1040, at='scrivo'))),
]

TRANS = [('{x:1080,opacity:1,rotationY:-20}', '{x:-1080,opacity:1,rotationY:20}'),
         ('{scale:1.7,opacity:0}', '{scale:0.55,opacity:0}'),
         ('{y:1920,opacity:1}', '{y:-1920,opacity:1}'),
         ('{x:-1080,opacity:1,rotationY:20}', '{x:1080,opacity:1,rotationY:-20}')]

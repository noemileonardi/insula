"""Bespoke visual components for the 'Sito' reel (MacBook 3D, desktop sites, glowing arrows,
time-picker drums, spotlight, Google scroll + timer, booking flow, confetti)."""
import random
from widgets import HT, E, chip, tag, T

def _o(it, **kw):
    if 'in_' in kw: kw['in'] = kw.pop('in_')
    d = dict(it); d.update(kw); return d

# ---------------------------------------------------------------------------------- desktop sites (1280x800 canvas)
def desk_new(long=False):
    extra = ''
    if long:
        extra = '''
<div style="padding:70px 90px;background:#F8F3EA"><div class="serif" style="font-size:64px;font-style:italic;color:#1E3A2F">Le domande dei pazienti</div>
<div style="display:flex;gap:28px;margin-top:34px">''' + ''.join(f'<div style="flex:1;background:#fff;border-radius:26px;padding:30px;font-size:28px;font-weight:700;box-shadow:0 10px 30px rgba(0,0,0,.06)">{q}<div style="font-weight:400;color:#777;font-size:22px;margin-top:12px">Leggi la risposta del cardiologo →</div></div>' for q in ['Palpitazioni: quando preoccuparsi?', 'Holter: come funziona?', 'Pressione alta: i primi segnali']) + '''</div></div>
<div style="padding:70px 90px;background:#fff"><div class="serif" style="font-size:64px;font-style:italic;color:#1E3A2F">Dicono di noi</div>
<div style="display:flex;gap:28px;margin-top:34px">''' + ''.join(f'<div style="flex:1;background:#F1ECF4;border-radius:26px;padding:30px;font-size:24px"><div style="color:#E8901C;font-size:30px">★★★★★</div>“{r}”<div style="margin-top:12px;font-weight:700">{n}</div></div>' for r, n in [('Spiega tutto con una chiarezza rara.', 'Giulia R.'), ('Ho prenotato alle 23 dal telefono.', 'Marco T.'), ('Puntuale, gentile, preparato.', 'Anna L.')]) + '''</div></div>
<div style="padding:70px 90px;background:#1E3A2F;color:#F4EEE3;display:flex;justify-content:space-between;align-items:center"><div class="serif" style="font-size:60px;font-style:italic">Prenota in due tocchi</div><div style="background:#F4EEE3;color:#1E3A2F;border-radius:999px;padding:24px 50px;font-size:30px;font-weight:800">Prenota una visita</div></div>'''
    return f'''<div class="dsite" style="width:1280px;font-family:Inter;color:#111;background:#fff;text-align:left;white-space:normal">
<div style="display:flex;align-items:center;justify-content:space-between;padding:26px 60px;border-bottom:1px solid #eee"><div style="font-weight:800;font-size:28px;color:#1E3A2F">Dott. M. Bianchi <span style="font-weight:500;color:#888">· Cardiologo</span></div>
<div style="display:flex;gap:34px;font-size:22px;color:#555;align-items:center"><span>Visite</span><span>Esami</span><span>Domande</span><span>Contatti</span><span style="background:#1E3A2F;color:#F4EEE3;border-radius:999px;padding:12px 26px;font-weight:700">Prenota</span></div></div>
<div style="display:flex;gap:50px;padding:60px 60px 50px;align-items:center;background:linear-gradient(120deg,#fff 50%,#F1ECF4)">
<div style="flex:1.1"><div style="font-size:20px;letter-spacing:.2em;color:#5B3A66;font-weight:700">CARDIOLOGIA A PALERMO</div>
<div class="serif" style="font-size:86px;line-height:.95;font-style:italic;color:#1E3A2F;margin-top:16px">Il tuo cuore,<br>in buone mani.</div>
<div style="font-size:26px;color:#555;margin-top:22px">Visite, ECG e Holter in centro città.<br>Prenota online, anche di notte.</div>
<div style="display:flex;gap:18px;margin-top:30px"><div style="background:#1E3A2F;color:#F4EEE3;border-radius:999px;padding:22px 44px;font-size:26px;font-weight:800">Prenota una visita</div><div style="border:2px solid #1E3A2F;color:#1E3A2F;border-radius:999px;padding:20px 36px;font-size:24px;font-weight:700">Chiama</div></div>
<div style="margin-top:24px;font-size:22px;color:#E8901C">★★★★★ <span style="color:#666">4,9 · 212 recensioni Google</span></div></div>
<div style="flex:.9;height:380px;border-radius:34px;background:linear-gradient(160deg,#CDB8D8,#1E3A2F);display:flex;align-items:center;justify-content:center;font-size:190px">❤️</div></div>{extra}</div>'''

def desk_old():
    return '''<div style="width:1280px;height:800px;background:#c9c9c9;font-family:'Times New Roman',serif;color:#222;text-align:left;white-space:normal">
<div style="background:#003399;color:#ffff00;font-size:44px;font-weight:bold;text-align:center;padding:22px">*** Benvenuti nel sito del Dott. Neri ***</div>
<div style="background:#e6e6e6;padding:10px 20px;font-size:22px;color:#0000ee;text-decoration:underline">Home &nbsp;|&nbsp; Chi sono &nbsp;|&nbsp; Curriculum &nbsp;|&nbsp; Congressi &nbsp;|&nbsp; Contatti</div>
<div style="display:flex;gap:30px;padding:26px">
<div style="width:330px;height:300px;border:2px solid #999;display:flex;align-items:center;justify-content:center;color:#999;font-size:22px;background:#ddd">✖ immagine non disponibile</div>
<div style="flex:1;font-size:21px;line-height:1.35">Il Dott. Neri si è laureato presso l'Università degli Studi nel 1998 con il massimo dei voti. Ha partecipato ai seguenti congressi: Roma 2006, Milano 2007, Napoli 2009, Bologna 2009...<br><br>
<b>Per appuntamenti telefonare dal lunedì al venerdì dalle 9:00 alle 12:00.</b><br><br><span style="color:#00e;text-decoration:underline">Clicca qui</span> per scaricare il curriculum (PDF 12 MB)<br><br>
<span style="background:#000;color:#0f0;font-family:monospace;padding:4px 10px">Visitatori: 000418</span><br><br><span style="font-size:17px">Ultimo aggiornamento: 03/2014 · Ottimizzato per Internet Explorer 6</span></div></div></div>'''

# ---------------------------------------------------------------------------------- MacBook (CSS 3D, aluminium)
def macbook(screen_html, x, y, w=820, scroll=None, **k):
    """screen_html is a 1280px-wide page; it is scaled into the display. scroll=(start_at, px) scrolls it."""
    sw = w - 36; sh = int(sw * 0.625); sc = sw / 1280
    html = f'''<div style="width:{w * 1.14:.0f}px;display:flex;flex-direction:column;align-items:center;filter:drop-shadow(0 60px 50px rgba(0,0,0,.28))">
<div style="width:{w}px;height:{sh + 36}px;border-radius:30px 30px 10px 10px;background:linear-gradient(180deg,#2a2b2f,#0d0d10);padding:18px 18px 18px;position:relative;box-shadow:inset 0 0 0 2px #45464b">
<div style="position:absolute;left:50%;top:0;width:{w * .16:.0f}px;height:22px;margin-left:-{w * .08:.0f}px;background:#0d0d10;border-radius:0 0 12px 12px;z-index:3"></div>
<div style="width:{sw}px;height:{sh}px;border-radius:12px;overflow:hidden;background:#fff;position:relative">
<div class="scr" style="position:absolute;left:0;top:0;width:1280px;transform-origin:0 0;transform:scale({sc:.4f})">{screen_html}</div>
<div style="position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.18) 0%,rgba(255,255,255,0) 38%);pointer-events:none"></div></div></div>
<div style="width:{w * 1.14:.0f}px;height:{w * .035:.0f}px;margin-top:-2px;border-radius:2px 2px {w * .03:.0f}px {w * .03:.0f}px;background:linear-gradient(180deg,#e9eaee 0%,#c4c6cc 55%,#8d9096 100%);position:relative">
<div style="position:absolute;left:50%;top:0;width:{w * .2:.0f}px;height:{w * .012:.0f}px;margin-left:-{w * .1:.0f}px;border-radius:0 0 10px 10px;background:linear-gradient(180deg,#a7a9af,#c9cbd0)"></div></div></div>'''
    it = HT(html, x, y, **k)
    if scroll:
        at, px = scroll
        it.setdefault('fx', []).append((at, f'tl.fromTo("#ID .scr",{{y:0}},{{y:-{px * sc:.0f},duration:Math.max(1,@END-@T-0.4),ease:"power1.inOut"}},@T);'))
    return it

def glow(x, y, w=900, h=700, color='57,231,95', **k):
    it = HT(f'<div style="width:{w}px;height:{h}px;border-radius:50%;background:radial-gradient(closest-side,rgba({color},.75),rgba({color},.25) 55%,rgba({color},0));filter:blur(30px)"></div>', x, y, idle=False, **k)
    it.setdefault('fx', []).append(('@', ''))
    it['fx'] = [(0, 'tl.to("#ID",{opacity:.75,scale:1.05,duration:0.9,yoyo:true,repeat:5,ease:"sine.inOut"},@T+0.7);')]
    return it

# ---------------------------------------------------------------------------------- glowing arrow between two points
def arrow(x1, y1, x2, y2, at, bend=120, color='#39E75F'):
    minx, miny = min(x1, x2) - 160, min(y1, y2) - 40
    w, h = abs(x2 - x1) + 320, abs(y2 - y1) + 80
    ax1, ay1, ax2, ay2 = x1 - minx, y1 - miny, x2 - minx, y2 - miny
    cx, cy = (ax1 + ax2) / 2 + bend, (ay1 + ay2) / 2
    html = f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible;filter:drop-shadow(0 0 6px {color}) drop-shadow(0 0 14px {color})">
<path class="ap" d="M{ax1},{ay1} Q{cx},{cy} {ax2},{ay2}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="1000"/>
<circle class="ad" r="11" fill="#fff" cx="{ax1}" cy="{ay1}" opacity="0"/>
<path class="ah" d="M{ax2 - 18},{ay2 - 22} L{ax2},{ay2} L{ax2 + 20},{ay2 - 18}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg>'''
    it = HT(html, minx + w / 2, miny + h / 2, idle=False)
    it['in'] = 'none'
    it['fx'] = [(at, 'tl.to("#ID .ap",{strokeDashoffset:0,duration:0.55,ease:"power2.inOut"},@T);'
                     f'tl.fromTo("#ID .ad",{{opacity:1,attr:{{cx:{ax1},cy:{ay1}}}}},{{keyframes:[{{attr:{{cx:{cx - bend / 2:.0f},cy:{cy:.0f}}},duration:0.27}},{{attr:{{cx:{ax2},cy:{ay2}}},duration:0.28}}],ease:"none"}},@T);'
                     'tl.to("#ID .ad",{opacity:0,duration:0.2},@T+0.55);tl.to("#ID .ah",{opacity:1,duration:0.15},@T+0.45);')]
    it['sfxs'] = [(at, 'swipe')]
    return it

# ---------------------------------------------------------------------------------- macOS-style time picker drums
def time_picker(x, y, at, h_from=17, h_to=23, m_from=41, m_to=0):
    row = 92
    hours = [(h_from + i) % 24 for i in range(-2, (h_to - h_from) + 3)]
    mins = [(m_from + i * 4) % 60 for i in range(-2, 17)] ; mins = mins[:16] + [58, 59, 0, 1, 2]
    def col(vals, cls):
        return f'<div class="{cls}" style="position:absolute;left:0;right:0;top:0">' + ''.join(f'<div style="height:{row}px;line-height:{row}px">{v:02d}</div>' for v in vals) + '</div>'
    hs_from, hs_to = 2 * row - 2 * row, -(len(hours) - 5) * row
    m_idx_to = len(mins) - 3
    html = f'''<div style="width:600px;height:{row * 5}px;border-radius:40px;background:rgba(30,32,40,.72);backdrop-filter:blur(30px);box-shadow:0 30px 80px rgba(0,0,0,.45),inset 0 0 0 1.5px rgba(255,255,255,.12);position:relative;overflow:hidden;font-family:Inter;font-weight:700;font-size:72px;color:#fff;text-align:center">
<div style="position:absolute;left:24px;right:24px;top:{row * 2}px;height:{row}px;border-radius:22px;background:rgba(255,255,255,.12)"></div>
<div style="position:absolute;left:60px;width:200px;top:0;bottom:0;overflow:hidden">{col(hours, 'hh')}</div>
<div style="position:absolute;left:270px;width:60px;top:{row * 2}px;line-height:{row}px">:</div>
<div style="position:absolute;left:340px;width:200px;top:0;bottom:0;overflow:hidden">{col(mins, 'mm')}</div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,32,40,.95),rgba(30,32,40,0) 34%,rgba(30,32,40,0) 66%,rgba(30,32,40,.95));pointer-events:none"></div></div>'''
    it = HT(html, x, y)
    it['fx'] = [(at, f'tl.fromTo("#ID .hh",{{y:0}},{{y:{-(len(hours) - 5) * row},duration:1.6,ease:"power3.inOut"}},@T);'
                     f'tl.fromTo("#ID .mm",{{y:0}},{{y:{-(m_idx_to - 2) * row},duration:1.9,ease:"power3.inOut"}},@T);')]
    it['sfxs'] = [(at, 'riser')] + [(f'{float(i) * 0.12}', 'key') for i in range(0)]
    return it

# ---------------------------------------------------------------------------------- spotlight scene (dark + beam)
def darkness(at):
    it = HT('<div style="width:1400px;height:2400px;background:#07080d"></div>', 540, 960, idle=False, depth=-50)
    it['in'] = 'none'; it['style'] = 'opacity:0;'
    it['fx'] = [(at, 'tl.to("#ID",{opacity:1,duration:0.35,ease:"power2.out"},@T-0.1);')]
    return it

def spotlight(x, at):
    html = '''<div style="width:900px;height:1500px;position:relative">
<div style="position:absolute;left:50%;top:0;width:900px;height:1400px;margin-left:-450px;background:linear-gradient(180deg,rgba(255,246,214,.55),rgba(255,246,214,.12) 70%,rgba(255,246,214,0));clip-path:polygon(43% 0,57% 0,100% 100%,0 100%);filter:blur(16px)"></div>
<div style="position:absolute;left:50%;bottom:40px;width:820px;height:200px;margin-left:-410px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,246,214,.55),rgba(255,246,214,0))"></div>
<div style="position:absolute;left:50%;top:-30px;width:180px;height:60px;margin-left:-90px;border-radius:0 0 90px 90px;background:linear-gradient(180deg,#2b2b30,#55555d)"></div></div>'''
    it = HT(html, x, 760, idle=False, depth=-40)
    it['in'] = 'none'; it['style'] = 'opacity:0;'
    it['fx'] = [(at, 'tl.to("#ID",{keyframes:[{opacity:.9,duration:.06},{opacity:.1,duration:.07},{opacity:1,duration:.08},{opacity:.35,duration:.06},{opacity:1,duration:.12}]},@T+0.15);')]
    it['sfxs'] = [(at, 'stamp')]
    return it

def worried_guy(x, y, at):
    """3D character drops onto the sofa (squash & settle), then scrolls his phone."""
    feed = ''.join(f'<div style="height:150px;margin:10px;border-radius:14px;background:{c}"></div>' for c in ['#CDB8D8', '#1E3A2F', '#F1ECF4', '#B39874', '#5B3A66', '#7FA992'] * 3)
    phone = f'''<div style="width:150px;height:290px;border-radius:26px;background:#111;padding:7px;box-shadow:0 0 40px rgba(130,170,255,.55)"><div style="width:100%;height:100%;border-radius:20px;overflow:hidden;background:#fff;position:relative"><div class="feed" style="position:absolute;left:0;right:0;top:0">{feed}</div></div></div>'''
    items = [
        _o(E('🛋️', x, y + 120, 520), in_='up', at=at, depth=0),
        _o(E('🙍', x, y - 40, 300), in_='none', at=at, depth=40, idle=False,
           fx=[(at, 'tl.fromTo("#ID",{y:-700,opacity:0,scaleY:1,scaleX:1},{immediateRender:false,keyframes:[{opacity:1,duration:0.01},{y:0,duration:0.45,ease:"power2.in"},{scaleY:0.86,scaleX:1.08,duration:0.1},{scaleY:1,scaleX:1,duration:0.25,ease:"back.out(3)"}]},@T+0.15);'
                     'tl.to("#ID",{rotation:-3,duration:1.2,yoyo:true,repeat:3,ease:"sine.inOut"},@T+1.0);')],
           sfxs=[(0.6, 'step')], style='opacity:0;'),
        _o(HT(phone, x + 150, y + 40), in_='pop', at=at, depth=80, idle=False,
           fx=[('telefono', 'tl.fromTo("#ID .feed",{y:0},{y:-1500,duration:6,ease:"none"},@T);')]),
    ]
    items[2]['at'] = 'telefono'
    return items

# ---------------------------------------------------------------------------------- Google results scrolling + timer
def google_scroll(x, y, start_at, timer_at, scale=0.86):
    rows = ''.join(f'''<div style="padding:22px 26px;border-bottom:1px solid #eee"><div style="font-size:18px;color:#3c8a46">{u}</div><div style="font-size:26px;color:#1a0dab;font-weight:600;margin:4px 0">{t}</div><div style="font-size:19px;color:#555">{d}</div></div>'''
                   for u, t, d in [('cardiologiapalermo.it', 'Cardiologo a Palermo – Visite ed ECG', 'Prenota online la tua visita cardiologica...'),
                                   ('miodottore.it', 'I migliori cardiologi a Palermo', '212 recensioni · prenota subito'),
                                   ('dottneri.it', 'Benvenuti nel sito del Dott. Neri', 'Il Dott. Neri si è laureato nel 1998...'),
                                   ('centrocuore.it', 'Centro Cuore Palermo', 'Holter, ecocardiogramma, test da sforzo'),
                                   ('dottbianchi.it', 'Palpitazioni: quando preoccuparsi', 'La risposta del cardiologo in 2 minuti'),
                                   ('paginegialle.it', 'Cardiologi Palermo – PagineGialle', 'Indirizzi e numeri di telefono'),
                                   ('ospedale.it', 'Ambulatorio di cardiologia', 'Orari e modalità di accesso')] * 2)
    screen = f'''<div style="position:absolute;inset:0;background:#fff;font-family:Inter;text-align:left;white-space:normal">
<div style="padding:70px 22px 16px;border-bottom:1px solid #eee;background:#fff;position:relative;z-index:2"><div style="font-size:40px;font-weight:800;text-align:center;margin-bottom:14px"><span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span></div>
<div style="border:2px solid #ddd;border-radius:999px;padding:14px 22px;font-size:26px">🔍 cardiologo Palermo</div></div>
<div class="res" style="position:absolute;left:0;right:0;top:190px">{rows}</div></div>'''
    from widgets import phone
    ph = phone(screen, x, y, scale)
    ph['fx'] = [(start_at, 'tl.fromTo("#ID .res",{y:0},{y:-1400,duration:Math.max(1.5,@END-@T-0.3),ease:"none"},@T);')]
    ring = '''<div style="width:250px;height:250px;position:relative;border-radius:50%;background:rgba(17,17,17,.86);box-shadow:0 20px 50px rgba(0,0,0,.35)">
<svg width="250" height="250" viewBox="0 0 250 250" style="position:absolute;inset:0;transform:rotate(-90deg)"><circle cx="125" cy="125" r="100" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="16"/>
<circle class="rg" cx="125" cy="125" r="100" fill="none" stroke="#D7192B" stroke-width="16" stroke-linecap="round" stroke-dasharray="628" stroke-dashoffset="628"/></svg>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-family:Inter;font-weight:800"><div><span class="tv" style="font-size:72px">0,0</span><span style="font-size:36px"> s</span></div><div style="font-size:20px;color:#bbb;font-weight:600">caricamento…</div></div></div>'''
    timer = HT(ring, 830, 370, depth=120)
    timer['at'] = timer_at
    timer['fx'] = [(timer_at, 'tl.to("#ID .rg",{strokeDashoffset:0,duration:2.4,ease:"none"},@T);'
                              '(function(){var o={v:0},n=document.querySelector("#ID .tv");tl.to(o,{v:3,duration:2.4,ease:"none",onUpdate:function(){n.textContent=o.v.toFixed(1).replace(".",",");}},@T);tl.set(o,{v:0},0);})();')]
    timer['sfxs'] = [(timer_at, 'riser')]
    return [ph, timer]

# ---------------------------------------------------------------------------------- booking flow on a phone
def booking(x, y, at_day, at_slot, at_btn, at_ok, scale=0.9):
    days = ''.join(f'<div class="dd{i}" style="flex:1;border-radius:18px;padding:12px 0;text-align:center;background:#F2F2F2;font-size:20px;font-weight:700">{d}<br><span style="font-size:30px">{n}</span></div>' for i, (d, n) in enumerate([('LUN', 24), ('MAR', 25), ('MER', 26), ('GIO', 27)]))
    slots = ''.join(f'<div class="sl{i}" style="border-radius:16px;padding:16px 0;text-align:center;border:2px solid #e3e3e3;font-size:24px;font-weight:700">{s}</div>' for i, s in enumerate(['8:30', '9:00', '9:30', '10:00', '11:30', '12:00', '15:30', '16:00', '17:30']))
    screen = f'''<div style="position:absolute;inset:0;background:#fff;font-family:Inter;text-align:left;white-space:normal;padding:80px 26px 0">
<div style="font-size:22px;color:#888">Dott. M. Bianchi · Cardiologo</div><div style="font-size:38px;font-weight:800;margin:6px 0 22px">Prenota una visita</div>
<div style="display:flex;gap:10px">{days}</div>
<div style="font-size:22px;color:#888;margin:26px 0 12px">Orari disponibili</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">{slots}</div>
<div class="bk" style="margin-top:28px;border-radius:999px;background:#1E3A2F;color:#F4EEE3;text-align:center;padding:22px;font-size:28px;font-weight:800">Prenota adesso</div>
<div class="ok" style="position:absolute;inset:0;background:rgba(255,255,255,.96);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0">
<div class="okc" style="width:170px;height:170px;border-radius:50%;background:#1E9E52;color:#fff;font-size:110px;display:flex;align-items:center;justify-content:center">✓</div>
<div style="font-size:36px;font-weight:800;margin-top:24px">Visita prenotata</div><div style="font-size:24px;color:#666">Martedì 25 · 9:30</div></div></div>'''
    from widgets import phone
    ph = phone(screen, x, y, scale)
    ph['fx'] = [(at_day, 'tl.to("#ID .dd1",{backgroundColor:"#1E3A2F",color:"#F4EEE3",scale:1.08,duration:0.25},@T);'),
                (at_slot, 'tl.to("#ID .sl2",{backgroundColor:"#39E75F",borderColor:"#39E75F",scale:1.1,duration:0.2,yoyo:true,repeat:1},@T);tl.to("#ID .sl2",{backgroundColor:"#39E75F",borderColor:"#39E75F",duration:0.01},@T+0.41);'),
                (at_btn, 'tl.to("#ID .bk",{scale:0.92,duration:0.1,yoyo:true,repeat:1},@T);'),
                (at_ok, 'tl.to("#ID .ok",{opacity:1,duration:0.25},@T);tl.fromTo("#ID .okc",{scale:0,rotation:-90},{scale:1,rotation:0,duration:0.5,ease:"back.out(2.5)"},@T+0.05);')]
    ph['sfxs'] = [(at_day, 'click'), (at_slot, 'click'), (at_btn, 'click'), (at_ok, 'sparkle')]
    finger = E('👆', x + 70, y + 160, 150)
    finger.update({'in': 'none', 'idle': False, 'style': 'opacity:0;', 'depth': 160})
    finger['fx'] = [(at_day, 'tl.set("#ID",{opacity:1},@T-0.35);tl.fromTo("#ID",{x:-160,y:-340},{x:-140,y:-300,duration:0.3},@T-0.3);'),
                    (at_slot, 'tl.to("#ID",{x:20,y:-60,duration:0.35,ease:"power2.inOut"},@T-0.35);'),
                    (at_btn, 'tl.to("#ID",{x:0,y:150,duration:0.35,ease:"power2.inOut"},@T-0.35);tl.to("#ID",{opacity:0,duration:0.2},@T+0.4);')]
    notif = HT('<div style="width:860px;background:rgba(255,255,255,.97);border-radius:34px;padding:24px 30px;display:flex;gap:22px;align-items:center;box-shadow:0 20px 50px rgba(0,0,0,.25);font-family:Inter;text-align:left;white-space:normal"><div style="width:80px;height:80px;border-radius:20px;background:#1E9E52;color:#fff;font-size:46px;display:flex;align-items:center;justify-content:center">✓</div><div><div style="font-weight:800;font-size:30px">Prenotazione confermata</div><div style="font-size:26px;color:#666">Dott. M. Bianchi · Mar 25 · 9:30</div></div></div>', 540, 260)
    notif.update({'in': 'down', 'at': at_ok})
    return [ph, finger, notif] + confetti(at_ok, n=60, y0=-100, spread=1000)

# ---------------------------------------------------------------------------------- confetti
def confetti(at, n=90, y0=-200, spread=1100, seed=3, depth=-20):
    rnd = random.Random(seed)
    cols = ['#39E75F', '#CDB8D8', '#5B3A66', '#1E3A2F', '#B39874', '#E8901C', '#2747F5', '#ffffff']
    pieces = ''.join(f'<i class="cf" style="position:absolute;left:{rnd.uniform(0, spread):.0f}px;top:{rnd.uniform(-400, 0):.0f}px;width:{rnd.choice([12, 16, 20])}px;height:{rnd.choice([22, 28, 10])}px;background:{rnd.choice(cols)};border-radius:{rnd.choice([2, 10])}px;opacity:0"></i>' for _ in range(n))
    it = HT(f'<div style="position:relative;width:{spread}px;height:10px">{pieces}</div>', 540, 200 + y0, idle=False, depth=depth)
    it['in'] = 'none'
    js = 'gsap.utils.toArray("#ID .cf").forEach(function(el,i){var r=((i*9301+49297)%233280)/233280;'
    js += 'tl.fromTo(el,{y:0,rotation:r*360,opacity:1},{y:2000+r*400,x:(r-0.5)*300,rotation:r*1440+360,duration:2.6+r*1.6,ease:"power1.in",immediateRender:false},@T+r*0.4);});'
    it['fx'] = [(at, js)]
    return [it]

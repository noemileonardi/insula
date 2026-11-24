"""Reusable visual building blocks -> lists of engine items."""
import html as H

def E(ch, x=540, y=720, size=300, **k):
    return dict(k='emoji', ch=ch, x=x, y=y, size=size, **k)

def T(s, x=540, y=720, size=64, **k):
    return _t(s, x, y, size, **k)

def _t(s, x, y, size, **k):
    d = dict(k='text', x=x, y=y, **k); d['s'] = s; d['size'] = size
    return d

def chip(s, x, y, bg='blue', size=46, **k):
    d = dict(k='chip', x=x, y=y, bg=bg, **k); d['s'] = s; d['size'] = size; return d

def tag(s, x, y, bg='lime', size=50, **k):
    d = dict(k='tag', x=x, y=y, bg=bg, **k); d['s'] = s; d['size'] = size; return d

def HT(html, x=540, y=720, **k):
    return dict(k='html', html=html, x=x, y=y, **k)

def bignum(n, label, color='orange'):
    return [HT(f'<div class="serif" style="font-size:520px;font-style:italic;color:#E8901C;line-height:.8">{n}</div>', 540, 640, **{'in': 'spin'}),
            HT(f'<div class="serif" style="font-size:96px;font-style:italic;color:#111">{label}</div>', 540, 1040, **{'in': 'up', 'dt': 0.35})]

def phone(inner, x=540, y=760, sc=1.0, **k):
    return HT(f'<div class="phone" style="transform:scale({sc})"><div class="scr"><div class="notch"></div>{inner}</div></div>', x, y, **k)

def cal(full=True, x=540, y=740, title='Agenda', **k):
    days = ['LUN', 'MAR', 'MER', 'GIO', 'VEN']
    cols = ['#1E3A2F', '#5B3A66', '#B39874', '#7FA992', '#9474A3']
    cells = ''.join(f'<div class="hd">{d}</div>' for d in days)
    for r in range(6):
        for c in range(5):
            fill = f'<i style="background:{cols[(r*2+c)%5]}"></i>' if full else ''
            cells += f'<div class="cell">{fill}</div>'
    head = f'<div style="grid-column:1/6;display:flex;justify-content:space-between;font-weight:800;font-size:38px;margin-bottom:6px"><span>{title}</span><span style="color:#999;font-weight:600">3 mesi</span></div>'
    it = HT(f'<div class="cal">{head}{cells}</div>', x, y, **k)
    if full:
        it['stg'] = [dict(sel='.cell i', dt=0.3, each=0.03, frm={'scaleX': 0}, to={'scaleX': 1}, ease='power2.out', sfx=True)]
    return it

def bubbles(lines, x=540, y0=430, gap=150, me=False, start=0, step=0.5, beat=None, ats=None):
    out = []
    for i, l in enumerate(lines):
        side = (i % 2)
        d = HT(f'<div class="bubble{" me" if (me if isinstance(me,bool) else me[i]) else ""}">{H.escape(l)}</div>', x + (-90 if side == 0 else 90), y0 + i * gap, **{'in': 'pop'})
        if ats: d['at'] = ats[i]
        else: d['dt'] = start + i * step
        if beat is not None: d['beat'] = beat
        out.append(d)
    return out

def ig_post(caption, likes, art, x=540, y=760, **k):
    return HT(f'''<div class="post"><div style="display:flex;align-items:center;gap:16px;padding:22px 26px"><div style="width:62px;height:62px;border-radius:50%;background:#ddd"></div><div style="font-weight:700;font-size:28px">dott.rossi</div></div>
<div style="height:600px;display:flex;align-items:center;justify-content:center;background:{art[1]};font-size:230px;font-family:'Noto Color Emoji'">{art[0]}</div>
<div style="padding:22px 28px;font-size:30px"><div style="font-size:44px;margin-bottom:10px">♡ &nbsp;💬 &nbsp;➤</div><b>{likes}</b><div style="margin-top:8px;color:#333">{H.escape(caption)}</div></div></div>''', x, y, **k)

def ig_profile(name, posts, followers, tiles_html, sub='Dermatologo · Palermo'):
    return f'''<div style="padding:80px 30px 0;font-family:Inter">
<div style="display:flex;align-items:center;gap:26px"><div style="width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#CDB8D8,#1E3A2F);border:5px solid #fff;box-shadow:0 0 0 4px #E1306C"></div>
<div style="display:flex;gap:26px;text-align:center;font-size:22px;color:#444"><div><b style="font-size:34px;color:#111">{posts}</b><br>post</div><div><b style="font-size:34px;color:#111">{followers}</b><br>follower</div><div><b style="font-size:34px;color:#111">312</b><br>seguiti</div></div></div>
<div style="margin-top:18px;font-weight:700;font-size:28px">{name}</div><div style="color:#666;font-size:24px">{sub}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin:24px -30px 0">{tiles_html}</div></div>'''

def tiles_uniform(n=12):
    cols = ['#CDB8D8', '#1E3A2F', '#F1ECF4']
    fg = ['#3d2347', '#F4EEE3', '#5B3A66']
    out = ''
    for i in range(n):
        c = i % 3
        txt = ['Il mito<br>del martedì', 'Domande<br>dal tuo<br>ambulatorio', 'Vero<br>o falso?'][c]
        out += f'<div class="tile" style="height:200px;background:{cols[c]};color:{fg[c]};font-size:34px;border-radius:0">{txt}</div>'
    return out

def serp(query, rows, x=540, y=760, **k):
    r = ''.join(f'''<div class="row" style="display:flex;gap:22px;align-items:center;padding:22px 0;border-top:2px solid #eee">
<div style="width:96px;height:96px;border-radius:18px;background:{c};flex:none"></div><div style="flex:1"><div style="font-size:34px;font-weight:700;color:#1a0dab">{H.escape(t)}</div>
<div style="font-size:28px;color:#E8901C">{st} <span style="color:#666">{H.escape(sub)}</span></div></div></div>''' for t, st, sub, c in rows)
    return HT(f'''<div class="serp"><div style="display:flex;align-items:center;gap:18px;border:3px solid #e3e3e3;border-radius:999px;padding:20px 30px;font-size:36px;margin-bottom:18px">🔍 <span>{H.escape(query)}</span></div>{r}</div>''', x, y, **k)

def site_new(x=540, y=760, **k):
    return HT('''<div class="site"><div style="background:#1E3A2F;color:#F4EEE3;padding:90px 44px 60px">
<div style="font-size:24px;letter-spacing:.2em;opacity:.7">DOTT. M. BIANCHI</div><div class="serif" style="font-size:86px;line-height:.95;margin-top:24px;font-style:italic">Cardiologo<br>a Palermo</div>
<div style="font-size:30px;margin-top:22px;opacity:.85">Visite, ECG e Holter<br>in centro città.</div></div>
<div style="padding:40px 44px"><div class="btn" style="text-align:center;font-size:38px;padding:28px">Prenota una visita</div>
<div style="display:flex;gap:16px;margin-top:34px"><div style="flex:1;height:180px;border-radius:24px;background:#F1ECF4;padding:20px;font-weight:700;font-size:26px">Palpitazioni: quando preoccuparsi</div><div style="flex:1;height:180px;border-radius:24px;background:#F8F3EA;padding:20px;font-weight:700;font-size:26px">Holter: come funziona</div></div>
<div style="margin-top:26px;font-size:30px;color:#E8901C">★★★★★ <span style="color:#555">4,9 · 212 recensioni</span></div></div></div>''', x, y, **k)

def site_old(x=540, y=760, **k):
    return HT('''<div class="site" style="background:#d9d9d9;font-family:'Times New Roman',serif"><div style="background:#003399;color:#ff0;padding:30px 20px;font-size:30px;text-align:center;font-weight:bold">Benvenuti nel sito del Dott. Neri</div>
<div style="padding:16px;font-size:17px;color:#222;line-height:1.3">Home | Chi sono | Curriculum | Congressi | Contatti<br><br>
<div style="width:100%;height:260px;border:2px solid #999;display:flex;align-items:center;justify-content:center;color:#999;font-size:22px">🖼 immagine non disponibile</div><br>
Il Dott. Neri si è laureato presso l'Università degli Studi nel 1998 con il massimo dei voti. Ha partecipato ai seguenti congressi: Roma 2006, Milano 2007, Napoli 2009, Bologna 2009...<br><br>
Per appuntamenti telefonare dal lunedì al venerdì dalle 9:00 alle 12:00.<br><br><span style="color:#00f;text-decoration:underline">Clicca qui</span><br><br>Visitatori: 000418<br>Ultimo aggiornamento: 03/2014</div></div>''', x, y, **k)

def counter(to, x, y, s=200, suf='', pre='', dec=0, c='ink', **k):
    d = dict(k='count', to=to, x=x, y=y, suf=suf, pre=pre, dec=dec, c=c, **k); d['size'] = s; return d

def bars(vals, x=540, y=1000, h=600, w=150, gap=60, colors=None, labels=None, beat=None, start=0.2, step=0.15, top=None):
    out = []; n = len(vals); total_w = n * w + (n - 1) * gap
    colors = colors or ['#5B3A66'] * n
    for i, v in enumerate(vals):
        cx = x - total_w / 2 + i * (w + gap) + w / 2
        bh = h * v
        d = HT(f'<div style="width:{w}px;height:{bh}px;background:{colors[i]};border-radius:12px 12px 0 0"></div>', cx, y - bh / 2, **{'in': 'grow', 'dt': start + i * step})
        d['style'] = 'transform-origin:50% 100%;'
        if beat is not None: d['beat'] = beat
        out.append(d)
        if labels:
            l = _t(labels[i], cx, y + 50, 34, **{'in': 'fade', 'dt': start + i * step}); l['c'] = 'grey'
            if beat is not None: l['beat'] = beat
            out.append(l)
        if top:
            l = _t(top[i], cx, y - bh - 50, 44, **{'in': 'up', 'dt': start + i * step + 0.5})
            if beat is not None: l['beat'] = beat
            out.append(l)
    out.append(HT('<div style="width:%dpx;height:5px;background:#111"></div>' % (total_w + 120), x, y, **{'in': 'growx'}))
    return out

def yt_channel(photo, x=540, y=740, **k):
    return HT(f'''<div style="width:920px;background:#fff;border-radius:34px;box-shadow:0 30px 80px rgba(0,0,0,.14);overflow:hidden;text-align:left;font-family:Inter;white-space:normal">
<div style="height:200px;background:linear-gradient(90deg,#0c2340,#1f5fa8)"></div>
<div style="display:flex;gap:30px;padding:0 40px;margin-top:-70px;align-items:flex-end"><div style="width:190px;height:190px;border-radius:50%;border:8px solid #fff;background:url({photo}) center/86% no-repeat #E9EEF8;flex:none"></div>
<div style="padding-bottom:12px"><div style="font-size:54px;font-weight:800">Doctor Mike <span style="font-size:36px;color:#888">✔</span></div><div style="font-size:30px;color:#666">@DoctorMike</div></div></div>
<div style="padding:26px 40px 36px;display:flex;align-items:center;justify-content:space-between"><div style="font-size:34px;color:#444"><b id="ytsubs" style="color:#111">~15 Mln</b> iscritti</div>
<div style="background:#111;color:#fff;border-radius:999px;padding:18px 40px;font-size:32px;font-weight:700">Iscriviti</div></div></div>''', x, y, **k)

def cta(word, x=540, y=900, **k):
    k.setdefault('type_at', word); k.setdefault('rate', 0.16)
    return HT(f'''<div style="width:900px;background:#fff;border-radius:40px;box-shadow:0 30px 80px rgba(0,0,0,.16);padding:34px 36px;text-align:left;font-family:Inter;white-space:normal">
<div style="font-size:30px;font-weight:700;margin-bottom:20px">Commenti</div>
<div style="display:flex;gap:18px;align-items:center"><div style="width:76px;height:76px;border-radius:50%;background:linear-gradient(135deg,#CDB8D8,#1E3A2F);flex:none"></div>
<div style="flex:1;border:3px solid #e5e5e5;border-radius:999px;padding:20px 30px;font-size:44px;font-weight:800;color:#111;letter-spacing:.04em;min-height:110px">{{{{TYPE:{word}}}}}</div><div style="font-size:34px;font-weight:800;color:#2747F5">Pubblica</div></div></div>''', x, y, **k)

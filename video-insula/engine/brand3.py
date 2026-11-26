"""VIDEO 3 – BRAND / Doctor Mike, v3 (from scratch): results-first case study.
Identity: 'editoriale' – Insula site aesthetic (cream, deep green, gold, lilac, Cormorant Garamond + Jost),
montage language of the reference reels: cut-outs, giant numbers, bar charts, stamps, labels, 3D devices."""
from widgets import E, T, HT, chip, tag, counter, phone, cta
from sito_fx import confetti

CREAM, GREEN, GOLD, LIL, VIOLET, INK = '#FDFBF7', '#1E3A2F', '#B39874', '#CDB8D8', '#5B3A66', '#1E2A24'
M3 = 'assets/mike_v3/'

def o(it, **kw):
    if 'in_' in kw: kw['in'] = kw.pop('in_')
    d = dict(it); d.update(kw); return d

def S(*items, **kw):
    out = []
    for i in items:
        out += i if isinstance(i, list) else [i]
    d = dict(items=out, bg=CREAM); d.update(kw); return d

def CUT(src, x, y, h, w0h0, **k):
    w0, h0 = w0h0
    d = dict(k='img', src=src, x=x, y=y, w=int(h * w0 / h0), h=h, r=0, fit='contain', depth=150,
             style='filter:drop-shadow(0 40px 40px rgba(30,42,36,.28));-webkit-mask-image:linear-gradient(180deg,#000 86%,transparent);mask-image:linear-gradient(180deg,#000 86%,transparent);')
    d.update(k); return d

def SHOT(src, x, y, w, h, r=36, **k):
    d = dict(k='img', src=src, x=x, y=y, w=w, h=h, r=r, pos='top', depth=40,
             style='box-shadow:0 40px 90px rgba(30,42,36,.30),0 0 0 6px #fff;')
    d.update(k); return d

def ph_img(src, x, y, sc=0.82, **k):
    it = phone(f'<img src="{src}" style="position:absolute;left:0;top:0;width:100%">', x, y, sc)
    it.update(k); return it

def BIG(txt, x, y, size, c=GREEN, it=False, **k):
    d = HT(f'<div style="font:{"italic " if it else ""}500 {size}px \'Cormorant Garamond\';color:{c};line-height:.9;letter-spacing:-.01em">{txt}</div>', x, y)
    d.update(k); return d

def KICK(txt, x, y, **k):
    d = HT(f'<div style="display:flex;align-items:center;gap:20px;font:400 30px Jost;letter-spacing:.32em;color:{GOLD}"><i style="display:block;width:70px;height:2px;background:{GOLD}"></i>{txt}<i style="display:block;width:70px;height:2px;background:{GOLD}"></i></div>', x, y)
    d.update(k); return d

def STAMP(txt, x, y, ok=True, **k):
    c = '#1E9E52' if ok else '#D7192B'
    d = HT(f'<div style="border:8px solid {c};color:{c};font:600 76px Jost;padding:4px 28px;border-radius:14px;letter-spacing:.06em;background:rgba(253,251,247,.85)">{txt}</div>', x, y)
    d.update({'in': 'stamp'}); d.update(k); return d

def NUMBER(to, x, y, size, suf='', dec=0, c=GREEN, label='', at=0, dur=1.3, pre=''):
    items = [counter(to, x, y, size, suf=suf, dec=dec, c=c, at=at, dur=dur, pre=pre,
                     style="font-family:'Cormorant Garamond';font-weight:600;letter-spacing:-.02em;")]
    if label:
        items.append(o(T(label, x, y + size * 0.62, 40, c=INK, style="font-family:Jost;font-weight:400;letter-spacing:.18em;text-transform:uppercase;"), in_='up', at=at))
    return items

def chapter(n, title, icon=None):
    """editorial chapter card (site style) – distinct from video 1 (big numbers) and video 2 (HUD)."""
    roman = ['I', 'II', 'III', 'IV'][n - 1]
    card = HT(f'''<div style="width:860px;padding:60px 60px 54px;border-radius:44px;background:{GREEN};color:#F4EEE3;text-align:left;white-space:normal;box-shadow:0 50px 100px rgba(30,58,47,.35)">
<div style="display:flex;align-items:center;gap:20px;font:400 28px Jost;letter-spacing:.34em;color:{GOLD}">LEVA {n:02d}<i style="display:block;flex:1;height:2px;background:{GOLD};opacity:.6"></i></div>
<div style="display:flex;align-items:flex-end;gap:30px;margin-top:22px"><div style="font:italic 500 200px 'Cormorant Garamond';line-height:.8;color:{LIL}">{roman}</div>
<div style="font:500 92px 'Cormorant Garamond';line-height:.95">{title}</div></div></div>''', 540, 780)
    card.update({'in': 'flip', 'sfxs': [(0, 'boom')]})
    out = [card]
    if icon: out.append(o(E(icon, 860, 470, 190), in_='spin', at=0.3))
    return out

def bars(vals, labels, tops, y=1150, h=560, w=230, gap=110, at_list=(0, 0), colors=(VIOLET, GREEN)):
    out = []; n = len(vals); total = n * w + (n - 1) * gap
    for i, v in enumerate(vals):
        cx = 540 - total / 2 + i * (w + gap) + w / 2; bh = h * v
        b = HT(f'<div style="width:{w}px;height:{bh}px;border-radius:18px 18px 0 0;background:repeating-linear-gradient(45deg,{colors[i]},{colors[i]} 22px,{colors[i]}dd 22px,{colors[i]}dd 44px);box-shadow:0 30px 60px rgba(30,42,36,.25)"></div>', cx, y - bh / 2)
        b.update({'in': 'grow', 'at': at_list[i], 'style': 'transform-origin:50% 100%;', 'idle': False, 'sfxs': [(at_list[i], 'riser')]})
        out.append(b)
        out.append(o(T(labels[i], cx, y + 60, 34, c=INK, style="font-family:Jost;font-weight:500;"), in_='up', at=at_list[i]))
        out += [counter(tops[i], cx, y - bh - 70, 96, suf=' Mln', c=colors[i], at=at_list[i], dur=1.1, style="font-family:'Cormorant Garamond';font-weight:600;")]
    out.append(HT(f'<div style="width:{total + 140}px;height:5px;background:{INK}"></div>', 540, y, **{'in': 'growx', 'idle': False}))
    return out

def spike_crash(at_up, at_down):
    svg = f'''<svg width="900" height="520" viewBox="0 0 900 520"><path class="up" d="M20,480 C200,470 300,440 380,380 S470,60 520,40" fill="none" stroke="{GREEN}" stroke-width="12" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200"/>
<path class="dn" d="M520,40 C560,120 600,420 880,490" fill="none" stroke="#D7192B" stroke-width="12" stroke-linecap="round" stroke-dasharray="900" stroke-dashoffset="900"/></svg>'''
    it = HT(f'<div style="padding:30px;border-radius:36px;background:#fff;box-shadow:0 40px 90px rgba(30,42,36,.18)">{svg}</div>', 540, 760)
    it.update({'in': 'up', 'fx': [(at_up, 'tl.to("#ID .up",{strokeDashoffset:0,duration:1.1,ease:"power2.in"},@T);'), (at_down, 'tl.to("#ID .dn",{strokeDashoffset:0,duration:0.9,ease:"power2.in"},@T);')],
               'sfxs': [(at_up, 'riser'), (at_down, 'swipe')]})
    return it

def letters_morph(src, dst, at):
    """'Mikhail Varshavski' flies apart, 'Doctor Mike' assembles."""
    a = ''.join(f'<span class="a{i}" style="display:inline-block">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(src))
    b = ''.join(f'<span class="b{i}" style="display:inline-block;opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(dst))
    html = f'''<div style="position:relative;width:1000px;height:260px;font:500 110px 'Cormorant Garamond';color:{INK};text-align:center">
<div style="position:absolute;inset:0;display:flex;justify-content:center;align-items:center">{a}</div>
<div style="position:absolute;inset:0;display:flex;justify-content:center;align-items:center;font-style:italic;color:{GREEN};font-size:150px">{b}</div></div>'''
    js = ''.join(f'tl.to("#ID .a{i}",{{y:{(-1) ** i * (180 + i * 9)},x:{(i - len(src) / 2) * 30},rotation:{(-1) ** i * 60},opacity:0,duration:0.55,ease:"power2.in"}},@T+{i * 0.015:.3f});' for i in range(len(src)))
    js += ''.join(f'tl.fromTo("#ID .b{i}",{{y:{-200 + (i % 3) * 120},opacity:0,rotationX:-90}},{{y:0,opacity:1,rotationX:0,duration:0.5,ease:"back.out(2)",immediateRender:false}},@T+{0.45 + i * 0.05:.3f});' for i in range(len(dst)))
    it = HT(html, 540, 700, idle=False)
    it.update({'in': 'fade', 'fx': [(at, js)], 'sfxs': [(at, 'swipe'), (at, 'sparkle')]})
    return it

def org_chart(at):
    node = lambda t, c: f'<div class="nd" style="padding:20px 30px;border-radius:24px;background:{c};color:#F4EEE3;font:500 34px Jost;box-shadow:0 20px 40px rgba(30,42,36,.2)">{t}</div>'
    html = f'''<div style="position:relative;width:900px;height:620px">
<div style="position:absolute;left:50%;top:0;transform:translateX(-50%)">{node("Doctor Mike", GREEN)}</div>
<svg width="900" height="620" style="position:absolute;inset:0"><path class="ln" d="M450,90 L450,200 M150,200 L750,200 M150,200 L150,300 M450,200 L450,300 M750,200 L750,300" stroke="{GOLD}" stroke-width="5" fill="none" stroke-dasharray="1600" stroke-dashoffset="1600"/></svg>
<div style="position:absolute;left:30px;top:300px">{node("🎬 Montaggio", VIOLET)}</div><div style="position:absolute;left:330px;top:300px">{node("🔬 Ricerca", VIOLET)}</div><div style="position:absolute;left:640px;top:300px">{node("🎙️ Podcast", VIOLET)}</div>
<div style="position:absolute;left:50%;top:470px;transform:translateX(-50%)">{node("📅 Calendario fisso", GOLD)}</div></div>'''
    it = HT(html, 540, 760)
    it.update({'in': 'up', 'fx': [(at, 'tl.to("#ID .ln",{strokeDashoffset:0,duration:1,ease:"power2.out"},@T);tl.fromTo("#ID .nd",{scale:0,opacity:0},{scale:1,opacity:1,duration:0.4,stagger:0.18,ease:"back.out(2)",immediateRender:false},@T+0.2);')],
               'sfxs': [(at, 'click'), (0.6, 'click'), (0.9, 'click')]})
    return it

def week_grid(at):
    cells = ''.join(f'<i class="wk" style="display:block;height:58px;border-radius:12px;background:{(VIOLET if d in (1, 4) else "#EDE7DD")}"></i>' for w in range(8) for d in range(7))
    it = HT(f'<div style="display:grid;grid-template-columns:repeat(7,86px);gap:12px;padding:34px;border-radius:36px;background:#fff;box-shadow:0 40px 90px rgba(30,42,36,.18)">{cells}</div>', 540, 700)
    it.update({'in': 'up', 'stg': [dict(sel='.wk', at=at, each=0.025, frm={'scale': 0}, to={'scale': 1}, sfx=True)]})
    return it

LEVE = [('un nome', 'che si ricorda', GREEN), ('contenuti', 'su ciò che i pazienti cercano', VIOLET), ('costanza', 'che non dipende dal tempo libero', GOLD), ('credibilità', 'mai in vendita', '#7FA992')]
def leve_cards():
    out = []
    for i, (a, b, c) in enumerate(LEVE):
        card = HT(f'''<div style="width:860px;height:200px;border-radius:32px;background:#fff;display:flex;align-items:center;gap:34px;padding:0 40px;box-shadow:0 30px 60px rgba(30,42,36,.15);border-left:16px solid {c};text-align:left;white-space:normal">
<div style="font:italic 500 110px 'Cormorant Garamond';color:{c};width:90px">{i + 1}</div><div><div style="font:500 64px 'Cormorant Garamond';color:{INK};line-height:1">{a}</div><div style="font:300 28px Jost;color:#5B6760;letter-spacing:.04em">{b}</div></div></div>''', 540, 420 + i * 230)
        card.update({'in': 'left' if i % 2 == 0 else 'right', 'at': ['nome', 'contenuti', 'costanza', 'credibilità'][i]})
        out.append(card)
    return out

# ------------------------------------------------------------------------------------------- scenes
BRAND3 = [
 dict(t="Cinque miliardi e seicento milioni di visualizzazioni.", v=S(
        o(E('▶️', 540, 450, 260), in_='spin'), NUMBER(5.6, 540, 820, 300, suf=' MLD', dec=1, c=GREEN, label='visualizzazioni', at='Cinque', dur=1.6))),
 dict(t="Quindici milioni di iscritti su YouTube.", v=S(
        o(ph_img(M3 + 'i0623.png', 540, 820, 0.85), in_='up'), o(tag('15,1 Mln iscritti', 820, 360, size=56, bg=LIL, c=INK), at='Quindici'))),
 dict(t="Più di cinque milioni su Instagram. / Tre su TikTok.", v=S(
        o(ph_img('assets/img/mike_ig_full.jpg', 330, 830, 0.7), in_='left', at='Instagram'),
        o(ph_img(M3 + 'i0624.png', 760, 860, 0.7), in_='right', at='TikTok'),
        o(tag('5,6 Mln', 330, 330, size=56, bg=LIL, c=INK), at='cinque'), o(tag('3,1 Mln', 760, 360, size=56, bg=LIL, c=INK), at='Tre'))),
 dict(t="E non è un attore, / non è un influencer.", v=S(
        o(BIG('attore', 540, 560, 150), in_='pop', at='attore', strike='non#2'), o(BIG('influencer', 540, 900, 150, it=True, c=VIOLET), in_='pop', at='influencer', strike='influencer'))),
 dict(t="È un *medico di famiglia* / del New Jersey.", v=S(
        o(CUT('assets/img/mike_scrubs_cut.png', 540, 760, 900, (376, 535)), in_='left'),
        o(chip('medico di famiglia', 540, 1230, bg=GREEN, size=56), at='medico'), o(chip('📍 New Jersey', 800, 330, bg=GOLD, size=40), at='Jersey'))),
 dict(t="Nel 2015 una rivista lo nomina / «il dottore più sexy d'America».", v=S(
        o(SHOT(M3 + 'i0632.jpg', 540, 760, 640, 793, r=8), in_='zoom', rot=-4),
        o(tag('People · 2015', 810, 320, size=54, bg=GOLD, c='#fff'), at='2015'))),
 dict(t="Aveva quasi un milione di follower.", v=S(
        o(E('📸', 540, 480, 220), in_='pop'), NUMBER(1, 540, 860, 280, suf=' Mln', c=VIOLET, label='follower nel 2015', at='quasi', dur=1.0))),
 dict(t="Per chiunque altro sarebbe stato il picco… / e poi il nulla.", v=S(spike_crash('picco', 'nulla'), o(BIG('…e poi il nulla.', 540, 1200, 90, it=True, c='#D7192B'), in_='up', at='nulla'))),
 dict(t="Lui invece fa una scelta: / smettere di essere *il dottore bello* / e diventare *il dottore di cui ti fidi*.", v=S(
        o(CUT(M3 + 'i0630_cut.png', 540, 640, 760, (1206, 1500)), in_='zoom'),
        o(chip('il dottore bello', 540, 1050, bg='#9A9A9A', size=54), at='bello', strike='diventare'),
        o(chip('il dottore di cui ti fidi', 540, 1180, bg=GREEN, size=58), at='fidi'))),
 dict(t="Leva numero uno: il nome.", v=S(chapter(1, 'Il nome', '🏷️')), p=0.2),
 dict(t="Mikhail Varshavski diventa *Doctor Mike*.", v=S(letters_morph('Mikhail Varshavski', 'Doctor Mike', 'diventa'))),
 dict(t="Due parole: chi è e cosa fa. / Lo ricordi dopo averlo sentito una volta.", v=S(
        o(BIG('Doctor', 330, 600, 140, it=True), in_='left'), o(BIG('Mike', 780, 600, 140, it=True, c=VIOLET), in_='right'),
        o(chip('cosa fa', 330, 780, bg=GREEN), at='cosa'), o(chip('chi è', 780, 780, bg=VIOLET), at='chi'), o(E('🧠', 540, 1050, 200), at='ricordi', in_='pop'))),
 dict(t="Leva numero due: / parlare di ciò che la gente guarda già.", v=S(chapter(2, 'Ciò che guardano già', '📺')), p=0.2),
 dict(t="Grey's Anatomy, Dr. House, / le bufale dei social.", v=S(
        o(ph_img(M3 + 'i0625.png', 540, 820, 0.85), in_='up', fx=[('House', 'tl.to("#ID .scr img",{y:-260,duration:1.4,ease:"power2.inOut"},@T);')]),
        o(chip("Grey's Anatomy", 300, 330, bg=VIOLET), at="Grey's"), o(chip('Dr. House', 800, 360, bg=GREEN), at='House'), o(chip('bufale', 540, 1260, bg='#D7192B'), at='bufale'))),
 dict(t="«Questo in corsia succede davvero?» / «Questo no.»", v=S(
        o(SHOT('assets/img/mike_tile1.jpg', 540, 760, 560, 750), in_='zoom'),
        STAMP('VERO', 330, 430, at='davvero'), STAMP('FALSO', 760, 1080, ok=False, at='no'))),
 dict(t="La reazione a Grey's Anatomy: *33 milioni* di visualizzazioni. / Quella a The Good Doctor: *44 milioni*.", v=S(
        bars([33 / 44, 1.0], ["Grey's Anatomy", 'The Good Doctor'], [33, 44], at_list=('33', '44')))),
 dict(t="La curiosità c'era già. / Lui ci ha aggiunto la *competenza*.", v=S(
        o(dict(k='video', src='assets/mike_clips/mike_dieta.mp4', x=540, y=740, w=520, h=758, depth=60, style='border-radius:34px;border:8px solid #fff;box-shadow:0 40px 80px rgba(30,42,36,.3);background:#111;'), in_='zoom'),
        o(chip('@doctor.mike', 380, 400, bg=INK, size=34), at=0.2), o(chip('competenza', 540, 1180, bg=GREEN, size=60), at='competenza'))),
 dict(t="Leva numero tre: la costanza.", v=S(chapter(3, 'La costanza', '📅')), p=0.2),
 dict(t="Due video a settimana, da quasi dieci anni. / Più di *milletrecento* video.", v=S(
        week_grid('Due'), NUMBER(1300, 540, 1180, 150, suf='+', c=VIOLET, label='video pubblicati', at='milletrecento', dur=1.2))),
 dict(t="Nel 2017 assume un montatore. / Poi una squadra.", v=S(
        o(chip('2017', 540, 330, bg=GOLD, size=60), at='2017'), o(E('🧑‍💻', 540, 700, 280), at='montatore', in_='walkl'),
        *[o(E(ch, 300 + 240 * i, 1060, 160), at='squadra', in_='pop', dt=0) for i, ch in enumerate(['👩‍💼', '🧑‍🎤', '👨‍🔬'])])),
 dict(t="Nel 2022 lancia un podcast, *The Checkup*.", v=S(
        o(ph_img(M3 + 'i0627.png', 330, 820, 0.66), in_='left'),
        o(dict(k='video', src='assets/mike_v3/podcast_ospite.mp4', x=780, y=820, w=430, h=600, depth=60, style='border-radius:30px;border:8px solid #fff;box-shadow:0 40px 80px rgba(30,42,36,.3);background:#111;'), in_='right', at='podcast'),
        o(tag('★ 4,9 su Spotify', 540, 1260, size=50, bg=GOLD, c='#fff'), at='Checkup'), o(chip('2022', 540, 320, bg=VIOLET, size=56), at='2022'))),
 dict(t="Il suo canale non è un hobby: / è organizzato come un ambulatorio.", v=S(org_chart('ambulatorio'))),
 dict(t="Leva numero quattro: la credibilità.", v=S(chapter(4, 'La credibilità', '🩺')), p=0.2),
 dict(t="E intanto continua a fare il medico.", v=S(
        o(CUT(M3 + 'i0631_cut.png', 380, 760, 820, (1206, 1487)), in_='left'),
        o(SHOT(M3 + 'i0628.png', 800, 720, 380, 520, r=24), in_='right', at='fare'),
        o(chip('medico in attività', 540, 1250, bg=GREEN, size=50), at='medico'))),
 dict(t="Quando sbaglia in un video, / lo corregge pubblicamente.", v=S(
        o(dict(k='video', src='assets/mike_clips/mike_chirurgo.mp4', x=540, y=740, w=520, h=866, depth=60, style='border-radius:34px;border:8px solid #fff;box-shadow:0 40px 80px rgba(30,42,36,.3);background:#111;'), in_='zoom'),
        STAMP('CORREZIONE', 540, 1180, ok=True, at='corregge'))),
 dict(t="Ha creato una fondazione che finanzia borse di studio, / e un evento di beneficenza ha raccolto *oltre un milione di dollari*.", v=S(
        o(SHOT(M3 + 'i0626.png', 540, 560, 520, 761, r=24), in_='up'),
        o(E('🎓', 860, 330, 180), at='borse', in_='pop'),
        NUMBER(1, 540, 1200, 150, suf=' Mln $+', c=GREEN, label='raccolti in beneficenza', at='oltre', dur=1.0))),
 dict(t="Ed è per questo / che i brand della salute lo scelgono come volto.", v=S(
        o(CUT('assets/img/mike_ritratto_cut.png', 540, 700, 620, (1206, 863)), in_='zoom'),
        o(E('🤝', 540, 1100, 200), at='brand', in_='pop'), o(chip('brand della salute', 540, 1260, bg=VIOLET, size=46), at='salute'))),
 dict(t="Tu non devi diventare Doctor Mike.", v=S(o(BIG('Doctor Mike', 540, 760, 160, it=True), in_='pop', strike='Mike'))),
 dict(t="Ti bastano le stesse quattro leve, nella tua città: / un *nome* che si ricorda, / *contenuti* che rispondono a ciò che i pazienti già cercano, / una *costanza* che non dipende da quando hai tempo, / e una *credibilità* che non metti mai in vendita.", v=S(leve_cards(), capy=1420)),
 dict(t="Noi di Insula costruiamo brand per medici, / dal nome al primo video, / nel rispetto del codice deontologico.", v=S(
        confetti(0.3, n=80), o(dict(k='img', src='assets/img/insula-logo.webp', x=540, y=640, w=420, h=420, r=210), in_='spin'),
        o(chip('dal nome al primo video', 540, 990, bg=VIOLET), at='nome'), o(tag('✓ codice deontologico', 540, 1140, size=54, bg=LIL, c=INK), at='codice'))),
 dict(t="Se vuoi capire quale potrebbe essere il tuo, / commentami *BRAND* / e ti scrivo in privato.", v=S(
        o(cta('BRAND', 540, 760), in_='up'),
        o(HT('<div class="bubble me">Ciao! Ti scrivo in privato 👋</div>'), y=1040, at='scrivo'))),
]

TRANS = [('{rotationY:-90,x:540,opacity:1,transformOrigin:"0% 50%"}', '{rotationY:90,x:-540,opacity:1}'),
         ('{y:1920,opacity:1}', '{y:-1920,opacity:1}'),
         ('{scale:0.6,opacity:0,rotationZ:-6}', '{scale:1.5,opacity:0}'),
         ('{x:-1080,opacity:1}', '{x:1080,opacity:1}')]

CSS = """
@font-face{font-family:"Cormorant Garamond";src:url(assets/fonts/cormorant-garamond-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:"Cormorant Garamond";src:url(assets/fonts/cormorant-garamond-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:"Cormorant Garamond";src:url(assets/fonts/cormorant-garamond-latin-500-italic.woff2);font-weight:500;font-style:italic}
@font-face{font-family:Jost;src:url(assets/fonts/jost-latin-300-normal.woff2);font-weight:300}
@font-face{font-family:Jost;src:url(assets/fonts/jost-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:Jost;src:url(assets/fonts/jost-latin-500-normal.woff2);font-weight:500}
.cap{font-family:Jost,sans-serif;font-weight:500;letter-spacing:0;color:#1E2A24}
.cap.em{font-family:"Cormorant Garamond",serif;font-style:italic;font-weight:500;font-size:112px;color:#5B3A66}
.b1{background:radial-gradient(circle,#D5C5DF 0%,rgba(213,197,223,0) 70%)}
.b2{background:radial-gradient(circle,#EADCC4 0%,rgba(234,220,196,0) 70%)}
.floor{background-image:linear-gradient(rgba(30,58,47,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(30,58,47,.06) 2px,transparent 2px)}
.chip{font-family:"Cormorant Garamond",serif}
"""

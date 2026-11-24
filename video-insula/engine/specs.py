from widgets import *

def o(it, **kw):
    if 'in_' in kw: kw['in'] = kw.pop('in_')
    it = dict(it); it.update(kw); return it

def S(*items, **kw):
    """scene"""
    d = dict(items=list(items)); d.update(kw); return d

BLANK = dict(items=[], capy=900)          # word-only scene, like "nessuno" / "quasi" in the reference
DOC_A, DOC_B = '👩‍⚕️', '👨‍⚕️'
TAIL = {'social': 2.2, 'sito': 2.2, 'brand': 2.2}

# =====================================================================================
SOCIAL = [
 dict(t="Questo è un dermatologo.", v=S(o(E(DOC_A, 540, 700, 380), in_='left', float=True), o(chip('dermatologo', 540, 960), at=3))),
 dict(t="E anche questo è un dermatologo.", v=S(o(E(DOC_A, 300, 700, 300), in_='none'), o(chip('dermatologo', 300, 920, size=38), in_='none'),
        o(E(DOC_B, 790, 700, 300), in_='right'), o(chip('dermatologo', 790, 920, size=38), at=4))),
 dict(t="Stessa laurea, / stessa specializzazione, / stessa città.", v=S(
        o(T('🎓  stessa laurea', 540, 520, 62), at=0), o(T('🩺  stessa specializzazione', 540, 700, 62), at=2), o(T('📍  stessa città', 540, 880, 62), at=4),
        o(HT('<div class="dbox" style="width:900px;height:560px;border-color:#5B3A66"></div>', 540, 700), in_='fade', at=4))),
 dict(t="Eppure uno ha l'agenda *piena* per i prossimi tre mesi,", v=S(cal(True, 540, 700, title='Dott. A'),
        o(HT('<div class="stamp" style="background:rgba(255,255,255,.85)">PIENA</div>', 640, 1020), in_='stamp', at=4))),
 dict(t="l'altro aspetta che squilli il telefono.", v=S(o(cal(False, 540, 640, title='Dott. B'), in_='fade'),
        o(E('☎️', 540, 1050, 240), in_='pop', at=3, shake=0.4)), p=0.3),
 dict(t="E non è perché uno è più bravo dell'altro.", v=S(o(E(DOC_A, 280, 720, 260), in_='left'), o(E(DOC_B, 800, 720, 260), in_='right'),
        o(T('=', 540, 700, 200), at=4, c='violet'))),
 dict(t="Il motivo sono *tre cose* che il primo fa sui social", v=S(o(E('📱', 540, 760, 360), in_='zoom', float=True),
        o(T('1', 330, 470, 150, font='serif', i=True, c='orange'), at=3), o(T('2', 540, 380, 150, font='serif', i=True, c='orange'), at=4),
        o(T('3', 750, 470, 150, font='serif', i=True, c='orange'), at=5))),
 dict(t="e che quasi nessun medico ha mai notato.", v=BLANK, p=0.35),

 dict(t="*Prima cosa:* risponde prima che tu chieda.", v=S(*bignum('1', 'risponde prima')), p=0.25),
 dict(t="Oggi più di nove italiani su dieci cercano informazioni sulla salute online, / su Google o sull'intelligenza artificiale.", v=S(
        counter(94.2, 540, 560, 230, suf='%', dec=1, c='violet', at=3),
        o(T('cerca informazioni sulla salute online', 540, 760, 44), in_='up', at=8),
        o(HT(''.join(f'<span style="font-size:76px;font-family:Noto Color Emoji;opacity:{1 if i < 9 else .25}">🧑</span>' for i in range(10)), 540, 920), in_='fade', at=3,
          stg=[dict(sel='span', at=3, each=0.08, frm={'scale':0}, to={'scale':1})]),
        o(chip('Google', 360, 1080, bg='#4285F4', size=40), at=10), o(chip('AI', 720, 1080, bg='violet', size=40), at=13),
        o(T('Fonte: Sociometrica / FieldCare 2026', 540, 1190, 26, c='grey'), in_='fade', dt=1))),
 dict(t="Lui lo sa.", v=BLANK, p=0.25),
 dict(t="Prende le dieci domande che sente ogni giorno in ambulatorio / e le trasforma in dieci video.", v=S(
        *bubbles(['Il sole fa bene ai brufoli?', 'Ogni quanto controllo un neo?', 'La crema va messa la sera?'], y0=360, gap=140, ats=[1, 3, 6]),
        o(HT(''.join(f'<div class="tile" style="width:150px;height:240px;background:{["#CDB8D8","#1E3A2F","#F1ECF4","#B39874","#5B3A66"][i%5]};color:{["#3d2347","#F4EEE3","#5B3A66","#fff","#fff"][i%5]};font-size:30px;display:inline-flex;margin:6px">▶<br>#{i+1}</div>' for i in range(10)),
             540, 960, w=860, style='white-space:normal;text-align:center;'), in_='fade', at=12, stg=[dict(sel='.tile', at=12, each=0.07, sfx=True)]))),
 dict(t="«Il sole fa bene ai brufoli?» / «Ogni quanto controllo un neo?»", v=S(
        o(phone('<div style="position:absolute;inset:0;background:linear-gradient(180deg,#F1ECF4,#CDB8D8);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;text-align:center"><div style="font-size:150px;font-family:Noto Color Emoji">☀️</div><div class="serif" style="font-size:66px;font-style:italic;line-height:1;margin-top:30px;color:#3d2347">Il sole fa bene ai brufoli?</div><div style="margin-top:40px;font-size:26px;font-weight:700;color:#5B3A66">VERO O FALSO</div></div>', 330, 760, 0.74), in_='left'),
        o(phone('<div style="position:absolute;inset:0;background:linear-gradient(180deg,#1E3A2F,#0f2119);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;text-align:center"><div style="font-size:150px;font-family:Noto Color Emoji">🔍</div><div class="serif" style="font-size:66px;font-style:italic;line-height:1;margin-top:30px;color:#F4EEE3">Ogni quanto controllo un neo?</div><div style="margin-top:40px;font-size:26px;font-weight:700;color:#C9D2C9">1 MINUTO</div></div>', 750, 760, 0.74), in_='right', at=7))),
 dict(t="Così, quando il paziente entra nello studio, / lo conosce *già*.", v=S(o(E('🚪', 400, 700, 330), in_='pop'),
        o(E('🙋', 720, 740, 240), in_='right', at=4),
        o(HT('<div class="bubble">La seguo su Instagram! 😊</div>'), y=380, at=9))),
 dict(t="E si fida.", v=S(o(E('🤝', 540, 700, 360), in_='pop'), o(HT('<div class="stamp ok">FIDUCIA</div>', 540, 1010), in_='stamp', dt=0.3)), p=0.3),
 dict(t="L'altro invece pubblica gli auguri di Natale / e la foto della sala d'attesa.", v=S(
        o(ig_post('Buon Natale a tutti i pazienti!', '3 Mi piace', ('🎄', '#f4f4f4'), 330, 740, style='transform:scale(.72);'), in_='left', at=0),
        o(ig_post('La nostra sala d’attesa', '1 Mi piace', ('🪑', '#efe9e1'), 760, 820, style='transform:scale(.72);'), in_='right', at=8))),

 dict(t="*Seconda cosa:* il format.", v=S(*bignum('2', 'il format')), p=0.25),
 dict(t="Il primo esce sempre lo stesso giorno, / con gli stessi colori, / con la stessa rubrica: «Il mito del martedì».", v=S(
        o(phone(ig_profile('Dott.ssa Bianchi', '148', '24,6K', tiles_uniform(12)), 540, 780, 0.95), in_='up',
          stg=[dict(sel='.tile', at=6, each=0.06, sfx=True)]),
        o(chip('ogni martedì', 830, 330, bg='violet'), at=5), o(tag('stessi colori', 830, 1180, bg='#CDB8D8'), at=9))),
 dict(t="Dopo tre mesi, la gente lo *aspetta*. / Come un programma in TV.", v=S(o(E('📺', 540, 760, 380), in_='zoom'),
        o(HT('<div class="bubble me">È martedì! 🔔 Nuovo video</div>'), y=420, at=3), o(chip('appuntamento fisso', 540, 1080, bg='green'), at=7))),
 dict(t="L'altro pubblica quando si ricorda: / tre post a maggio, / poi il silenzio fino a settembre.", v=S(
        o(HT('<div style="display:flex;gap:26px;font-family:Inter;font-weight:700;font-size:34px;color:#999">' + ''.join(
            f'<div style="width:150px;text-align:center"><div style="height:220px;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:12px">{"".join("<i style='display:block;width:60px;height:60px;border-radius:50%;background:#5B3A66'></i>" for _ in range(n))}</div><div style="margin-top:16px;color:{"#111" if n else "#bbb"}">{m}</div></div>'
            for m, n in [('MAG', 3), ('GIU', 0), ('LUG', 0), ('AGO', 0), ('SET', 1)]) + '</div>', 540, 700), in_='fade',
          stg=[dict(sel='i', at=7, each=0.15, sfx=True)]),
        o(T('…silenzio…', 540, 1000, 70, font='serif', i=True, c='grey'), at=12))),
 dict(t="E l'algoritmo, / come le persone, / si dimentica di chi sparisce.", v=S(
        *bars([1, .7, .45, .25, .1], 540, 1000, 520, 120, 40, colors=['#5B3A66', '#7a5a86', '#9a80a6', '#bba9c4', '#ddd3e2'], labels=['MAG', 'GIU', 'LUG', 'AGO', 'SET']),
        o(T('copertura', 540, 1110, 40, c='grey'), in_='fade', dt=1), o(T('↓', 900, 520, 160, c='red'), at=9))),

 dict(t="*Terza cosa,* / ed è il colpo finale: / le regole.", v=S(*bignum('3', 'le regole'), o(E('⚖️', 830, 360, 160), at=8)), p=0.25),
 dict(t="Il primo sa esattamente cosa un medico *non* può dire.", v=S(o(E('🤐', 540, 620, 300), in_='pop'),
        o(HT('<div class="dbox" style="width:640px;height:150px;border-color:#D7192B;display:flex;align-items:center;justify-content:center"><span class="sans" style="font-size:64px;color:#D7192B">cosa NON dire</span></div>', 540, 960), at=6))),
 dict(t="Niente prima e dopo ad effetto, / niente sconti, / niente «il migliore della città».", v=S(
        o(T('📸 prima / dopo', 540, 520, 66), at=0, strike=1), o(T('🏷️ sconti', 540, 720, 66), at=6, strike=7),
        o(T('🏆 «il migliore della città»', 540, 920, 60), at=9, strike=12))),
 dict(t="Il codice deontologico vuole informazione, / non pubblicità.", v=S(
        o(HT('<div class="card" style="width:640px;height:480px;background:#fff;border:3px solid #eee"><div style="font-size:120px;font-family:Noto Color Emoji">📜</div><div style="font-size:40px">Codice di Deontologia Medica</div><div style="color:#888;font-size:32px">artt. 55 – 56</div></div>', 540, 640), in_='up'),
        o(tag('informazione ✓', 330, 1000, bg='lime'), at=3), o(tag('pubblicità ✕', 760, 1000, bg='#FFD2D6', c='#9a0f1c'), at=5))),
 dict(t="E proprio per questo / i suoi contenuti sono *credibili*.", v=S(o(E('⭐', 540, 680, 330), in_='spin'), o(HT('<div class="stamp ok">CREDIBILE</div>', 540, 1010), in_='stamp', at=7))),
 dict(t="L'altro copia i trend dei centri estetici, / mette «meno trenta per cento» sulla visita / e rischia una segnalazione all'Ordine.", v=S(
        o(ig_post('PROMO! Visita dermatologica scontata', '7 Mi piace', ('💆', '#fbe7ee'), 540, 700, style='transform:scale(.78);'), in_='up'),
        o(HT('<div class="stamp" style="font-size:120px;background:#fff">−30%</div>', 760, 520), in_='stamp', at=8),
        o(HT('<div class="card" style="width:700px;height:240px;background:#fff;flex-direction:row;gap:28px;border:4px solid #D7192B"><span style="font-size:110px;font-family:Noto Color Emoji">✉️</span><span style="font-size:40px;text-align:left;white-space:normal;width:420px">Ordine dei Medici<br><span style="color:#D7192B">segnalazione</span></span></div>', 540, 1080), in_='up', at=15))),
 dict(t="E guarda il risultato.", v=BLANK, p=0.3),
 dict(t="Il primo non è un influencer.", v=S(o(T('influencer', 540, 700, 130, font='serif', i=True), in_='pop', strike=4))),
 dict(t="È semplicemente il medico che la gente *conosce* / prima ancora di entrare in studio.", v=S(o(E(DOC_A, 540, 720, 330), in_='pop'),
        *[o(E(ch, 540 + dx, 720 + dy, 120), at=2 + i) for i, (ch, dx, dy) in enumerate([('🙋‍♀️', -330, -260), ('🙋', 330, -260), ('🧓', -380, 120), ('👩', 380, 120), ('👨‍🦱', -200, 380), ('👵', 220, 380)])])),
 dict(t="Noi di Insula facciamo esattamente questo, / solo per medici:", v=S(
        o(dict(k='img', src='assets/img/insula-logo.webp', x=540, y=700, w=460, h=460, r=230), in_='spin'),
        o(T('solo per medici', 540, 1040, 70, font='serif', i=True, c='green'), at=7))),
 dict(t="piano editoriale, / video, / testi, / tutto nel rispetto del codice deontologico.", v=S(
        o(chip('piano editoriale', 540, 440, bg='green'), at=0), o(chip('video', 540, 590, bg='violet'), at=2), o(chip('testi', 540, 740, bg='#B39874'), at=3),
        o(tag('✓ codice deontologico', 540, 920, size=58), at=7))),
 dict(t="Tu fai il medico. / Ai social pensiamo noi.", v=S(o(E('🩺', 300, 720, 280), in_='left'), o(E('📱', 790, 720, 280), in_='right', at=4),
        o(E('🤝', 540, 1000, 160), at=6))),
 dict(t="Se vuoi capire come funzionerebbe per la tua specializzazione, / commentami *SOCIAL* / e ti scrivo in privato.", v=S(
        o(cta('SOCIAL', 540, 760), in_='up'),
        o(HT('<div class="bubble me">Ciao! Ti scrivo in privato 👋</div>'), y=1040, at=12))),
]

VIDEOS = {'social': SOCIAL}
from specs_more import SITO, BRAND
VIDEOS.update(sito=SITO, brand=BRAND)

# ------------------------------------------------------------------ AI 3D scenes (used when the image exists)
def _attach(video, prefix, sid, *items, capy=1300):
    for b in VIDEOS[video]:
        if b['t'].startswith(prefix) and b.get('v') is not None:
            b['v'] = dict(b['v']); b['v']['ai'] = dict(id=sid, items=list(items), capy=capy); return
    raise KeyError(prefix)

_attach('social', "Eppure uno ha l'agenda", 'soc_agenda_piena', o(HT('<div class="stamp" style="background:rgba(255,255,255,.9)">PIENA</div>', 760, 330), in_='stamp', at='piena'))
_attach('social', "l'altro aspetta", 'soc_telefono_muto', o(chip('0 chiamate', 760, 330, bg='#9A9A9A'), at='telefono'))
_attach('social', "Così, quando il paziente", 'soc_ti_conosce', o(HT('<div class="bubble">La seguo su Instagram! 😊</div>'), y=330, at='conosce'))
_attach('social', "Dopo tre mesi", 'soc_programma_tv', o(HT('<div class="bubble me">È martedì! 🔔 Nuovo video</div>'), y=330, at='aspetta'))
_attach('social', "L'altro copia i trend", 'soc_ordine', o(HT('<div class="stamp" style="font-size:110px;background:rgba(255,255,255,.9)">−30%</div>', 780, 330), in_='stamp', at='trenta'), o(chip('segnalazione', 300, 330, bg='red'), at='segnalazione'))
_attach('social', "Tu fai il medico", 'soc_insula_team', o(chip('il medico', 300, 330, bg='green'), at='medico'), o(chip('noi: i social', 780, 330, bg='violet'), at='social'))
_attach('sito', "Immagina un paziente", 'sito_divano_notte')
_attach('sito', "Sono le undici di sera", 'sito_divano_notte', o(T('23:00', 540, 330, 170, c='#F4EEE3'), in_='zoom'))
_attach('sito', "Due tocchi", 'sito_prenota_ok', o(HT('<div class="stamp ok" style="background:rgba(255,255,255,.92)">FATTO</div>', 540, 330), in_='stamp', at='fissato'))
_attach('sito', "Sul sito del secondo c'è scritto", 'sito_telefono_attesa', o(HT('<div style="background:#f3f0e6;border:3px solid #bbb;padding:24px 30px;font-family:Times New Roman,serif;font-size:40px;text-align:center;white-space:normal;color:#222;width:700px">Telefonare lun–ven<br><b>9:00 – 12:00</b></div>', 540, 330), in_='down', at='telefonare'))
_attach('sito', "Il primo dorme", 'sito_dorme', o(chip('3 nuove prenotazioni', 540, 330, bg='green'), at='agenda'))
_attach('sito', "Il secondo paga un sito", 'sito_cassetto', o(chip('biglietto da visita', 540, 330, bg='#9A9A9A'), at='biglietto'))
_attach('brand', "Reagisce a Grey", 'brand_reaction', o(HT('<div class="stamp ok" style="background:rgba(255,255,255,.9)">VERO</div>', 300, 330), in_='stamp', at='davvero'), o(HT('<div class="stamp" style="background:rgba(255,255,255,.9)">FALSO</div>', 780, 330), in_='stamp', at='no'))
_attach('brand', "Lui però pubblica", 'brand_set_video', o(tag('2 video a settimana', 540, 330, size=60), at='settimana'))
_attach('brand', "E già nel 2017", 'brand_montatore', o(chip('2017', 540, 330, bg='red', size=60), at='2017'))
_attach('brand', "Il brand è quello", 'brand_pazienti_parlano', o(HT('<div class="bubble">Vai dalla dottoressa dei nei!</div>'), y=330, at='dicono'))
_attach('brand', "E intanto", 'brand_visita', o(HT('<div class="stamp ok" style="background:rgba(255,255,255,.9)">CREDIBILE</div>', 540, 330), in_='stamp', at='credibile'))

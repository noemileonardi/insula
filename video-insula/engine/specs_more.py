from widgets import *

def o(it, **kw):
    if 'in_' in kw: kw['in'] = kw.pop('in_')
    it = dict(it); it.update(kw); return it

def S(*items, **kw):
    d = dict(items=list(items)); d.update(kw); return d

BLANK = dict(items=[], capy=900)
NIGHT = '#0E1626'

def notif(txt, sub, y, **k):
    return HT(f'<div style="width:840px;background:rgba(255,255,255,.96);border-radius:34px;padding:26px 30px;display:flex;gap:24px;align-items:center;box-shadow:0 20px 50px rgba(0,0,0,.18);font-family:Inter;text-align:left;white-space:normal"><div style="width:84px;height:84px;border-radius:20px;background:#1E3A2F;color:#F4EEE3;display:flex;align-items:center;justify-content:center;font-size:44px;font-family:Noto Color Emoji">📅</div><div><div style="font-weight:800;font-size:32px">{txt}</div><div style="font-size:28px;color:#666">{sub}</div></div></div>', 540, y, **k)

def page_card(title, y, **k):
    return HT(f'<div style="width:820px;background:#fff;border-radius:28px;box-shadow:0 20px 50px rgba(0,0,0,.12);padding:30px 36px;font-family:Inter;text-align:left;white-space:normal;border-left:14px solid #5B3A66"><div style="font-size:24px;color:#2a7f3f">dottbianchi.it › approfondimenti</div><div style="font-size:40px;font-weight:800;color:#1a0dab;margin-top:6px">{title}</div></div>', 540, y, **k)

SITO = [
 dict(t="Questo è il sito di un cardiologo.", v=S(o(site_new(540, 760, style='transform:scale(.85)'), in_='left'), o(chip('cardiologo', 540, 1230), at='cardiologo'))),
 dict(t="E anche questo è il sito di un cardiologo.", v=S(o(site_new(300, 760, style='transform:scale(.5)'), in_='none'),
        o(site_old(790, 760, style='transform:scale(.5)'), in_='right'), o(chip('cardiologo', 300, 1080, size=38), in_='none'), o(chip('cardiologo', 790, 1080, size=38), at='cardiologo'))),
 dict(t="Stesso curriculum, / stessa città, / stesso prezzo della visita.", v=S(
        o(T('📄  stesso curriculum', 540, 520, 62), at=0), o(T('📍  stessa città', 540, 700, 62), at=2), o(T('💶  stesso prezzo', 540, 880, 62), at=4),
        o(HT('<div class="dbox" style="width:860px;height:560px;border-color:#5B3A66"></div>', 540, 700), in_='fade', at=4))),
 dict(t="Ma uno riceve prenotazioni *anche di notte*,", v=S(
        o(T('🌙', 880, 330, 120), in_='pop'),
        o(notif('Nuova prenotazione', 'Visita cardiologica · alle 23:14', 500), in_='down', at='prenotazioni'),
        o(notif('Nuova prenotazione', 'Holter · alle 23:41', 700), in_='down', at='anche'),
        o(notif('Nuova prenotazione', 'ECG · alle 00:07', 900), in_='down', at='notte'), bg=NIGHT, dark=True)),
 dict(t="l'altro ha un sito che nessuno apre.", v=S(o(site_old(540, 720, style='transform:scale(.72);filter:grayscale(1)'), in_='up'),
        o(HT('<div class="stamp" style="background:#fff">0 visite</div>', 540, 1080), in_='stamp', at='nessuno')), p=0.3),
 dict(t="Il motivo sono *tre dettagli* / che fanno la differenza tra un sito vetrina / e un sito che lavora per te.", v=S(
        o(T('1', 330, 380, 150, font='serif', i=True, c='orange'), at='tre'), o(T('2', 540, 300, 150, font='serif', i=True, c='orange'), at='tre'), o(T('3', 750, 380, 150, font='serif', i=True, c='orange'), at='dettagli'),
        o(E('🖼️', 300, 760, 220), at='vetrina'), o(chip('sito vetrina', 300, 960, bg='#9A9A9A'), at='vetrina'),
        o(E('⚙️', 780, 760, 220), at='lavora', in_='spin'), o(chip('sito che lavora', 780, 960, bg='green'), at='lavora'))),
 dict(t="Immagina un paziente.", v=S(o(E('🛋️', 540, 820, 380), in_='up'), o(E('🧑', 540, 640, 220), in_='pop', dt=0.3), o(T('🌙', 860, 330, 120), in_='fade'), bg=NIGHT, dark=True)),
 dict(t="Sono le undici di sera, / sente il cuore che batte strano.", v=S(
        o(T('23:00', 540, 520, 220, c='#F4EEE3'), in_='zoom'),
        o(E('❤️', 540, 860, 240), at='cuore', shake=0.2), bg=NIGHT, dark=True)),
 dict(t="Prende il telefono / e scrive: «cardiologo Palermo».", v=S(
        o(phone('<div style="padding:150px 26px 0"><div style="font-size:56px;font-weight:800;text-align:center;margin-bottom:34px">Google</div><div style="border:3px solid #ddd;border-radius:999px;padding:22px 26px;font-size:33px;font-weight:600;color:#111;min-height:92px;text-align:left;white-space:nowrap">🔍 {{TYPE:cardiologo Palermo}}</div></div>', 540, 760, 0.95), in_='up', type_at='scrive', rate=0.12), bg=NIGHT, dark=True), p=0.9),

 dict(t="*Primo dettaglio:* il pollice.", v=S(*bignum('1', 'il pollice'), o(E('👍', 820, 360, 150), at='pollice')), p=0.25),
 dict(t="Quel paziente non è al computer. / È sul divano, / col telefono in mano.", v=S(
        o(E('💻', 540, 520, 230), in_='pop', out='divano'), o(T('✕', 540, 520, 300, c='red'), at='computer', out='divano'),
        o(E('🛋️', 380, 820, 260), at='divano'), o(E('📱', 720, 800, 240), at='telefono'))),
 dict(t="Il sito del primo si apre in un attimo / e si legge con un dito.", v=S(
        o(site_new(540, 760, style='transform:scale(.85)'), in_='up'), o(tag('⚡ 0,8 secondi', 800, 340), at='attimo'), o(E('👆', 760, 1080, 170), at='dito'))),
 dict(t="Quello del secondo è stato fatto nel 2014: / testo minuscolo, / foto che non caricano, / un menu che non si apre.", v=S(
        o(site_old(540, 760, style='transform:scale(.85)'), in_='up'), o(chip('2014', 830, 330, bg='#9A9A9A'), at='2014'),
        o(tag('testo minuscolo', 300, 560, bg='#FFD2D6', c='#9a0f1c'), at='testo'), o(tag('foto ✕', 790, 720, bg='#FFD2D6', c='#9a0f1c'), at='foto'),
        o(tag('menu ✕', 300, 980, bg='#FFD2D6', c='#9a0f1c'), at='menu'))),
 dict(t="Secondo Google, / se una pagina da mobile ci mette più di tre secondi, / più della metà delle persone *se ne va*.", v=S(
        o(HT('<div style="width:220px;height:220px;border-radius:50%;border:18px solid #eee;border-top-color:#2747F5"></div>', 540, 520), in_='spin'),
        counter(3, 540, 520, 80, suf=' s', c='blue', at='tre', dur=1.0),
        counter(53, 540, 870, 230, suf='%', c='red', at='metà', dur=0.9),
        o(T('abbandona la pagina', 540, 1060, 48), at='va'), o(T('Fonte: Google / Think with Google', 540, 1160, 26, c='grey'), in_='fade', at='metà'))),
 dict(t="Il paziente torna indietro. / E clicca sul prossimo.", v=S(
        o(serp('cardiologo Palermo', [('Dott. M. Bianchi – Cardiologo', '★★★★★', '4,9 · aperto', '#1E3A2F'), ('Dott. Neri – Cardiologia', '★★★☆☆', '3 recensioni', '#bbb'), ('Centro Cuore', '★★★★☆', '4,2', '#CDB8D8')], 540, 760), in_='up'),
        o(E('👆', 800, 700, 140), at='clicca'), o(HT('<div class="dbox" style="width:880px;height:150px;border-color:#2747F5"></div>', 540, 640), at='prossimo'))),

 dict(t="*Secondo dettaglio:* prenota in due tocchi.", v=S(*bignum('2', 'due tocchi')), p=0.25),
 dict(t="Sul sito del primo c'è un solo bottone, / grande, / sempre visibile: «Prenota una visita».", v=S(
        o(HT('<div class="btn">Prenota una visita</div>', 540, 700), at=0), o(E('👆', 700, 860, 170), at='Prenota'),
        o(chip('sempre visibile', 540, 440, bg='violet'), at='visibile'))),
 dict(t="Due tocchi / e l'appuntamento è fissato.", v=S(
        o(HT('<div class="card" style="width:720px;height:420px;background:#fff;border:3px solid #eee"><div style="font-size:120px;font-family:Noto Color Emoji">✅</div><div style="font-size:48px">Visita confermata</div><div style="color:#888;font-size:34px">martedì · 14:30</div></div>', 540, 700), in_='pop'),
        o(HT('<div class="stamp ok">FATTO</div>', 540, 1040), in_='stamp', at='fissato'))),
 dict(t="Sul sito del secondo c'è scritto: / «telefonare dal lunedì al venerdì, / dalle nove alle dodici».", v=S(
        o(HT('<div style="width:820px;background:#f3f0e6;border:3px solid #bbb;padding:44px;font-family:Times New Roman,serif;font-size:50px;text-align:center;white-space:normal;color:#222">Per appuntamenti telefonare<br>dal <b>lunedì</b> al <b>venerdì</b><br>dalle <b>9:00</b> alle <b>12:00</b></div>', 540, 680), in_='up'),
        o(E('☎️', 540, 1050, 180), at='telefonare'))),
 dict(t="Alle undici di sera, / il paziente sceglie chi gli permette di prenotare *adesso*.", v=S(
        o(T('23:00', 540, 460, 180, c='#F4EEE3'), in_='zoom'), o(HT('<div class="btn" style="background:#F4EEE3;color:#1E3A2F">Prenota adesso</div>', 540, 820), at='prenotare'),
        o(E('👆', 700, 980, 160), at='adesso'), bg=NIGHT, dark=True)),

 dict(t="*Terzo dettaglio,* / il più sottovalutato: / parlare la lingua di Google.", v=S(*bignum('3', 'la lingua di Google'), o(E('🔍', 820, 360, 150), at='Google')), p=0.25),
 dict(t="Il primo ha una pagina per ogni domanda che i pazienti si fanno davvero: / «Palpitazioni: quando preoccuparsi». / «Holter: come funziona».", v=S(
        o(page_card('Palpitazioni: quando preoccuparsi', 520), at=0), o(page_card('Holter: come funziona', 740), at='Holter'),
        o(page_card('Pressione alta: i primi segnali', 960), at='domanda', in_='fade'))),
 dict(t="E una scheda Google con foto, / orari aggiornati / e *recensioni* a cui risponde.", v=S(
        o(serp('cardiologo vicino a me', [('Dott. M. Bianchi – Cardiologo', '★★★★★', '4,9 · 212 recensioni', '#1E3A2F')], 540, 560), in_='up'),
        o(tag('📷 foto', 250, 840), at='foto'), o(tag('🕐 orari', 540, 840), at='orari'), o(tag('⭐ recensioni', 830, 840), at='recensioni'),
        o(HT('<div class="bubble">Grazie per la fiducia, a presto!</div>'), y=1050, at='risponde'))),
 dict(t="Il secondo ha una pagina sola: / «Chi sono». / Con l'elenco dei congressi del 2009.", v=S(
        o(HT('<div style="width:800px;background:#fff;border:3px solid #bbb;padding:40px;font-family:Times New Roman,serif;font-size:36px;text-align:left;white-space:normal;color:#222"><div style="font-size:60px;font-weight:bold;margin-bottom:20px;color:#003399">Chi sono</div>Congressi:<br>• Roma, 2006<br>• Milano, 2007<br>• Napoli, 2009<br>• Bologna, 2009<br>• …</div>', 540, 720), in_='up'),
        o(chip('2009', 820, 420, bg='#9A9A9A'), at='2009'))),
 dict(t="Google non può consigliare / quello che non riesce a capire.", v=S(o(E('🤖', 540, 680, 300), in_='pop'), o(T('?', 760, 480, 220, c='red', font='serif', i=True), at='capire'))),
 dict(t="E guarda il risultato.", v=BLANK, p=0.3),
 dict(t="Il primo dorme / e il suo sito continua a riempirgli l'agenda.", v=S(o(E('😴', 540, 400, 200), in_='pop'), o(cal(True, 540, 860, title='Dott. Bianchi', style='transform:scale(.8)'), in_='up', at='sito'))),
 dict(t="Il secondo paga un sito / che fa da *biglietto da visita* / in un cassetto.", v=S(
        o(E('🗄️', 540, 840, 380), in_='up'), o(HT('<div style="width:440px;height:250px;background:#fff;border-radius:10px;box-shadow:0 20px 40px rgba(0,0,0,.2);font-family:Times New Roman,serif;display:flex;flex-direction:column;justify-content:center;align-items:center;font-size:34px;rotate:-6deg;white-space:normal;text-align:center">Dott. Neri<br><span style="font-size:24px;color:#666">www.dottneri.it</span></div>', 540, 480), at='biglietto'))),
 dict(t="Noi di Insula costruiamo siti per medici / pensati per il telefono, / per la prenotazione / e per Google.", v=S(
        o(dict(k='img', src='assets/img/insula-logo.webp', x=540, y=520, w=380, h=380, r=190), in_='spin'),
        o(chip('📱 telefono', 540, 830, bg='green'), at='telefono'), o(chip('📅 prenotazione', 540, 960, bg='violet'), at='prenotazione'), o(chip('🔍 Google', 540, 1090, bg='#B39874'), at='Google'))),
 dict(t="Testi scritti da chi conosce la comunicazione sanitaria, / non da chi vende siti a tutti.", v=S(o(E('✍️', 540, 620, 280), in_='pop'),
        o(tag('comunicazione sanitaria ✓', 540, 920), at='comunicazione'), o(T('siti per tutti', 540, 1080, 60, c='grey'), at='vende', strike='tutti'))),
 dict(t="Se vuoi sapere cosa cambierei nel tuo sito, / commentami *SITO* / e ti scrivo in privato.", v=S(
        o(cta('SITO', 540, 760), in_='up'),
        o(HT('<div class="bubble me">Ciao! Ti scrivo in privato 👋</div>'), y=1040, at='scrivo'))),
]

# =====================================================================================
MIKE = 'assets/img/mike_scrubs.jpg'        # photos supplied by the client
MIKE_R = 'assets/img/mike_ritratto.jpg'
def CUT(name, x, y, h, **k):
    from PIL import Image
    w0, h0 = Image.open(f'assets/img/{name}_cut.png').size
    d = dict(k='img', src=f'assets/img/{name}_cut.png', x=x, y=y, w=int(h * w0 / h0), h=h, r=0, fit='contain', depth=150,
             style='filter:drop-shadow(0 40px 40px rgba(0,0,0,.25));-webkit-mask-image:linear-gradient(180deg,#000 85%,transparent);mask-image:linear-gradient(180deg,#000 85%,transparent);')
    d.update(k); return d

def mag(x=540, y=740, **k):
    return HT(f'''<div style="width:600px;height:800px;position:relative;box-shadow:0 30px 80px rgba(0,0,0,.25);background:url({MIKE}) center 20%/cover #0c2340;font-family:Inter;color:#fff;text-align:left;white-space:normal;overflow:hidden">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,0) 35%,rgba(0,0,0,.75))"></div>
<div style="position:absolute;top:24px;left:30px;font-size:110px;font-weight:900;letter-spacing:-.04em;color:#D7192B">RIVISTA</div>
<div style="position:absolute;top:150px;right:30px;font-size:30px;font-weight:700">2015</div>
<div class="serif" style="position:absolute;bottom:40px;left:30px;right:30px;font-size:74px;line-height:.95;font-style:italic">Il dottore più sexy d’America</div></div>''', x, y, **k)

def MCLIP(name, x, y, w, **k):
    from PIL import Image
    import subprocess
    wh = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', f'assets/mike_clips/{name}.mp4'], capture_output=True, text=True).stdout.strip().split(',')
    h = int(w * int(wh[1]) / int(wh[0]))
    d = dict(k='video', src=f'assets/mike_clips/{name}.mp4', x=x, y=y, w=w, h=h, depth=60,
             style='border-radius:34px;border:8px solid #fff;box-shadow:0 40px 80px rgba(0,0,0,.28);background:#111;')
    d.update(k); return d

def card3(n, label, bg, y, at):
    return o(HT(f'<div class="card" style="width:820px;height:190px;flex-direction:row;gap:30px;background:{bg}"><span class="serif" style="font-size:110px;font-style:italic;color:#E8901C">{n}</span><span style="font-size:52px">{label}</span></div>', 540, y), at=at)

BRAND = [
 dict(t="Questo è un medico di famiglia del New Jersey.", v=S(o(CUT('mike_scrubs', 540, 700, 860), in_='left'),
        o(chip('medico di famiglia', 540, 1130, bg='green'), at='medico'), o(chip('🇺🇸 New Jersey', 780, 340, bg='blue', size=40), at='Jersey'))),
 dict(t="Ed è anche uno dei medici più seguiti *del pianeta*:", v=S(
        o(E('🌍', 540, 640, 380), in_='spin'), o(CUT('mike_ritratto', 540, 1010, 300), at='seguiti'))),
 dict(t="circa quindici milioni di iscritti su YouTube / e più di cinque milioni di follower su Instagram.", v=S(
        counter(15, 280, 330, 100, suf=' Mln', c='red', at='quindici', dur=1.2), o(T('YouTube', 280, 420, 40, c='grey'), at='YouTube'),
        counter(5.6, 800, 330, 100, suf=' Mln', dec=1, c='violet', at='cinque', dur=1.2), o(T('Instagram', 800, 420, 40, c='grey'), at='Instagram'),
        o(phone('<img src="assets/img/mike_ig_full.jpg" style="position:absolute;top:60px;left:0;width:100%">', 540, 900, 0.62), in_='up', at='follower'))),
 dict(t="Si chiama Mikhail Varshavski. / Ma tu probabilmente lo conosci come *Doctor Mike*.", v=S(
        o(T('Mikhail Varshavski', 540, 440, 76, font='serif', i=True), in_='up', out='Ma'),
        o(yt_channel(MIKE_R, 540, 740), in_='up', at='Ma'))),
 dict(t="Nel 2015 una rivista americana lo nomina «il dottore più sexy d'America».", v=S(o(mag(540, 720), in_='zoom'), o(tag('2015', 860, 300, size=60), at='2015'))),
 dict(t="Poteva diventare l'ennesimo bel ragazzo di Instagram / e sparire dopo una stagione.", v=S(
        o(HT(f'<div class="post"><div style="display:flex;align-items:center;gap:16px;padding:22px 26px"><div style="width:62px;height:62px;border-radius:50%;background:url({MIKE}) center 20%/cover #E9EEF8"></div><div style="font-weight:700;font-size:28px">dr.mike</div></div><div style="height:560px;background:url({MIKE}) center 20%/cover #E9EEF8"></div><div style="padding:20px 28px;font-size:34px">🔥🔥🔥 <b>virale</b></div></div>', 540, 700, style='transform:scale(.8)'), in_='up', out='sparire'),
        o(T('sparire?', 540, 700, 120, font='serif', i=True, c='grey'), at='sparire'))),
 dict(t="Invece, / dieci anni dopo, / è ancora lì.", v=S(
        o(HT('<div style="width:860px;height:10px;background:#111;border-radius:5px"></div>', 540, 760), in_='growx', at='dieci'),
        o(chip('2015', 150, 650, bg='#9A9A9A'), at='Invece'), o(chip('2026', 930, 650, bg='red'), at='dopo'),
        o(CUT('mike_palco', 540, 470, 560), at='ancora', in_='up'))),
 dict(t="Il motivo sono *tre scelte di brand* / che puoi copiare anche tu, / anche se non vuoi diventare famoso.", v=S(
        o(CUT('mike_ritratto', 540, 780, 560), in_='zoom'),
        o(T('1', 260, 470, 150, font='serif', i=True, c='orange'), at='tre'), o(T('2', 540, 380, 150, font='serif', i=True, c='orange'), at='scelte'),
        o(T('3', 820, 470, 150, font='serif', i=True, c='orange'), at='brand'), o(chip('copiabili', 540, 1080, bg='violet'), at='copiare'))),

 dict(t="*Prima scelta:* il nome.", v=S(*bignum('1', 'il nome')), p=0.25),
 dict(t="«Mikhail Varshavski» / è difficile da dire, / figurati da ricordare.", v=S(
        o(T('Mikhail Varshavski', 540, 620, 100, font='serif', i=True), in_='up'), o(T('?', 900, 460, 160, c='red'), at='difficile'), o(T('?', 180, 800, 160, c='red'), at='ricordare'))),
 dict(t="«Doctor Mike» / no.", v=S(o(T('Doctor Mike', 540, 640, 150, font='serif', i=True, c='green'), in_='zoom'), o(HT('<div class="stamp ok">FACILE</div>', 540, 900), in_='stamp', at='no'))),
 dict(t="Due parole, / e sai già chi è / e cosa fa.", v=S(
        o(T('Doctor', 340, 600, 120, font='serif', i=True), in_='left'), o(T('Mike', 760, 600, 120, font='serif', i=True), in_='right'),
        o(chip('cosa fa', 340, 780, bg='green'), at='cosa'), o(chip('chi è', 760, 780, bg='violet'), at='chi'))),
 dict(t="Ora pensa al tuo profilo: / «Dott. Mario Rossi, / medico chirurgo, / specialista in…» / e si perde a metà.", v=S(
        o(phone('<div style="padding:120px 34px 0;text-align:center"><div style="width:150px;height:150px;border-radius:50%;background:linear-gradient(135deg,#CDB8D8,#1E3A2F);margin:0 auto 26px"></div><div style="font-size:34px;font-weight:600;line-height:1.35;text-align:left;min-height:200px">{{TYPE:Dott. Mario Rossi, medico chirurgo, specialista in…}}</div></div>', 540, 760, 0.95), in_='up', type_at='Dott', rate=0.06),
        o(T('…?', 540, 900, 120, c='grey', font='serif', i=True), at='perde'))),
 dict(t="Il brand è quello che i pazienti dicono di te / quando *non* sei nella stanza.", v=S(
        *bubbles(['Vai dalla dottoressa dei nei!', 'Quello che spiega tutto su Instagram?', 'Sì, il cardiologo dei video!'], y0=420, gap=170, ats=['pazienti', 'dicono', 'quando']),
        o(E('🚪', 540, 1020, 160), at='stanza'))),
 dict(t="E devono riuscire a dirlo.", v=BLANK, p=0.3),

 dict(t="*Seconda scelta:* parlare di quello che la gente guarda già.", v=S(*bignum('2', 'ciò che guardano già')), p=0.25),
 dict(t="Doctor Mike non parte raccontando se stesso.", v=S(o(E('🤳', 540, 680, 300), in_='pop'), o(T('io, io, io…', 540, 960, 80, font='serif', i=True), at='raccontando', strike='stesso'))),
 dict(t="Reagisce a Grey's Anatomy / e a Dr. House: / «questo in corsia succede davvero?» / «Questo no.»", v=S(
        o(dict(k='img', src='assets/img/mike_tile1.jpg', x=540, y=680, w=480, h=640, r=30), in_='zoom'), o(chip("Grey's Anatomy", 300, 380, bg='#2747F5'), at="Grey's"), o(chip('Dr. House', 790, 400, bg='violet'), at='House'),
        o(HT('<div class="stamp ok">VERO</div>', 300, 980), in_='stamp', at='davvero'), o(HT('<div class="stamp">FALSO</div>', 780, 980), in_='stamp', at='no'))),
 dict(t="Smonta i miti / che la gente trova già sui social.", v=S(
        o(T('«Il limone cura tutto»', 540, 360, 60, font='serif', i=True), at='Smonta', strike='miti'), o(T('«Il caffè fa male al cuore»', 540, 500, 60, font='serif', i=True), at='gente', strike='trova'),
        o(T('«Antibiotici per il raffreddore»', 540, 640, 58, font='serif', i=True), at='già', strike='social'),
        o(MCLIP('mike_dieta', 540, 1000, 430), at='Smonta', in_='up'), o(chip('@doctor.mike', 400, 700, bg='#111', size=34), at='Smonta'))),
 dict(t="Così sposta l'attenzione / dalla sua faccia / alla sua *competenza*.", v=S(
        o(CUT('mike_scrubs', 280, 720, 520), at='faccia', in_='left'), o(T('→', 540, 720, 140, c='violet'), at='alla'),
        o(MCLIP('mike_chirurgo', 790, 720, 380), at='alla', in_='right'), o(chip('competenza', 790, 1100, bg='green'), at='competenza'))),
 dict(t="Da «il dottore bello» / a «il dottore di cui mi fido».", v=S(
        o(chip('il dottore bello', 540, 560, bg='#9A9A9A', size=56), at=0, strike='a'), o(T('↓', 540, 720, 120, c='violet'), at='a'),
        o(chip('il dottore di cui mi fido', 540, 880, bg='green', size=56), at='fido'))),

 dict(t="*Terza scelta,* / la meno glamour / e la più importante: / la costanza.", v=S(*bignum('3', 'la costanza')), p=0.25),
 dict(t="Il suo canale *non* esplode subito.", v=S(*bars([.08, .1, .13, .15, .2, .24], 540, 1000, 520, 100, 36, colors=['#CDB8D8'] * 6, labels=['', '', '', '', '', '']),
        o(T('lento.', 540, 480, 110, font='serif', i=True, c='grey'), at='esplode'))),
 dict(t="Lui però pubblica due video a settimana. / Sempre.", v=S(
        o(MCLIP('mike_podcast', 540, 680, 600), in_='zoom'), o(chip('@doctor.mike · The Checkup', 540, 300, bg='#111', size=34), at='pubblica'),
        o(tag('2 video a settimana', 540, 1150, size=60), at='settimana'))),
 dict(t="E già nel 2017 / assume un montatore, / perché ha capito che da solo / non può fare il medico / e anche la casa di produzione.", v=S(
        o(chip('2017', 540, 380, bg='red', size=60), at='2017'), o(E('🧑‍💻', 330, 700, 240), at='montatore'), o(E('🎬', 760, 700, 240), at='montatore'),
        o(E('🩺', 330, 1000, 160), at='medico'), o(E('🎥', 760, 1000, 160), at='produzione'))),
 dict(t="Tratta il suo brand come tratta l'ambulatorio: / con orari, / persone / e processi.", v=S(
        o(E('🏥', 540, 520, 260), in_='pop'), o(chip('🕐 orari', 540, 800, bg='green'), at='orari'), o(chip('👥 persone', 540, 930, bg='violet'), at='persone'), o(chip('⚙️ processi', 540, 1060, bg='#B39874'), at='processi'))),
 dict(t="E intanto / continua a fare il medico. / Ed è proprio questo che lo rende credibile.", v=S(
        o(CUT('mike_scrubs', 540, 700, 760), in_='zoom'), o(chip('medico in attività', 540, 360, bg='green'), at='medico'),
        o(HT('<div class="stamp ok" style="background:#fff">CREDIBILE</div>', 540, 1040), in_='stamp', at='credibile'))),
 dict(t="E qui arriva la parte che ti interessa.", v=BLANK, p=0.3),
 dict(t="Non devi diventare Doctor Mike.", v=S(o(T('Doctor Mike', 540, 700, 140, font='serif', i=True), in_='pop', strike='Mike'))),
 dict(t="Ti basta fare le stesse tre scelte / in piccolo, / nella tua città: / un *nome* che si ricorda, / un *format* riconoscibile, / una *costanza* che non dipende da quando hai tempo.", v=S(
        card3(1, 'un nome', '#F1ECF4', 480, 'nome'), card3(2, 'un format', '#F8F3EA', 700, 'format'), card3(3, 'una costanza', '#E6EEE9', 920, 'costanza'))),
 dict(t="Questo video l'abbiamo costruito con le stesse tecniche / per farti arrivare fino a qui. / E se mi stai ancora ascoltando, / direi che funzionano.", v=S(
        o(E('🎯', 540, 640, 300), in_='spin'), o(E('👀', 540, 980, 180), at='ascoltando'), o(HT('<div class="stamp ok">FUNZIONA</div>', 540, 380), in_='stamp', at='funzionano'))),
 dict(t="Noi di Insula costruiamo brand per medici, / dal nome al primo video, / nel rispetto del codice deontologico.", v=S(
        o(dict(k='img', src='assets/img/insula-logo.webp', x=540, y=560, w=420, h=420, r=210), in_='spin'),
        o(chip('dal nome al primo video', 540, 900, bg='violet'), at='nome'), o(tag('✓ codice deontologico', 540, 1060, size=56), at='codice'))),
 dict(t="Se vuoi capire quale potrebbe essere il tuo, / commentami *BRAND* / e ti scrivo in privato.", v=S(
        o(cta('BRAND', 540, 760), in_='up'),
        o(HT('<div class="bubble me">Ciao! Ti scrivo in privato 👋</div>'), y=1040, at='scrivo'))),
]

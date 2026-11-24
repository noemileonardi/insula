"""Generate the stylized 3D scene images with Gemini (Nano Banana).
Usage: python3 tools/scenes_ai.py [scene_id ...]     (no args = all missing)
The API key is injected by the environment proxy (network secret, header x-goog-api-key).
"""
import base64, json, os, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'scenes')
MODELS = ['gemini-3-pro-image-preview', 'gemini-2.5-flash-image', 'gemini-2.5-flash-image-preview']

STYLE = ("Stylized 3D render in the style of a premium animated short film: soft clay-like characters with realistic proportions, "
         "expressive faces, semi-realistic materials, warm cinematic lighting, shallow depth of field. "
         "Background walls and floor made of subtle faceted low-poly geometric panels (white and warm grey), clean and elegant. "
         "Colour accents: deep forest green #1E3A2F, soft lilac #CDB8D8, warm beige. Modern Italian setting. "
         "Vertical 9:16 composition, main subject in the upper-middle part of the frame, empty calm area in the lower third. "
         "Absolutely no text, no letters, no logos, no watermarks.")

SCENES = {
    # ---------------- VIDEO 1 – SOCIAL
    'soc_agenda_piena': "A busy, bright dermatology clinic waiting room: several patients of different ages sitting and waiting, a friendly receptionist at the desk, a confident female dermatologist in a white coat greeting a patient at the door.",
    'soc_telefono_muto': "An empty, quiet medical office: a male doctor in a white coat sitting alone at his desk, chin on his hand, staring at a silent landline phone. Empty chairs, dim afternoon light, a little melancholic.",
    'soc_ti_conosce': "A smiling patient entering a doctor's office and shaking hands warmly with a female dermatologist in a white coat, as if they already know each other. Bright, welcoming room with plants.",
    'soc_programma_tv': "A young couple sitting on a sofa in a cosy living room in the evening, both looking at a smartphone together with curiosity, the phone screen glowing on their faces.",
    'soc_ordine': "A worried doctor in a white coat sitting at his desk reading an official letter with a red seal, opened envelope on the desk, tense atmosphere.",
    'soc_insula_team': "Foreground: a female doctor in a white coat calmly talking with a patient. Background: a small creative team (two young professionals) filming her with a smartphone on a tripod and a ring light.",
    # ---------------- VIDEO 2 – SITO
    'sito_divano_notte': "Night time, a man in his forties sitting on a sofa in a dark living room, lit only by his smartphone screen, one hand on his chest, slightly worried expression. Window with city lights behind.",
    'sito_prenota_ok': "A relieved, smiling woman on a sofa at night looking at her smartphone, a soft green glow from the screen, cosy blanket, warm lamp.",
    'sito_telefono_attesa': "A frustrated patient standing in front of a closed medical office door, phone pressed to the ear, waiting on hold. A small clock on the wall. Corridor with faceted walls.",
    'sito_dorme': "A doctor peacefully sleeping in a cosy bedroom at night; on the nightstand his smartphone lights up with a soft glow of incoming notifications.",
    'sito_cassetto': "An old wooden office drawer pulled open, full of dusty paper business cards and an old CRT monitor on the desk above, cobwebs, nostalgic grey light.",
    # ---------------- VIDEO 3 – BRAND
    'brand_studio_famiglia': "A young male family doctor in a white coat with a stethoscope standing in a bright suburban family clinic, friendly and confident, arms crossed, examination bed behind him.",
    'brand_reaction': "A young doctor in scrubs sitting on a sofa in a home studio, reacting with an exaggerated surprised expression to a medical TV drama playing on a big TV; a camera on a tripod and a ring light record him.",
    'brand_set_video': "A small home video studio: a camera on a tripod, a ring light, a microphone on an arm and a young doctor in a white coat sitting in front of it ready to record, calm and focused.",
    'brand_montatore': "A video editor with headphones at a desk with two large monitors showing a video editing timeline, coffee cup, focused, cosy evening light.",
    'brand_pazienti_parlano': "Two patients chatting animatedly and smiling in a clinic waiting room, one showing the other something on her smartphone.",
    'brand_visita': "A kind family doctor examining a child sitting on an examination bed with a stethoscope, the mother smiling next to them. Warm, bright clinic.",
}

def gen(sid, prompt, model):
    body = {"contents": [{"parts": [{"text": prompt + "\n\n" + STYLE}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
    req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                                 data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    d = json.load(urllib.request.urlopen(req, timeout=180))
    for c in d.get('candidates', []):
        for p in c.get('content', {}).get('parts', []):
            if 'inlineData' in p:
                ext = 'png' if 'png' in p['inlineData'].get('mimeType', '') else 'jpg'
                path = os.path.join(OUT, f'{sid}.{ext}')
                open(path, 'wb').write(base64.b64decode(p['inlineData']['data']))
                return path
    raise RuntimeError(json.dumps(d)[:400])

def main():
    os.makedirs(OUT, exist_ok=True)
    ids = sys.argv[1:] or [k for k in SCENES if not any(os.path.exists(os.path.join(OUT, f'{k}.{e}')) for e in ('png', 'jpg'))]
    for sid in ids:
        for m in MODELS:
            try:
                print(sid, '->', gen(sid, SCENES[sid], m), f'({m})', flush=True); break
            except urllib.error.HTTPError as e:
                print(sid, m, e.code, e.read()[:200], flush=True)
            except Exception as e:
                print(sid, m, 'ERR', e, flush=True)

if __name__ == '__main__':
    main()

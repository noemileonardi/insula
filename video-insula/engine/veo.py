"""Animate the chosen 3D scene stills with Veo (Gemini API, image-to-video).
Usage: python3 tools/veo.py [scene_id ...]      (no args = every scene without an .mp4)
The API key is injected by the environment proxy (network secret, header x-goog-api-key).
"""
import base64, json, os, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, 'assets', 'scenes')
API = 'https://generativelanguage.googleapis.com/v1beta'
MODELS = ['veo-3.1-fast-generate-preview', 'veo-3.0-fast-generate-001', 'veo-3.1-generate-preview']

STYLE = ' Keep the exact same characters, 3D animated film style, colours and room. Natural, subtle, realistic body movement, correct anatomy, smooth slow camera push-in. No text, no subtitles, no new people.'
MOTION = {
    'soc_telefono_muto': 'The doctor sighs, looks at the silent phone on the desk, taps his fingers on the desk and glances at the door.',
    'soc_ti_conosce': 'The doctor and the elderly woman shake hands warmly and smile at each other, she nods happily.',
    'soc_programma_tv': 'The couple on the sofa scroll their phones, the woman laughs and shows her screen to the man, he smiles.',
    'soc_ordine': 'The doctor reads the letter, his expression becomes worried, he lowers the paper slowly and sighs.',
    'soc_insula_team': 'The doctor smiles and starts talking to the camera on the tripod, gesturing naturally with one hand.',
    'sito_divano_notte': 'The man looks at his phone, puts a hand on his chest with a worried face, then starts typing on the phone.',
    'sito_prenota_ok': 'The woman taps her phone, smiles with relief and relaxes back into the sofa.',
    'sito_telefono_attesa': 'The man waits impatiently in the corridor, shifts his weight, checks his watch and looks at the closed door.',
    'sito_cassetto': 'Dust particles float in the light, the camera slowly moves closer to the dusty business cards in the drawer.',
    'brand_montatore': 'The video editor works at the computer, moves the mouse and types, the timeline on the monitors moves.',
    'brand_pazienti_parlano': 'The two women chat and laugh together, one shows her phone to the other who nods enthusiastically.',
    'brand_visita': 'The doctor gently talks to the little girl, she smiles and swings her legs, the doctor nods kindly.',
}

def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=120))

def animate(sid):
    img = base64.b64encode(open(os.path.join(SC, f'{sid}.png'), 'rb').read()).decode()
    body = {'instances': [{'prompt': MOTION[sid] + STYLE, 'image': {'bytesBase64Encoded': img, 'mimeType': 'image/png'}}],
            'parameters': {'aspectRatio': '9:16', 'durationSeconds': 8, 'personGeneration': 'allow_adult'}}
    for m in MODELS:
        try:
            op = call(f'{API}/models/{m}:predictLongRunning', body); break
        except urllib.error.HTTPError as e:
            print(sid, m, e.code, e.read()[:300], flush=True); op = None
    if not op: return
    while not op.get('done'):
        time.sleep(10); op = call(f"{API}/{op['name']}")
    if 'error' in op: print(sid, 'ERROR', op['error']); return
    uri = op['response']['generateVideoResponse']['generatedSamples'][0]['video']['uri']
    data = urllib.request.urlopen(urllib.request.Request(uri), timeout=300).read()
    out = os.path.join(SC, f'{sid}.mp4'); open(out, 'wb').write(data)
    print(sid, '->', out, flush=True)

if __name__ == '__main__':
    ids = sys.argv[1:] or [k for k in MOTION if os.path.exists(os.path.join(SC, f'{k}.png')) and not os.path.exists(os.path.join(SC, f'{k}.mp4'))]
    for sid in ids: animate(sid)

"""Generate the 3D scene images locally (CPU) with SDXL base + SDXL-Lightning 4-step UNet.
Licences: SDXL base 1.0 = CreativeML Open RAIL++-M, SDXL-Lightning = OpenRAIL++ (commercial use allowed).
Usage: python3 tools/scenes_local.py [scene_id ...] [--seed N] [--tag suffix]
"""
import os, sys, time
import torch
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes_ai import SCENES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'scenes')
import glob
BASE = glob.glob('/root/.cache/huggingface/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*')[0]

# short, anatomy-safe prompts: few people, waist-up framing, hands mostly hidden or resting
LOCAL = {
 'soc_agenda_piena': "waist-up portrait of a smiling female dermatologist in white coat, behind her a bright waiting room with patients seated, softly blurred",
 'soc_telefono_muto': "a lonely male doctor in white coat seated at his desk, waist-up, looking sadly at a silent desk telephone, empty office",
 'soc_ti_conosce': "a smiling female doctor in white coat welcoming a happy middle-aged man in a blue casual sweater at the door of her bright office, waist-up, only two people",
 'soc_programma_tv': "a young couple seated on a sofa in a cosy living room at evening, waist-up, smiling and looking at one smartphone together",
 'soc_ordine': "a worried male doctor in white coat at his desk, waist-up, reading an official letter, opened envelope on the desk",
 'soc_insula_team': "a female doctor in white coat speaking to a camera on a tripod with a ring light, cosy medical office, waist-up",
 'sito_divano_notte': "night, a worried man seated on a sofa in a dark living room, waist-up, face lit by his smartphone, city window behind",
 'sito_prenota_ok': "night, a relieved smiling woman on a sofa with a blanket, waist-up, looking at her glowing smartphone, warm lamp",
 'sito_telefono_attesa': "close-up of a bored frustrated man holding a smartphone to his ear with one hand, waiting on hold, other hand in pocket, corridor with closed door behind",
 'sito_dorme': "a man sound asleep in bed at night, eyes closed, head on pillow, arms under the blanket, a glowing smartphone lying on the nightstand",
 'sito_cassetto': "an old wooden desk drawer open with dusty paper business cards, old computer monitor, still life, no people",
 'brand_montatore': "a young video editor with headphones seated at a desk, back three-quarter view, two monitors with video editing timeline",
 'brand_pazienti_parlano': "two smiling women seated side by side in a clinic waiting room, waist-up, chatting, one shows her smartphone",
 'brand_visita': "a kind family doctor with stethoscope listening to the heart of a smiling child seated on an examination bed, waist-up",
}

STYLE = ("3d render, pixar style animated film still, stylized characters, medium shot, soft cinematic lighting, "
         "white faceted low-poly walls, clean modern interior, green and lilac accents")

def pipe():
    torch.set_num_threads(os.cpu_count())
    from accelerate import init_empty_weights
    with init_empty_weights():
        unet = UNet2DConditionModel.from_config(UNet2DConditionModel.load_config(BASE, subfolder='unet'))
    sd = load_file(glob.glob('/root/.cache/huggingface/hub/models--ByteDance--SDXL-Lightning/snapshots/*/sdxl_lightning_4step_unet.safetensors')[0])
    sd = {k: v.to(torch.bfloat16) for k, v in sd.items()}
    unet.load_state_dict(sd, assign=True); del sd
    p = StableDiffusionXLPipeline.from_pretrained(BASE, unet=unet, variant='fp16', torch_dtype=torch.bfloat16)
    p.vae.to(torch.float32)
    p.upcast_vae = lambda: None
    p.scheduler = EulerDiscreteScheduler.from_config(p.scheduler.config, timestep_spacing='trailing')
    p.set_progress_bar_config(disable=True)
    return p

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    seeds = [int(x) for x in sys.argv[sys.argv.index('--seeds') + 1].split(',')] if '--seeds' in sys.argv else [7]
    tag = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else ''
    if '--seeds' in sys.argv: args = [a for a in args if a != sys.argv[sys.argv.index('--seeds') + 1]]
    if tag: args = [a for a in args if a != tag]
    os.makedirs(OUT, exist_ok=True)
    ids = args or [k for k in SCENES if not any(os.path.exists(os.path.join(OUT, f'{k}.{e}')) for e in ('png', 'jpg'))]
    p = pipe()
    for sid, seed in [(i, sd) for i in ids for sd in seeds]:
        t = time.time()
        tag = f'_s{seed}' if len(seeds) > 1 else tag
        prompt = LOCAL.get(sid, SCENES[sid].split('.')[0]) + ', ' + STYLE
        g = torch.Generator().manual_seed(seed)
        with torch.inference_mode():
            lat = p(prompt=prompt, num_inference_steps=4, guidance_scale=0, width=768, height=1344, generator=g, output_type='latent').images
            img = p.vae.decode(lat.float() / p.vae.config.scaling_factor).sample
            im = p.image_processor.postprocess(img, output_type='pil')[0]
        path = os.path.join(OUT, 'cand' if len(seeds) > 1 else '', f'{sid}{tag}.png'); im.save(path)
        print(sid, '->', path, f'{time.time() - t:.0f}s', flush=True)

if __name__ == '__main__':
    main()

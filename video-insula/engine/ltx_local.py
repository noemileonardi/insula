"""Free, local image-to-video with LTX-Video 2B distilled (CPU).
Usage: python3 tools/ltx_local.py <scene_id> [--frames 65] [--seed 3]
Writes assets/scenes/cand_video/<scene_id>_s<seed>.mp4 (review before promoting to assets/scenes/<id>.mp4)
"""
import gc, glob, os, sys, time
import torch
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veo import MOTION

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, 'assets', 'scenes')
REPO = glob.glob('/root/.cache/huggingface/hub/models--Lightricks--LTX-Video-0.9.5/snapshots/*')[0]
CKPT = glob.glob('/root/.cache/huggingface/hub/models--Lightricks--LTX-Video/snapshots/*/ltxv-2b-0.9.8-distilled.safetensors')[0]
W, H = 512, 896
STYLE = ' 3D animated film style, smooth natural motion, the camera slowly pushes in, stable faces, correct anatomy.'

def encode(prompts):
    from transformers import T5EncoderModel, T5TokenizerFast
    tok = T5TokenizerFast.from_pretrained(REPO, subfolder='tokenizer')
    enc = T5EncoderModel.from_pretrained(REPO, subfolder='text_encoder', torch_dtype=torch.bfloat16, low_cpu_mem_usage=True)
    out = []
    for p in prompts:
        t = tok(p, padding='max_length', max_length=128, truncation=True, return_tensors='pt')
        with torch.inference_mode():
            e = enc(t.input_ids, attention_mask=t.attention_mask)[0]
        out.append((e, t.attention_mask))
    del enc; gc.collect()
    return out

def main():
    sid = sys.argv[1]
    frames = int(sys.argv[sys.argv.index('--frames') + 1]) if '--frames' in sys.argv else 65
    seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 3
    torch.set_num_threads(os.cpu_count())
    t0 = time.time()
    (pe, pm), (ne, nm) = encode([MOTION[sid] + STYLE, 'worst quality, deformed, distorted face, extra limbs, blurry, jittery'])
    print('text encoded', f'{time.time() - t0:.0f}s', flush=True)
    from diffusers import LTXConditionPipeline, LTXVideoTransformer3DModel, AutoencoderKLLTXVideo
    from diffusers.pipelines.ltx.pipeline_ltx_condition import LTXVideoCondition
    from diffusers.utils import export_to_video
    tr = LTXVideoTransformer3DModel.from_single_file(CKPT, torch_dtype=torch.bfloat16)
    vae = AutoencoderKLLTXVideo.from_single_file(CKPT, torch_dtype=torch.bfloat16)
    pipe = LTXConditionPipeline.from_pretrained(REPO, transformer=tr, vae=vae, text_encoder=None, tokenizer=None, torch_dtype=torch.bfloat16)
    img = Image.open(os.path.join(SC, f'{sid}.png')).convert('RGB').resize((W, H), Image.LANCZOS)
    cond = LTXVideoCondition(image=img, frame_index=0)
    g = torch.Generator().manual_seed(seed)
    t1 = time.time()
    with torch.inference_mode():
        video = pipe(conditions=[cond], prompt_embeds=pe, prompt_attention_mask=pm, negative_prompt_embeds=ne, negative_prompt_attention_mask=nm,
                     width=W, height=H, num_frames=frames, timesteps=[1000, 993, 987, 981, 975, 909, 725, 0.03], guidance_scale=1.0,
                     decode_timestep=0.05, decode_noise_scale=0.025, image_cond_noise_scale=0.0, generator=g, output_type='pil').frames[0]
    os.makedirs(os.path.join(SC, 'cand_video'), exist_ok=True)
    out = os.path.join(SC, 'cand_video', f'{sid}_s{seed}.mp4')
    export_to_video(video, out, fps=20)
    print(sid, '->', out, f'gen {time.time() - t1:.0f}s total {time.time() - t0:.0f}s', flush=True)

if __name__ == '__main__':
    main()

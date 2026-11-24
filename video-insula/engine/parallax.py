"""Turn a still 3D scene into a moving 2.5D shot: depth map + virtual camera (dolly-in, orbit, parallax).
Usage: python3 tools/parallax.py <scene_id> [seconds] [move]
moves: dolly (push in), orbit_l / orbit_r (sideways orbit), rise (crane up), drift
Output: assets/scenes/<scene_id>.mp4 (1080x1920, 30 fps)
"""
import os, subprocess, sys, glob
import numpy as np, cv2
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
DEPTH = glob.glob('/root/.cache/huggingface/hub/models--depth-anything--Depth-Anything-V2-Small-hf/snapshots/*')[0]
_pipe = None

def depth_of(img):
    global _pipe
    if _pipe is None:
        from transformers import pipeline
        _pipe = pipeline('depth-estimation', model=DEPTH, device='cpu')
    d = np.array(_pipe(img)['predicted_depth'].squeeze().cpu().numpy(), dtype=np.float32)
    d = cv2.resize(d, img.size, interpolation=cv2.INTER_CUBIC)
    d = (d - np.percentile(d, 2)) / (np.percentile(d, 98) - np.percentile(d, 2) + 1e-6)
    d = np.clip(d, 0, 1)
    # soften + slightly grow foreground so edges travel with their objects (less tearing)
    d = cv2.dilate(d, np.ones((9, 9), np.uint8))
    d = cv2.GaussianBlur(d, (0, 0), 6)
    return d

def ease(x):
    return x * x * (3 - 2 * x)

def render(sid, seconds=6.0, move='dolly'):
    src = os.path.join(ROOT, 'assets', 'scenes', f'{sid}.png')
    img = Image.open(src).convert('RGB')
    # work on an overscanned canvas so the camera never sees the borders
    OW, OH = int(W * 1.18), int(H * 1.18)
    big = img.resize((OW, OH), Image.LANCZOS)
    dep = depth_of(big)
    a = np.asarray(big, dtype=np.uint8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, H * 0.45
    n = int(seconds * FPS)
    out = os.path.join(ROOT, 'assets', 'scenes', f'{sid}.mp4')
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    # depth sampled on the output grid (approximation, fine for gentle moves)
    for i in range(n):
        t = ease(i / max(1, n - 1))
        zoom = {'dolly': 0.24, 'orbit_l': 0.12, 'orbit_r': 0.12, 'rise': 0.12, 'drift': 0.08}[move] * t
        px = {'orbit_l': -130, 'orbit_r': 130, 'drift': 50, 'dolly': 35}.get(move, 0) * (t - 0.5) * 2
        py = {'rise': -80, 'dolly': -20}.get(move, 0) * (t - 0.5) * 2
        # base mapping: output pixel -> overscan canvas
        bx = (xx - cx) + OW / 2
        by = (yy - cy) + OH * 0.45
        d = cv2.remap(dep, bx, by, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        s = 1 + zoom * (0.35 + 0.65 * d)            # near things grow faster than far things
        mx = OW / 2 + (xx - cx) / s - px * (d - 0.35)  # near things slide more than far things
        my = OH * 0.45 + (yy - cy) / s - py * (d - 0.35)
        frame = cv2.remap(a, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        ff.stdin.write(frame.tobytes())
    ff.stdin.close(); ff.wait()
    print(sid, '->', out, f'{seconds}s {move}')

if __name__ == '__main__':
    render(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 6.0, sys.argv[3] if len(sys.argv) > 3 else 'dolly')

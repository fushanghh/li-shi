import subprocess, math, numpy as np
from terrain import *
from PIL import Image
m = Map(97, 124, 20, 42, z=7)
S = 1
base = m.relief(scale=S)
size = (base.shape[1], base.shape[0])
riv = [(1.6 if r <= 3 else 0.8, s) for r, s in m.rivers(minrank=6)]
base = compose(base, glow_lines(size, riv, S, glow=5, alpha=.5))
hl = [(2.4, s) for r, s in m.rivers(names=['黄河', '长江'])]
HL = glow_lines(size, hl, S, glow=12, alpha=1)
# route: Chang'an -> Luoyang -> Kaifeng -> Hangzhou -> Fuzhou
route_ll = [(108.94, 34.34), (112.45, 34.62), (114.31, 34.80), (117.2, 32.9), (119.0, 31.6), (120.16, 30.27), (119.6, 28.6), (119.3, 26.08)]
FPS = 30; DUR = 8
p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', 'demo_map.mp4'], stdin=subprocess.PIPE)
for i in range(FPS * DUR):
    t = i / FPS
    e = 0.5 - 0.5 * math.cos(math.pi * min(1, t / DUR))
    # camera: wide -> zoom to Jiangnan
    cx0, cy0 = size[0] * 0.5, size[1] * 0.5
    cx1, cy1 = [v * S for v in m.xy(116.0, 30.0)]
    vw = size[0] * (1 - 0.38 * e)
    cx, cy = cx0 + (cx1 - cx0) * e, cy0 + (cy1 - cy0) * e
    hl_a = min(1, t / 1.5)
    full = compose(base, HL * hl_a)
    frame = camera(full, cx, cy, vw)
    k = 1920 / vw; vh = vw * 1080 / 1920
    x0 = min(max(cx - vw / 2, 0), size[0] - vw); y0 = min(max(cy - vh / 2, 0), size[1] - vh)
    pts = [((m.xy(*q)[0] * S - x0) * k, (m.xy(*q)[1] * S - y0) * k) for q in route_ll]
    prog = min(1, max(0, (t - 1.5) / 5))
    R, head = route_layer((1920, 1080), pts, prog, width=8, t=t)
    fr = Image.fromarray(compose(np.asarray(frame), R))
    if t > 6.3:
        fr = gold_label(fr, '南迁', int(pts[-1][0]), int(pts[-1][1]) - 80, alpha=min(1, (t - 6.3) / 0.6))
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()

import time; t=time.time()
from terrain import *
from PIL import Image, ImageDraw, ImageFont
m = Map(97, 124, 20, 42, z=6)
print(m.W, m.H, time.time()-t)
base = m.relief(scale=1)
print('relief', time.time()-t)
riv = m.rivers(minrank=6)
lines=[(1.3 if r<=3 else 0.7, s) for r,s in riv]
L1 = glow_lines((base.shape[1], base.shape[0]), lines, 1, glow=4, alpha=.55)
# highlight Yellow River & Yangtze
hl=[(2.2,s) for r,s in m.rivers(names=['黄河','长江'])]
L2 = glow_lines((base.shape[1], base.shape[0]), hl, 1, glow=10, alpha=1)
img = Image.fromarray(compose(base, L1, L2))
# crop 16:9 around center-east
W,H=img.size; print(W,H)
img.save('demo_full.png')

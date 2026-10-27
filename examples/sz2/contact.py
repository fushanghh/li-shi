# 每镜抽帧（默认 60% 处）拼总图
import sys, render as R
from PIL import Image
fr = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
only = sys.argv[2].split(',') if len(sys.argv) > 2 and sys.argv[2] != 'all' else None
ims = []
for i, x in enumerate(R.L):
    if only and x[0] not in only: continue
    s0, s1 = R.seg[i]; tt = R.starts[i] + R.dur[i] * fr
    if x[0] == 'die' and fr > 0.9: tt = R.starts[i] + R.dur[i] * 0.5
    sf = R.frame(tt); sf.write_to_png('/tmp/_f.png')
    ims.append((x[0], Image.open('/tmp/_f.png').convert('RGB').resize((480, 270))))
cols = 6; rows = (len(ims) + cols - 1) // cols
out = Image.new('RGB', (cols * 484, rows * 290), (30, 30, 30))
from PIL import ImageDraw
dr = ImageDraw.Draw(out)
for k, (nm, im) in enumerate(ims):
    x, y = (k % cols) * 484, (k // cols) * 290
    out.paste(im, (x + 2, y + 2)); dr.text((x + 6, y + 274), nm, fill=(255, 255, 0))
out.save(sys.argv[3] if len(sys.argv) > 3 else 'contact.png')

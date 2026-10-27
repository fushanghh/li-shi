import sys; sys.path.insert(0,'/workspace/work/mapref')
from terrain import *
m = Map(108.5, 124.5, 28.5, 42.5, z=7)
base = m.relief(scale=2)
size=(base.shape[1], base.shape[0])
riv=[(1.3 if r<=4 else 0.7, s) for r,s in m.rivers(minrank=6)]
base=compose(base, glow_lines(size, riv, 2, glow=4, alpha=.45))
hl=[(2.6,s) for r,s in m.rivers(names=['黄河','长江','Yellow','Yangtze'])]
base=compose(base, glow_lines(size, hl, 2, glow=10, alpha=.9))
Image.fromarray(base).save('china.png')
import json; json.dump(dict(z=7, px0=m.px0, py0=m.py0, W=size[0], H=size[1]), open('china.json','w'))
print(size)

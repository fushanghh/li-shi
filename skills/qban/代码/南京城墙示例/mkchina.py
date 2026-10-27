import sys; sys.path.insert(0,'/workspace/work/mapref')
from terrain import *
from shade import colorize
m = Map(108.5, 124.5, 28.5, 42.5, z=7)
d = ndimage.zoom(m.dem, 2, order=1); land = d > 0
d = ndimage.gaussian_filter(np.maximum(d, 0), 0.8)
base = colorize(d, ~land, 600, 6.0, 2500)
size = (base.shape[1], base.shape[0])
riv = [(1.3 if r <= 4 else 0.7, s) for r, s in m.rivers(minrank=6)]
base = compose(base, glow_lines(size, riv, 2, color=(.55, .80, 1.0), glow=4, alpha=.45))
hl = [(2.6, s) for r, s in m.rivers(names=['黄河', '长江', 'Yellow', 'Yangtze'])]
base = compose(base, glow_lines(size, hl, 2, color=(.55, .80, 1.0), glow=10, alpha=.9))
Image.fromarray(base).save('china.png')
Image.fromarray(base).resize((size[0]//4, size[1]//4)).save('/tmp/ref/china_small.png')
print(size)

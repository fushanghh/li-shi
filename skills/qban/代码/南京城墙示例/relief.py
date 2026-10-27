import numpy as np
from scipy import ndimage
from PIL import Image
from shade import colorize
S = 2
dem = np.load('dem.npy').astype(np.float32)
water = ndimage.binary_opening(ndimage.gaussian_filter(dem, 1.5) < 3.5, iterations=2)
lab, nl = ndimage.label(water); sz = ndimage.sum(water, lab, range(1, nl+1))
water = np.isin(lab, [i+1 for i, z in enumerate(sz) if z > 4000])
d = ndimage.gaussian_filter(dem, 1.3)
d = ndimage.zoom(d, S, order=3)
water = ndimage.zoom(water.astype(np.float32), S, order=1) > 0.5
img = colorize(d, water, 9.5, 2.5, 300)
Image.fromarray(img).save('relief.png')
Image.fromarray(img).resize((img.shape[1]//3, img.shape[0]//3)).save('/tmp/ref/rel_small.png')

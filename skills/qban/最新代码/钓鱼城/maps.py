"""Regenerate wide.png / local.png with the new gray-brown / blue-gray palette (no gold)."""
import sys, json, math, numpy as np
sys.path.insert(0, '.')
from terrain import Map, shade_rgb, paint_water
from scipy import ndimage
from PIL import Image
import cairocffi as cairo


def draw_lines(rgb, lines):
    """lines: list of (width, [(x,y)...]) in image px; blue river with lighter core"""
    H, W = rgb.shape[:2]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(surf)
    cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col, segs in lines:
        for seg in segs:
            cr.move_to(*seg[0]); [cr.line_to(*p) for p in seg[1:]]
            cr.set_source_rgba(*col, 1); cr.set_line_width(lw); cr.stroke()
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data()).astype(np.float32)
    al = a[..., 3:4] / 255
    src = a[..., [2, 1, 0]] / np.maximum(al, 1e-6)
    return rgb * (1 - al) + src * al


# ---------------- wide: Sichuan basin
m = Map(102.0, 115.0, 28.5, 36.2, z=8)
d = m.dem.copy(); d = np.where(d < -500, np.nanmedian(d), d)
mpp = 156543.0 * math.cos(math.radians(31)) / 2 ** 8
rgb, h = shade_rgb(d, mpp, exag=3.2, sm=0.6)
# basin plains a bit warmer/lighter
riv = m.rivers(minrank=9)
big = ['嘉陵江', '长江', '金沙江', '汉水', '岷江']
small = [s for r, s in riv]
hl = [s for r, s in m.rivers(names=big)]
rgb = draw_lines(rgb, [(6.0, (0.10, 0.22, 0.40), small), (3.6, (0.32, 0.60, 0.90), small),
                       (14.0, (0.10, 0.22, 0.40), hl), (9.0, (0.28, 0.60, 0.95), hl), (3.0, (0.70, 0.88, 1.0), hl)])
img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)); img.save('wide.png'); print('wide', img.size)

# ---------------- local: Hechuan confluence (z13, scale 2)
d0 = np.load('dem_hc.npy'); d0 = np.where(d0 < -500, np.nanmedian(d0), d0)
sc = 2
d2 = ndimage.zoom(d0, sc, order=1)
mpp = 156543.0 * math.cos(math.radians(30)) / 2 ** 13 / sc
rgb2, _ = shade_rgb(d2, mpp, exag=2.4, sm=1.2)
rgb2 = paint_water(rgb2, ndimage.grey_opening(d2, size=(15, 15)), 200)
img2 = Image.fromarray(np.clip(rgb2, 0, 255).astype(np.uint8)); img2.save('local.png'); print('local', img2.size)
img.resize((1183, 831)).save('/tmp/wide_s.png'); im = img2.copy(); im.thumbnail((1400, 1100)); im.save('/tmp/local_s.png')

import sys, json, math
sys.path.insert(0, '.')
import numpy as np
import cairocffi as cairo
from terrain import Map
from PIL import Image
m = Map(111.0, 121.0, 33.0, 38.6, z=8)
base = m.relief(scale=1)
Hh, Ww = base.shape[:2]
# rivers drawn as clear blue lines (no screen-glow)
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Ww, Hh); cr = cairo.Context(surf)
cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)
for rank, seg in m.rivers(minrank=9):
    big = rank <= 3
    for lw, col in ((5.0 if big else 3.0, (0.10, 0.22, 0.40, 0.55)), (3.0 if big else 1.6, (0.30, 0.62, 0.95, 1.0))):
        cr.move_to(*seg[0]); [cr.line_to(*p) for p in seg[1:]]
        cr.set_line_width(lw); cr.set_source_rgba(*col); cr.stroke()
a = np.ndarray((Hh, Ww, 4), np.uint8, surf.get_data()).astype(np.float32)
al = a[..., 3:4] / 255; rgb = a[..., [2, 1, 0]]  # premultiplied BGRA
out = base.astype(np.float32) * (1 - al) + rgb
img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)); img.save('wide.png'); print(img.size)
P = {'大梁': (114.35, 34.80), '新郑': (113.73, 34.40), '临淄': (118.30, 36.85), '邯郸': (114.49, 36.61),
     '大名说': (115.15, 36.28), '莘县说': (115.67, 36.23), '郯城说': (118.37, 34.61)}
json.dump({'wide': dict(size=img.size, pts={k: m.xy(*v) for k, v in P.items()})}, open('maps.json', 'w'), ensure_ascii=False, indent=1)

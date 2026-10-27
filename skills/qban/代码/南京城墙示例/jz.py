from hist import *
import json, math
import numpy as np
from PIL import Image

# ------------------------------------------------------------ extra props
def moon(c, x, y, r, a=1.0):
    if a <= 0: return
    pat = cairo.RadialGradient(x, y, r * 0.5, x, y, r * 3)
    pat.add_color_stop_rgba(0, *CREAM, 0.35 * a); pat.add_color_stop_rgba(1, *CREAM, 0)
    c.set_source(pat); c.arc(x, y, r * 3, 0, 6.283); c.fill()
    rgba(c, (0.98, 0.93, 0.80), a); c.arc(x, y, r, 0, 6.283); c.fill()


def torch(c, x, y, T, a=1.0, s=1.0):
    if a <= 0: return
    rgba(c, BROWN, a); c.rectangle(x - 4 * s, y, 8 * s, 60 * s); c.fill()
    pat = cairo.RadialGradient(x, y - 10 * s, 0, x, y - 10 * s, 90 * s)
    pat.add_color_stop_rgba(0, 1, 0.7, 0.3, 0.45 * a); pat.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
    c.set_source(pat); c.arc(x, y - 10 * s, 90 * s, 0, 6.283); c.fill()
    for col, sc in ((REDL, 1.0), ((1, .65, .2), .65), ((1, .9, .5), .35)):
        h = 46 * s * sc * (0.85 + 0.15 * math.sin(T * 11 + x)); w = 18 * s * sc
        sw = 4 * math.sin(T * 8 + x)
        c.move_to(x - w, y); c.curve_to(x - w, y - h * .5, x + sw, y - h * .8, x + sw, y - h)
        c.curve_to(x + sw, y - h * .8, x + w, y - h * .5, x + w, y); c.close_path(); rgba(c, col, .9 * a); c.fill()


def horse(c, x, yf, s=1.0, T=0, a=1.0, face=1, rider=True, col=(0.36, 0.24, 0.16)):
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    g = T * 14
    rgba(c, tuple(v * 0.8 for v in col), a); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, (lx, ph) in enumerate(((-70, 0), (-50, 2.2), (55, 1.1), (75, 3.3))):
        sw = math.sin(g + ph) * 22
        c.move_to(lx, -95); c.line_to(lx + sw, -45); c.line_to(lx + sw * 0.6, -4); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    rgba(c, col, a)
    c.save(); c.translate(0, -115); c.scale(105, 38); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    c.move_to(50, -140); c.line_to(110, -220); c.line_to(160, -205); c.line_to(110, -100); c.close_path(); c.fill()
    c.save(); c.translate(150, -195); c.rotate(0.7); c.scale(46, 22); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    rgba(c, INKC, a); c.move_to(108, -212); c.line_to(80, -150); c.line_to(95, -150); c.line_to(122, -205); c.fill()
    c.move_to(-100, -125); c.curve_to(-140, -110, -150, -70, -140, -50); c.set_line_width(10); c.stroke()
    if rider:
        rgba(c, GOLD, a); c.move_to(-25, -140); c.line_to(30, -140); c.line_to(25, -235); c.line_to(-15, -235); c.close_path(); c.fill()
        rgba(c, RED, a); c.move_to(-15, -230); c.line_to(-80 - 10 * math.sin(T * 9), -200); c.line_to(-10, -190); c.close_path(); c.fill()
        rgba(c, SKIN, a); c.arc(6, -258, 22, 0, 6.283); c.fill()
        rgba(c, INKC, a); c.arc(6, -264, 24, math.pi, 2 * math.pi); c.fill(); c.rectangle(-22, -268, 56, 8); c.fill()
    c.restore()


def ingot(c, x, y, s=1.0, a=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-60, -20); c.curve_to(-50, 10, 50, 10, 60, -20); c.curve_to(40, 25, -40, 25, -60, -20); c.close_path()
    c.move_to(-46, -14); c.curve_to(-30, 18, 30, 18, 46, -14); c.line_to(30, -24); c.curve_to(10, -10, -10, -10, -30, -24); c.close_path()
    pat = cairo.LinearGradient(0, -30, 0, 25); pat.add_color_stop_rgba(0, *GOLDL, a); pat.add_color_stop_rgba(1, *GOLDD, a)
    c.set_source(pat); c.fill()
    rgba(c, GOLDL, a); c.save(); c.translate(0, -22); c.scale(24, 14); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    c.restore()


def eye(c, x, y, s=1.0, op=1.0, a=1.0, col=GOLDL):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s * max(0.05, op))
    c.move_to(-60, 0); c.curve_to(-25, -38, 25, -38, 60, 0); c.curve_to(25, 38, -25, 38, -60, 0); c.close_path()
    rgba(c, CREAM, a); c.fill()
    rgba(c, INKC, a); c.arc(0, 0, 20, 0, 6.283); c.fill()
    rgba(c, col, a); c.arc(0, 0, 9, 0, 6.283); c.fill()
    c.restore()


def doc(c, x, y, w, h, a=1.0, title='路引', fields=(), t=99, sealch=None, seal_t=99):
    """vertical official document, fields written right-to-left as columns"""
    if a <= 0: return
    rgba(c, (0, 0, 0), 0.35 * a); c.rectangle(x - w / 2 + 10, y - h / 2 + 12, w, h); c.fill()
    rgba(c, (0.95, 0.91, 0.80), a); c.rectangle(x - w / 2, y - h / 2, w, h); c.fill()
    rgba(c, RED, 0.8 * a); c.set_line_width(4); c.rectangle(x - w / 2 + 14, y - h / 2 + 14, w - 28, h - 28); c.stroke()
    n = len(fields) + 1
    colw = (w - 60) / n
    xs = [x + w / 2 - 30 - colw * (k + 0.5) for k in range(n)]
    for k, ch in enumerate(title):
        label(c, ch, xs[0], y - h / 2 + 90 + k * 76, 62, RED, a)
    for i, f in enumerate(fields):
        aa = a * fin(t, 0.3 + i * 0.35, 0.3)
        for k, ch in enumerate(f):
            label(c, ch, xs[i + 1], y - h / 2 + 80 + k * 46, 36, INKC, aa)
    if sealch:
        p = pop(t, seal_t, 0.35)
        if p > 0:
            seal(c, sealch, x - w / 2 + 110, y + h / 2 - 110, 1.6 - 0.6 * p, clamp(p * 1.5), -0.12)


def lock(c, x, y, s=1.0, a=1.0, closed=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, GOLDL, a); c.set_line_width(14)
    c.arc(0, -40 - 22 * (1 - closed), 32, math.pi, 0); c.stroke()
    pat = cairo.LinearGradient(-50, 0, 50, 0); pat.add_color_stop_rgba(0, *GOLDD, a); pat.add_color_stop_rgba(0.4, *GOLDL, a); pat.add_color_stop_rgba(1, *GOLDD, a)
    rrect(c, -50, -45, 100, 80, 10); c.set_source(pat); c.fill()
    rgba(c, INKC, a); c.arc(0, -12, 9, 0, 6.283); c.fill(); c.rectangle(-4, -12, 8, 26); c.fill()
    c.restore()


def candle(c, x, yf, h, T, a=1.0):
    if a <= 0: return
    rgba(c, (0.92, 0.88, 0.80), a); c.rectangle(x - 40, yf - h, 80, h); c.fill()
    rgba(c, (0.80, 0.74, 0.62), a); c.rectangle(x - 40, yf - h, 18, h); c.fill()
    torch(c, x, yf - h, T, a, 1.4)


def neighbors_grid(c, x0, y0, cols, rows, dx, dy, s, t, t0, a=1.0, hl=None, plaque=None):
    for r in range(rows):
        for k in range(cols):
            i = r * cols + k
            p = fin(t, t0 + i * 0.03, 0.3)
            wall = (0.86, 0.82, 0.74)
            if hl and i in hl:
                wall = lerpc(wall, (1, 0.83, 0.45), hl[i])
            house(c, x0 + k * dx, y0 + r * dy, s * (0.6 + 0.4 * p), a * p, plaque=None, wall=wall)


def node(c, x, y, txt, a=1.0, red=0.0, r=46):
    if a <= 0: return
    col = lerpc(GOLD, REDL, red)
    pat = cairo.RadialGradient(x, y, 0, x, y, r * 2.2)
    pat.add_color_stop_rgba(0, *col, 0.35 * a * (0.4 + red)); pat.add_color_stop_rgba(1, *col, 0)
    c.set_source(pat); c.arc(x, y, r * 2.2, 0, 6.283); c.fill()
    rgba(c, (0.16, 0.11, 0.07), a); c.arc(x, y, r, 0, 6.283); c.fill()
    rgba(c, col, a); c.set_line_width(5); c.arc(x, y, r, 0, 6.283); c.stroke()
    mini(c, x, y + 22, 0.95, lerpc(CREAM, REDL, red), a)
    label(c, txt, x, y + r + 40, 30, lerpc(GOLDL, REDL, red), a)


def link(c, x0, y0, x1, y1, a=1.0, col=GOLD, w=4):
    if a <= 0: return
    rgba(c, col, a); c.set_line_width(w); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()


def goldbar_label(c, s, x, y, size=52, a=1.0, bar=None):
    if a <= 0: return
    bar = bar or size * len(s) * 0.9 + 80
    for dy in (-size * 0.95, size * 0.45):
        pat = cairo.LinearGradient(x - bar, 0, x + bar, 0)
        for u, al in ((0, 0), (0.25, 1), (0.75, 1), (1, 0)):
            pat.add_color_stop_rgba(u, *GOLDL, al * a)
        c.set_source(pat); c.rectangle(x - bar, y + dy, 2 * bar, 3); c.fill()
    rich(c, s, x, y, size, 99, (1, 0.94, 0.80), a, 'c', 0, 0.01)


def glowline(c, pts, a=1.0, w=7, col=(1, 0.97, 0.9), halo=GOLDL, dash_t=None):
    if a <= 0 or len(pts) < 2: return
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for ww, al, cc in ((w * 5, 0.10, halo), (w * 2.6, 0.22, halo), (w, 0.95, col)):
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]
        rgba(c, cc, al * a); c.set_line_width(ww); c.stroke()
    if dash_t is not None:
        c.set_dash([w * 1.2, w * 1.2], -dash_t * 40)
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]
        rgba(c, (0.7, 0.55, 0.3), 0.6 * a); c.set_line_width(w * 0.5); c.stroke(); c.set_dash([])
    c.set_line_cap(cairo.LINE_CAP_BUTT)


def partial(pts, prog):
    if prog >= 1: return pts
    L = [0]
    for i in range(len(pts) - 1): L.append(L[-1] + math.dist(pts[i], pts[i + 1]))
    cut = L[-1] * max(0, prog); out = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= cut: out.append(pts[i])
        else:
            f = (cut - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append((pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f)); break
    return out


# ------------------------------------------------------------ gold relief map
_MB = None


def _load():
    global _MB, META
    if _MB is None:
        _MB = Image.open('/workspace/work/ybs/mapbase.png').convert('RGB')
        META = json.load(open('/workspace/work/ybs/mapmeta.json'))
    return _MB, META


def ll2b(lon, lat):
    _, m = _load(); z = m['z']
    x = (lon + 180) / 360 * 2 ** z * 256 - m['px0']
    r = math.radians(lat)
    y = (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** z * 256 - m['py0']
    return x, y


def draw_map(c, lon, lat, vw):
    img, m = _load()
    cx, cy = ll2b(lon, lat)
    vh = vw * H / W
    x0 = min(max(cx - vw / 2, 0), m['W'] - vw); y0 = min(max(cy - vh / 2, 0), m['H'] - vh)
    fr = img.transform((W, H), Image.AFFINE, (vw / W, 0, x0, 0, vh / H, y0), resample=Image.BILINEAR)
    a = np.asarray(fr)
    bgra = np.empty((H, W, 4), np.uint8); bgra[..., 0] = a[..., 2]; bgra[..., 1] = a[..., 1]; bgra[..., 2] = a[..., 0]; bgra[..., 3] = 255
    buf = bytearray(bgra.tobytes())
    s = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_ARGB32, W, H, W * 4)
    c.set_source_surface(s, 0, 0); c.paint()
    k = W / vw

    def f(lo, la):
        bx, by = ll2b(lo, la)
        return (bx - x0) * k, (by - y0) * k
    return f

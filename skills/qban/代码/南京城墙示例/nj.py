"""Nanjing Ming wall: gold relief map of Nanjing + overlays, plan diagrams, cross sections."""
from songci import *
import json

Z = 13; S = 2


def _lx(lon, z): return (lon + 180) / 360 * 2 ** z * 256


def _ly(lat, z):
    r = math.radians(lat)
    return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** z * 256


PX0, PY0 = _lx(118.56, Z), _ly(32.14, Z)


def ll(lon, lat):
    return ((_lx(lon, Z) - PX0) * S, (_ly(lat, Z) - PY0) * S)


_RS = {}


def _surf(name):
    if name not in _RS:
        _RS[name] = cairo.ImageSurface.create_from_png(name)
    return _RS[name]


def nmap(c, lon, lat, vw, bright=0.0):
    """paint Nanjing relief, leave context transformed into relief px. caller restores. returns k"""
    k = W / vw; cx, cy = ll(lon, lat)
    c.save(); c.translate(W / 2, H / 2); c.scale(k, k); c.translate(-cx, -cy)
    c.set_source_surface(_surf('relief.png'), 0, 0); c.get_source().set_filter(cairo.FILTER_BILINEAR); c.paint()
    return k


CJ = json.load(open('china.json'))


def cll(lon, lat):
    return ((_lx(lon, CJ['z']) - CJ['px0']) * 2, (_ly(lat, CJ['z']) - CJ['py0']) * 2)


def cmap(c, lon, lat, vw):
    k = W / vw; cx, cy = cll(lon, lat)
    c.save(); c.translate(W / 2, H / 2); c.scale(k, k); c.translate(-cx, -cy)
    c.set_source_surface(_surf('china.png'), 0, 0); c.get_source().set_filter(cairo.FILTER_BILINEAR); c.paint()
    return k


# ---------------------------------------------------------------- geography (approximate, schematic)
WALL = [(118.7766, 32.0132), (118.7860, 32.0155), (118.7930, 32.0195), (118.7975, 32.0222), (118.8040, 32.0228),
        (118.8115, 32.0232), (118.8200, 32.0250), (118.8240, 32.0300), (118.8255, 32.0440), (118.8250, 32.0530),
        (118.8190, 32.0590), (118.8125, 32.0645), (118.8050, 32.0652), (118.7965, 32.0648), (118.7925, 32.0700),
        (118.7905, 32.0800), (118.7915, 32.0890), (118.7840, 32.0935), (118.7760, 32.0960), (118.7650, 32.0985),
        (118.7560, 32.0978), (118.7505, 32.0952), (118.7480, 32.0870), (118.7482, 32.0760), (118.7478, 32.0640),
        (118.7480, 32.0545), (118.7520, 32.0450), (118.7540, 32.0390), (118.7570, 32.0290), (118.7585, 32.0200),
        (118.7630, 32.0150), (118.7700, 32.0135), (118.7766, 32.0132)]
NORTH_IDX = (15, 24)   # wall indices of the northern stretch (神策门 → 定淮门) incl. 狮子山
GATES = [("正阳门", 118.8115, 32.0232), ("通济门", 118.7975, 32.0222), ("聚宝门", 118.7766, 32.0132),
         ("三山门", 118.7570, 32.0290), ("石城门", 118.7540, 32.0390), ("清凉门", 118.7480, 32.0545),
         ("定淮门", 118.7482, 32.0760), ("仪凤门", 118.7530, 32.0966), ("钟阜门", 118.7650, 32.0985),
         ("金川门", 118.7760, 32.0960), ("神策门", 118.7915, 32.0890), ("太平门", 118.8125, 32.0645),
         ("朝阳门", 118.8255, 32.0440)]
XWLAKE = [(118.7935, 32.0672), (118.8010, 32.0680), (118.8070, 32.0722), (118.8088, 32.0790), (118.8045, 32.0862),
          (118.7975, 32.0885), (118.7935, 32.0845), (118.7928, 32.0760)]
OLD = [(118.7766, 32.0137), (118.7632, 32.0154), (118.7588, 32.0202), (118.7573, 32.0290), (118.7543, 32.0390),
       (118.7600, 32.0560), (118.7800, 32.0582), (118.7930, 32.0542), (118.7972, 32.0225), (118.7860, 32.0159)]
GONG = (118.8145, 32.0335, 118.8222, 32.0450)
HUANG = (118.8062, 32.0262, 118.8236, 32.0512)
YANQUE = (118.8195, 32.0405, 0.0085, 0.0072)
QH_IN = [(118.7972, 32.0207), (118.7900, 32.0200), (118.7870, 32.0186), (118.7800, 32.0206), (118.7720, 32.0230),
         (118.7640, 32.0248), (118.7586, 32.0256)]
QH_OUT = [(118.8150, 32.0205), (118.7978, 32.0205), (118.7900, 32.0138), (118.7770, 32.0098), (118.7650, 32.0112),
          (118.7556, 32.0170), (118.7542, 32.0282), (118.7503, 32.0400), (118.7450, 32.0520), (118.7380, 32.0600),
          (118.7300, 32.0650)]
OUTER = [(118.7530, 32.1040), (118.7900, 32.1180), (118.8300, 32.1300), (118.8700, 32.1200), (118.9000, 32.0950),
         (118.9150, 32.0600), (118.8900, 32.0200), (118.8500, 31.9950), (118.8000, 31.9850), (118.7600, 31.9880),
         (118.7350, 32.0050)]
SQUARE = (118.7520, 32.0180, 118.8220, 32.0780)
HILLS = {"钟山": (118.8440, 32.0700), "狮子山": (118.7480, 32.1010), "石头城": (118.7395, 32.0560),
         "鸡鸣山": (118.7880, 32.0612), "覆舟山": (118.8060, 32.0610), "富贵山": (118.8300, 32.0565)}


def P(pts): return [ll(*p) for p in pts]


def path(c, pts, closed=False):
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    if closed: c.close_path()


def gstroke(c, pts, k, w=6, col=(1, 0.97, 0.9), halo=GOLDL, a=1.0, dash=None, closed=False):
    if a <= 0 or len(pts) < 2: return
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for ww, al, cc in ((w * 5, 0.10, halo), (w * 2.4, 0.25, halo), (w, 0.97, col)):
        if dash: c.set_dash([d / k for d in dash])
        path(c, pts, closed); rgba(c, cc, al * a); c.set_line_width(ww / k); c.stroke()
    c.set_dash([])


def wallline(c, k, prog=1.0, a=1.0, w=9, idx=None, col=(1, 0.96, 0.86), halo=GOLDL):
    pts = P(WALL if idx is None else WALL[idx[0]:idx[1] + 1])
    pts = partial(pts, prog)
    gstroke(c, pts, k, w, col, halo, a)
    if len(pts) > 1:   # brick ticks
        c.set_dash([4 / k, 7 / k]); path(c, pts); rgba(c, (0.45, 0.30, 0.12), 0.55 * a); c.set_line_width(w * 0.45 / k); c.stroke(); c.set_dash([])
    return pts


def poly(c, pts, k, fill, fa, edge=GOLDL, ea=1.0, w=3, dash=None):
    path(c, P(pts), True); rgba(c, fill, fa); c.fill()
    gstroke(c, P(pts), k, w, edge, edge, ea, dash, True)


def lake(c, k, a=1.0, pts=None):
    pts = pts or XWLAKE
    path(c, P(pts), True); rgba(c, (0.20, 0.44, 0.70), 0.95 * a); c.fill()
    gstroke(c, P(pts), k, 2.5, (0.80, 0.92, 1.0), (0.45, 0.72, 1.0), a, None, True)


def ellipse_pts(cx, cy, rx, ry, n=40):
    return [(cx + rx * math.cos(i * 6.283 / n), cy + ry * math.sin(i * 6.283 / n)) for i in range(n)]


def rect_pts(r):
    x0, y0, x1, y1 = r
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def rivers(c, k, a=1.0, prog=1.0):
    gstroke(c, partial(P(QH_OUT), prog), k, 3.5, (0.80, 0.92, 1.0), (0.45, 0.72, 1.0), a)
    gstroke(c, partial(P(QH_IN), prog), k, 2.6, (0.80, 0.92, 1.0), (0.45, 0.72, 1.0), 0.85 * a)


def mlabel(c, s_, lon, lat, k, a=1.0, size=40, col=TXT, bar=True, t=99, dy=0):
    """label in map space, constant screen size, two thin gold bars"""
    if a <= 0: return
    x, y = ll(lon, lat)
    c.save(); c.translate(x, y + dy / k); c.scale(1 / k, 1 / k)
    fnt(c, size, FONT_X); w_ = c.text_extents(s_)[4]
    if bar:
        rgba(c, GOLDL, 0.9 * a)
        for yy in (-size * 1.05, size * 0.32):
            c.rectangle(-w_ / 2 - 26, yy, w_ + 52, 3); c.fill()
    text2(c, s_, 0, 0, size, t, col, a, 'c', 0.03, 0.22, FONT_X)
    c.restore()


def mdot(c, lon, lat, k, a=1.0, r=9, col=GOLDL):
    if a <= 0: return
    x, y = ll(lon, lat)
    rgba(c, col, 0.25 * a); c.arc(x, y, r * 2.4 / k, 0, 6.283); c.fill()
    rgba(c, (1, 0.97, 0.9), a); c.arc(x, y, r / k, 0, 6.283); c.fill()


def houses(c, k, a=1.0, n=150, seed=3):
    """tiny roofs scattered inside old city"""
    if a <= 0: return
    rs = np.random.RandomState(seed)
    pts = P(OLD)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    pth = None
    cnt = 0
    while cnt < n:
        x = rs.uniform(min(xs), max(xs)); y = rs.uniform(min(ys), max(ys))
        if not inside(x, y, pts): continue
        cnt += 1
        aa = a * clamp(a * 1.6 - cnt / n * 0.6)
        if aa <= 0: continue
        s_ = 7 / k * 1.0
        rgba(c, (0.95, 0.80, 0.50), 0.85 * aa)
        c.move_to(x - s_ * 1.4, y); c.line_to(x, y - s_); c.line_to(x + s_ * 1.4, y); c.close_path(); c.fill()
        rgba(c, (0.70, 0.55, 0.32), 0.85 * aa); c.rectangle(x - s_, y, s_ * 2, s_ * 0.9); c.fill()


def inside(x, y, pts):
    n = len(pts); ins = False; j = n - 1
    for i in range(n):
        xi, yi = pts[i]; xj, yj = pts[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi): ins = not ins
        j = i
    return ins


def fit_shape(pts, cx, cy, size):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    s_ = size / max(max(xs) - min(xs), max(ys) - min(ys))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (x - mx) * s_, cy + (y - my) * s_) for x, y in pts], s_, (mx, my)


def screen_glow(c, pts, w=7, col=(1, 0.96, 0.86), halo=GOLDL, a=1.0, closed=False, dash=None):
    if a <= 0 or len(pts) < 2: return
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for ww, al, cc in ((w * 5, 0.10, halo), (w * 2.4, 0.25, halo), (w, 0.97, col)):
        if dash: c.set_dash(dash)
        path(c, pts, closed); rgba(c, cc, al * a); c.set_line_width(ww); c.stroke()
    c.set_dash([])


def fc_plan(c, cx, cy, size, a=1.0, prog=1.0, t=99):
    """Beijing Forbidden City plan: moat, rectangular wall, halls on axis"""
    if a <= 0: return
    w_, h_ = size * 0.72, size
    m = 26
    rgba(c, (0.25, 0.42, 0.55), 0.8 * a); c.set_line_width(10)
    c.rectangle(cx - w_ / 2 - m, cy - h_ / 2 - m, w_ + 2 * m, h_ + 2 * m); c.stroke()
    pts = [(cx - w_ / 2, cy - h_ / 2), (cx + w_ / 2, cy - h_ / 2), (cx + w_ / 2, cy + h_ / 2), (cx - w_ / 2, cy + h_ / 2), (cx - w_ / 2, cy - h_ / 2)]
    screen_glow(c, partial(pts, prog), 7, (1, 0.6, 0.45), REDL, a)
    for k_, (yy, ww, hh) in enumerate(((0.36, 0.30, 0.07), (0.18, 0.40, 0.10), (0.02, 0.22, 0.06), (-0.12, 0.30, 0.08),
                                       (-0.30, 0.26, 0.07), (-0.42, 0.18, 0.05))):
        aa = a * fin(t, 0.6 + k_ * 0.12)
        rgba(c, (0.98, 0.78, 0.30), 0.9 * aa); c.rectangle(cx - w_ * ww / 2 / 0.72 * 0.72, cy + h_ * yy - h_ * hh / 2, w_ * ww / 0.72 * 0.72, h_ * hh); c.fill()
    rgba(c, (1, 0.9, 0.6), 0.35 * a); c.set_line_width(3); c.move_to(cx, cy - h_ / 2); c.line_to(cx, cy + h_ / 2); c.stroke()


def nj_plan(c, cx, cy, size, a=1.0, prog=1.0, w=7):
    pts = P(WALL)
    sp, s_, _ = fit_shape(pts, cx, cy, size)
    screen_glow(c, partial(sp, prog), w, (1, 0.96, 0.86), GOLDL, a)
    return sp


# ------------------------------------------------------------ flat pieces
def ridge_section(c, x0, x1, yb, peak, a=1.0):
    """hill silhouette; returns top y function"""
    rgba(c, (0.42, 0.34, 0.22), a)
    c.move_to(x0, yb)
    xm = (x0 + x1) / 2
    for i in range(0, 41):
        x = x0 + (x1 - x0) * i / 40
        u = (x - xm) / ((x1 - x0) / 2)
        y = yb - peak * max(0, 1 - u * u) ** 0.8
        c.line_to(x, y)
    c.line_to(x1, yb); c.close_path(); c.fill()
    rgba(c, (0.62, 0.50, 0.30), a); c.set_line_width(4)
    for i in range(0, 41):
        x = x0 + (x1 - x0) * i / 40
        u = (x - xm) / ((x1 - x0) / 2)
        y = yb - peak * max(0, 1 - u * u) ** 0.8
        (c.move_to if i == 0 else c.line_to)(x, y)
    c.stroke()


def wallblock(c, x, yb, w, h, a=1.0):
    rgba(c, (0.36, 0.33, 0.30), a); c.rectangle(x - w / 2, yb - h, w, h); c.fill()
    rgba(c, (0.52, 0.48, 0.44), a); c.rectangle(x - w / 2, yb - h, w, 10); c.fill()
    m = w / 7
    for k_ in range(4): c.rectangle(x - w / 2 + k_ * 2 * m, yb - h - m * 0.9, m, m * 0.9)
    c.fill()
    rgba(c, (0, 0, 0), 0.25 * a); c.set_line_width(1.5)
    for r in range(1, int(h / 16)):
        c.move_to(x - w / 2, yb - h + r * 16); c.line_to(x + w / 2, yb - h + r * 16)
    c.stroke()


def brick(c, x, y, s=1.0, a=1.0, txt=("袁州府", "宜春县", "窑匠"), t=99):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.45, 0.44, 0.42), a); c.rectangle(-200, -100, 400, 200); c.fill()
    rgba(c, (0.58, 0.57, 0.54), a); c.rectangle(-200, -100, 400, 14); c.fill()
    rgba(c, (0.25, 0.24, 0.22), a); c.set_line_width(5); c.rectangle(-150, -70, 300, 140); c.stroke()
    for i, s2 in enumerate(txt):
        text2(c, s2, 105 - i * 105, -10, 50, t - i * 0.25, (0.95, 0.92, 0.85), a, 'c', 0.05, 0.25, FONT_X)
    c.restore()


def badge(c, x, y, ch, lab, a=1.0, t=99, col=LACQ, r=92):
    if a <= 0: return
    s_ = back(clamp(t / 0.45)) if t < 0.45 else 1.0
    c.save(); c.translate(x, y); c.scale(max(0.01, s_), max(0.01, s_))
    rgba(c, col, a); c.arc(0, 0, r, 0, 6.283); c.fill()
    rgba(c, GOLDL, a); c.set_line_width(5); c.arc(0, 0, r - 10, 0, 6.283); c.stroke()
    text2(c, ch, 0, r * 0.32, r * 0.95, 99, (1, 0.95, 0.85), a, 'c', 0, 0.01, FONT_X)
    c.restore()
    text2(c, lab, x, y + r + 66, 46, t - 0.2, TXT, a, 'c', 0.03, 0.22, FONT_X)

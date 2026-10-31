# 1896 新艺术运动（慕夏海报）引擎 —— Python + cairo 移植自 huashu 10_nouveau
import math, random
import numpy as np, cairocffi as cairo
from scipy.ndimage import gaussian_filter

W, H = 1920, 1080
TAU = math.pi * 2
def hx(s): s = s.lstrip('#'); return tuple(int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))
C = dict(paper=hx('efe6cf'), gold=hx('c9a24a'), goldD=hx('9c7a2e'), line=hx('4e3320'), green=hx('b9cba0'), green2=hx('cfd3a6'),
         peach=hx('ecc9a2'), banner=hx('8fac80'), cream=hx('f6eedb'), poppy=hx('d9706a'), poppyD=hx('b4504b'), stem=hx('5f8a58'),
         leaf=hx('8fb38a'), skin=hx('f6dcc4'), skinD=hx('e8bfa2'), blush=hx('eaa59a'), red=hx('c2453a'), redD=hx('8e2c26'),
         teal=hx('5f9a8a'), pink=hx('e6aaa5'), pinkD=hx('d48e8c'), hair=hx('3a2a20'), hairHi=hx('6a4c38'), iron=hx('3d7763'))
LINE = C['line']

def cl(x, a=0, b=1): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t

# ---------- 线 ----------
def dense(pts, n=10):
    o = []; N = len(pts); g = lambda i: pts[max(0, min(N - 1, i))]
    for i in range(N - 1):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            o.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    o.append(tuple(pts[-1])); return o

def ribbon_path(c, pts, wf):
    n = len(pts); L = []; R = []
    for i in range(n):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1; dx /= d; dy /= d
        w = wf(i / max(1, n - 1)) / 2
        L.append((pts[i][0] - dy * w, pts[i][1] + dx * w)); R.append((pts[i][0] + dy * w, pts[i][1] - dx * w))
    c.move_to(*L[0])
    for p in L[1:]: c.line_to(*p)
    for p in R[::-1]: c.line_to(*p)
    c.close_path()

def swellW(wmax, wend=1.0): return lambda q: wend + (wmax - wend) * math.sin(math.pi * q)
def spiral(cx, cy, r0, a0, turns, d=1, n=28):
    return [(cx + math.cos(a0 + d * q * turns * TAU) * r0 * (1 - q * 0.85), cy + math.sin(a0 + d * q * turns * TAU) * r0 * (1 - q * 0.85)) for q in [i / n for i in range(n + 1)]]

def ink(c, pts, wmax, col=LINE, wend=1.0, n=8, a=1):
    c.set_source_rgba(*col, a); ribbon_path(c, dense(pts, n), swellW(wmax, wend)); c.fill()

def smooth_path(c, pts, closed=True, n=8):
    d = dense(pts + ([pts[0], pts[1]] if closed else []), n)
    if closed: d = d[:len(d) - n]
    c.move_to(*d[0])
    for p in d[1:]: c.line_to(*p)
    if closed: c.close_path()

def shape(c, pts, fill, lw=2.2, col=LINE, closed=True, n=8):
    c.new_path(); smooth_path(c, pts, closed, n)
    if fill is not None: c.set_source_rgb(*fill); c.fill_preserve()
    c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()

def ell(c, x, y, rx, ry, fill, lw=2, rot=0, col=LINE):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, TAU); c.restore()
    if fill is not None: c.set_source_rgb(*fill); c.fill_preserve()
    if lw: c.set_source_rgb(*col); c.set_line_width(lw); c.stroke()
    else: c.new_path()

# ---------- 文字 ----------
def font(c, fam, size, bold=False):
    c.select_font_face(fam, 0, 1 if bold else 0); c.set_font_size(size)

def title(c, s, x, y, size, fam='LXGW WenKai', fill=C['cream'], stroke=LINE, sw=7, track=10, align='c'):
    font(c, fam, size, True)
    ws = [c.text_extents(ch)[4] + track for ch in s]; tw = sum(ws) - track
    x0 = x - tw / 2 if align == 'c' else (x if align == 'l' else x - tw)
    c.new_path(); xx = x0
    for ch, w in zip(s, ws): c.move_to(xx, y + size * 0.36); c.text_path(ch); xx += w
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_source_rgb(*stroke); c.set_line_width(sw); c.stroke_preserve(); c.set_source_rgb(*fill); c.fill()
    return tw

def label(c, s, x, y, size, col=LINE, fam='LXGW WenKai', align='c', a=1, bold=False):
    font(c, fam, size, bold); tw = c.text_extents(s)[4]
    x0 = x - tw / 2 if align == 'c' else (x if align == 'l' else x - tw)
    c.set_source_rgba(*col, a); c.move_to(x0, y + size * 0.36); c.show_text(s); return tw

# ---------- 底版 ----------
_cache = {}
def cached(key, fn):
    if key not in _cache:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); fn(cairo.Context(s)); s.flush(); _cache[key] = s
    return _cache[key]

def background(c, top=C['green'], mid=C['green2'], bot=C['peach'], dot=(120 / 255, 140 / 255, 100 / 255)):
    c.set_source_rgb(*C['paper']); c.paint()
    g = cairo.LinearGradient(0, 30, 0, 905); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(0.55, *mid); g.add_color_stop_rgb(1, *bot)
    c.set_source(g); c.rectangle(34, 32, W - 68, 875); c.fill()
    c.set_source_rgba(*dot, 0.38); c.set_line_width(1.6)
    for j, y in enumerate(range(62, 900, 54)):
        for x in range(64 + (j % 2) * 31, 1880, 62):
            c.new_path(); c.arc(x, y, 10, 0, TAU); c.stroke(); c.arc(x, y, 2.6, 0, TAU); c.fill()
    # 石版斑驳
    r = np.random.default_rng(3); nz = gaussian_filter(r.normal(0, 1, (135, 240)), 3); nz = (nz - nz.min()) / (nz.max() - nz.min())
    img = np.zeros((135, 240, 4), np.uint8); a = np.clip(nz * 1.4 - 0.25, 0, 1) * 60
    img[..., 0] = (40 * a / 255).astype(np.uint8); img[..., 1] = (70 * a / 255).astype(np.uint8); img[..., 2] = (90 * a / 255).astype(np.uint8); img[..., 3] = a.astype(np.uint8)
    s = cairo.ImageSurface.create_for_data(bytearray(img.tobytes()), cairo.FORMAT_ARGB32, 240, 135)
    c.save(); c.scale(W / 240, H / 135); c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_BILINEAR); c.paint_with_alpha(0.5); c.restore()

def mosaic_band(c, y=898):
    tiles = [hx(t) for t in ('f1ead6', '8fb08a', 'c9a24a', 'f1ead6', 'a9c39a', 'd98c8c', 'c9a24a', 'f1ead6', '6f9a80')]
    c.set_source_rgb(*LINE); c.rectangle(34, y, W - 68, 34); c.fill()
    k = 0
    for x in range(38, 1880, 24):
        c.set_source_rgb(*tiles[(k * 7 + (k >> 2)) % 9]); c.rectangle(x, y + 5, 20, 24); c.fill(); k += 1

def banner(c, text, sub=None, col=C['banner']):
    c.set_source_rgb(*col); c.rectangle(34, 934, W - 68, 114); c.fill()
    c.set_source_rgb(*LINE); c.rectangle(34, 932, W - 68, 3); c.fill(); c.rectangle(34, 1046, W - 68, 3); c.fill()
    for s in (1, -1):
        c.save()
        if s < 0: c.translate(W, 0); c.scale(-1, 1)
        c.set_source_rgb(*C['cream']); ribbon_path(c, dense([(100, 960), (112, 948), (128, 958), (200, 985), (300, 990), (400, 984)], 10), swellW(7, 1)); c.fill()
        c.set_source_rgb(*C['gold']); ribbon_path(c, dense([(130, 1010), (150, 1022), (180, 1004), (260, 985), (330, 975), (380, 975)], 10), swellW(8, 1)); c.fill()
        c.set_source_rgb(*C['cream']); ribbon_path(c, dense(spiral(112, 956, 16, math.pi, 0.9, 1), 2), lambda q: 4.5 - q * 3); c.fill()
        c.set_source_rgb(*C['gold']); ribbon_path(c, dense(spiral(142, 1012, 15, 0, 0.8, -1), 2), lambda q: 5 - q * 3.5); c.fill()
        c.set_source_rgb(*LINE); ribbon_path(c, dense([(200, 1030), (260, 1010), (340, 1000)], 10), swellW(3, .6)); c.fill()
        c.set_source_rgb(*hx('d07a86')); c.new_path(); c.arc(420, 993, 8, 0, TAU); c.fill()
        c.restore()
    if sub:
        title(c, text, W / 2, 978, 54, track=14, sw=6)
        label(c, sub, W / 2, 1024, 24, C['cream'], 'Noto Serif CJK SC')
    else:
        title(c, text, W / 2, 992, 64, track=16)

def gold_frame(c):
    c.set_source_rgb(*C['gold']); c.set_line_width(6); c.rectangle(22, 20, W - 44, H - 40); c.stroke()
    c.set_source_rgb(*LINE); c.set_line_width(2); c.rectangle(31, 29, W - 62, H - 58); c.stroke(); c.rectangle(16, 14, W - 32, H - 28); c.stroke()

def grain(c, amt=0.05):
    r = np.random.default_rng(7); n = r.random((H // 2, W // 2))
    img = np.zeros((H // 2, W // 2, 4), np.uint8); a = (n > 0.82) * 255 * amt * 2.5
    img[..., 0] = (32 * a / 255).astype(np.uint8); img[..., 1] = (51 * a / 255).astype(np.uint8); img[..., 2] = (78 * a / 255).astype(np.uint8); img[..., 3] = a.astype(np.uint8)
    s = cairo.ImageSurface.create_for_data(bytearray(img.tobytes()), cairo.FORMAT_ARGB32, W // 2, H // 2)
    c.save(); c.scale(2, 2); c.set_source_surface(s, 0, 0); c.paint(); c.restore()

# ---------- 光环 ----------
def halo(c, x, y, R, t=0, ring=hx('ebb8b2'), inner=hx('f3e3c8'), petal=hx('e9c9a0'), stud=C['gold'], motif='rose'):
    ell(c, x, y, R, R, ring, 3)
    ell(c, x, y, R * 0.86, R * 0.86, inner, 2.5)
    for i in range(18):
        a = i / 18 * TAU + 0.9 * t
        ell(c, x + math.cos(a) * R * 0.93, y + math.sin(a) * R * 0.93, 7, 7, stud, 1.8)
    n = 32 if motif == 'rose' else 16
    for i in range(n):
        a = i / n * TAU - 0.63 * t
        if motif == 'rose':
            px, py = x + math.cos(a) * R * 0.66, y + math.sin(a) * R * 0.66
            ell(c, px, py, R * 0.14, R * 0.055, petal, 1.6, a)
        else:   # 敦煌藻井莲花
            px, py = x + math.cos(a) * R * 0.62, y + math.sin(a) * R * 0.62
            c.save(); c.translate(px, py); c.rotate(a + math.pi / 2)
            shape(c, [(0, R * 0.2), (-R * 0.09, 0), (0, -R * 0.18), (R * 0.09, 0)], petal, 1.6)
            c.restore()
    ell(c, x, y, R * 0.46, R * 0.46, None, 2)

def arch_window(c, x0, x1, ybot, acy, ary, inner_fn, cols=('3f7fa0', 'e0b040', '6fb0a0', 'e9e0c4', '3f7fa0', 'd9a03a')):
    acx = (x0 + x1) / 2; arx = (x1 - x0) / 2
    def path(ins):
        c.new_path(); c.move_to(x0 + ins, ybot - ins); c.line_to(x0 + ins, acy)
        c.save(); c.translate(acx, acy); c.scale(arx - ins, ary - ins); c.arc(0, 0, 1, math.pi, TAU); c.restore()
        c.line_to(x1 - ins, ybot - ins); c.close_path()
    path(0); c.set_source_rgb(*C['cream']); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(3); c.stroke()
    path(30); c.save(); c.clip(); inner_fn(c); c.restore()
    path(30); c.set_source_rgb(*LINE); c.set_line_width(3.5); c.stroke()
    # 彩色小玻璃边带
    pts = []
    for y in np.arange(ybot - 22, acy, -4): pts.append((x0 + 22, y))
    for a in np.arange(math.pi, TAU + 1e-6, 0.02): pts.append((acx + math.cos(a) * (arx - 22), acy + math.sin(a) * (ary - 22)))
    for y in np.arange(acy, ybot - 22, 4): pts.append((x1 - 22, y))
    acc = 0; k = 0
    for i in range(1, len(pts)):
        acc += math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
        if acc >= 17:
            acc = 0; a = math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])
            c.save(); c.translate(*pts[i]); c.rotate(a); c.rectangle(-7, -7, 14, 14); c.set_source_rgb(*hx(cols[k % len(cols)])); c.fill_preserve()
            c.set_source_rgb(*LINE); c.set_line_width(1.5); c.stroke(); c.restore(); k += 1

# ---------- 慕夏剪影描边：离屏层 → 深棕错位垫底 ----------
def mucha_layer(c, drawfn):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); g = cairo.Context(s); drawfn(g); s.flush()
    sh = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); gs = cairo.Context(sh)
    gs.set_source_rgb(*LINE); gs.mask_surface(s, 0, 0)
    for dx, dy in ((-1.5, -1.5), (3.5, 4.5), (2, 2.5)):
        c.set_source_surface(sh, dx, dy); c.paint()
    c.set_source_surface(s, 0, 0); c.paint()

# ---------- 花 ----------
def poppy(c, x, y, r, t=0, ph=0, col=C['poppy'], colD=C['poppyD']):
    sw = math.sin(7.5 * t + ph) * 13 + math.sin(3.1 * t + 2 * ph) * 5
    ink(c, [(x, y + 260), (x + sw * 0.4, y + 130), (x + sw, y)], 7, C['stem'], 2)
    for k in range(5):
        a = k / 5 * TAU + ph
        ell(c, x + sw + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.45, r * 0.62, r * 0.5, col if k % 2 else colD, 2.2, a)
    ell(c, x + sw, y, r * 0.28, r * 0.28, hx('3f6a4a'), 2)

def lily(c, x, y, r, t=0, ph=0):
    sw = math.sin(6 * t + ph) * 9
    ink(c, [(x, y + 240), (x + sw * 0.4, y + 120), (x + sw, y)], 6, C['stem'], 2)
    for k in range(6):
        a = k / 6 * TAU + ph - math.pi / 2
        c.save(); c.translate(x + sw, y); c.rotate(a)
        shape(c, [(0, 0), (r * 0.35, -r * 0.18), (r, 0), (r * 0.35, r * 0.18)], hx('f7f2e6'), 2)
        c.restore()
    ell(c, x + sw, y, 6, 6, C['gold'], 1.5)

def vines(c, x, y, R, t=0, col=C['gold']):
    """光环两侧的鞭线卷草（慕夏标志）"""
    for sd in (-1, 1):
        for k, (dx, w) in enumerate(((0.0, 12), (0.12, 7))):
            pts = [(x + sd * R * (1.02 + dx + 0.10 * math.sin(q * 3.2 + t + k)), y + R * (0.95 - q * 1.7)) for q in [i / 14 for i in range(15)]]
            end = pts[-1]; pts += spiral(end[0] - sd * 20, end[1], 22, 0 if sd > 0 else math.pi, 1.1, -sd, 14)[1:]
            c.set_source_rgb(*(col if k == 0 else C['cream'])); ribbon_path(c, dense(pts, 4), lambda q: w * (1 - q * 0.8) + 1.2); c.fill()
            ink(c, pts, 1.4, LINE, 0.5, 4)
        for j in range(4):   # 叶
            q = 0.2 + j * 0.18; lx = x + sd * R * 1.06; ly = y + R * (0.95 - q * 1.7)
            c.save(); c.translate(lx, ly); c.rotate(sd * (0.8 + 0.2 * math.sin(t * 4 + j)))
            shape(c, [(0, 0), (sd * 22, -12), (sd * 46, 0), (sd * 22, 10)], C['leaf'], 1.8)
            c.restore()

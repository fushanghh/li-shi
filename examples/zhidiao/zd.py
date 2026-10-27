"""纸雕山河 —— 自有画风底层库
每个元素都是一张剪下来的纸：手剪毛边、纸纤维纹理、按层深投影；金箔只给焦点。"""
import cairocffi as cairo, numpy as np, math
from PIL import Image, ImageFilter

import os
W, H = int(os.environ.get('ZD_W', 1920)), int(os.environ.get('ZD_H', 1080))
rng = np.random.default_rng(3)
FONT = "Noto Serif CJK SC"

def hexc(h, a=1.0):
    h = h.lstrip('#'); return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

# ---- 调色：宣纸 + 矿物色 + 一点金 ----
P = dict(
    xuan='#efe4cc', xuan2='#e2d2ae', xuan3='#cdb98f', mo='#231c17', mo2='#3b3029',
    zhu='#b8332a', zhu2='#8e231d', qing='#2f5d6b', qing2='#1f3f4a', lv='#5f8a6a', lv2='#3f6650',
    zhe='#9c5b32', zhe2='#6e3c20', huang='#d9a441', jin='#caa04a', jin2='#f0d58a',
    skin='#ecc9a0', skin2='#d7a87a', hui='#7d7468', bai='#f6efe0', zi='#5b3f63', tie='#59646b', tie2='#3c444a')


import os
MODE = os.environ.get('ZD_MODE', 'paper')
if MODE == 'macaron':   # 学自用户给的成都玉林路等距插画：奶油底+马卡龙粉彩+深靛细描边+噪点白边
    P.update(xuan='#fbf8ef', xuan2='#f1ead8', xuan3='#f6d9bf', mo='#2b2a3a', mo2='#4a4860',
             zhu='#ef7474', zhu2='#d9535e', qing='#9cc3ec', qing2='#7aa5dc', lv='#a9d8c2', lv2='#5fb889',
             zhe='#f4bfa3', zhe2='#c98f80', huang='#f7d67a', jin='#f2b632', jin2='#fff0b0',
             skin='#fde3cf', skin2='#f2c4a8', hui='#bdbad0', bai='#ffffff', zi='#b9b3e6', tie='#bcc6e0', tie2='#8f99bb')
OUTLINE = MODE == 'macaron'

def rough(pts, amp=1.6, step=14, closed=True, seed=None):
    """手剪毛边：细分后小抖动"""
    r = np.random.default_rng(seed) if seed is not None else rng
    out = []; n = len(pts)
    for i in range(n if closed else n - 1):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        L = math.hypot(x1 - x0, y1 - y0); k = max(1, int(L / step))
        for j in range(k):
            u = j / k; out.append((x0 + (x1 - x0) * u + r.normal(0, amp), y0 + (y1 - y0) * u + r.normal(0, amp)))
    if not closed: out.append(pts[-1])
    return out


def ellipse_pts(cx, cy, rx, ry, n=40, a0=0, a1=2 * math.pi):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + (0 if a1 - a0 >= 2 * math.pi - 1e-6 else 1))]


class Layer:
    """一张纸。depth 越大离观众越近，投影越远越虚"""
    def __init__(self, depth=1.0):
        self.s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); self.c = cairo.Context(self.s); self.depth = depth
        self.c.set_line_join(cairo.LINE_JOIN_ROUND); self.c.set_line_cap(cairo.LINE_CAP_ROUND)

    def poly(self, pts, col, amp=1.4, holes=(), seed=None):
        c = self.c; pts = rough(pts, amp, seed=seed)
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path()
        for h in holes:   # 镂空（剪纸的灵魂）
            hp = rough(h, amp * 0.6, 8, seed=seed); c.move_to(*hp[0]); [c.line_to(*p) for p in hp[1:]]; c.close_path()
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); rgba = hexc(col) if isinstance(col, str) else col; c.set_source_rgba(*rgba)
        if OUTLINE and rgba[3] > 0.9:
            c.fill_preserve(); c.set_source_rgba(*hexc(P['mo'], 0.9)); c.set_line_width(2.4); c.stroke()
        else: c.fill()

    def ell(self, cx, cy, rx, ry, col, holes=(), amp=1.0):
        self.poly(ellipse_pts(cx, cy, rx, ry, max(16, int((rx + ry) / 3))), col, amp, holes)

    def line(self, pts, col, w=3, a=1.0):
        c = self.c; c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]
        c.set_source_rgba(*hexc(col, a)); c.set_line_width(w); c.stroke()

    def curve(self, pts, col, w=3, a=1.0):
        c = self.c; c.move_to(*pts[0])
        for i in range(1, len(pts) - 2, 3): c.curve_to(*pts[i], *pts[i + 1], *pts[i + 2])
        c.set_source_rgba(*hexc(col, a)); c.set_line_width(w); c.stroke()

    def text(self, s, x, y, size, col, a=1.0, anchor='c', bold=True, vertical=False, spacing=1.0):
        c = self.c; c.select_font_face(FONT, 0, 1 if bold else 0); c.set_font_size(size); c.set_source_rgba(*hexc(col, a))
        if vertical:
            for i, ch in enumerate(s):
                e = c.text_extents(ch); c.move_to(x - e[4] / 2, y + i * size * spacing); c.show_text(ch)
            return
        e = c.text_extents(s); w = e[4]
        dx = {'c': -w / 2, 'l': 0, 'r': -w}[anchor]; c.move_to(x + dx, y); c.show_text(s)

    def arr(self):
        a = np.frombuffer(self.s.get_data(), np.uint8).reshape(H, W, 4).astype(np.float32) / 255
        return a  # BGRA premultiplied


_grain = None
def grain():
    global _grain
    if _grain is None:
        g = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
        im = Image.fromarray(((g * 0.5 + 0.5).clip(0, 1) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
        g = np.asarray(im, np.float32) / 255 - 0.5
        fib = rng.normal(0, 1, (H, W // 8)).astype(np.float32)   # 横向长纤维
        fim = Image.fromarray(((fib * 0.5 + 0.5).clip(0, 1) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1))
        _grain = g * 0.06 + (np.asarray(fim, np.float32) / 255 - 0.5) * 0.05
    return _grain


def compose(layers, bg=None, light=(0.5, 0.25), vign=0.55, glow=()):
    """层叠：每层先加纸纹，再按深度投影"""
    if bg is None or MODE == 'macaron': bg = P['xuan']
    mac = MODE == 'macaron'
    out = np.zeros((H, W, 3), np.float32); b = hexc(bg); out[:] = (b[2], b[1], b[0])
    gr = grain()[..., None]
    for L in layers:
        a = L.arr(); al = a[..., 3:4]
        if al.max() == 0: continue
        d = L.depth
        sh = Image.fromarray((al[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2 + 3.5 * d))
        sh = np.asarray(sh, np.float32)[..., None] / 255
        dx, dy = int(4 + 7 * d), int(5 + 9 * d)
        sh = np.roll(np.roll(sh, dy, 0), dx, 1) * ((0.10 + 0.02 * d) if mac else (0.30 + 0.06 * d))
        out *= (1 - sh * 0.85)
        if not mac: out[..., 0] *= (1 - sh[..., 0] * 0.1)  # 投影偏暖
        rgb = a[..., :3] * (1 + gr * (0.4 if mac else 1))               # 纸纹
        # 纸边受光：上缘一丝亮线
        edge = np.clip(al - np.roll(al, 2, 0), 0, 1)
        rgb = rgb + edge * 0.12 * al
        out = out * (1 - al) + rgb
    # 顶光 + 暗角
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lx, ly = light[0] * W, light[1] * H
    r = np.sqrt(((xx - lx) / W) ** 2 + ((yy - ly) / H * 0.8) ** 2)
    if not mac: out *= (1.08 - vign * np.clip(r, 0, 1.2) ** 1.6)[..., None]
    for (gx, gy, gr_, ga) in glow:   # 金箔焦点光晕
        rr = np.sqrt((xx - gx) ** 2 + (yy - gy) ** 2) / gr_
        out += (np.exp(-rr ** 2) * ga)[..., None] * np.array([0.35, 0.65, 0.95], np.float32)
    out += gr * 0.6 * 0.5 * (0.3 if mac else 1)
    if mac:   # 噪点白边：越靠边越多白色颗粒
        dist = np.minimum.reduce([xx, W - 1 - xx, yy, H - 1 - yy]) / 110.0
        noise = np.random.default_rng(9).random((H, W)).astype(np.float32)
        m = (noise > np.clip(dist, 0, 1) ** 0.7)[..., None]
        out = np.where(m, np.array([0.937, 0.973, 0.984], np.float32), out)
    img = (np.clip(out, 0, 1) * 255).astype(np.uint8)[..., ::-1]
    return Image.fromarray(img)


# ---------------------------------------------------------------- 组件
def roof(L, cx, y, w, h, col=P['mo2'], ridge=P['zhu'], tiers=1):
    """飞檐：两端上翘"""
    for k in range(tiers):
        ww = w * (1 - 0.28 * k); yy = y - k * h * 1.05
        pts = [(cx - ww / 2 - ww * 0.06, yy - h * 0.55)]
        for i in range(9):
            u = i / 8; x = cx - ww / 2 + ww * u
            pts.append((x, yy - h * (0.95 - 0.35 * (2 * u - 1) ** 2)))
        pts += [(cx + ww / 2 + ww * 0.06, yy - h * 0.55), (cx + ww / 2 - ww * 0.04, yy), (cx - ww / 2 + ww * 0.04, yy)]
        L.poly(pts, col, 1.0)
        L.poly([(cx - ww * 0.42, yy - h * 0.98), (cx + ww * 0.42, yy - h * 0.98), (cx + ww * 0.42, yy - h * 1.08), (cx - ww * 0.42, yy - h * 1.08)], ridge, 0.6)
        for i in range(1, 12):   # 瓦垄刻线（镂空）
            x = cx - ww / 2 + ww * i / 12
            L.line([(x, yy - h * 0.15), (x, yy - h * 0.8)], P['mo'], 1.5, 0.6)


def wall(L, x0, x1, ytop, ybot, col=P['xuan3'], dark=P['zhe2'], merlon=True):
    L.poly([(x0, ybot), (x0, ytop), (x1, ytop), (x1, ybot)], col, 1.2)
    # 砖缝刻线
    hrow = 22; r = 0
    for y in np.arange(ytop + hrow, ybot, hrow):
        L.line([(x0 + 4, y), (x1 - 4, y)], dark, 1.4, 0.35)
        off = 0 if r % 2 else 24
        for x in np.arange(x0 + off, x1, 48): L.line([(x, y - hrow), (x, y)], dark, 1.2, 0.3)
        r += 1
    if merlon:
        for x in np.arange(x0, x1 - 20, 40): L.poly([(x, ytop), (x, ytop - 20), (x + 24, ytop - 20), (x + 24, ytop)], col, 0.8)


def flag(L, x, ytop, h, col, char, wave=0.0, pole=P['mo2'], left=False):
    L.line([(x, ytop), (x, ytop + h)], pole, 4)
    s = -1 if left else 1; fw, fh = 78, 96
    pts = [(x, ytop + 6)]
    for i in range(7):
        u = i / 6; pts.append((x + s * fw * u, ytop + 6 + 8 * math.sin(u * 3 + wave)))
    for i in range(7):
        u = 1 - i / 6; pts.append((x + s * fw * u, ytop + 6 + fh + 8 * math.sin(u * 3 + wave) - (10 if i == 0 else 0)))
    L.poly(pts, col, 0.8)
    L.text(char, x + s * fw / 2, ytop + 6 + fh / 2 + 18, 44, P['bai'])


def seal(L, s, x, y, size=150, rot=-0.08, col=P['zhu']):
    """朱砂印：结论盖章"""
    c = L.c; c.save(); c.translate(x, y); c.rotate(rot)
    L.poly([(-size / 2, -size / 2), (size / 2, -size / 2), (size / 2, size / 2), (-size / 2, size / 2)], col, 2.5)
    L.poly([(-size / 2 + 9, -size / 2 + 9), (size / 2 - 9, -size / 2 + 9), (size / 2 - 9, size / 2 - 9), (-size / 2 + 9, size / 2 - 9)], (0, 0, 0, 0), 1)
    c.set_line_width(4); c.set_source_rgba(*hexc(P['xuan'])); c.rectangle(-size / 2 + 10, -size / 2 + 10, size - 20, size - 20); c.stroke()
    if len(s) == 1: L.text(s, 0, size * 0.3, size * 0.72, P['xuan'])
    else:
        L.text(s[:2], 0, -size * 0.04, size * 0.36, P['xuan']); L.text(s[2:], 0, size * 0.36, size * 0.36, P['xuan'])
    # 印泥不匀：随机挖几个白点
    for _ in range(40):
        px, py = rng.uniform(-size / 2, size / 2, 2); c.arc(px, py, rng.uniform(1, 3.5), 0, 6.3)
        c.set_source_rgba(*hexc(P['xuan'], 0.7)); c.fill()
    c.restore()


def caption(L, s, hl=(), y=985):
    """自有字幕：左下撕纸条 + 墨字，关键词朱砂并画一道朱笔圈"""
    c = L.c; c.select_font_face(FONT, 0, 1); c.set_font_size(50)
    w = c.text_extents(s)[4]; x0 = 120
    L.poly([(x0 - 40, y - 62), (x0 + w + 50, y - 70), (x0 + w + 70, y + 26), (x0 - 30, y + 30)], P['bai'], 3.0)
    L.poly([(x0 - 40, y - 62), (x0 - 26, y - 62), (x0 - 18, y + 30), (x0 - 30, y + 30)], P['zhu'], 1.5)
    x = x0
    i = 0
    while i < len(s):
        hit = next((h for h in hl if s.startswith(h, i)), None)
        seg = hit or s[i]; ww = c.text_extents(seg)[4]
        c.move_to(x, y); c.set_source_rgba(*hexc(P['zhu'] if hit else P['mo'])); c.show_text(seg)
        if hit:   # 朱笔勾圈
            L.curve([(x - 6, y + 12), (x + ww * 0.3, y + 20), (x + ww * 0.7, y + 18), (x + ww + 8, y + 8)], P['zhu'], 3.5, 0.85)
        x += ww; i += len(seg)


def tag(L, s, x=1800, y=80):
    """右上：竖排年代地点签"""
    L.poly([(x - 34, y - 20), (x + 34, y - 20), (x + 34, y + 44 * len(s) + 10), (x - 34, y + 44 * len(s) + 10)], P['mo'], 1.2)
    L.text(s, x, y + 30, 36, P['jin2'], vertical=True, spacing=1.2)

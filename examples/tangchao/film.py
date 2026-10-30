# 唐朝风 · 敦煌女人社 成片
import sys, math, json, numpy as np, cairocffi as cairo
from lib import *
FPS = 30
BLUE = hx('6f9fd8'); GREENW = hx('8fc49a'); ORANGE = hx('e8643a')

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); k = 1.70158; x -= 1; return x * x * ((k + 1) * x + k) + 1
def lerp(a, b, u): return a + (b - a) * u
def lerpv(a, b, u): return tuple(lerp(p, q, u) for p, q in zip(a, b))
def font(c, size, bold=True): c.select_font_face('Noto Serif CJK SC', 0, 1 if bold else 0); c.set_font_size(size)
def tadv(c, s): return c.text_extents(s)[4]
def text(c, s, x, y, size, col=CREAM, a=1.0, align='l', shadow=0.55):
    font(c, size); w = tadv(c, s)
    if align == 'c': x -= w / 2
    elif align == 'r': x -= w
    if shadow: c.move_to(x + 3, y + 4); c.set_source_rgba(0.06, 0.03, 0.01, a * shadow); c.show_text(s)
    c.move_to(x, y); c.set_source_rgba(*col, a); c.show_text(s); return w
def vtext(c, s, x, y, size, col, a=1.0, gap=1.1):
    font(c, size)
    for i, ch in enumerate(s):
        w = tadv(c, ch); c.move_to(x - w / 2, y + i * size * gap); c.set_source_rgba(*col, a); c.show_text(ch)

# ---------- 缓存背景 ----------
_cache = {}
def cached(key, fn):
    if key not in _cache:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cc = cairo.Context(s); fn(cc); s.flush(); _cache[key] = s
    return _cache[key]
def paint_bg(c, key, fn): c.set_source_surface(cached(key, fn), 0, 0); c.paint()

def room_full(c): room(c)
def room_table(c): room(c); table(c)

def exterior(c):
    g = cairo.LinearGradient(0, 0, 0, 700); g.add_color_stop_rgb(0, *hx('c79a5a')); g.add_color_stop_rgb(1, *hx('e8c78a'))
    c.set_source(g); c.paint()
    glow(c, 1500, 260, 260, (1, 0.95, 0.75), 0.6); ell(c, 1500, 260, 70, 70, hx('fbe9b8'), 0)
    # 鸣沙山两层
    for col, base, amp, ph in ((hx('b98a52'), 520, 120, 0.3), (hx('a0703f'), 600, 90, 1.7)):
        c.new_path(); c.move_to(0, H)
        for x in range(0, W + 41, 40): c.line_to(x, base - amp * (0.5 + 0.5 * math.sin(x / 260 + ph)) * (0.6 + 0.4 * math.sin(x / 90 + ph * 2)))
        c.line_to(W, H); c.close_path(); c.set_source_rgb(*col); c.fill()
    # 地面
    c.rectangle(0, 760, W, 320); c.set_source_rgb(*hx('b08654')); c.fill()
    for y in (800, 870, 960): c.rectangle(0, y, W, 3); c.set_source_rgba(*INK, 0.18); c.fill()
    # 夯土院墙
    poly(c, [(0, 470), (1240, 470), (1240, 780), (0, 780)], hx('c9a06a'), 3)
    for y in range(500, 780, 46): stroke(c, [(0, y), (1240, y)], hx('a98250'), 2, False)
    # 屋檐
    poly(c, [(-20, 470), (1260, 470), (1200, 420), (40, 420)], hx('6e6a62'), 3)
    for x in range(40, 1200, 34): stroke(c, [(x, 424), (x - 4, 468)], hx('4e4a44'), 3, False)
    # 门
    poly(c, [(760, 520), (940, 520), (940, 780), (760, 780)], hx('6a3e22'), 3)
    stroke(c, [(850, 520), (850, 780)], INK, 3, False)
    for x in (830, 870): ell(c, x, 650, 7, 7, GOLD, 2)
    poly(c, [(740, 500), (960, 500), (960, 524), (740, 524)], hx('4a2a18'), 3)
    # 晾衣绳
    stroke(c, [(140, 560), (420, 585), (640, 560)], INK, 2)
    poly(c, [(190, 566), (260, 572), (258, 680), (192, 676)], hx('e9dfc6'), 2.6)
    poly(c, [(420, 585), (500, 580), (498, 690), (422, 692)], hx('6e8fb0'), 2.6)

def cave(c):
    c.set_source_rgb(*hx('2a1a10')); c.paint()
    c.new_path(); c.move_to(460, H); c.line_to(460, 380); c.curve_to(460, 120, 1460, 120, 1460, 380); c.line_to(1460, H); c.close_path()
    c.set_source_rgb(*hx('4a3220')); c.fill()
    for i in range(7):
        for j in range(5):
            x = 560 + i * 120; y = 820 - j * 64
            ell(c, x, y, 52, 26, hx('d9c49a') if (i + j) % 3 else hx('c8ad80'), 2.4)
            ell(c, x - 30, y, 10, 22, hx('8a6a40'), 2)
    # 壁上千佛小龛暗影
    for i in range(10):
        c.rectangle(520 + i * 90, 300, 50, 70); c.set_source_rgba(0, 0, 0, 0.25); c.fill()

def card_bg(c):
    c.set_source_rgb(*hx('2e1b0f')); c.paint()
    glow(c, W / 2, H / 2, 800, hx('593c23'), 0.9)

def vignette(c, k=0.75):
    g = cairo.RadialGradient(W / 2, H / 2, 380, W / 2, H / 2, 1150); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.06, 0.03, 0.01, k)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
def tint(c, col, a): c.rectangle(0, 0, W, H); c.set_source_rgba(*col, a); c.fill()
def dust(c, T, n=50, area=(500, 200, 1750, 1000), a=0.55):
    r = np.random.default_rng(7)
    for i in range(n):
        x0, y0, sp, ph = r.uniform(area[0], area[2]), r.uniform(area[1], area[3]), r.uniform(8, 20), r.uniform(0, 6)
        x = x0 + math.sin(T * 0.4 + ph) * 30; y = (y0 - T * sp - area[1]) % (area[3] - area[1]) + area[1]
        glow(c, x, y, 5, (1, 0.92, 0.7), a * (0.5 + 0.5 * math.sin(T * 2 + ph)))

# ---------- 道具 ----------
def lamp(c, x, y, lit, T, s=1.0):
    stroke(c, [(x, y), (x, y - 90 * s)], hx('6a4a2a'), 6 * s, False)
    ell(c, x, y, 26 * s, 7 * s, hx('6a4a2a'), 2.4)
    c.new_path(); c.arc(x, y - 90 * s, 22 * s, 0, math.pi); fill_stroke(c, hx('b07a3a'), 2.4)
    if lit > 0:
        f = 1 + 0.12 * math.sin(T * 17 + x)
        glow(c, x, y - 108 * s, 90 * s * lit, (1, 0.8, 0.4), 0.55 * lit)
        c.save(); c.translate(x, y - 96 * s); c.scale(s * lit, s * lit * f)
        c.new_path(); c.move_to(0, 0); c.curve_to(-12, -10, -6, -26, 0, -38); c.curve_to(6, -26, 12, -10, 0, 0)
        c.set_source_rgb(1, 0.78, 0.3); c.fill(); c.restore()
def sack(c, x, y, s, col, label):
    blob(c, [(x - 50 * s, y), (x - 58 * s, y - 60 * s), (x - 30 * s, y - 100 * s), (x - 14 * s, y - 118 * s), (x + 14 * s, y - 118 * s), (x + 30 * s, y - 100 * s), (x + 58 * s, y - 60 * s), (x + 50 * s, y)], col, 3)
    stroke(c, [(x - 20 * s, y - 104 * s), (x + 20 * s, y - 104 * s)], INK, 3, False)
    if label: font(c, 34 * s); w = tadv(c, label); c.move_to(x - w / 2, y - 36 * s); c.set_source_rgb(*RED2); c.show_text(label)
def jar(c, x, y, s, col=hx('7a4a2e'), label=None):
    blob(c, [(x - 26 * s, y), (x - 44 * s, y - 40 * s), (x - 40 * s, y - 80 * s), (x - 18 * s, y - 96 * s), (x + 18 * s, y - 96 * s), (x + 40 * s, y - 80 * s), (x + 44 * s, y - 40 * s), (x + 26 * s, y)], col, 3)
    poly(c, [(x - 16 * s, y - 96 * s), (x + 16 * s, y - 96 * s), (x + 13 * s, y - 112 * s), (x - 13 * s, y - 112 * s)], RED2, 2.4)
    if label: font(c, 30 * s); w = tadv(c, label); c.move_to(x - w / 2, y - 36 * s); c.set_source_rgb(*CREAM); c.show_text(label)
def scrollp(c, x, y, w, h, title, op=1.0, glowa=0.4, rot=0.0, lines=4, red=False):
    hh = h * op
    if glowa > 0: glow(c, x, y, max(w, h) * 1.1, (1, 0.85, 0.45), glowa)
    c.save(); c.translate(x, y); c.rotate(rot)
    if hh > 4:
        poly(c, [(-w / 2, -hh / 2), (w / 2, -hh / 2), (w / 2, hh / 2), (-w / 2, hh / 2)], hx('f1e2bb'), 3)
        c.save(); c.rectangle(-w / 2, -hh / 2, w, hh); c.clip()
        for k in range(lines):
            for j in range(int(h / 34)):
                c.rectangle(-w / 2 + 26 + k * (w - 90) / max(lines, 1), -h / 2 + 50 + j * 26, 5, 13); c.set_source_rgba(*INK, 0.5); c.fill()
        if title: vtext(c, title, w / 2 - 34, -h / 2 + 60, 44, RED2)
        c.restore()
    for yy in (-hh / 2 - 8, hh / 2 - 6): poly(c, [(-w / 2 - 14, yy), (w / 2 + 14, yy), (w / 2 + 14, yy + 14), (-w / 2 - 14, yy + 14)], RED2, 2.4)
    c.restore()
def tablet(c, x, y, s, txt):
    poly(c, [(x - 30 * s, y), (x + 30 * s, y), (x + 30 * s, y - 170 * s), (x, y - 196 * s), (x - 30 * s, y - 170 * s)], hx('1a120c'), 3)
    vtext(c, txt, x, y - 140 * s, 30 * s, GOLD)
def stove(c, x, y, T):
    poly(c, [(x - 160, y), (x + 160, y), (x + 150, y - 150), (x - 150, y - 150)], hx('8a6a4a'), 3)
    c.new_path(); c.arc(x, y - 30, 50, math.pi, 0); fill_stroke(c, hx('1a0f08'), 3)
    for k in range(5):
        fx = x - 34 + k * 17; fh = 40 + 18 * math.sin(T * 13 + k * 2)
        c.new_path(); c.move_to(fx - 12, y - 30); c.curve_to(fx - 10, y - 30 - fh * 0.6, fx, y - 30 - fh, fx + 2, y - 30 - fh); c.curve_to(fx + 4, y - 30 - fh * 0.5, fx + 12, y - 40, fx + 12, y - 30)
        c.set_source_rgba(1, 0.55 + 0.1 * k % 0.3, 0.15, 0.9); c.fill()
    glow(c, x, y - 50, 120, (1, 0.6, 0.2), 0.5)
    ell(c, x, y - 160, 120, 24, hx('3a3a3a'), 3)
    for k in range(3):
        ph = (T * 0.6 + k / 3) % 1
        stroke(c, [(x - 40 + k * 40, y - 190 - ph * 160), (x - 50 + k * 40 + 20 * math.sin(T * 3 + k), y - 230 - ph * 160), (x - 40 + k * 40, y - 270 - ph * 160)], (1, 1, 1), 8 * (1 - ph) + 1)
def stick(c, x, y, ang, L=300):
    c.save(); c.translate(x, y); c.rotate(ang)
    poly(c, [(-L / 2, -9), (L / 2, -12), (L / 2, 12), (-L / 2, 9)], hx('8a5a30'), 3); c.restore()
def bundle(c, x, y, s=1.0):
    blob(c, [(x - 50 * s, y), (x - 60 * s, y - 50 * s), (x - 20 * s, y - 80 * s), (x + 30 * s, y - 80 * s), (x + 60 * s, y - 40 * s), (x + 48 * s, y)], hx('3f5f88'), 3)
    stroke(c, [(x - 10 * s, y - 80 * s), (x - 20 * s, y - 104 * s), (x + 10 * s, y - 100 * s), (x + 4 * s, y - 80 * s)], INK, 4)

# ---------- 信息组件 ----------
def nameplate(c, x, y, role, name, a):
    if a <= 0: return
    c.save(); c.translate(x, y); s = 0.7 + 0.3 * back(a); c.scale(s, s)
    font(c, 54); w = max(tadv(c, name), 120) + 60
    c.new_path(); c.rectangle(-w / 2, -50, w, 96); c.set_source_rgba(0.12, 0.07, 0.03, 0.88 * a); c.fill_preserve(); c.set_source_rgba(*GOLD, a); c.set_line_width(3); c.stroke()
    text(c, role, 0, -60, 30, GOLD, a, 'c', 0.6)
    text(c, name, 0, 24, 54, CREAM, a, 'c', 0)
    c.restore()
def counter(c, x, y, label, n, t_pop, size=110, col=GOLD):
    k = 1 + 0.35 * max(0, 1 - t_pop * 5)
    c.save(); c.translate(x, y); c.scale(k, k)
    w1 = text(c, label, 0, 0, size * 0.6, CREAM, 1, 'l')
    text(c, '×' + str(n), w1 + 10, 0, size, col, 1, 'l')
    c.restore()
def stamp(c, s, x, y, t, size=150, col=RED, rot=-0.15):
    if t < 0: return
    k = 1 + 1.6 * max(0, 1 - t * 6); a = clamp(t * 6)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    font(c, size); w = tadv(c, s)
    c.rectangle(-w / 2 - 26, -size * 0.95, w + 52, size * 1.25); c.set_source_rgba(*col, a); c.set_line_width(10); c.stroke()
    c.move_to(-w / 2, size * 0.12); c.set_source_rgba(*col, a); c.show_text(s); c.restore()
def pip(c, x, y, w, h, fn, label, a, T):
    if a <= 0: return
    c.save(); c.translate(x, y); s = 0.85 + 0.15 * eout(a); c.scale(s, s)
    c.rectangle(-w / 2, -h / 2, w, h); c.clip()
    c.save(); c.translate(-w / 2, -h / 2); c.scale(w / W, h / H); fn(c, T); c.restore()
    tint(c, hx('3a2a1a'), 0.38)
    c.reset_clip(); c.rectangle(-w / 2, -h / 2, w, h); c.set_source_rgba(*GOLD, a); c.set_line_width(4); c.stroke()
    text(c, label, w / 2 - 20, h / 2 - 22, 30, CREAM, a, 'r', 0.6)
    c.restore()
def iconscroll(c, cells, hi, T, y=620, x0=180, cw=300, ch=380, cross=None, a=1.0):
    n = len(cells); wtot = n * cw + 40
    poly(c, [(x0 - 30, y - ch / 2 - 30), (x0 + wtot, y - ch / 2 - 30), (x0 + wtot, y + ch / 2 + 30), (x0 - 30, y + ch / 2 + 30)], hx('efe0bc'), 3)
    stroke(c, [(x0 - 30, y - ch / 2 - 22), (x0 + wtot, y - ch / 2 - 22)], RED2, 4, False)
    stroke(c, [(x0 - 30, y + ch / 2 + 22), (x0 + wtot, y + ch / 2 + 22)], RED2, 4, False)
    for i, (num, ic, cap) in enumerate(cells):
        cx = x0 + 20 + i * cw + cw / 2 - 20
        c.rectangle(cx - cw / 2 + 20, y - ch / 2, cw - 40, ch); c.set_source_rgb(*hx('f7ecd2')); c.fill_preserve(); c.set_source_rgba(*INK, 0.4); c.set_line_width(2); c.stroke()
        text(c, num, cx, y - ch / 2 + 70, 54, hx('927955'), 1, 'c', 0)
        ic(c, cx, y + 40, T)
        text(c, cap, cx, y + ch / 2 - 30, 40, INK, 1, 'c', 0)
        if hi is not None and i <= hi[0]:
            aa = clamp(hi[1] * 5) if i == hi[0] else 1
            c.rectangle(cx - cw / 2 + 14, y - ch / 2 - 6, cw - 28, ch + 12); c.set_source_rgba(*RED, aa); c.set_line_width(7); c.stroke()

# ---------- 字幕 ----------
def subtitle(c, lines, t):
    font(c, 84); y = 150
    k = 0
    for segs in lines:
        x = 80
        for txt, col in segs:
            a = clamp((t - 0.08 - k * 0.22) / 0.3); k += 1
            font(c, 84); w = tadv(c, txt)
            if a > 0:
                c.move_to(x + 4, y + 5 + (1 - a) * 10); c.set_source_rgba(0.08, 0.04, 0.02, 0.6 * a); c.show_text(txt)
                c.move_to(x, y + (1 - a) * 10); c.set_source_rgba(*col, a); c.show_text(txt)
                if col != CREAM:
                    c.rectangle(x, y + 16, (w - 14) * a, 6); c.set_source_rgba(*col, a); c.fill()
            x += w
        y += 112
    font(c, 20); c.move_to(24, 34); c.set_source_rgba(*CREAM, 0.6); c.show_text('人物和场面都是示意')

def S(*parts):
    """解析：'普通[红:xx]普通' -> segs"""
    out = []
    for line in parts:
        segs = []; i = 0
        while i < len(line):
            if line[i] == '[':
                j = line.index(']', i); tag, txt = line[i + 1:j].split(':', 1)
                segs.append((txt, {'红': ORANGE, '金': GOLD, '蓝': BLUE, '绿': GREENW}[tag])); i = j + 1
            else:
                j = line.find('[', i); j = len(line) if j < 0 else j; segs.append((line[i:j], CREAM)); i = j
        out.append(segs)
    return out

# ---------- 人物配色 ----------
TOPS = [hx('a8b28a'), hx('8fb3b0'), hx('d9b56a'), hx('b7a0c0'), hx('c9b48a'), hx('9fc0a0')]
SKS = [RED, hx('3f5f88'), hx('5f8f6a'), hx('b8503a'), hx('c9873a'), hx('7a4f8a')]
NUN = hx('8a4a2c')
def br(T, ph=0): return 2.5 * math.sin(T * 2.2 + ph)
def sw(T, ph=0, k=0.25): return k * math.sin(T * 1.6 + ph)

# =============== 镜头 ===============
def banquet(c, t, T, phase='fight'):
    paint_bg(c, 'room', room_full)
    back_ = []
    back_.append(woman(c, 330, 900 + br(T), 470, 1, TOPS[1], SKS[1], expr='shock' if phase != 'calm' else 'calm', armN=(0.4, -0.2, 0.3, -1.3) if phase != 'calm' else None, sw=sw(T)))
    back_.append(woman(c, 760, 900 + br(T, 1), 470, 1, TOPS[2], SKS[2], expr='grin', armN=(0.6, 0.6, 1.0, 1.4), headtilt=0.1 * math.sin(T * 5), sw=sw(T, 1)))
    raise_ = phase in ('stop', 'rule')
    nunarm = (0.8, -0.4, 1.5, -1.0 - 0.3 * math.sin(T * 9)) if raise_ else (0.3, 1.0, 0.9, 1.6)
    woman(c, 1230, 900 + br(T, 2), 500, -1, robe=NUN, shaved=True, expr='stern', armN=nunarm, armF=(0.3, 1.0, 0.7, 1.7), talk=abs(math.sin(T * 9)) if raise_ else 0)
    back_.append(woman(c, 1400, 900 + br(T, 3), 470, -1, TOPS[3], SKS[3], expr='shock' if phase != 'calm' else 'calm', armN=(0.3, -0.3, 0.2, -1.2) if phase != 'calm' else None, sw=sw(T, 3)))
    c.set_source_surface(cached('table', lambda cc: table(cc)), 0, 0); c.paint()
    if phase == 'calm':
        A = woman(c, 520, 1065 + br(T), 640, 1, TOPS[0], SKS[0], expr='grin', armN=(0.6, 0.4, 1.4, 0.4 + 0.2 * math.sin(T * 3)), sw=sw(T))
        B = woman(c, 1010, 1065 + br(T, 1), 640, -1, TOPS[1], hx('c9873a'), expr='calm', armN=(0.6, 0.5, 1.3, 0.6), talk=abs(math.sin(T * 7)), sw=sw(T, 2))
        return
    pump = math.sin(T * 10)
    A = woman(c, 520, 1065 + br(T), 640, 1, TOPS[0], SKS[0], lean=0.12, expr='angry', armN=(1.2, -0.2 + 0.3 * pump, 2.5, -0.6 + 0.4 * pump), armF=(-0.4, 0.9, 0.3, 1.9), sw=sw(T, 0, 0.4))
    B = woman(c, 1010, 1065 + br(T, 1), 640, -1, TOPS[1], hx('c9873a'), lean=0.12, expr='angry', armN=(1.2, -0.3 - 0.3 * pump, 2.4, -0.8 - 0.4 * pump), armF=(0.6, 1.0, 1.0, 1.5), sw=sw(T, 2, 0.4))
    L = woman(c, 1600, 1065 + br(T, 2), 640, -1, hx('d9c38a'), hx('3f5f88'), expr='calm', armN=(0.6, 0.9, 0.9, 1.7), armF=(0.4, 1.0, 0.9, 1.8), sw=sw(T, 4))
    hxp, hyp = L['n']
    scrollp(c, hxp - 20, hyp - 70, 190, 240, '社条', op=1.0 if phase == 'rule' else 0.0, glowa=0.45 if phase == 'rule' else 0.1, rot=-0.06)
    mx = (A['n'][0] + B['n'][0]) / 2; my = (A['n'][1] + B['n'][1]) / 2
    glow(c, mx, my, 120, (1, 0.6, 0.3), 0.5)
    c.save(); c.translate(mx, my - 10); c.rotate(T * 3); anger(c, 0, 0, 60); c.restore()
    if t > 0.3: bubble(c, A['head'][0] + 30, A['head'][1] - 30, '…!', 0.9 * min(1, back((t - 0.3) * 4)))
    if t > 0.6: bubble(c, B['head'][0] - 10, B['head'][1] - 40, '…?!', 0.9 * min(1, back((t - 0.6) * 4)))
    if t > 0.9:
        exclaim(c, back_[0]['head'][0] - 10, back_[0]['head'][1] - 10, 0.8)
        exclaim(c, back_[2]['head'][0] - 10, back_[2]['head'][1] - 10, 0.8)
    dust(c, T)

def sh_hook(c, t, d, T): banquet(c, t, T, 'fight'); tint(c, (0.6, 0.15, 0.05), 0.08)
def sh_fight(c, t, d, T): banquet(c, t, T, 'fight'); tint(c, (0.6, 0.15, 0.05), 0.1)
def sh_stop(c, t, d, T): banquet(c, t, T, 'stop'); tint(c, (0.6, 0.15, 0.05), 0.1)
def sh_rule(c, t, d, T):
    banquet(c, t, T, 'rule'); tint(c, (0.6, 0.15, 0.05), 0.06)
def sh_calm(c, t, d, T): banquet(c, t, T, 'calm')

def sh_scroll_close(c, t, d, T):
    paint_bg(c, 'room', room_full)
    L = woman(c, 1300, 1700 + br(T), 1500, -1, hx('d9c38a'), hx('3f5f88'), expr='stern', armN=(0.8, 0.6, 1.3, 1.1), armF=(0.5, 0.8, 1.2, 1.2), talk=abs(math.sin(T * 8)) * (t > 1.2))
    op = eout((t - 0.3) / 0.8)
    scrollp(c, 760, 640, 420, 560, '社条', op=op, glowa=0.5 * op)
    stamp(c, '罚', 760, 680, t - 2.0, 170)
    dust(c, T)

def title_card(c, t, d, T):
    paint_bg(c, 'card', card_bg)
    a = eout(t / 0.6)
    c.save(); c.translate(W / 2, H / 2); c.scale(0.9 + 0.1 * a, 0.9 + 0.1 * a)
    poly(c, [(-560, -240), (560, -240), (560, 240), (-560, 240)], hx('efe0bc'), 4)
    c.rectangle(-530, -210, 1060, 420); c.set_source_rgb(*RED2); c.set_line_width(4); c.stroke()
    text(c, '敦煌女人社', 0, 30, 170, hx('2e1b0f'), a, 'c', 0)
    text(c, '十五姐妹的山河之誓', 0, 150, 60, RED2, clamp((t - 0.6) / 0.4), 'c', 0)
    text(c, 'S.527 · 后周显德六年', 0, -140, 34, hx('927955'), clamp((t - 0.9) / 0.4), 'c', 0)
    c.restore()
    stamp(c, '社', W / 2 + 470, H / 2 + 200, t - 1.3, 80)
    dust(c, T, 30, (0, 0, W, H), 0.4)

def sh_arrive(c, t, d, T):
    paint_bg(c, 'ext', exterior)
    for i in range(7):
        x = -200 + i * 170 + t * 150
        if x > 900: x = 900 - (x - 900) * 0.05
        woman(c, x, 1000 + 3 * math.sin(T * 6 + i), 430 - (i % 2) * 20, 1, TOPS[i % 6], SKS[i % 6], expr='calm' if i % 3 else 'grin', armN=(0.3, 1.0, 0.5 + 0.3 * math.sin(T * 6 + i), 1.9), sw=0.3 * math.sin(T * 6 + i))
    text(c, '沙州 · 敦煌', 1700, 980, 46, hx('3a2414'), clamp(t / 0.5), 'r', 0)

def sh_leaders(c, t, d, T):
    paint_bg(c, 'room', room_full)
    for x, y, h, args in ((600, 1050, 640, dict(robe=NUN, shaved=True, expr='stern')),
                         (1000, 1050, 640, dict(top=TOPS[4], skirt=SKS[1], expr='proud')),
                         (1400, 1050, 640, dict(top=hx('d9c38a'), skirt=hx('3f5f88'), expr='calm'))):
        woman(c, x, y + br(T, x), h, 1 if x < 1000 else -1, armN=(0.4, 0.9, 0.7, 1.7), sw=sw(T, x / 100), **args)
    for i, (x, r, n) in enumerate(((600, '社官', '尼功德进'), (1000, '社长', '侯富子'), (1400, '录事', '印定磨'))):
        nameplate(c, x + (60 if i == 0 else 0), 860, r, n, clamp((t - 0.4 - i * 0.6) / 0.3))
    dust(c, T)

def sh_sisters(c, t, d, T):
    paint_bg(c, 'room', room_full)
    ks = [(380, 600), (640, 560), (900, 640), (1160, 590), (1420, 620)]
    for i, (x, h) in enumerate(ks):
        bow = 0.12 * ease((t - 1.0 - i * 0.15) / 0.5) * (1 - ease((t - 2.6) / 0.5))
        woman(c, x, 1050 + br(T, i), h, 1, TOPS[i], SKS[i], lean=bow, expr='grin' if i % 2 else 'calm', armN=(0.9, 0.3, 0.8, 1.2), armF=(0.6, 0.4, 0.8, 1.3), sw=sw(T, i))
    text(c, '姊', 520, 560, 110, GOLD, clamp((t - 1.8) / 0.3), 'c'); text(c, '妹', 1300, 560, 110, GOLD, clamp((t - 2.2) / 0.3), 'c')
    dust(c, T)

def sh_lamps(c, t, d, T, pray=False):
    paint_bg(c, 'card', card_bg)
    glow(c, W / 2, 700, 900, hx('442c19'), 0.8)
    n = 15
    lit = int(clamp((t - 0.3) / 2.6) * n) if not pray else n
    for i in range(n):
        x = 220 + i * 105; y = 960 - (i % 2) * 40
        lamp(c, x, y, 1.0 if i < lit else 0, T, 1.0)
    if pray:
        for i in range(5):
            woman(c, 340 + i * 300, 800, 430, 1 if i < 3 else -1, TOPS[i], SKS[i], lean=0.1, expr='calm', armN=(1.0, 0.0, 0.7, 0.9), armF=(0.8, 0.1, 0.7, 0.95), sw=sw(T, i))
        pip(c, 1450, 330, 640, 380, lambda cc, TT: (paint_bg(cc, 'room', room_full), tablet(cc, 860, 760, 1.6, '父之位'), tablet(cc, 1060, 760, 1.6, '母之位')), '为父母祈福', clamp((t - 0.5) / 0.4), T)
    else:
        counter(c, 1280, 420, '灯', max(lit, 0), (t - 0.3) * n / 2.6 % 1)
    dust(c, T, 40, (0, 300, W, 1000))

def sh_lamp_pray(c, t, d, T): sh_lamps(c, t, d, T, True)

def home(cc):
    room(cc)
    poly(cc, [(820, 760), (1260, 760), (1260, 780), (820, 780)], hx('4a2a18'), 3)
    tablet(cc, 1040, 760, 1.4, '先考之位')
    for k in range(3): stroke(cc, [(980 + k * 10, 760), (978 + k * 10, 740)], (0.9, 0.85, 0.7), 2, False)

def sh_chai(c, t, d, T):
    paint_bg(c, 'home', home)
    woman(c, 700, 1050 + br(T), 660, 1, hx('cfc8b8'), hx('8a8070'), lean=0.08, expr='sad', armN=(0.5, 0.6, 0.6, 1.0), armF=(0.4, 0.8, 0.6, 1.1), headtilt=0.12, sw=sw(T))
    nameplate(c, 820, 880, '社员', '柴家娘', clamp((t - 0.6) / 0.3))
    tint(c, hx('5a5a5a'), 0.22)

def sh_zhuantie(c, t, d, T):
    paint_bg(c, 'ext', exterior)
    pos = [(200, 1), (620, 1), (1040, 1), (1460, -1)]
    k = clamp(t / (d - 0.5)) * 3
    for i, (x, f) in enumerate(pos):
        woman(c, x + (80 if i < 3 else -80), 1040, 520, 1, TOPS[i], SKS[i], expr='calm', armN=(0.9, 0.2, 1.7, 0.6), sw=sw(T, i))
    seg = int(min(k, 2.999)); u = ease(k - seg)
    x = lerp(pos[seg][0] + 200, pos[seg + 1][0], u); y = 640 - 80 * math.sin(u * math.pi)
    scrollp(c, x, y, 90, 130, '转帖', 1.0, 0.35, rot=u * 0.6)
    text(c, '转帖', 1700, 980, 46, hx('3a2414'), 1, 'r', 0)

def ic_oil(c, x, y, T): jar(c, x, y + 60, 0.9, hx('b07a3a'), '油')
def ic_flour(c, x, y, T): sack(c, x, y + 60, 0.9, hx('efe8d8'), '面')
def ic_grain(c, x, y, T): sack(c, x, y + 60, 0.9, hx('d6b060'), '粟')
def sh_items(c, t, d, T):
    paint_bg(c, 'room', room_full)
    iconscroll(c, [('一合', ic_oil, '油'), ('一斤', ic_flour, '白面'), ('一斗', ic_grain, '粟')], (int(clamp((t - 0.5) / 2.4) * 2.99), ((t - 0.5) / 0.8) % 1), T, y=650, x0=180)
    woman(c, 1500, 1060 + br(T), 640, -1, TOPS[5], SKS[5], expr='grin', armN=(0.6, 0.6, 1.2, 0.8), armF=(0.4, 0.8, 1.1, 0.9), sw=sw(T))
    sack(c, 1380, 880, 0.8, hx('efe8d8'), '面')
    dust(c, T)

def sh_pile(c, t, d, T):
    paint_bg(c, 'home', home)
    n = int(clamp((t - 0.2) / 2.8) * 15)
    for i in range(n):
        row = i // 5; col = i % 5
        sack(c, 300 + col * 110 + row * 50, 1030 - row * 90, 0.75, hx('efe8d8'), '')
    counter(c, 260, 520, '白面', n, ((t - 0.2) / 2.8 * 15) % 1)
    text(c, '斤', 260 + 400, 520, 66, CREAM, 1 if n else 0, 'l')
    woman(c, 1560, 1050, 640, -1, hx('cfc8b8'), hx('8a8070'), expr='shock' if t > 2 else 'sad', armN=(0.4, 0.6, 0.6, 1.0), sw=sw(T))

def sh_kitchen(c, t, d, T):
    paint_bg(c, 'room', room_full)
    stove(c, 1350, 1000, T)
    woman(c, 950, 1060 + br(T), 620, 1, TOPS[2], SKS[2], lean=0.08, expr='grin', armN=(1.0, 0.2, 2.0, 0.5 + 0.2 * math.sin(T * 8)), sw=sw(T))
    woman(c, 560, 1060 + br(T, 1), 600, 1, TOPS[3], SKS[3], expr='calm', armN=(0.5, 0.6, 1.1, 0.9), armF=(0.4, 0.8, 1.0, 1.0), sw=sw(T, 1), talk=abs(math.sin(T * 7)))
    sack(c, 700, 960, 0.7, hx('d6b060'), '粟')
    woman(c, 280, 1060, 560, 1, TOPS[4], SKS[4], expr='calm', armN=(0.4, 0.4, 0.6, 0.0), sw=sw(T, 2))
    dust(c, T)

def sh_nofuss(c, t, d, T):
    paint_bg(c, 'home', home)
    woman(c, 620, 1050 + br(T), 640, 1, hx('cfc8b8'), hx('8a8070'), lean=0.15 * ease((t - 0.3) / 0.6), expr='calm', armN=(0.9, 0.3, 0.8, 1.2), armF=(0.6, 0.4, 0.8, 1.3), sw=sw(T))
    pip(c, 1380, 520, 760, 460, lambda cc, TT: (paint_bg(cc, 'roomtable', lambda q: (room(q), table(q)))), '招待厚薄', clamp((t - 0.6) / 0.4), T)
    stamp(c, '不追究', 1380, 560, t - 1.8, 110, hx('d9a040'))

def sh_shock(c, t, d, T):
    paint_bg(c, 'room', room_full)
    s = 1 + 0.08 * ease(t / 1.5)
    c.save(); c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
    glow(c, 860, 520, 360, (1, 0.85, 0.4), 0.4)
    for k in range(2):
        c.new_path(); c.arc(860, 520, 200 + k * 40 + 10 * math.sin(T * 6), 0, 7); c.set_source_rgba(*GOLD, 0.7); c.set_line_width(5); c.stroke()
    A = woman(c, 860, 1500, 1200, 1, TOPS[0], SKS[0], expr='shock', armN=(0.3, 0.6, 0.4, 1.4), headtilt=-0.05)
    c.restore()
    exclaim(c, 1150, 400, 1.3)

def sh_quit(c, t, d, T):
    paint_bg(c, 'room', room_full)
    u = ease((t - 0.8) / 2.5)
    Q = woman(c, 1000 + u * 500, 1060 + 4 * math.sin(T * 7) * (u > 0), 620, 1, TOPS[4], SKS[4], expr='angry', armN=(0.3, 0.8, 0.5, 1.6), armF=(-0.5, 0.2, -0.6, 0.9), sw=0.4 * math.sin(T * 7) if u > 0 else 0)
    bundle(c, Q['f'][0] - 20, Q['f'][1] + 70, 0.9)
    for i, x in enumerate((300, 550)):
        woman(c, x, 1060, 600, 1, TOPS[i], SKS[i], expr='shock', armN=(0.6, -0.2, 1.4, -0.6), sw=sw(T, i))
    if t > 1.2: bubble(c, 1100 + u * 500, 300, '退社!', 0.9)

def sh_sticks(c, t, d, T):
    paint_bg(c, 'card', card_bg)
    n = int(clamp((t - 0.3) / 1.8) * 3)
    for i in range(3):
        if i < n or (i == n and t > 0.3):
            k = clamp(((t - 0.3) - i * 0.6) / 0.15)
            stick(c, 500 + i * 220, 560, -0.9 + 0.2 * (1 - k) * -3, 420)
    counter(c, 1100, 520, '棒', n, ((t - 0.3) / 0.6) % 1)
    if t > 2.6:
        jar(c, 1400, 900, 1.6, hx('7a4a2e'), '酒席'); text(c, '+1', 1560, 760, 90, GOLD, clamp((t - 2.6) / 0.2), 'l')

def sh_nofree(c, t, d, T):
    paint_bg(c, 'room', room_full)
    scrollp(c, 760, 620, 520, 620, '社条', 1.0, 0.45)
    stamp(c, '的无免者', 1350, 640, t - 1.0, 120, RED, -0.08)
    dust(c, T)

def other_late(cc, TT):
    room(cc); table(cc)
    woman(cc, 1400, 1060, 640, -1, TOPS[5], SKS[5], expr='sad', armN=(0.4, 0.6, 0.6, 1.0))
    jar(cc, 1100, 1000, 1.8, hx('7a4a2e'), '半瓮')
def sh_other(c, t, d, T):
    paint_bg(c, 'card', card_bg)
    pip(c, W / 2, 660, 1200, 660, other_late, '据其他社邑文书', clamp(t / 0.4), T)
    font(c, 30)

def sh_sign(c, t, d, T):
    paint_bg(c, 'card', card_bg)
    poly(c, [(360, 260), (1560, 260), (1560, 960), (360, 960)], hx('efe0bc'), 4)
    names = ['尼功德进', '侯富子', '印定磨', '柴家娘', '某家女', '某家妻', '某家娘', '某家女', '某家妻', '某家娘', '某家女', '某家妻', '某家娘', '某家女', '某家妻']
    n = int(clamp((t - 0.3) / 3.0) * 15)
    for i in range(n):
        x = 1480 - i * 76; vtext(c, names[i] if i < 4 else '□□□', x, 330, 40, INK)
        c.new_path(); c.arc(x, 760, 18, 0, 7); c.set_source_rgba(*RED, 0.85); c.fill()
    counter(c, 1180, 1030, '画押', n, ((t - 0.3) / 3.0 * 15) % 1, 80)

def sh_oath(c, t, d, T):
    paint_bg(c, 'ext', exterior)
    glow(c, 400, 220, 200, (0.9, 0.95, 1), 0.6); ell(c, 400, 220, 54, 54, hx('eef0f4'), 0)
    for i in range(6):
        woman(c, 300 + i * 260, 1040 + br(T, i), 520, 1 if i < 3 else -1, TOPS[i], SKS[i], expr='proud', armN=(0.5, -0.4, 0.6, -1.5) if i in (1, 4) else (0.4, 0.9, 0.7, 1.7), sw=sw(T, i, 0.5))
    tint(c, (1, 0.8, 0.3), 0.06)

def sh_contrast(c, t, d, T):
    paint_bg(c, 'ext', exterior)
    poly(c, [(760, 520), (940, 520), (940, 780), (760, 780)], hx('3a2414'), 3)
    u = ease((t - 1.2) / 1.2)
    for i in range(5):
        woman(c, 850 + (i - 2) * 230 * u, 1040, 520, 1, TOPS[i], SKS[i], expr='proud' if u > 0.5 else 'calm', armN=(0.4, 0.9, 0.7, 1.7), sw=sw(T, i))
    if t < 1.3: stamp(c, '?', 1300, 400, t - 0.2, 120, hx('e0b24a'), 0)

def ic_help(c, x, y, T):
    for k in range(3): ell(c, x - 50 + k * 50, y - 20, 22, 22, SKIN, 2.4); poly(c, [(x - 72 + k * 50, y + 60), (x - 28 + k * 50, y + 60), (x - 30 + k * 50, y + 10), (x - 70 + k * 50, y + 10)], SKS[k], 2)
def ic_fee(c, x, y, T): sack(c, x, y + 70, 1.0, hx('d6b060'), '粟')
def ic_rule(c, x, y, T): scrollp(c, x, y + 10, 120, 160, '', 1, 0, lines=3)
def sh_icons(c, t, d, T):
    paint_bg(c, 'room', room_full)
    iconscroll(c, [('一', ic_help, '互助会'), ('二', ic_fee, '会费'), ('三', ic_rule, '公约')], (int(clamp((t - 0.6) / 2.2) * 2.99), ((t - 0.6) / 0.73) % 1), T, y=640, x0=440)
    dust(c, T)

def sh_cave(c, t, d, T):
    paint_bg(c, 'cave', cave)
    s = 1 + 0.12 * ease(t / d)
    c.save(); c.translate(W / 2, 620); c.scale(s, s); c.translate(-W / 2, -620)
    scrollp(c, W / 2, 560, 300, 380, '社条', eout((t - 0.6) / 0.8), 0.6)
    c.restore()
    glow(c, W / 2, 0, 600, (1, 0.9, 0.6), 0.25)
    dust(c, T, 50, (500, 100, 1400, 1000))
    text(c, '莫高窟 · 藏经洞', 1700, 980, 46, CREAM, clamp(t / 0.5), 'r', 0.5)

def sh_number(c, t, d, T):
    paint_bg(c, 'card', card_bg)
    scrollp(c, 620, 600, 380, 520, '社条', 1, 0.4)
    k = 1 + 0.4 * max(0, 1 - t * 4)
    c.save(); c.translate(1300, 620); c.scale(k, k); text(c, 'S.527', 0, 0, 170, GOLD, clamp(t * 3), 'c'); c.restore()
    text(c, '英国国家图书馆藏', 1300, 760, 50, CREAM, clamp((t - 0.8) / 0.4), 'c')

# 镜头表：(时长, 函数, 字幕, 音效[(t,kind)])
SHOTS = [
 (5.0, sh_hook, S('一千多年前的[绿:敦煌]，', '一群女人给自己[金:定了规矩]。'), [(0.3, 'pop'), (0.6, 'pop'), (0.9, 'ding')]),
 (4.6, sh_scroll_close, S('席上吵架[红:不听劝]？', '罚你[金:请全社吃一桌]。'), [(0.3, 'paper'), (2.0, 'thud')]),
 (4.2, title_card, [], [(0.0, 'drum'), (1.3, 'thud')]),
 (5.0, sh_arrive, S('[金:公元959年]，正月初三，', '[绿:沙州敦煌]。'), [(0.0, 'whoosh')]),
 (5.2, sh_leaders, S('社官是尼姑[蓝:功德进]，', '社长[蓝:侯富子]，录事[蓝:印定磨]。'), [(0.4, 'pop'), (1.0, 'pop'), (1.6, 'pop')]),
 (5.0, sh_sisters, S('社条开头就写：', '[金:大者若姊，小者若妹]。'), [(1.8, 'ding'), (2.2, 'ding')]),
 (5.2, sh_lamps, S('正月建福，每人交', '[金:粟一斗]、[金:灯油一盏]。'), [(0.3 + i * 0.173, 'tick') for i in range(15)]),
 (4.4, sh_lamp_pray, S('十五盏灯一起点亮，', '为家里[金:父母祈福]。'), [(0.5, 'whoosh')]),
 (5.0, sh_chai, S('社里的[蓝:柴家娘]，', '家里出了[红:丧事]。'), [(0.6, 'pop')]),
 (4.6, sh_zhuantie, S('录事写下[金:转帖]，', '一家传一家。'), [(0.2, 'paper'), (1.5, 'paper'), (2.9, 'paper')]),
 (5.4, sh_items, S('每人捧来：[金:油一合]、', '[金:白面一斤]、[金:粟一斗]。'), [(0.5, 'ding'), (1.3, 'ding'), (2.1, 'ding')]),
 (4.6, sh_pile, S('十五个人，', '就是[金:十五斤白面]。'), [(0.2 + i * 0.187, 'tick') for i in range(15)]),
 (4.6, sh_kitchen, S('上门[金:做饭]，', '帮着[金:送葬]。'), [(0.0, 'fire')]),
 (5.0, sh_nofuss, S('主家招待厚了薄了，', '社条写明：[金:不追究]。'), [(0.6, 'whoosh'), (1.8, 'thud')]),
 (4.6, sh_fight, S('可饭后一喝酒，', '有人[红:划拳红了眼]。'), [(0.3, 'pop'), (0.6, 'pop'), (0.9, 'ding')]),
 (4.4, sh_stop, S('社官喊停，', '[红:谁劝都不听]。'), [(0.4, 'pop')]),
 (5.0, sh_rule, S('录事展开社条：', '罚她[金:请全社吃一桌]！'), [(0.2, 'paper'), (1.2, 'ding')]),
 (4.0, sh_shock, S('这一桌，', '[红:得她自己掏]。'), [(0.1, 'boing')]),
 (4.8, sh_quit, S('更狠的是[红:退社]，', '有人闹着要走——'), [(0.8, 'whoosh'), (1.2, 'pop')]),
 (5.2, sh_sticks, S('先[红:打三棍]，', '再[红:罚一桌酒席]。'), [(0.3, 'whack'), (0.9, 'whack'), (1.5, 'whack'), (2.6, 'ding')]),
 (5.0, sh_nofree, S('社条原话：', '[红:的无免者]，谁也别想免。'), [(1.0, 'thud')]),
 (5.2, sh_other, S('别的社更严：', '开会迟到，[红:罚酒半瓮]。'), [(0.0, 'whoosh')]),
 (4.8, sh_sign, S('最后，[金:十五人]', '逐一画押。'), [(0.3 + i * 0.2, 'tick') for i in range(15)]),
 (5.2, sh_oath, S('[金:如水如鱼]，', '[金:山河为誓，日月证知]。'), [(0.0, 'drum')]),
 (4.8, sh_contrast, S('都说古代女人', '[红:大门不出，二门不迈]，'), [(0.2, 'boing'), (1.2, 'whoosh')]),
 (5.0, sh_icons, S('可她们早就有了', '[金:互助会]、[金:会费]和[金:公约]。'), [(0.6, 'ding'), (1.33, 'ding'), (2.06, 'ding')]),
 (5.0, sh_cave, S('一千年后，这张纸', '在[绿:藏经洞]里被翻了出来。'), [(0.6, 'paper')]),
 (4.6, sh_number, S('编号[金:S.527]，', '今藏[绿:英国国家图书馆]。'), [(0.0, 'thud')]),
 (5.4, sh_hook, S('一千多年前的[绿:敦煌]，', '一群女人给自己[金:定了规矩]。'), [(0.3, 'pop'), (0.6, 'pop'), (0.9, 'ding')]),
]
STARTS = np.cumsum([0] + [s[0] for s in SHOTS])
TOTAL = STARTS[-1]

def frame(fi):
    T = fi / FPS
    k = int(np.searchsorted(STARTS, T, side='right') - 1); k = min(k, len(SHOTS) - 1)
    d, fn, sub, _ = SHOTS[k]; t = T - STARTS[k]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    # 镜头内缓推
    z = 1 + 0.035 * (t / d)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    fn(c, t, d, T)
    c.restore()
    vignette(c)
    if sub: subtitle(c, sub, t)
    # 转场：金色竖光扫过
    if t < 0.22 and k > 0:
        u = t / 0.22; x = lerp(-200, W + 200, u)
        g = cairo.LinearGradient(x - 160, 0, x + 160, 0); g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0); g.add_color_stop_rgba(0.5, 1, 0.9, 0.6, 0.85); g.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
        c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    if T > TOTAL - 0.4: tint(c, (0, 0, 0), 0)
    s.flush()
    return np.ndarray((H, W, 4), np.uint8, s.get_data())[..., :3].copy()  # BGR

if __name__ == '__main__':
    import subprocess
    mode = sys.argv[1]
    if mode == 'sheet':
        from PIL import Image
        ts = [STARTS[i] + SHOTS[i][0] * 0.7 for i in range(len(SHOTS))]
        sel = ts[int(sys.argv[2]):int(sys.argv[3])]
        ims = [Image.fromarray(frame(int(t * FPS))[..., ::-1]).resize((640, 360)) for t in sel]
        cols = 3; rows = (len(ims) + 2) // 3; sheet = Image.new('RGB', (640 * cols, 360 * rows))
        for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 640, (i // cols) * 360))
        sheet.save(sys.argv[4], quality=85)
    elif mode == 'part':
        p, P = int(sys.argv[2]), int(sys.argv[3])
        N = int(TOTAL * FPS); a = N * p // P; b = N * (p + 1) // P
        ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', f'part{p}.mp4'], stdin=subprocess.PIPE)
        for fi in range(a, b): ff.stdin.write(frame(fi).tobytes())
        ff.stdin.close(); ff.wait()
    elif mode == 'events':
        ev = [(float(STARTS[i] + t0), kind) for i, s in enumerate(SHOTS) for (t0, kind) in s[3]]
        ev += [(float(STARTS[i]), 'swish') for i in range(1, len(SHOTS))]
        json.dump({'total': float(TOTAL), 'ev': ev}, open('events.json', 'w')); print(TOTAL)

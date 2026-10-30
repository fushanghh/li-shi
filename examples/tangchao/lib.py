# 史海风 · 敦煌女人社 剧照（纯代码 cairo）
import math, numpy as np, cairocffi as cairo
from PIL import Image, ImageFilter
W, H = 1920, 1080
def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
INK = hx('2e1b0f'); SKIN = hx('dcab7c'); SKIN2 = hx('94502c'); BLUSH = hx('d9796a')
HAIR = hx('17110d'); GOLD = hx('e0b24a'); RED = hx('c0392b'); RED2 = hx('8d442d')
CREAM = hx('efe2c2'); CREAM2 = hx('d8c49a')
WALL = hx('593c23'); WALL2 = hx('442c19'); BEAM = hx('3a2414'); WOOD = hx('715d40'); WOOD2 = hx('5a4630')
LIGHT = hx('f6e3b0')

def fill_stroke(c, col, lw=3.2, a=1.0, line=INK):
    c.set_source_rgba(*col, a); c.fill_preserve(); c.set_source_rgba(*line, a); c.set_line_width(lw); c.stroke()
def poly(c, pts, col, lw=3.2, close=True):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    if close: c.close_path()
    fill_stroke(c, col, lw)
def smooth(c, pts, close=True):
    n = len(pts); c.new_path(); c.move_to(*pts[0])
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (close or i > 0) else pts[0]; p1 = pts[i]; p2 = pts[(i + 1) % n]; p3 = pts[(i + 2) % n] if (close or i + 2 < n) else pts[-1]
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    if close: c.close_path()
def blob(c, pts, col, lw=3.2): smooth(c, pts, True); fill_stroke(c, col, lw)
def ell(c, x, y, rx, ry, col, lw=3.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); fill_stroke(c, col, lw)
def stroke(c, pts, col=INK, lw=3, curve=True):
    if curve and len(pts) > 2: smooth(c, pts, False)
    else:
        c.new_path(); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]
    c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
def hose(c, p0, pc, p1, w, col):
    for lw, cc in ((w + 6, INK), (w, col)):
        c.new_path(); c.move_to(*p0); c.curve_to(pc[0], pc[1], pc[0], pc[1], *p1)
        c.set_source_rgb(*cc); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
def glow(c, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 7); c.fill()

# ---------- 唐女（瘦长，头≈1/7） ----------
def woman(c, x, yf, h, face=1, top=hx('a8b28a'), skirt=RED, pibo=CREAM, lean=0.0, expr='calm',
          armN=None, armF=None, seated=False, shaved=False, robe=None, headtilt=0.0, sw=0.0, talk=0.0):
    """face=1 朝右, -1 朝左。armN/armF: (肘控制点dx,dy, 手dx,dy) 相对肩，单位=h"""
    u = h / 7.0; s = face
    c.save(); c.translate(x, yf)
    c.rotate(lean * s)
    # 关键点（朝右坐标，最后镜像）
    def P(px, py): return (px * s, py)
    neck = (0.15 * u, -6.0 * u); chest = -5.35 * u
    shN = P(0.25 * u, -5.5 * u); shF = P(-0.35 * u, -5.55 * u)
    def arm(spec, sh, near):
        if spec is None: spec = (0.2, 1.1, 0.35, 2.2)
        ex, ey, hx_, hy_ = spec
        pc = (sh[0] + ex * u * s, sh[1] + ey * u); ph = (sh[0] + hx_ * u * s, sh[1] + hy_ * u)
        sl = top if robe is None else robe
        col = sl if near else tuple(v * 0.82 for v in sl)
        hose(c, sh, pc, ph, 0.36 * u, col)
        ell(c, ph[0], ph[1], 0.24 * u, 0.2 * u, SKIN if near else SKIN2, 2.6)
        return ph
    hands = {}
    hands['f'] = arm(armF, shF, False)
    # 披帛 后环
    if robe is None:
        stroke(c, [P(-0.5 * u, -5.4 * u), P(-0.95 * u - sw * u * s, -3.6 * u), P(-1.0 * u - sw * 1.6 * u * s, -1.6 * u), P(-0.8 * u - sw * 1.6 * u * s, -1.4 * u), P(-0.7 * u, -3.4 * u), P(-0.35 * u, -5.0 * u)], INK, 0.11 * u + 5)
        stroke(c, [P(-0.5 * u, -5.4 * u), P(-0.95 * u - sw * u * s, -3.6 * u), P(-1.0 * u - sw * 1.6 * u * s, -1.6 * u), P(-0.8 * u - sw * 1.6 * u * s, -1.4 * u), P(-0.7 * u, -3.4 * u), P(-0.35 * u, -5.0 * u)], pibo, 0.11 * u)
    # 下身：高腰长裙 / 僧衣
    if seated:
        sk = [P(-0.62 * u, chest), P(0.6 * u, chest), P(0.75 * u, -2.6 * u), P(2.0 * u, -2.4 * u), P(2.1 * u, -1.8 * u), P(-0.7 * u, -1.8 * u)]
    else:
        sk = [P(-0.62 * u, chest), P(0.62 * u, chest), P(0.78 * u, -2.2 * u), P(0.95 * u, 0), P(-0.9 * u, 0), P(-0.82 * u, -2.2 * u)]
    if robe is not None:
        sk = [P(-0.8 * u, -5.7 * u), P(0.7 * u, -5.7 * u), P(0.85 * u, -2.2 * u), P(1.0 * u, 0), P(-1.0 * u, 0), P(-0.95 * u, -2.2 * u)] if not seated else \
             [P(-0.8 * u, -5.7 * u), P(0.7 * u, -5.7 * u), P(0.85 * u, -2.6 * u), P(2.0 * u, -2.4 * u), P(2.1 * u, -1.8 * u), P(-0.9 * u, -1.8 * u)]
        poly(c, sk, robe)
        # 袈裟斜纹
        stroke(c, [P(-0.7 * u, -5.6 * u), P(0.75 * u, -3.4 * u)], tuple(v * 0.75 for v in robe), 0.18 * u, False)
        for k in range(3): stroke(c, [P((-0.7 + 0.45 * k) * u, -3.0 * u), P((-0.7 + 0.45 * k) * u, -1.9 * u)], tuple(v * 0.8 for v in robe), 2.2, False)
    else:
        poly(c, sk, skirt)
        c.save(); poly_path = sk; c.new_path(); c.move_to(*sk[0]); [c.line_to(*p) for p in sk[1:]]; c.close_path(); c.clip()
        for k in range(-3, 4): stroke(c, [P(k * 0.22 * u, chest + 0.3 * u), P(k * 0.28 * u, 0)], tuple(v * 0.8 for v in skirt), 2.2, False)
        c.restore()
        # 裙腰带
        poly(c, [P(-0.64 * u, chest - 0.08 * u), P(0.64 * u, chest - 0.08 * u), P(0.66 * u, chest + 0.18 * u), P(-0.66 * u, chest + 0.18 * u)], tuple(v * 0.7 for v in skirt), 2.4)
        # 上身半臂
        poly(c, [P(-0.55 * u, -5.75 * u), P(0.5 * u, -5.75 * u), P(0.6 * u, chest), P(-0.6 * u, chest)], top)
        stroke(c, [P(0.0, -5.75 * u), P(0.18 * u, -5.45 * u), P(0.3 * u, chest)], INK, 2.4)
        if not seated:
            # 鞋尖
            ell(c, *P(0.55 * u, -0.02 * u), 0.3 * u, 0.12 * u, INK, 2)
    # 颈
    poly(c, [P(-0.05 * u, -6.2 * u), P(0.3 * u, -6.2 * u), P(0.3 * u, -5.7 * u), P(-0.05 * u, -5.7 * u)], SKIN, 2.6)
    # 头
    c.save(); hcx, hcy = P(0.22 * u, -6.65 * u); c.translate(hcx, hcy); c.rotate(headtilt * s)
    R = 0.5 * u
    if not shaved:
        # 高髻（后）
        blob(c, [P(-0.35 * R, -0.7 * R), P(-0.6 * R, -1.6 * R), P(-0.2 * R, -2.35 * R), P(0.45 * R, -2.25 * R), P(0.55 * R, -1.6 * R), P(0.3 * R, -0.8 * R)], HAIR, 3)
        blob(c, [P(-1.0 * R, -0.2 * R), P(-0.9 * R, -0.9 * R), P(-0.3 * R, -1.15 * R), P(0.5 * R, -1.05 * R), P(0.4 * R, -0.3 * R), P(-0.5 * R, 0.6 * R)], HAIR, 3)
    # 脸（3/4 侧，唐代丰腴圆脸）
    blob(c, [P(-0.9 * R, -0.15 * R), P(-0.62 * R, -0.95 * R), P(0.3 * R, -1.05 * R), P(0.85 * R, -0.6 * R), P(0.98 * R, 0.02 * R), P(0.9 * R, 0.5 * R), P(0.58 * R, 0.92 * R), P(0.05 * R, 1.05 * R), P(-0.6 * R, 0.78 * R)], SKIN, 3)
    if shaved:
        blob(c, [P(-0.85 * R, -0.3 * R), P(-0.55 * R, -1.08 * R), P(0.45 * R, -1.02 * R), P(0.88 * R, -0.45 * R), P(0.2 * R, -0.62 * R), P(-0.6 * R, -0.2 * R)], hx('a87a54'), 2.4)
    else:
        # 前额刘海 + 鬓发
        blob(c, [P(-0.9 * R, -0.25 * R), P(-0.6 * R, -1.05 * R), P(0.5 * R, -1.08 * R), P(0.92 * R, -0.5 * R), P(0.35 * R, -0.62 * R), P(-0.3 * R, -0.45 * R), P(-0.55 * R, 0.3 * R)], HAIR, 2.6)
        stroke(c, [P(-0.75 * R, 0.0), P(-0.82 * R, 0.8 * R), P(-0.7 * R, 1.2 * R)], HAIR, 4)
        # 金簪 + 红珠
        stroke(c, [P(-0.9 * R, -1.45 * R), P(0.85 * R, -1.75 * R)], GOLD, 5, False)
        ell(c, *P(0.88 * R, -1.76 * R), 0.13 * R, 0.13 * R, RED, 2)
        # 花钿
        ell(c, *P(0.45 * R, -0.5 * R), 0.06 * R, 0.06 * R, RED, 0)
    # 腮红
    glow(c, *P(0.38 * R, 0.32 * R), 0.36 * R, BLUSH, 0.6)
    LIP = hx('b8322a')
    def lips(open_=0.0):
        mx, my = P(0.6 * R, 0.6 * R)
        if open_ > 0.05:
            ell(c, mx, my, 0.1 * R, 0.04 * R + 0.1 * R * open_, hx('5a1a12'), 2)
        else:
            ell(c, mx, my, 0.1 * R, 0.06 * R, LIP, 0)
            stroke(c, [P(0.51 * R, 0.6 * R), P(0.69 * R, 0.6 * R)], hx('6a1a12'), 1.6, False)
    def brow(y0, y1, w=3.6):
        stroke(c, [P(0.24 * R, y0 * R), P(0.42 * R, (min(y0, y1) - 0.06) * R), P(0.62 * R, y1 * R)], INK, w)
    def eye_open():
        ell(c, *P(0.45 * R, -0.15 * R), 0.13 * R, 0.09 * R, (1, 1, 1), 2.2)
        ell(c, *P(0.49 * R, -0.15 * R), 0.06 * R, 0.07 * R, INK, 0)
        stroke(c, [P(0.3 * R, -0.22 * R), P(0.45 * R, -0.27 * R), P(0.6 * R, -0.2 * R)], INK, 3)
    if expr == 'shock':
        ell(c, *P(0.45 * R, -0.15 * R), 0.2 * R, 0.2 * R, (1, 1, 1), 2.6); ell(c, *P(0.49 * R, -0.15 * R), 0.07 * R, 0.07 * R, INK, 0)
        ell(c, *P(0.6 * R, 0.6 * R), 0.08 * R, 0.11 * R, hx('5a1a12'), 2)
        brow(-0.55, -0.6)
    elif expr == 'angry':
        stroke(c, [P(0.22 * R, -0.42 * R), P(0.62 * R, -0.22 * R)], INK, 4.5, False)
        eye_open()
        c.new_path(); c.move_to(*P(0.48 * R, 0.55 * R)); c.line_to(*P(0.74 * R, 0.52 * R)); c.line_to(*P(0.64 * R, 0.74 * R)); c.close_path(); fill_stroke(c, hx('5a1a12'), 2.2)
    elif expr == 'grin':
        stroke(c, [P(0.3 * R, -0.12 * R), P(0.45 * R, -0.22 * R), P(0.6 * R, -0.12 * R)], INK, 3)
        brow(-0.42, -0.42)
        c.new_path(); c.move_to(*P(0.46 * R, 0.52 * R)); c.curve_to(*P(0.5 * R, 0.75 * R), *P(0.7 * R, 0.75 * R), *P(0.76 * R, 0.5 * R)); c.close_path(); fill_stroke(c, (1, 1, 1), 2.2)
    elif expr == 'stern':
        stroke(c, [P(0.3 * R, -0.13 * R), P(0.6 * R, -0.13 * R)], INK, 3.2, False)
        stroke(c, [P(0.24 * R, -0.42 * R), P(0.62 * R, -0.38 * R)], INK, 4, False)
        stroke(c, [P(0.52 * R, 0.6 * R), P(0.7 * R, 0.6 * R)], INK, 2.6, False)
    elif expr == 'sad':
        stroke(c, [P(0.3 * R, -0.1 * R), P(0.45 * R, -0.04 * R), P(0.6 * R, -0.1 * R)], INK, 3)
        stroke(c, [P(0.24 * R, -0.3 * R), P(0.62 * R, -0.48 * R)], INK, 3.6, False)
        stroke(c, [P(0.5 * R, 0.66 * R), P(0.6 * R, 0.6 * R), P(0.7 * R, 0.66 * R)], INK, 2.4)
        ell(c, *P(0.5 * R, 0.12 * R), 0.05 * R, 0.09 * R, hx('9fd0e0'), 1.2)
    elif expr == 'proud':
        stroke(c, [P(0.3 * R, -0.12 * R), P(0.45 * R, -0.2 * R), P(0.6 * R, -0.12 * R)], INK, 3)
        brow(-0.45, -0.48)
        lips(); stroke(c, [P(0.48 * R, 0.56 * R), P(0.6 * R, 0.66 * R), P(0.74 * R, 0.54 * R)], INK, 2)
    else:  # calm 半闭眼
        stroke(c, [P(0.3 * R, -0.15 * R), P(0.45 * R, -0.08 * R), P(0.6 * R, -0.15 * R)], INK, 3)
        brow(-0.42, -0.45)
        lips(talk)
    # 小鼻子（不外凸）
    stroke(c, [P(0.8 * R, 0.08 * R), P(0.86 * R, 0.26 * R), P(0.76 * R, 0.3 * R)], INK, 2.2)
    c.restore()
    # 近手
    hands['n'] = arm(armN, shN, True)
    # 披帛 前环
    if robe is None:
        pts = [P(0.35 * u, -5.6 * u), P(0.75 * u, -4.0 * u), P(0.82 * u + sw * 1.6 * u * s, -2.0 * u) if not seated else P(1.2 * u, -2.2 * u), P(0.62 * u + sw * 1.6 * u * s, -1.85 * u) if not seated else P(1.05 * u, -2.0 * u), P(0.55 * u, -3.8 * u), P(0.3 * u, -5.2 * u)]
        stroke(c, pts, INK, 0.11 * u + 5); stroke(c, pts, pibo, 0.11 * u)
    m = c.get_matrix()
    out = {k: m.transform_point(*v) for k, v in hands.items()}
    out['head'] = m.transform_point(*P(0.22 * u, -7.6 * u))
    c.restore()
    return out

# ---------- 场景 ----------
def room(c):
    c.set_source_rgb(*WALL); c.paint()
    # 后墙板 + 梁柱
    for x in range(0, W, 240):
        c.rectangle(x, 0, 6, H); c.set_source_rgba(*WALL2, 0.6); c.fill()
    c.rectangle(0, 70, W, 46); c.set_source_rgb(*BEAM); c.fill()
    c.rectangle(0, 116, W, 8); c.set_source_rgb(*WOOD2); c.fill()
    for x in (150, 1010, 1770):
        c.rectangle(x - 34, 0, 68, H); c.set_source_rgb(*BEAM); c.fill(); c.rectangle(x - 34, 0, 10, H); c.set_source_rgba(*WOOD, 0.5); c.fill()
    # 木格窗（逆光亮栅）
    wx0, wx1, wy0, wy1 = 1090, 1690, 230, 640
    c.rectangle(wx0, wy0, wx1 - wx0, wy1 - wy0); c.set_source_rgb(*LIGHT); c.fill()
    g = cairo.LinearGradient(0, wy0, 0, wy1); g.add_color_stop_rgba(0, 1, 0.97, 0.85, 0.6); g.add_color_stop_rgba(1, 0.95, 0.8, 0.5, 0.3)
    c.rectangle(wx0, wy0, wx1 - wx0, wy1 - wy0); c.set_source(g); c.fill()
    for x in np.arange(wx0, wx1 + 1, 38):
        c.rectangle(x - 7, wy0, 14, wy1 - wy0); c.set_source_rgb(*hx('4a3020')); c.fill()
    for y in (wy0, wy1 - 16): c.rectangle(wx0 - 20, y - 6, wx1 - wx0 + 40, 22); c.set_source_rgb(*BEAM); c.fill()
    c.rectangle(wx0 - 20, wy0 - 6, 22, wy1 - wy0 + 22); c.fill(); c.rectangle(wx1 - 2, wy0 - 6, 22, wy1 - wy0 + 22); c.fill()
    # 屏风（左）
    for i in range(4):
        x0 = 240 + i * 150
        c.rectangle(x0, 240, 140, 470); c.set_source_rgb(*hx('e6d6b0')); c.fill_preserve(); c.set_source_rgb(*BEAM); c.set_line_width(10); c.stroke()
        for k in range(3):
            y = 360 + k * 110; c.new_path(); c.move_to(x0 + 10, y)
            for j in range(6): c.curve_to(x0 + 10 + j * 22 + 8, y - 30, x0 + 10 + j * 22 + 14, y + 30, x0 + 10 + (j + 1) * 22, y)
            c.set_source_rgba(*hx('5f8f86'), 0.75); c.set_line_width(4); c.stroke()
    # 地板
    c.rectangle(0, 780, W, 300); c.set_source_rgb(*hx('4f351f')); c.fill()
    for y in (820, 880, 960, 1050):
        c.rectangle(0, y, W, 4); c.set_source_rgba(*INK, 0.45); c.fill()
    # 体积光（从窗斜射）
    g = cairo.LinearGradient(1390, 300, 1100, 1000); g.add_color_stop_rgba(0, 1, 0.92, 0.7, 0.32); g.add_color_stop_rgba(1, 1, 0.9, 0.6, 0.0)
    c.new_path(); c.move_to(1090, 260); c.line_to(1690, 260); c.line_to(1500, 1080); c.line_to(560, 1080); c.close_path(); c.set_source(g); c.fill()

def table(c):
    # 长桌 + 长凳（敦煌宴饮图那种长条桌）
    poly(c, [(330, 690), (1600, 690), (1640, 720), (290, 720)], hx('7a4a2a'), 3)
    poly(c, [(290, 720), (1640, 720), (1640, 744), (290, 744)], hx('5a3420'), 3)
    for x in (330, 960, 1600): poly(c, [(x - 12, 744), (x + 12, 744), (x + 10, 860), (x - 10, 860)], hx('4a2a18'), 3)
    # 胡饼、碗、酒壶
    for x in (430, 640, 880, 1120, 1360, 1520):
        ell(c, x, 688, 52, 12, CREAM, 2.6)
    for x in (430, 880, 1360):
        for k in range(3): ell(c, x, 678 - k * 9, 34, 9, hx('d6a050'), 2.2)
    for x in (640, 1120, 1520):
        c.new_path(); c.arc(x, 676, 26, 0, math.pi); fill_stroke(c, hx('3e6a72'), 2.6)
        for k in range(4): ell(c, x - 12 + k * 8, 672, 5, 5, RED, 1.2)
    # 酒瓮
    c.save(); c.translate(1760, 900)
    blob(c, [(-40, 0), (-80, -80), (-84, -160), (-50, -230), (50, -230), (84, -160), (80, -80), (40, 0)], hx('7a4a2e'), 3)
    poly(c, [(-34, -230), (34, -230), (28, -254), (-28, -254)], RED2, 3)
    stroke(c, [(-80, -150), (80, -150)], GOLD, 5, False)
    c.restore()
    # 酒碗
    for x in (560, 1240):
        c.new_path(); c.arc(x, 680, 16, 0, math.pi); fill_stroke(c, CREAM2, 2.4)

def comic(c):
    pass

def caption(c, lines):
    c.select_font_face('Noto Serif CJK SC', 0, 1)
    size = 88; y = 150
    for segs in lines:
        x = 80
        for txt, col in segs:
            c.set_font_size(size)
            ext = c.text_extents(txt)
            for dx, dy, a in ((4, 5, 0.6),):
                c.move_to(x + dx, y + dy); c.set_source_rgba(0.08, 0.04, 0.02, a); c.show_text(txt)
            c.move_to(x, y); c.set_source_rgb(*col); c.show_text(txt)
            if col != CREAM:
                c.rectangle(x, y + 16, ext[4] - 18, 6); c.set_source_rgb(*col); c.fill()
            x += ext[4]
        y += 118
    c.set_font_size(20); c.move_to(24, 34); c.set_source_rgba(*CREAM, 0.6); c.show_text('人物和场面都是示意')

def bubble(c, x, y, txt, s=1.0):
    blob(c, [(x - 70 * s, y), (x - 50 * s, y - 50 * s), (x + 50 * s, y - 52 * s), (x + 74 * s, y - 4 * s), (x + 40 * s, y + 36 * s), (x - 10 * s, y + 38 * s), (x - 40 * s, y + 62 * s), (x - 38 * s, y + 32 * s)], hx('f4ead2'), 3)
    c.select_font_face('Noto Serif CJK SC', 0, 1); c.set_font_size(46 * s); e = c.text_extents(txt)
    c.move_to(x - e[4] / 2, y + 16 * s); c.set_source_rgb(*RED); c.show_text(txt)

def anger(c, x, y, r):
    for k in range(3):
        a0 = k * 2.1
        c.new_path(); c.arc(x, y, r, a0, a0 + 1.2); c.set_source_rgba(*RED, 0.9); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    for k in range(4):
        a = 0.4 + k * 1.57
        stroke(c, [(x + math.cos(a) * 20, y + math.sin(a) * 20), (x + math.cos(a) * 46, y + math.sin(a) * 46)], RED, 7, False)

def exclaim(c, x, y, s=1.0):
    c.select_font_face('Noto Serif CJK SC', 0, 1); c.set_font_size(90 * s)
    c.move_to(x + 3, y + 4); c.set_source_rgba(0, 0, 0, 0.5); c.show_text('！'); c.move_to(x, y); c.set_source_rgb(*hx('f4ead2')); c.show_text('！')

def scene(c):
    room(c)
    # 后排坐着的姐妹（桌后）
    TOPS = [hx('a8b28a'), hx('8fb3b0'), hx('d9b56a'), hx('b7a0c0')]
    SK = [RED, hx('3f5f88'), hx('5f8f6a'), hx('b8503a')]
    back = []
    back.append(woman(c, 330, 900, 470, 1, TOPS[1], SK[1], expr='shock', armN=(0.4, -0.2, 0.3, -1.3), armF=(0.2, 1.0, 0.5, 1.6)))
    back.append(woman(c, 760, 900, 470, 1, TOPS[2], SK[2], expr='grin', armN=(0.6, 0.6, 1.0, 1.4), headtilt=0.1))
    nun = woman(c, 1230, 900, 500, -1, robe=hx('8a4a2c'), shaved=True, expr='stern', armN=(0.8, -0.4, 1.5, -1.0), armF=(0.3, 1.0, 0.7, 1.7))
    back.append(woman(c, 1400, 900, 470, -1, TOPS[3], SK[3], expr='shock', armN=(0.3, -0.3, 0.2, -1.2)))
    table(c)
    # 前排：两人隔桌划拳
    A = woman(c, 520, 1065, 640, 1, TOPS[0], SK[0], lean=0.12, expr='angry', armN=(1.2, -0.2, 2.5, -0.6), armF=(-0.4, 0.9, 0.3, 1.9))
    B = woman(c, 1010, 1065, 640, -1, hx('8fb3b0'), hx('c9873a'), lean=0.12, expr='angry', armN=(1.2, -0.3, 2.4, -0.8), armF=(0.6, 1.0, 1.0, 1.5))
    # 录事：站在右侧捧社条
    L = woman(c, 1600, 1065, 640, -1, hx('d9c38a'), hx('3f5f88'), expr='calm', armN=(0.6, 0.9, 0.9, 1.7), armF=(0.4, 1.0, 0.9, 1.8))
    # 社条卷轴（发金光）
    hxp, hyp = L['n']
    glow(c, hxp - 20, hyp - 70, 220, (1, 0.85, 0.45), 0.45)
    c.save(); c.translate(hxp - 20, hyp - 70); c.rotate(-0.06)
    poly(c, [(-95, -120), (95, -120), (95, 120), (-95, 120)], hx('f1e2bb'), 3)
    for k in range(4):
        for j in range(7): c.rectangle(-66 + k * 30, -70 + j * 24, 5, 13); c.set_source_rgba(*INK, 0.5); c.fill()
    c.select_font_face('Noto Serif CJK SC', 0, 1); c.set_font_size(48); c.set_source_rgb(*RED2)
    c.move_to(46, -64); c.show_text('社'); c.move_to(46, -12); c.show_text('条')
    for yy in (-128, 120): poly(c, [(-108, yy), (108, yy), (108, yy + 14), (-108, yy + 14)], RED2, 2.4)
    c.restore()
    # 漫画符号
    mx = (A['n'][0] + B['n'][0]) / 2; my = (A['n'][1] + B['n'][1]) / 2
    glow(c, mx, my, 120, (1, 0.6, 0.3), 0.5)
    anger(c, mx, my - 10, 60)
    bubble(c, A['head'][0] + 30, A['head'][1] - 30, '…!', 0.9)
    bubble(c, B['head'][0] - 10, B['head'][1] - 40, '…?!', 0.9)
    exclaim(c, back[0]['head'][0] - 10, back[0]['head'][1] - 10, 0.8)
    exclaim(c, back[2]['head'][0] - 10, back[2]['head'][1] - 10, 0.8)
    # 尘粒
    r = np.random.default_rng(3)
    for i in range(60):
        x, y = r.uniform(600, 1700), r.uniform(250, 1000); glow(c, x, y, r.uniform(3, 7), (1, 0.92, 0.7), r.uniform(0.3, 0.7))
    return dict(A=A, B=B, L=L, nun=nun)

def render(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    scene(c)
    # 暗角
    g = cairo.RadialGradient(W / 2, H / 2, 380, W / 2, H / 2, 1150); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.06, 0.03, 0.01, 0.75)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    # 冲突：整体偏红
    c.rectangle(0, 0, W, H); c.set_source_rgba(0.6, 0.15, 0.05, 0.08); c.fill()
    caption(c, [[('席上划拳，', CREAM), ('谁劝都不听', hx('e8643a')), ('，', CREAM)],
                [('按社条：', CREAM), ('罚她请全社吃一桌', GOLD), ('。', CREAM)]])
    s.flush()
    a = np.ndarray((H, W, 4), np.uint8, s.get_data())[..., [2, 1, 0]].copy()
    im = Image.fromarray(a)
    # 轻 bloom
    bl = im.filter(ImageFilter.GaussianBlur(18)); arr = np.asarray(im).astype(np.float32); b = np.asarray(bl).astype(np.float32)
    lum = b.mean(2, keepdims=True); arr = np.clip(arr + np.clip(lum - 170, 0, None) / 85 * b * 0.18, 0, 255)
    Image.fromarray(arr.astype(np.uint8)).save(path, quality=92)


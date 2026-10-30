# 近现代剪影人物与道具（杨振宁一期专用）
from kit import *
import math, random

def man(c, x, y, s=1.0, pose='stand', face=1, a=1.0, col=INK, p=1.0, t=0, glasses=False,
        kid=False, old=0.0, suit=True, gown=False, hair='short', walk=0.0):
    """近现代男子剪影。y=脚底。pose: stand walk point write hold raise fist wipe bow sit behind wave"""
    c.save(); c.translate(x, y); c.scale(s * face, s)
    q = ease(p)
    lean = old * 0.10 + (0.35 * q if pose == 'bow' else 0) + (0.06 if pose == 'wipe' else 0)
    c.set_source_rgba(*col, a)
    # 腿
    sw = math.sin(walk * 6.2832) * 0.35 if pose == 'walk' else 0
    if pose == 'sit':
        poly(c, [(-30, -95), (10, -95), (70, -90), (70, -70), (5, -68)], col, a)
        poly(c, [(50, -90), (72, -90), (70, 0), (52, 0)], col, a)
        c.rectangle(-60, -100, 120, 10); c.fill()  # 椅面
        c.rectangle(-58, -100, 8, 100); c.fill(); c.rectangle(50, -100, 8, 100); c.fill()
        c.rectangle(-60, -230, 8, 135); c.fill()  # 椅背
        hipy = -100
    elif gown:
        c.move_to(-40, 0); c.line_to(44, 0); c.curve_to(40, -40, 34, -80, 30, -110); c.line_to(-28, -110); c.curve_to(-34, -80, -42, -40, -40, 0); c.fill()
        hipy = -100
    else:
        for k, ph in ((0, sw), (1, -sw)):
            c.save(); c.translate(-12 + k * 24, -100); c.rotate(ph)
            poly(c, [(-13, 0), (13, 0), (11, 100), (-11, 100)], col, a)
            c.rectangle(-11, 92, 30, 9); c.fill()
            c.restore()
        hipy = -100
    # 躯干
    c.save(); c.translate(0, hipy); c.rotate(lean)
    if gown:
        poly(c, [(-34, 0), (34, 0), (30, -118), (-30, -118)], col, a)
    else:
        poly(c, [(-34, 8), (34, 8), (32, -112), (-32, -112)], col, a)
    # 头
    hy = -150 - old * 4
    c.rectangle(-9, -126, 18, 16); c.fill()
    c.arc(4, hy, 27, 0, 6.2832); c.fill()
    if hair == 'short':
        c.arc(0, hy - 6, 28, 3.3, 6.0); c.fill()
    if old > 0.5:
        c.set_source_rgba(0.75, 0.75, 0.72, 0.55 * a); c.set_line_width(4); c.arc(0, hy - 4, 27, 3.5, 5.6); c.stroke()
        c.set_source_rgba(*col, a)
    if glasses:
        c.set_source_rgba(*GOLD, 0.75 * a); c.set_line_width(2.2)
        c.arc(22, hy + 2, 7, 0, 6.28); c.stroke(); c.move_to(15, hy + 1); c.line_to(-6, hy - 2); c.stroke()
        c.set_source_rgba(*col, a)
    # 领口高光（西装/中山装）
    if suit and not gown:
        c.set_source_rgba(0.55, 0.42, 0.30, 0.35 * a); c.set_line_width(2)
        c.move_to(-12, -110); c.line_to(0, -70); c.line_to(12, -110); c.stroke()
        c.set_source_rgba(*col, a)
    # 手臂
    c.set_line_width(20); c.set_line_cap(1); c.set_line_join(1)
    sx, sy = 18, -104
    def arm(pts):
        c.move_to(sx, sy)
        for pt in pts: c.line_to(*pt)
        c.stroke(); c.arc(pts[-1][0], pts[-1][1], 11, 0, 6.28); c.fill()
    if pose in ('stand', 'sit', 'bow'): arm([(26, -55), (22, -12)])
    elif pose == 'walk': arm([(18 + 30 * sw, -55), (18 + 50 * sw, -15)])
    elif pose == 'point': arm([(lerp(26, 60, q), lerp(-55, -100, q)), (lerp(22, 110, q), lerp(-12, -120, q))])
    elif pose == 'write':
        wy = math.sin(t * 9) * 8
        arm([(55, -120), (lerp(70, 95, q), -175 + wy)])
    elif pose == 'hold': arm([(40, -70), (70, -82)])
    elif pose == 'raise': arm([(lerp(26, 34, q), lerp(-55, -170, q)), (lerp(22, 42, q), lerp(-12, -240, q))])
    elif pose == 'fist': arm([(40, -150), (60, -230)])
    elif pose == 'wipe': arm([(48, -90), (lerp(22, 30, q), lerp(-12, -145, q))])
    elif pose == 'behind': arm([(10, -60), (-18, -40)])
    elif pose == 'wave': arm([(48, -150), (60 + 12 * math.sin(t * 8), -215)])
    elif pose == 'offer': arm([(lerp(26, 60, q), lerp(-55, -85, q)), (lerp(22, 105, q), lerp(-12, -92, q))])
    # 后手
    c.set_source_rgba(*col, a)
    if pose in ('hold',): c.move_to(-14, -104); c.line_to(10, -70); c.line_to(60, -78); c.stroke()
    elif pose == 'walk': c.move_to(-14, -104); c.line_to(-14 - 30 * sw, -55); c.line_to(-14 - 50 * sw, -15); c.stroke()
    elif pose not in ('behind',): c.move_to(-14, -104); c.line_to(-22, -55); c.line_to(-18, -12); c.stroke()
    else: c.move_to(-14, -104); c.line_to(-26, -60); c.line_to(-8, -42); c.stroke()
    c.restore()
    if old > 0.6 and pose not in ('sit',):  # 手杖
        c.set_source_rgba(*col, a); c.set_line_width(6); c.move_to(48, -95); c.line_to(58, 0); c.stroke()
    c.restore()

def woman(c, x, y, s=1, face=1, a=1, col=INK, pose='stand', p=1, t=0):
    """旗袍女子剪影（吴健雄）"""
    c.save(); c.translate(x, y); c.scale(s * face, s); c.set_source_rgba(*col, a)
    c.move_to(-26, 0); c.line_to(26, 0); c.curve_to(30, -60, 22, -110, 30, -150); c.curve_to(34, -190, 26, -205, 22, -212)
    c.line_to(-22, -212); c.curve_to(-30, -190, -32, -160, -26, -140); c.curve_to(-18, -100, -30, -50, -26, 0); c.fill()
    c.rectangle(-8, -228, 16, 18); c.fill(); c.arc(3, -250, 25, 0, 6.28); c.fill(); c.arc(-20, -258, 13, 0, 6.28); c.fill()
    c.set_line_width(16); c.set_line_cap(1); q = ease(p)
    if pose == 'reach': c.move_to(16, -200); c.line_to(lerp(30, 70, q), lerp(-140, -170, q)); c.line_to(lerp(26, 110, q), lerp(-100, -175, q))
    else: c.move_to(16, -200); c.line_to(30, -150); c.line_to(26, -105)
    c.stroke(); c.restore()

def crowd_m(c, y, n=12, s=0.7, x0=150, x1=1770, a=1, seed=1, t=0, clap=0):
    rnd = random.Random(seed)
    for i in range(n):
        x = lerp(x0, x1, i / max(1, n - 1)) + rnd.uniform(-20, 20)
        pz = 'raise' if (clap and rnd.random() < 0.4) else 'stand'
        man(c, x, y + rnd.uniform(-6, 6), s * rnd.uniform(0.9, 1.08), pose=pz, face=1 if x < W / 2 else -1, a=a, p=clap, hair='short')

def mirror(c, x, y, s=1, a=1, lit=1, crack=0.0, t=0, shards=0.0, seed=4):
    """贯穿全片的发光主体：一面椭圆镜（宇称=镜像对称）"""
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, 0, 420, (0.9, 0.95, 1.0), 0.38 * lit * a)
    glow(c, 0, 0, 240, (1.0, 0.9, 0.7), 0.30 * lit * a)
    if shards <= 0:
        c.set_source_rgba(0.10, 0.08, 0.06, a); c.save(); c.scale(1, 1.3); c.arc(0, 0, 150, 0, 6.28); c.restore(); c.fill()
        g = cairo.RadialGradient(-40, -60, 10, 0, 0, 180)
        g.add_color_stop_rgba(0, 0.98, 0.98, 1.0, a * (0.6 + 0.4 * lit)); g.add_color_stop_rgba(1, 0.55, 0.65, 0.78, a * (0.6 + 0.4 * lit))
        c.set_source(g); c.save(); c.scale(1, 1.3); c.arc(0, 0, 132, 0, 6.28); c.restore(); c.fill()
        c.set_source_rgba(1, 1, 1, 0.5 * a); c.set_line_width(4); c.save(); c.scale(1, 1.3); c.arc(0, 0, 118, 3.7, 4.6); c.restore(); c.stroke()
        if crack > 0:
            rnd = random.Random(seed); c.set_source_rgba(1, 1, 1, a); c.set_line_width(3)
            for k in range(9):
                an = k * 6.28 / 9 + rnd.uniform(-0.2, 0.2); L_ = 170 * crack * rnd.uniform(0.6, 1)
                c.move_to(0, 0); px, py = 0, 0
                for j in range(4):
                    px += math.cos(an + rnd.uniform(-0.4, 0.4)) * L_ / 4; py += math.sin(an + rnd.uniform(-0.4, 0.4)) * L_ / 4 * 1.3
                    c.line_to(px, py)
                c.stroke()
            glow(c, 0, 0, 200, (1, 1, 1), 0.6 * crack * a)
    else:
        rnd = random.Random(seed)
        for k in range(26):
            an = rnd.uniform(0, 6.28); r0 = rnd.uniform(10, 130)
            sp = rnd.uniform(400, 1300) * shards
            cx = math.cos(an) * (r0 + sp); cy = math.sin(an) * (r0 + sp) * 1.3 + 300 * shards * shards
            rot = rnd.uniform(-3, 3) * shards
            c.save(); c.translate(cx, cy); c.rotate(rot); sz = rnd.uniform(18, 46)
            col = (0.85 + 0.15 * rnd.random(), 0.92, 1.0)
            poly(c, [(-sz, -sz * 0.4), (sz * 0.7, -sz), (sz * 0.5, sz * 0.8), (-sz * 0.6, sz * 0.5)], col, a * (1 - shards * 0.5))
            c.restore()
        glow(c, 0, 0, 500 * (0.5 + shards), (1, 1, 1), 0.7 * (1 - shards) * a)
    c.restore()

def rays(c, x, y, k, col=GOLD, n=24, r=1400, a=0.5, rot=0):
    if k <= 0: return
    for i in range(n):
        an = i * 6.2832 / n + rot
        c.move_to(x, y); c.line_to(x + math.cos(an - 0.035) * r, y + math.sin(an - 0.035) * r)
        c.line_to(x + math.cos(an + 0.035) * r, y + math.sin(an + 0.035) * r); c.close_path()
        c.set_source_rgba(*col, a * k * (0.5 + 0.5 * (i % 2))); c.fill()

def sparks(c, t, x, y, n=60, col=GOLD, spread=900, seed=9, a=1, k=1):
    rnd = random.Random(seed)
    for i in range(n):
        an = rnd.uniform(0, 6.28); sp = rnd.uniform(0.3, 1) * spread
        tt = (t * rnd.uniform(0.6, 1.4) + rnd.random()) % 1
        px = x + math.cos(an) * sp * tt; py = y + math.sin(an) * sp * tt
        c.set_source_rgba(*col, a * k * (1 - tt)); c.arc(px, py, rnd.uniform(2, 5) * (1 - tt * 0.5), 0, 6.28); c.fill()

def ground(c, y=880, col=INK): c.set_source_rgb(*col); c.rectangle(0, y, W, H - y + 400); c.fill()

def auditorium(c, x, y, s=1, col=INK, a=1, lit=0):
    """清华大礼堂式穹顶建筑剪影（示意）"""
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-300, 0), (300, 0), (300, -220), (-300, -220)], col, a)
    poly(c, [(-130, -220), (130, -220), (0, -320)], col, a)
    c.set_source_rgba(*col, a); c.arc(0, -330, 120, 3.1416, 6.2832); c.fill(); c.rectangle(-120, -340, 240, 20); c.fill()
    c.rectangle(-8, -470, 16, 30); c.fill(); c.arc(0, -455, 22, 3.14, 6.28); c.fill()
    for i in range(4):
        xx = -90 + i * 60
        c.set_source_rgba(1, 0.75, 0.4, lit * 0.8 * a) if lit else c.set_source_rgba(0.3, 0.22, 0.15, 0.35 * a)
        c.rectangle(xx - 14, -180, 28, 120); c.fill()
    c.restore()

def ship(c, x, y, s=1, a=1, t=0, col=INK):
    c.save(); c.translate(x, y + math.sin(t * 1.4) * 4); c.scale(s, s); c.rotate(math.sin(t * 1.1) * 0.012)
    poly(c, [(-420, -60), (420, -60), (360, 40), (-380, 40)], col, a)
    poly(c, [(-260, -60), (220, -60), (200, -150), (-240, -150)], col, a)
    poly(c, [(-160, -150), (120, -150), (110, -220), (-150, -220)], col, a)
    c.set_source_rgba(*col, a); c.rectangle(-40, -320, 60, 110); c.fill()
    for i in range(10):
        c.set_source_rgba(1, 0.8, 0.45, 0.7 * a); c.arc(-220 + i * 46, -105, 7, 0, 6.28); c.fill()
    c.restore()
    for k in range(5):
        tt = (t * 0.25 + k * 0.2) % 1
        c.set_source_rgba(0.3, 0.3, 0.32, 0.35 * (1 - tt) * a); c.arc(x - 10 * s - tt * 160 * s, y - 330 * s - tt * 220 * s, (30 + tt * 70) * s, 0, 6.28); c.fill()

def plane(c, x, y, s=1, a=1, col=INK):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(*col, a); c.save(); c.scale(1, 0.16); c.arc(0, 0, 170, 0, 6.28); c.restore(); c.fill()
    poly(c, [(-30, 0), (40, 0), (-60, 130), (-100, 130)], col, a); poly(c, [(-30, 0), (40, 0), (-60, -130), (-100, -130)], col, a)
    poly(c, [(-140, 0), (-120, 0), (-170, -60), (-185, -60)], col, a)
    c.restore()

def bomber(c, x, y, s=1, a=1):
    plane(c, x, y, s, a)

def blackboard(c, x, y, w, h, a=1):
    c.set_source_rgba(0.05, 0.07, 0.06, a); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgba(0.35, 0.25, 0.15, a); c.set_line_width(10); c.rectangle(x, y, w, h); c.stroke()

def chalk(c, s, x, y, size, k, col=(0.92, 0.95, 0.9), a=1, font="Noto Serif CJK SC"):
    """逐字写出的粉笔公式（ASCII/符号）"""
    n = int(len(s) * cl(k))
    if n <= 0: return
    c.select_font_face(font, cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
    c.set_source_rgba(*col, a); c.move_to(x, y); c.show_text(s[:n])

def mushroom(c, x, y, k, t, a=1, s=1):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    hgt = 520 * ease(k)
    glow(c, 0, -hgt, 600 * ease(k), (1, 0.75, 0.4), 0.55 * a)
    c.set_source_rgba(0.85, 0.55, 0.30, 0.9 * a)
    c.move_to(-50, 0); c.curve_to(-40, -hgt * 0.5, -60, -hgt * 0.8, -70, -hgt + 40); c.line_to(70, -hgt + 40); c.curve_to(60, -hgt * 0.8, 40, -hgt * 0.5, 50, 0); c.fill()
    rnd = random.Random(3)
    for i in range(24):
        an = rnd.uniform(3.2, 6.2); r = rnd.uniform(60, 220) * ease(k)
        cx = math.cos(an) * r * 1.3; cy = -hgt + math.sin(an) * r * 0.5
        col = mix((1, 0.85, 0.55), (0.55, 0.30, 0.20), rnd.random())
        c.set_source_rgba(*col, 0.85 * a); c.arc(cx, cy, rnd.uniform(60, 120) * ease(k), 0, 6.28); c.fill()
    c.set_source_rgba(0.7, 0.45, 0.30, 0.7 * a); c.save(); c.scale(1, 0.25); c.arc(0, 0, 420 * ease(k), 0, 6.28); c.restore(); c.fill()
    c.restore()

def letter(c, x, y, s=1, a=1, lit=1, lines=7, k=1, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    glow(c, 0, 0, 300, (1, 0.88, 0.62), 0.45 * lit * a)
    c.set_source_rgba(0.93, 0.89, 0.78, a); c.rectangle(-150, -200, 300, 400); c.fill()
    c.set_source_rgba(0.75, 0.15, 0.12, 0.6 * a); c.set_line_width(2)
    for i in range(lines + 1): c.move_to(-130 + i * 260 / lines, -180); c.line_to(-130 + i * 260 / lines, 180)
    c.stroke()
    c.set_source_rgba(0.15, 0.12, 0.10, 0.85 * a); c.set_line_width(5)
    for i in range(lines):
        hh = 330 * cl(k * lines - i)
        if hh > 0:
            xx = 130 - 260 / lines * (i + 0.5)
            yy = -170
            while yy < -170 + hh:
                c.move_to(xx - 8, yy); c.line_to(xx + 8, yy + 6); yy += 26
            c.stroke()
    c.restore()

def bouquet(c, x, y, s=1, a=1, t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(*INK, a); c.set_line_width(4)
    for i in range(9):
        an = -1.57 + (i - 4) * 0.13; c.move_to(0, 0); c.line_to(math.cos(an) * 160, math.sin(an) * 160); c.stroke()
    rnd = random.Random(2)
    for i in range(12):
        an = -1.57 + rnd.uniform(-0.6, 0.6); r = rnd.uniform(140, 200)
        col = [(0.95, 0.92, 0.88), (0.92, 0.55, 0.55), (0.98, 0.85, 0.55)][i % 3]
        c.set_source_rgba(*col, 0.92 * a); c.arc(math.cos(an) * r, math.sin(an) * r, rnd.uniform(16, 26), 0, 6.28); c.fill()
    c.restore()

def window(c, x, y, w, h, light=(0.85, 0.85, 0.95), a=1):
    c.set_source_rgba(*light, 0.55 * a); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgba(*INK, a); c.set_line_width(10); c.rectangle(x, y, w, h); c.stroke()
    c.move_to(x + w / 2, y); c.line_to(x + w / 2, y + h); c.move_to(x, y + h / 2); c.line_to(x + w, y + h / 2); c.stroke()

def chandelier(c, x, y, s=1, a=1, t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(*INK, a); c.set_line_width(3); c.move_to(0, -300); c.line_to(0, 0); c.stroke()
    for i in range(7):
        xx = (i - 3) * 40; yy = 20 + abs(i - 3) * -6
        glow(c, xx, yy, 60, (1, 0.85, 0.55), 0.55 * a)
        c.set_source_rgba(1, 0.9, 0.7, a); c.arc(xx, yy, 6, 0, 6.28); c.fill()
    c.restore()

def tinroof(c, y0, t, rain=1.0, a=1):
    c.set_source_rgb(0.06, 0.06, 0.07); c.rectangle(0, 0, W, y0); c.fill()
    c.set_source_rgba(0.45, 0.45, 0.48, 0.5 * a); c.set_line_width(2)
    for i in range(0, W, 38): c.move_to(i, 0); c.line_to(i + 20, y0); 
    c.stroke()
    rnd = random.Random(8)
    for i in range(int(160 * rain)):
        xx = (rnd.uniform(0, W) + t * 60) % W; yy = (rnd.uniform(y0, H) + t * rnd.uniform(900, 1300)) % (H - y0) + y0
        c.set_source_rgba(0.7, 0.75, 0.85, 0.28); c.set_line_width(2); c.move_to(xx, yy); c.line_to(xx - 6, yy + 34); c.stroke()

def nametag(c, s, x, y, a=1, col=(0.92, 0.88, 0.80), size=40):
    text(c, s, x, y, size, col, a, 'c')

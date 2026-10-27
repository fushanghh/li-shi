# 假如你是孙中山 —— 第一视角镜头（你=孙中山，镜头是你的眼睛和双手；全片唯一发光物：青天白日旗）
from kit import *
from pov import arm, bg, ground, eyelids, rain, fog, table, label, bust, tree, cup
import math, random

BLUE = (0.10, 0.22, 0.62); BLUE_LIT = (0.20, 0.42, 0.95); SUNW = (1.0, 0.98, 0.92)
FLAGGLOW = (0.55, 0.70, 1.0)
CNT_AT = {'die1': 1.7, 'yangdie': 0.5, 'hhg2': 0.9}

def sm(x): return ease(x)

# ================= 发光主体：青天白日旗 =================
def sun_emblem(c, x, y, r, lit, a=1.0):
    col_w = mix((0.35, 0.35, 0.38), SUNW, lit); col_b = mix((0.06, 0.08, 0.14), BLUE_LIT, lit)
    c.save(); c.translate(x, y)
    for k in range(12):
        an = k * math.pi / 6
        c.move_to(math.cos(an) * r, math.sin(an) * r)
        c.line_to(math.cos(an + 0.16) * r * 0.52, math.sin(an + 0.16) * r * 0.52)
        c.line_to(math.cos(an - 0.16) * r * 0.52, math.sin(an - 0.16) * r * 0.52); c.close_path()
    c.set_source_rgba(*col_w, a); c.fill()
    c.set_source_rgba(*col_b, a); c.arc(0, 0, r * 0.5, 0, 6.2832); c.fill()
    c.set_source_rgba(*col_w, a); c.arc(0, 0, r * 0.42, 0, 6.2832); c.fill()
    c.restore()

def flagcloth(c, x, y, w, h, t, lit=1.0, amp=14, a=1.0, glowk=1.0, n=36):
    """旗面左缘中点在(x,y)，向右展开"""
    if lit > 0:
        glow(c, x + w * 0.5, y, w * 1.25, FLAGGLOW, 0.32 * lit * a * glowk)
        glow(c, x + w * 0.5, y, w * 0.45, (1, 1, 0.95), 0.25 * lit * a * glowk)
    sw = w / n
    def dy(i): q = i / n; return math.sin(t * 3.2 - i * 0.35) * amp * q
    for i in range(n):
        x0 = x + i * sw; y0 = dy(i); y1 = dy(i + 1)
        shade = 0.82 + 0.18 * math.cos(t * 3.2 - i * 0.35)
        col = tuple(v * shade for v in mix((0.05, 0.07, 0.14), BLUE_LIT, lit))
        c.move_to(x0, y + y0 - h / 2); c.line_to(x0 + sw + 0.8, y + y1 - h / 2)
        c.line_to(x0 + sw + 0.8, y + y1 + h / 2); c.line_to(x0, y + y0 + h / 2); c.close_path()
        c.set_source_rgba(*col, a); c.fill()
    sun_emblem(c, x + w / 2, y + dy(n // 2), h * 0.34, lit, a)

def flag_on_pole(c, x, y, L, w, t, lit=1.0, a=1.0, glowk=1.0):
    """杆底(x,y)，杆长L"""
    c.set_source_rgba(*INK, a); c.set_line_width(max(4, w * 0.03)); c.move_to(x, y); c.line_to(x, y - L); c.stroke()
    flagcloth(c, x, y - L + w * 0.33, w, w * 0.66, t, lit, amp=w * 0.04, a=a, glowk=glowk)

def held_flag(c, lt, x=1500, y=1000, L=330, w=240, lit=0.9, glowk=1.0):
    arm(c, x + 280, y + 330, x, y, w0=140, w1=48, hand='fist', col=(0.025, 0.025, 0.03))
    flag_on_pole(c, x + 4, y + 30, L, w, lt, lit, glowk=glowk)

def folded_flag(c, x, y, s, lit, t):
    glow(c, x, y, 220 * s, FLAGGLOW, 0.35 * lit)
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-110, -40), (110, -40), (120, 40), (-100, 40)], mix((0.05, 0.07, 0.14), BLUE_LIT, lit))
    sun_emblem(c, 0, 0, 32, lit)
    c.restore()

# ================= 粒子 =================
def embers(c, t, n=60, seed=5, a=0.8, x0=0, x1=W, y0=H, h=H, col=(1, 0.55, 0.15)):
    rnd = random.Random(seed)
    for i in range(n):
        sp = rnd.uniform(60, 180); ph = rnd.uniform(0, 10)
        y = y0 - ((t * sp + ph * 100) % h); x = rnd.uniform(x0, x1) + math.sin(t * 2 + i) * 20
        r = rnd.uniform(1.5, 3.5); fl = 0.5 + 0.5 * math.sin(t * 9 + i)
        c.set_source_rgba(*col, a * fl * (y - (y0 - h)) / h); c.arc(x, y, r, 0, 6.28); c.fill()

def smoke(c, t, y=600, n=10, a=0.35, seed=3, col=(0.12, 0.10, 0.10)):
    rnd = random.Random(seed)
    for i in range(n):
        x = (rnd.uniform(-300, W + 300) + t * rnd.uniform(15, 45)) % (W + 600) - 300
        yy = y + rnd.uniform(-250, 200) - t * 8; r = rnd.uniform(250, 480)
        g = cairo.RadialGradient(x, yy, 0, x, yy, r)
        g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
        c.set_source(g); c.arc(x, yy, r, 0, 6.28); c.fill()

def puddles(c, t, y=900, col=(1, 0.55, 0.2), a=0.18, seed=4):
    rnd = random.Random(seed)
    for i in range(14):
        x = rnd.uniform(0, W); w = rnd.uniform(80, 260); yy = y + rnd.uniform(0, 160)
        c.set_source_rgba(*col, a * (0.6 + 0.4 * math.sin(t * 3 + i))); c.rectangle(x, yy, w, 3); c.fill()

def gaslamp(c, x, y, s=1, t=0, a=1):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(*INK, a); c.rectangle(-7, -420, 14, 420); c.fill()
    poly(c, [(-28, -470), (28, -470), (20, -420), (-20, -420)], INK, a)
    poly(c, [(-34, -470), (34, -470), (0, -505)], INK, a)
    k = 0.85 + 0.15 * math.sin(t * 7)
    c.set_source_rgba(1, 0.78, 0.45, 0.75 * a * k); c.rectangle(-18, -465, 36, 40); c.fill()
    c.restore()
    glow(c, x, y - 445 * s, 170 * s, (1, 0.7, 0.35), 0.16 * a * k)

def torch(c, x, y, t, s=1, a=1, seed=0):
    c.set_source_rgba(*INK, a); c.set_line_width(7 * s); c.move_to(x, y); c.line_to(x + 8 * s, y - 120 * s); c.stroke()
    glow(c, x + 8 * s, y - 140 * s, 160 * s, (1, 0.5, 0.15), 0.22 * a)
    flame(c, x + 8 * s, y - 120 * s, 50 * s, t, seed, a)

def lingnan_houses(c, base=760, col=(0.03, 0.03, 0.04), seed=2):
    rnd = random.Random(seed); x = -100
    while x < W + 100:
        w = rnd.uniform(180, 300); h = rnd.uniform(200, 320)
        c.set_source_rgb(*col); c.rectangle(x, base - h, w, h + 600); c.fill()
        # 镬耳墙
        c.move_to(x, base - h); c.curve_to(x, base - h - 90, x + w * 0.5, base - h - 140, x + w * 0.5, base - h - 140)
        c.curve_to(x + w * 0.5, base - h - 140, x + w, base - h - 90, x + w, base - h); c.close_path(); c.fill()
        x += w + rnd.uniform(-20, 30)

def tonglau(c, x, base, w, h, t, lit=(), col=(0.03, 0.03, 0.035)):
    c.set_source_rgb(*col); c.rectangle(x, base - h, w, h + 600); c.fill()
    fl = int(h // 170)
    for f in range(fl):
        yy = base - (f + 1) * 170
        c.set_source_rgba(0.12, 0.11, 0.10, 0.9); c.rectangle(x - 18, yy + 120, w + 36, 8); c.fill()  # 露台
        for k in range(int(w // 22)): c.rectangle(x - 14 + k * 22, yy + 92, 3, 30); c.fill()
        for j in range(3):
            wx = x + 30 + j * (w - 60) / 3
            if (f, j) in lit:
                k = 0.85 + 0.15 * math.sin(t * 4 + j)
                c.set_source_rgba(0.95, 0.65, 0.30, 0.7 * k); c.rectangle(wx, yy + 20, (w - 60) / 3 - 20, 70); c.fill()
                glow(c, wx + 30, yy + 55, 120, (1, 0.6, 0.25), 0.10)
            else:
                c.set_source_rgba(0.07, 0.07, 0.08, 1); c.rectangle(wx, yy + 20, (w - 60) / 3 - 20, 70); c.fill()
    # 骑楼拱
    c.set_source_rgb(0, 0, 0)
    for k in range(3):
        ax = x + 20 + k * (w - 40) / 3; aw = (w - 40) / 3 - 18
        c.rectangle(ax, base - 120, aw, 120); c.fill(); c.arc(ax + aw / 2, base - 120, aw / 2, math.pi, 2 * math.pi); c.fill()

def terraces(c, base=900, col=(0.06, 0.05, 0.05), lit=(), t=0, seed=1):
    """伦敦乔治式联排：砖墙+窗格"""
    c.set_source_rgb(*col); c.rectangle(-200, base - 820, W + 400, 900); c.fill()
    for k in range(40):
        c.set_source_rgba(0.12, 0.08, 0.07, 0.35); c.rectangle(-200, base - 820 + k * 22, W + 400, 1.5); c.fill()
    for fy in (base - 720, base - 520, base - 330):
        for i in range(9):
            wx = -60 + i * 240
            c.set_source_rgba(0.02, 0.02, 0.025, 1); c.rectangle(wx, fy, 110, 150); c.fill()
            if (fy, i) in lit:
                c.set_source_rgba(0.85, 0.62, 0.32, 0.55); c.rectangle(wx + 6, fy + 6, 98, 138); c.fill()
            c.set_source_rgba(*col, 1); c.rectangle(wx + 52, fy, 6, 150); c.rectangle(wx, fy + 72, 110, 6); c.fill()
    # 铁栏杆
    c.set_source_rgba(0.01, 0.01, 0.01, 1)
    for k in range(0, W + 40, 18): c.rectangle(k, base - 60, 3, 60); c.fill()
    c.rectangle(0, base - 60, W, 4); c.fill()

def harbor(c, t, base=720):
    bg(c, [(0, (0.03, 0.05, 0.09)), (0.55, (0.10, 0.14, 0.20)), (1, (0.02, 0.03, 0.05))])
    stars(c, t, 60, seed=4, ymax=400, a=0.5)
    # 太平山
    poly(c, [(-100, base), (200, base - 150), (520, base - 330), (760, base - 280), (1000, base - 360), (1300, base - 220), (1700, base - 160), (2100, base)], (0.04, 0.05, 0.07))
    rnd = random.Random(7)
    for i in range(160):
        x = rnd.uniform(0, W); y = base - rnd.uniform(0, 140) * (1 - abs(x - 900) / 1400)
        c.set_source_rgba(1, 0.75, 0.4, 0.35 + 0.3 * math.sin(t * 2 + i)); c.arc(x, y, rnd.uniform(1, 2.2), 0, 6.28); c.fill()
    vgrad(c, base, H, [(0, (0.04, 0.06, 0.09)), (1, (0.01, 0.015, 0.02))])
    for i in range(30):
        yy = base + 10 + i * 12
        c.set_source_rgba(1, 0.7, 0.35, 0.06); c.rectangle(rnd.uniform(0, W), yy, rnd.uniform(60, 200), 2); c.fill()

def steamship(c, x, y, s, t, a=1, whistle=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-300, -40), (300, -40), (260, 20), (-270, 20)], INK, a)
    c.set_source_rgba(*INK, a); c.rectangle(-180, -90, 300, 50); c.fill()
    c.rectangle(-40, -190, 44, 100); c.fill()
    c.set_line_width(5); c.move_to(-240, -40); c.line_to(-240, -260); c.move_to(200, -40); c.line_to(200, -230); c.stroke()
    for k in range(6):
        c.set_source_rgba(1, 0.75, 0.4, 0.5 * a); c.arc(-150 + k * 45, -65, 5, 0, 6.28); c.fill()
    for k in range(5):  # 烟
        q = (t * 0.4 + k * 0.2) % 1
        g = cairo.RadialGradient(-18 - q * 260, -200 - q * 160, 0, -18 - q * 260, -200 - q * 160, 40 + q * 90)
        g.add_color_stop_rgba(0, 0.25, 0.25, 0.27, 0.35 * (1 - q) * a); g.add_color_stop_rgba(1, 0.25, 0.25, 0.27, 0)
        c.set_source(g); c.arc(-18 - q * 260, -200 - q * 160, 40 + q * 90, 0, 6.28); c.fill()
    if whistle > 0:  # 汽笛白汽
        for k in range(4):
            r = 20 + whistle * 70 + k * 18
            c.set_source_rgba(0.85, 0.88, 0.9, 0.45 * (1 - whistle) * a); c.arc(10 + k * 16, -200 - whistle * 40 - k * 10, r, 0, 6.28); c.fill()
    c.restore()

def window_bars(c, x, y, w, h, n=5, col=INK, frame=40):
    c.set_source_rgb(*col)
    c.rectangle(x - frame, y - frame, w + 2 * frame, frame); c.rectangle(x - frame, y + h, w + 2 * frame, frame)
    c.rectangle(x - frame, y, frame, h); c.rectangle(x + w, y, frame, h); c.fill()
    for k in range(1, n): c.rectangle(x + k * w / n - 6, y, 12, h); c.fill()

def reach(c, q, tx, ty, fromx=1250, fromy=1250, close=0.0, a=1.0):
    """你的手去够 (tx,ty)；q 伸出进度，close 握空"""
    x1 = lerp(fromx - 60, tx, sm(q)); y1 = lerp(fromy + 80, ty, sm(q))
    arm(c, fromx, fromy, x1, y1, w0=150, w1=50, hand=('fist' if close > 0.5 else 'open'), col=(0.025, 0.025, 0.03), rim=0.25, a=a)

def name(c, s, x, y, size=46, a=1, col=(0.95, 0.88, 0.72)):
    y = max(y, 440)
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    w = c.text_extents(s)[4]
    c.set_source_rgba(0, 0, 0, 0.45 * a); rr(c, x - w / 2 - 16, y - size - 6, w + 32, size + 24, 8); c.fill()
    c.set_source_rgba(*GOLD, 0.8 * a); c.rectangle(x - w / 2 - 16, y + 12, w + 32, 2); c.fill()
    text(c, s, x, y, size, col, a, 'c')

def paperstrokes(c, x, y, w, h, prog, seed=1, col=(0.08, 0.06, 0.05), cols=10):
    rnd = random.Random(seed); cw = w / cols; tot = cols * 12; k = 0
    for j in range(cols):
        cx = x + w - (j + 0.5) * cw
        for i in range(12):
            k += 1
            if k / tot > prog: return
            yy = y + 20 + i * (h - 40) / 12
            c.set_source_rgba(*col, 0.85); c.rectangle(cx - rnd.uniform(6, 14), yy, rnd.uniform(12, 28), rnd.uniform(10, 20)); c.fill()

def post(c, key, lt, d, p):
    # 冷暖调色
    tone = {'leak': (0.0, 0.03, 0.08, 0.10), 'london': (0.05, 0.06, 0.08, 0.10), 'charge': (0.25, 0.08, 0.0, 0.10),
            'nanjing': (0.25, 0.18, 0.05, 0.08), 'twist': (0.25, 0.18, 0.08, 0.18)}.get(key)
    if tone: c.set_source_rgba(*tone); c.paint()
    if key == 'twist':  # 胶片颗粒+划痕
        rnd = random.Random(int(lt * 24))
        for i in range(160):
            c.set_source_rgba(1, 0.95, 0.8, rnd.uniform(0.03, 0.12)); c.rectangle(rnd.uniform(0, W), rnd.uniform(0, H), 2, 2); c.fill()
        for i in range(2):
            c.set_source_rgba(0.9, 0.85, 0.7, 0.15); c.rectangle(rnd.uniform(0, W), 0, 1.5, H); c.fill()

CAM = {
 'hook': (1.0, 1.12, 960, 640), 'hook2': (1.05, 1.15, 960, 560), 'hook3': (1.0, 1.08, 960, 700), 'title': (1.0, 1.05, 960, 700),
 'flag': (1.0, 1.10, 900, 600), 'leak': (1.02, 1.10, 960, 600), 'back': (1.0, 1.08, 1100, 600), 'quote': (1.0, 1.12, 960, 520),
 'caught': (1.02, 1.12, 960, 600), 'gong': (1.0, 1.15, 980, 620), 'gong2': (1.0, 1.06, 960, 600), 'gong3': (1.05, 1.2, 900, 650),
 'die1': (1.0, 1.10, 960, 600), 'void1': (1.0, 1.2, 960, 560), 'first': (1.0, 1.1, 960, 650), 'ban': (1.0, 1.08, 960, 600),
 'london': (1.0, 1.25, 960, 560), 'cell': (1.0, 1.08, 960, 450), 'note': (1.0, 1.06, 960, 560), 'cantlie': (1.0, 1.08, 960, 600),
 'globe': (1.0, 1.14, 960, 620), 'free': (1.0, 1.15, 960, 560), 'huizhou': (1.0, 1.08, 960, 600), 'li': (1.0, 1.1, 900, 600),
 'li2': (1.0, 1.1, 960, 650), 'yang': (1.0, 1.12, 1150, 420), 'yang0': (1.0, 1.1, 900, 560), 'yang1': (1.0, 1.08, 960, 600),
 'shot': (1.02, 1.08, 960, 600), 'yangdie': (1.0, 1.12, 960, 760), 'void2': (1.0, 1.2, 960, 560), 'tomb': (1.0, 1.1, 960, 700),
 'zheng': (1.0, 1.1, 960, 650), 'zheng2': (1.0, 1.15, 960, 700), 'lin': (1.0, 1.12, 1000, 600), 'lin2': (1.0, 1.12, 960, 640),
 'lin3': (1.0, 1.08, 960, 560), 'charge': (1.0, 1.15, 1100, 600), 'hhg': (1.0, 1.1, 960, 650), 'hhg2': (1.0, 1.08, 960, 600),
 'wuchang': (1.0, 1.12, 960, 560), 'nanjing': (1.0, 1.1, 960, 560), 'count': (1.0, 1.06, 960, 650), 'twist': (1.0, 1.05, 960, 600),
 'twist2': (1.0, 1.06, 960, 650), 'gold': (1.0, 1.15, 960, 640), 'end': (1.0, 1.08, 960, 640),
}

# ================= 钩子 =================
def S_hook(c, lt, d, p):
    bg(c, [(0, (0.02, 0.025, 0.04)), (1, (0.01, 0.01, 0.015))])
    # 窗外雨夜
    c.set_source_rgb(0.05, 0.07, 0.10); c.rectangle(1200, 300, 520, 420); c.fill()
    c.save(); c.rectangle(1200, 300, 520, 420); c.clip(); rain(c, lt, 80, 0.3, seed=3); c.restore()
    window_bars(c, 1200, 300, 520, 420, n=3, col=(0.015, 0.015, 0.02), frame=26)
    table(c, 760, col=(0.05, 0.035, 0.03))
    q = sm(p / 0.7)
    flagcloth(c, 960 - lerp(120, 330, q), 900, lerp(240, 660, q), lerp(300, 420, q), lt * 0.4, lit=lerp(0.4, 1.0, q), amp=6)
    arm(c, 300, 1350, 960 - lerp(120, 330, q) - 10, 900, w0=150, w1=50, hand='open', col=(0.025, 0.025, 0.03))
    arm(c, 1620, 1350, 960 + lerp(120, 330, q) + 10, 900, w0=150, w1=50, hand='open', col=(0.025, 0.025, 0.03))
    dust(c, lt, 40, col=(0.75, 0.85, 1), a=0.35)

def S_hook2(c, lt, d, p):
    bg(c, [(0, (0.05, 0.05, 0.06)), (1, (0.02, 0.02, 0.025))])
    for k in range(30):
        c.set_source_rgba(0.09, 0.08, 0.08, 0.6); c.rectangle(0, k * 38, W, 2); c.fill()
    # 通缉告示
    px, py, pw, ph = 620, 300, 680, 600
    c.set_source_rgb(0.30, 0.26, 0.19); c.rectangle(px, py, pw, ph); c.fill()
    c.set_source_rgba(0.12, 0.09, 0.06, 0.5); c.rectangle(px + 20, py + 20, pw - 40, ph - 40); c.set_line_width(3); c.stroke()
    for i, s in enumerate(("通", "缉")): text(c, s, px + pw / 2 - 90 + i * 180, py + 160, 130, (0.10, 0.07, 0.05), 1, 'c', shadow=False)
    text(c, "孫 文", px + pw / 2, py + 330, 120, (0.45, 0.08, 0.05), 1, 'c', shadow=False)
    text(c, "花紅壹千元", px + pw / 2, py + 470, 64, (0.10, 0.07, 0.05), 1, 'c', shadow=False)
    # 火把光扫过
    sx = lerp(-200, 2200, p)
    glow(c, sx, 650, 600, (1, 0.5, 0.15), 0.25)
    for k in range(3): sil(c, sx - 300 - k * 160, 1250, 2.2, hat='qing', face=1, a=0.95)
    torch(c, sx - 250, 900, lt, 1.4)
    rain(c, lt, 120, 0.22, seed=8)

def S_hook3(c, lt, d, p):
    bg(c, [(0, (0.10, 0.03, 0.02)), (0.62, (0.48, 0.14, 0.05)), (1, (0.10, 0.03, 0.02))])
    smoke(c, lt, 500, 8, 0.4)
    ground(c, 900, (0.02, 0.01, 0.01))
    xs = (420, 700, 960, 1220, 1500)
    for i, x in enumerate(xs):
        t0 = 0.12 + i * 0.13; q = cl((p - t0) / 0.18)
        sc = 1.6 + abs(x - 960) * -0.0004
        if q <= 0: sil(c, x, 910, sc, hat='qcap' if i % 2 else 'short', face=1 if x < 960 else -1, a=0.95)
        else:
            sil(c, x, 910, sc, hat='qcap' if i % 2 else 'short', pose='lie', p=q, face=1 if x < 960 else -1, a=0.95)
            if q < 0.4: redflash(c, (0.4 - q) * 1.2)
    glow(c, 960, 1040, 700, FLAGGLOW, 0.12)
    held_flag(c, lt, 1560, 1040, 300, 230, 0.9)

def S_title(c, lt, d, p):
    bg(c, [(0, (0.01, 0.015, 0.03)), (1, (0.03, 0.04, 0.07))])
    flag_on_pole(c, 740, 1260, 560, 440, lt, 1.0, glowk=1.1)
    dust(c, lt, 50, col=(0.7, 0.8, 1), a=0.35, up=True)
    a = ease(lt / 0.5)
    text(c, "假 如 你 是 孙 中 山", W / 2, 270, 42, GOLD, a, 'c')
    text(c, "替你倒下的人", W / 2, 420, 124, (1, 0.97, 0.92), a, 'c')
    text(c, "为什么死的总是他们，不是你？", W / 2, 545, 70, (0.95, 0.32, 0.26), ease((lt - 0.8) / 0.5), 'c')

# ================= 陆皓东 =================
def S_flag(c, lt, d, p):
    bg(c, [(0, (0.06, 0.045, 0.035)), (1, (0.02, 0.015, 0.012))])
    for k in range(9):  # 百叶窗
        c.set_source_rgba(0.13, 0.09, 0.06, 0.6); c.rectangle(1300, 320 + k * 40, 400, 14); c.fill()
    table(c, 880, col=(0.04, 0.03, 0.02))
    sil(c, 720, 1080, 2.3, hat='qcap', pose='offer', p=sm(p / 0.5), face=1)
    name(c, "陆皓东", 690, 380)
    q = sm((p - 0.2) / 0.5)
    fx = lerp(980, 1080, q); fy = lerp(700, 760, q)
    flagcloth(c, fx - 40, fy, lerp(260, 380, q), lerp(170, 250, q), lt * 0.6, lit=lerp(0.6, 1, q), amp=6)
    reach(c, cl((p - 0.35) / 0.4), fx + 60, fy + 140, 1500, 1300)

def S_leak(c, lt, d, p):
    bg(c, [(0, (0.02, 0.03, 0.05)), (0.7, (0.06, 0.07, 0.09)), (1, (0.03, 0.03, 0.04))])
    lingnan_houses(c, 780, (0.025, 0.028, 0.035))
    ground(c, 840, (0.03, 0.03, 0.04))
    puddles(c, lt, 860)
    for k in range(5):
        x = lerp(1900, 300, (p * 0.6 + k * 0.17) % 1.2)
        sil(c, x, 900, 1.05, hat='qing', face=-1, a=0.95)
        torch(c, x - 30, 760, lt, 0.9, seed=k)
    fog(c, lt, 760, 0.12)
    rain(c, lt, 260, 0.35, seed=2)
    # 前景：你躲在墙角
    poly(c, [(-50, -50), (330, -50), (360, H + 50), (-50, H + 50)], (0.01, 0.01, 0.012))
    arm(c, 120, 1300, 330, 640, w0=130, w1=46, hand='open', col=(0.02, 0.02, 0.025))
    folded_flag(c, 1700, 1040, 0.8, 0.5, lt)

def S_back(c, lt, d, p):
    bg(c, [(0, (0.02, 0.03, 0.05)), (1, (0.04, 0.04, 0.05))])
    lingnan_houses(c, 800, (0.03, 0.03, 0.04), seed=5)
    # 机关门
    c.set_source_rgb(0.18, 0.12, 0.06); c.rectangle(1300, 480, 220, 380); c.fill()
    glow(c, 1410, 700, 260, (1, 0.6, 0.25), 0.15)
    ground(c, 860, (0.03, 0.03, 0.04)); puddles(c, lt, 880)
    for k in range(2): sil(c, lerp(700, 200, p) - k * 120, 900, 1.0, hat='qcap', face=-1, a=0.9)
    x = lerp(600, 1380, sm(p)); s = lerp(1.6, 1.2, p)
    sil(c, x, 900 + 60 * (1 - p), s, hat='qcap', pose='point', face=1)
    name(c, "陆皓东", x, 900 + 60 * (1 - p) - 300 * s - 40)
    rain(c, lt, 260, 0.35, seed=6)
    reach(c, cl(p / 0.5), 900, 820, 600, 1300, close=cl((p - 0.6) * 3))

def S_quote(c, lt, d, p):
    bg(c, [(0, (0.03, 0.04, 0.06)), (1, (0.01, 0.01, 0.02))])
    rain(c, lt, 160, 0.25, seed=9)
    glow(c, 960, 640, 760, (0.40, 0.50, 0.66), 0.45)
    bust(c, 900, 1150, 1.7, hat='queue', col=(0.02, 0.02, 0.025))
    c.set_source_rgba(*FLAGGLOW, 0.35); c.set_line_width(4)
    c.save(); c.translate(900, 1150); c.scale(1.7, 1.7); c.arc(0, -340, 72, -0.6, 0.9); c.restore(); c.stroke()
    name(c, "陆皓东", 900, 420)
    held_flag(c, lt, 1580, 1050, 300, 220, 0.8)

def S_caught(c, lt, d, p):
    bg(c, [(0, (0.16, 0.07, 0.03)), (1, (0.04, 0.02, 0.01))])
    glow(c, 700, 650, 520, (1, 0.5, 0.2), 0.25)
    # 火盆烧名册
    poly(c, [(820, 900), (1100, 900), (1060, 980), (860, 980)], (0.05, 0.03, 0.02))
    fires(c, lt, [880, 960, 1040], 905, 90 * (1 - p * 0.6))
    glow(c, 960, 860, 400, (1, 0.45, 0.1), 0.18)
    embers(c, lt, 70, a=0.7, x0=800, x1=1150, y0=880, h=700)
    sil(c, 700, 1000, 1.9, hat='qcap', face=1)
    name(c, "陆皓东", 700, 330)
    q = sm((p - 0.25) / 0.4)
    for k in range(3): sil(c, lerp(2200, 1350 + k * 170, q), 1000, 1.9, hat='qing', pose='point', face=-1)
    if 0.25 < p < 0.35: redflash(c, 0.6)

def S_gong(c, lt, d, p):
    bg(c, [(0, (0.04, 0.03, 0.02)), (1, (0.01, 0.01, 0.01))])
    table(c, 500, col=(0.06, 0.04, 0.03))
    c.set_source_rgb(0.42, 0.36, 0.26); c.rectangle(560, 560, 760, 440); c.fill()
    paperstrokes(c, 560, 560, 760, 440, cl(p * 1.1), cols=12)
    k = min(cl(p * 1.1), 0.999); j = int(k * 12)
    hx = 560 + 760 - (j + 0.5) * 760 / 12; hy = 600 + (k * 12 - j) * 380
    arm(c, 1700, 1300, hx + 40, hy + 40, w0=140, w1=44, hand='fist', col=(0.02, 0.02, 0.02))
    c.set_source_rgb(0.35, 0.33, 0.30); c.set_line_width(10)  # 镣铐
    c.save(); c.translate(lerp(1700, hx + 40, 0.8), lerp(1300, hy + 40, 0.8)); c.arc(0, 0, 38, 0, 6.28); c.restore(); c.stroke()
    c.set_source_rgb(0.02, 0.02, 0.02); c.set_line_width(8); c.move_to(hx + 40, hy + 40); c.line_to(hx, hy); c.stroke()
    glow(c, 960, 780, 500, (1, 0.7, 0.4), 0.06)

def S_gong2(c, lt, d, p):
    bg(c, [(0, (0.05, 0.05, 0.07)), (0.7, (0.20, 0.14, 0.10)), (1, (0.06, 0.04, 0.03))])
    ground(c, 860, (0.02, 0.015, 0.015))
    rnd = random.Random(3)
    for i in range(34):
        x = 200 + i * 47 + rnd.uniform(-10, 10); t0 = rnd.uniform(0, 0.7); q = sm((p - t0) / 0.25)
        if q > 0: sil(c, x, 870, lerp(0.3, 0.55, q), hat='short' if i % 3 else 'qcap', face=1, a=q)
    glow(c, 360, 760, 500, (0.9, 0.6, 0.4), 0.25)
    bust(c, 330, 1250, 1.8, hat='queue', col=(0.015, 0.015, 0.02))
    name(c, "陆皓东", 330, 520)
    folded_flag(c, 1650, 1020, 0.7, 0.7, lt)

def S_gong3(c, lt, d, p):
    bg(c, [(0, (0.03, 0.025, 0.02)), (1, (0.01, 0.01, 0.01))])
    table(c, 500, col=(0.05, 0.035, 0.025))
    c.set_source_rgb(0.40, 0.34, 0.25); c.rectangle(560, 560, 760, 440); c.fill()
    paperstrokes(c, 560, 560, 760, 440, 1.0, cols=12)
    q = sm(p / 0.5)
    c.set_source_rgb(0.02, 0.02, 0.02); c.set_line_width(10); c.move_to(1400, lerp(700, 960, q)); c.line_to(1520, lerp(640, 960, q)); c.stroke()
    arm(c, 1750, 1300, lerp(1450, 1650, q), lerp(700, 1100, q), w0=140, w1=44, hand='open', col=(0.02, 0.02, 0.02))

def S_die1(c, lt, d, p):
    hit = 1.7 / d
    bg(c, [(0, (0.16, 0.16, 0.18)), (0.6, (0.45, 0.20, 0.12)), (1, (0.10, 0.06, 0.05))])
    glow(c, 960, 720, 800, (0.9, 0.5, 0.35), 0.25)
    lingnan_houses(c, 560, (0.13, 0.09, 0.08), seed=9)
    ground(c, 820, (0.05, 0.035, 0.03))
    rain(c, lt, 140, 0.25, seed=4)
    for i, (x, nm) in enumerate(((620, "朱贵全"), (960, "陆皓东"), (1300, "丘四"))):
        a = 1 if p < hit else 1 - sm((p - hit) / (0.5 - hit * 0.5))
        sil(c, x, 860, 1.25, hat='queue', pose='kneel', face=1 if x < 960 else -1, a=max(a, 0))
        name(c, nm, x, 520, 40 if nm != "陆皓东" else 48, a=max(a, 0.0) * 0.95 + 0.05)
    if p < hit:
        sil(c, 1100, 860, 1.5, hat='qing', pose='sword', p=sm(p / hit), face=-1)
    else:
        redflash(c, cl(1 - (p - hit) / 0.12) * 1.6)
    reach(c, cl(p / (hit + 0.15)), 960, 760, 1150, 1300, close=cl((p - hit - 0.25) * 4))

def S_void1(c, lt, d, p):
    bg(c, [(0, (0, 0, 0)), (1, (0.01, 0.01, 0.015))])
    rain(c, lt, 90, 0.18, seed=10)
    flag_on_pole(c, 900, 900, 380, 300, lt * 0.5, 0.75 + 0.15 * math.sin(lt * 2))

def S_first(c, lt, d, p):
    bg(c, [(0, (0.04, 0.035, 0.03)), (1, (0.01, 0.01, 0.01))])
    table(c, 640, col=(0.05, 0.035, 0.025))
    c.set_source_rgb(0.40, 0.36, 0.30); c.rectangle(640, 680, 620, 380); c.fill()
    paperstrokes(c, 640, 680, 620, 380, cl(p * 1.2), cols=11, seed=4)
    folded_flag(c, 1500, 820, 0.9, 1.0, lt)
    arm(c, 300, 1350, lerp(900, 760, p), 900, w0=140, w1=44, hand='fist', col=(0.02, 0.02, 0.025))

# ================= 1896 =================
def S_ban(c, lt, d, p):
    harbor(c, lt)
    steamship(c, lerp(1500, 1250, p), 780, 0.9, lt, whistle=cl((p - 0.3) / 0.5))
    steamship(c, 380, 740, 0.45, lt + 2)
    fog(c, lt, 760, 0.10)
    # 船舷栏杆前景
    c.set_source_rgb(0.01, 0.01, 0.012); c.rectangle(-100, 930, W + 200, 30); c.fill()
    for k in range(0, W + 100, 120): c.rectangle(k, 930, 16, 200); c.fill()
    arm(c, 300, 1300, 620, 935, w0=140, w1=46, hand='fist', col=(0.02, 0.02, 0.025))
    held_flag(c, lt, 1580, 1080, 280, 210, 0.7, glowk=0.8)

def S_london(c, lt, d, p):
    bg(c, [(0, (0.10, 0.11, 0.12)), (1, (0.04, 0.04, 0.045))])
    terraces(c, 900, lit={(580, 3)})
    c.set_source_rgb(0.02, 0.02, 0.02); c.rectangle(860, 600, 200, 300); c.fill()
    c.set_source_rgb(0.12, 0.09, 0.06); c.rectangle(870, 610, 180, 290); c.fill()
    glow(c, 960, 760, 200, (1, 0.7, 0.4), 0.12)
    text(c, "49", 960, 580, 40, (0.6, 0.55, 0.45), 1, 'c', shadow=False)
    gaslamp(c, 420, 920, 1.2, lt); gaslamp(c, 1560, 920, 1.2, lt)
    ground(c, 900, (0.05, 0.05, 0.055))
    fog(c, lt, 700, 0.28, seed=3)
    sil(c, 520, 1350, 3.0, hat='bowler', robe='suit', face=1)
    sil(c, 1400, 1350, 3.0, hat='bowler', robe='suit', face=-1)
    arm(c, 450, 1300, 760, 900, w0=140, w1=46, hand='open', col=(0.02, 0.02, 0.025))
    arm(c, 1470, 1300, 1160, 900, w0=140, w1=46, hand='open', col=(0.02, 0.02, 0.025))

def S_cell(c, lt, d, p):
    bg(c, [(0, (0.03, 0.03, 0.035)), (1, (0.01, 0.01, 0.012))])
    c.set_source_rgb(0.18, 0.20, 0.24); c.rectangle(700, 300, 520, 380); c.fill()
    fog(c, lt, 450, 0.15, seed=7)
    window_bars(c, 700, 300, 520, 380, n=5, col=(0.01, 0.01, 0.012), frame=40)
    glow(c, 960, 500, 600, (0.6, 0.65, 0.75), 0.10)
    arm(c, 450, 1300, 760, 560, w0=140, w1=46, hand='fist', col=(0.02, 0.02, 0.025))
    arm(c, 1470, 1300, 1150, 580, w0=140, w1=46, hand='fist', col=(0.02, 0.02, 0.025))
    folded_flag(c, 960, 1060, 0.7, 0.45, lt)

def S_note(c, lt, d, p):
    if p < 0.5:
        q = p / 0.5
        bg(c, [(0, (0.10, 0.11, 0.12)), (1, (0.05, 0.05, 0.055))])
        ground(c, 700, (0.06, 0.06, 0.065))
        fog(c, lt, 600, 0.2)
        rnd = random.Random(2)
        for i in range(5):
            st = i * 0.15; qq = cl((q - st) / 0.5)
            if qq > 0:
                x = 960 + rnd.uniform(-300, 300) * qq; y = lerp(300, 820, qq)
                c.set_source_rgb(0.75, 0.72, 0.65); c.save(); c.translate(x, y); c.rotate(qq * 6); c.rectangle(-14, -10, 28, 20); c.restore(); c.fill()
        sil(c, lerp(1500, 1150, q), 900, 1.2, hat='bowler', robe='suit', pose='point', face=-1)
        window_bars(c, 560, 230, 800, 760, n=5, col=(0.01, 0.01, 0.012), frame=200)
    else:
        q = (p - 0.5) / 0.5
        bg(c, [(0, (0.04, 0.04, 0.05)), (1, (0.02, 0.02, 0.02))])
        terraces(c, 1000, col=(0.05, 0.045, 0.045))
        c.set_source_rgb(0.08, 0.06, 0.05); c.rectangle(1100, 600, 220, 400); c.fill()
        text(c, "46", 1210, 580, 40, (0.6, 0.55, 0.45), 1, 'c', shadow=False)
        gaslamp(c, 800, 1000, 1.1, lt)
        sil(c, 1000, 1000, 1.5, hat='vlady', robe='dress', pose='offer', p=q, face=1)
        name(c, "女管家 贺维夫人", 1000, 480, 40)
        c.set_source_rgb(0.8, 0.77, 0.7); c.rectangle(lerp(1150, 1110, q), 975, 40, 24); c.fill()
        fog(c, lt, 800, 0.15)

def S_cantlie(c, lt, d, p):
    bg(c, [(0, (0.09, 0.10, 0.11)), (1, (0.03, 0.03, 0.035))])
    # 外交部柱廊
    c.set_source_rgb(0.05, 0.05, 0.055); c.rectangle(1050, 300, 900, 600); c.fill()
    poly(c, [(1020, 300), (1980, 300), (1500, 180)], (0.05, 0.05, 0.055))
    for k in range(6): c.set_source_rgb(0.09, 0.09, 0.1); c.rectangle(1100 + k * 150, 340, 46, 560); c.fill()
    ground(c, 900, (0.05, 0.05, 0.055))
    gaslamp(c, 700, 920, 1.2, lt)
    fog(c, lt, 700, 0.22)
    x = lerp(300, 950, p)
    sil(c, x, 980, 1.9, hat='top', robe='suit', pose='stand', face=1)
    name(c, "康德黎 James Cantlie", x, 980 - 1.9 * 330, 42)
    sil(c, 1850, 960, 1.1, hat='bowler', robe='suit', face=-1, a=0.8)
    name(c, "侦探", 1820, 560, 40, a=0.8)

def S_globe(c, lt, d, p):
    bg(c, [(0, (0.07, 0.07, 0.08)), (1, (0.02, 0.02, 0.02))])
    for k in range(18): sil(c, 80 + k * 105, 1100, 1.4, hat='bowler' if k % 3 else 'top', robe='suit', face=1 if k % 2 else -1, a=0.85)
    c.save(); c.translate(960, 640); c.rotate(-0.04 + 0.02 * math.sin(lt)); s = lerp(0.85, 1.0, sm(p)); c.scale(s, s)
    c.set_source_rgb(0.62, 0.58, 0.50); c.rectangle(-480, -300, 960, 600); c.fill()
    c.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for (s_, y, sz) in (("THE GLOBE", -200, 92), ("STARTLING STORY!", -80, 58), ("KIDNAPPED IN LONDON!", 0, 52), ("IMPRISONMENT AT THE CHINESE LEGATION!", 70, 30)):
        c.set_font_size(sz); w = c.text_extents(s_)[4]; c.set_source_rgb(0.08, 0.07, 0.06); c.move_to(-w / 2, y); c.show_text(s_)
    c.set_source_rgb(0.08, 0.07, 0.06); c.rectangle(-440, -170, 880, 4); c.fill()
    for k in range(5): c.set_source_rgba(0.15, 0.13, 0.11, 0.6); c.rectangle(-430, 110 + k * 32, 860, 12); c.fill()
    c.restore()

def S_free(c, lt, d, p):
    q = sm(p / 0.4)
    bg(c, [(0, (0.02, 0.02, 0.02)), (1, (0.01, 0.01, 0.01))])
    # 门开，外面是雾与人群
    ow = lerp(0, 700, q)
    c.save(); c.rectangle(960 - ow / 2, 120, ow, 960); c.clip()
    bg(c, [(0, (0.35, 0.36, 0.38)), (1, (0.15, 0.15, 0.16))])
    for k in range(12): sil(c, 640 + k * 60, 1000, 0.9, hat='bowler', robe='suit', face=1 if k % 2 else -1, a=0.7)
    sil(c, 960, 1180, 2.3, hat='top', robe='suit', pose='offer', p=1, face=-1)
    fog(c, lt, 600, 0.2)
    c.restore()
    name(c, "康德黎", 960, 360, 46, a=q)
    reach(c, cl((p - 0.3) / 0.4), 820, 860, 1300, 1300, close=cl((p - 0.7) * 4))
    held_flag(c, lt, 300, 1080, 300, 220, lerp(0.6, 1.0, p))

# ================= 1900 =================
def S_huizhou(c, lt, d, p):
    bg(c, [(0, (0.10, 0.06, 0.05)), (0.6, (0.40, 0.20, 0.10)), (1, (0.10, 0.06, 0.04))])
    mountains(c, lt, cols=[(0.16, 0.10, 0.08), (0.10, 0.06, 0.05), (0.05, 0.03, 0.03)], base=820)
    smoke(c, lt, 600, 6, 0.3, col=(0.2, 0.15, 0.12))
    n = int(lerp(8, 60, sm(p))); rnd = random.Random(1)
    for i in range(60):
        if i >= n: break
        x = rnd.uniform(100, 1820); y = rnd.uniform(860, 960); sil(c, x, y, rnd.uniform(0.35, 0.55), hat='qcap', face=1)
    sil(c, 960, 1100, 1.6, hat='qcap', pose='raise', p=sm(p / 0.4), face=1)
    name(c, "郑士良", 960, 500)

def S_li(c, lt, d, p):
    bg(c, [(0, (0.12, 0.09, 0.05)), (1, (0.04, 0.03, 0.02))])
    glow(c, 1000, 700, 600, (1, 0.7, 0.4), 0.25)
    for k in range(4):
        c.set_source_rgb(0.08, 0.055, 0.035); c.rectangle(200, 400 + k * 150, 500, 20); c.fill()
        for j in range(5): poly(c, [(230 + j * 90, 400 + k * 150), (290 + j * 90, 400 + k * 150), (280 + j * 90, 370 + k * 150), (240 + j * 90, 370 + k * 150)], (0.45, 0.42, 0.38))
    sil(c, 1000, 1080, 2.3, hat='qcap', pose='offer', p=sm(p / 0.5), face=1, robe=(0.06, 0.04, 0.03))
    name(c, "李纪堂", 1000, 370)
    poly(c, [(1230, 760), (1420, 760), (1410, 860), (1240, 860)], (0.12, 0.08, 0.05))
    reach(c, cl((p - 0.3) / 0.4), 1330, 870, 1600, 1300)

def S_li2(c, lt, d, p):
    bg(c, [(0, (0.10, 0.07, 0.05)), (1, (0.02, 0.015, 0.01))])
    glow(c, 1200, 650, 700, (1, 0.65, 0.35), 0.22)
    ground(c, 900, (0.03, 0.02, 0.015))
    poly(c, [(760, 900), (1160, 900), (1140, 720), (780, 720)], (0.10, 0.07, 0.04))
    rnd = random.Random(3)
    for i in range(60):
        q = (lt * 0.8 + rnd.uniform(0, 1)) % 1
        if rnd.uniform(0, 1) < 1 - p:
            x = 960 + rnd.uniform(-160, 160) + q * rnd.uniform(-600, 600); y = 720 - math.sin(q * 3.14) * 200 + q * 300
            c.set_source_rgba(0.6, 0.57, 0.5, 0.8 * (1 - q)); c.arc(x, y, 7, 0, 6.28); c.fill()
    sil(c, 1450, 900, 1.5, hat='qcap', pose='sit', face=-1, a=lerp(0.3, 1, p))
    name(c, "李纪堂", 1450, 560, 42, a=lerp(0.3, 1, p))

# ================= 杨衢云 =================
def S_yang(c, lt, d, p):
    bg(c, [(0, (0.02, 0.03, 0.05)), (1, (0.04, 0.04, 0.05))])
    tonglau(c, 900, 900, 560, 700, lt, lit={(1, 1)})
    tonglau(c, 220, 980, 520, 640, lt, col=(0.025, 0.025, 0.03))
    tonglau(c, 1520, 940, 520, 760, lt, col=(0.025, 0.025, 0.03))
    for k in range(8): c.set_source_rgba(0.08, 0.08, 0.09, 1); c.rectangle(-100, 940 + k * 22, W + 200, 4); c.fill()  # 石板阶
    gaslamp(c, 760, 980, 1.0, lt)
    fog(c, lt, 900, 0.12)
    sil(c, 1180, 1000 - 340 + 6, 0.35, hat='queue', face=-1, a=0.9)
    for k in range(2): sil(c, 500 + k * 120, 1100, 1.4, hat='qcap', face=1, a=0.9)
    name(c, "杨衢云", 1180, 520, 44)

def S_yang0(c, lt, d, p):
    bg(c, [(0, (0.06, 0.045, 0.03)), (1, (0.02, 0.015, 0.012))])
    c.set_source_rgb(0.12, 0.09, 0.06); c.rectangle(1250, 320, 380, 460); c.fill()
    window_bars(c, 1250, 320, 380, 460, n=2, col=(0.02, 0.015, 0.012), frame=22)
    glow(c, 900, 620, 700, (1, 0.62, 0.3), 0.30)
    bust(c, 860, 1150, 1.6, hat='queue', col=(0.015, 0.015, 0.02))
    name(c, "杨衢云", 860, 470)
    sil(c, 1450, 1080, 1.2, hat='qcap', face=-1, pose='point', a=0.7)
    folded_flag(c, 300, 1040, 0.6, 0.6, lt)

def S_yang1(c, lt, d, p):
    bg(c, [(0, (0.07, 0.05, 0.03)), (1, (0.02, 0.015, 0.01))])
    c.set_source_rgb(0.14, 0.10, 0.06); c.rectangle(300, 300, 1300, 420); c.fill()  # 黑板
    c.set_source_rgba(0.6, 0.6, 0.55, 0.5); c.select_font_face("serif", 0, 1); c.set_font_size(54)
    c.move_to(400, 470); c.show_text("A  B  C  D")
    table(c, 860, col=(0.05, 0.035, 0.025))
    sil(c, 700, 860, 1.5, hat='queue', pose='point', face=1)
    name(c, "杨衢云", 700, 290 + 60, 44)
    for k in range(3): sil(c, 1100 + k * 170, 1000, 0.8 + k * 0.05, hat='short', face=-1, a=0.9)
    gaslamp(c, 1750, 900, 0.8, lt)

def S_shot(c, lt, d, p):
    hit = 0.62
    bg(c, [(0, (0.16, 0.11, 0.07)), (1, (0.04, 0.03, 0.02))])
    glow(c, 760, 640, 650, (1, 0.65, 0.35), 0.30)
    c.set_source_rgb(0.01, 0.01, 0.01); c.rectangle(1450, 300, 300, 640); c.fill()
    table(c, 880, col=(0.05, 0.035, 0.025))
    sil(c, 1560, 960, 1.7, hat='queue', pose='point', face=-1)
    if p < hit:
        sil(c, 700, 960, 1.5, hat='queue', pose='raise', p=sm(p / 0.4), face=1)
        c.set_source_rgb(0.2, 0.12, 0.08); c.rectangle(lerp(760, 790, p), lerp(800, 560, sm(p / 0.4)), 70, 90); c.fill()
        sil(c, lerp(820, 640, sm(p / 0.4)), lerp(960, 1000, p), 0.6, hat='short', face=1, pose='kneel')
    else:
        sil(c, 700, 960, 1.5, hat='queue', pose='lie', p=sm((p - hit) / 0.3), face=1)
    name(c, "杨衢云", 700, 400, 44)
    if p > hit:
        q = (p - hit) / 0.05
        if q < 1: glow(c, 1400, 640, 500, (1, 0.85, 0.5), 0.9 * (1 - q)); c.set_source_rgba(1, 0.95, 0.85, 0.5 * (1 - q)); c.paint()
        redflash(c, cl(1 - (p - hit) / 0.15) * 1.3)

def S_yangdie(c, lt, d, p):
    bg(c, [(0, (0.03, 0.02, 0.02)), (1, (0.01, 0.005, 0.005))])
    ground(c, 700, (0.04, 0.025, 0.02))
    c.save(); c.translate(860, 900); c.rotate(-0.2)
    c.set_source_rgb(0.25, 0.15, 0.09); c.rectangle(-150, -100, 300, 200); c.fill()
    c.set_source_rgb(0.4, 0.33, 0.24); c.rectangle(-140, -92, 280, 6); c.fill()
    c.set_source_rgb(0, 0, 0); c.arc(30, -10, 16, 0, 6.28); c.fill()
    c.restore()
    glow(c, 860, 860, 600, (0.6, 0.25, 0.15), 0.25)
    sil(c, 600, 960, 1.3, hat='queue', pose='lie', p=1, face=1)
    redflash(c, cl(1 - p / 0.15))
    reach(c, cl(p / 0.5), 900, 820, 1250, 1300, close=cl((p - 0.7) * 4))
    c.set_source_rgba(0, 0, 0, sm((p - 0.6) / 0.4) * 0.6); c.paint()

def S_void2(c, lt, d, p):
    bg(c, [(0, (0, 0, 0)), (1, (0.01, 0.01, 0.015))])
    flag_on_pole(c, 900, 900, 380, 300, lt * 0.5, 0.75 + 0.15 * math.sin(lt * 2))

def S_tomb(c, lt, d, p):
    bg(c, [(0, (0.14, 0.15, 0.16)), (1, (0.06, 0.06, 0.065))])
    for k in range(9):
        x = 100 + k * 220; s = 0.7
        poly(c, [(x - 40, 820), (x + 40, 820), (x + 34, 700), (x - 34, 700)], (0.06, 0.06, 0.065))
    tree(c, 1650, 860, 0.6, lt, leaves=(0.05, 0.06, 0.05))
    ground(c, 820, (0.05, 0.05, 0.055))
    poly(c, [(720, 1080), (1200, 1080), (1170, 560), (750, 560)], (0.22, 0.22, 0.23))
    c.save(); c.translate(960, 560); c.scale(1, 0.25); c.arc(0, 0, 210, math.pi, 2 * math.pi); c.restore(); c.set_source_rgb(0.22, 0.22, 0.23); c.fill()
    text(c, "6348", 960, 800, 110, (0.10, 0.10, 0.11), 1, 'c', shadow=False)
    fog(c, lt, 900, 0.18)
    arm(c, 1700, 1350, 1230, 760, w0=140, w1=46, hand='open', col=(0.02, 0.02, 0.025), a=sm(p / 0.5))

# ================= 郑士良 =================
def S_zheng(c, lt, d, p):
    bg(c, [(0, (0.02, 0.025, 0.04)), (1, (0.04, 0.04, 0.05))])
    tonglau(c, -100, 820, 800, 700, lt, lit={(1, 0)}, col=(0.025, 0.025, 0.03))
    tonglau(c, 1200, 820, 820, 680, lt, lit={(2, 2)}, col=(0.025, 0.025, 0.03))
    ground(c, 820, (0.03, 0.03, 0.035)); puddles(c, lt, 840, col=(1, 0.65, 0.3))
    gaslamp(c, 760, 840, 0.9, lt); gaslamp(c, 1300, 840, 0.9, lt)
    x = lerp(1500, 900, p)
    glow(c, x - 100, 760, 600, (1, 0.6, 0.3), 0.28)
    c.save(); c.translate(x, 940); c.set_source_rgb(*INK)
    c.arc(0, -40, 60, 0, 6.28); c.set_line_width(10); c.stroke()
    poly(c, [(-80, -100), (60, -100), (60, -220), (-60, -230)], INK)
    c.set_line_width(8); c.move_to(-80, -110); c.line_to(-330, -150); c.stroke()
    c.restore()
    sil(c, x + 10, 840 - 40, 0.85, hat='queue', pose='sit', face=-1)
    sil(c, x - 380, 950, 1.0, hat='qcap', pose='point', face=-1)
    name(c, "郑士良", x + 10, 520)
    rain(c, lt, 60, 0.15)

def S_zheng2(c, lt, d, p):
    bg(c, [(0, (0.05, 0.03, 0.02)), (1, (0.01, 0.01, 0.01))])
    table(c, 620, col=(0.06, 0.04, 0.03))
    cup(c, 760, 800, 1.1); 
    c.save(); c.translate(1120, 820); c.rotate(1.4); cup(c, 0, 0, 1.0); c.restore()
    c.set_source_rgba(0.35, 0.05, 0.04, 0.8); c.save(); c.translate(1250, 860); c.scale(1, 0.25); c.arc(0, 0, lerp(40, 200, sm(p)), 0, 6.28); c.restore(); c.fill()
    arm(c, 1500, 500, 1450, 760, w0=120, w1=42, hand='open', col=(0.02, 0.02, 0.02))

# ================= 林觉民 / 黄花岗 =================
def S_lin(c, lt, d, p):
    bg(c, [(0, (0.02, 0.03, 0.05)), (1, (0.01, 0.01, 0.02))])
    c.set_source_rgb(0.05, 0.08, 0.12); c.rectangle(1150, 280, 560, 460); c.fill()
    moon(c, 1500, 400, 45, 0.9)
    for k in range(10): c.set_source_rgba(0.6, 0.65, 0.75, 0.15); c.rectangle(1180 + (k * 53) % 500, 640 + k * 8, 80, 2); c.fill()
    window_bars(c, 1150, 280, 560, 460, n=2, col=(0.01, 0.01, 0.015), frame=26)
    table(c, 820, col=(0.04, 0.035, 0.035))
    glow(c, 1050, 650, 650, (0.55, 0.65, 0.85), 0.35)
    sil(c, 860, 1000, 1.6, hat='short', robe='suit', pose='sit', face=1)
    c.set_source_rgb(0.75, 0.75, 0.72); poly(c, [(980, 820), (1180, 820), (1200, 860), (960, 860)], (0.75, 0.75, 0.72))
    name(c, "林觉民", 860, 680 - 60, 44)
    glow(c, 1450, 500, 500, (0.6, 0.7, 0.9), 0.08)

def S_lin2(c, lt, d, p):
    bg(c, [(0, (0.03, 0.03, 0.04)), (1, (0.01, 0.01, 0.015))])
    c.save(); c.translate(960, 680); c.rotate(-0.05)
    c.set_source_rgb(0.62, 0.61, 0.58); c.rectangle(-460, -330, 920, 640); c.fill()
    cols = ["意映卿卿如晤吾今以", "此书与汝永别矣吾作", "此书时尚是世中一人", "汝看此书时吾已成为", "阴间一鬼吾作此书泪", "珠和笔墨齐下不能竟"]
    for j, s in enumerate(cols):
        for i, ch in enumerate(s):
            text(c, ch, 380 - j * 120, -260 + i * 64, 50, (0.12, 0.10, 0.09), 0.85, 'c', shadow=False)
    c.restore()
    # 泪痕
    q = (lt * 0.5) % 1
    c.set_source_rgba(0.45, 0.45, 0.44, 0.5); c.arc(700, lerp(300, 700, q), 10, 0, 6.28); c.fill()
    arm(c, 1700, 1350, 1300, 950, w0=130, w1=42, hand='fist', col=(0.02, 0.02, 0.025))

def S_lin3(c, lt, d, p):
    bg(c, [(0, (0.03, 0.03, 0.05)), (1, (0.01, 0.01, 0.02))])
    c.set_source_rgb(0.20, 0.22, 0.30); c.save(); c.translate(1150, 560); c.arc(0, 0, 300, 0, 6.28); c.restore(); c.fill()
    moon(c, 1230, 430, 50, 0.85)
    c.set_source_rgb(0.015, 0.015, 0.02); c.set_line_width(10); c.move_to(860, 300); c.curve_to(1000, 400, 1100, 380, 1300, 520); c.stroke()
    for k in range(9): c.set_source_rgba(0.8, 0.78, 0.8, 0.7); c.arc(900 + k * 45, 340 + (k * 23) % 80, 9, 0, 6.28); c.fill()
    c.set_source_rgb(0.01, 0.01, 0.015); c.set_line_width(60); c.arc(1150, 560, 330, 0, 6.28); c.stroke()
    sil(c, 1080, 1120, 1.7, hat='vlady', robe='dress', face=-1)
    name(c, "妻子 陈意映", 640, 600, 42)

def S_charge(c, lt, d, p):
    bg(c, [(0, (0.20, 0.06, 0.02)), (0.6, (0.65, 0.25, 0.06)), (1, (0.25, 0.08, 0.03))])
    lingnan_houses(c, 700, (0.06, 0.025, 0.02), seed=3)
    fires(c, lt, [300, 700, 1500, 1800], 700, 160)
    smoke(c, lt, 500, 10, 0.45, col=(0.10, 0.05, 0.04))
    ground(c, 840, (0.05, 0.02, 0.015))
    rnd = random.Random(6)
    for i in range(16):
        ph = rnd.uniform(0, 1); x = ((lt * 260 + ph * 2400) % 2600) - 300; s = rnd.uniform(0.9, 1.6)
        y = 850 + (s - 0.9) * 280
        sil(c, x, y, s, hat='short', pose='raise' if i % 3 == 0 else 'point', p=1, face=1)
        c.set_source_rgba(0.95, 0.95, 0.92, 0.9); c.rectangle(x + 8 * s, y - 175 * s, 30 * s, 12 * s); c.fill()   # 白巾
    embers(c, lt, 120, a=0.9)
    held_flag(c, lt, 1500, 1060, 380, 300, 1.0)

def S_hhg(c, lt, d, p):
    bg(c, [(0, (0.22, 0.07, 0.03)), (0.6, (0.50, 0.18, 0.05)), (1, (0.08, 0.03, 0.02))])
    fires(c, lt, [300, 1600], 860, 140)
    smoke(c, lt, 600, 10, 0.5, col=(0.08, 0.05, 0.05))
    ground(c, 860, (0.03, 0.015, 0.01))
    sil(c, 960, 880, 1.6, hat='short', robe='suit', pose='kneel' if p < 0.35 else 'lie', p=sm((p - 0.35) / 0.4), face=1)
    c.set_source_rgba(0.95, 0.95, 0.92, 0.9 * (1 - sm((p - 0.4) / 0.4))); c.rectangle(980, 650, 40, 14); c.fill()
    name(c, "林觉民", 960, 480)
    if 0.3 < p < 0.45: redflash(c, 1.2 * (0.45 - p) / 0.15)
    embers(c, lt, 70, a=0.7)
    reach(c, cl(p / 0.6), 980, 780, 1250, 1300, close=cl((p - 0.8) * 5))

def S_hhg2(c, lt, d, p):
    bg(c, [(0, (0.25, 0.20, 0.18)), (0.6, (0.40, 0.28, 0.18)), (1, (0.10, 0.07, 0.05))])
    poly(c, [(-100, 860), (500, 700), (1100, 640), (1700, 720), (2100, 860), (2100, 1200), (-100, 1200)], (0.06, 0.045, 0.035))
    rnd = random.Random(72)
    n = int(72 * sm(p / 0.7))
    for i in range(72):
        if i >= n: break
        x = 140 + (i % 18) * 92 + rnd.uniform(-8, 8); y = 760 + (i // 18) * 70 + abs(x - 1100) * 0.08
        sc = 0.6 + (i // 18) * 0.15
        poly(c, [(x - 14 * sc, y), (x + 14 * sc, y), (x + 11 * sc, y - 46 * sc), (x - 11 * sc, y - 46 * sc)], (0.03, 0.02, 0.02))
    smoke(c, lt, 500, 6, 0.25, col=(0.3, 0.25, 0.22))
    folded_flag(c, 1620, 1020, 0.7, 0.8, lt)

def S_wuchang(c, lt, d, p):
    bg(c, [(0, (0.18, 0.06, 0.02)), (0.6, (0.75, 0.35, 0.08)), (1, (0.30, 0.10, 0.03))])
    citywall(c, 760, col=(0.06, 0.025, 0.015), h=200)
    fires(c, lt, [400, 900, 1400], 560, 130)
    smoke(c, lt, 400, 8, 0.4, col=(0.12, 0.06, 0.04))
    rnd = random.Random(8)
    for i in range(24):
        x = rnd.uniform(-50, 1970); s = rnd.uniform(1.0, 1.8); y = 880 + (s - 1) * 300
        sil(c, x, y, s, hat='short', pose='raise', p=1, face=1 if x < 960 else -1)
    embers(c, lt, 120, a=0.9)

def S_nanjing(c, lt, d, p):
    bg(c, [(0, (0.55, 0.40, 0.20)), (0.6, (0.95, 0.70, 0.35)), (1, (0.40, 0.25, 0.12))])
    glow(c, 960, 520, 900, (1, 0.9, 0.6), 0.35)
    roofhall(c, 960, 700, 1100, 420, col=(0.10, 0.06, 0.03))
    rnd = random.Random(12)
    for i in range(40):
        x = rnd.uniform(-40, 1960); s = rnd.uniform(0.8, 1.6); y = 900 + (s - 0.8) * 260
        sil(c, x, y, s, hat='short' if i % 2 else 'qcap', pose='raise', p=1, face=1 if x < 960 else -1)
    q = sm(p / 0.6)
    arm(c, 1200, 1350, 1100, lerp(1150, 860, q), w0=150, w1=50, hand='fist', col=(0.03, 0.025, 0.02))
    flag_on_pole(c, 1104, lerp(1180, 890, q), 430, 400, lt, 1.0, glowk=1.2)
    dust(c, lt, 50, col=(1, 0.95, 0.8), a=0.5, up=True)

# ================= 收尾 =================
def S_count(c, lt, d, p):
    bg(c, [(0, (0.02, 0.02, 0.03)), (0.75, (0.16, 0.12, 0.10)), (1, (0.04, 0.04, 0.05))])
    glow(c, 960, 860, 900, (0.8, 0.55, 0.35), 0.22)
    rnd = random.Random(77)
    for i in range(76):
        row = i // 20; x = 120 + (i % 20) * 88 + (row % 2) * 44; s = 0.45 + row * 0.18; y = 780 + row * 85
        a = cl((p * 1.6 - i / 76)) * 0.95
        sil(c, x, y, s, hat='short' if i % 2 else 'qcap', face=1 if x < 960 else -1, a=a)
    glow(c, 960, 1080, 700, FLAGGLOW, 0.12)

def S_twist(c, lt, d, p):
    bg(c, [(0, (0.10, 0.07, 0.04)), (1, (0.04, 0.03, 0.02))])
    tonglau(c, 0, 900, 600, 700, lt, lit={(1, 1)}, col=(0.05, 0.04, 0.03))
    tonglau(c, 1300, 900, 620, 700, lt, lit={(2, 0)}, col=(0.05, 0.04, 0.03))
    ground(c, 900, (0.05, 0.04, 0.03))
    a = 1 - sm((p - 0.4) / 0.5)
    for k, x in enumerate((650, 820, 990, 1160, 1330)):
        sil(c, x, 980, 1.3, hat=('short', 'qcap', 'bowler', 'queue', 'short')[k], face=1 if k % 2 else -1, a=a * 0.95)
    c.set_source_rgb(0, 0, 0); c.rectangle(0, 0, W, 60); c.rectangle(0, H - 60, W, 60); c.fill()
    for k in range(0, W, 80): c.set_source_rgb(0.2, 0.18, 0.15); rr(c, k + 20, 18, 40, 24, 4); c.fill(); rr(c, k + 20, H - 42, 40, 24, 4); c.fill()

def S_twist2(c, lt, d, p):
    bg(c, [(0, (0.04, 0.04, 0.06)), (1, (0.08, 0.06, 0.05))])
    rnd = random.Random(5)
    for i in range(60):
        x = rnd.uniform(0, W); s = rnd.uniform(0.35, 0.6); a = cl(p * 2 - i / 60) * 0.7
        sil(c, x, 800, s, hat='short' if i % 2 else 'qcap', face=1, a=a)
    ppl = [("陆皓东", 'queue'), ("杨衢云", 'queue'), ("郑士良", 'qcap'), ("康德黎", 'top'), ("李纪堂", 'qcap'), ("林觉民", 'short')]
    for k, (nm, h) in enumerate(ppl):
        x = 240 + k * 288; a = cl((p - k * 0.08) / 0.2)
        sil(c, x, 1000, 1.25, hat=h, robe='suit' if h in ('top', 'short') else None, face=1 if x < 960 else -1, a=a)
        name(c, nm, x, 540, 40, a=a)

def S_gold(c, lt, d, p):
    bg(c, [(0, (0.0, 0.0, 0.0)), (1, (0.02, 0.02, 0.03))])
    for k in range(77):
        x = 80 + (k % 39) * 46 + (k // 39) * 23; y = 980 + (k // 39) * 40
        sil(c, x, y, 0.32, hat='short' if k % 2 else 'qcap', face=1, a=0.5)
    flag_on_pole(c, 820, 1100, 420, 360, lt * 0.6, 1.0, glowk=1.2)

def S_end(c, lt, d, p):
    bg(c, [(0, (0.06, 0.06, 0.10)), (0.6, (0.30, 0.20, 0.15)), (1, (0.06, 0.04, 0.03))])
    poly(c, [(-100, 900), (700, 760), (1200, 740), (2100, 880), (2100, 1200), (-100, 1200)], (0.03, 0.025, 0.02))
    for k in range(30):
        x = 200 + k * 55; sil(c, x, 780 + abs(x - 960) * 0.1, 0.45, hat='short' if k % 2 else 'qcap', face=1, a=0.85)
    flag_on_pole(c, 900, 900, 330, 260, lt, 1.0)

# ================= 阈值母题（新）=================
WARM = (1.0, 0.78, 0.45)
def row_bg(c, lt, tone=(0.03, 0.035, 0.05)):
    bg(c, [(0, tone), (0.7, tuple(v * 1.8 for v in tone)), (1, (0.01, 0.01, 0.012))])
    ground(c, 930, (0.015, 0.015, 0.02))
    dust(c, lt, 30, col=(0.8, 0.8, 0.9), a=0.2)

def row(c, lt, nums, lit, xs=None, y=930, s=1.0, fallen=None, nsize=62, red=0.0, hats=None, labels=None, numa=1.0):
    n = len(nums); fallen = fallen or {}
    xs = xs or [230 + i * (1460 / (n - 1)) for i in range(n)]
    for i in range(n):
        x = xs[i]; l = lit[i]
        if l > 0: glow(c, x, y - 150 * s, 260 * s, mix(WARM, RED, red), 0.45 * l)
    for i in range(n):
        x = xs[i]; l = lit[i]; h = (hats[i] if hats else ('qcap' if i % 2 else 'short'))
        if i in fallen:
            sil(c, x, y, s, hat=h, pose='lie', p=fallen[i], face=1)
        else:
            sil(c, x, y, s, hat=h, pose='raise' if l > 0.05 else 'stand', p=sm(l), face=1 if x < 960 else -1)
        v = nums[i]
        if v is not None and i not in fallen:
            col = mix((0.55, 0.55, 0.6), mix(GOLD, RED, red), l)
            text(c, str(v), x, y - 330 * s - 18, nsize * (1 + 0.15 * l), col, numa, 'c')
        if labels: text(c, labels[i], x, y + 70, 44, mix((0.6, 0.58, 0.55), GOLD, l), numa, 'c')

def S_t1(c, lt, d, p):
    bg(c, [(0, (0.03, 0.035, 0.05)), (0.7, (0.10, 0.08, 0.07)), (1, (0.02, 0.02, 0.025))])
    rnd = random.Random(31)
    for r in range(3):
        for i in range(22):
            x = 60 + i * 86 + (r % 2) * 43 + rnd.uniform(-10, 10); s = 0.45 + r * 0.22; y = 760 + r * 90
            if r == 2 and abs(x - 960) < 120: continue
            sil(c, x, y, s, hat='qcap' if (i + r) % 2 else 'short', face=1 if x < 960 else -1, a=0.92)
    q = sm((p - 0.35) / 0.4)
    glow(c, 960, 800, 420, WARM, 0.5 * q)
    sil(c, 960, lerp(1000, 1060, q), 1.25, hat='short', pose='raise', p=q, face=1)

def S_t2(c, lt, d, p):
    row_bg(c, lt)
    a = sm((p - 0.2) / 0.3)
    row(c, lt, list(range(10)), [0] * 10, numa=a)

def S_t3(c, lt, d, p):
    row_bg(c, lt)
    lit = [cl((p * 1.25 - 0.08 - i * 0.085) / 0.07) for i in range(10)]
    row(c, lt, list(range(10)), lit)

def S_t4(c, lt, d, p):
    row_bg(c, lt, (0.04, 0.03, 0.035))
    nums = [0, 2, 2, 3, 4, 5, 6, 7, 8, 9]
    q = sm((p - 0.05) / 0.25)
    lit = [cl(p / 0.15)] + [0] * 9
    if p > 0.25: lit[1] = 0.15 * max(0, math.sin((p - 0.25) * 30)) * (1 - cl((p - 0.6) / 0.2))
    row(c, lt, nums, lit)
    if q > 0: text(c, "1 → 2", 392, 500, 44, (0.95, 0.35, 0.28), q, 'c')

def S_t5(c, lt, d, p):
    row_bg(c, lt)
    pulse = 0.75 + 0.25 * math.sin(lt * 3)
    row(c, lt, list(range(10)), [pulse] + [0] * 9)

def S_r1(c, lt, d, p):
    row_bg(c, lt, (0.05, 0.03, 0.03))
    k = sm((p - 0.3) / 0.25)
    nums = [None] + [i - (1 if k > 0.5 else 0) for i in range(1, 10)]
    lit = [0] + [cl((p - 0.6) / 0.15)] + [0] * 8
    row(c, lt, nums, lit, fallen={0: 1.0})
    if 0 < k < 1 or p < 0.75:
        a = math.sin(math.pi * cl((p - 0.3) / 0.45))
        for i in range(1, 10): text(c, "−1", 230 + i * 162.2 + 44, 500 - 40 * k, 34, GOLD, a * 0.9, 'c')

def S_hz2(c, lt, d, p):
    row_bg(c, lt, (0.06, 0.035, 0.025))
    stop = 0.55; dim = cl((p - stop) / 0.2)
    lit = [cl((min(p, stop) * 1.6 - i * 0.12) / 0.08) * (1 - dim * 0.85) for i in range(10)]
    row(c, lt, list(range(10)), lit, red=dim)
    if p > stop: redflash(c, cl(1 - (p - stop) / 0.12) * 0.8)

def S_r2(c, lt, d, p):
    row_bg(c, lt, (0.03, 0.03, 0.05))
    k = int(lerp(1, 7, sm(p / 0.8)))
    nums = [max(0, i - k) for i in range(10)]
    lit = [0.35 if v == 0 else 0 for v in nums]
    row(c, lt, nums, lit)

PROV = list("鄂湘陕赣晋滇黔苏浙桂皖粤闽川")
def S_prov(c, lt, d, p):
    row_bg(c, lt, (0.08, 0.04, 0.02))
    xs = [140 + i * (1640 / 13) for i in range(14)]
    lit = [cl((p * 1.3 - 0.05 - i * 0.06) / 0.06) for i in range(14)]
    row(c, lt, [None] * 14, lit, xs=xs, y=800, s=0.78, labels=PROV)
    embers(c, lt, 60, a=0.6)

def S_zero(c, lt, d, p):
    row_bg(c, lt, (0.06, 0.06, 0.08))
    xs = [230 + i * 162.2 for i in range(10)]
    # 0号位置空着，只留一圈光
    pulse = 0.7 + 0.3 * math.sin(lt * 2.5)
    glow(c, xs[0], 780, 260, WARM, 0.5 * pulse)
    c.set_source_rgba(*WARM, 0.5 * pulse); c.set_line_width(3)
    c.save(); c.translate(xs[0], 932); c.scale(1, 0.22); c.arc(0, 0, 90, 0, 6.2832); c.restore(); c.stroke()
    text(c, "0", xs[0], 582, 72, GOLD, pulse, 'c')
    for i in range(1, 10):
        sil(c, xs[i], 930, 1.0, hat='qcap' if i % 2 else 'short', face=-1)
        text(c, str(i), xs[i], 582, 62, (0.55, 0.55, 0.6), 1, 'c')

CAM.update({'t1': (1.0, 1.10, 960, 760), 't2': (1.0, 1.05, 960, 700), 't3': (1.0, 1.06, 960, 700), 't4': (1.0, 1.06, 700, 700),
            't5': (1.0, 1.06, 700, 700), 'r1': (1.0, 1.06, 960, 700), 'hz2': (1.0, 1.06, 960, 700), 'r2': (1.0, 1.05, 960, 700),
            'prov': (1.0, 1.06, 960, 700), 'zero': (1.0, 1.05, 960, 640)})

def S_o2(c, lt, d, p):
    bg(c, [(0, (0.03, 0.03, 0.045)), (0.7, (0.12, 0.08, 0.06)), (1, (0.02, 0.02, 0.025))])
    ground(c, 930, (0.015, 0.015, 0.02))
    for k, (nm, h, x) in enumerate((("陆皓东", 'queue', 500), ("杨衢云", 'queue', 960), ("林觉民", 'short', 1420))):
        a = cl((p - k * 0.18) / 0.15)
        glow(c, x, 780, 260, WARM, 0.35 * a)
        sil(c, x, 930, 1.25, hat=h, robe='suit' if h == 'short' else None, face=1 if x < 960 else -1, a=a)
        name(c, nm, x, 500, 46, a=a)

def S_o3(c, lt, d, p):
    S_wuchang(c, lt, d, p)
    c.set_source_rgba(0, 0, 0, 0.45 * (1 - sm(p))); c.paint()

CAM.update({'o2': (1.0, 1.06, 960, 680), 'o3': (1.0, 1.08, 960, 560)})

# 第一视角（POV）工具：手臂、凤羽、眼睑、道具
from kit import *
import math, random
FEATHER = (1.0, 0.62, 0.22)
SKIN_RIM = (0.85, 0.55, 0.30)

def bg(c, stops, y0=-200, y1=H + 200):
    g = cairo.LinearGradient(0, y0, 0, y1)
    for p, col in stops: g.add_color_stop_rgb(p, *col)
    c.set_source(g); c.rectangle(-300, y0, W + 600, y1 - y0); c.fill()

def ground(c, y, col=INK):
    c.set_source_rgb(*col); c.rectangle(-300, y, W + 600, H - y + 400); c.fill()

def arm(c, x0, y0, x1, y1, w0=170, w1=58, a=1, hand='open', rim=0.35, curl=0.0, col=INK):
    """从画面下沿伸入的“你”的手臂：宽袖 + 手。(x0,y0) 袖口根部（画外），(x1,y1) 手腕"""
    dx, dy = x1 - x0, y1 - y0; Ln = math.hypot(dx, dy) or 1
    ux, uy = dx / Ln, dy / Ln; nx, ny = -uy, ux
    # 袖子（宽袖口在手腕处略收）
    cuff = w1 * 1.6
    pts = [(x0 + nx * w0, y0 + ny * w0), (x1 - ux * 40 + nx * cuff, y1 - uy * 40 + ny * cuff),
           (x1 - ux * 40 - nx * cuff, y1 - uy * 40 - ny * cuff), (x0 - nx * w0, y0 - ny * w0)]
    poly(c, pts, col, a)
    # 袖口边缘高光
    c.set_source_rgba(*SKIN_RIM, rim * a); c.set_line_width(3)
    c.move_to(*pts[0]); c.line_to(*pts[1]); c.line_to(*pts[2]); c.stroke()
    if hand == 'none': return
    ang = math.atan2(dy, dx)
    c.save(); c.translate(x1, y1); c.rotate(ang); c.set_source_rgba(*col, a)
    c.save(); c.scale(1.25, 1); c.arc(30, 0, w1 * 0.75, 0, 6.28); c.restore(); c.fill()
    c.set_line_cap(1); c.set_line_width(w1 * 0.32)
    if hand == 'open':
        for k in range(4):
            an = (k - 1.5) * 0.22
            c.move_to(55, (k - 1.5) * w1 * 0.3); c.line_to(55 + math.cos(an) * w1 * 1.3, (k - 1.5) * w1 * 0.3 + math.sin(an) * w1 * 1.3)
        c.stroke()
        c.move_to(30, -w1 * 0.6); c.line_to(60, -w1 * 1.3); c.stroke()
    elif hand == 'point':
        c.move_to(55, -w1 * 0.1); c.line_to(55 + w1 * 1.7, -w1 * 0.15); c.stroke()
        c.move_to(30, -w1 * 0.55); c.line_to(55, -w1 * 0.95); c.stroke()
    elif hand == 'fist':
        c.arc(62, 0, w1 * 0.55, 0, 6.28); c.fill()
        c.move_to(30, -w1 * 0.6); c.line_to(55, -w1 * 0.7); c.stroke()
    c.set_source_rgba(*SKIN_RIM, rim * a * 0.8); c.set_line_width(2.5)
    c.arc(30, 0, w1 * 0.95, -1.9, -0.6); c.stroke()
    c.restore()

def feather(c, x, y, s=1.0, ang=0.0, lit=1.0, t=0.0, a=1.0):
    """凤羽：全片唯一发光物。(x,y)=羽根，ang=羽尖方向（0朝上）"""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    fl = 1 + 0.06 * math.sin(t * 3.1) + 0.03 * math.sin(t * 7.3)
    if lit > 0:
        glow(c, 0, -170, 380 * fl, FEATHER, 0.55 * lit * a)
        glow(c, 0, -190, 150, (1, 0.9, 0.6), 0.5 * lit * a)
    dead = (0.22, 0.20, 0.19)
    vane_out = mix(dead, (0.95, 0.38, 0.12), lit); vane_in = mix((0.30, 0.28, 0.26), (1.0, 0.86, 0.45), lit)
    # 外羽片
    c.move_to(0, -20); c.curve_to(-70, -90, -80, -230, -10, -340); c.curve_to(40, -280, 70, -140, 0, -20); c.close_path()
    c.set_source_rgba(*vane_out, a); c.fill()
    # 内羽片
    c.move_to(0, -60); c.curve_to(-40, -110, -45, -230, -6, -305); c.curve_to(25, -250, 40, -140, 0, -60); c.close_path()
    c.set_source_rgba(*vane_in, a); c.fill()
    # 羽眼
    c.set_source_rgba(*mix(dead, (0.9, 0.2, 0.08), lit), a); c.save(); c.translate(-8, -265); c.scale(1, 1.4); c.arc(0, 0, 16, 0, 6.28); c.restore(); c.fill()
    c.set_source_rgba(*mix((0.12, 0.12, 0.12), (0.2, 0.05, 0.02), lit), a); c.arc(-8, -265, 8, 0, 6.28); c.fill()
    # 羽丝
    c.set_source_rgba(*mix(dead, (1, 0.7, 0.3), lit), 0.5 * a); c.set_line_width(1.5)
    for i in range(12):
        yy = -40 - i * 24; c.move_to(0, yy); c.line_to(-48 * math.sin((i + 1) / 13 * 3.0), yy - 30); c.move_to(0, yy); c.line_to(40 * math.sin((i + 1) / 13 * 3.0), yy - 26)
    c.stroke()
    # 羽轴
    c.set_source_rgba(*mix((0.4, 0.38, 0.35), (1, 0.95, 0.8), lit), a); c.set_line_width(4)
    c.move_to(0, 30); c.curve_to(0, -100, -4, -220, -10, -335); c.stroke()
    c.restore()

def eyelids(c, o, soft=60):
    """o=1 全睁，0 全闭"""
    if o >= 1: return
    o = cl(o); e = ease(o)
    cy = H / 2; ctr = cy - e * (cy + 160); cor = ctr + 420 * math.sin(math.pi * e) * 0.9
    for sgn in (1, -1):
        def Y(v): return cy + (v - cy) * sgn
        c.move_to(-50, Y(-300)); c.line_to(W + 50, Y(-300)); c.line_to(W + 50, Y(cor))
        c.curve_to(W * 0.7, Y(ctr), W * 0.3, Y(ctr), -50, Y(cor)); c.close_path()
        c.set_source_rgb(0, 0, 0); c.fill()
        for k in range(6):  # 柔边
            off = (k + 1) * soft / 6 * sgn
            c.move_to(-50, Y(cor) + off); c.curve_to(W * 0.3, Y(ctr) + off, W * 0.7, Y(ctr) + off, W + 50, Y(cor) + off)
            c.set_source_rgba(0, 0, 0, 0.12); c.set_line_width(soft / 6 * 2); c.stroke()

def slips(c, x, y, w, h, ang=0, a=1, n=None, col=(0.62, 0.50, 0.32), lines=True):
    """竹简（展开）"""
    c.save(); c.translate(x, y); c.rotate(ang)
    n = n or max(4, int(w / 26)); sw = w / n
    for i in range(n):
        shade = 0.85 + 0.15 * ((i * 7) % 3) / 2
        c.set_source_rgba(*(v * shade for v in col), a); c.rectangle(-w / 2 + i * sw + 1, -h / 2, sw - 3, h); c.fill()
        if lines:
            c.set_source_rgba(0.12, 0.08, 0.05, 0.55 * a)
            for j in range(int(h / 34) - 1):
                c.rectangle(-w / 2 + i * sw + sw * 0.3, -h / 2 + 18 + j * 34, sw * 0.4, 20); c.fill()
    c.set_source_rgba(0.25, 0.15, 0.08, a); c.set_line_width(3)
    for yy in (-h * 0.3, h * 0.3): c.move_to(-w / 2, yy); c.line_to(w / 2, yy)
    c.stroke(); c.restore()

def scroll_roll(c, x, y, L=220, r=26, ang=0, a=1, col=(0.58, 0.46, 0.30)):
    c.save(); c.translate(x, y); c.rotate(ang)
    c.set_source_rgba(*col, a); rr(c, -L / 2, -r, L, 2 * r, r); c.fill()
    c.set_source_rgba(0.3, 0.2, 0.1, a); c.set_line_width(2)
    for i in range(1, 8): c.move_to(-L / 2 + i * L / 8, -r); c.line_to(-L / 2 + i * L / 8, r)
    c.stroke(); c.set_source_rgba(0.5, 0.1, 0.08, a); c.rectangle(-6, -r - 2, 12, 2 * r + 4); c.fill()
    c.restore()

def tree(c, x, base, s=1, t=0, leaves=(0.06, 0.08, 0.05), seed=4):
    rnd = random.Random(seed)
    c.save(); c.translate(x, base); c.scale(s, s)
    c.set_source_rgb(*INK)
    c.move_to(-110, 0); c.curve_to(-70, -300, -90, -500, -40, -760); c.line_to(40, -760); c.curve_to(70, -500, 60, -300, 120, 0); c.close_path(); c.fill()
    br = [((-40, -600), (-420, -820), 44), ((30, -650), (480, -880), 44), ((0, -740), (-160, -1050), 36), ((10, -740), (260, -1080), 34), ((-50, -420), (-360, -560), 30)]
    c.set_line_cap(1)
    for (a0, a1, wd) in br:
        c.set_line_width(wd); c.move_to(*a0); c.curve_to(a0[0], a0[1] - 80, (a0[0] + a1[0]) / 2, a1[1] + 40, *a1); c.stroke()
    for i in range(70):
        lx = rnd.uniform(-650, 650); ly = rnd.uniform(-1200, -600) + abs(lx) * 0.25
        r = rnd.uniform(50, 120); sw = math.sin(t * 1.3 + i) * 4
        c.set_source_rgba(*leaves, 0.95); c.arc(lx + sw, ly, r, 0, 6.28); c.fill()
    c.restore()

def coffin(c, x, y, w, h, a=1):
    poly(c, [(x - w / 2, y), (x + w / 2, y), (x + w * 0.42, y - h), (x - w * 0.42, y - h)], (0.06, 0.04, 0.035), a)
    poly(c, [(x - w * 0.42, y - h), (x + w * 0.42, y - h), (x + w * 0.34, y - h * 1.35), (x - w * 0.34, y - h * 1.35)], (0.10, 0.07, 0.06), a)
    c.set_source_rgba(0.85, 0.82, 0.76, 0.75 * a); c.rectangle(x - 28, y - h * 1.35, 56, h * 1.35); c.fill()

def rain(c, t, n=220, a=0.35, seed=9, slant=-0.25):
    rnd = random.Random(seed); c.set_line_width(1.6)
    for i in range(n):
        x = rnd.uniform(-200, W + 200); sp = rnd.uniform(900, 1400); y = (rnd.uniform(0, H) + t * sp) % (H + 200) - 100
        L = rnd.uniform(30, 60)
        c.set_source_rgba(0.75, 0.8, 0.9, a * rnd.uniform(0.4, 1)); c.move_to(x + slant * (y), y); c.line_to(x + slant * (y + L), y + L); c.stroke()

def cup(c, x, y, s=1, a=1):
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-70, -80), (70, -80), (50, 0), (-50, 0)], (0.10, 0.06, 0.04), a)
    c.set_source_rgba(0.55, 0.12, 0.08, a); c.save(); c.translate(0, -80); c.scale(1, 0.22); c.arc(0, 0, 70, 0, 6.28); c.restore(); c.fill()
    c.set_source_rgba(0.75, 0.55, 0.3, 0.35 * a); c.set_line_width(2); c.save(); c.translate(0, -80); c.scale(1, 0.22); c.arc(0, 0, 70, 0, 6.28); c.restore(); c.stroke()
    c.restore()

def table(c, y, col=(0.07, 0.04, 0.03), rim=(0.5, 0.28, 0.14)):
    poly(c, [(-300, H + 300), (W + 300, H + 300), (W + 300, y), (-300, y)], col)
    c.set_source_rgba(*rim, 0.45); c.rectangle(-300, y, W + 600, 4); c.fill()

def arrow(c, x, y, ang, L=180, a=1, col=INK, w=4):
    c.save(); c.translate(x, y); c.rotate(ang); c.set_source_rgba(*col, a)
    c.set_line_width(w); c.move_to(-L, 0); c.line_to(0, 0); c.stroke()
    poly(c, [(0, -w * 2.2), (w * 5, 0), (0, w * 2.2)], col, a)
    poly(c, [(-L, 0), (-L - 20, -w * 3), (-L + 30, 0), (-L - 20, w * 3)], col, a)
    c.restore()

def plaque(c, x, y, s, a=1, w=260, h=520, col=GOLD):
    c.set_source_rgba(0.12, 0.06, 0.03, a); rr(c, x - w / 2, y - h / 2, w, h, 12); c.fill()
    c.set_source_rgba(0.55, 0.35, 0.18, 0.7 * a); c.set_line_width(5); rr(c, x - w / 2 + 12, y - h / 2 + 12, w - 24, h - 24, 8); c.stroke()
    n = len(s); fs = min(w * 0.6, (h - 80) / n)
    for i, ch in enumerate(s):
        text(c, ch, x, y - h / 2 + 50 + fs * (i + 0.85), fs, col, a, 'c')

def stele(c, x, y, w, h, s, a=1):
    poly(c, [(x - w / 2, y), (x + w / 2, y), (x + w * 0.46, y - h), (x - w * 0.46, y - h)], (0.16, 0.16, 0.17), a)
    c.save(); c.translate(x, y - h); c.scale(1, 0.35); c.arc(0, 0, w * 0.46, 3.1416, 6.2832); c.restore()
    c.set_source_rgba(0.16, 0.16, 0.17, a); c.fill()
    c.set_source_rgba(0.3, 0.3, 0.3, 0.5 * a); c.set_line_width(3); c.rectangle(x - w * 0.34, y - h + 40, w * 0.68, h - 80); c.stroke()
    fs = (h - 140) / len(s)
    for i, ch in enumerate(s): text(c, ch, x, y - h + 70 + fs * (i + 0.85), fs * 0.92, (0.62, 0.15, 0.12), a, 'c', shadow=False)

def fog(c, t, y=700, a=0.25, seed=2):
    rnd = random.Random(seed)
    for i in range(16):
        x = (rnd.uniform(-300, W + 300) + t * rnd.uniform(10, 30)) % (W + 600) - 300
        yy = y + rnd.uniform(-200, 250); r = rnd.uniform(220, 420)
        g = cairo.RadialGradient(x, yy, 0, x, yy, r)
        g.add_color_stop_rgba(0, 0.6, 0.62, 0.66, a); g.add_color_stop_rgba(1, 0.6, 0.62, 0.66, 0)
        c.set_source(g); c.arc(x, yy, r, 0, 6.28); c.fill()

def label(c, s, x, y, size=44, a=1, col=(0.92, 0.88, 0.80)):
    text(c, s, x, y, size, col, a, 'c')

def bust(c, x, y, s=1, hat='bun', a=1, col=INK, robe=None):
    """正面半身剪影（近景，面向你）"""
    c.save(); c.translate(x, y); c.scale(s, s)
    rc = robe or col
    c.set_source_rgba(*rc, a)
    c.move_to(-230, 0); c.curve_to(-220, -150, -150, -210, -60, -230); c.line_to(60, -230); c.curve_to(150, -210, 220, -150, 230, 0); c.close_path(); c.fill()
    # 交领
    c.set_source_rgba(0.45, 0.38, 0.30, 0.35 * a); c.set_line_width(4); c.move_to(-60, -228); c.line_to(30, -60); c.move_to(60, -228); c.line_to(-10, -120); c.stroke()
    c.set_source_rgba(*col, a); c.rectangle(-28, -270, 56, 50); c.fill()
    c.save(); c.translate(0, -340); c.scale(0.86, 1); c.arc(0, 0, 80, 0, 6.28); c.restore(); c.fill()
    if hat == 'bun': c.arc(0, -430, 34, 0, 6.28); c.fill(); c.rectangle(-8, -470, 16, 30); c.fill()
    elif hat == 'guan':
        poly(c, [(-60, -395), (60, -395), (50, -470), (-36, -455)], col, a)
        c.set_source_rgba(0.55, 0.42, 0.30, 0.45 * a); c.set_line_width(3); c.move_to(-60, -395); c.line_to(50, -470); c.stroke()
    elif hat == 'helm':
        c.set_source_rgba(*col, a); c.arc(0, -350, 92, 3.3, 6.12); c.fill(); c.set_line_width(5); c.move_to(0, -440); c.line_to(0, -520); c.stroke()
        c.set_source_rgba(0.75, 0.15, 0.1, a); c.arc(0, -525, 14, 0, 6.28); c.fill()
    c.restore()

from song import *

BRICK = (0.40, 0.38, 0.36)
BRICKD = (0.26, 0.25, 0.24)

_stars = [(random.Random(k).uniform(0, W), random.Random(k + 5).uniform(0, 620), random.Random(k + 9).uniform(0.6, 2.2),
           random.Random(k + 3).uniform(0, 6.28)) for k in range(160)]


def bg_night(c, T, horizon=760, moonxy=(1650, 170), warm=0.0):
    g = cairo.LinearGradient(0, 0, 0, horizon)
    g.add_color_stop_rgb(0, 0.025, 0.03, 0.055); g.add_color_stop_rgb(0.75, 0.06, 0.07, 0.10)
    g.add_color_stop_rgb(1, 0.13 + 0.2 * warm, 0.11 + 0.06 * warm, 0.10)
    c.set_source(g); c.paint()
    for (x, y, r, ph) in _stars:
        if x < 1050 and y < 520: continue  # keep caption zone clean
        rgba(c, (0.9, 0.9, 1.0), 0.35 + 0.35 * math.sin(T * 1.5 + ph)); c.arc(x, y, r, 0, 6.283); c.fill()
    if moonxy:
        mx, my = moonxy
        spot(c, mx, my, 300, 0.5, (0.8, 0.85, 1.0))
        rgba(c, (0.93, 0.92, 0.84)); c.arc(mx, my, 46, 0, 6.283); c.fill()
        rgba(c, (0.03, 0.035, 0.06)); c.arc(mx + 20, my - 10, 42, 0, 6.283); c.fill()
    # dunes
    for k, (yy, col, amp) in enumerate(((horizon - 40, (0.09, 0.08, 0.08), 40), (horizon + 30, (0.07, 0.06, 0.055), 55), (horizon + 120, (0.05, 0.045, 0.04), 30))):
        c.move_to(0, H)
        for x in range(0, W + 41, 40):
            c.line_to(x, yy + amp * math.sin(x / 260 + k * 2) + amp * 0.4 * math.sin(x / 90 + k))
        c.line_to(W, H); c.close_path(); rgba(c, col); c.fill()


def wall(c, x0, x1, ybase, h=120, a=1.0, towers=(), lit=0.0):
    if a <= 0: return
    rgba(c, BRICKD, a); c.rectangle(x0, ybase - h, x1 - x0, h); c.fill()
    rgba(c, BRICK, a); c.rectangle(x0, ybase - h, x1 - x0, 14); c.fill()
    m = 26
    for k in range(int((x1 - x0) / (m * 2)) + 1):
        c.rectangle(x0 + k * m * 2, ybase - h - 22, m, 22)
    c.fill()
    rgba(c, (0, 0, 0), 0.25 * a); c.set_line_width(1.5)
    for r in range(1, int(h / 22)):
        c.move_to(x0, ybase - h + r * 22); c.line_to(x1, ybase - h + r * 22)
    c.stroke()
    for tx in towers:
        rgba(c, BRICK, a); c.rectangle(tx - 60, ybase - h - 90, 120, h + 90); c.fill()
        rgba(c, BRICKD, a)
        for k in range(4): c.rectangle(tx - 60 + k * 34, ybase - h - 112, 20, 22)
        c.fill()
        rgba(c, lerpc((0.08, 0.07, 0.06), (1.0, 0.75, 0.4), lit), a); c.rectangle(tx - 14, ybase - h - 60, 28, 38); c.fill()


def gatehouse(c, x, ybase, s=1.0, a=1.0, open_=0.0, bridge=1.0, lit=0.6):
    """Ming 关城 gate with two-tier 城楼 and drawbridge (bridge=1 raised)"""
    if a <= 0: return
    c.save(); c.translate(x, ybase); c.scale(s, s)
    wall(c, -900, 900, 0, 300, a, (), 0)
    rgba(c, BRICK, a); c.rectangle(-260, -330, 520, 330); c.fill()
    # arch
    rgba(c, (0.03, 0.025, 0.02), a)
    c.move_to(-80, 0); c.line_to(-80, -150); c.arc(0, -150, 80, math.pi, 2 * math.pi); c.line_to(80, 0); c.close_path(); c.fill()
    # doors
    dw = 80 * (1 - open_)
    rgba(c, (0.36, 0.14, 0.08), a); c.rectangle(-80, -230, dw, 230); c.rectangle(80 - dw, -230, dw, 230); c.fill()
    rgba(c, GOLD, 0.7 * a)
    for k in range(5):
        for j in range(3):
            c.arc(-70 + j * 22, -200 + k * 40, 3, 0, 6.283); c.fill(); c.arc(70 - j * 22, -200 + k * 40, 3, 0, 6.283); c.fill()
    # 城楼
    rgba(c, (0.55, 0.13, 0.10), a)
    for k in range(6): c.rectangle(-210 + k * 84, -460, 16, 130)
    c.fill()
    rgba(c, lerpc((0.15, 0.08, 0.05), (0.95, 0.70, 0.35), lit), a)
    for k in range(5): c.rectangle(-194 + k * 84, -440, 68, 100)
    c.fill()
    rgba(c, (0.16, 0.17, 0.19), a)
    c.move_to(-330, -470); c.curve_to(-250, -480, -200, -510, -170, -540); c.line_to(170, -540); c.curve_to(200, -510, 250, -480, 330, -470)
    c.line_to(300, -490); c.line_to(-300, -490); c.close_path(); c.fill()
    c.rectangle(-240, -560, 480, 30); c.fill()
    c.move_to(-280, -556); c.curve_to(-220, -566, -180, -600, -150, -640); c.line_to(150, -640); c.curve_to(180, -600, 220, -566, 280, -556); c.close_path(); c.fill()
    rgba(c, GOLD, 0.5 * a); c.rectangle(-330, -472, 660, 3); c.fill()
    # plaque
    rgba(c, (0.12, 0.10, 0.09), a); c.rectangle(-60, -320, 120, 60); c.fill()
    text2(c, "关", 0, -276, 40, 99, GOLDT, a, 'c', fam=FONT_B)
    # drawbridge
    ang = bridge * 1.35
    c.save(); c.translate(0, 0); 
    rgba(c, (0.30, 0.22, 0.14), a)
    c.move_to(-90, 0); c.line_to(90, 0); c.line_to(90 - 0, -0)
    c.restore()
    L = 230
    ex, ey = 0, -L * math.sin(ang)
    rgba(c, (0.32, 0.23, 0.15), a)
    c.move_to(-95, 0); c.line_to(95, 0); c.line_to(95 * 0.9, ey + 0.0 - 0); c.line_to(-95 * 0.9, ey); c.close_path(); c.fill()
    rgba(c, (0.15, 0.15, 0.15), a); c.set_line_width(4)
    c.move_to(-110, -250); c.line_to(-85, ey); c.move_to(110, -250); c.line_to(85, ey); c.stroke()
    # moat
    rgba(c, (0.06, 0.08, 0.11), a); c.rectangle(-900, 0, 1800, 40); c.fill()
    c.restore()


def yurt(c, x, yf, s=1.0, a=1.0, lit=0.3):
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, (0.62, 0.56, 0.46), a)
    c.move_to(-90, 0); c.line_to(-90, -70); c.curve_to(-60, -110, 60, -110, 90, -70); c.line_to(90, 0); c.close_path(); c.fill()
    rgba(c, (0.40, 0.30, 0.22), a); c.set_line_width(4); c.move_to(-90, -40); c.line_to(90, -40); c.stroke()
    rgba(c, lerpc((0.15, 0.1, 0.06), (1.0, 0.72, 0.35), lit), a); c.rectangle(-18, -50, 36, 50); c.fill()
    c.restore()


def campfire(c, x, yf, T, a=1.0, s=1.0):
    if a <= 0: return
    spot(c, x, yf - 30 * s, 220 * s, 0.9 * a)
    flames(c, x, yf, 50 * s, 80 * s, T, a)


def grassfire(c, x0, x1, yf, T, prog, a=1.0):
    if a <= 0 or prog <= 0: return
    xe = x0 + (x1 - x0) * prog
    spot(c, (x0 + xe) / 2, yf - 60, max(200, (xe - x0) * 0.7), 0.9 * a, (1, 0.5, 0.2))
    n = int((xe - x0) / 46) + 1
    for k in range(n):
        xx = x0 + k * 46
        h = 70 + 40 * math.sin(k * 1.3 + T * 5)
        flames(c, xx, yf + 8 * math.sin(k), 40, h * (1 if xx < xe - 60 else 0.6), T + k * 0.3, a)
    rgba(c, (0.05, 0.03, 0.02), 0.6 * a); c.rectangle(x0, yf, xe - x0, 30); c.fill()


def grass(c, x0, x1, yf, T, a=1.0, h=40, col=(0.20, 0.22, 0.14)):
    if a <= 0: return
    rgba(c, col, a); c.set_line_width(3)
    for k in range(int((x1 - x0) / 14)):
        xx = x0 + k * 14 + 5 * math.sin(k * 7)
        hh = h * (0.6 + 0.4 * math.sin(k * 3.1))
        c.move_to(xx, yf); c.line_to(xx + 8 * math.sin(T * 1.5 + k * 0.4), yf - hh)
    c.stroke()


def lantern(c, x, y, s=1.0, a=1.0, T=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    spot(c, 0, 0, 120, 0.6 * a)
    rgba(c, (0.9, 0.55, 0.25), a); c.save(); c.scale(34, 46); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    rgba(c, (0.2, 0.15, 0.1), a); c.rectangle(-20, -52, 40, 10); c.rectangle(-20, 42, 40, 10); c.fill()
    rgba(c, (0.6, 0.3, 0.12), a); c.set_line_width(2)
    for k in (-18, 0, 18): c.move_to(k, -42); c.curve_to(k * 1.6, 0, k * 1.6, 0, k, 42)
    c.stroke(); c.restore()


def rocket(c, x, y, s=1.0, a=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.45, 0.30, 0.18), a); c.rectangle(-3, -40, 6, 120); c.fill()
    rgba(c, (0.70, 0.15, 0.10), a); c.rectangle(-12, -70, 24, 50); c.fill()
    c.move_to(-12, -70); c.line_to(0, -92); c.line_to(12, -70); c.fill()
    c.restore()


def gun3(c, x, y, s=1.0, a=1.0):
    """三眼铳"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.45, 0.30, 0.18), a); c.rectangle(-140, -6, 120, 12); c.fill()
    rgba(c, (0.35, 0.36, 0.38), a)
    for k in (-14, 0, 14): rrect(c, -30, k - 6, 140, 12, 5); c.fill()
    rgba(c, (0.5, 0.5, 0.52), a); c.rectangle(-30, -22, 18, 44); c.rectangle(60, -22, 10, 44); c.fill()
    c.restore()


def drum(c, x, y, s=1.0, a=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.55, 0.14, 0.10), a); c.rectangle(-50, -40, 100, 80); c.fill()
    rgba(c, (0.86, 0.78, 0.60), a); c.save(); c.translate(-50, 0); c.scale(14, 40); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    rgba(c, GOLD, a)
    for k in range(5): c.arc(-30 + k * 18, -30, 3, 0, 6.283); c.fill(); c.arc(-30 + k * 18, 30, 3, 0, 6.283); c.fill()
    c.restore()


def stele(c, x, yf, s=1.0, a=1.0, lines=("远哨夜不收", "离关一百里")):
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, (0.36, 0.35, 0.33), a); c.move_to(-110, 0); c.line_to(-100, -330); c.curve_to(-60, -360, 60, -360, 100, -330); c.line_to(110, 0); c.close_path(); c.fill()
    rgba(c, (0.28, 0.27, 0.26), a); c.set_line_width(3); c.move_to(-80, -300); c.line_to(80, -300); c.stroke()
    for j, ln in enumerate(lines):
        for k, ch in enumerate(ln):
            text2(c, ch, 40 - j * 70, -250 + k * 44, 36, 99, (0.86, 0.82, 0.74), a, 'c', fam=FONT_B)
    c.restore()


def arrows_flying(c, x0, y0, x1, y1, T, n, a=1.0):
    if a <= 0: return
    for k in range(n):
        u = ((T * 1.2 + k / n) % 1)
        x = lerp(x0, x1, u); y = lerp(y0, y1, u) - 120 * math.sin(u * math.pi)
        ang = math.atan2((y1 - y0) - 120 * math.pi * math.cos(u * math.pi), x1 - x0)
        c.save(); c.translate(x + k * 18, y + k * 9); c.rotate(ang)
        rgba(c, (0.85, 0.80, 0.70), a); c.set_line_width(3); c.move_to(-40, 0); c.line_to(0, 0); c.stroke()
        c.move_to(0, 0); c.line_to(-10, -5); c.line_to(-10, 5); c.fill()
        c.restore()

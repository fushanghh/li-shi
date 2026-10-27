"""Song Ci case: bright outdoor road, tree, hanged figure, neck diagrams, village, woodshed, sickles."""
from qing import *

ROPE = (0.86, 0.74, 0.50)
PURP = (0.62, 0.12, 0.22)
SONGCI = 'official'
RICH = (0.58, 0.40, 0.18)


def bg_day(c, T, horizon=860, warm=0.55, hills=True):
    """bright dawn countryside"""
    g = cairo.LinearGradient(0, 0, 0, horizon)
    g.add_color_stop_rgb(0, 0.30, 0.38, 0.56); g.add_color_stop_rgb(0.6, *lerpc((0.62, 0.62, 0.66), (0.86, 0.62, 0.42), warm))
    g.add_color_stop_rgb(1, *lerpc((0.88, 0.80, 0.62), (1.0, 0.76, 0.46), warm))
    c.set_source(g); c.paint()
    spot(c, 1500, horizon - 40, 700, 0.9, (1.0, 0.86, 0.55))
    if hills:
        for k, (yb, col) in enumerate(((horizon - 150, (0.52, 0.50, 0.56)), (horizon - 80, (0.40, 0.40, 0.42)))):
            rgba(c, col); c.move_to(0, horizon)
            for x in range(0, W + 41, 40):
                c.line_to(x, yb + 40 * math.sin(x / (230 + k * 90) + k * 2) + 22 * math.sin(x / 97 + k))
            c.line_to(W, horizon); c.close_path(); c.fill()
    g2 = cairo.LinearGradient(0, horizon, 0, H)
    g2.add_color_stop_rgb(0, 0.50, 0.46, 0.30); g2.add_color_stop_rgb(1, 0.26, 0.24, 0.16)
    c.set_source(g2); c.rectangle(0, horizon, W, H - horizon); c.fill()
    # road
    rgba(c, (0.70, 0.60, 0.44)); c.move_to(0, horizon + 70); c.line_to(W, horizon + 40); c.line_to(W, horizon + 120); c.line_to(0, horizon + 170); c.close_path(); c.fill()
    rgba(c, (0.82, 0.74, 0.56)); c.rectangle(0, horizon, W, 4); c.fill()


def bg_night2(c, T, horizon=860):
    g = cairo.LinearGradient(0, 0, 0, horizon)
    g.add_color_stop_rgb(0, 0.08, 0.10, 0.22); g.add_color_stop_rgb(1, 0.22, 0.24, 0.40)
    c.set_source(g); c.paint()
    from ming import _stars
    for (x, y, r, ph) in _stars:
        rgba(c, (0.95, 0.95, 1.0), 0.5 + 0.35 * math.sin(T * 1.5 + ph)); c.arc(x, y, r, 0, 6.283); c.fill()
    rgba(c, (0.98, 0.95, 0.82)); c.arc(1660, 170, 56, 0, 6.283); c.fill()
    spot(c, 1660, 170, 360, 0.6, (0.85, 0.88, 1.0))
    rgba(c, (0.16, 0.17, 0.24)); c.rectangle(0, horizon, W, H - horizon); c.fill()
    rgba(c, (0.28, 0.27, 0.34)); c.move_to(0, horizon + 70); c.line_to(W, horizon + 40); c.line_to(W, horizon + 120); c.line_to(0, horizon + 170); c.close_path(); c.fill()


def tree(c, x, yf, s=1.0, a=1.0, T=0):
    """old 槐树 with a long branch reaching right at ~-560 (local); returns branch hook point"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, (0.30, 0.20, 0.13), a)
    c.move_to(-60, 0); c.curve_to(-40, -200, -50, -380, -30, -560); c.line_to(30, -560); c.curve_to(40, -380, 30, -200, 70, 0); c.close_path(); c.fill()
    c.set_line_width(26); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(0, -520); c.curve_to(120, -560, 260, -570, 380, -560); c.stroke()
    c.set_line_width(20); c.move_to(-10, -540); c.curve_to(-120, -620, -180, -660, -230, -700); c.stroke()
    c.set_line_width(16); c.move_to(10, -560); c.line_to(40, -720); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    for (fx, fy, r, col) in ((-220, -720, 110, (0.30, 0.42, 0.24)), (40, -770, 140, (0.36, 0.50, 0.28)), (220, -650, 120, (0.32, 0.46, 0.26)),
                             (380, -610, 90, (0.38, 0.52, 0.30)), (-90, -640, 100, (0.40, 0.54, 0.30))):
        rgba(c, col, a); c.arc(fx + 4 * math.sin(T + fx), fy, r, 0, 6.283); c.fill()
        rgba(c, (0.55, 0.68, 0.38), 0.5 * a); c.arc(fx - r * 0.3, fy - r * 0.3, r * 0.45, 0, 6.283); c.fill()
    c.restore()


def hanged(c, hx, hy, s=1.0, a=1.0, sway=0.0, rope_slack=0.0, T=0, kind='commoner2'):
    """figure hanging from point (hx,hy). rope_slack wobbles the rope"""
    if a <= 0: return
    L = 150 * s
    c.save(); c.translate(hx, hy); c.rotate(sway)
    rgba(c, ROPE, a); c.set_line_width(6 * s)
    c.move_to(0, 0)
    if rope_slack > 0:
        w = rope_slack * 26 * s * math.sin(T * 9)
        c.curve_to(w, L * 0.33, -w, L * 0.66, 0, L)
    else:
        c.line_to(0, L)
    c.stroke()
    sperson(c, 0, L + 350 * s, s, kind, a, 1, 'stand')
    rgba(c, ROPE, a); c.set_line_width(7 * s); c.arc(2 * s, L + 22 * s, 15 * s, 0, 6.283); c.stroke()
    c.restore()


def supine(c, x, y, s=1.0, a=1.0, kind='commoner2', mat=True):
    """body lying on its back on a straw mat, head left"""
    if a <= 0: return
    if mat:
        rgba(c, (0.80, 0.68, 0.42), a); rrect(c, x - 330 * s, y - 10 * s, 640 * s, 40 * s, 8 * s); c.fill()
        rgba(c, (0.62, 0.50, 0.28), a); c.set_line_width(2)
        for k in range(16):
            xx = x - 320 * s + k * 40 * s; c.move_to(xx, y - 8 * s); c.line_to(xx, y + 28 * s)
        c.stroke()
    c.save(); c.translate(x + 150 * s, y - 34 * s); c.rotate(-math.pi / 2)
    sperson(c, 0, 0, s, kind, a, 1, 'stand')
    c.restore()


def stickman_tap(c, x0, y0, x1, y1, a=1.0):
    if a <= 0: return
    rgba(c, (0.45, 0.30, 0.16), a); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y0); c.line_to(x1, y1); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)


def dim(c, x0, y0, x1, y1, txt, a=1.0, t=99, col=GOLDL, size=40, off=(30, 0)):
    """dimension line with end ticks + label"""
    if a <= 0: return
    p = ease(clamp(t / 0.6))
    xe, ye = lerp(x0, x1, p), lerp(y0, y1, p)
    rgba(c, (0.05, 0.04, 0.03), 0.8 * a); c.set_line_width(9); c.move_to(x0, y0); c.line_to(xe, ye); c.stroke()
    rgba(c, col, a); c.set_line_width(4); c.set_dash([14, 8]); c.move_to(x0, y0); c.line_to(xe, ye); c.stroke(); c.set_dash([])
    ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
    for (px, py) in ((x0, y0), (xe, ye)):
        c.move_to(px - 18 * math.cos(ang), py - 18 * math.sin(ang)); c.line_to(px + 18 * math.cos(ang), py + 18 * math.sin(ang))
    c.set_line_width(5); c.stroke()
    if p > 0.6:
        text2(c, txt, (x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], size, t - 0.6, col, a, 'l', 0.03, 0.2, FONT_X)


def neck(c, x, y, s=1.0, a=1.0, marks=(), T=0, t=99):
    """big profile head + neck diagram (facing right). marks: list of ('purple'|'white'|'flat', t0)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.99, 0.93, 0.80), 0.10 * a); c.arc(0, 0, 330, 0, 6.283); c.fill()
    rgba(c, (0.88, 0.72, 0.56), a)
    # neck
    c.move_to(-80, 40); c.curve_to(-80, 120, -90, 200, -110, 300); c.line_to(120, 300); c.curve_to(90, 200, 80, 120, 80, 60); c.close_path(); c.fill()
    # head
    c.move_to(-130, -60); c.curve_to(-150, -230, 60, -290, 130, -170); c.curve_to(150, -140, 150, -110, 165, -90)
    c.line_to(185, -40); c.line_to(160, -30); c.curve_to(170, 0, 160, 30, 140, 40); c.curve_to(120, 80, 60, 100, 0, 90)
    c.curve_to(-60, 90, -120, 40, -130, -60); c.close_path(); c.fill()
    rgba(c, (0.80, 0.62, 0.46), a); c.save(); c.translate(-20, -40); c.scale(30, 42); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()  # ear
    rgba(c, HAT, a)
    c.move_to(-140, -60); c.curve_to(-160, -240, 70, -310, 140, -160); c.curve_to(60, -200, -40, -160, -60, -60); c.close_path(); c.fill()
    rgba(c, (0.25, 0.15, 0.12), 0.8 * a); c.set_line_width(5); c.move_to(105, -95); c.line_to(130, -92); c.stroke()  # closed eye
    rgba(c, (0.55, 0.30, 0.28), a); c.set_line_width(5); c.move_to(120, 22); c.line_to(150, 18); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for (kind, t0) in marks:
        p = ease(seg(t, t0, t0 + 0.8))
        if p <= 0: continue
        if kind == 'purple':   # rises diagonally from throat to behind the ear
            pts = [(100, 150), (40, 120), (-30, 60), (-50, -4)]
            for lw, col, al in ((30, PURP, 0.35), (16, PURP, 1.0)):
                rgba(c, col, al * a * p); c.set_line_width(lw)
                c.move_to(*pts[0]); c.curve_to(*pts[1], *pts[2], *pts[3]); c.stroke()
        elif kind == 'white':
            rgba(c, (0.98, 0.98, 0.96), a * p); c.set_line_width(10)
            c.move_to(92, 210); c.curve_to(30, 205, -30, 200, -88, 196); c.stroke()
        elif kind == 'flat':
            for lw, col, al in ((26, (0.25, 0.10, 0.12), 0.35), (14, (0.25, 0.10, 0.12), 1.0)):
                rgba(c, col, al * a * p); c.set_line_width(lw)
                c.move_to(94, 160); c.curve_to(30, 160, -30, 160, -84, 160); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.restore()


def hut(c, x, yf, s=1.0, a=1.0, hl=0.0, label_=None, T=0):
    """small Song farmhouse; hl = gold highlight"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    if hl > 0: spot(c, 0, -120, 330, hl)
    rgba(c, (0.90, 0.85, 0.74), a); c.rectangle(-130, -150, 260, 150); c.fill()
    rgba(c, (0.36, 0.22, 0.14), a); c.rectangle(-30, -100, 60, 100); c.fill()
    rgba(c, (0.98, 0.82, 0.48) if hl > 0 else (0.40, 0.30, 0.20), a); c.rectangle(-105, -120, 46, 40); c.fill(); c.rectangle(60, -120, 46, 40); c.fill()
    rgba(c, (0.30, 0.30, 0.34), a)
    c.move_to(-175, -140); c.curve_to(-120, -150, -90, -190, -70, -220); c.line_to(70, -220); c.curve_to(90, -190, 120, -150, 175, -140)
    c.line_to(160, -160); c.line_to(-160, -160); c.close_path(); c.fill()
    c.rectangle(-80, -232, 160, 14); c.fill()
    if hl > 0:
        rgba(c, GOLDL, hl * a); c.set_line_width(6); c.rectangle(-134, -154, 268, 158); c.stroke()
    c.restore()
    if label_:
        bigtag(c, label_, x, yf + 70 * s, 44 * s, T, GOLDT if hl > 0 else TXT, a)


def shed(c, T, beam_y=260, dust=1.0, rub=0.0, lamp_x=1400):
    """woodshed interior: plank walls, big beam, firewood"""
    g = cairo.LinearGradient(0, 0, 0, 900)
    g.add_color_stop_rgb(0, 0.30, 0.22, 0.15); g.add_color_stop_rgb(1, 0.46, 0.34, 0.22)
    c.set_source(g); c.paint()
    for k in range(14):
        rgba(c, (0.24, 0.17, 0.11), 0.7); c.rectangle(k * 140, 0, 4, 900); c.fill()
    rgba(c, (0.62, 0.48, 0.30)); c.rectangle(0, 900, W, H - 900); c.fill()
    rgba(c, (0.78, 0.62, 0.40)); c.rectangle(0, 900, W, 5); c.fill()
    spot(c, lamp_x, 520, 900, 1.0)
    # firewood stack
    for r in range(4):
        for k in range(7 - r):
            xx = 220 + k * 64 + r * 32; yy = 870 - r * 56
            rgba(c, (0.55, 0.38, 0.22)); c.arc(xx, yy, 30, 0, 6.283); c.fill()
            rgba(c, (0.78, 0.62, 0.40)); c.arc(xx, yy, 20, 0, 6.283); c.fill()
            rgba(c, (0.55, 0.38, 0.22)); c.arc(xx, yy, 8, 0, 6.283); c.fill()
    # beam
    rgba(c, (0.36, 0.24, 0.14)); c.rectangle(0, beam_y, W, 70); c.fill()
    rgba(c, (0.50, 0.36, 0.22)); c.rectangle(0, beam_y, W, 10); c.fill()
    # dust layer on beam top
    rnd = random.Random(3)
    for k in range(260):
        xx = rnd.uniform(0, W); yy = beam_y - rnd.uniform(0, 6)
        disturbed = abs(xx - 1180) < 70
        if disturbed and rub > 0:
            xx += rnd.uniform(-60, 60) * rub; yy -= rnd.uniform(0, 30) * rub
        rgba(c, (0.82, 0.78, 0.70), 0.6 * dust); c.arc(xx, yy, rnd.uniform(1.5, 4), 0, 6.283); c.fill()
    rgba(c, (0.80, 0.76, 0.68), 0.75 * dust); c.rectangle(0, beam_y - 4, 1110, 4); c.rectangle(1250, beam_y - 4, W, 4); c.fill()
    if rub > 0:
        rgba(c, (0.55, 0.40, 0.25), rub); c.set_line_width(5)
        for k in range(6):
            c.move_to(1120 + k * 22, beam_y - 2); c.line_to(1130 + k * 22, beam_y + 68); c.stroke()


def bench(c, x, yf, s=1.0, a=1.0, tipped=0.0):
    if a <= 0: return
    c.save(); c.translate(x, yf); c.rotate(-1.4 * tipped); c.scale(s, s)
    rgba(c, (0.50, 0.32, 0.18), a); c.rectangle(-90, -80, 180, 18); c.fill()
    c.rectangle(-76, -62, 14, 62); c.fill(); c.rectangle(62, -62, 14, 62); c.fill()
    c.restore()


def sickle(c, x, y, s=1.0, a=1.0, rot=0.0, blood=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rgba(c, (0.50, 0.34, 0.18), a); c.rectangle(-6, 0, 12, 110); c.fill()
    rgba(c, (0.78, 0.80, 0.84), a)
    c.move_to(-6, 4); c.curve_to(-20, -70, 50, -110, 110, -80); c.curve_to(60, -84, 10, -60, 8, 4); c.close_path(); c.fill()
    if blood > 0:
        rgba(c, (0.55, 0.08, 0.08), 0.8 * blood * a); c.arc(40, -66, 10, 0, 6.283); c.fill(); c.arc(70, -80, 6, 0, 6.283); c.fill()
    c.restore()


def flies(c, x, y, n, T, a=1.0, r=60):
    if a <= 0: return
    for k in range(n):
        ph = k * 2.39
        fx = x + r * math.sin(T * (2.1 + k * 0.13) + ph) * (0.5 + 0.5 * math.sin(k))
        fy = y + r * 0.6 * math.cos(T * (2.7 + k * 0.11) + ph * 1.3)
        rgba(c, (0.04, 0.04, 0.05), a); c.save(); c.translate(fx, fy); c.scale(10, 7); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
        rgba(c, (0.85, 0.88, 0.95), 0.6 * a)
        wv = 4 * abs(math.sin(T * 40 + k))
        c.save(); c.translate(fx - 2, fy - 4); c.scale(6, 3 + wv); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()


def checkline(c, x, y, s_, t, size=52, ok=True):
    if t < 0: return
    p = ease(clamp(t / 0.4))
    col = GOLDL if ok else REDL
    rgba(c, col, p); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x, y - 16); c.line_to(x + 16, y); c.line_to(x + 44, y - 36); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
    text2(c, s_, x + 70, y, size, t, TXT, 1, 'l', 0.03, 0.2, FONT_X)


def stretcher(c, x, yf, s, a, walk, T):
    """two men carrying a plank with a body"""
    sperson(c, x - 230 * s, yf, s, 'commoner', a, 1, 'hold', walk=walk)
    sperson(c, x + 230 * s, yf, s, 'commoner2', a, 1, 'hold', walk=walk + 1.6 if walk is not None else None, robe=RICH)
    yb = yf - 170 * s
    rgba(c, (0.55, 0.40, 0.24), a); c.rectangle(x - 290 * s, yb, 580 * s, 14 * s); c.fill()
    supine(c, x, yb - 4 * s, 0.75 * s, a, mat=False)


def scroll_h(c, x, y, w, h, a=1.0, txt='', size=46, t=99):
    if a <= 0: return
    rgba(c, (0, 0, 0), 0.35 * a); c.rectangle(x - w / 2 + 8, y - h / 2 + 10, w, h); c.fill()
    rgba(c, (0.95, 0.90, 0.78), a); c.rectangle(x - w / 2, y - h / 2, w, h); c.fill()
    rgba(c, (0.45, 0.28, 0.16), a)
    for sx in (x - w / 2 - 14, x + w / 2 - 6):
        rrect(c, sx, y - h / 2 - 16, 20, h + 32, 8); c.fill()
    rgba(c, RED, 0.7 * a); c.set_line_width(3); c.rectangle(x - w / 2 + 12, y - h / 2 + 10, w - 24, h - 20); c.stroke()
    fnt(c, size, FONT_X); w_ = c.text_extents(txt)[4]
    rgba(c, (0.55, 0.10, 0.07), a * clamp(t / 0.4)); c.move_to(x - w_ / 2, y + size * 0.36); c.show_text(txt)

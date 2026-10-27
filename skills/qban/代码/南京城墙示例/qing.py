"""Qing palace: brighter backgrounds, Qing men (暖帽+辫), Qing women (两把头+旗袍+花盆底), swaddled baby, room."""
from gong import *

QROBE = {'qemp': (0.95, 0.76, 0.22), 'qoff': (0.20, 0.22, 0.34), 'qeunuch': (0.24, 0.36, 0.56), 'anda': (0.42, 0.30, 0.22),
         'qprince': (0.36, 0.50, 0.66), 'qkid': (0.80, 0.62, 0.30), 'qguard': (0.50, 0.16, 0.12)}
QLADY = {'qconsort': ((0.86, 0.36, 0.42), (0.95, 0.80, 0.40)), 'qempress': ((0.95, 0.72, 0.22), (0.30, 0.42, 0.70)),
         'qconcub': ((0.46, 0.66, 0.56), (0.92, 0.86, 0.66)), 'qmaid': ((0.40, 0.62, 0.66), (0.90, 0.86, 0.74)),
         'qmaid2': ((0.70, 0.52, 0.76), (0.92, 0.86, 0.74)), 'mama': ((0.34, 0.40, 0.58), (0.80, 0.76, 0.64)),
         'baomu': ((0.52, 0.40, 0.30), (0.86, 0.80, 0.66)), 'han': ((0.30, 0.42, 0.62), (0.24, 0.24, 0.28)),
         'qgirl': ((0.92, 0.56, 0.52), (0.95, 0.88, 0.72))}


def bg_dark2(c, T, sx=1200, sy=600, sr=700):
    g = cairo.RadialGradient(sx, sy, 0, sx, sy, max(sr * 1.6, 1200))
    g.add_color_stop_rgb(0, 0.30, 0.20, 0.12); g.add_color_stop_rgb(0.5, 0.15, 0.10, 0.07); g.add_color_stop_rgb(1, 0.08, 0.06, 0.05)
    c.set_source(g); c.paint()


def bg_q(c, T, horizon=860, warm=1.0, stars=0.0, night=0.0):
    """brighter dusk sky; night lerps to a lit blue night"""
    top = lerpc((0.16, 0.18, 0.30), (0.07, 0.09, 0.20), night)
    mid = lerpc(lerpc((0.20, 0.20, 0.30), (0.42, 0.24, 0.24), warm), (0.12, 0.14, 0.28), night)
    hor = lerpc(lerpc((0.30, 0.28, 0.34), (0.92, 0.55, 0.26), warm), (0.24, 0.24, 0.40), night)
    g = cairo.LinearGradient(0, 0, 0, horizon)
    g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(0.55, *mid); g.add_color_stop_rgb(1, *hor)
    c.set_source(g); c.paint()
    if stars > 0:
        from ming import _stars
        for (x, y, r, ph) in _stars:
            rgba(c, (0.95, 0.95, 1.0), stars * (0.4 + 0.35 * math.sin(T * 1.5 + ph))); c.arc(x, y, r, 0, 6.283); c.fill()
    g2 = cairo.LinearGradient(0, horizon, 0, H)
    g2.add_color_stop_rgb(0, 0.34, 0.28, 0.24); g2.add_color_stop_rgb(1, 0.16, 0.13, 0.11)
    c.set_source(g2); c.rectangle(0, horizon, W, H - horizon); c.fill()
    rgba(c, (0.62, 0.55, 0.48)); c.rectangle(0, horizon, W, 5); c.fill()


def bg_room(c, T, floor=900, lamp_x=1300, warmth=1.0):
    """palace interior: red lacquer wall with lattice windows, wood floor, warm lamp glow"""
    g = cairo.LinearGradient(0, 0, 0, floor)
    g.add_color_stop_rgb(0, 0.32, 0.12, 0.09); g.add_color_stop_rgb(1, 0.56, 0.22, 0.14)
    c.set_source(g); c.paint()
    for k in range(5):
        x = 140 + k * 380
        rgba(c, (0.26, 0.10, 0.07)); c.rectangle(x - 14, 0, 28, floor); c.fill()   # pillars
    for k in range(4):
        x0 = 210 + k * 380
        rgba(c, (0.96, 0.84, 0.58), 0.55); c.rectangle(x0, 180, 240, 380); c.fill()  # paper window glow
        rgba(c, (0.36, 0.14, 0.09)); c.set_line_width(6)
        for i in range(5): c.move_to(x0 + i * 60, 180); c.line_to(x0 + i * 60, 560)
        for j in range(7): c.move_to(x0, 180 + j * 63); c.line_to(x0 + 240, 180 + j * 63)
        c.stroke()
        c.set_line_width(10); c.rectangle(x0, 180, 240, 380); c.stroke()
    rgba(c, (0.88, 0.70, 0.28)); c.rectangle(0, 120, W, 14); c.fill()
    g2 = cairo.LinearGradient(0, floor, 0, H)
    g2.add_color_stop_rgb(0, 0.46, 0.30, 0.18); g2.add_color_stop_rgb(1, 0.24, 0.15, 0.09)
    c.set_source(g2); c.rectangle(0, floor, W, H - floor); c.fill()
    rgba(c, (0.70, 0.52, 0.30)); c.rectangle(0, floor, W, 5); c.fill()
    spot(c, lamp_x, floor - 300, 900, 0.9 * warmth)


def queue(c, a, x0=-16, y0=-244, L=120):
    rgba(c, (0.10, 0.08, 0.07), a); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y0); c.curve_to(x0 - 14, y0 + L * 0.3, x0 - 8, y0 + L * 0.7, x0 - 14, y0 + L); c.stroke()
    rgba(c, (0.75, 0.15, 0.10), a); c.set_line_width(6); c.move_to(x0 - 14, y0 + L); c.line_to(x0 - 14, y0 + L + 14); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)


def qhat(c, a, bead=(0.85, 0.15, 0.12), emp=False):
    """暖帽 at head center (2,-250)"""
    rgba(c, (0.12, 0.10, 0.09), a)
    c.move_to(-28, -262); c.line_to(32, -262); c.line_to(28, -282); c.line_to(-24, -282); c.close_path(); c.fill()
    rgba(c, (0.20, 0.16, 0.14), a); c.arc(2, -268, 20, math.pi, 2 * math.pi); c.fill()
    rgba(c, (0.86, 0.16, 0.12), a)
    c.move_to(-20, -270)
    for k in range(9):
        ang = math.pi + k * math.pi / 8
        c.line_to(2 + 24 * math.cos(ang), -272 + 22 * math.sin(ang))
    c.close_path(); c.fill()
    rgba(c, bead, a); c.arc(2, -298, 7 if not emp else 9, 0, 6.283); c.fill()
    if emp:
        rgba(c, (1, 0.95, 0.75), a); c.arc(2, -312, 6, 0, 6.283); c.fill()


def qperson(c, x, yf, s=1.0, kind='qoff', a=1.0, face=1, pose='stand', walk=None, prop=None, T=0):
    """Qing man: Song body (bare head) + 暖帽 + 辫子 + 补褂 / 龙纹"""
    if a <= 0: return
    col = QROBE.get(kind, (0.4, 0.35, 0.3))
    sperson(c, x, yf, s, 'bare' if kind != 'qkid' else 'bare', a, face, pose if pose != 'carry' else 'hold', 1.0, walk, col)
    c.save(); c.translate(x, yf); c.scale(s * face, s); c.translate(0, -110)
    if kind == 'qemp':
        rgba(c, (0.85, 0.20, 0.12), a); c.set_line_width(4)
        c.move_to(-26, -150); c.curve_to(-6, -170, 10, -130, 28, -150); c.stroke()  # dragon squiggle
        c.move_to(-36, -40); c.curve_to(-10, -60, 14, -20, 40, -40); c.stroke()
        for k in range(5):
            rgba(c, (0.25, 0.45, 0.80), a); c.rectangle(-50 + k * 20, 20, 16, 10); c.fill()   # sea-wave hem
    elif kind in ('qoff', 'qeunuch'):
        rgba(c, (0.10, 0.10, 0.16) if kind == 'qoff' else (0.14, 0.20, 0.36), a)
        c.move_to(-32, -208); c.line_to(32, -208); c.line_to(42, -40); c.line_to(-42, -40); c.close_path(); c.fill()  # 补褂
        rgba(c, (0.92, 0.80, 0.40), a); c.rectangle(-22, -178, 44, 44); c.fill()
        rgba(c, (0.85, 0.30, 0.20), a); c.arc(0, -156, 10, 0, 6.283); c.fill()
    if kind == 'qkid':
        rgba(c, (0.12, 0.10, 0.09), a); c.arc(2, -266, 20, math.pi, 2 * math.pi); c.fill()
        rgba(c, (0.86, 0.16, 0.12), a); c.arc(2, -288, 7, 0, 6.283); c.fill()
        queue(c, a, L=90)
    else:
        queue(c, a)
        qhat(c, a, (0.95, 0.82, 0.30) if kind == 'qemp' else ((0.30, 0.45, 0.85) if kind == 'qeunuch' else (0.85, 0.15, 0.12)), kind == 'qemp')
    c.restore()


def baby(c, x, y, s=1.0, a=1.0, col=(0.95, 0.78, 0.30), T=0, cry=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    if cry > 0: c.rotate(0.06 * math.sin(T * 18) * cry)
    rgba(c, col, a); c.save(); c.scale(46, 24); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    rgba(c, tuple(v * 0.75 for v in col), a); c.set_line_width(3)
    for k in (-18, 0, 18): c.move_to(k - 6, -20); c.line_to(k + 6, 20)
    c.stroke()
    rgba(c, (0.85, 0.20, 0.15), a); c.rectangle(-8, -24, 10, 48); c.fill()   # binding band
    rgba(c, SKIN2, a); c.arc(34, -6, 15, 0, 6.283); c.fill()
    rgba(c, col, a); c.arc(36, -12, 16, math.pi * 1.05, 1.95 * math.pi); c.fill()  # hood
    c.restore()


def qlady(c, x, yf, s=1.0, kind='qmaid', a=1.0, face=1, pose='stand', walk=None, prop=None, T=0, p=1.0, babycol=None):
    """Qing woman ~390px at s=1: straight 旗袍 w/ trim, 花盆底 shoes, 两把头 or braid"""
    if a <= 0: return
    rb, trim = QLADY.get(kind, QLADY['qmaid'])
    dk = tuple(v * 0.72 for v in rb)
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    kn = p if pose == 'kneel' else 0.0
    sw = math.sin(walk) * 8 if walk is not None else 0
    lift = 0
    if kind in ('qconsort', 'qempress', 'qconcub', 'mama', 'qgirl'):   # 花盆底
        lift = 16
        rgba(c, (0.95, 0.92, 0.86), a)
        for fx in (-8 + sw, 12 - sw):
            c.move_to(fx - 6, 0); c.line_to(fx + 6, 0); c.line_to(fx + 9, -lift); c.line_to(fx - 9, -lift); c.close_path(); c.fill()
    rgba(c, (0.12, 0.09, 0.08), a)
    for fx in (-8 + sw, 12 - sw):
        c.save(); c.translate(fx + 6, -lift - 4); c.scale(14, 6); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    c.translate(0, -lift + 70 * kn)
    # robe
    rgba(c, rb, a)
    c.move_to(-26, -220); c.line_to(26, -220); c.curve_to(36, -160, 38, -80, 40 + sw * 0.4, -8)
    c.line_to(-38 + sw * 0.4, -8); c.curve_to(-36, -80, -36, -160, -26, -220); c.close_path(); c.fill()
    rgba(c, trim, a); c.rectangle(-39 + sw * 0.4, -26, 80, 16); c.fill()                # hem trim
    c.set_line_width(7); c.move_to(-6, -218); c.curve_to(14, -206, 22, -196, 26, -176); c.stroke()  # 大襟 trim
    if kind == 'han':  # apron
        rgba(c, (0.86, 0.82, 0.72), a); c.rectangle(-30, -150, 62, 110); c.fill()
    # arms
    rgba(c, dk, a); c.set_line_width(19); c.set_line_cap(cairo.LINE_CAP_ROUND)
    hx, hy = 22, -104
    if pose in ('hold', 'carry'):
        c.move_to(14, -200); c.line_to(30, -156); c.line_to(58, -150); c.stroke(); hx, hy = 62, -150
        c.move_to(-6, -200); c.line_to(16, -140); c.line_to(48, -134); c.stroke()
    elif pose == 'reach':
        c.move_to(14, -200); c.line_to(52, -190); c.line_to(92, -196); c.stroke(); hx, hy = 96, -196
    elif pose == 'raise':
        c.move_to(14, -200); c.line_to(44, -240); c.line_to(66, -280); c.stroke(); hx, hy = 70, -284
    elif pose == 'cover':  # hand to face
        c.move_to(14, -200); c.line_to(40, -180); c.line_to(24, -246); c.stroke(); hx, hy = 24, -246
    else:
        c.move_to(14, -200); c.line_to(22, -150); c.line_to(22, -108); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    rgba(c, trim, a); c.arc(hx, hy, 7, 0, 6.283); c.fill()   # cuff
    # head
    rgba(c, SKIN2, a); c.rectangle(-6, -242, 12, 24); c.fill()
    c.arc(2, -258, 19, 0, 6.283); c.fill()
    c.move_to(19, -264); c.line_to(28, -252); c.line_to(19, -248); c.close_path(); c.fill()
    rgba(c, (0.12, 0.08, 0.06), 0.8 * a); c.arc(13, -261, 2.0, 0, 6.283); c.fill()
    rgba(c, HAT, a); c.arc(-2, -264, 19, math.pi * 0.95, 2.05 * math.pi); c.fill()
    if kind in ('qconsort', 'qempress', 'qconcub', 'mama', 'qgirl'):
        big = {'qempress': 1.25, 'qconsort': 1.15, 'qconcub': 1.0, 'mama': 0.8, 'qgirl': 0.75}[kind]
        rgba(c, HAT, a); c.arc(-2, -272, 17, math.pi, 2 * math.pi); c.fill()
        c.save(); c.translate(-2, -282); c.scale(big, big)
        rgba(c, (0.08, 0.07, 0.07), a); c.move_to(-46, 0); c.line_to(46, 0); c.line_to(40, -26); c.line_to(-40, -26); c.close_path(); c.fill()
        if kind != 'mama':
            for (fx, fc) in ((-30, (0.95, 0.40, 0.50)), (-12, (0.98, 0.90, 0.60)), (14, (0.95, 0.40, 0.50)), (32, (0.65, 0.80, 0.95))):
                rgba(c, fc, a); c.arc(fx, -13, 7, 0, 6.283); c.fill()
            rgba(c, (0.95, 0.30, 0.25), a); c.set_line_width(3); c.move_to(40, -6); c.line_to(48, 30); c.stroke()   # tassel
        c.restore()
        rgba(c, HAT, a); c.save(); c.translate(-22, -244); c.scale(14, 10); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()  # 燕尾
    elif kind == 'han':
        rgba(c, HAT, a); c.arc(-20, -258, 13, 0, 6.283); c.fill()
        rgba(c, (0.85, 0.80, 0.70), a); c.rectangle(-30, -262, 22, 4); c.fill()
    else:  # maid / baomu: long single braid
        rgba(c, HAT, a); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(-16, -252); c.curve_to(-26, -200, -18, -160, -24, -110); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
        rgba(c, (0.85, 0.20, 0.15), a); c.rectangle(-30, -112, 12, 10); c.fill()
    if pose in ('hold', 'carry') and babycol is not None:
        baby(c, 46, -150, 0.95, a, babycol, T)
    c.restore()


def lying(c, x, yf, s=1.0, a=1.0, T=0, reach=0.0):
    """mother lying in bed: pillow, head, quilt; optional arm reaching up"""
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, (0.95, 0.88, 0.70), a); rrect(c, -260, -210, 90, 44, 16); c.fill()   # pillow
    rgba(c, SKIN2, a); c.arc(-200, -214, 22, 0, 6.283); c.fill()
    rgba(c, HAT, a); c.arc(-212, -220, 22, math.pi * 0.6, 1.7 * math.pi); c.fill()
    rgba(c, (0.88, 0.36, 0.40), a)
    c.move_to(-180, -232); c.curve_to(-60, -250, 120, -236, 250, -210); c.line_to(250, -170); c.line_to(-180, -170); c.close_path(); c.fill()
    rgba(c, (0.98, 0.84, 0.44), a); c.set_line_width(4)
    for k in range(5): c.move_to(-140 + k * 80, -236); c.line_to(-150 + k * 80, -172)
    c.stroke()
    if reach > 0:
        rgba(c, (0.88, 0.36, 0.40), a); c.set_line_width(16); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(-170, -228); c.line_to(-170 + 120 * reach, -260 - 90 * reach); c.stroke()
        rgba(c, SKIN2, a); c.arc(-170 + 128 * reach, -266 - 96 * reach, 9, 0, 6.283); c.fill()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.restore()


def bigtag(c, s_, x, y, size, t, col=GOLDT, a=1.0):
    """big floating outlined label"""
    text2(c, s_, x, y, size, t, col, a, 'c', 0.04, 0.25, FONT_X)


def ingots(c, x, y, n, a=1.0, s=0.8):
    for k in range(n):
        ingot(c, x + (k % 4) * 70 * s, y - (k // 4) * 40 * s, s, a)


def calendar_dots(c, x, y, cols, rows, n_on, a=1.0, r=11, gap=34, col=GOLDL):
    for i in range(cols * rows):
        cx, cy = x + (i % cols) * gap, y + (i // cols) * gap
        on = i < n_on
        rgba(c, col if on else (0.4, 0.35, 0.3), a * (1 if on else 0.5))
        c.arc(cx, cy, r if on else r * 0.6, 0, 6.283); c.fill()

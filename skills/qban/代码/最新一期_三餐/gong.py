"""Ming Forbidden City props: yellow-roof halls, red palace walls, gates, palace women, bells, nested plan."""
from ming import *

YEL = (0.95, 0.72, 0.20)
YELD = (0.66, 0.45, 0.12)
PRED = (0.64, 0.14, 0.10)
PREDD = (0.42, 0.09, 0.07)
MARB = (0.80, 0.78, 0.73)


def bg_dusk(c, T, horizon=820, warm=1.0, stars=0.0):
    g = cairo.LinearGradient(0, 0, 0, horizon)
    g.add_color_stop_rgb(0, 0.03, 0.035, 0.07)
    g.add_color_stop_rgb(0.55, *lerpc((0.06, 0.06, 0.10), (0.16, 0.09, 0.11), warm))
    g.add_color_stop_rgb(1, *lerpc((0.10, 0.09, 0.12), (0.62, 0.30, 0.12), warm))
    c.set_source(g); c.paint()
    if stars > 0:
        from ming import _stars
        for (x, y, r, ph) in _stars:
            if x < 1100 and y < 560: continue
            rgba(c, (0.9, 0.9, 1.0), stars * (0.35 + 0.35 * math.sin(T * 1.5 + ph))); c.arc(x, y, r, 0, 6.283); c.fill()
    rgba(c, (0.07, 0.055, 0.05)); c.rectangle(0, horizon, W, H - horizon); c.fill()
    rgba(c, (0.16, 0.13, 0.11)); c.rectangle(0, horizon, W, 4); c.fill()


def yroof(c, w, y, h, a=1.0, eave=60, col=YEL):
    """hip roof spanning [-w/2-eave, w/2+eave] from y (eave line) up h"""
    rw = w / 2 + eave
    rgba(c, col, a)
    c.move_to(-rw, y); c.curve_to(-rw + 40, y - 14, -w / 2, y - h * 0.35, -w / 2 + h * 0.6, y - h)
    c.line_to(w / 2 - h * 0.6, y - h); c.curve_to(w / 2, y - h * 0.35, rw - 40, y - 14, rw, y)
    c.line_to(rw - 18, y + 14); c.line_to(-rw + 18, y + 14); c.close_path(); c.fill()
    rgba(c, YELD, a); c.set_line_width(2)
    n = int(rw / 22)
    for k in range(-n, n + 1):
        xx = k * 22
        c.move_to(xx, y + 10); c.line_to(xx * (w / 2 - h * 0.6) / rw, y - h + 4)
    c.stroke()
    rgba(c, (1.0, 0.88, 0.5), 0.8 * a); c.rectangle(-rw + 18, y + 8, 2 * rw - 36, 4); c.fill()
    rgba(c, YELD, a); c.rectangle(-w / 2 + h * 0.6 - 10, y - h - 10, w - h * 1.2 + 20, 12); c.fill()
    for sg in (-1, 1):
        c.save(); c.translate(sg * (w / 2 - h * 0.6 + 4), y - h - 8); c.scale(sg, 1)
        c.move_to(0, 0); c.curve_to(8, -24, 26, -36, 14, -50); c.curve_to(30, -40, 30, -16, 20, 0); c.close_path(); c.fill()
        c.restore()


def mhall(c, x, yf, s=1.0, a=1.0, glow=0.0, n=5, double=True, plaque=None, base=True):
    """Ming palace hall: marble terrace, red columns, lattice doors, yellow glazed double-eave roof"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    w = n * 110
    if base:
        for k, (ww, hh) in enumerate(((w + 260, 40), (w + 190, 36), (w + 130, 34))):
            yy = -k * 36
            rgba(c, MARB if k % 2 == 0 else (0.70, 0.68, 0.64), a); c.rectangle(-ww / 2, yy - hh, ww, hh); c.fill()
            rgba(c, (0.55, 0.53, 0.50), a); c.set_line_width(2)
            for j in range(int(ww / 26)):
                c.move_to(-ww / 2 + j * 26 + 13, yy - hh); c.line_to(-ww / 2 + j * 26 + 13, yy - hh - 12)
            c.stroke(); c.rectangle(-ww / 2, yy - hh - 12, ww, 3); c.fill()
        c.translate(0, -108)
    rgba(c, PREDD, a); c.rectangle(-w / 2, -300, w, 300); c.fill()
    for k in range(n):
        xx = -w / 2 + k * 110 + 16
        gl = glow * (0.65 + 0.35 * math.sin(k * 1.7 + 1))
        rgba(c, lerpc((0.48, 0.14, 0.10), (1.0, 0.80, 0.45), gl), a); c.rectangle(xx, -270, 78, 250); c.fill()
        rgba(c, lerpc((0.30, 0.07, 0.05), (0.75, 0.42, 0.18), gl), a); c.set_line_width(3)
        for j in range(1, 4):
            c.move_to(xx + j * 19.5, -270); c.line_to(xx + j * 19.5, -120)
        for j in range(1, 8):
            c.move_to(xx, -270 + j * 21); c.line_to(xx + 78, -270 + j * 21)
        c.stroke()
    for k in range(n + 1):
        rgba(c, PRED, a); c.rectangle(-w / 2 - 9 + k * 110, -312, 18, 312); c.fill()
    rgba(c, (0.16, 0.36, 0.40), a); c.rectangle(-w / 2 - 20, -336, w + 40, 26); c.fill()
    rgba(c, GOLD, 0.9 * a); c.rectangle(-w / 2 - 20, -323, w + 40, 3); c.fill()
    for k in range(n * 2 + 1):
        bx = -w / 2 - 10 + k * 55
        rgba(c, (0.20, 0.45, 0.42), a); c.rectangle(bx - 11, -356, 22, 20); c.fill()
    if double:
        yroof(c, w + 10, -356, 70, a, 70)
        rgba(c, PREDD, a); c.rectangle(-w / 2 + 50, -440, w - 100, 30); c.fill()
        yroof(c, w - 60, -436, 120, a, 70)
        top = -556
    else:
        yroof(c, w + 10, -356, 150, a, 80)
        top = -506
    if plaque:
        rgba(c, (0.12, 0.20, 0.42), a); rrect(c, -70, -428 if double else -400, 140, 52, 6); c.fill()
        rgba(c, GOLD, a); c.set_line_width(3); rrect(c, -70, -428 if double else -400, 140, 52, 6); c.stroke()
        text2(c, plaque, 0, (-428 if double else -400) + 38, 30, 99, (1.0, 0.86, 0.5), a, 'c', fam=FONT_B)
    c.restore()


def redwall(c, x0, x1, yb, h=220, a=1.0, shade=1.0):
    if a <= 0: return
    rgba(c, lerpc((0.28, 0.07, 0.05), PRED, shade), a); c.rectangle(x0, yb - h, x1 - x0, h); c.fill()
    rgba(c, (0.45, 0.43, 0.40), a); c.rectangle(x0, yb - 26, x1 - x0, 26); c.fill()
    rgba(c, YELD, a); c.rectangle(x0 - 10, yb - h - 10, x1 - x0 + 20, 16); c.fill()
    rgba(c, YEL, a)
    c.move_to(x0 - 18, yb - h - 4); c.line_to(x0 + 6, yb - h - 30); c.line_to(x1 - 6, yb - h - 30); c.line_to(x1 + 18, yb - h - 4); c.close_path(); c.fill()
    rgba(c, YELD, 0.8 * a); c.set_line_width(2)
    for k in range(int((x1 - x0) / 18)):
        xx = x0 + k * 18
        c.move_to(xx, yb - h - 6); c.line_to(xx + 4, yb - h - 28)
    c.stroke()


def pgate(c, x, yb, s=1.0, a=1.0, closed=1.0, lit=0.5, plaque=None, T=0, lock=0.0):
    """palace gate in a red wall: yellow roof, two studded red doors (closed 0..1)"""
    if a <= 0: return
    c.save(); c.translate(x, yb); c.scale(s, s)
    rgba(c, PRED, a); c.rectangle(-220, -360, 440, 360); c.fill()
    rgba(c, (0.45, 0.43, 0.40), a); c.rectangle(-230, -30, 460, 30); c.fill()
    # opening
    rgba(c, (0.05, 0.03, 0.02), a); c.rectangle(-110, -280, 220, 250); c.fill()
    if lit > 0:
        spot(c, 0, -120, 260, lit * (1 - closed) * a)
        rgba(c, (1.0, 0.75, 0.40), 0.45 * lit * (1 - closed) * a); c.rectangle(-110, -280, 220, 250); c.fill()
    lw = 110 * closed
    for sg in (-1, 1):
        x0 = sg * 110 - (sg * lw if sg > 0 else -lw * 0) if False else None
        if sg < 0: dx0, dx1 = -110, -110 + lw
        else: dx0, dx1 = 110 - lw, 110
        if lw > 1:
            rgba(c, (0.70, 0.15, 0.11), a); c.rectangle(dx0, -280, dx1 - dx0, 250); c.fill()
            rgba(c, (0.40, 0.08, 0.06), a); c.set_line_width(3); c.rectangle(dx0, -280, dx1 - dx0, 250); c.stroke()
            for r in range(7):
                for k in range(5):
                    xx = dx0 + (k + 0.5) * (dx1 - dx0) / 5
                    rgba(c, (1.0, 0.82, 0.38), a); c.arc(xx, -262 + r * 34, 5.5 * (dx1 - dx0) / 110 + 0.5, 0, 6.283); c.fill()
    if lock > 0 and closed > 0.95:
        c.save(); c.translate(0, -160); c.scale(1 + 0.4 * (1 - eout(lock)), 1 + 0.4 * (1 - eout(lock)))
        rgba(c, (0.85, 0.70, 0.35), a * lock); c.rectangle(-30, -12, 60, 24); c.fill()
        rgba(c, (0.55, 0.42, 0.18), a * lock); c.set_line_width(6); c.arc(0, -12, 18, math.pi, 0); c.stroke()
        c.restore()
    yroof(c, 470, -360, 120, a, 70)
    if plaque:
        rgba(c, (0.12, 0.20, 0.42), a); rrect(c, -80, -350, 160, 54, 6); c.fill()
        rgba(c, GOLD, a); c.set_line_width(3); rrect(c, -80, -350, 160, 54, 6); c.stroke()
        text2(c, plaque, 0, -311, 32, 99, (1.0, 0.86, 0.5), a, 'c', fam=FONT_B)
    c.restore()


LADY = {'maid': ((0.25, 0.48, 0.46), (0.78, 0.70, 0.54)), 'maid2': ((0.55, 0.40, 0.62), (0.80, 0.72, 0.58)),
        'consort': ((0.78, 0.26, 0.24), (0.36, 0.24, 0.30)), 'empress': ((0.82, 0.18, 0.14), (0.20, 0.25, 0.45)),
        'nurse': ((0.46, 0.38, 0.30), (0.34, 0.30, 0.26)), 'girl': ((0.85, 0.55, 0.45), (0.80, 0.72, 0.58))}


def lady(c, x, yf, s=1.0, kind='maid', a=1.0, face=1, pose='stand', walk=None, prop=None, T=0, p=1.0):
    """palace woman ~380px at s=1: cross-collar jacket, long flared skirt, bun / 翟冠 / 凤冠"""
    if a <= 0: return
    jk, sk = LADY.get(kind, LADY['maid'])
    dj = tuple(v * 0.72 for v in jk); ds = tuple(v * 0.75 for v in sk)
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    kn = p if pose == 'kneel' else 0.0
    if pose == 'run': c.rotate(0.12)
    sw = math.sin(walk) * 10 if walk is not None else 0
    # feet
    rgba(c, (0.12, 0.09, 0.08), a)
    for fx in (-10 + sw, 10 - sw):
        c.save(); c.translate(fx + 10, -4); c.scale(14, 6); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    c.translate(0, 70 * kn)
    # skirt
    rgba(c, sk, a)
    c.move_to(-26, -160); c.line_to(26, -160); c.curve_to(36, -90, 50 + sw * 0.5, -40, 58 + sw, -6)
    c.line_to(-52 + sw, -6); c.curve_to(-46, -40, -36, -90, -26, -160); c.close_path(); c.fill()
    rgba(c, ds, a); c.set_line_width(2.5)
    for k in (-1, 0, 1):
        c.move_to(k * 10, -150); c.line_to(k * 24 + sw * 0.6, -10)
    c.stroke()
    rgba(c, ds, a); c.rectangle(-52 + sw, -20, 110, 14); c.fill()
    # jacket
    rgba(c, jk, a)
    c.move_to(-26, -218); c.line_to(26, -218); c.curve_to(34, -180, 40, -140, 40, -112)
    c.line_to(-40, -112); c.curve_to(-40, -140, -34, -180, -26, -218); c.close_path(); c.fill()
    rgba(c, (0.95, 0.90, 0.80), a); c.set_line_width(5)
    c.move_to(-14, -218); c.line_to(16, -150); c.stroke()  # cross collar
    if kind == 'empress':
        rgba(c, GOLD, a); c.set_line_width(9); c.move_to(4, -214); c.line_to(16, -110); c.line_to(18, -40); c.stroke()  # 霞帔
    rgba(c, dj, a); c.rectangle(-36, -150, 72, 8); c.fill()
    # arm
    rgba(c, dj, a); c.set_line_width(19); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if pose in ('hold', 'lamp', 'bell'):
        c.move_to(14, -200); c.line_to(36, -150); c.line_to(66, -150); c.stroke(); hx, hy = 72, -150
    elif pose == 'raise':
        c.move_to(14, -200); c.line_to(48, -240); c.line_to(74, -282); c.stroke(); hx, hy = 78, -288
    elif pose == 'run':
        c.move_to(14, -200); c.line_to(52, -176); c.line_to(76, -196); c.stroke(); hx, hy = 80, -198
        c.move_to(-10, -200); c.line_to(-40, -170); c.line_to(-62, -150); c.stroke()
    elif pose == 'pull':
        c.move_to(14, -200); c.line_to(50, -170); c.line_to(80, -160); c.stroke(); hx, hy = 84, -160
    else:
        c.move_to(14, -200); c.line_to(24, -150); c.line_to(22, -108); c.stroke(); hx, hy = 22, -104
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    rgba(c, dj, a); c.move_to(hx - 26, hy - 6); c.line_to(hx + 2, hy - 2); c.line_to(hx - 4, hy + 30); c.line_to(hx - 34, hy + 20); c.close_path(); c.fill()
    # head
    rgba(c, SKIN2, a); c.rectangle(-6, -240, 12, 24); c.fill()
    c.arc(2, -256, 19, 0, 6.283); c.fill()
    c.move_to(19, -262); c.line_to(28, -250); c.line_to(19, -246); c.close_path(); c.fill()
    rgba(c, (0.12, 0.08, 0.06), 0.8 * a); c.arc(13, -259, 2.0, 0, 6.283); c.fill()
    rgba(c, HAT, a)
    c.arc(-2, -262, 19, math.pi * 0.95, 2.05 * math.pi); c.fill()
    c.arc(-20, -258, 11, 0, 6.283); c.fill()
    if kind in ('maid', 'maid2', 'girl'):
        c.arc(-6, -284, 11, 0, 6.283); c.fill()
        rgba(c, GOLD, a); c.rectangle(-26, -287, 34, 3); c.fill()
    elif kind == 'nurse':
        rgba(c, (0.30, 0.26, 0.22), a); c.arc(-2, -264, 22, math.pi * 0.9, 2.1 * math.pi); c.fill()
        c.move_to(-22, -262); c.line_to(-34, -230); c.line_to(-16, -244); c.close_path(); c.fill()
    else:
        big = 1.35 if kind == 'empress' else 1.0
        rgba(c, (0.90, 0.68, 0.25), a)
        c.move_to(-26 * big, -272); c.curve_to(-26 * big, -312 * (1 + (big - 1) * 0.3), 24 * big, -312 * (1 + (big - 1) * 0.3), 24 * big, -272); c.close_path(); c.fill()
        rgba(c, (0.15, 0.30, 0.55), a); c.rectangle(-26 * big, -276, 50 * big, 7); c.fill()
        for k in range(5):
            rgba(c, (1, 0.95, 0.85), a); c.arc(-20 * big + k * 10 * big, -292, 3, 0, 6.283); c.fill()
        rgba(c, REDL, a); c.arc(0, -302 - (big - 1) * 30, 5, 0, 6.283); c.fill()
        if kind == 'empress':
            rgba(c, (0.90, 0.68, 0.25), a); c.set_line_width(5)
            for sg in (-1, 1):
                c.move_to(sg * 20, -276); c.curve_to(sg * 50, -270, sg * 60, -252, sg * 64, -236); c.stroke()
                rgba(c, (1, 0.95, 0.85), a); c.arc(sg * 64, -232, 4, 0, 6.283); c.fill(); rgba(c, (0.90, 0.68, 0.25), a)
    # props in hand
    if prop == 'bell':
        handbell(c, hx + 14, hy + 4, 0.9, a, T)
    elif prop == 'lamp':
        rgba(c, (0.3, 0.2, 0.1), a); c.set_line_width(4); c.move_to(hx, hy); c.line_to(hx + 40, hy - 30); c.line_to(hx + 40, hy + 10); c.stroke()
        lantern(c, hx + 40, hy + 50, 0.7, a, T)
    elif prop == 'bowl':
        bowl(c, hx + 14, hy - 4, 0.7, a, T)
    c.restore()


def handbell(c, x, y, s=1.0, a=1.0, T=0, ring=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(0.35 * math.sin(T * 9) * ring); c.scale(s, s)
    rgba(c, (0.35, 0.22, 0.12), a); c.rectangle(-4, -30, 8, 30); c.fill()
    g = cairo.LinearGradient(-26, 0, 26, 0)
    g.add_color_stop_rgba(0, 0.70, 0.52, 0.20, a); g.add_color_stop_rgba(0.5, 1.0, 0.86, 0.45, a); g.add_color_stop_rgba(1, 0.62, 0.44, 0.16, a)
    c.set_source(g); c.move_to(-14, 0); c.curve_to(-18, 20, -26, 34, -28, 46); c.line_to(28, 46); c.curve_to(26, 34, 18, 20, 14, 0); c.close_path(); c.fill()
    rgba(c, (0.45, 0.32, 0.12), a); c.arc(0, 50, 6, 0, 6.283); c.fill()
    c.restore()
    if ring > 0:
        ph = (T * 2.2) % 1.0
        for k in range(2):
            pp = (ph + k * 0.5) % 1.0
            rgba(c, GOLDL, (1 - pp) * 0.6 * a * ring); c.set_line_width(3)
            c.arc(x, y + 20 * s, 40 * s + pp * 70 * s, -2.4, -0.7); c.stroke()


def bowl(c, x, y, s=1.0, a=1.0, T=0, steam=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, (0.90, 0.88, 0.82), a); c.move_to(-40, 0); c.curve_to(-36, 34, 36, 34, 40, 0); c.close_path(); c.fill()
    rgba(c, (0.25, 0.35, 0.60), a); c.set_line_width(3); c.move_to(-36, 12); c.curve_to(-20, 20, 20, 20, 36, 12); c.stroke()
    rgba(c, (0.35, 0.20, 0.10), a); c.save(); c.scale(38, 7); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    if steam > 0:
        rgba(c, (1, 1, 1), 0.35 * a * steam); c.set_line_width(3)
        for k in (-14, 0, 14):
            c.move_to(k, -8)
            for j in range(1, 6):
                c.line_to(k + 6 * math.sin(T * 3 + j + k), -8 - j * 12)
            c.stroke()
    c.restore()


def bed(c, x, yf, s=1.0, a=1.0, curtain=0.6):
    """架子床 canopy bed"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, (0.36, 0.16, 0.10), a)
    c.rectangle(-300, -150, 600, 40); c.fill()
    for xx in (-300, 284): c.rectangle(xx, -560, 16, 560); c.fill()
    c.rectangle(-310, -580, 620, 30); c.fill()
    rgba(c, (0.62, 0.30, 0.16), a); c.rectangle(-290, -112, 580, 112); c.fill()
    rgba(c, (0.80, 0.70, 0.45), a); c.rectangle(-280, -175, 560, 28); c.fill()  # bedding
    rgba(c, (0.88, 0.62, 0.30), 0.55 * a)
    cw = 290 * curtain
    for sg in (-1, 1):
        x0 = sg * 284
        c.move_to(x0, -550); c.line_to(x0 - sg * cw, -550); c.curve_to(x0 - sg * cw * 0.7, -300, x0 - sg * cw * 0.9, -260, x0 - sg * cw * 0.6, -150)
        c.line_to(x0, -150); c.close_path(); c.fill()
    c.restore()


def stamp(c, ch, x, y, s=1.0, a=1.0):
    seal(c, ch, x, y, s, a)


def dial(c, x, y, r, a=1.0, hi=None, hand=None, prog=1.0):
    """十二时辰 dial, hi = branch index to highlight (申=8, 酉=9), angle 0 = 子 at top"""
    if a <= 0: return
    br = "子丑寅卯辰巳午未申酉戌亥"
    rgba(c, (0.08, 0.07, 0.07), 0.9 * a); c.arc(x, y, r, 0, 6.283); c.fill()
    rgba(c, GOLD, a); c.set_line_width(3); c.arc(x, y, r, 0, 6.283); c.stroke()
    for k, ch in enumerate(br):
        ang = -math.pi / 2 + k * math.pi / 6
        if hi is not None and k in (hi if isinstance(hi, tuple) else (hi,)):
            rgba(c, LACQ, 0.85 * a * prog); c.move_to(x, y); c.arc(x, y, r - 4, ang - math.pi / 12, ang + math.pi / 12); c.close_path(); c.fill()
        text2(c, ch, x + (r - 36) * math.cos(ang), y + (r - 36) * math.sin(ang) + 12, 32, 99, TXT if (hi is None or k not in (hi if isinstance(hi, tuple) else (hi,))) else (1, 0.9, 0.6), a, 'c', fam=FONT_B)
    if hand is not None:
        ang = -math.pi / 2 + hand * math.pi / 6
        rgba(c, GOLDL, a); c.set_line_width(6); c.move_to(x, y); c.line_to(x + (r - 70) * math.cos(ang), y + (r - 70) * math.sin(ang)); c.stroke()
        c.arc(x, y, 9, 0, 6.283); c.fill()


def roundbadge(c, x, y, txt, a=1.0, col=LACQ, r=34, size=34):
    if a <= 0: return
    rgba(c, col, a); c.arc(x, y, r, 0, 6.283); c.fill()
    text2(c, txt, x, y + size * 0.36, size, 99, TXT, a, 'c', fam=FONT_B)


def stick(c, x0, y0, x1, y1, a=1.0):
    if a <= 0: return
    rgba(c, (0.50, 0.30, 0.16), a); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y0); c.line_to(x1, y1); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)


def plan(c, x, y, s=1.0, a=1.0, prog=(1, 1, 1, 1), lab=1.0, hi=None):
    """nested schematic: 京城 > 皇城 > 紫禁城 > 后宫(内廷). prog per ring 0..1"""
    rings = [((-560, -400, 1120, 800), '京城', (0.55, 0.52, 0.48)), ((-420, -330, 840, 640), '皇城', (0.80, 0.42, 0.30)),
             ((-210, -260, 420, 500), '紫禁城', (0.92, 0.30, 0.22)), ((-170, -200, 340, 190), '后宫（内廷）', (1.0, 0.80, 0.42))]
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, ((rx, ry, rw, rh), name, col) in enumerate(rings):
        p = prog[k]
        if p <= 0: continue
        lw = 5 if k < 3 else 4
        per = 2 * (rw + rh); L = per * ease(p)
        pts = [(rx, ry), (rx + rw, ry), (rx + rw, ry + rh), (rx, ry + rh), (rx, ry)]
        hh = (hi == k)
        if hh:
            rgba(c, col, 0.16 * a); c.rectangle(rx, ry, rw, rh); c.fill()
        rgba(c, col, a); c.set_line_width(lw + (3 if hh else 0))
        c.move_to(*pts[0]); acc = 0
        for i in range(4):
            (ax, ay), (bx, by) = pts[i], pts[i + 1]
            d = abs(bx - ax) + abs(by - ay)
            if acc + d <= L:
                c.line_to(bx, by); acc += d
            else:
                u = (L - acc) / d; c.line_to(ax + (bx - ax) * u, ay + (by - ay) * u); break
        c.stroke()
        if lab > 0:
            fs = 44 if k < 3 else 40
            text2(c, name, rx + 16, ry + 54, fs, 99, col, a * lab * fin(p, 0.6), 'l', fam=FONT_X)
    c.restore()

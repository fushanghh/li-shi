import math, random
import cairocffi as cairo

W, H, FPS = 1920, 1080, 30
GY = 900
SERIF = "Noto Serif CJK SC"
SANS = "Noto Sans CJK SC"

WHITE = (0.97, 0.95, 0.90)
CREAM = (0.93, 0.87, 0.74)
GOLD = (0.86, 0.66, 0.30)
GOLDL = (1.0, 0.83, 0.45)
GOLDD = (0.60, 0.44, 0.18)
RED = (0.72, 0.17, 0.13)
REDL = (0.90, 0.28, 0.20)
GREEN = (0.26, 0.45, 0.28)
GREENL = (0.45, 0.66, 0.35)
PURPLE = (0.42, 0.24, 0.48)
SKIN = (0.95, 0.82, 0.68)
ROBE = (0.84, 0.75, 0.56)
BLUEG = (0.32, 0.40, 0.52)
NAVY = (0.10, 0.14, 0.28)
GREY = (0.62, 0.58, 0.52)
DARK = (0.08, 0.06, 0.05)
INKC = (0.10, 0.08, 0.07)
BROWN = (0.45, 0.30, 0.18)


def clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)


def seg(t, a, b):
    if b <= a:
        return 1.0 if t >= a else 0.0
    return clamp((t - a) / (b - a))


def ease(x):
    x = clamp(x); return x * x * (3 - 2 * x)


def eout(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def back(x):
    x = clamp(x); s = 1.7; x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def lerp(a, b, u):
    return a + (b - a) * u


def lerpc(a, b, u):
    return tuple(lerp(x, y, u) for x, y in zip(a, b))


def pop(t, t0, d=0.5):
    return back(seg(t, t0, t0 + d))


def fin(t, t0, d=0.4):
    return eout(seg(t, t0, t0 + d))


def rgba(c, col, a=1.0):
    c.set_source_rgba(col[0], col[1], col[2], a)


# ------------------------------------------------------------- text
def font(c, size, bold=True, fam=SERIF):
    c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def parse(s, base):
    """[gold underlined]  {red underlined}  <gold plain>"""
    out = []; col = base; ul = False
    for ch in s:
        if ch == '[': col, ul = GOLDL, True; continue
        if ch == '{': col, ul = REDL, True; continue
        if ch == '<': col, ul = GOLDL, False; continue
        if ch in ']}>': col, ul = base, False; continue
        out.append((ch, col, ul))
    return out


def text_w(c, s, size, bold=True, fam=SERIF):
    font(c, size, bold, fam)
    return sum(c.text_extents(ch)[4] for ch, _, _ in parse(s, WHITE))


def rich(c, s, x, y, size, t=99, base=WHITE, a=1.0, align='l', stagger=0.03, fade=0.3, shadow=True,
         fam=SERIF, bold=True, maxw=None):
    if maxw:
        w = text_w(c, s, size, bold, fam)
        if w > maxw:
            size = size * maxw / w
    chars = parse(s, base)
    font(c, size, bold, fam)
    advs = [c.text_extents(ch)[4] for ch, _, _ in chars]
    tot = sum(advs)
    x0 = x if align == 'l' else (x - tot / 2 if align == 'c' else x - tot)
    cx = x0
    runs = []
    for i, ((ch, col, ul), adv) in enumerate(zip(chars, advs)):
        p = eout(seg(t - i * stagger, 0, fade))
        aa = p * a
        if aa > 0.003 and ch != ' ':
            dy = (1 - p) * size * 0.25
            if shadow:
                c.set_source_rgba(0, 0, 0, 0.55 * aa); c.move_to(cx + size * 0.04, y + dy + size * 0.05); c.show_text(ch)
            rgba(c, col, aa); c.move_to(cx, y + dy); c.show_text(ch)
        if ul:
            runs.append((cx, adv, col, p * a))
        cx += adv
    c.new_path()
    # underlines
    for (ux, adv, col, aa) in runs:
        if aa <= 0.01:
            continue
        rgba(c, col, aa)
        c.rectangle(ux, y + size * 0.16, adv * aa if aa < 1 else adv, max(3, size * 0.06)); c.fill()
    return tot, size


def label(c, s, x, y, size=34, col=GOLDL, a=1.0, t=99, bold=True):
    if a <= 0:
        return
    rich(c, s, x, y, size, t, col, a, 'c', stagger=0.0, fade=0.01)


def source(c, s, a=1.0):
    if a <= 0:
        return
    rich(c, s, 960, 1052, 26, 99, (0.62, 0.57, 0.50), a, 'c', 0, 0.01, shadow=False, fam=SANS, bold=False)


def bignum(c, s, x, y, size, t, t0, col=GOLDL, align='c'):
    p = pop(t, t0, 0.55)
    if p <= 0:
        return
    c.save(); c.translate(x, y); c.scale(p, p)
    rich(c, s, 0, 0, size, 99, col, clamp(p * 1.5), align, 0, 0.01)
    c.restore()


def caption(c, t, lines, x=110, y0=150, size=58, gap=1.52):
    """lines: list of (t0, text) or (t0, text, size, color)"""
    y = y0
    for ln in lines:
        t0, s = ln[0], ln[1]
        sz = ln[2] if len(ln) > 2 and ln[2] else size
        col = ln[3] if len(ln) > 3 else WHITE
        if t >= t0:
            rich(c, s, x, y, sz, t - t0, col, 1.0, 'l', 0.035, 0.3, maxw=1720)
        y += sz * gap


# ------------------------------------------------------------- background
_dust = [(random.Random(k).uniform(0, W), random.Random(k + 999).uniform(0, H),
          random.Random(k + 77).uniform(1.2, 3.4), random.Random(k + 55).uniform(0, 6.28)) for k in range(80)]


def bg(c, t, cx=960, cy=560, red=0.0, rays=1.0, dunes=True, ground=True, T=0):
    base_c = lerpc((0.20, 0.145, 0.095), (0.30, 0.09, 0.06), red)
    edge_c = lerpc((0.055, 0.04, 0.03), (0.09, 0.025, 0.02), red)
    pat = cairo.RadialGradient(cx, cy, 50, cx, cy, 1300)
    pat.add_color_stop_rgb(0, *base_c); pat.add_color_stop_rgb(1, *edge_c)
    c.set_source(pat); c.paint()
    if rays > 0:
        rc = lerpc(GOLD, REDL, red)
        n = 28
        rot = T * 0.025
        pat = cairo.RadialGradient(cx, cy, 0, cx, cy, 1500)
        pat.add_color_stop_rgba(0, rc[0], rc[1], rc[2], 0.30 * rays)
        pat.add_color_stop_rgba(0.45, rc[0], rc[1], rc[2], 0.10 * rays)
        pat.add_color_stop_rgba(1, rc[0], rc[1], rc[2], 0.0)
        for k in range(n):
            a0 = rot + k * 2 * math.pi / n
            a1 = a0 + math.pi / n * 0.9
            c.move_to(cx, cy)
            c.line_to(cx + 2200 * math.cos(a0), cy + 2200 * math.sin(a0))
            c.line_to(cx + 2200 * math.cos(a1), cy + 2200 * math.sin(a1))
            c.close_path()
        c.set_source(pat); c.fill()
        # center glow
        pat = cairo.RadialGradient(cx, cy, 0, cx, cy, 520)
        pat.add_color_stop_rgba(0, rc[0], rc[1], rc[2], 0.22 * rays)
        pat.add_color_stop_rgba(1, rc[0], rc[1], rc[2], 0)
        c.set_source(pat); c.paint()
    if dunes:
        for layer, (yb, amp, col, sp) in enumerate(((700, 50, (0.17, 0.12, 0.08), 0.9), (790, 40, (0.13, 0.09, 0.06), 1.4))):
            col = lerpc(col, (0.20, 0.07, 0.05), red)
            c.move_to(0, GY)
            for x in range(0, W + 41, 40):
                y = yb + amp * math.sin(x * 0.004 * sp + layer * 2) + amp * 0.5 * math.sin(x * 0.011 + layer)
                c.line_to(x, y)
            c.line_to(W, GY); c.close_path()
            rgba(c, col, 0.85); c.fill()
    if ground:
        rgba(c, lerpc((0.06, 0.045, 0.035), (0.10, 0.03, 0.02), red)); c.rectangle(0, GY, W, H - GY); c.fill()
        pat = cairo.LinearGradient(0, 0, W, 0)
        for u, al in ((0, 0.0), (0.2, 0.75), (0.8, 0.75), (1, 0.0)):
            pat.add_color_stop_rgba(u, GOLD[0], GOLD[1], GOLD[2], al)
        c.set_source(pat); c.rectangle(0, GY, W, 3); c.fill()
    # dust
    for (x, y, r, ph) in _dust:
        yy = (y - T * 14 * (r / 2)) % H
        xx = x + 12 * math.sin(T * 0.5 + ph)
        al = 0.25 + 0.25 * math.sin(T * 1.3 + ph * 3)
        rgba(c, GOLDL, al); c.arc(xx, yy, r * 0.8, 0, 6.283); c.fill()


# ------------------------------------------------------------- props
def rrect(c, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def roof(c, x, y, w, h, a, col=GOLD):
    """x center, y = bottom of roof (eave line)"""
    c.move_to(x - w / 2 - 30, y - 18)
    c.curve_to(x - w / 2 + 10, y + 8, x - w / 2 + 40, y, x - w / 2 + 60, y)
    c.line_to(x + w / 2 - 60, y)
    c.curve_to(x + w / 2 - 40, y, x + w / 2 - 10, y + 8, x + w / 2 + 30, y - 18)
    c.line_to(x + w / 2 - 60, y - h)
    c.line_to(x - w / 2 + 60, y - h)
    c.close_path()
    pat = cairo.LinearGradient(0, y - h, 0, y)
    pat.add_color_stop_rgba(0, *GOLDL, a); pat.add_color_stop_rgba(1, *col, a)
    c.set_source(pat); c.fill()
    rgba(c, GOLDD, 0.8 * a); c.set_line_width(3)
    n = int(w / 45)
    for k in range(1, n):
        xx = x - w / 2 + 60 + (w - 120) * k / n
        c.move_to(xx, y - h + 4); c.line_to(xx + (xx - x) * 0.12, y - 4); c.stroke()
    rgba(c, GOLDD, a); c.rectangle(x - w / 2 + 60, y - h - 8, w - 120, 10); c.fill()


def palace(c, x, yf, s=1.0, plaque='唐', a=1.0, tilt=0.0, burn=0.0, T=0):
    if a <= 0:
        return
    c.save(); c.translate(x, yf); c.rotate(tilt); c.scale(s, s)
    rgba(c, (0.62, 0.60, 0.56), a); c.rectangle(-330, -40, 660, 40); c.fill()
    rgba(c, (0.78, 0.76, 0.70), a); c.rectangle(-330, -40, 660, 8); c.fill()
    rgba(c, (0.42, 0.08, 0.07), a); c.rectangle(-270, -250, 540, 210); c.fill()
    for k in range(7):
        xx = -255 + k * 85
        rgba(c, (0.75, 0.16, 0.12), a); c.rectangle(xx, -250, 16, 210); c.fill()
    rgba(c, (0.55, 0.32, 0.18), a)
    for xx in (-200, -120, 90, 170):
        c.rectangle(xx, -210, 30, 120); c.fill()
    rgba(c, (0.06, 0.03, 0.02), a); c.rectangle(-50, -190, 100, 150); c.fill()
    roof(c, 0, -250, 640, 70, a)
    rgba(c, (0.40, 0.08, 0.07), a); c.rectangle(-210, -360, 420, 50); c.fill()
    roof(c, 0, -360, 540, 80, a)
    # ridge horns
    rgba(c, GOLDL, a)
    for sx in (-1, 1):
        c.move_to(sx * 210, -448); c.curve_to(sx * 230, -470, sx * 245, -480, sx * 250, -500)
        c.curve_to(sx * 222, -485, sx * 210, -470, sx * 200, -448); c.close_path(); c.fill()
    if plaque:
        rgba(c, GOLDL, a); c.rectangle(-58, -318, 116, 74); c.fill()
        rgba(c, NAVY, a); c.rectangle(-52, -312, 104, 62); c.fill()
        label(c, plaque, 0, -266, 44, GOLDL, a)
    if burn > 0:
        flames(c, 0, -40, 600, 420 * burn, T, a * min(1, burn * 2))
    c.restore()


def flames(c, x, yb, w, h, T, a):
    r = random.Random(4)
    for k in range(14):
        fx = x - w / 2 + w * (k + 0.5) / 14 + r.uniform(-15, 15)
        fh = h * r.uniform(0.5, 1.0) * (0.85 + 0.15 * math.sin(T * 9 + k))
        fw = w / 9
        for col, sc in ((REDL, 1.0), ((1.0, 0.62, 0.20), 0.65), ((1.0, 0.88, 0.45), 0.35)):
            hh = fh * sc; ww = fw * sc
            sway = 10 * math.sin(T * 6 + k * 1.3)
            c.move_to(fx - ww / 2, yb)
            c.curve_to(fx - ww / 2, yb - hh * 0.5, fx + sway - ww * 0.2, yb - hh * 0.7, fx + sway, yb - hh)
            c.curve_to(fx + sway + ww * 0.2, yb - hh * 0.7, fx + ww / 2, yb - hh * 0.5, fx + ww / 2, yb)
            c.close_path(); rgba(c, col, 0.85 * a); c.fill()


def person(c, x, yf, s=1.0, kind='scholar', robe=None, a=1.0, walk=0.0, face=1, hold=None, glow=0.0):
    """walk: phase (radians) >0 animates, face: 1 right, -1 left"""
    if a <= 0:
        return
    if robe is None:
        robe = {'scholar': ROBE, 'official': PURPLE, 'peasant': (0.62, 0.52, 0.38), 'soldier': GOLD,
                'redofficial': RED, 'kid': (0.55, 0.62, 0.70)}[kind]
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    bob = -abs(math.sin(walk)) * 6 if walk else 0
    c.translate(0, bob)
    if glow > 0:
        pat = cairo.RadialGradient(0, -110, 0, 0, -110, 170)
        pat.add_color_stop_rgba(0, *GOLDL, 0.45 * glow * a); pat.add_color_stop_rgba(1, *GOLDL, 0)
        c.set_source(pat); c.arc(0, -110, 170, 0, 6.283); c.fill()
    # feet
    sw = math.sin(walk) * 10 if walk else 0
    rgba(c, INKC, a)
    c.rectangle(-22 + sw, -10, 18, 10); c.fill()
    c.rectangle(6 - sw, -10, 18, 10); c.fill()
    # robe
    c.move_to(-30, -160); c.line_to(30, -160); c.line_to(46, -8); c.line_to(-46, -8); c.close_path()
    rgba(c, robe, a); c.fill()
    rgba(c, tuple(v * 0.75 for v in robe), a)
    c.move_to(0, -160); c.line_to(14, -110); c.line_to(0, -60); c.set_line_width(4); c.stroke()
    c.rectangle(-36, -100, 72, 9); c.fill()
    # sleeve / arm
    rgba(c, tuple(v * 0.88 for v in robe), a)
    rrect(c, 8, -158, 30, 84, 14); c.fill()
    rgba(c, SKIN, a); c.arc(28, -70, 9, 0, 6.283); c.fill()
    if hold == 'scroll':
        rgba(c, CREAM, a); c.rectangle(30, -96, 18, 54); c.fill()
        rgba(c, BROWN, a); c.rectangle(27, -100, 24, 6); c.fill(); c.rectangle(27, -44, 24, 6); c.fill()
    elif hold == 'book':
        rgba(c, BLUEG, a); c.rectangle(24, -100, 40, 30); c.fill()
        rgba(c, CREAM, a); c.rectangle(24, -76, 40, 5); c.fill()
    elif hold == 'spear':
        rgba(c, BROWN, a); c.rectangle(34, -300, 6, 300); c.fill()
        rgba(c, (0.85, 0.85, 0.85), a); c.move_to(37, -340); c.line_to(46, -300); c.line_to(28, -300); c.close_path(); c.fill()
    elif hold == 'bundle':
        rgba(c, (0.55, 0.40, 0.25), a); c.arc(-30, -140, 30, 0, 6.283); c.fill()
    # neck + head
    rgba(c, SKIN, a); c.rectangle(-8, -172, 16, 14); c.fill()
    c.arc(0, -192, 25, 0, 6.283); c.fill()
    # hats
    if kind == 'scholar' or kind == 'kid':
        rgba(c, INKC, a)
        c.arc(-2, -200, 26, math.pi, 2 * math.pi); c.fill()
        c.rectangle(-28, -204, 52, 8); c.fill()
        if kind == 'scholar':
            c.move_to(-20, -205); c.curve_to(-40, -200, -46, -186, -42, -176); c.set_line_width(5); c.stroke()
    elif kind in ('official', 'redofficial'):
        rgba(c, INKC, a)
        rrect(c, -24, -236, 48, 36, 10); c.fill()
        c.rectangle(-28, -210, 56, 12); c.fill()
        c.rectangle(-82, -214, 164, 6); c.fill()
        c.arc(-82, -211, 6, 0, 6.283); c.fill(); c.arc(82, -211, 6, 0, 6.283); c.fill()
    elif kind == 'peasant':
        rgba(c, (0.88, 0.76, 0.50), a)
        c.move_to(-58, -198); c.line_to(0, -236); c.line_to(58, -198); c.close_path(); c.fill()
        rgba(c, (0.66, 0.54, 0.32), a); c.rectangle(-58, -200, 116, 5); c.fill()
    elif kind == 'soldier':
        rgba(c, GOLDL, a)
        c.arc(0, -198, 28, math.pi, 2 * math.pi); c.fill()
        c.rectangle(-30, -200, 60, 8); c.fill()
        c.move_to(-4, -226); c.line_to(0, -250); c.line_to(4, -226); c.fill()
        rgba(c, RED, a); c.rectangle(-36, -110, 72, 10); c.fill()
    c.restore()


def mini(c, x, yf, s, col, a=1.0):
    """tiny generic figure for grids"""
    if a <= 0:
        return
    rgba(c, col, a)
    c.arc(x, yf - 46 * s, 9 * s, 0, 6.283); c.fill()
    c.move_to(x - 10 * s, yf - 34 * s); c.line_to(x + 10 * s, yf - 34 * s); c.line_to(x + 15 * s, yf); c.line_to(x - 15 * s, yf)
    c.close_path(); c.fill()


def seal(c, ch, x, y, s=1.0, a=1.0, rot=-0.06, size=None):
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    n = len(ch)
    w = 120 if n == 1 else 70 * n + 40
    rgba(c, RED, a); rrect(c, -w / 2, -60, w, 120, 10); c.fill()
    rgba(c, (1, 0.9, 0.85), 0.8 * a); c.set_line_width(4); rrect(c, -w / 2 + 9, -51, w - 18, 102, 6); c.stroke()
    rich(c, ch, 0, 26, size or (74 if n == 1 else 60), 99, (1, 0.96, 0.92), a, 'c', 0, 0.01, shadow=False)
    c.restore()


def cylinder(c, x, yf, w, h, col=RED, a=1.0):
    if a <= 0 or h <= 0:
        return
    rx, ry = w / 2, w * 0.16
    pat = cairo.LinearGradient(x - rx, 0, x + rx, 0)
    dk = tuple(v * 0.6 for v in col); lt = tuple(min(1, v * 1.25) for v in col)
    pat.add_color_stop_rgba(0, *dk, a); pat.add_color_stop_rgba(0.35, *lt, a); pat.add_color_stop_rgba(1, *dk, a)
    c.move_to(x - rx, yf - h); c.line_to(x - rx, yf)
    c.save(); c.translate(x, yf); c.scale(rx, ry); c.arc(0, 0, 1, math.pi, 0, ); c.restore()
    c.line_to(x + rx, yf - h); c.close_path()
    c.set_source(pat); c.fill()
    c.save(); c.translate(x, yf - h); c.scale(rx, ry); c.arc(0, 0, 1, 0, 6.283); c.restore()
    rgba(c, lt, a); c.fill()
    rgba(c, GOLD, a * 0.8); c.set_line_width(2)
    for k in range(int(h / 26)):
        yy = yf - 13 - k * 26
        c.save(); c.translate(x, yy); c.scale(rx, ry); c.arc(0, 0, 1, 0.1, math.pi - 0.1); c.restore(); c.stroke()


def gate(c, x, yf, s, opening, a=1.0, plaque='贡院'):
    """opening: gap width in px (unscaled)"""
    if a <= 0:
        return
    c.save(); c.translate(x, yf); c.scale(s, s)
    wall_w = 260
    for sx in (-1, 1):
        x0 = sx * opening / 2 if sx > 0 else -opening / 2 - wall_w
        rgba(c, (0.45, 0.10, 0.08), a); c.rectangle(x0, -330, wall_w, 330); c.fill()
        rgba(c, (0.36, 0.08, 0.06), a)
        for k in range(6):
            c.rectangle(x0, -330 + k * 55, wall_w, 3); c.fill()
    span = opening + 2 * wall_w
    roof(c, 0, -330, span + 60, 70, a)
    if plaque:
        rgba(c, GOLDL, a); c.rectangle(-70, -315, 140, 58); c.fill()
        rgba(c, NAVY, a); c.rectangle(-64, -309, 128, 46); c.fill()
        label(c, plaque, 0, -274, 32, GOLDL, a)
    c.restore()


def house(c, x, yf, s=1.0, a=1.0, plaque='书院', wall=(0.86, 0.82, 0.74), roofc=(0.30, 0.27, 0.25)):
    if a <= 0:
        return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, wall, a); c.rectangle(-150, -170, 300, 170); c.fill()
    rgba(c, (0.40, 0.12, 0.08), a); c.rectangle(-36, -110, 72, 110); c.fill()
    rgba(c, (0.35, 0.25, 0.18), a); c.rectangle(-120, -130, 50, 50); c.fill(); c.rectangle(70, -130, 50, 50); c.fill()
    c.move_to(-200, -160); c.curve_to(-170, -150, -150, -170, -130, -175); c.line_to(-90, -250); c.line_to(90, -250)
    c.line_to(130, -175); c.curve_to(150, -170, 170, -150, 200, -160); c.line_to(140, -190); c.line_to(-140, -190)
    c.close_path()
    c.move_to(-200, -160); c.line_to(-130, -175); c.line_to(130, -175); c.line_to(200, -160); c.line_to(150, -195); c.line_to(-150, -195); c.close_path()
    rgba(c, roofc, a); c.fill()
    rgba(c, GOLD, a); c.rectangle(-95, -256, 190, 8); c.fill()
    if plaque:
        rgba(c, GOLDL, a); c.rectangle(-56, -168, 112, 46); c.fill()
        rgba(c, NAVY, a); c.rectangle(-51, -163, 102, 36); c.fill()
        label(c, plaque, 0, -135, 26, GOLDL, a)
    c.restore()


def rice(c, x, yf, h, a=1.0, sway=0.0, grain=1.0):
    if a <= 0:
        return
    rgba(c, GREENL, a); c.set_line_width(5)
    tipx = x + 24 + sway
    c.move_to(x, yf); c.curve_to(x, yf - h * 0.6, x + 6 + sway * 0.5, yf - h * 0.9, tipx, yf - h * 0.95); c.stroke()
    c.set_line_width(4); rgba(c, GREEN, a)
    c.move_to(x, yf - 10); c.curve_to(x - 20, yf - h * 0.4, x - 34, yf - h * 0.55, x - 40, yf - h * 0.6); c.stroke()
    if grain > 0:
        for k in range(7):
            u = k / 7
            gx = lerp(x + 8 + sway * 0.5, tipx + 8, u) + 10 * (k % 2)
            gy = yf - h * 0.85 + u * h * 0.32
            rgba(c, GOLDL, a * grain); c.save(); c.translate(gx, gy); c.scale(7, 10); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()


def book(c, x, y, w=120, h=26, col=BLUEG, a=1.0):
    if a <= 0:
        return
    rgba(c, col, a); c.rectangle(x - w / 2, y - h, w, h); c.fill()
    rgba(c, CREAM, a); c.rectangle(x - w / 2 + 6, y - h + 5, w - 12, 4); c.fill()
    rgba(c, (0.96, 0.92, 0.84), a); c.rectangle(x - w / 2, y - 6, w, 6); c.fill()


def paper(c, x, y, w, h, a=1.0, lines=8, written=1.0, seed=1):
    if a <= 0:
        return
    rgba(c, (0.95, 0.91, 0.80), a); c.rectangle(x - w / 2, y - h / 2, w, h); c.fill()
    rgba(c, (0.70, 0.30, 0.22), 0.6 * a); c.set_line_width(2)
    for k in range(lines + 1):
        xx = x - w / 2 + 20 + (w - 40) * k / lines
        c.move_to(xx, y - h / 2 + 20); c.line_to(xx, y + h / 2 - 20); c.stroke()
    r = random.Random(seed)
    rgba(c, INKC, 0.8 * a)
    for k in range(lines):
        xx = x + w / 2 - 20 - (w - 40) * (k + 0.5) / lines
        L = (h - 60) * r.uniform(0.5, 1.0) * clamp(written * lines - k)
        if L > 0:
            yy = y - h / 2 + 30
            while yy < y - h / 2 + 30 + L:
                c.rectangle(xx - 7, yy, 14, 10); yy += 18
            c.fill()


def scroll_item(c, x, y, w, h, a=1.0, text=None, size=40):
    if a <= 0:
        return
    rgba(c, (0.95, 0.91, 0.80), a); c.rectangle(x - w / 2, y - h / 2, w, h); c.fill()
    rgba(c, BROWN, a); rrect(c, x - w / 2 - 14, y - h / 2 - 16, w + 28, 18, 8); c.fill()
    rrect(c, x - w / 2 - 14, y + h / 2 - 2, w + 28, 18, 8); c.fill()
    if text:
        for k, ch in enumerate(text):
            label(c, ch, x, y - h / 2 + 60 + k * (size + 10), size, INKC, a)


def balance(c, x, y, tilt, a=1.0, L=330, ltxt='北', rtxt='南', lload=None, rload=None):
    """tilt>0: left side down"""
    if a <= 0:
        return
    rgba(c, GOLDD, a); c.rectangle(x - 10, y, 20, GY - y); c.fill()
    c.rectangle(x - 120, GY - 20, 240, 20); c.fill()
    ang = tilt * 0.32
    lx, ly = x - L * math.cos(ang), y + L * math.sin(ang)
    rx, ry = x + L * math.cos(ang), y - L * math.sin(ang)
    rgba(c, GOLDL, a); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(lx, ly); c.line_to(rx, ry); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.arc(x, y, 22, 0, 6.283); c.fill()
    for px, py, txt, load in ((lx, ly, ltxt, lload), (rx, ry, rtxt, rload)):
        rgba(c, GOLD, 0.8 * a); c.set_line_width(4)
        c.move_to(px, py); c.line_to(px - 120, py + 180); c.stroke()
        c.move_to(px, py); c.line_to(px + 120, py + 180); c.stroke()
        c.move_to(px - 150, py + 180); c.curve_to(px - 110, py + 240, px + 110, py + 240, px + 150, py + 180); c.close_path()
        rgba(c, GOLD, a); c.fill()
        if load:
            load(px, py + 180)
        if txt:
            label(c, txt, px, py + 230, 40, INKC, a)


# ------------------------------------------------------------- map
CITIES = {'长安': (560, 470), '洛阳': (760, 480), '开封': (900, 490), '临安': (1290, 760), '福州': (1230, 905),
          '燕京': (1000, 260)}


def land(c, a=1.0, ytop=0, T=0):
    pts = [(0, 230), (1180, 230), (1260, 260), (1330, 300), (1560, 330), (1600, 380), (1420, 470), (1400, 560),
           (1480, 650), (1440, 720), (1360, 820), (1300, 920), (1200, 1010), (1050, 1080), (0, 1080)]
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()
    rgba(c, (0.24, 0.18, 0.12), 0.9 * a); c.fill_preserve()
    rgba(c, GOLD, 0.6 * a); c.set_line_width(3); c.stroke()


def river(c, pts, col, a, width=6, dash=None, prog=1.0):
    if a <= 0:
        return
    n = max(2, int(len(pts) * prog))
    rgba(c, col, a); c.set_line_width(width)
    if dash:
        c.set_dash(dash)
    c.move_to(*pts[0])
    for p in pts[1:n]:
        c.line_to(*p)
    c.stroke(); c.set_dash([])


def wavy(x0, x1, y, amp, k, ph=0):
    return [(x, y + amp * math.sin(x * k + ph) + 0.4 * amp * math.sin(x * k * 2.3 + ph)) for x in range(int(x0), int(x1) + 1, 20)]


HUANGHE = wavy(300, 1340, 400, 25, 0.008)
HUAIHE = wavy(500, 1420, 590, 14, 0.010, 1.0)
CHANGJIANG = wavy(300, 1460, 690, 22, 0.007, 2.0)


def citydot(c, name, a=1.0, glow=0.0, col=GOLDL, size=30, dx=0, dy=-24):
    if a <= 0:
        return
    x, y = CITIES[name]
    if glow > 0:
        pat = cairo.RadialGradient(x, y, 0, x, y, 200 * glow)
        pat.add_color_stop_rgba(0, *GOLDL, 0.55 * a); pat.add_color_stop_rgba(1, *GOLDL, 0)
        c.set_source(pat); c.arc(x, y, 200 * glow, 0, 6.283); c.fill()
    rgba(c, col, a); c.arc(x, y, 10, 0, 6.283); c.fill()
    rgba(c, DARK, a); c.arc(x, y, 4, 0, 6.283); c.fill()
    label(c, name, x + dx, y + dy, size, col, a)


def swords(c, x, y, s, a):
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    for sg in (1, -1):
        c.save(); c.rotate(sg * 0.75)
        rgba(c, (0.85, 0.85, 0.85), a); c.rectangle(-4, -50, 8, 70); c.fill()
        rgba(c, REDL, a); c.rectangle(-14, 20, 28, 6); c.fill(); c.rectangle(-3, 26, 6, 18); c.fill()
        c.restore()
    c.restore()


def arrow(c, x0, y0, x1, y1, col, a, w=6, head=22):
    if a <= 0:
        return
    rgba(c, col, a); c.set_line_width(w)
    ang = math.atan2(y1 - y0, x1 - x0)
    c.move_to(x0, y0); c.line_to(x1 - head * 0.7 * math.cos(ang), y1 - head * 0.7 * math.sin(ang)); c.stroke()
    c.move_to(x1, y1)
    c.line_to(x1 - head * math.cos(ang - 0.45), y1 - head * math.sin(ang - 0.45))
    c.line_to(x1 - head * math.cos(ang + 0.45), y1 - head * math.sin(ang + 0.45))
    c.close_path(); c.fill()


def cross(c, x, y, s, a, col=REDL):
    if a <= 0:
        return
    rgba(c, col, a); c.set_line_width(14 * s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x - 50 * s, y - 50 * s); c.line_to(x + 50 * s, y + 50 * s)
    c.move_to(x + 50 * s, y - 50 * s); c.line_to(x - 50 * s, y + 50 * s); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)

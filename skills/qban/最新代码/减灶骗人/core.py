import math, random
import cairocffi as cairo

W, H, FPS = 1920, 1080, 30
SERIF = "Noto Serif CJK SC"
HAND = "ZCOOL KuaiLe"

WHITE = (0.98, 0.96, 0.92)
CREAM = (0.95, 0.90, 0.78)
GOLD = (0.93, 0.76, 0.42)
GOLDL = (1.0, 0.86, 0.52)
GOLDD = (0.62, 0.47, 0.22)
RED = (0.78, 0.18, 0.14)
REDL = (0.96, 0.36, 0.28)
YEL = (1.0, 0.88, 0.30)
INK = (0.13, 0.09, 0.07)
GREY = (0.66, 0.62, 0.56)
TAU = 2 * math.pi
EVENTS = []
REC = [False]


def rec(t0, kind):
    if REC[0]:
        EVENTS.append((t0, kind))


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
    x = clamp(x); s = 2.0; x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def lerp(a, b, u):
    return a + (b - a) * u


def lerpc(a, b, u):
    return tuple(lerp(x, y, u) for x, y in zip(a, b))


def pop(t, t0, d=0.35):
    return back(seg(t, t0, t0 + d))


def fin(t, t0, d=0.3):
    return eout(seg(t, t0, t0 + d))


def rgba(c, col, a=1.0):
    c.set_source_rgba(col[0], col[1], col[2], a)


def dk(col, k=0.72):
    return tuple(v * k for v in col[:3])


def lt(col, k=0.3):
    return tuple(v + (1 - v) * k for v in col[:3])


def rr(c, x, y, w, h, r):
    r = max(0.1, min(r, w / 2, h / 2))
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def ell(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(max(rx, .01), max(ry, .01)); c.arc(0, 0, 1, 0, TAU); c.restore()


def fill2(c, col, a=1.0, lw=3.0, k=0.68):
    """flat fill with same-hue darker outline (no black outline)"""
    rgba(c, col, a); c.fill_preserve()
    rgba(c, dk(col, k), a); c.set_line_width(lw); c.stroke()


def font(c, size, fam=SERIF, bold=True):
    c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def tw(c, s, size, fam=SERIF):
    font(c, size, fam)
    return c.text_extents(s)[4]


def text(c, s, x, y, size, col=WHITE, a=1.0, align='l', fam=SERIF, shadow=0.5):
    font(c, size, fam)
    w = c.text_extents(s)[4]
    x0 = x if align == 'l' else (x - w / 2 if align == 'c' else x - w)
    if shadow:
        c.set_source_rgba(0, 0, 0, shadow * a); c.move_to(x0 + size * 0.03, y + size * 0.05); c.show_text(s)
    rgba(c, col, a); c.move_to(x0, y); c.show_text(s)
    c.new_path()
    return w


def vtext(c, s, x, y, size, col, a=1.0, gap=1.08, fam=SERIF):
    font(c, size, fam)
    for i, ch in enumerate(s):
        w = c.text_extents(ch)[4]
        rgba(c, col, a); c.move_to(x - w / 2, y + size * 0.88 + i * size * gap); c.show_text(ch)
    c.new_path()


# ---------------------------------------------------------------- captions
def caption(c, t, top, big, col=GOLDL, t_top=0.05, t_big=0.45, x=80, y=118, bsize=112, instant=False):
    """two-layer caption"""
    if top and not instant: rec(t_top, 'tick')
    if big and not instant: rec(t_big, 'boom' if col[0] > 0.9 and col[1] < 0.5 else 'pop')
    if top:
        font(c, 50)
        cx = x
        for i, ch in enumerate(top):
            p = 1.0 if instant else eout(seg(t - t_top - i * 0.018, 0, 0.18))
            adv = c.text_extents(ch)[4]
            if p > 0.01:
                c.move_to(cx, y + (1 - p) * 10); c.text_path(ch)
                c.set_source_rgba(0.14, 0.08, 0.05, 0.9 * p); c.set_line_width(7); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
                rgba(c, WHITE, p); c.fill()
            cx += adv
        c.new_path()
    if big:
        size = bsize
        w = tw(c, big, size)
        if w > W - x - 70:
            size = size * (W - x - 70) / w; w = W - x - 70
        yb = y + 40 + size * 0.95
        p = 1.0 if instant else seg(t, t_big, t_big + 0.32)
        if p > 0:
            pe = eout(p)
            blur = (1 - pe) * 16
            font(c, size)
            # glow/shadow
            for k in range(3):
                c.set_source_rgba(0, 0, 0, 0.22 * pe); c.move_to(x + 3 + k * 2, yb + 5 + k * 2); c.show_text(big)
            if blur > 0.6:
                for i in range(8):
                    ang = i * TAU / 8
                    rgba(c, col, 0.16 * pe); c.move_to(x + math.cos(ang) * blur, yb + math.sin(ang) * blur); c.show_text(big)
                c.move_to(x, yb); c.text_path(big)
                c.set_source_rgba(0.16, 0.09, 0.05, pe * pe); c.set_line_width(size * 0.11); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
                rgba(c, col, pe * pe); c.fill()
            else:
                c.move_to(x, yb); c.text_path(big)
                c.set_source_rgba(0.16, 0.09, 0.05, 1.0); c.set_line_width(size * 0.11); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
                rgba(c, col, 1.0); c.fill()
            c.new_path()
            # underline fading left->right
            q = 1.0 if instant else eout(seg(t, t_big + 0.1, t_big + 0.6))
            L = (w + 120) * q
            g = cairo.LinearGradient(x, 0, x + max(L, 1), 0)
            g.add_color_stop_rgba(0, col[0], col[1], col[2], 0.95)
            g.add_color_stop_rgba(0.6, col[0], col[1], col[2], 0.55)
            g.add_color_stop_rgba(1, col[0], col[1], col[2], 0.0)
            c.set_source(g); c.rectangle(x, yb + size * 0.2, L, 5); c.fill()


def sticker(c, s, x, y, t, t0, size=72, col=YEL, rot=-0.12, a=1.0, wob=True):
    rec(t0, 'sticker')
    if t < t0:
        return
    sc = pop(t, t0, 0.3)
    if sc <= 0.01:
        return
    c.save(); c.translate(x, y)
    r = rot + (0.03 * math.sin((t - t0) * 6) if wob else 0)
    c.rotate(r); c.scale(sc, sc)
    font(c, size, HAND, bold=False)
    lines = s.split('\n')
    for li, ln in enumerate(lines):
        w = c.text_extents(ln)[4]
        yy = li * size * 1.05 + size * 0.35 - (len(lines) - 1) * size * 0.5
        xx = -w / 2 + li * size * 0.3
        c.move_to(xx, yy); c.text_path(ln)
        c.set_source_rgba(0.12, 0.06, 0.04, a); c.set_line_width(size * 0.16); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        rgba(c, col, a); c.fill()
    c.restore()


def nameplate(c, x, y, pre, name, a=1.0, size=40):
    """dark box with gold border; grey small prefix + white big name; centered at x, bottom at y"""
    if a <= 0.01:
        return
    w1 = tw(c, pre, size * 0.58) if pre else 0
    w2 = tw(c, name, size)
    gap = 10 if pre else 0
    W_ = w1 + gap + w2 + 34
    h = size * 1.45
    x0 = x - W_ / 2
    rr(c, x0, y - h, W_, h, 6)
    c.set_source_rgba(0.12, 0.08, 0.06, 0.92 * a); c.fill_preserve()
    rgba(c, GOLD, a); c.set_line_width(2.5); c.stroke()
    if pre:
        text(c, pre, x0 + 17, y - h * 0.3, size * 0.58, GREY, a, shadow=0)
    text(c, name, x0 + 17 + w1 + gap, y - h * 0.27, size, WHITE, a, shadow=0)


def srcbox(c, book, txt, x, y, a=1.0, size=34, align='l'):
    """source tag: dark box gold edge, grey 《》 + white text"""
    if a <= 0.01:
        return
    w1 = tw(c, book, size * 0.7); w2 = tw(c, txt, size) if txt else 0
    Wd = w1 + (14 if txt else 0) + w2 + 36; h = size * 1.55
    x0 = x if align == 'l' else x - Wd / 2
    rr(c, x0, y, Wd, h, 5)
    c.set_source_rgba(0.08, 0.06, 0.05, 0.85 * a); c.fill_preserve()
    rgba(c, GOLDD, a); c.set_line_width(2); c.stroke()
    text(c, book, x0 + 18, y + h * 0.66, size * 0.7, GREY, a, shadow=0)
    if txt:
        text(c, txt, x0 + 18 + w1 + 14, y + h * 0.7, size, WHITE, a, shadow=0)


def wrap(c, s, size, maxw, fam=SERIF):
    font(c, size, fam)
    lines = []; cur = ''
    for ch in s:
        if c.text_extents(cur + ch)[4] > maxw and cur:
            if ch in '，。、；：！？」”）':
                cur += ch; lines.append(cur); cur = ''; continue
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def quote(c, t, t0, orig, plain, book, x=80, y=760, w=900, a=1.0, osize=48, psize=42):
    rec(t0, 'paper')
    p = fin(t, t0, 0.3)
    if p <= 0.01:
        return
    ol = wrap(c, orig, osize, w - 150)
    pl = wrap(c, plain, psize, w - 150)
    h = 36 + len(ol) * osize * 1.35 + 18 + len(pl) * psize * 1.38 + 70
    yy = y - h + (1 - p) * 30
    rr(c, x, yy, w, h, 10)
    c.set_source_rgba(0.09, 0.06, 0.05, 0.84 * p * a); c.fill_preserve()
    rgba(c, GOLDD, p * a); c.set_line_width(2.5); c.stroke()
    # tags
    cy = yy + 36 + osize
    rr(c, x + 22, cy - osize * 0.86, 84, osize * 1.05, 5); rgba(c, GOLD, p * a); c.fill()
    text(c, '原文', x + 30, cy - 4, 32, INK, p * a, shadow=0)
    for i, ln in enumerate(ol):
        text(c, ln, x + 124, cy + i * osize * 1.35, osize, GOLDL, p * a, shadow=0)
    cy2 = cy + len(ol) * osize * 1.35 + 18
    p2 = fin(t, t0 + 0.45, 0.3)
    rr(c, x + 22, cy2 - psize * 0.9, 84, psize * 1.12, 5); rgba(c, WHITE, p2 * a); c.fill()
    text(c, '白话', x + 30, cy2 - 3, 32, INK, p2 * a, shadow=0)
    for i, ln in enumerate(pl):
        text(c, ln, x + 124, cy2 + i * psize * 1.38, psize, WHITE, p2 * a, shadow=0)
    text(c, book, x + w - 22, yy + h - 20, 26, GREY, p * a, align='r', shadow=0)
    return h


def redcircle(c, x, y, rx, ry, t, t0, d=0.45, a=1.0, lw=9):
    rec(t0, 'scribble')
    p = eout(seg(t, t0, t0 + d))
    if p <= 0:
        return
    c.save(); c.translate(x, y); c.scale(rx, ry)
    c.arc(0, 0, 1, -math.pi * 0.6, -math.pi * 0.6 + TAU * 1.05 * p)
    c.restore()
    rgba(c, (0.85, 0.15, 0.12), a); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)


def bignum(c, s, x, y, size, t, t0, col=GOLDL, unit='', usize=None, align='c'):
    rec(t0, 'ding')
    sc = pop(t, t0, 0.4)
    if sc <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(sc, sc)
    font(c, size)
    w = c.text_extents(s)[4]
    x0 = -w / 2 if align == 'c' else 0
    c.set_source_rgba(0, 0, 0, 0.45); c.move_to(x0 + 6, 8); c.show_text(s)
    c.move_to(x0, 0); c.text_path(s); c.set_source_rgba(0.16, 0.09, 0.05, 1); c.set_line_width(size * 0.09)
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve(); rgba(c, col); c.fill()
    if unit:
        us = usize or size * 0.32
        font(c, us); uw = c.text_extents(unit)[4]
        c.move_to(-uw / 2 if align == 'c' else 0, us * 1.5); c.text_path(unit)
        c.set_source_rgba(0.16, 0.09, 0.05, 1); c.set_line_width(us * 0.16); c.stroke_preserve(); rgba(c, WHITE); c.fill()
    c.restore(); c.new_path()


def stamp(c, s, x, y, t, t0, size=90, col=RED, rot=-0.2):
    rec(t0, 'seal')
    if t < t0:
        return
    u = seg(t, t0, t0 + 0.18)
    sc = lerp(2.2, 1.0, eout(u)); a = u
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    font(c, size); w = c.text_extents(s)[4]
    rr(c, -w / 2 - 22, -size * 0.85, w + 44, size * 1.2, 10)
    rgba(c, col, a); c.set_line_width(8); c.stroke()
    rgba(c, col, a); c.move_to(-w / 2, size * 0.18); c.show_text(s)
    c.restore(); c.new_path()


def dust(c, T, seed=3, n=40, col=(1, 0.9, 0.7), a=0.35, area=(0, 0, W, H)):
    rnd = random.Random(seed)
    x0, y0, w, h = area
    for i in range(n):
        x = x0 + (rnd.random() * w + T * rnd.uniform(-8, 8)) % w
        y = y0 + (rnd.random() * h - T * rnd.uniform(4, 14)) % h
        r = rnd.uniform(1.2, 3.2)
        rgba(c, col, a * (0.5 + 0.5 * math.sin(T * 2 + i)))
        c.arc(x, y, r, 0, TAU); c.fill()


def glow(c, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    g.add_color_stop_rgba(0.5, col[0], col[1], col[2], a * 0.35)
    g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(g); c.arc(x, y, r, 0, TAU); c.fill()


def footer(c, s, a=1.0):
    if s and a > 0.01:
        w = tw(c, s, 26)
        rr(c, W - 44 - w - 28, H - 70, w + 28, 46, 6)
        c.set_source_rgba(0.08, 0.06, 0.05, 0.78 * a); c.fill_preserve()
        rgba(c, GOLDD, a * 0.9); c.set_line_width(1.5); c.stroke()
        text(c, s, W - 58, H - 38, 26, (0.85, 0.80, 0.72), a, align='r', shadow=0)


def otext(c, s, x, y, size, col=WHITE, a=1.0, align='l', fam=SERIF, lw=None):
    """text with dark outline (readable on bright backgrounds)"""
    if a <= 0.01:
        return
    font(c, size, fam)
    w = c.text_extents(s)[4]
    x0 = x if align == 'l' else (x - w / 2 if align == 'c' else x - w)
    c.move_to(x0, y); c.text_path(s)
    c.set_source_rgba(0.16, 0.09, 0.05, a); c.set_line_width(lw or size * 0.12); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    rgba(c, col, a); c.fill()

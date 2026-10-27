"""v2 look: dark low-detail backdrops, pure-white serif captions, gold hand underline,
spotlight subject, Song-dynasty flat figures & architecture."""
from jz import *
from jz import _load

TXT = (0.97, 0.96, 0.93)
TXT2 = (0.70, 0.67, 0.62)
GOLDT = (0.98, 0.80, 0.42)
REDT = (0.95, 0.36, 0.28)
SKIN2 = (0.80, 0.62, 0.46)
HAT = (0.07, 0.06, 0.06)
LACQ = (0.72, 0.13, 0.09)

FONT_N = "Noto Serif CJK SC Medium"
FONT_B = "Noto Serif CJK SC SemiBold"
FONT_X = "Noto Serif CJK SC Bold"


def fnt(c, size, fam=FONT_N):
    if fam == FONT_X:
        c.select_font_face("Noto Serif CJK SC", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    else:
        c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def parse2(s, base):
    out = []; col = base; ul = False
    for ch in s:
        if ch == '[': col, ul = GOLDT, True; continue
        if ch == '{': col, ul = REDT, True; continue
        if ch == '<': col, ul = GOLDT, False; continue
        if ch in ']}>': col, ul = base, False; continue
        out.append((ch, col, ul))
    return out


def tw(c, s, size, fam=FONT_N):
    fnt(c, size, fam)
    return sum(c.text_extents(ch)[4] for ch, _, _ in parse2(s, TXT))


POP = True
OUTW = 0.13


def text2(c, s, x, y, size, t=99, base=TXT, a=1.0, align='l', stagger=0.028, fade=0.28, fam=FONT_N, ul_t=None):
    chars = parse2(s, base)
    fnt(c, size, fam)
    advs = [c.text_extents(ch)[4] for ch, _, _ in chars]
    tot = sum(advs)
    x0 = x if align == 'l' else (x - tot / 2 if align == 'c' else x - tot)
    cx = x0; runs = []; cur = None
    for i, ((ch, col, ul), adv) in enumerate(zip(chars, advs)):
        p = eout(seg(t - i * stagger, 0, fade)); aa = p * a
        if aa > 0.003 and ch != ' ':
            sc_ = 1 + 0.35 * (1 - p) if POP else 1.0
            c.save(); c.translate(cx + adv / 2, y - size * 0.35); c.scale(sc_, sc_); c.translate(-(cx + adv / 2), -(y - size * 0.35))
            c.move_to(cx, y + (0 if POP else (1 - p) * size * 0.18)); c.text_path(ch)
            c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.set_source_rgba(0.04, 0.03, 0.02, 0.92 * aa); c.set_line_width(max(4, size * OUTW)); c.stroke_preserve()
            rgba(c, col, aa); c.fill()
            c.restore()
        if ul:
            if cur is None: cur = [cx, cx + adv, col, i]
            else: cur[1] = cx + adv
        elif cur is not None:
            runs.append(cur); cur = None
        cx += adv
    if cur is not None: runs.append(cur)
    c.new_path()
    for (ux0, ux1, col, i0) in runs:
        p = ease(seg(t - i0 * stagger - 0.25, 0, 0.45)) * a
        if p <= 0.01: continue
        w = (ux1 - ux0 + 10) * p
        yy = y + size * 0.20
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        for lw_, cc_, al_ in ((max(3, size * 0.055) + size * 0.08, (0.04, 0.03, 0.02), 0.85), (max(3, size * 0.06), col, 0.95)):
            rgba(c, cc_, al_ * a); c.set_line_width(lw_)
            c.move_to(ux0 - 4, yy + 2)
            c.curve_to(ux0 + w * 0.3, yy - 3, ux0 + w * 0.7, yy + 4, ux0 - 4 + w, yy - 1); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
    return tot


KIND = {'n': (68, TXT, FONT_X, 1.30), 'b': (110, GOLDT, FONT_X, 1.22), 'q': (60, GOLDT, FONT_X, 1.32),
        'l': (42, TXT2, FONT_B, 1.4), 's': (58, TXT, FONT_X, 1.30), 'm': (88, TXT, FONT_X, 1.24)}
MAXL = 3


def caps2(c, t, lines, x=90, y0=80, maxw=1740):
    """rolling caption block: at most MAXL lines, older lines scroll up and fade; big bold outlined text"""
    info = []
    for ln in lines:
        t0, s_ = ln[0], ln[1]
        k = ln[2] if len(ln) > 2 else 'n'
        size, col, fam, gap = KIND[k]
        w_ = tw(c, s_, size, fam)
        if w_ > maxw: size = size * maxw / w_
        info.append((t0, s_, size, col, fam, size * gap))
    vis = sum(ease(seg(t, t0, t0 + 0.35)) for (t0, *_r) in info)
    first = max(0.0, vis - MAXL)
    fi = int(first); fr = first - fi
    scroll = sum(h for (*_r, h) in info[:fi]) + (info[fi][5] * fr if fi < len(info) else 0)
    y = y0 - scroll
    for idx, (t0, s_, size, col, fam, h) in enumerate(info):
        if t >= t0:
            a = 1.0
            if y < y0 - 2: a = clamp(1 - (y0 - y) / (h * 0.8))
            if a > 0.01:
                text2(c, s_, x, y + size * 0.84, size, t - t0, col, a, 'l', 0.03, 0.22, fam)
        y += h


def footer(c, s, a=1.0):
    if a <= 0 or not s: return
    fnt(c, 24, "Noto Sans CJK SC"); rgba(c, (0.70, 0.67, 0.62), 0.9 * a)
    w = c.text_extents(s)[4]; c.move_to(W - 50 - w, H - 34); c.show_text(s)


def counter(c, label_s, num, unit, a=1.0, x=1500, y=70):
    if a <= 0: return
    rgba(c, LACQ, a); c.rectangle(x, y + 6, 22, 22); c.fill()
    fnt(c, 30); rgba(c, TXT2, a); c.move_to(x + 36, y + 28); c.show_text(label_s)
    fnt(c, 92, FONT_B); rgba(c, TXT, a); c.move_to(x, y + 130); c.show_text(num)
    nw = c.text_extents(num)[4]
    fnt(c, 38); rgba(c, TXT2, a); c.move_to(x + nw + 14, y + 128); c.show_text(unit)
    rgba(c, (0.6, 0.55, 0.5), 0.5 * a); c.rectangle(x, y + 156, 330, 2); c.fill()


# ------------------------------------------------------------ backdrops
_WOOD = None


def _wood():
    global _WOOD
    if _WOOD is None:
        r = np.random.RandomState(3)
        y = np.arange(H)[:, None]; x = np.arange(W)[None, :]
        plank = (y // 150) % 2
        grain = np.sin(x / 37.0 + np.sin(y / 9.0) * 2.0 + (y // 150) * 1.7) * 0.5 + 0.5
        n = r.rand(H // 4 + 1, W // 4 + 1); n = np.kron(n, np.ones((4, 4)))[:H, :W]
        v = 0.85 + 0.08 * grain + 0.07 * n - 0.05 * plank
        seam = ((y % 150) < 3).astype(float)
        v = v * (1 - 0.45 * seam)
        base = np.array([0.20, 0.135, 0.075])
        img = (v[..., None] * base[None, None, :]).clip(0, 1)
        a = (img * 255).astype(np.uint8)
        bgra = np.empty((H, W, 4), np.uint8); bgra[..., 0] = a[..., 2]; bgra[..., 1] = a[..., 1]; bgra[..., 2] = a[..., 0]; bgra[..., 3] = 255
        _WOOD = cairo.ImageSurface.create_for_data(bytearray(bgra.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4)
    return _WOOD


_DMAP = None


def _darkmap():
    global _DMAP
    if _DMAP is None:
        img, m = _load()
        a = np.asarray(img).astype(np.float32) / 255
        lum = a.mean(axis=2)
        # relief from luminance gradient
        gy, gx = np.gradient(lum)
        shade = np.clip(0.5 + (gx - gy) * 6, 0, 1)
        v = 0.55 * lum + 0.45 * shade
        v = (v - v.min()) / (v.max() - v.min())
        col = np.stack([v * 0.30 + 0.02, v * 0.24 + 0.015, v * 0.16 + 0.01], 2)
        _DMAP = Image.fromarray((col.clip(0, 1) * 255).astype(np.uint8))
    return _DMAP, _load()[1]


def draw_dmap(c, lon, lat, vw):
    img, m = _darkmap()
    cx, cy = ll2b(lon, lat)
    vh = vw * H / W
    x0 = min(max(cx - vw / 2, 0), m['W'] - vw); y0 = min(max(cy - vh / 2, 0), m['H'] - vh)
    fr = img.transform((W, H), Image.AFFINE, (vw / W, 0, x0, 0, vh / H, y0), resample=Image.BILINEAR)
    a = np.asarray(fr)
    bgra = np.empty((H, W, 4), np.uint8); bgra[..., 0] = a[..., 2]; bgra[..., 1] = a[..., 1]; bgra[..., 2] = a[..., 0]; bgra[..., 3] = 255
    s = cairo.ImageSurface.create_for_data(bytearray(bgra.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4)
    c.set_source_surface(s, 0, 0); c.paint()
    k = W / vw

    def f(lo, la):
        bx, by = ll2b(lo, la)
        return (bx - x0) * k, (by - y0) * k
    return f


def spot(c, x, y, r, a=1.0, col=(1.0, 0.78, 0.45)):
    if a <= 0: return
    pat = cairo.RadialGradient(x, y, 0, x, y, r)
    pat.add_color_stop_rgba(0, *col, 0.30 * a); pat.add_color_stop_rgba(0.5, *col, 0.12 * a); pat.add_color_stop_rgba(1, *col, 0)
    c.set_source(pat); c.arc(x, y, r, 0, 6.283); c.fill()


def lamp(c, x, y, T, a=1.0):
    spot(c, x, y, 380, 0.7 * a)
    rgba(c, (0.35, 0.25, 0.15), a); c.save(); c.translate(x, y + 18); c.scale(40, 12); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    fl = 1 + 0.08 * math.sin(T * 13) + 0.05 * math.sin(T * 7.3)
    rgba(c, (1, 0.75, 0.35), a); c.save(); c.translate(x, y); c.scale(9 * fl, 16 * fl); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    rgba(c, (1, 0.95, 0.8), a); c.save(); c.translate(x, y + 3); c.scale(4, 8); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()


def bg_wood(c, T, sx=1200, sy=600, sr=700):
    c.set_source_surface(_wood(), 0, 0); c.paint()
    # darken left text zone
    g = cairo.LinearGradient(0, 0, 1100, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.paint()
    lamp(c, 1840, 70, T)
    spot(c, sx, sy, sr, 1.0)


def bg_dark(c, T, sx=1200, sy=600, sr=700):
    rgba(c, (0.045, 0.038, 0.032)); c.paint()
    spot(c, sx, sy, sr, 0.9)


def ui_panel(c, x, y, w, h, title=None, a=1.0):
    if a <= 0: return
    rgba(c, (0.07, 0.07, 0.08), 0.92 * a); rrect(c, x, y, w, h, 22); c.fill()
    rgba(c, (0.75, 0.72, 0.66), 0.55 * a); c.set_line_width(2.5); rrect(c, x, y, w, h, 22); c.stroke()
    if title:
        text2(c, title, x + w / 2, y + 58, 36, 99, TXT, a, 'c')
        rgba(c, (0.75, 0.72, 0.66), 0.3 * a); c.rectangle(x, y + 86, w, 2); c.fill()


def chip(c, s, x, y, col=LACQ, a=1.0, size=30):
    if a <= 0: return
    w = tw(c, s, size) + 34
    rgba(c, col, 0.92 * a); rrect(c, x - w / 2, y - size * 0.95, w, size * 1.5, 6); c.fill()
    rgba(c, (1, 0.9, 0.8), 0.6 * a); c.set_line_width(2); rrect(c, x - w / 2 + 4, y - size * 0.95 + 4, w - 8, size * 1.5 - 8, 4); c.stroke()
    text2(c, s, x, y + size * 0.15, size, 99, (1, 0.97, 0.92), a, 'c')


def qmark(c, x, y, s, a=1.0, T=0):
    if a <= 0: return
    c.save(); c.translate(x, y + 6 * math.sin(T * 3 + x)); c.scale(s, s)
    text2(c, "?", 0, 0, 120, 99, GOLDT, a, 'c', fam=FONT_B)
    c.restore()


# ------------------------------------------------------------ Song figures
ROBES = {'official': (0.56, 0.14, 0.12), 'official2': (0.20, 0.36, 0.30), 'emperor': (0.70, 0.32, 0.12),
         'courier': (0.36, 0.40, 0.44), 'commoner': (0.45, 0.38, 0.30), 'commoner2': (0.30, 0.36, 0.40),
         'soldier': (0.30, 0.30, 0.32), 'yue': (0.32, 0.30, 0.30), 'kid': (0.55, 0.45, 0.32),
         'mingsoldier': (0.66, 0.16, 0.12), 'scout': (0.30, 0.25, 0.20), 'mongol': (0.24, 0.40, 0.44),
         'mongol2': (0.48, 0.34, 0.22), 'jurchen': (0.28, 0.30, 0.42), 'mingoff': (0.50, 0.12, 0.12), 'tongshi': (0.36, 0.38, 0.30),
         'eunuch': (0.22, 0.34, 0.55), 'eunuch2': (0.66, 0.18, 0.14), 'doctor': (0.32, 0.44, 0.38), 'craft': (0.50, 0.42, 0.32),
         'mingemp': (0.86, 0.64, 0.18), 'zhangcha': (0.42, 0.36, 0.28)}


def sperson(c, x, yf, s=1.0, kind='official', a=1.0, face=1, pose='stand', p=1.0, walk=None, robe=None):
    """slender flat Song figure, ~380px tall at s=1. pose: stand, bow, kneel, raise, cry, point"""
    if a <= 0: return
    col = robe or ROBES.get(kind, (0.4, 0.35, 0.3))
    dk = tuple(v * 0.72 for v in col)
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    kneel = p if pose == 'kneel' else 0.0
    bow = p if pose in ('bow', 'kneel') else 0.0
    # legs / boots
    leg_h = 150 * (1 - 0.55 * kneel)
    sw = math.sin(walk) * 22 if walk is not None else 0
    rgba(c, (0.10, 0.08, 0.07), a)
    for lx, ph in ((-14, sw), (12, -sw)):
        c.move_to(lx - 9, -leg_h); c.line_to(lx + 9, -leg_h); c.line_to(lx + 9 + ph * 0.6, -8); c.line_to(lx + 22 + ph * 0.6, 0)
        c.line_to(lx - 9 + ph * 0.6, 0); c.close_path(); c.fill()
    c.translate(0, -leg_h + 40)
    c.rotate(0.55 * bow)
    # robe body
    soldier = kind in ('soldier', 'yue')
    short = kind in ('mingsoldier', 'scout', 'jurchen', 'craft', 'zhangcha')
    rgba(c, col, a)
    hem = 70 if not soldier else 52
    hy = 30 if not (soldier or short) else (-10 if soldier else -40)
    if kind == 'scout':  # sheepskin cloak behind
        rgba(c, (0.80, 0.74, 0.62), a)
        c.move_to(-34, -214); c.curve_to(-60, -150, -64, -90, -60, -50)
        for k in range(5): c.line_to(-60 + k * 12, -44 + (k % 2) * 8)
        c.line_to(0, -210); c.close_path(); c.fill()
        rgba(c, (0.45, 0.32, 0.18), a); c.set_line_width(4); c.arc(-30, -150, 70, 1.9, 4.4); c.stroke()  # bow on back
        rgba(c, col, a)
    c.move_to(-30, -210); c.line_to(30, -210); c.curve_to(40, -120, 46, -60, hem * 0.75, hy)
    c.line_to(-hem * 0.75, hy); c.curve_to(-46, -60, -40, -120, -30, -210); c.close_path(); c.fill()
    if kind in ('mingsoldier', 'mongol', 'mongol2', 'jurchen', 'tongshi', 'eunuch', 'eunuch2', 'craft', 'zhangcha'):
        rgba(c, tuple(v * 0.6 for v in col), a); c.rectangle(-4, -206, 8, 200 + hy); c.fill()  # front opening line
    if kind in ('mingoff', 'mingemp', 'eunuch2'):
        rgba(c, GOLD if kind != 'mingemp' else (0.95, 0.80, 0.35), a); c.rectangle(-22, -180, 44, 44); c.fill()  # 补子
    if soldier:
        # armor scales + skirt
        rgba(c, (0.55, 0.50, 0.42) if kind == 'soldier' else (0.62, 0.52, 0.34), a)
        c.rectangle(-32, -205, 64, 110); c.fill()
        rgba(c, (0.25, 0.22, 0.18), 0.6 * a); c.set_line_width(2)
        for r in range(6):
            yy = -195 + r * 18
            for k in range(4):
                c.arc(-24 + k * 16, yy, 8, 0, math.pi); c.stroke()
        rgba(c, dk, a); c.move_to(-40, -95); c.line_to(40, -95); c.line_to(48, -5); c.line_to(-48, -5); c.close_path(); c.fill()
        if kind == 'yue':
            rgba(c, (0.62, 0.10, 0.08), a)
            c.move_to(-26, -205); c.curve_to(-60, -120, -70, -40, -78, 20); c.line_to(-30, 0); c.line_to(-20, -200); c.close_path(); c.fill()
    # round collar + belt
    rgba(c, dk, a); c.arc(0, -206, 17, 0, math.pi); c.fill()
    rgba(c, (0.12, 0.10, 0.08) if not soldier else (0.75, 0.6, 0.3), a); c.rectangle(-34, -118, 68, 9); c.fill()
    rgba(c, GOLD, a); c.rectangle(-8, -120, 16, 13); c.fill()
    # arms
    rgba(c, dk, a); c.set_line_width(20); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if pose in ('raise', 'point'):
        c.move_to(18, -195); c.line_to(52, -240 if pose == 'raise' else -190); c.line_to(80, -285 if pose == 'raise' else -195); c.stroke()
        rgba(c, SKIN2, a); c.arc(84, -290 if pose == 'raise' else -195, 9, 0, 6.283); c.fill()
    elif pose == 'cry':
        c.move_to(18, -195); c.line_to(40, -150); c.line_to(22, -232); c.stroke()
    elif bow > 0 or pose == 'hold':
        c.move_to(18, -195); c.line_to(42, -150); c.line_to(60, -150); c.stroke()
        rgba(c, dk, a); c.move_to(40, -168); c.line_to(72, -160); c.line_to(66, -120); c.line_to(36, -130); c.close_path(); c.fill()  # wide sleeve
    else:
        c.move_to(16, -195); c.line_to(26, -130); c.line_to(24, -96); c.stroke()
        c.move_to(26, -150); c.line_to(44, -96); c.line_to(18, -92); c.line_to(16, -150); c.fill()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    # neck + head (profile, facing +x)
    rgba(c, SKIN2, a); c.rectangle(-6, -232, 13, 26); c.fill()
    c.arc(2, -250, 21, 0, 6.283); c.fill()
    c.move_to(21, -256); c.line_to(30, -244); c.line_to(21, -240); c.close_path(); c.fill()
    rgba(c, (0.12, 0.08, 0.06), 0.8 * a); c.arc(14, -253, 2.2, 0, 6.283); c.fill()
    # headwear
    rgba(c, HAT, a)
    if kind in ('official', 'official2', 'emperor'):
        c.move_to(-20, -258); c.line_to(22, -258); c.line_to(20, -284); c.line_to(6, -296); c.line_to(-16, -292); c.line_to(-22, -276); c.close_path(); c.fill()
        c.rectangle(-120, -272, 240, 5); c.fill()          # 直脚幞头 long wings
        if kind == 'emperor':
            rgba(c, GOLD, a); c.rectangle(-20, -262, 42, 4); c.fill()
    elif kind in ('soldier', 'yue'):
        rgba(c, (0.48, 0.45, 0.40) if kind == 'soldier' else (0.66, 0.55, 0.32), a)
        c.arc(2, -258, 24, math.pi, 2 * math.pi); c.fill(); c.rectangle(-24, -260, 18, 26); c.fill()
        rgba(c, (0.75, 0.15, 0.1), a); c.move_to(2, -282); c.curve_to(-10, -310, -26, -300, -30, -292); c.line_to(2, -288); c.fill()
    elif kind == 'mingsoldier':
        rgba(c, (0.40, 0.38, 0.36), a); c.arc(2, -262, 22, math.pi, 2 * math.pi); c.fill()
        c.save(); c.translate(2, -262); c.scale(40, 6); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
        rgba(c, (0.80, 0.15, 0.10), a); c.move_to(2, -284); c.line_to(-6, -306); c.line_to(10, -306); c.close_path(); c.fill()
    elif kind == 'scout':
        rgba(c, (0.62, 0.55, 0.42), a); c.arc(0, -258, 23, math.pi * 0.9, 2.1 * math.pi); c.fill()
        c.move_to(-22, -258); c.line_to(-30, -228); c.line_to(-12, -236); c.close_path(); c.fill()
    elif kind in ('mongol', 'mongol2'):
        rgba(c, (0.55, 0.20, 0.16) if kind == 'mongol' else (0.30, 0.22, 0.18), a)
        c.move_to(-22, -262); c.line_to(2, -304); c.line_to(26, -262); c.close_path(); c.fill()
        rgba(c, (0.70, 0.60, 0.45), a); c.rectangle(-26, -266, 54, 12); c.fill()
        rgba(c, HAT, a); c.set_line_width(5); c.move_to(-16, -250); c.line_to(-22, -214); c.stroke()
    elif kind == 'jurchen':
        rgba(c, (0.16, 0.14, 0.14), a); c.arc(2, -262, 21, math.pi, 2 * math.pi); c.fill()
        c.move_to(-26, -262); c.line_to(30, -262); c.line_to(24, -272); c.line_to(-20, -272); c.close_path(); c.fill()
        rgba(c, (0.85, 0.15, 0.10), a); c.arc(2, -284, 6, 0, 6.283); c.fill()
        rgba(c, HAT, a); c.set_line_width(5); c.move_to(-18, -252); c.curve_to(-30, -220, -26, -190, -34, -150); c.stroke()
    elif kind == 'mingoff':
        c.move_to(-20, -256); c.line_to(22, -256); c.line_to(20, -286); c.line_to(-18, -286); c.close_path(); c.fill()
        for sg in (-1, 1):
            c.save(); c.translate(sg * 34, -270); c.scale(16, 7); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    elif kind == 'mingemp':
        c.move_to(-20, -256); c.line_to(22, -256); c.line_to(20, -284); c.curve_to(10, -296, -10, -296, -18, -284); c.close_path(); c.fill()
        for sg in (-1, 1):
            c.save(); c.translate(-6 + sg * 12, -290); c.rotate(sg * 0.3); c.scale(7, 16); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    elif kind in ('eunuch', 'eunuch2'):
        c.move_to(-22, -256); c.line_to(24, -256); c.line_to(22, -280); c.curve_to(12, -296, -12, -296, -20, -282); c.close_path(); c.fill()
        c.move_to(-22, -262); c.line_to(-40, -250); c.line_to(-38, -242); c.line_to(-18, -252); c.close_path(); c.fill()
    elif kind == 'doctor':
        c.move_to(-22, -254); c.line_to(24, -254); c.line_to(28, -300); c.line_to(-26, -300); c.close_path(); c.fill()
    elif kind == 'tongshi':
        c.arc(2, -262, 22, math.pi, 2 * math.pi); c.fill(); c.rectangle(-26, -264, 56, 6); c.fill()
    elif kind == 'kid':
        c.arc(-10, -272, 9, 0, 6.283); c.fill(); c.arc(16, -272, 9, 0, 6.283); c.fill()
    elif kind == 'bare':
        pass
    else:  # courier / commoner: soft 幞头 with hanging ribbons
        c.move_to(-21, -254); c.line_to(22, -258); c.curve_to(20, -286, -18, -290, -21, -254); c.fill()
        c.set_line_width(5); c.move_to(-18, -262); c.curve_to(-34, -250, -38, -232, -44, -214); c.stroke()
    c.restore()


def song_hall(c, x, yf, s=1.0, a=1.0, glow=0.0, n=5):
    """Song palace hall: platform, red columns, lattice, bracket band, gentle curved roof"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    w = n * 110
    rgba(c, (0.62, 0.58, 0.52), a); c.rectangle(-w / 2 - 70, -50, w + 140, 50); c.fill()
    rgba(c, (0.45, 0.42, 0.38), a); c.rectangle(-w / 2 - 70, -50, w + 140, 8); c.fill()
    for k in range(5):
        rgba(c, (0.50, 0.47, 0.42), a); c.rectangle(-60 + k * 24 - 0, -50 + k * 10, 120 - k * 48 + 0 if False else 0, 0)
    # wall + lattice
    rgba(c, (0.22, 0.16, 0.12), a); c.rectangle(-w / 2, -300, w, 250); c.fill()
    for k in range(n):
        xx = -w / 2 + k * 110 + 14
        gl = glow * (0.6 + 0.4 * math.sin(k * 1.7))
        rgba(c, lerpc((0.36, 0.26, 0.17), (1.0, 0.80, 0.45), gl), a); c.rectangle(xx, -280, 82, 200); c.fill()
        rgba(c, (0.22, 0.14, 0.09), a); c.set_line_width(3)
        for j in range(1, 4):
            c.move_to(xx + j * 20.5, -280); c.line_to(xx + j * 20.5, -80)
        for j in range(1, 9):
            c.move_to(xx, -280 + j * 22); c.line_to(xx + 82, -280 + j * 22)
        c.stroke()
    for k in range(n + 1):
        rgba(c, (0.66, 0.14, 0.10), a); c.rectangle(-w / 2 - 8 + k * 110, -310, 16, 260); c.fill()
    # beam + brackets
    rgba(c, (0.50, 0.12, 0.09), a); c.rectangle(-w / 2 - 20, -330, w + 40, 24); c.fill()
    for k in range(n * 2 + 1):
        bx = -w / 2 - 10 + k * 55
        rgba(c, (0.20, 0.35, 0.32), a); c.rectangle(bx - 12, -352, 24, 22); c.fill()
        rgba(c, GOLD, 0.8 * a); c.rectangle(bx - 16, -356, 32, 5); c.fill()
    # roof (Song: gentle concave, wide eaves, low pitch)
    rw = w / 2 + 150
    rgba(c, (0.18, 0.19, 0.22), a)
    c.move_to(-rw, -350); c.curve_to(-rw + 60, -365, -w / 2, -385, -w / 2 + 40, -420)
    c.line_to(w / 2 - 40, -420); c.curve_to(w / 2, -385, rw - 60, -365, rw, -350)
    c.line_to(rw - 30, -372); c.line_to(-rw + 30, -372); c.close_path(); c.fill()
    c.move_to(-w / 2 + 40, -420); c.curve_to(-w / 4, -455, w / 4, -455, w / 2 - 40, -420); c.close_path(); c.fill()
    rgba(c, (0.30, 0.31, 0.35), a); c.set_line_width(2)
    for k in range(18):
        xx = -rw + 40 + k * (2 * rw - 80) / 17
        c.move_to(xx, -360); c.line_to(xx * 0.8, -425); c.stroke()
    rgba(c, (0.12, 0.12, 0.14), a); c.rectangle(-w / 2 + 30, -430, w - 60, 12); c.fill()
    for sg in (-1, 1):  # 鸱吻
        c.save(); c.translate(sg * (w / 2 - 34), -430); c.scale(sg, 1)
        c.move_to(0, 0); c.curve_to(10, -30, 30, -44, 18, -60); c.curve_to(36, -50, 34, -20, 22, 0); c.close_path(); c.fill()
        c.restore()
    rgba(c, GOLD, 0.6 * a); c.rectangle(-rw, -352, 2 * rw, 3); c.fill()
    c.restore()


def plaque2(c, x, y, s=1.0, a=1.0, glow=0.0, rot=0.0, txt=True, T=0):
    """朱漆金字木牌 — '御前文字不得入铺' (《长编》卷339)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if glow > 0:
        spot(c, 0, 0, 360, glow * a, (1, 0.8, 0.4))
    rgba(c, (0, 0, 0), 0.45 * a); rrect(c, -64, -196, 140, 400, 10); c.fill()
    g = cairo.LinearGradient(-70, 0, 70, 0)
    g.add_color_stop_rgba(0, 0.50, 0.08, 0.06, a); g.add_color_stop_rgba(0.35, 0.80, 0.17, 0.11, a); g.add_color_stop_rgba(1, 0.46, 0.07, 0.05, a)
    c.set_source(g); rrect(c, -70, -200, 140, 400, 10); c.fill()
    rgba(c, GOLDL, a); c.set_line_width(4); rrect(c, -56, -186, 112, 372, 6); c.stroke()
    if txt:
        for k, ch in enumerate("御前文字不得入铺"):
            text2(c, ch, 0, -150 + k * 44, 36, 99, (1.0, 0.86, 0.45), a, 'c', fam=FONT_B)
    # shine sweep
    sh = (T * 0.5) % 2.0
    if sh < 1:
        xx = -140 + 280 * sh
        g2 = cairo.LinearGradient(xx - 40, 0, xx + 40, 0)
        g2.add_color_stop_rgba(0, 1, 1, 1, 0); g2.add_color_stop_rgba(0.5, 1, 0.95, 0.8, 0.28 * a); g2.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.set_source(g2); rrect(c, -70, -200, 140, 400, 10); c.fill()
    c.restore()


def goldtablet(c, x, y, s=1.0, a=1.0, T=0):
    """the imagined solid-gold plaque"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    g = cairo.LinearGradient(-60, -150, 60, 150)
    g.add_color_stop_rgba(0, 1, 0.88, 0.5, a); g.add_color_stop_rgba(0.5, 0.80, 0.58, 0.20, a); g.add_color_stop_rgba(1, 1, 0.85, 0.45, a)
    c.set_source(g); rrect(c, -60, -150, 120, 300, 30); c.fill()
    rgba(c, (0.55, 0.38, 0.12), a); c.set_line_width(4); rrect(c, -48, -138, 96, 276, 22); c.stroke()
    text2(c, "令", 0, 24, 70, 99, (0.55, 0.36, 0.10), a, 'c', fam=FONT_B)
    c.restore()


def horse2(c, x, yf, s=1.0, T=0, a=1.0, face=1, rider=True, col=(0.30, 0.20, 0.13)):
    """slender galloping horse with Song courier"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    g = T * 13
    lc = tuple(v * 0.75 for v in col)
    rgba(c, lc, a); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for lx, ph in ((-80, 0), (-58, 2.4), (62, 1.0), (84, 3.4)):
        sw = math.sin(g + ph) * 30
        c.move_to(lx, -110); c.line_to(lx + sw * 0.8, -58); c.line_to(lx + sw * 0.4 - 6, -6); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    bob = math.sin(g * 2) * 4
    c.translate(0, bob)
    rgba(c, col, a)
    c.move_to(-110, -140); c.curve_to(-60, -170, 60, -165, 100, -150); c.curve_to(118, -130, 110, -100, 90, -96)
    c.curve_to(30, -90, -60, -92, -100, -100); c.curve_to(-125, -110, -124, -132, -110, -140); c.close_path(); c.fill()
    c.move_to(70, -150); c.curve_to(110, -200, 130, -230, 150, -238); c.line_to(196, -212); c.line_to(186, -196)
    c.line_to(150, -200); c.curve_to(130, -160, 115, -130, 98, -110); c.close_path(); c.fill()
    rgba(c, (0.08, 0.06, 0.05), a)
    c.move_to(146, -238); c.curve_to(120, -220, 100, -180, 82, -150); c.line_to(96, -150); c.curve_to(110, -185, 128, -215, 152, -232); c.fill()
    c.move_to(-112, -132); c.curve_to(-150, -120 + 6 * math.sin(g), -170, -100, -180, -80 + 8 * math.sin(g)); c.set_line_width(12); c.stroke()
    rgba(c, (0.4, 0.1, 0.08), a); c.rectangle(-30, -168, 60, 14); c.fill()
    if rider:
        c.save(); c.translate(-6, -150); c.rotate(0.18)
        sperson(c, 0, 0, 0.48, rider if isinstance(rider, str) else 'courier', a, 1, 'stand')
        c.restore()
    c.restore()


def tent(c, x, yf, s=1.0, a=1.0, col=(0.85, 0.74, 0.52), flag=REDL, T=0):
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, col, a); c.move_to(-60, 0); c.line_to(0, -70); c.line_to(60, 0); c.close_path(); c.fill()
    rgba(c, tuple(v * 0.6 for v in col), a); c.move_to(-14, 0); c.line_to(0, -40); c.line_to(14, 0); c.close_path(); c.fill()
    rgba(c, (0.3, 0.2, 0.12), a); c.rectangle(-2, -110, 4, 42); c.fill()
    rgba(c, flag, a); c.move_to(2, -110); c.line_to(34 + 4 * math.sin(T * 6), -100); c.line_to(2, -90); c.close_path(); c.fill()
    c.restore()


def camp(c, x, y, s=1.0, a=1.0, T=0, flag=REDL, col=(0.90, 0.78, 0.54), glow=0.0):
    if a <= 0: return
    if glow > 0: spot(c, x, y - 30 * s, 160 * s, glow * a)
    tent(c, x - 50 * s, y, 0.6 * s, a, col, flag, T); tent(c, x + 50 * s, y, 0.6 * s, a, col, flag, T + 1)
    tent(c, x, y + 12 * s, 0.8 * s, a, col, flag, T + 2)


def mappalace(c, x, y, s=1.0, a=1.0, glow=0.0):
    if a <= 0: return
    if glow > 0: spot(c, x, y - 30 * s, 160 * s, glow * a)
    song_hall(c, x, y, 0.16 * s, a, 0.6, 3)


def maplabel(c, s, x, y, a=1.0, col=TXT, size=30):
    if a <= 0: return
    text2(c, s, x, y, size, 99, col, a, 'c')


def dotted(c, pts, prog, a=1.0, col=(1.0, 0.85, 0.55), T=0):
    if a <= 0 or prog <= 0: return
    pp = partial(pts, prog)
    rgba(c, col, 0.9 * a); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_dash([0.1, 16], -T * 30)
    c.move_to(*pp[0]); [c.line_to(*q) for q in pp[1:]]; c.stroke(); c.set_dash([])
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    return pp[-1]


def ruler(c, x, y, L, a=1.0, prog=1.0):
    if a <= 0: return
    w = L * prog
    rgba(c, (0.85, 0.72, 0.48), a); c.rectangle(x, y, w, 60); c.fill()
    rgba(c, (0.35, 0.25, 0.15), a); c.set_line_width(2)
    for k in range(0, 33):
        xx = x + k * L / 31
        if xx > x + w: break
        h = 30 if k % 10 == 0 else (20 if k % 5 == 0 else 12)
        c.move_to(xx, y); c.line_to(xx, y + h); c.stroke()

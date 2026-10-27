import math, random, json
from core import *
from sets import vgrad, lantern
from fx import flag, t_ladder

MAPJ = json.load(open('/workspace/work/diaoyu_boyi/maps.json'))
_IMG = {}


def img(name):
    if name not in _IMG:
        _IMG[name] = cairo.ImageSurface.create_from_png('/workspace/work/diaoyu_boyi/%s.png' % name)
    return _IMG[name]


def mapview(c, name, cx, cy, vw, a=1.0, dark=0.15):
    """draw map image so that source point (cx,cy) is screen centre and vw source px span screen width"""
    s = W / vw
    c.save(); c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-cx, -cy)
    c.set_source_surface(img(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a)
    c.restore()
    if dark:
        c.set_source_rgba(0.04, 0.03, 0.02, dark); c.paint()
    return lambda px, py: (W / 2 + (px - cx) * s, H / 2 + (py - cy) * s)


def campath(t, keys):
    """keys: list of (t, cx, cy, vw); eased interpolation"""
    if t <= keys[0][0]:
        return keys[0][1:]
    for k0, k1 in zip(keys[:-1], keys[1:]):
        if t <= k1[0]:
            u = ease((t - k0[0]) / (k1[0] - k0[0]))
            vw = math.exp(lerp(math.log(k0[3]), math.log(k1[3]), u))
            return lerp(k0[1], k1[1], u), lerp(k0[2], k1[2], u), vw
    return keys[-1][1:]


def goldlabel(c, s_, x, y, a=1.0, size=48, col=GOLDL):
    """map label: dark box + white text + coloured accent bar (high contrast on light terrain)"""
    if a <= 0.01:
        return
    w = tw(c, s_, size)
    bw, bh = w + size * 0.9, size * 1.45
    x0, y0 = x - bw / 2, y - size * 1.08
    rr(c, x0 + 4, y0 + 6, bw, bh, 10); c.set_source_rgba(0, 0, 0, 0.35 * a); c.fill()
    rr(c, x0, y0, bw, bh, 10); c.set_source_rgba(0.07, 0.07, 0.09, 0.88 * a); c.fill_preserve()
    rgba(c, col, 0.95 * a); c.set_line_width(2.5); c.stroke()
    c.rectangle(x0 + 10, y0 + bh - 7, bw - 20, 4); rgba(c, col, a); c.fill()
    text(c, s_, x, y, size, WHITE, a, align='c', shadow=0)


def pin(c, x, y, t, t0, col=GOLDL, r=14):
    p = back(seg(t, t0, t0 + 0.35))
    if p <= 0.01:
        return
    rec(t0, 'pop')
    glow(c, x, y, 60 * p, col, 0.5)
    c.arc(x, y, (r + 5) * p, 0, TAU); rgba(c, WHITE); c.fill()
    c.arc(x, y, r * p, 0, TAU); rgba(c, col); c.fill()


def dashroute(c, pts, prog, col=(1, 1, 1), w=7, a=1.0, T=0.0):
    if prog <= 0 or len(pts) < 2:
        return
    L = [0.0]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L.append(L[-1] + math.hypot(x1 - x0, y1 - y0))
    tot = L[-1] * prog
    c.move_to(*pts[0]); end = pts[0]
    for i in range(1, len(pts)):
        if L[i] <= tot:
            c.line_to(*pts[i]); end = pts[i]
        else:
            u = (tot - L[i - 1]) / max(L[i] - L[i - 1], 1e-6)
            end = (lerp(pts[i - 1][0], pts[i][0], u), lerp(pts[i - 1][1], pts[i][1], u)); c.line_to(*end); break
    path = c.copy_path(); c.new_path()
    for lw, al in ((w * 3.2, 0.18), (w, 1.0)):
        c.append_path(path); c.set_dash([22, 14], -T * 40); rgba(c, col, a * al); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.set_dash([]); c.set_line_cap(cairo.LINE_CAP_BUTT)
    # arrow head
    if len(pts) >= 2:
        x0, y0 = pts[0]
        ang = math.atan2(end[1] - (pts[-2][1] if prog >= 1 else y0), end[0] - (pts[-2][0] if prog >= 1 else x0))
        c.move_to(end[0] + math.cos(ang) * 22, end[1] + math.sin(ang) * 22)
        c.line_to(end[0] + math.cos(ang + 2.4) * 22, end[1] + math.sin(ang + 2.4) * 22)
        c.line_to(end[0] + math.cos(ang - 2.4) * 22, end[1] + math.sin(ang - 2.4) * 22); c.close_path(); rgba(c, col, a); c.fill()


# ------------------------------------------------------------------ illustrated terrain
ROCK = (0.46, 0.30, 0.20)
ROCKL = (0.66, 0.46, 0.28)
RIVER = (0.26, 0.48, 0.70)


def river_band(c, T, y, h=150, a=1.0):
    vgrad(c, y, y + h, (0.22, 0.42, 0.64), (0.14, 0.28, 0.46))
    for k in range(4):
        yy = y + 20 + k * h / 4
        c.move_to(0, yy)
        for x in range(0, W + 40, 40):
            c.line_to(x, yy + math.sin(x * 0.012 + T * 2 + k) * 6)
        rgba(c, (0.70, 0.86, 0.98), 0.35 * a); c.set_line_width(3); c.stroke()


def fortress(c, x, yb, s=1.0, a=1.0, T=0.0, walls=1.0, flags=True, inner=0.0, top_w=760):
    """mesa with cliffs; walls on the rim. yb = river level. top surface at yb-420*s"""
    c.save(); c.translate(x, yb); c.scale(s, s)
    tw_ = top_w / 2
    top = -420
    c.move_to(-tw_ - 260, 0)
    c.curve_to(-tw_ - 160, -60, -tw_ - 60, -200, -tw_ - 20, top + 30)
    c.line_to(-tw_, top); c.line_to(tw_, top); c.line_to(tw_ + 30, top + 40)
    c.curve_to(tw_ + 70, -200, tw_ + 160, -60, tw_ + 260, 0); c.close_path()
    rgba(c, ROCK, a); c.fill_preserve(); rgba(c, dk(ROCK, 0.6), a); c.set_line_width(4); c.stroke()
    # cliff striations
    rnd = random.Random(3)
    rgba(c, dk(ROCK, 0.75), a); c.set_line_width(3)
    for i in range(18):
        xx = rnd.uniform(-tw_ - 120, tw_ + 120); y0 = rnd.uniform(top + 30, -120)
        c.move_to(xx, y0); c.line_to(xx + rnd.uniform(-20, 20), y0 + rnd.uniform(60, 140)); c.stroke()
    # lit rim
    c.move_to(-tw_ - 20, top + 30); c.line_to(-tw_, top); c.line_to(tw_, top); c.line_to(tw_ + 30, top + 40)
    rgba(c, (0.95, 0.75, 0.42), a); c.set_line_width(5); c.stroke()
    # green top
    c.rectangle(-tw_, top - 16, top_w, 18); rgba(c, (0.40, 0.55, 0.30), a); c.fill()
    if inner > 0.01:
        # fields + pond
        for i in range(5):
            c.rectangle(-tw_ + 40 + i * 120, top - 30, 100, 16); rgba(c, (0.62, 0.72, 0.32), a * inner); c.fill()
        ell(c, tw_ - 150, top - 22, 90, 14); rgba(c, (0.40, 0.70, 0.92), a * inner); c.fill()
    if walls > 0.01:
        n = int(18 * walls)
        for i in range(n):
            wx = -tw_ + i * top_w / 18
            c.rectangle(wx, top - 70, top_w / 18 - 4, 54); rgba(c, (0.74, 0.66, 0.54), a); c.fill()
            c.rectangle(wx + 6, top - 88, top_w / 36, 18); c.fill()
        if walls >= 1:
            # gate tower
            for gx in (-tw_ + 60, tw_ - 80):
                c.rectangle(gx - 46, top - 150, 92, 82); rgba(c, (0.62, 0.22, 0.16), a); c.fill()
                c.move_to(gx - 70, top - 150); c.curve_to(gx - 30, top - 165, gx - 10, top - 195, gx, top - 200)
                c.curve_to(gx + 10, top - 195, gx + 30, top - 165, gx + 70, top - 150); c.close_path(); rgba(c, (0.22, 0.22, 0.28), a); c.fill()
            if flags:
                for fx_ in (-tw_ + 200, 0, tw_ - 240):
                    flag(c, fx_, top - 70, 0.7, (0.86, 0.20, 0.16), a, T, pole=160)
    c.restore()


def mesa_bg(c, T, sky=((0.10, 0.08, 0.14), (0.42, 0.26, 0.22))):
    vgrad(c, 0, 860, sky[0], sky[1])
    # far hills
    for k, col in enumerate(((0.20, 0.14, 0.14), (0.26, 0.18, 0.15))):
        c.move_to(0, 860)
        for x in range(0, W + 60, 60):
            c.line_to(x, 640 + k * 70 + math.sin(x * 0.004 + k * 2) * 40 + math.sin(x * 0.011 + k) * 20)
        c.line_to(W, 860); c.close_path(); rgba(c, col); c.fill()
    dust(c, T, 4, 30, (1, 0.85, 0.6), 0.25)


def mongol(c, x, yf, s, T, expr='calm', pose='hold', walk=0.0, prop=None, name=None, pre=''):
    from chibi2 import chibi
    chibi(c, x, yf, s, hatk='khitan', robe=(0.45, 0.30, 0.22), collar='round', expr=expr, pose=pose, T=T, walk=walk, prop=prop,
          name=name, label_pre=pre)


def mengge(c, x, yf, s, T, expr='calm', pose='hold', sw=False, shake=0.0, name='蒙哥', pre='大汗'):
    from chibi2 import chibi
    chibi(c, x, yf, s, hatk='yuan', robe=(0.25, 0.32, 0.52), collar='round', patch='dragon', expr=expr, pose=pose, T=T,
          sw=sw, shake=shake, name=name, label_pre=pre)


def cavalry(c, x, yf, s, T, run=0.0):
    from fx import horse_rider
    horse_rider(c, x, yf, s, 1.0, run, flagc=(0.30, 0.36, 0.55))


def mast_tower(c, x, yb, s=1.0, a=1.0, T=0.0, climb=0.0, fling=0.0):
    c.save(); c.translate(x, yb); c.scale(s, s)
    wood = (0.55, 0.36, 0.20)
    for lx in (-110, 110):
        c.move_to(lx, 0); c.line_to(lx * 0.6, -330); rgba(c, wood, a); c.set_line_width(16); c.stroke()
    for k in range(5):
        y = -k * 70
        c.move_to(-110 + k * 9, y); c.line_to(110 - k * 9, y - 60); c.set_line_width(7); c.stroke()
        c.move_to(110 - k * 9, y); c.line_to(-110 + k * 9, y - 60); c.stroke()
    c.rectangle(-90, -360, 180, 34); rgba(c, dk(wood, 0.8), a); c.fill()
    c.move_to(0, -360); c.line_to(0, -760); rgba(c, wood, a); c.set_line_width(12); c.stroke()
    # climber
    if fling <= 0.01:
        cy = lerp(-380, -730, climb)
        c.arc(14, cy - 40, 20, 0, TAU); rgba(c, (0.99, 0.96, 0.92), a); c.fill()
        c.arc(14, cy - 44, 21, math.pi * 1.05, math.pi * 1.95); c.close_path(); rgba(c, (0.40, 0.28, 0.20), a); c.fill()
        rr(c, 0, cy - 20, 28, 44, 8); rgba(c, (0.45, 0.30, 0.22), a); c.fill()
    else:
        fx_ = -fling * 900; fy = -730 - math.sin(fling * math.pi) * 260 + fling * 300
        c.save(); c.translate(fx_, fy); c.rotate(fling * 9)
        c.arc(0, -20, 20, 0, TAU); rgba(c, (0.99, 0.96, 0.92), a); c.fill()
        rr(c, -14, 0, 28, 44, 8); rgba(c, (0.45, 0.30, 0.22), a); c.fill()
        c.restore()
    c.restore()


def trebuchet(c, x, yb, s=1.0, a=1.0, fire=0.0):
    """Song 炮 (traction trebuchet). fire 0..1 arm swing"""
    c.save(); c.translate(x, yb); c.scale(s, s)
    wood = (0.58, 0.38, 0.22)
    for lx in (-60, 60):
        c.move_to(lx * 1.6, 0); c.line_to(0, -200); rgba(c, wood, a); c.set_line_width(16); c.stroke()
    c.rectangle(-120, -14, 240, 14); rgba(c, dk(wood, 0.8), a); c.fill()
    ang = lerp(0.9, -1.1, ease(fire))
    c.save(); c.translate(0, -200); c.rotate(ang)
    c.move_to(-90, 0); c.line_to(220, 0); rgba(c, wood, a); c.set_line_width(14); c.stroke()
    if fire < 0.6:
        c.arc(220, 20, 22, 0, TAU); rgba(c, (0.62, 0.60, 0.58), a); c.fill()
    for k in range(4):
        c.move_to(-90 + k * 6, 0); c.line_to(-100 + k * 10, 120); rgba(c, (0.85, 0.75, 0.55), a); c.set_line_width(3); c.stroke()
    c.restore()
    c.arc(0, -200, 12, 0, TAU); rgba(c, (0.3, 0.2, 0.12), a); c.fill()
    c.restore()


def bigfish(c, x, y, s=1.0, a=1.0, rot=0.0, T=0.0):
    c.save(); c.translate(x, y); c.rotate(rot + math.sin(T * 6) * 0.08); c.scale(s, s)
    c.move_to(-120, 0); c.curve_to(-60, -70, 70, -60, 110, 0); c.curve_to(70, 60, -60, 70, -120, 0); c.close_path()
    fill2(c, (0.80, 0.84, 0.88), a, 3, 0.7)
    c.move_to(-110, 0); c.line_to(-180, -50); c.line_to(-170, 0); c.line_to(-180, 50); c.close_path(); fill2(c, (0.70, 0.74, 0.80), a, 3, 0.7)
    c.arc(70, -12, 9, 0, TAU); rgba(c, (0.14, 0.10, 0.09), a); c.fill()
    rgba(c, (0.62, 0.66, 0.72), a); c.set_line_width(3)
    for k in range(4):
        c.arc(-20 + k * 24, 0, 26, -0.9, 0.9); c.stroke()
    c.restore()


def bread(c, x, y, n=8, s=1.0, a=1.0):
    for i in range(n):
        bx = x + (i % 4) * 70 * s - 105 * s; by = y - (i // 4) * 34 * s
        ell(c, bx, by, 36 * s, 18 * s); fill2(c, (0.96, 0.92, 0.80), a, 2, 0.75)


def letter(c, x, y, s=1.0, a=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -110, -70, 220, 140, 6); fill2(c, (0.96, 0.90, 0.76), a, 3, 0.7)
    rgba(c, (0.4, 0.3, 0.2), a); c.set_line_width(4)
    for k in range(4):
        c.move_to(70 - k * 40, -50); c.line_to(70 - k * 40, 50); c.stroke()
    c.restore()


def rain(c, T, a=0.6, n=140, seed=3):
    rnd = random.Random(seed)
    rgba(c, (0.75, 0.85, 1.0), a); c.set_line_width(2.5)
    for i in range(n):
        x = rnd.random() * (W + 200); sp = rnd.uniform(900, 1400)
        y = (rnd.random() * H + T * sp) % (H + 100) - 50
        c.move_to(x - y * 0.15, y); c.line_to(x - y * 0.15 - 12, y + 46); c.stroke()


def timeline(c, t, t0, x0, x1, y, items, hl=None, a=1.0):
    p = eout(seg(t, t0, t0 + 0.6))
    c.move_to(x0, y); c.line_to(lerp(x0, x1, p), y); rgba(c, GOLD, a); c.set_line_width(6); c.stroke()
    for i, (frac, top, sub, col) in enumerate(items):
        tt = t0 + 0.4 + i * 0.35
        q = pop(t, tt, 0.3)
        if q <= 0.01:
            continue
        rec(tt, 'pop')
        x = lerp(x0, x1, frac)
        c.arc(x, y, 14 * q, 0, TAU); rgba(c, col, a); c.fill()
        text(c, top, x, y - 34, 44, col, a * q, align='c')
        if sub:
            text(c, sub, x, y + 64, 36, WHITE, a * q, align='c')


def shore(c, y=1000):
    c.move_to(0, y)
    for x in range(0, W + 60, 60):
        c.line_to(x, y + math.sin(x * 0.01) * 8)
    c.line_to(W, H); c.line_to(0, H); c.close_path(); rgba(c, (0.36, 0.26, 0.18)); c.fill()
    c.move_to(0, y)
    for x in range(0, W + 60, 60):
        c.line_to(x, y + math.sin(x * 0.01) * 8)
    rgba(c, (0.62, 0.48, 0.32)); c.set_line_width(4); c.stroke()

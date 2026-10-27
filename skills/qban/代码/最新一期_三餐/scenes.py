from px import *

SCENES = []
NOTE = "画面为示意"


def scene(D, caps=(), src=None, sfx=(), cam=None, note=NOTE, ov=None):
    def deco(fn):
        s_ = ((src + "　") if src else "") + (note or "")
        SCENES.append(dict(D=D, caps=list(caps), src=s_.strip("　"), bg='none', spot=(960, 540, 800),
                           fn=fn, sfx=list(sfx), counter=None, cam=cam or (960, 540, 1.0, 1.0), cx=90, cy=80, ov=ov))
        return fn
    return deco


def C(c, x, yf, s, era, role, pose='stand', face=1, expr='calm', **kw):
    chibi(c, x, yf, s, era, role, pose, face, expr, **kw)


def wk(t, a, b, x0, x1):
    u = seg(t, a, b)
    return lerp(x0, x1, ease(u)), (t * 9 if 0 < u < 1 else None)


HANP = (0.55, 0.45, 0.32)     # peasant hemp
SHANG = (0.62, 0.42, 0.24)
QIRO = (0.55, 0.16, 0.12)
HX = (0.36, 0.44, 0.58)       # 韩信
PIAO = (0.58, 0.54, 0.48)
SONGB = (0.30, 0.42, 0.52)


# ------------------------------------------------------------------ quote scroll with 白话
def quote(c, t, t0, x, y, orig, bh, size=46, bsize=36, title='原文', t1=None):
    p = ease(seg(t, t0, t0 + 0.6))
    a = 1.0 - (seg(t, t1, t1 + 0.4) if t1 else 0.0)
    if p <= 0 or a <= 0: return
    tws = [tw(c, s_, size, FONT_X) for s_ in orig]
    fnt(c, bsize, FONT_B)
    bws = [c.text_extents(s_)[4] for s_ in bh]
    ww = max(max(tws), max(bws) if bws else 0) + 110
    hh = len(orig) * size * 1.45 + 40 + len(bh) * bsize * 1.42 + 60
    cw = ww * p
    c.save()
    rgba(c, (0, 0, 0), 0.4 * a); c.rectangle(x - cw / 2 + 10, y - hh / 2 + 12, cw, hh); c.fill()
    g = cairo.LinearGradient(0, y - hh / 2, 0, y + hh / 2)
    g.add_color_stop_rgba(0, 0.96, 0.91, 0.78, a); g.add_color_stop_rgba(1, 0.86, 0.78, 0.60, a)
    c.set_source(g); c.rectangle(x - cw / 2, y - hh / 2, cw, hh); c.fill()
    rgba(c, (0.55, 0.30, 0.15), 0.6 * a); c.set_line_width(2); c.rectangle(x - cw / 2 + 12, y - hh / 2 + 12, cw - 24, hh - 24); c.stroke()
    for sx in (-1, 1):
        g = cairo.LinearGradient(0, y - hh / 2 - 14, 0, y + hh / 2 + 14)
        g.add_color_stop_rgba(0, 0.30, 0.16, 0.08, a); g.add_color_stop_rgba(0.5, 0.55, 0.32, 0.16, a); g.add_color_stop_rgba(1, 0.30, 0.16, 0.08, a)
        c.set_source(g); rrect(c, x + sx * cw / 2 - 14, y - hh / 2 - 18, 28, hh + 36, 10); c.fill()
    c.rectangle(x - cw / 2, y - hh / 2, cw, hh); c.clip()
    yy = y - hh / 2 + 30 + size * 0.95
    left = x - max(tws) / 2
    for i, s_ in enumerate(orig):
        ink(c, s_, left, yy, size, (t - t0 - 0.5 - i * 0.4) * 1.6, a)
        yy += size * 1.45
    tb = t0 + 0.9 + len(orig) * 0.45
    fb = ease(seg(t, tb, tb + 0.35))
    if bh and fb > 0:
        rgba(c, (0.55, 0.30, 0.15), 0.5 * a * fb); c.rectangle(x - ww / 2 + 50, yy - size * 0.55, ww - 100, 2); c.fill()
        yy += 6
        bl = x - max(bws) / 2
        for i, s_ in enumerate(bh):
            f2 = ease(seg(t, tb + i * 0.35, tb + i * 0.35 + 0.35))
            fnt(c, bsize, FONT_B); rgba(c, (0.50, 0.10, 0.05), a * f2)
            c.move_to(bl, yy + bsize * 0.2); c.show_text(s_)
            yy += bsize * 1.42
    c.restore()
    if title and p > 0.6:
        seal(c, title, x - ww / 2 + 46, y - hh / 2 + 4, 0.42, a * fin(t, t0 + 0.4))


# ------------------------------------------------------------------ 时辰日晷 (motif)
BR = "子丑寅卯辰巳午未申酉戌亥"


def _ang(k):
    return math.pi / 2 + k * math.pi / 6


def sundial(c, x, y, r, t, sun=None, meals=(), ghost=(), a=1.0, hi=()):
    if a <= 0: return
    spot(c, x, y, r * 1.9, 0.6 * a)
    rgba(c, (0, 0, 0), 0.5 * a); c.arc(x + 8, y + 12, r, 0, 6.283); c.fill()
    c.move_to(x, y); c.arc(x, y, r, math.pi, 2 * math.pi); c.close_path()
    g = cairo.RadialGradient(x, y - r * 0.4, 10, x, y, r)
    g.add_color_stop_rgba(0, 0.46, 0.30, 0.14, a); g.add_color_stop_rgba(1, 0.22, 0.13, 0.07, a)
    c.set_source(g); c.fill()
    c.move_to(x, y); c.arc(x, y, r, 0, math.pi); c.close_path()
    g = cairo.RadialGradient(x, y + r * 0.4, 10, x, y, r)
    g.add_color_stop_rgba(0, 0.12, 0.15, 0.30, a); g.add_color_stop_rgba(1, 0.05, 0.06, 0.13, a)
    c.set_source(g); c.fill()
    for k in hi:
        rgba(c, LACQ, 0.75 * a); c.move_to(x, y); c.arc(x, y, r - 3, _ang(k) - math.pi / 12, _ang(k) + math.pi / 12); c.close_path(); c.fill()
    rgba(c, GOLD, a); c.set_line_width(5); c.arc(x, y, r, 0, 6.283); c.stroke()
    rgba(c, GOLD, 0.45 * a); c.set_line_width(2); c.arc(x, y, r * 0.70, 0, 6.283); c.stroke()
    for k in range(12):
        an = _ang(k - 0.5)
        c.move_to(x + r * 0.70 * math.cos(an), y + r * 0.70 * math.sin(an)); c.line_to(x + r * math.cos(an), y + r * math.sin(an)); c.stroke()
        an = _ang(k)
        text2(c, BR[k], x + r * 0.85 * math.cos(an), y + r * 0.85 * math.sin(an) + r * 0.055, r * 0.14, 99,
              (1, 0.92, 0.65) if k in hi else TXT, a, 'c', fam=FONT_X)
    if sun is not None:
        an = _ang(sun); sx, sy = x + r * 0.45 * math.cos(an), y + r * 0.45 * math.sin(an)
        rgba(c, GOLDL, 0.8 * a); c.set_line_width(5); c.move_to(x, y); c.line_to(sx, sy); c.stroke()
        day = math.sin(an) < 0.1
        spot(c, sx, sy, r * 0.35, a, (1, 0.8, 0.4) if day else (0.6, 0.7, 1.0))
        rgba(c, (1, 0.82, 0.40) if day else (0.85, 0.88, 1.0), a); c.arc(sx, sy, r * 0.075, 0, 6.283); c.fill()
    rgba(c, GOLDL, a); c.arc(x, y, r * 0.04, 0, 6.283); c.fill()
    for (k, lab) in ghost:
        an = _ang(k); bx, by = x + r * 1.20 * math.cos(an), y + r * 1.20 * math.sin(an)
        bowl(c, bx, by, 0.75, 0.35 * a, t, 0)
        text2(c, lab, bx, by + 70, 30, 99, (0.7, 0.66, 0.6), 0.6 * a, 'c', fam=FONT_B)
    for (k, lab, t0, col) in meals:
        if t < t0: continue
        p = back(seg(t, t0, t0 + 0.45))
        an = _ang(k); bx, by = x + r * 1.22 * math.cos(an), y + r * 1.22 * math.sin(an)
        c.save(); c.translate(bx, by); c.scale(max(p, 0.01), max(p, 0.01)); c.translate(-bx, -by)
        spot(c, bx, by, 120, a)
        bowl(c, bx, by - 6, 0.9, a, t, 1)
        lx, ly = bx + 72 * math.cos(an), by + 72 * math.sin(an) + 14
        if math.sin(an) < -0.8: lx, ly = bx + 95, by + 4
        text2(c, lab, lx, ly, 40, 99, col, a, 'c', fam=FONT_X)
        c.restore()


# ------------------------------------------------------------------ props
def mapbg(c, lon, lat, vw, dark=0.25):
    f = draw_map(c, lon, lat, vw)
    rgba(c, (0.02, 0.015, 0.01), dark); c.rectangle(-500, -500, W + 1000, H + 1000); c.fill()
    return f


def maptag(c, name, x, y, a=1.0, size=40, dot=True, glow=0.0):
    if a <= 0: return
    if dot:
        if glow > 0: spot(c, x, y, 120 * glow, a)
        rgba(c, GOLDL, a); c.arc(x, y, 11, 0, 6.283); c.fill(); rgba(c, DARK, a); c.arc(x, y, 4, 0, 6.283); c.fill()
    goldbar_label(c, name, x, y - 46, size, a)


def stars(c, t, a=1.0, n=60, ymax=600):
    if a <= 0: return
    for k in range(n):
        rr = random.Random(k * 13 + 5)
        x, y = rr.uniform(0, W), rr.uniform(20, ymax)
        rgba(c, (0.95, 0.92, 0.85), a * (0.35 + 0.35 * math.sin(t * 2 + k)))
        c.arc(x, y, rr.uniform(1, 2.6), 0, 6.283); c.fill()


def sunball(c, x, y, r=60, a=1.0, col=(1, 0.62, 0.30)):
    if a <= 0: return
    spot(c, x, y, r * 6, a, col)
    rgba(c, col, a); c.arc(x, y, r, 0, 6.283); c.fill()


def field(c, t, yb=900, x0=-100, x1=2020, a=1.0, grain=0.6):
    for k, x in enumerate(range(x0, x1, 46)):
        rice(c, x + 10 * math.sin(k), yb + 10, 70 + 15 * math.sin(k * 1.7), a * 0.8, 5 * math.sin(t * 1.5 + k * 0.4), grain)


def yardwall(c, x0, x1, yb, h=260, a=1.0):
    if a <= 0: return
    rgba(c, (0.30, 0.24, 0.18), a); c.rectangle(x0, yb - h, x1 - x0, h); c.fill()
    rgba(c, (0.36, 0.29, 0.22), a)
    for k in range(int((x1 - x0) / 90) + 1):
        c.rectangle(x0 + k * 90 + 4, yb - h + 30, min(82, max(0, x1 - x0 - k * 90 - 8)), h - 40)
    c.fill()
    rgba(c, (0.14, 0.11, 0.09), a); c.move_to(x0 - 30, yb - h); c.line_to(x1 + 30, yb - h); c.line_to(x1, yb - h - 40); c.line_to(x0, yb - h - 40); c.close_path(); c.fill()
    rgba(c, GOLD, 0.6 * a); c.set_line_width(2.5); c.move_to(x0 - 30, yb - h); c.line_to(x1 + 30, yb - h); c.stroke()


def fanggate(c, x, yb, close=0.0, a=1.0, label="坊门"):
    rgba(c, (0.03, 0.025, 0.02), a); c.rectangle(x - 110, yb - 300, 220, 300); c.fill()
    spot(c, x, yb - 120, 200, 0.6 * (1 - close) * a)
    for sg in (-1, 1):
        w_ = 110 * close
        rgba(c, (0.45, 0.12, 0.08), a); c.rectangle(x + sg * 110 - (w_ if sg > 0 else 0), yb - 300, w_, 300); c.fill()
        rgba(c, GOLD, 0.6 * a)
        for j in range(3):
            for i in range(2):
                if w_ > 30: c.arc(x + sg * (110 - 25 - i * 40 * close), yb - 240 + j * 90, 4, 0, 6.283); c.fill()
    for sg in (-1, 1):
        rgba(c, (0.40, 0.10, 0.07), a); c.rectangle(x + sg * 125 - 15, yb - 340, 30, 340); c.fill()
    rgba(c, (0.14, 0.10, 0.08), a); c.move_to(x - 190, yb - 330); c.line_to(x + 190, yb - 330); c.line_to(x + 150, yb - 400); c.line_to(x - 150, yb - 400); c.close_path(); c.fill()
    rgba(c, GOLD, 0.7 * a); c.set_line_width(2.5); c.move_to(x - 190, yb - 330); c.line_to(x + 190, yb - 330); c.stroke()
    tag(c, label, x, yb - 450, a, 34)


def chariot(c, x, yf, s, T, a=1.0, face=1, spin=True):
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    horse2(c, 300, 0, 0.95, T, a, 1, rider=False)
    horse2(c, 250, 8, 0.95, T + 0.3, a * 0.9, 1, rider=False, col=(0.24, 0.16, 0.10))
    rgba(c, (0.36, 0.20, 0.10), a); c.set_line_width(10); c.move_to(60, -120); c.curve_to(150, -140, 200, -150, 260, -150); c.stroke()
    c.restore()


def chariot_front(c, x, yf, s, T, a=1.0, face=1):
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    rgba(c, (0.40, 0.16, 0.08), a); rrect(c, -100, -170, 190, 80, 8); c.fill()
    rgba(c, GOLD, 0.8 * a); c.set_line_width(3); rrect(c, -100, -170, 190, 80, 8); c.stroke()
    wr = 78
    rgba(c, (0.20, 0.12, 0.07), a); c.set_line_width(10); c.arc(-10, -wr, wr, 0, 6.283); c.stroke()
    rgba(c, (0.50, 0.32, 0.16), a); c.set_line_width(5)
    for k in range(8):
        an = -T * 9 + k * math.pi / 4
        c.move_to(-10, -wr); c.line_to(-10 + wr * math.cos(an), -wr + wr * math.sin(an)); c.stroke()
    rgba(c, GOLD, a); c.arc(-10, -wr, 10, 0, 6.283); c.fill()
    c.restore()


def plastron(c, x, y, s, t, a=1.0, glow=0.0, crack=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    spot(c, 0, 0, 380, 0.7 * a)
    c.move_to(0, -220)
    c.curve_to(120, -220, 160, -140, 150, -40); c.line_to(170, -10); c.line_to(150, 20)
    c.curve_to(160, 140, 110, 210, 0, 215); c.curve_to(-110, 210, -160, 140, -150, 20)
    c.line_to(-170, -10); c.line_to(-150, -40); c.curve_to(-160, -140, -120, -220, 0, -220); c.close_path()
    g = cairo.RadialGradient(-30, -60, 20, 0, 0, 260)
    g.add_color_stop_rgba(0, 0.95, 0.88, 0.70, a); g.add_color_stop_rgba(1, 0.70, 0.58, 0.40, a)
    c.set_source(g); c.fill_preserve(); rgba(c, (0.40, 0.28, 0.16), a); c.set_line_width(4); c.stroke()
    rgba(c, (0.45, 0.32, 0.18), 0.6 * a); c.set_line_width(2)
    c.move_to(0, -215); c.line_to(0, 212); c.stroke()
    for yy in (-110, 0, 110):
        c.move_to(-150, yy + 10); c.curve_to(-60, yy - 10, 60, yy - 10, 150, yy + 10); c.stroke()
    # cracks 卜
    rgba(c, (0.20, 0.10, 0.05), a); c.set_line_width(3.5)
    for (cx, cy) in ((-80, -150), (60, -60), (-60, 60), (80, 140)):
        u = clamp(crack * 3 - (cx + 100) / 300)
        c.move_to(cx, cy - 34 * u); c.line_to(cx, cy + 34 * u); c.move_to(cx, cy); c.line_to(cx + 26 * u, cy - 14 * u); c.stroke()
    # glyph columns
    for (gx, txt) in ((95, "大食"), (-95, "小食")):
        if glow > 0: spot(c, gx, -10, 150, glow * a, (1, 0.85, 0.4))
        for j, ch in enumerate(txt):
            fnt(c, 62, FONT_X); ew = c.text_extents(ch)[4]
            col = lerpc((0.30, 0.15, 0.06), (0.85, 0.20, 0.08), glow)
            rgba(c, col, a); c.move_to(gx - ew / 2, -40 + j * 76); c.show_text(ch)
    c.restore()


def brazier(c, x, yf, t, a=1.0):
    rgba(c, (0.25, 0.20, 0.16), a); c.move_to(x - 70, yf - 90); c.line_to(x + 70, yf - 90); c.line_to(x + 50, yf); c.line_to(x - 50, yf); c.close_path(); c.fill()
    campfire(c, x, yf - 90, t, a, 0.9)


def growl(c, x, y, t, t0, a=1.0):
    u = seg(t, t0, t0 + 1.4)
    if u <= 0 or u >= 1: return
    al = a * math.sin(math.pi * u)
    rgba(c, GOLDL, al); c.set_line_width(4)
    for k in range(3):
        rr = 30 + k * 22 + 20 * u
        c.arc(x, y, rr, -0.6, 0.6); c.stroke()
    bubble(c, x + 110, y - 90, "咕噜……", al, 40)


def stall(c, x, yf, w=420, a=1.0, t=0, nb=3):
    rgba(c, (0.36, 0.22, 0.12), a); c.rectangle(x - w / 2, yf - 150, w, 150); c.fill()
    rgba(c, GOLD, 0.7 * a); c.rectangle(x - w / 2 - 10, yf - 158, w + 20, 8); c.fill()
    for k in range(nb):
        bowl(c, x - w / 2 + (k + 0.5) * w / nb, yf - 170, 0.8, a, t + k, 1)


def shop(c, x, yf, plaque, t, a=1.0, lit=1.0, w=440, h=230):
    bldg(c, x, yf, w, h, 'song', a, lit, t, plaque=None)
    if plaque:   # 幌子 banner hanging from a pole, upper right
        bx = x + w / 2 - 20; top = yf - h - 150
        rgba(c, (0.30, 0.18, 0.10), a); c.rectangle(bx - 4, top - 30, 8, 60); c.rectangle(bx - 50, top - 30, 54, 7); c.fill()
        n = len(plaque); bh_ = n * 58 + 40
        sw_ = 4 * math.sin(t * 1.3)
        rgba(c, (0.72, 0.14, 0.10), a); c.move_to(bx - 70, top - 23); c.line_to(bx - 4, top - 23); c.line_to(bx - 4 + sw_, top - 23 + bh_); c.line_to(bx - 37 + sw_, top - 23 + bh_ - 16); c.line_to(bx - 70 + sw_, top - 23 + bh_); c.close_path(); c.fill()
        rgba(c, GOLD, 0.8 * a); c.set_line_width(2); c.rectangle(bx - 64, top - 17, 54, bh_ - 30); c.stroke()
        for j, ch in enumerate(plaque):
            fnt(c, 44, FONT_X); ew = c.text_extents(ch)[4]
            rgba(c, (1, 0.93, 0.80), a); c.move_to(bx - 37 - ew / 2 + sw_ * j / n, top + 30 + j * 56); c.show_text(ch)
    for dx in (-w / 2 + 30, w / 2 - 30):
        lantern(c, x + dx, yf - h + 30, 0.6, a * lit, t)


def stove(c, x, yf, a=1.0, fire=0.0, t=0):
    rgba(c, (0.40, 0.33, 0.27), a); rrect(c, x - 110, yf - 150, 220, 150, 14); c.fill()
    rgba(c, (0.05, 0.04, 0.03), a); c.arc(x, yf - 60, 36, math.pi, 2 * math.pi); c.fill()
    rgba(c, (0.25, 0.25, 0.27), a); c.save(); c.translate(x, yf - 152); c.scale(80, 18); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    if fire > 0: campfire(c, x, yf - 40, t, a * fire, 0.5)


def ingots_rain(c, t, t0, x, y, a=1.0):
    for k in range(8):
        u = seg(t, t0 + k * 0.08, t0 + k * 0.08 + 0.6)
        if u <= 0: continue
        rr = random.Random(k + 3)
        xx = x + rr.uniform(-160, 160); yy = lerp(y - 360, y - rr.uniform(0, 60), eout(u))
        ingot(c, xx, yy, 0.7, a)


# ====================================================================== 1 HOOK
def ov_hook(c, t):
    text2(c, "下午三四点就吃完“晚饭”，", 960, 175, 88, 99, TXT, 1.0, 'c', 0.0, 0.01, FONT_X)
    if t >= 2.8:
        c.save(); popin(c, t, 2.8, 960, 300, 0.45)
        text2(c, "古人一天[只吃两顿]？", 960, 340, 124, 99, TXT, 1.0, 'c', 0.0, 0.01, FONT_X)
        c.restore()


@scene(7.4, [], sfx=[(0.0, 'boom', .45), (0.6, 'pour', .3), (2.2, 'growl', .9), (2.8, 'clash', .6), (2.85, 'seal', .8), (4.6, 'growl', .7)],
       cam=(960, 640, 900, 660, 1.0, 1.07), note=None, ov=ov_hook)
def s_hook(c, t):
    bgp(c, t, 1500, 700, 900, 'red')
    dk = seg(t, 2.6, 6.0)
    rgba(c, (0.03, 0.04, 0.09), 0.85 * dk); c.rectangle(-300, -300, W + 600, H + 600); c.fill()
    stars(c, t, dk, 50, 520)
    sunball(c, 1560, lerp(640, 900, ease(seg(t, 0.0, 5.0))), 56, 1 - 0.7 * dk)
    hills(c, t, 800, (SIL1, SIL2), 3)
    ground(c, 900)
    field(c, t, 900, 1100, 2000, 0.8, 0.0)
    # farmer eats, then hungry at dusk
    eat = t < 2.2
    C(c, 640, 980, 1.6, 'qinhan', 'peasant', 'hold' if eat else 'stand', 1, 'happy' if eat else ('sad' if t < 4.4 else 'sleep'),
      T=t, robe=HANP, sweat=fin(t, 3.0) * (1 - fin(t, 4.4)))
    bowl(c, 700, 760 if eat else 900, 0.9, 1.0, t, 1.0 if eat else 0.0)
    if eat:
        rgba(c, (0.95, 0.92, 0.85)); c.save(); c.translate(700, 754); c.scale(30 * (1 - seg(t, 0.3, 2.0)) + 0.1, 6); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    growl(c, 700, 860, t, 2.2)
    growl(c, 700, 860, t, 4.6)
    sundial(c, 230, 640, 140, t, sun=lerp(7.6, 9.8, seg(t, 0, 6.0)), meals=[(8, "最后一顿", 0.3, GOLDT)], a=1.0)
    flash(c, t, 2.8)


# ====================================================================== 2 three vs two
@scene(9.0, [(0.1, "今天，一日三餐天经地义"), (2.6, "可在古代很长时间里，[一天两顿]才是常态"), (5.6, "三餐是怎么来的？线索藏在[时辰]里")],
       sfx=[(0.4, 'tick', .6), (0.7, 'tick', .6), (1.0, 'tick', .6), (3.2, 'thud', .6), (5.8, 'chimeL', .4), (6.4, 'shimmer', .3)],
       cam=(960, 620, 1000, 640, 1.0, 1.06))
def s_intro(c, t):
    bgp(c, t, 960, 700, 900, 'brown')
    ground(c, 960)
    a1 = 1 - seg(t, 5.0, 5.6)
    for k, (lab, x) in enumerate((("早", 560), ("午", 960), ("晚", 1360))):
        p = back(seg(t, 0.4 + k * 0.3, 0.8 + k * 0.3))
        if p <= 0: continue
        gone = (k == 1) and t > 3.2
        c.save(); c.translate(x, 640); c.scale(p, p); c.translate(-x, -640)
        spot(c, x, 640, 200, a1)
        bowl(c, x, 640, 1.6, a1 * (0.35 if gone else 1.0), t + k, 0 if gone else 1)
        text2(c, lab, x, 800, 70, 99, GOLDT, a1, 'c', fam=FONT_X)
        c.restore()
    if a1 > 0: redx(c, 960, 660, 0.9, t, 3.2)
    sundial(c, 1180, 640, 250, t, sun=lerp(3, 10, seg(t, 5.6, 9.0)), a=fin(t, 5.3),
            meals=[(4, "早", 6.6, GOLDT), (8, "晚", 7.2, GOLDT)])
    C(c, 300, 1000, 1.5, 'song', 'kid', 'think', 1, 'shock' if t > 3.2 else 'calm', T=t)


# ====================================================================== 3 oracle bone
def ov_oracle(c, t):
    quote(c, t, 4.6, 1430, 560, ["甲寅大食雨，", "乙卯小食大啟。"],
          ["白话：甲寅日“大食”时会下雨吗？", "乙卯日“小食”时会转晴吗？"], 48, 36, '卜辞')


@scene(10.0, [(0.1, "最早的证据，刻在[甲骨]上"), (2.2, "商人把一天分成几段，其中两段叫——"), (4.0, "“[大食]”和“[小食]”", 'm')],
       src="据《甲骨文合集》21021", sfx=[(0.6, 'fire', .3), (1.2, 'clash', .3), (1.6, 'clash', .25), (4.0, 'seal', .7), (4.6, 'brush', .4)],
       cam=(700, 620, 760, 620, 1.0, 1.1), ov=ov_oracle)
def s_oracle(c, t):
    bgp(c, t, 700, 640, 800, 'red')
    rgba(c, (0.10, 0.07, 0.05)); c.rectangle(-200, 300, W + 400, 600); c.fill()
    ground(c, 900)
    brazier(c, 280, 900, t)
    plastron(c, 720, 640, 0.95, t, 1.0, fin(t, 4.0, 0.6), seg(t, 0.8, 2.4))
    C(c, 360, 985, 1.5, 'qinhan', 'scholar', 'point' if t > 2.0 else 'stand', 1, 'shock' if 1.2 < t < 2.6 else 'calm', T=t, robe=SHANG, p=fin(t, 2.0))


# ====================================================================== 4 大食小食 on dial
@scene(10.5, [(0.1, "[大食]约在上午七到九点：吃饱了下地"), (3.4, "[小食]约在下午三到五点：天快黑了，吃少点"), (6.8, "早饭丰盛，晚饭简单", 's')],
       src="时段为学界解读（董作宾、宋镇豪等）", sfx=[(0.5, 'seal', .6), (3.8, 'seal', .6), (1.6, 'thud', .3), (2.1, 'thud', .3), (5.2, 'growl', .4)],
       cam=(960, 600, 960, 620, 1.0, 1.05))
def s_dashi(c, t):
    bgp(c, t, 640, 640, 900, 'brown')
    hills(c, t, 760, (SIL1, SIL2), 1)
    ground(c, 920)
    field(c, t, 920, 900, 2000, 0.9, 0.3)
    sundial(c, 520, 640, 250, t, sun=lerp(3.5, 9.5, seg(t, 0, 7.5)), hi=(4, 8),
            meals=[(4, "大食", 0.5, GOLDT), (8, "小食", 3.8, GOLDT)])
    if t < 3.4:
        pose, expr, prop = ('hold', 'happy', None) if t < 1.4 else ('stand', 'happy', 'hoe')
        x = 1250 if t < 1.4 else lerp(1250, 1450, ease(seg(t, 1.4, 3.0)))
        C(c, x, 990, 1.6, 'qinhan', 'peasant', pose, 1, expr, T=t, robe=HANP, prop=prop, walk=(t * 9 if 1.4 < t < 3.0 else None))
        if t < 1.4:
            bowl(c, 1315, 770, 1.4, 1, t, 1)
    else:
        C(c, 1350, 990, 1.6, 'qinhan', 'peasant', 'hold' if t < 6.0 else 'stand', -1, 'calm' if t < 6.0 else 'sleep', T=t, robe=HANP)
        if t < 6.0:
            bowl(c, 1290, 790, 0.7, 1, t, 1)
        rgba(c, (0.03, 0.04, 0.09), 0.5 * seg(t, 5.5, 8.0)); c.rectangle(-300, -300, W + 600, H + 600); c.fill()


# ====================================================================== 5 饔飧
def ov_yong(c, t):
    quote(c, t, 1.0, 1360, 560, ["贤者与民并耕而食，", "饔飧而治。"],
          ["白话：贤君和百姓一起种地养活自己，", "一边自己做早晚两顿饭，一边治理国家"], 48, 34, '孟子', t1=5.6)
    quote(c, t, 6.0, 1360, 600, ["朝曰饔，夕曰飧。"], ["白话：早饭叫“饔”，晚饭叫“飧”"], 54, 40, '赵岐注')


@scene(11.0, [(0.1, "先秦时，两顿饭有了专名"), (6.2, "早饭[饔]（yōng），晚饭[飧]（sūn）")],
       src="据《孟子·滕文公上》及赵岐注", sfx=[(1.0, 'brush', .4), (6.0, 'brush', .4), (7.0, 'seal', .6), (7.6, 'seal', .6)],
       cam=(800, 620, 760, 640, 1.0, 1.06), ov=ov_yong)
def s_yong(c, t):
    bgp(c, t, 600, 680, 900, 'brown')
    hills(c, t, 760, (SIL1, SIL2), 5)
    ground(c, 920)
    field(c, t, 920, -100, 900, 0.9, 0.5)
    hoe = (t * 3) % 2 < 1
    C(c, 260, 990, 1.45, 'qinhan', 'official', 'stand', 1, 'happy', T=t, prop='hoe', robe=(0.45, 0.30, 0.20))
    C(c, 560, 990, 1.4, 'qinhan', 'peasant', 'stand', -1 if hoe else 1, 'happy', T=t + 1, prop='hoe', robe=HANP)
    # cooking pot (釜) with steam, two bowls marked
    rgba(c, (0.24, 0.20, 0.16)); c.move_to(760, 800); c.curve_to(760, 900, 960, 900, 960, 800); c.close_path(); c.fill()
    campfire(c, 860, 920, t, 1.0, 0.6)
    bowl(c, 860, 790, 1.4, 1.0, t, 1)
    if t > 6.6:
        for k, (lab, x) in enumerate((("饔", 760), ("飧", 960))):
            c.save(); popin(c, t, 7.0 + 0.6 * k, x, 640); seal(c, lab, x, 640, 0.9, 1.0, -0.05 + 0.1 * k); c.restore()


# ====================================================================== 6 餔 / 晡时
def ov_bu(c, t):
    quote(c, t, 1.2, 1360, 820, ["餔，日加申时食也。"], ["白话：“餔”，就是申时（下午三到五点）吃的那顿饭"], 52, 36, '说文')


@scene(9.5, [(0.1, "《说文解字》还专门给晚饭造了字"), (6.0, "这个饭点，后来就叫“[晡时]”")],
       src="据《说文解字·食部》、段玉裁注", sfx=[(1.2, 'brush', .4), (3.0, 'seal', .6), (6.0, 'chime', .3)],
       cam=(800, 600, 780, 620, 1.0, 1.05), ov=ov_bu)
def s_bu(c, t):
    bgp(c, t, 560, 640, 800, 'brown')
    ground(c, 960)
    sundial(c, 560, 640, 260, t, sun=lerp(6, 8.3, seg(t, 0.5, 3.0)), hi=(8,) if t > 3.0 else (), meals=[(8, "餔", 3.0, GOLDT)])
    if t > 6.0:
        c.save(); popin(c, t, 6.0, 560, 640); seal(c, "晡", 560, 640, 0.9, 1.0); c.restore()


# ====================================================================== 7 灭此朝食
def ov_qi(c, t):
    quote(c, t, 3.0, 1380, 560, ["余姑翦灭此而朝食。"], ["白话：我先灭了他们，回来再吃早饭！"], 50, 38, '左传', t1=6.6)


@scene(11.0, [(0.1, "早饭有多重要？春秋有位国君拿它[立军令状]"), (2.0, "公元前589年，齐晋[鞌之战]，齐顷公放话："), (7.6, "结果——{齐军大败}", 'm')],
       src="据《左传·成公二年》", sfx=[(0.4, 'gallop', .6), (3.0, 'brush', .3), (3.6, 'riserS', .3), (6.8, 'clash', .6), (7.4, 'boom', .6), (7.6, 'seal', .8)],
       cam=(800, 620, 860, 640, 1.0, 1.06), ov=ov_qi)
def s_qi(c, t):
    bgp(c, t, 700, 640, 900, 'red' if t > 7.2 else 'brown')
    hills(c, t, 740, (SIL1, SIL2), 2)
    ground(c, 920)
    x = lerp(150, 620, ease(seg(t, 0.0, 3.0)))
    if t > 7.2: x = lerp(620, 380, ease(seg(t, 7.2, 8.4)))
    shake = 8 * math.sin(t * 60) * (1 - seg(t, 7.2, 8.0)) if t > 7.2 else 0
    face = 1 if t < 7.2 else -1
    yf = 930
    chariot(c, x + shake, yf, 1.0, t if t < 6.8 or t > 7.2 else 0, 1.0, face)
    C(c, x - 10 * face + shake, yf - 100, 1.25, 'qinhan', 'emperor', 'raise' if t < 7.2 else 'stand', face,
      'angry' if t < 6.6 else 'shock', T=t, robe=QIRO, p=1.0, sweat=fin(t, 7.6))
    chariot_front(c, x + shake, yf, 1.0, t, 1.0, face)
    if t > 6.4:
        for k, xx in enumerate((1500, 1700, 1880)):
            sx, ph = wk(t, 6.4 + k * 0.1, 7.2 + k * 0.1, xx + 400, xx)
            C(c, sx, 985, 1.3, 'qinhan', 'soldier', 'point', -1, 'angry', T=t + k, prop='spear', walk=ph, p=fin(t, 7.2))
        if 6.8 < t < 7.6:
            arrows_flying(c, 1500, 640, x + 100, 760, t * 3, 5, 1.0)
    flash(c, t, 7.4)


# ====================================================================== 8 why two
def icon_card(c, x, y, title, kind, t, t0):
    if t < t0: return
    c.save(); popin(c, t, t0, x, y)
    rgba(c, (0.10, 0.07, 0.05), 0.92); rrect(c, x - 150, y - 170, 300, 340, 22); c.fill()
    rgba(c, GOLD); c.set_line_width(3); rrect(c, x - 150, y - 170, 300, 340, 22); c.stroke()
    if kind == 'sun':
        sunball(c, x, y - 30, 42, 1.0); rgba(c, (0.15, 0.10, 0.06)); c.rectangle(x - 130, y + 10, 260, 50); c.fill()
        rgba(c, (0.03, 0.04, 0.09), 0.6 * (0.5 + 0.5 * math.sin(t * 1.5))); c.rectangle(x - 130, y - 140, 260, 200); c.fill()
    elif kind == 'grain':
        rgba(c, (0.55, 0.38, 0.20)); c.move_to(x - 80, y + 50); c.curve_to(x - 110, y - 60, x - 60, y - 110, x, y - 110); c.curve_to(x + 60, y - 110, x + 110, y - 60, x + 80, y + 50); c.close_path(); c.fill()
        text2(c, "粟", x, y - 10, 70, 99, TXT, 1, 'c', fam=FONT_X)
    else:
        lamp(c, x, y - 30, t, 1.0); coin(c, x - 60, y + 40, 18); coin(c, x + 60, y + 40, 18)
    text2(c, title, x, y + 140, 44, 99, TXT, 1, 'c', fam=FONT_X)
    c.restore()


def coin(c, x, y, r=16, a=1.0):
    if a <= 0: return
    rgba(c, (0.95, 0.75, 0.30), a); c.arc(x, y, r, 0, 6.283); c.fill()
    rgba(c, (0.55, 0.38, 0.12), a); c.rectangle(x - r * 0.3, y - r * 0.3, r * 0.6, r * 0.6); c.fill()


@scene(10.5, [(0.1, "为什么只吃两顿？"), (1.6, "天亮下地，[天黑就睡]"), (4.4, "粮食不宽裕，[灯油]也金贵"), (7.2, "天黑后再开一顿饭，费粮又费灯", 's')],
       sfx=[(1.6, 'thud', .5), (4.4, 'thud', .5), (5.6, 'thud', .5), (7.2, 'growl', .4)],
       cam=(960, 620, 960, 640, 1.0, 1.05))
def s_why(c, t):
    bgp(c, t, 700, 680, 900, 'brown')
    rgba(c, (0.03, 0.04, 0.09), 0.6 * seg(t, 6.0, 9.0)); c.rectangle(-300, -300, W + 600, H + 600); c.fill()
    hills(c, t, 780, (SIL1, SIL2), 7)
    ground(c, 930)
    sl = t > 7.6
    C(c, 260, 1000, 1.45, 'qinhan', 'peasant', 'stand', 1, 'sleep' if sl else 'calm', T=t, robe=HANP, prop=None if sl else 'hoe')
    C(c, 470, 1000, 1.35, 'qinhan', 'lady', 'stand', 1, 'sleep' if sl else 'calm', T=t + 1, robe=(0.55, 0.40, 0.36))
    icon_card(c, 860, 620, "日出而作", 'sun', t, 1.6)
    icon_card(c, 1220, 620, "粮少", 'grain', t, 4.4)
    icon_card(c, 1580, 620, "灯油贵", 'lamp', t, 5.6)


# ====================================================================== 9 晁错
def ov_cc(c, t):
    quote(c, t, 1.4, 960, 560, ["人情，一日不再食则饥。"], ["白话：人之常情，一天吃不上两顿饭就会挨饿"], 54, 40, '汉书')


@scene(10.0, [(0.1, "西汉晁错给汉文帝上书，说得很直白"), (6.6, "“[再食]”就是吃第二顿：两顿才算正常")],
       src="据《汉书·食货志上》晁错《论贵粟疏》", sfx=[(1.4, 'brush', .4), (6.6, 'seal', .6)],
       cam=(960, 600, 960, 620, 1.0, 1.05), ov=ov_cc)
def s_cc(c, t):
    court(c, t, 'qinhan', plaque='未央', sx=960, sy=640, px_=None)
    C(c, 300, 990, 1.55, 'qinhan', 'official', 'bow', 1, 'calm', T=t, prop='tablet', p=ease(seg(t, 0.3, 1.0)), robe=(0.20, 0.22, 0.30))
    C(c, 1640, 990, 1.6, 'qinhan', 'emperor', 'think' if t < 6.6 else 'stand', -1, 'calm' if t < 6.6 else 'happy', T=t)


# ====================================================================== 10 白虎通
def ov_bh(c, t):
    quote(c, t, 1.0, 1340, 560, ["平旦食……昼食……", "餔食……暮食。", "诸侯三饭，卿大夫再饭。"],
          ["白话：天子天亮、中午、下午、傍晚各吃一顿；", "诸侯一天三顿，卿大夫一天两顿"], 46, 32, '白虎通', t1=6.2)


def bowls_row(c, x, y, n, t, t0):
    for k in range(n):
        if t < t0 + k * 0.15: continue
        p = back(seg(t, t0 + k * 0.15, t0 + k * 0.15 + 0.35))
        bx = x + (k - (n - 1) / 2) * 76
        c.save(); c.translate(bx, y); c.scale(p, p); c.translate(-bx, -y)
        bowl(c, bx, y, 0.85, 1, t + k, 0.6); c.restore()


@scene(12.5, [(0.1, "吃几顿，还分[身份]"), (6.4, "东汉《白虎通》：天子[四顿]，诸侯三顿，大夫两顿"),
              (8.6, "种地的百姓呢？“饭即食，饱即作”", 'q'), (10.2, "白话：饿了就吃，吃饱就干活", 's')],
       src="据《白虎通·礼乐》", sfx=[(1.0, 'brush', .4), (6.6, 'tick', .5), (6.75, 'tick', .5), (6.9, 'tick', .5), (7.05, 'tick', .5), (8.6, 'thud', .4)],
       cam=(960, 620, 960, 640, 1.0, 1.04), ov=ov_bh)
def s_bh(c, t):
    bgp(c, t, 700, 640, 950, 'brown')
    rgba(c, (0.12, 0.08, 0.055)); c.rectangle(-200, 200, W + 400, 700); c.fill()
    ground(c, 900, (0.10, 0.07, 0.05))
    lamp(c, 120, 520, t, 0.8)
    ex = 420 if t < 6.2 else lerp(420, 380, seg(t, 6.2, 6.8))
    C(c, ex, 990, 1.55, 'qinhan', 'emperor', 'hold', 1, 'happy', T=t)
    bowls_row(c, ex, 520, 4, t, 2.4 if t < 6.2 else 0)
    if t > 6.2:
        C(c, 860, 990, 1.4, 'qinhan', 'official', 'stand', 1, 'happy', T=t + 1, robe=QIRO, a=fin(t, 6.3))
        bowls_row(c, 860, 540, 3, t, 6.6)
        C(c, 1300, 990, 1.35, 'qinhan', 'official', 'stand', 1, 'calm', T=t + 2, robe=(0.20, 0.36, 0.30), a=fin(t, 6.5))
        bowls_row(c, 1300, 560, 2, t, 6.9)
    if t > 8.6:
        C(c, 1720, 990, 1.4, 'qinhan', 'peasant', 'stand', -1, 'happy', T=t, robe=HANP, prop='hoe', a=fin(t, 8.6))


# ====================================================================== 11 韩信蹭饭
def ov_hx(c, t):
    quote(c, t, 3.4, 1400, 560, ["亭长妻患之，乃晨炊蓐食。"], ["白话：亭长老婆嫌他，天没亮就做好饭，", "端到床上吃光"], 46, 36, '史记', t1=7.2)


@scene(11.5, [(0.1, "饭点一过，就没饭吃"), (1.6, "韩信年轻时穷，常去亭长家[蹭饭]"), (8.0, "等韩信到饭点上门：{锅里空了}", 'm')],
       src="据《史记·淮阴侯列传》", sfx=[(3.4, 'brush', .4), (5.0, 'pour', .3), (7.6, 'creak', .4), (8.0, 'thud', .7), (8.6, 'growl', .7)],
       cam=(800, 620, 860, 640, 1.0, 1.06), ov=ov_hx)
def s_hx1(c, t):
    bgp(c, t, 600, 640, 900, 'blue' if t < 6.5 else 'brown')
    rgba(c, (0.13, 0.09, 0.06)); c.rectangle(-200, 220, W + 400, 700); c.fill()
    ground(c, 900, (0.10, 0.07, 0.05))
    candle(c, 120, 720, 90, t, 1.0)
    bed(c, 480, 900, 0.95, 1.0, 0.5)
    eat = 4.4 < t < 7.0
    C(c, 470, 740, 1.15, 'qinhan', 'lady', 'kneel', 1, 'happy' if eat else ('sleep' if t < 4.4 else 'calm'), T=t, robe=(0.60, 0.36, 0.30), p=1.0)
    if t > 4.4:
        bowl(c, 540, 650, 0.8, 1, t, 1 if eat else 0)
    stove(c, 1000, 900, 1.0, 1 - seg(t, 6.0, 7.0), t)
    if t > 7.4:
        x, ph = wk(t, 7.4, 8.0, 2100, 1240)
        C(c, x, 990, 1.55, 'qinhan', 'scholar', 'stand' if t < 9.4 else 'stand', -1 if t < 9.6 else 1,
          'shock' if t < 9.0 else 'angry', T=t, robe=HX, walk=ph if t < 9.6 else t * 9)
        if t > 9.6:
            pass
    if t > 8.2:
        redx(c, 1000, 700, 0.5, t, 8.2)


# ====================================================================== 12 漂母
def ov_pm(c, t):
    quote(c, t, 3.4, 1400, 560, ["有一母见信饥，饭信，", "竟漂数十日。"], ["白话：一位大娘见他挨饿，分饭给他吃，", "一直到漂洗完，一连几十天"], 46, 34, '史记', t1=7.4)


@scene(11.0, [(0.1, "韩信只好去河边钓鱼"), (1.6, "洗丝絮的[漂母]，看他饿着"), (7.8, "后来韩信封王，赏漂母[千金]", 'm')],
       src="据《史记·淮阴侯列传》", sfx=[(0.4, 'drip', .4), (2.4, 'pour', .3), (3.4, 'brush', .4), (7.8, 'coins', .7), (8.1, 'shimmer', .4)],
       cam=(760, 640, 800, 660, 1.0, 1.06), ov=ov_pm)
def s_pm(c, t):
    bgp(c, t, 600, 680, 900, 'brown')
    hills(c, t, 700, (SIL1, SIL2), 9)
    rgba(c, (0.10, 0.16, 0.26)); c.rectangle(-200, 760, W + 400, 140); c.fill()
    rgba(c, (0.6, 0.75, 0.85), 0.25); c.set_line_width(2)
    for k in range(6):
        c.move_to(-100, 790 + k * 20)
        for x in range(-100, 2100, 60): c.line_to(x, 790 + k * 20 + 4 * math.sin(x * 0.02 + t * 2 + k))
        c.stroke()
    ground(c, 900)
    hx_happy = t > 2.6
    C(c, 380, 990, 1.5, 'qinhan', 'scholar', 'hold' if hx_happy else 'stand', 1, 'happy' if hx_happy else 'sad', T=t, robe=HX)
    rgba(c, (0.50, 0.32, 0.16)); c.set_line_width(5); c.move_to(300, 820); c.line_to(140, 600); c.stroke()
    rgba(c, (0.9, 0.9, 0.9), 0.6); c.set_line_width(1.5); c.move_to(140, 600); c.line_to(120, 800); c.stroke()
    if hx_happy:
        bowl(c, 440, 790, 0.9, 1, t, 1)
    C(c, 760, 990, 1.45, 'qinhan', 'lady', 'hold' if t < 2.6 else 'stand', -1, 'happy', T=t + 1, robe=PIAO)
    if t < 2.6:
        bowl(c, 700, 780, 0.9, 1, t, 1)
    if t > 7.8:
        ingots_rain(c, t, 7.8, 760, 920)


# ====================================================================== 13 唐宵禁
def ov_tang(c, t):
    quote(c, t, 6.6, 1440, 560, ["诸犯夜者，笞二十。"], ["白话：凡是夜里违禁出坊的，打二十板子"], 52, 38, '唐律')


@scene(11.5, [(0.1, "到了唐代，城里有[宵禁]"), (1.8, "天黑鼓响，[坊门]一关"), (4.2, "闭门鼓后还在坊外走，就叫“[犯夜]”")],
       src="据《唐律疏议·杂律》", sfx=[(1.8, 'drum', .9), (2.3, 'drum', .9), (2.8, 'drum', .9), (3.3, 'creak', .5), (4.0, 'lock', .7), (6.6, 'brush', .4), (8.6, 'thud', .8), (8.7, 'clash', .5)],
       cam=(700, 640, 760, 660, 1.0, 1.06), ov=ov_tang)
def s_tang(c, t):
    bgp(c, t, 700, 640, 900, 'blue')
    stars(c, t, 0.8, 40, 380)
    moon(c, 1180, 200, 40, 1.0)
    yardwall(c, -200, 640, 880, 280); yardwall(c, 900, 1150, 880, 280)
    fanggate(c, 770, 880, ease(seg(t, 3.2, 4.2)), 1.0, "坊门")
    ground(c, 880)
    b = (t - 1.8) % 0.5 if 1.8 < t < 3.3 else 1
    drum(c, 160, 720, 1.5 * (1 + 0.06 * (1 - min(1, b * 4))), 1.0)
    x, ph = wk(t, 4.4, 6.0, 400, 520)
    C(c, x, 990, 1.4, 'tang', 'scholar', 'stand', 1, 'shock' if t > 6.4 else 'calm', T=t, walk=ph, sweat=fin(t, 6.4), robe=(0.44, 0.52, 0.66))
    sx, ph2 = wk(t, 5.6, 6.6, -200, 200)
    C(c, sx, 990, 1.5, 'tang', 'soldier', 'point' if t > 6.6 else 'stand', 1, 'angry', T=t, prop='spear', walk=ph2, p=fin(t, 6.6))
    if t > 8.6:
        c.save(); popin(c, t, 8.6, 520, 560); seal(c, "笞二十", 520, 560, 1.5, 1.0, -0.06); c.restore()
    flash(c, t, 8.6)


# ====================================================================== 14 点心
def ov_dx(c, t):
    quote(c, t, 1.6, 1420, 560, ["治妆未毕，我未及餐，", "尔且可点心。"], ["白话：我还没梳妆完，顾不上吃饭，", "你先吃点东西垫垫肚子"], 48, 36, '漫录', t1=7.4)


@scene(12.0, [(0.1, "两顿之间饿了？唐人有“[点心]”"), (7.6, "弟弟一口就[吃光了]"), (9.4, "郑傪：{刚给过了，怎么又要？}")],
       src="据宋人笔记《能改斋漫录·点心》", sfx=[(1.6, 'brush', .4), (7.6, 'pour', .4), (9.0, 'creak', .3), (9.4, 'thud', .7)],
       cam=(640, 640, 640, 660, 1.0, 1.06), ov=ov_dx)
def s_dx(c, t):
    bgp(c, t, 600, 640, 900, 'brown')
    rgba(c, (0.13, 0.09, 0.06)); c.rectangle(-200, 220, W + 400, 700); c.fill()
    ground(c, 900, (0.10, 0.07, 0.05))
    lamp(c, 60, 520, t, 0.8)
    # mirror table
    rgba(c, (0.35, 0.18, 0.10)); c.rectangle(80, 760, 160, 140); c.fill()
    rgba(c, (0.80, 0.80, 0.85)); c.arc(160, 700, 54, 0, 6.283); c.fill(); rgba(c, GOLD); c.set_line_width(5); c.arc(160, 700, 54, 0, 6.283); c.stroke()
    C(c, 330, 990, 1.45, 'tang', 'lady', 'point' if 1.6 < t < 4 else 'stand', 1, 'calm', T=t, robe=(0.78, 0.40, 0.46), p=fin(t, 1.6))
    eat = t > 7.4
    C(c, 640, 990, 1.3, 'tang', 'kid', 'hold', -1, 'happy', T=t + 1, belly=0.6 * seg(t, 7.4, 8.4))
    bowl(c, 585, 800, 0.9, 1, t, 0 if eat else 1)
    if t > 8.8:
        mx, ph = wk(t, 8.8, 9.4, -150, 120)
        C(c, mx, 990, 1.25, 'tang', 'lady', 'raise', 1, 'calm', T=t, robe=(0.40, 0.50, 0.46), walk=ph, p=1.0)
        C(c, 900, 990, 1.55, 'tang', 'official', 'point', -1, 'angry', T=t, p=fin(t, 9.4), robe=(0.30, 0.38, 0.55), a=fin(t, 9.0))


# ====================================================================== 15 宋 坊墙倒
@scene(10.0, [(0.1, "到了宋代，城市变了样"), (2.4, "[临街开店]，坊墙挡不住买卖"), (5.6, "天黑以后，也能出门[买吃的]了", 'm')],
       src="", sfx=[(1.2, 'rumble', .7), (1.5, 'boom', .4), (3.6, 'shimmer', .4), (6.0, 'chime', .3)],
       cam=(960, 620, 960, 640, 1.0, 1.08))
def s_wall(c, t):
    bgp(c, t, 960, 640, 950, 'brown' if t < 4.5 else 'blue')
    stars(c, t, seg(t, 4.5, 6.0), 40, 300)
    nt = seg(t, 4.0, 6.0)
    for k, (x, pq) in enumerate(((360, "酒"), (960, "饼"), (1560, "茶"))):
        shop(c, x, 880, pq, t + k, 1.0, 0.3 + 0.7 * nt)
    ground(c, 880)
    # collapsing wall pieces
    for k in range(10):
        u = seg(t, 1.0 + k * 0.06, 2.2 + k * 0.06)
        if u >= 1: continue
        x0 = -100 + k * 220
        c.save(); c.translate(x0 + 110, 880); c.rotate(0.6 * ease(u) * (1 if k % 2 else -1)); c.translate(0, 300 * ease(u) ** 2)
        yardwall(c, -110, 110, 0, 300, 1 - u); c.restore()
    if t > 3.0:
        for k, (x, role, rb) in enumerate(((700, 'scholar', SONGB), (1300, 'merchant', (0.55, 0.36, 0.20)), (1870, 'lady', (0.70, 0.42, 0.40)))):
            xx, ph = wk(t, 3.0 + k * 0.3, 6.5, x - 200, x)
            C(c, xx, 990, 1.3, 'song', role, 'stand', 1, 'happy', T=t + k, walk=ph, robe=rb, prop='lantern' if role == 'lady' and t > 5 else None)


# ====================================================================== 16 夜市
def ov_ns(c, t):
    quote(c, t, 1.4, 1420, 560, ["夜市直至三更尽，", "才五更又复开张。"], ["白话：夜市一直开到后半夜一点多，", "凌晨三四点又开张了"], 50, 36, '梦华录', t1=6.8)


@scene(12.0, [(0.1, "北宋都城[汴京]的夜市"), (7.0, "胡饼、灌肠、[香糖果子]……"), (9.2, "深夜饿了，城里人[有地方吃]了", 'm')],
       src="据《东京梦华录》卷三", sfx=[(1.4, 'brush', .4), (7.0, 'tick', .5), (7.4, 'tick', .5), (7.8, 'tick', .5), (9.2, 'shimmer', .4)],
       cam=(700, 620, 760, 640, 1.0, 1.06), ov=ov_ns)
def s_ns(c, t):
    bgp(c, t, 700, 640, 950, 'blue')
    stars(c, t, 0.7, 40, 260)
    shop(c, 380, 820, "灌肠", t, 1.0, 1.0, 420, 220)
    shop(c, 900, 820, "胡饼", t + 1, 1.0, 1.0, 420, 220)
    shop(c, 1500, 820, "果子", t + 2, 1.0, 1.0, 420, 220)
    ground(c, 880)
    for x in (150, 650, 1150, 1700):
        lantern(c, x, 420 + 10 * math.sin(t + x), 0.7, 1.0, t)
    stall(c, 560, 990, 360, 1.0, t, 3)
    C(c, 300, 1000, 1.35, 'song', 'merchant', 'raise', 1, 'happy', T=t, p=1.0)
    C(c, 830, 1000, 1.35, 'song', 'scholar', 'hold', -1, 'happy', T=t + 1, robe=SONGB)
    bowl(c, 780, 800, 0.8, 1, t, 1)
    if t > 6.8:
        C(c, 1150, 1000, 1.3, 'song', 'kid', 'cheer', -1, 'happy', T=t + 2, a=fin(t, 6.8))
        C(c, 1450, 1000, 1.35, 'song', 'lady', 'hold', -1, 'happy', T=t + 3, robe=(0.70, 0.42, 0.40), a=fin(t, 7.0))
        bowl(c, 1395, 800, 0.8, fin(t, 7.0), t, 1)


# ====================================================================== 17 早市
def ov_zs(c, t):
    quote(c, t, 1.4, 1420, 560, ["酒店多点灯烛沽卖，", "并粥饭点心。"], ["白话：五更天，酒店就点着灯开卖，", "还有粥、饭和点心"], 50, 36, '梦华录', t1=6.6)


@scene(11.0, [(0.1, "五更天，寺院行者敲铁牌报晓"), (7.0, "上朝的官、赶早市的人，[出门先吃一口]"), (9.0, "早点，成了一顿饭", 's')],
       src="据《东京梦华录》卷三", sfx=[(0.4, 'clash', .4), (1.0, 'clash', .4), (1.6, 'clash', .4), (1.4, 'brush', .4), (7.0, 'pour', .3)],
       cam=(640, 640, 700, 650, 1.0, 1.06), ov=ov_zs)
def s_zs(c, t):
    bgp(c, t, 700, 640, 950, 'blue')
    rgba(c, (0.55, 0.30, 0.15), 0.25 * seg(t, 4, 11)); c.rectangle(-300, 500, W + 600, 500); c.fill()
    stars(c, t, 0.6 * (1 - seg(t, 5, 10)), 40, 300)
    shop(c, 640, 860, "酒", t, 1.0, 1.0, 520, 240)
    ground(c, 880)
    stall(c, 700, 990, 380, 1.0, t, 3)
    x, ph = wk(t, 0.0, 5.0, -100, 260)
    C(c, x, 1000, 1.35, 'song', 'peasant', 'raise', 1, 'calm', T=t, walk=ph, robe=(0.55, 0.40, 0.25), p=1.0)
    rgba(c, (0.60, 0.62, 0.66)); rrect(c, x + 50, 600, 46, 70, 6); c.fill()
    if t > 6.9:
        C(c, 1050, 1000, 1.45, 'song', 'official', 'hold', -1, 'happy', T=t, a=fin(t, 6.9))
        bowl(c, 990, 790, 0.85, fin(t, 6.9), t, 1)


# ====================================================================== 18 不置家蔬
def ov_bz(c, t):
    quote(c, t, 1.2, 1400, 560, ["市井经纪之家，往往只于", "市店旋置饮食，不置家蔬。"], ["白话：城里做买卖的人家，常常直接在店里", "买现成饭菜，家里不开伙"], 46, 34, '梦华录')


@scene(10.0, [(0.1, "不少城里人，干脆[不在家做饭]"), (7.4, "饿了就买：[几点都有得吃]", 'm')],
       src="据《东京梦华录》卷三", sfx=[(1.2, 'brush', .4), (5.0, 'coins', .5), (7.4, 'chime', .3)],
       cam=(560, 640, 600, 650, 1.0, 1.06), ov=ov_bz)
def s_bz(c, t):
    bgp(c, t, 560, 640, 900, 'brown')
    rgba(c, (0.12, 0.08, 0.055)); c.rectangle(-200, 260, W + 400, 640); c.fill()
    ground(c, 900, (0.10, 0.07, 0.05))
    stove(c, 160, 900, 1.0, 0.0, t)
    redx(c, 160, 760, 0.45, t, 2.0)
    stall(c, 760, 900, 300, 1.0, t, 2)
    C(c, 900, 990, 1.4, 'song', 'merchant', 'hold', -1, 'happy', T=t + 1, p=1.0, robe=(0.55, 0.36, 0.20))
    x, ph = wk(t, 2.6, 4.4, 200, 520)
    C(c, x, 990, 1.4, 'song', 'scholar', 'hold' if t > 5.0 else 'stand', 1, 'happy', T=t, walk=ph, robe=SONGB)
    if t > 5.0:
        bowl(c, x + 60, 790, 0.85, 1, t, 1)


# ====================================================================== 19 占城稻
@scene(12.0, [(0.1, "饭桌背后，是[粮食]"), (2.0, "1012年，宋真宗从福建调来[占城稻]三万斛"), (5.2, "分给江南、淮南、两浙三路去种")],
       src="据《宋史·食货志上一》", sfx=[(2.0, 'seal', .6), (5.2, 'whoosh', .4), (5.6, 'tick', .5), (6.0, 'tick', .5), (6.4, 'tick', .5), (8.0, 'brush', .4)],
       cam=(960, 560, 960, 580, 1.0, 1.05), note="地图为示意", ov=lambda c, t: quote(c, t, 8.0, 560, 860, ["不择地而生。"], ["白话：不挑田地，哪儿都能长"], 50, 36, '宋史'))
def s_rice(c, t):
    f = mapbg(c, 118.4, 29.5, 1500, 0.25)
    src = (1450, H - 130)
    if t > 2.0:
        rgba(c, GOLDL, fin(t, 2.0)); c.move_to(src[0] - 22, H - 60); c.line_to(src[0] + 22, H - 60); c.line_to(src[0], H - 96); c.close_path(); c.fill()
    dests = (("淮南", 119.43, 32.39), ("江南", 115.89, 28.68), ("两浙", 120.16, 30.27))
    maptag(c, "从福建北运", src[0], src[1], fin(t, 2.0), 44, True, fin(t, 2.0))
    for k, (nm, lo, la) in enumerate(dests):
        d = f(lo, la)
        pr = ease(seg(t, 5.2 + k * 0.4, 6.6 + k * 0.4))
        dotted(c, [src, ((src[0] + d[0]) / 2 + 40, (src[1] + d[1]) / 2), d], pr, 1.0, (1, 0.85, 0.55), t)
        if pr > 0.95:
            maptag(c, nm, d[0], d[1], fin(t, 6.6 + k * 0.4), 40, True, 0.6)
            for j in range(5):
                rice(c, d[0] - 50 + j * 25, d[1] + 70, 60, fin(t, 6.8 + k * 0.4), 4 * math.sin(t * 2 + j), 1.0)


# ====================================================================== 20 三餐
@scene(12.5, [(0.1, "粮食多了，城市[不睡]了"), (2.6, "早点、午饭、晚饭，外加夜宵"), (6.0, "一日三餐，在[城里]流行开来", 'm'), (9.0, "不过很多乡下地方，两顿饭还吃了很久", 's')],
       src="", sfx=[(2.8, 'seal', .5), (3.4, 'seal', .5), (4.0, 'seal', .5), (4.6, 'seal', .5), (6.0, 'shimmer', .5)],
       cam=(1000, 620, 1040, 640, 1.0, 1.04))
def s_three(c, t):
    bgp(c, t, 1250, 640, 900, 'brown')
    ground(c, 980)
    sundial(c, 1320, 700, 230, t, sun=(t * 1.6) % 12, ghost=[(4, "大食"), (8, "小食")] if t < 2.6 else (),
            meals=[(3, "早点", 2.8, GOLDT), (6, "午饭", 3.4, GOLDT), (9, "晚饭", 4.0, GOLDT), (11, "夜宵", 4.6, (0.70, 0.80, 1.0))])
    C(c, 420, 1000, 1.5, 'song', 'scholar', 'cheer' if t > 6 else 'stand', 1, 'happy', T=t, robe=SONGB)
    C(c, 650, 1000, 1.3, 'song', 'kid', 'cheer' if t > 6.2 else 'stand', 1, 'happy', T=t + 1)
    if t > 9.0:
        C(c, 150, 1000, 1.25, 'song', 'peasant', 'stand', 1, 'calm', T=t, prop='hoe', a=fin(t, 9.0), robe=HANP)


# ====================================================================== 21 END
@scene(10.5, [(0.1, "从商朝的“大食、小食”"), (2.0, "到汴京城的通宵灯火"), (4.6, "多出来的那一顿饭，", 'm'), (6.6, "是[粮食]和[城市]一起喂出来的", 'm')],
       src="", sfx=[(0.3, 'chimeL', .4), (2.0, 'shimmer', .4), (6.6, 'boom', .35)],
       cam=(960, 640, 960, 600, 1.06, 1.0), note=None)
def s_end(c, t):
    bgp(c, t, 960, 640, 950, 'blue')
    stars(c, t, 0.7, 50, 420)
    # left: shang/han dusk, right: song night city
    for k, x in enumerate((1180, 1560, 1940)):
        shop(c, x, 860, ("酒", "饼", "茶")[k], t + k, 1.0, fin(t, 2.0), 380, 210)
    hills(c, t, 820, (SIL1,), 4)
    ground(c, 880)
    C(c, 380, 990, 1.5, 'qinhan', 'peasant', 'stand', 1, 'sleep', T=t, robe=HANP)
    sundial(c, 780, 650, 150, t, sun=8.6, meals=[(4, "大食", 0.3, GOLDT), (8, "小食", 0.6, GOLDT)], a=1.0 - 0.4 * fin(t, 2.0))
    if t > 2.0:
        C(c, 1450, 1000, 1.35, 'song', 'scholar', 'hold', -1, 'happy', T=t, robe=SONGB, a=fin(t, 2.0))
        bowl(c, 1395, 800, 0.8, fin(t, 2.0), t, 1)
        C(c, 1830, 1000, 1.3, 'song', 'kid', 'cheer', -1, 'happy', T=t + 1, a=fin(t, 2.3))

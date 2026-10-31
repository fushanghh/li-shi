# 左宗棠 · 战争风 × 戚继光样片剪法：暗金西北地图 + 线描侧面/背影英雄 + 兵器对砍
import math, random
import cairocffi as cairo
from kit import W, H, FONT, text, glow, GOLD, RED, ease, eout, cl, lerp, mix, vgrad, poly, moon, flame, INK
from kit import horse as khorse
from fig import shape, line, tube, hatch, sword, soldier, LINE, INKF, ROBE, CAPE, CAPE_D, SKIN, STEEL
from side import side, back, head_side
from scenes import sky, mts, ground, embers, smoke, arrows, speedlines, stamp, flag, wall, troops
import mapx as M

BP = 0.4285584
BRUSH = 'Ma Shan Zheng'
TEAL = (0.10, 0.36, 0.40); TEAL_D = (0.05, 0.18, 0.22)
GUAN = (0.13, 0.16, 0.32)      # 左宗棠 官袍石青
WARM = (1.0, 0.82, 0.45)

def btext(c, s, x, y, size, col=(1, 0.95, 0.86), a=1, align='c', font=BRUSH, sp=0):
    c.select_font_face(font, 0, 0); c.set_font_size(size)
    ws = [c.text_extents(ch)[4] for ch in s]; tw = sum(ws) + sp * (len(s) - 1)
    xx = x - tw / 2 if align == 'c' else (x if align == 'l' else x - tw)
    for ch, w in zip(s, ws):
        c.set_source_rgba(0, 0, 0, 0.55 * a); c.move_to(xx + 3, y + 4); c.show_text(ch)
        c.set_source_rgba(*col, a); c.move_to(xx, y); c.show_text(ch); xx += w + sp
    return tw

def vbrush(c, s, x, y, size, col=(1, 0.95, 0.86), a=1, lt=None, speed=6):
    for i, ch in enumerate(s):
        aa = a if lt is None else a * cl((lt - i / speed) / 0.25)
        if aa > 0: btext(c, ch, x, y + i * size * 1.08, size, col, aa)

# ---------------- 特效件 ----------------
def sparks(c, lt, t0, x, y, n=60, seed=1, spd=900, col=(1, 0.85, 0.5), life=0.6):
    u = lt - t0
    if u < 0 or u > life: return
    r = random.Random(seed)
    k = u / life
    glow(c, x, y, 260 * (1 - k) + 40, (1, 0.9, 0.6), 0.9 * (1 - k))
    c.set_line_cap(1)
    for i in range(n):
        an = r.uniform(0, 6.283); v = r.uniform(0.3, 1) * spd
        dx, dy = math.cos(an) * v * u, math.sin(an) * v * u + 600 * u * u
        L = 0.04 * v
        c.set_source_rgba(*col, (1 - k) * r.uniform(0.5, 1)); c.set_line_width(r.uniform(2, 5))
        c.move_to(x + dx, y + dy); c.line_to(x + dx - math.cos(an) * L, y + dy - math.sin(an) * L); c.stroke()

def ring(c, lt, t0, x, y, R=700, col=(1, 0.85, 0.55), w=26):
    u = lt - t0
    if not (0 <= u < 0.45): return
    k = eout(u / 0.45)
    c.set_source_rgba(*col, 0.85 * (1 - k)); c.set_line_width(w * (1 - k) + 2); c.arc(x, y, 30 + R * k, 0, 6.283); c.stroke()

def slasharc(c, lt, t0, x, y, r=480, a0=-2.4, a1=0.7, col=(1, 0.95, 0.82), dur=0.35):
    u = lt - t0
    if not (0 <= u < dur + 0.2): return
    k = eout(u / dur); fade = 1 - cl((u - dur * 0.5) / 0.35)
    for j in range(7):
        c.set_source_rgba(*col, 0.55 * fade * (1 - j / 7)); c.set_line_width(30 - j * 4)
        c.arc(x, y, r - j * 7, a0, a0 + (a1 - a0) * k) if a1 > a0 else c.arc_negative(x, y, r - j * 7, a0, a0 + (a1 - a0) * k)
        c.stroke()

def streak(c, lt, t0, y0, y1, dur=0.35, col=(1, 0.93, 0.75), w=10):
    """光刀划屏（戚继光样片的光束）"""
    u = lt - t0
    if not (0 <= u < dur + 0.25): return
    k = eout(u / dur); fade = 1 - cl((u - dur) / 0.25)
    x0, x1 = -200, W + 200
    xh = lerp(x0, x1, k); yh = lerp(y0, y1, k)
    xt = lerp(x0, x1, max(0, k - 0.45)); yt = lerp(y0, y1, max(0, k - 0.45))
    for ww, aa in ((w * 6, 0.12), (w * 2.2, 0.35), (w, 1.0)):
        c.set_source_rgba(*col, aa * fade); c.set_line_width(ww); c.set_line_cap(1); c.move_to(xt, yt); c.line_to(xh, yh); c.stroke()
    glow(c, xh, yh, 180, (1, 0.95, 0.85), 0.9 * fade)

def inksplash(c, x, y, R, k, seed=3, col=(0.03, 0.02, 0.02), a=1):
    """墨迹炸开"""
    if k <= 0: return
    r = random.Random(seed)
    c.set_source_rgba(*col, a)
    c.arc(x, y, R * 0.55 * eout(k), 0, 6.283); c.fill()
    for i in range(46):
        an = r.uniform(0, 6.283); d = R * r.uniform(0.4, 1.25) * eout(k); rr = R * r.uniform(0.02, 0.11) * (1.1 - 0.4 * k)
        c.arc(x + math.cos(an) * d, y + math.sin(an) * d * 0.7, rr, 0, 6.283); c.fill()
        if i % 3 == 0:
            c.set_line_width(rr * 0.8); c.move_to(x + math.cos(an) * d * 0.45, y + math.sin(an) * d * 0.32)
            c.line_to(x + math.cos(an) * d, y + math.sin(an) * d * 0.7); c.stroke()

def bokeh(c, lt, n=26, seed=4, col=(1, 0.7, 0.35), a=0.35):
    r = random.Random(seed)
    for i in range(n):
        x = (r.uniform(0, W) + lt * r.uniform(-25, 25)) % W; y = (r.uniform(0, H) - lt * r.uniform(5, 30)) % H
        glow(c, x, y, r.uniform(18, 60), col, a * r.uniform(0.3, 1))

def dustcloud(c, lt, y, a=0.4, col=(0.55, 0.40, 0.25), seed=6, n=18, dx=-160):
    r = random.Random(seed)
    for i in range(n):
        x = (r.uniform(-200, W + 200) + lt * dx * r.uniform(0.6, 1.4)) % (W + 400) - 200
        glow(c, x, y + r.uniform(-80, 60), r.uniform(120, 260), col, a)

def snowmts(c, base, col, seed=2, hmin=160, hmax=380, step=210, a=1, cap=(0.85, 0.86, 0.9), lit=None):
    r = random.Random(seed); x = -100
    while x < W + 200:
        s = r.uniform(hmin, hmax); w = s * r.uniform(1.1, 1.6)
        c.set_source_rgba(*col, a); c.move_to(x - w, base); c.line_to(x, base - s); c.line_to(x + w, base); c.close_path(); c.fill()
        if lit:
            c.set_source_rgba(*lit, 0.3 * a); c.move_to(x - w, base); c.line_to(x, base - s); c.line_to(x - w * 0.1, base); c.close_path(); c.fill()
        k = 0.28
        c.set_source_rgba(*cap, 0.85 * a); c.move_to(x - w * k, base - s * (1 - k)); c.line_to(x, base - s); c.line_to(x + w * k, base - s * (1 - k))
        c.line_to(x + w * k * 0.4, base - s * (1 - k * 0.7)); c.line_to(x, base - s * (1 - k * 1.1)); c.line_to(x - w * k * 0.5, base - s * (1 - k * 0.6)); c.close_path(); c.fill()
        x += step * r.uniform(0.6, 1.3)
    c.set_source_rgba(*col, a); c.rectangle(0, base - 1, W, H - base + 40); c.fill()

TONES = {
    'dusk': ((0.10, 0.04, 0.03), (0.62, 0.24, 0.08), (0.20, 0.08, 0.05), (1, 0.5, 0.2)),
    'night': ((0.02, 0.03, 0.06), (0.10, 0.12, 0.20), (0.06, 0.07, 0.10), (0.6, 0.7, 1.0)),
    'fire': ((0.08, 0.02, 0.02), (0.55, 0.12, 0.04), (0.16, 0.05, 0.03), (1, 0.4, 0.15)),
    'day': ((0.28, 0.24, 0.20), (0.66, 0.52, 0.36), (0.30, 0.22, 0.14), (1, 0.8, 0.5)),
    'snow': ((0.12, 0.14, 0.18), (0.42, 0.44, 0.48), (0.20, 0.21, 0.24), (0.9, 0.9, 1.0)),
}
def land(c, lt, tone='dusk', base=760, gy=900, sun=None, seed=2):
    top, bot, mcol, lit = TONES[tone]
    sky(c, top, bot)
    if sun: glow(c, sun[0], sun[1], 600, lit, 0.45); c.set_source_rgba(1, 0.85, 0.6, 0.9); c.arc(sun[0], sun[1], sun[2], 0, 6.28); c.fill()
    if tone == 'night': moon(c, 1500, 220, 50, 0.8)
    snowmts(c, base, mix(mcol, top, 0.3), seed, lit=lit)
    mts(c, base + 70, mix(mcol, (0, 0, 0), 0.35), seed + 3, 60, 150, 140)
    ground(c, gy, mix(mcol, (0, 0, 0), 0.6))

def fall_side(c, x, y, s, lt, k, **kw):
    c.save(); c.translate(x, y); c.rotate(-kw.get('face', 1) * 1.35 * ease(k)); c.translate(-x, -y)
    side(c, x, y, s, lt, **kw); c.restore()

def zuo_side(c, x, y, s, lt, arms='rest', face=1, lit=0.0, **kw):
    side(c, x, y, s, lt, hat='qing', beard='grey', cape_col=CAPE, cape_dark=CAPE_D, armor=False, arms=arms, robe=GUAN,
         accent=(0.85, 0.7, 0.3), lit=lit, face=face, hair_tail=False, **kw)

def liu_side(c, x, y, s, lt, arms='rest', face=1, **kw):
    side(c, x, y, s, lt, hat='qing', beard='none', cape_col=CAPE, cape_dark=CAPE_D, armor=True, arms=arms, face=face, hair_tail=False, **kw)

def foe_side(c, x, y, s, lt, arms='rest', face=-1, **kw):
    side(c, x, y, s, lt, hat='turban', beard='short', cape_col=TEAL, cape_dark=TEAL_D, armor=True, arms=arms, face=face,
         robe=(0.18, 0.20, 0.22), accent=TEAL, hair_tail=False, rim=(0.4, 0.8, 0.9), **kw)

def head_close(c, x, y, s, lt, who='zuo', face=1, a=1):
    c.save(); c.translate(x, y); c.scale(s * face, s); c.translate(0, 880)
    hat, beard, robe = ('qing', 'grey', GUAN) if who == 'zuo' else (('qing', 'none', (0.2, 0.1, 0.08)) if who == 'liu' else ('turban', 'short', (0.18, 0.2, 0.22)))
    head_side(c, lt, hat, beard, a, hair_tail=False)
    shape(c, [(-110, -790), (-30, -800), (40, -800), (90, -770), (120, -560), (-150, -560)], robe, 4, LINE, a)
    line(c, [(30, -800), (80, -620)], 3, GOLD, a)
    if who == 'zuo':   # 朝珠
        for i in range(12):
            an = 0.3 + i * 0.12; c.set_source_rgba(0.75, 0.55, 0.25, a); c.arc(30 - math.cos(an) * 60, -760 + math.sin(an) * 150, 8, 0, 6.28); c.fill()
    c.restore()

def badge(c, x, y, r, name, sub, who='zuo', lt=0, a=1, col=GOLD):
    if a <= 0: return
    c.save(); c.arc(x, y, r, 0, 6.28); c.clip()
    c.set_source_rgba(0.12, 0.08, 0.05, a); c.paint()
    glow(c, x, y + r * 0.4, r * 1.2, (1, 0.5, 0.2), 0.3 * a)
    kw = dict(zuo=('qing', 'grey'), liu=('qing', 'none'), li=('qing', 'short'), agb=('turban', 'short'), zeng=('qing', 'short'))[who]
    s = r / 150.0; c.translate(x - 10 * s, y + 880 * s + r * 0.15); c.scale(s, s)
    head_side(c, lt, kw[0], kw[1], a, hair_tail=False)
    c.restore()
    c.set_source_rgba(*col, a); c.set_line_width(4); c.arc(x, y, r, 0, 6.28); c.stroke()
    text(c, name, x, y + r + 42, 36, (1, 0.94, 0.8), a, 'c')
    if sub: text(c, sub, x, y + r + 78, 24, (0.85, 0.78, 0.62), a, 'c', shadow=False)

def cannon(c, x, y, s, lt, fires=(), face=1):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    rec = 0
    for f in fires:
        u = lt - f
        if 0 <= u < 0.3: rec = 30 * (1 - u / 0.3)
    c.save(); c.translate(-rec, 0); c.rotate(-0.22)
    shape(c, [(-60, -160), (300, -150), (300, -112), (-60, -100)], (0.20, 0.20, 0.22), 4, LINE)
    shape(c, [(-100, -175), (-30, -175), (-30, -85), (-100, -85)], (0.24, 0.22, 0.20), 4, LINE)
    for k in range(3): line(c, [(40 + k * 80, -156), (40 + k * 80, -104)], 2, GOLD, 0.7)
    c.restore()
    shape(c, [(-160, -40), (60, -120), (90, -90), (-140, 0)], (0.30, 0.20, 0.10), 4, LINE)
    c.set_source_rgba(*LINE, 1); c.set_line_width(5); c.arc(0, -40, 70, 0, 6.28); c.stroke()
    for k in range(10):
        an = k * 0.628 + lt * 0.3; line(c, [(0, -40), (math.cos(an) * 70, -40 + math.sin(an) * 70)], 3, LINE)
    c.restore()
    for f in fires:
        u = lt - f
        if 0 <= u < 0.35:
            mx, my = x + face * s * 300 * math.cos(-0.22), y + s * (-130 - 300 * math.sin(0.22))
            glow(c, mx, my, 260 * s * (1 - u / 0.35) + 30, (1, 0.8, 0.4), 1 - u / 0.35)
            for j in range(3): glow(c, mx + face * (80 + j * 90) * s * eout(u / 0.35), my - j * 20, 120 * s, (0.5, 0.45, 0.4), 0.4 * (1 - u / 0.35))

def boom(c, lt, t0, x, y, s=1.0, seed=0):
    u = lt - t0
    if not (0 <= u < 1.4): return
    k = u / 1.4
    glow(c, x, y, 500 * s * eout(u / 0.25), (1, 0.75, 0.35), 0.9 * (1 - k))
    c.set_source_rgba(1, 0.95, 0.8, max(0, 1 - u / 0.2)); c.arc(x, y, 160 * s * eout(u / 0.12), 0, 6.28); c.fill()
    r = random.Random(seed)
    for i in range(14):
        an = r.uniform(3.4, 6.0); d = 300 * s * eout(u / 0.6) * r.uniform(0.5, 1.2)
        glow(c, x + math.cos(an) * d, y + math.sin(an) * d * 0.8 - 80 * k * s, r.uniform(90, 180) * s, (0.25, 0.2, 0.18), 0.6 * (1 - k))
    for i in range(16):
        an = r.uniform(3.3, 6.1); d = 520 * s * eout(u / 0.7) * r.uniform(0.4, 1)
        c.set_source_rgba(0.15, 0.12, 0.1, 1 - k); c.rectangle(x + math.cos(an) * d, y + math.sin(an) * d + 300 * u * u, 14 * s, 10 * s); c.fill()
    ring(c, lt, t0, x, y, 800 * s)

def cavalry(c, lt, n, y, s, speed, seed, x0=W + 200, spread=2600, a=1, rim=(1, 0.55, 0.2)):
    r = random.Random(seed)
    for i in range(n):
        ph = r.uniform(0, spread); yy = y + r.uniform(-30, 40) * s * 3; ss = s * r.uniform(0.85, 1.1)
        x = (x0 - (lt * speed + ph)) % (W + 600) - 300 if speed > 0 else ((lt * -speed + ph) % (W + 600) - 300)
        glow(c, x, yy - 200 * ss, 200 * ss, rim, 0.12 * a)
        if speed > 0:
            c.save(); c.translate(x, 0); c.scale(-1, 1); c.translate(-x, 0); khorse(c, x, yy, ss, lt + i, a, 'helm'); c.restore()
        else:
            khorse(c, x, yy, ss, lt + i, a, 'helm')

def clash_bg(c, lt, tone='fire', seed=1, armies=True):
    land(c, lt, tone, 700, 940, seed=seed)
    smoke(c, lt, 760, (0.25, 0.08, 0.04) if tone != 'night' else (0.1, 0.1, 0.14), 0.35)
    if armies:
        troops(c, 2, 900, 18, 0.16, -100, 900, 'chu', lt, lt * 60, 1, dy=24)
        troops(c, 2, 900, 18, 0.16, 1020, 2020, 'agb', lt, -lt * 60, -1, dy=24)
    ground(c, 940, (0.05, 0.03, 0.02))

# ================= 镜头 =================
# 每个 S_x(c, lt, d, p, **kw)；lt 本镜秒数，d 时长，p=lt/d
def S_coffin(c, lt, d, p, tone='night'):
    land(c, lt, tone, 740, 880, seed=7)
    dustcloud(c, lt, 860, 0.18, (0.4, 0.4, 0.5) if tone == 'night' else (0.6, 0.45, 0.3))
    x = lerp(1200, 900, p)
    troops(c, 3, 880, 22, 0.14, -200, 2100, 'chu', lt, lerp(0, -120, p), -1, dy=22)
    for k in range(4):  # 抬棺人
        soldier(c, x - 150 + k * 100, 990, 0.24, 'chu', lt, False, face=-1)
    shape(c, [(x - 230, 840), (x + 230, 830), (x + 250, 880), (x - 250, 892)], (0.18, 0.08, 0.05), 4, LINE)
    shape(c, [(x - 250, 892), (x + 250, 880), (x + 240, 920), (x - 240, 930)], (0.12, 0.05, 0.03), 4, LINE)
    line(c, [(x - 330, 905), (x + 330, 890)], 6, (0.4, 0.28, 0.15))
    flag(c, 400, 860, '左', (0.70, 0.10, 0.07), lt, 320, 1.0)
    flag(c, 1600, 840, '帥', (0.70, 0.10, 0.07), lt, 300, 0.9)
    ground(c, 1000, (0.03, 0.03, 0.04))
    bokeh(c, lt, 20, col=(0.8, 0.85, 1.0) if tone == 'night' else (1, 0.7, 0.35), a=0.2)

def S_oldface(c, lt, d, p, tone='night', who='zuo'):
    top, bot, mcol, lit = TONES[tone]
    sky(c, top, bot)
    glow(c, 1400, 500, 800, lit, 0.25)
    head_close(c, lerp(1000, 960, p), 660, lerp(2.35, 2.5, p), lt, who, face=1)
    embers(c, lt, 40, a=0.5) if tone != 'night' else bokeh(c, lt, 24, col=(0.8, 0.85, 1.0), a=0.25)

def S_title(c, lt, d, p):
    land(c, lt, 'dusk', 760, 1000, sun=(1300, 520, 90), seed=4)
    troops(c, 4, 1000, 24, 0.22, -40, 1960, 'chu', lt, 0, 1, dy=32)
    for x in (150, 520, 1380, 1760): flag(c, x, 940, '左', (0.72, 0.10, 0.07), lt, 360)
    smoke(c, lt, 780, (0.3, 0.1, 0.05), 0.3)
    back(c, 1400, 1460, 1.05, lt, hat='qing', lit=1.0, arms='raise', wind=1.6, tail=False)
    speedlines(c, lt, 960, 400, 90, 0.3 * (1 - ease(lt / 1.5)) + 0.06)
    k = eout(lt / 0.3); sc = lerp(2.2, 1.0, k)
    inksplash(c, 640, 430, 420, eout(lt / 0.25), seed=11, col=(0.04, 0.02, 0.02), a=0.75)
    c.save(); c.translate(640, 470); c.scale(sc, sc)
    btext(c, "左宗棠", 0, 0, 240, (1, 0.95, 0.84), k)
    c.restore()
    c.set_source_rgba(*RED, ease((lt - 0.4) / 0.3)); c.rectangle(640 - 330 * ease((lt - 0.4) / 0.3), 530, 660 * ease((lt - 0.4) / 0.3), 8); c.fill()
    text(c, "1812 — 1885", 640, 600, 40, GOLD, ease((lt - 0.8) / 0.4), 'c')
    embers(c, lt, 90, a=0.9)

def S_exam(c, lt, d, p):
    sky(c, (0.10, 0.07, 0.05), (0.22, 0.15, 0.09))
    glow(c, 960, 500, 900, (1, 0.7, 0.4), 0.15)
    for i in range(3):
        x = 520 + i * 440; k = eout((lt - i * BP) / 0.3)
        if k <= 0: continue
        c.save(); c.translate(x, 560); c.rotate(-0.05 + i * 0.05)
        shape(c, [(-160, -300), (160, -300), (160, 300), (-160, 300)], (0.86, 0.80, 0.66), 3, (0.5, 0.4, 0.3), k)
        for j in range(8): line(c, [(-120 + j * 34, -260), (-120 + j * 34, 240)], 2, (0.3, 0.25, 0.2), 0.6 * k)
        c.restore()
        btext(c, ['道光十三年', '道光十六年', '道光十八年'][i], x, 330, 34, (0.25, 0.15, 0.1), k)
        stamp(c, "落第", x, 600, 110, lt, hit=i * BP + 0.2, rot=-0.1 + i * 0.08)
    zuo_side(c, 180, 1180, 0.55, lt, arms='hang', face=1)

def S_couplet(c, lt, d, p):
    sky(c, (0.08, 0.05, 0.04), (0.20, 0.12, 0.07))
    for x, s_, t0 in ((1560, "身无半亩心忧天下", 0.0), (360, "读破万卷神交古人", 0.5)):
        k = eout((lt - t0) / 0.5)
        shape(c, [(x - 90, 120), (x + 90, 120), (x + 90, 120 + 860 * k), (x - 90, 120 + 860 * k)], (0.62, 0.10, 0.07), 3, GOLD)
        if k > 0.5: vbrush(c, s_, x, 230, 92, (0.08, 0.05, 0.04), 1, lt - t0 - 0.2, speed=12)
    head_close(c, 960, 640, 1.8, lt, 'zuo')

def S_mufu(c, lt, d, p):
    sky(c, (0.10, 0.05, 0.04), (0.30, 0.12, 0.06))
    glow(c, 960, 560, 800, (1, 0.6, 0.3), 0.25)
    shape(c, [(260, 640), (1660, 640), (1700, 700), (220, 700)], (0.28, 0.14, 0.07), 4, LINE)  # 案
    for k in range(4): line(c, [(400 + k * 360, 700), (400 + k * 360, 980)], 10, (0.2, 0.1, 0.05))
    shape(c, [(820, 560), (1100, 560), (1100, 640), (820, 640)], (0.86, 0.80, 0.66), 3, (0.5, 0.4, 0.3))
    zuo_side(c, lerp(560, 640, ease(p)), 1100, 0.72, lt, arms='point', p=ease(p * 2), face=1)
    for x in (1400, 1600): soldier(c, x, 1000, 0.34, 'chu', lt, False, face=-1, pose='stand')
    bokeh(c, lt, 20)

def S_recruit(c, lt, d, p):
    land(c, lt, 'day', 760, 980, seed=9)
    n = int(ease(p * 1.6) * 5) + 1
    for r_ in range(n):
        troops(c, 1, 1000 - r_ * 36, 20, 0.26 - r_ * 0.03, -50, 1970, 'chu', lt, lt * 40, 1, dy=30)
    for x in (300, 960, 1620): flag(c, x, 760, '楚', (0.72, 0.10, 0.07), lt, 320)
    liu_side(c, 300, 1150, 0.6, lt, arms='point', p=1, face=1)

def S_ship(c, lt, d, p):
    sky(c, (0.06, 0.08, 0.10), (0.32, 0.30, 0.28))
    glow(c, 1400, 520, 700, (1, 0.7, 0.4), 0.3)
    c.set_source_rgba(0.06, 0.09, 0.11, 1); c.rectangle(0, 760, W, 400); c.fill()
    for k in range(10): line(c, [(0, 770 + k * 30), (W, 770 + k * 30 + math.sin(lt + k) * 4)], 2, (0.5, 0.55, 0.6), 0.2)
    x = lerp(700, 1050, eout(p))
    shape(c, [(x - 420, 700), (x + 420, 690), (x + 330, 790), (x - 360, 800)], (0.15, 0.14, 0.14), 4, LINE)
    shape(c, [(x - 120, 690), (x + 60, 690), (x + 60, 560), (x - 120, 560)], (0.25, 0.20, 0.16), 3, LINE)
    shape(c, [(x + 120, 690), (x + 170, 690), (x + 170, 520), (x + 120, 520)], (0.12, 0.12, 0.12), 3, LINE)
    for mx in (x - 260, x + 280): line(c, [(mx, 690), (mx, 330)], 6, LINE)
    for k in range(5): glow(c, x + 145 + k * 30, 500 - k * 60 - lt * 40 % 60, 60 + k * 20, (0.5, 0.5, 0.5), 0.3)
    flag(c, x - 260, 330, '船', (0.72, 0.10, 0.07), lt, 0.1, 0.9)
    for k in range(6):  # 船台吊架
        line(c, [(80 + k * 50, 760), (80 + k * 50, 300)], 4, (0.4, 0.3, 0.2))
    zuo_side(c, 1700, 1180, 0.55, lt, arms='point', p=1, face=-1)

def S_map(c, lt, d, p, cam0=(86, 41.5, 0.8), cam1=None, gold=(), red=(), routes=(), arrows_=(), badges=(), zone=None, stamps=(), ring_=(), labels=(), dim=0):
    cam1 = cam1 or cam0
    q = ease(p)
    M.set_cam(lerp(cam0[0], cam1[0], q), lerp(cam0[1], cam1[1], q), lerp(cam0[2], cam1[2], q)); M.draw(c)
    if zone:   # 势力红区：(中心名/坐标, 半径lon, 起, 止)
        for ctr, rad, t0, t1 in zone:
            k = ease((lt - t0 * BP) / ((t1 - t0) * BP))
            if k <= 0: continue
            x, y = M.P(ctr) if isinstance(ctr, str) else M.sp(*ctr)
            R = rad * M.K * M.CAM.z * k
            g = cairo.RadialGradient(x, y, 0, x, y, R); g.add_color_stop_rgba(0, 0.8, 0.1, 0.06, 0.45); g.add_color_stop_rgba(1, 0.8, 0.1, 0.06, 0)
            c.set_source(g); c.arc(x, y, R, 0, 6.28); c.fill()
    for nm, cols, t0, t1 in routes:
        M.march(c, M.path_pts(nm), ease((lt - t0 * BP) / max(0.01, (t1 - t0) * BP)), cols or (1.0, 0.82, 0.45), 6)
    for (a, b, t0, t1) in arrows_:
        (x0, y0), (x1, y1) = [M.P(n) if isinstance(n, str) else M.sp(*n) for n in (a, b)]
        M.arrow(c, x0, y0, x1, y1, ease((lt - t0 * BP) / ((t1 - t0) * BP)), RED, 22)
    for nm in gold: M.city(c, nm, 'gold', lt, size=30)
    for nm, tb in red:
        if lt >= tb * BP: M.city(c, nm, 'red', lt, size=30, ring=1)
    for nm, tb in ring_:
        if lt >= tb * BP:
            M.city(c, nm, 'gold', lt, size=34, ring=1)
            x, y = M.P(nm); ring(c, lt, tb * BP, x, y, 300, (1, 0.85, 0.5), 14)
    for s_, nm, tb, size in stamps:
        x, y = M.P(nm) if isinstance(nm, str) else nm
        stamp(c, s_, x, y - 120, size, lt, hit=tb * BP)
    for (x, y, r, name, sub, who, t0) in badges:
        badge(c, x, y, r, name, sub, who, lt, ease((lt - t0 * BP) / 0.3))
    for s_, lo, la, size, t0 in labels:
        x, y = M.sp(lo, la); btext(c, s_, x, y, size, (0.95, 0.4, 0.3), ease((lt - t0 * BP) / 0.3))

def S_vs(c, lt, d, p, focus=None):
    sky(c, (0.05, 0.04, 0.04), (0.14, 0.09, 0.06))
    # 左：海浪兵舰 右：雪山大漠
    c.save(); c.rectangle(0, 0, W / 2, H); c.clip()
    sky(c, (0.03, 0.06, 0.09), (0.12, 0.20, 0.26))
    for k in range(12): line(c, [(0, 640 + k * 34), (W / 2, 640 + k * 34 + math.sin(lt * 2 + k) * 6)], 3, (0.5, 0.65, 0.75), 0.25)
    for x in (260, 640):
        shape(c, [(x - 160, 640), (x + 160, 636), (x + 120, 690), (x - 130, 694)], (0.14, 0.14, 0.15), 3, LINE)
        line(c, [(x, 636), (x, 470)], 5, LINE)
    c.restore()
    c.save(); c.rectangle(W / 2, 0, W / 2, H); c.clip()
    land(c, lt, 'dusk', 700, 900, seed=3)
    c.restore()
    line(c, [(W / 2, 0), (W / 2, H)], 4, GOLD)
    fa = 0.35 if focus == 'zuo' else 1; fb = 0.35 if focus == 'li' else 1
    badge(c, 480, 380, 150, "李鸿章", "主张 · 海防", 'li', lt, fa * ease(lt / 0.3))
    badge(c, 1440, 380, 150, "左宗棠", "主张 · 塞防", 'zuo', lt, fb * ease((lt - 0.2) / 0.3))
    if focus is None:
        btext(c, "VS", 960, 420, 140, (0.95, 0.35, 0.25), eout(lt / 0.3))

def S_back(c, lt, d, p, tone='dusk', arms='raise', who='zuo', flags=('左',), army='chu'):
    land(c, lt, tone, 760, 1000, sun=(700, 560, 80) if tone == 'dusk' else None, seed=5)
    troops(c, 5, 1010, 28, 0.20, -40, 1960, army, lt, 0, 1, dy=30)
    for i, x in enumerate((200, 620, 1320, 1720)): flag(c, x, 960, flags[i % len(flags)], (0.72, 0.10, 0.07), lt, 380)
    smoke(c, lt, 800, (0.3, 0.12, 0.05), 0.25)
    back(c, 960, 1500, lerp(1.0, 1.06, p), lt, hat='qing', lit=1.0 if arms in ('raise', 'sword') else 0.0, arms=arms, wind=1.5, tail=False,
         cape_col=CAPE if who != 'zuo' else (0.62, 0.09, 0.06))
    embers(c, lt, 70, a=0.8)

def S_weapon(c, lt, d, p):
    sky(c, (0.04, 0.03, 0.03), (0.12, 0.08, 0.06))
    glow(c, 960, 540, 800, (1, 0.6, 0.3), 0.15)
    cannon(c, lerp(760, 820, p), 760, 2.2, lt, fires=(BP * 3,))
    # 刻度尺（学样片）
    line(c, [(480, 860), (1560, 860)], 2, GOLD, 0.7)
    for k in range(13): line(c, [(480 + k * 90, 850), (480 + k * 90, 870)], 2, GOLD, 0.7)
    text(c, "德国克虏伯后膛炮（示意）", 1560, 910, 28, (0.85, 0.78, 0.62), 1, 'r', shadow=False)
    # 掠光
    k = (lt / (BP * 2)) % 1
    glow(c, lerp(400, 1500, k), lerp(760, 520, k), 140, (1, 0.95, 0.85), 0.8)

def S_march(c, lt, d, p, tone='dusk', night=False):
    land(c, lt, tone, 740, 900, sun=(1500, 560, 70) if tone == 'dusk' else None, seed=6)
    dustcloud(c, lt, 880, 0.2)
    troops(c, 4, 960, 26, 0.2, -300 + (lt * 90) % 160, 2100, 'chu', lt, lt * 90, 1, dy=26)
    for i, x in enumerate((240, 760, 1300)): flag(c, x + (lt * 90) % 200, 870, ['左', '劉', '湘'][i], (0.72, 0.10, 0.07), lt, 340)
    # 粮车
    for k in range(5):
        x = (k * 420 + lt * 90) % (W + 400) - 200
        shape(c, [(x - 70, 1000), (x + 70, 1000), (x + 60, 960), (x - 60, 960)], (0.35, 0.22, 0.1), 3, LINE)
        c.set_source_rgba(*LINE, 1); c.set_line_width(4); c.arc(x - 40, 1010, 22, 0, 6.28); c.stroke(); c.arc(x + 40, 1010, 22, 0, 6.28); c.stroke()
    ground(c, 1030, (0.04, 0.03, 0.02))

def S_bigword(c, lt, d, p, words="缓进急战", sub=None, tone='ink'):
    sky(c, (0.03, 0.02, 0.02), (0.10, 0.06, 0.04))
    bokeh(c, lt, 30)
    n = len(words); size = 230 if n <= 4 else 170
    x0 = W / 2 - (n - 1) * size * 0.55
    for i, ch in enumerate(words):
        t0 = i * BP * (d / BP / max(n, 1)) * 0.5 if d > BP * 3 else i * BP * 0.5
        k = cl((lt - t0) / 0.18)
        if k <= 0: continue
        x = x0 + i * size * 1.1
        inksplash(c, x, 520, 220, eout(k), seed=i + 3, col=(0.30, 0.04, 0.03), a=0.55)
        sc = lerp(2.0, 1.0, eout(k))
        c.save(); c.translate(x, 600); c.scale(sc, sc); btext(c, ch, 0, 0, size, (1, 0.94, 0.82), k); c.restore()
        ring(c, lt, t0, x, 520, 420, (1, 0.8, 0.5), 12)
    if sub: text(c, sub, W / 2, 800, 40, GOLD, ease((lt - BP * 2) / 0.4), 'c')

def S_black(c, lt, d, p, s_="", sub=None):
    c.set_source_rgb(0, 0, 0); c.paint()
    k = ease(lt / 0.25)
    btext(c, s_, W / 2, 560, 96, (1, 0.94, 0.86), k)
    if sub: text(c, sub, W / 2, 660, 34, (0.8, 0.72, 0.6), k, 'c', shadow=False)

def S_duel(c, lt, d, p, var='clash', tone='fire', hero='liu', seed=1):
    """兵器对砍：clash 刀刀相撞 / cut 一刀劈倒 / parry 格挡反击 / charge 冲阵"""
    mir = seed % 2 == 1; zoom = seed % 3 == 0
    clash_bg(c, lt, tone, seed)
    hb = BP  # 节拍
    c.save()
    if mir: c.translate(W, 0); c.scale(-1, 1)
    if zoom: c.translate(960, 430); c.scale(1.45, 1.45); c.translate(-960, -380)
    hx, fx_ = 760, 1180
    if var == 'clash':
        q = cl((lt - 0.12) / (hb * 0.8))
        hx = lerp(520, 730, eout(q)); fx_ = lerp(1400, 1190, eout(q))
        hp = ease(q); fp = ease(q)
        liu_side(c, hx, 1080, 0.82, lt, arms='slash' if q > 0 else 'raise', p=hp * 0.55, stride=0.9, wind=1.8)
        foe_side(c, fx_, 1080, 0.82, lt, arms='slash' if q > 0 else 'raise', p=fp * 0.55, stride=0.9, wind=1.8)
        tc = 0.12 + hb * 0.8
        sparks(c, lt, tc, 960, 430, 90, seed, 1100)
        ring(c, lt, tc, 960, 430, 900)
        if 0 <= lt - tc < 0.08: c.set_source_rgba(1, 1, 1, 0.6); c.paint()
        speedlines(c, lt, 960, 430, 60, 0.3 * cl(1 - (lt - tc) / 0.4))
    elif var == 'cut':
        q = cl((lt - 0.08) / (hb * 0.7))
        hx = lerp(380, 900, eout(q))
        liu_side(c, hx, 1080, 0.86, lt, arms='slash', p=ease(q), stride=1.1, wind=2.0, lean=0.1)
        fk = cl((lt - 0.08 - hb * 0.7) / 0.5)
        fall_side(c, 1250, 1080, 0.82, lt, fk, arms='raise', face=-1, hat='turban', beard='short', cape_col=TEAL, cape_dark=TEAL_D,
                  armor=True, robe=(0.18, 0.20, 0.22), accent=TEAL, hair_tail=False, rim=(0.4, 0.8, 0.9), stride=0.4)
        tc = 0.08 + hb * 0.55
        slasharc(c, lt, tc - 0.12, hx + 60, 480, 520, -2.3, 0.8)
        sparks(c, lt, tc, 1180, 500, 70, seed + 2, 900, (1, 0.35, 0.2))
        inksplash(c, 1260, 520, 300, cl((lt - tc) / 0.25), seed=seed, col=(0.55, 0.05, 0.03), a=0.55 * cl(1 - (lt - tc) / 1.2))
        speedlines(c, lt, 960, 500, 70, 0.35 * cl(1 - (lt - tc) / 0.5))
    elif var == 'parry':
        q = cl(lt / (hb * 0.6)); q2 = cl((lt - hb) / (hb * 0.5))
        foe_side(c, 1160, 1080, 0.84, lt, arms='slash', p=0.25 + 0.4 * ease(q), stride=0.8, wind=1.6)
        liu_side(c, 760 + 120 * eout(q2), 1080, 0.84, lt, arms='raise' if q2 <= 0 else 'fwd', p=1, stride=0.7, wind=1.6)
        sparks(c, lt, hb * 0.6, 930, 330, 70, seed, 900)
        ring(c, lt, hb * 0.6, 930, 330, 600)
        sparks(c, lt, hb * 1.5, 1180, 460, 90, seed + 5, 1100, (1, 0.4, 0.25))
        slasharc(c, lt, hb * 1.3, 1000, 460, 420, -0.8, 0.6)
    elif var == 'charge':
        x = lerp(-200, 1100, eout(cl(lt / (d * 0.8))))
        liu_side(c, x, 1080, 0.9, lt, arms='fwd', p=1, stride=1.2, wind=2.2, lean=0.12)
        speedlines(c, lt, 1500, 500, 90, 0.4)
        for k in range(3):
            sparks(c, lt, 0.25 + k * BP, 1300 + k * 80, 520 - k * 40, 50, seed + k, 900, (1, 0.5, 0.25))
    c.restore()
    embers(c, lt, 70, a=0.8)

def S_cav(c, lt, d, p, tone='dusk', dir_=1, label=None):
    land(c, lt, tone, 720, 940, sun=(1400, 600, 90) if tone == 'dusk' else None, seed=8)
    dustcloud(c, lt, 900, 0.35, (0.6, 0.4, 0.25), dx=160 * dir_)
    cavalry(c, lt, 9, 900, 0.55, -900 * dir_, 3)
    cavalry(c, lt, 7, 1060, 0.85, -1300 * dir_, 5)
    speedlines(c, lt, 960 + 700 * dir_, 600, 60, 0.25)
    for k in range(3): flag(c, (k * 640 + lt * 600 * dir_) % (W + 300) - 150, 820, '劉', (0.72, 0.10, 0.07), lt, 300, 0.9)
    embers(c, lt, 50, a=0.6)
    arrows(c, lt, 40, 9, -0.25 if dir_ > 0 else 3.4, speed=2600)

def S_siege(c, lt, d, p, tone='fire', name="古牧地", fires=(0.2, 2.2), booms=(0.6, 2.6), night=False):
    land(c, lt, tone, 700, 900, seed=10)
    wall(c, 900, 2100, 430, 900, (0.30, 0.27, 0.24), gate=1460, gate_name=name)
    for x in (1050, 1850): flag(c, x, 404, '阿', TEAL, lt, 220)
    for tb in booms:
        boom(c, lt, tb * BP, 1300 + (tb * 97) % 400, 520 + (tb * 53) % 200, 1.0, int(tb * 10))
    smoke(c, lt, 640, (0.25, 0.1, 0.05), 0.45)
    cannon(c, 330, 1000, 1.1, lt, fires=[f * BP for f in fires])
    cannon(c, 680, 1060, 0.9, lt, fires=[(f + 0.5) * BP for f in fires])
    troops(c, 2, 1040, 10, 0.24, 80, 820, 'chu', lt, 0, 1, dy=26)
    for f in fires:   # 炮弹轨迹
        u = lt - f * BP
        if 0 <= u < 0.4:
            k = u / 0.4; x = lerp(620, 1350, k); y = lerp(820, 560, k) - 200 * math.sin(k * 3.14)
            glow(c, x, y, 50, (1, 0.8, 0.4), 1); line(c, [(x - 80, y + 20), (x, y)], 4, (1, 0.9, 0.6), 0.8)
    arrows(c, lt, 30, 6, 3.1416 - 0.4, speed=1800)
    embers(c, lt, 80, a=0.9)

def S_fallcity(c, lt, d, p, name="喀什噶尔", tone='day'):
    land(c, lt, tone, 720, 920, seed=12)
    wall(c, 100, 1820, 440, 920, (0.32, 0.29, 0.26), gate=960, gate_name=name)
    k = eout(cl((lt - BP) / (BP * 1.5)))
    for x in (380, 1540):   # 敌旗倒下、清旗升起
        c.save(); c.translate(x, 414); c.rotate(1.2 * ease(cl(lt / BP))); flag(c, 0, 0, '阿', TEAL, lt, 200, 0.8, 1 - ease(cl(lt / BP))); c.restore()
        flag(c, x + 60, 414, '清', (0.80, 0.62, 0.10), lt, 140 + 160 * k, 1.0, k)
    troops(c, 4, 1060, 26, 0.22, -40, 1960, 'chu', lt, 0, 1, dy=30)
    liu_side(c, 960, 1180, 0.62, lt, arms='raise', p=ease(cl(lt / (BP * 1.2))), wind=1.5)
    if k > 0: ring(c, lt, BP * 1.6, 960, 300, 900)
    embers(c, lt, 60, (0.9, 0.8, 0.5) and 9, a=0.7)

def S_agbdead(c, lt, d, p):
    sky(c, (0.03, 0.03, 0.05), (0.12, 0.10, 0.12))
    glow(c, 960, 560, 700, (0.4, 0.7, 0.8), 0.15)
    k = cl((lt - BP) / (BP * 1.5))
    fall_side(c, 900, 1060, 0.9, lt, k * 0.6, arms='hang', face=-1, hat='turban', beard='short', cape_col=TEAL, cape_dark=TEAL_D,
              armor=True, robe=(0.18, 0.20, 0.22), accent=TEAL, hair_tail=False, rim=(0.4, 0.8, 0.9), stride=0.2)
    if k > 0: redflash_local(c, k)

def redflash_local(c, k):
    g = cairo.RadialGradient(W / 2, H / 2, 200, W / 2, H / 2, 1100)
    g.add_color_stop_rgba(0, 0.7, 0.05, 0.03, 0); g.add_color_stop_rgba(1, 0.7, 0.05, 0.03, 0.5 * k)
    c.set_source(g); c.paint()

def S_treaty(c, lt, d, p, title="中俄伊犁条约", st="收回"):
    sky(c, (0.06, 0.04, 0.03), (0.16, 0.10, 0.06))
    k = eout(lt / 0.5)
    shape(c, [(960 - 600 * k, 200), (960 + 600 * k, 200), (960 + 600 * k, 880), (960 - 600 * k, 880)], (0.86, 0.80, 0.66), 3, GOLD)
    if k > 0.9:
        vbrush(c, title, 1380, 300, 70, (0.12, 0.08, 0.05), 1, lt - 0.5, 12)
        for j in range(6): line(c, [(1240 - j * 110, 260), (1240 - j * 110, 820)], 3, (0.3, 0.25, 0.2), 0.5)
    stamp(c, st, 760, 560, 170, lt, hit=BP * 2)
    badge(c, 300, 400, 120, "曾纪泽", "出使俄国", 'zeng', lt, ease(lt / 0.3))

def S_willow(c, lt, d, p):
    sky(c, (0.16, 0.08, 0.05), (0.80, 0.42, 0.16))
    glow(c, 960, 640, 900, (1, 0.7, 0.35), 0.5); c.set_source_rgba(1, 0.88, 0.6, 0.95); c.arc(960, 640, 80, 0, 6.28); c.fill()
    mts(c, 720, (0.30, 0.14, 0.07), 4, 60, 140, 160)
    ground(c, 760, (0.20, 0.10, 0.05))
    # 透视大道
    poly(c, [(900, 760), (1020, 760), (1500, H), (420, H)], (0.32, 0.18, 0.08))
    for side_ in (-1, 1):
        for i in range(10):
            k = (i + (lt * 0.6) % 1) / 10; s = lerp(0.12, 1.5, k ** 2.2)
            x = 960 + side_ * lerp(80, 900, k ** 2.2); y = lerp(760, 1180, k ** 2.2)
            line(c, [(x, y), (x, y - 360 * s)], 10 * s, (0.12, 0.07, 0.04))
            for j in range(9):
                an = -1.57 + (j - 4) * 0.28
                tx, ty = x + math.cos(an) * 150 * s, y - 360 * s + math.sin(an) * 150 * s
                c.set_source_rgba(0.35, 0.40, 0.18, 0.9); c.set_line_width(4 * s)
                c.move_to(tx, ty); c.curve_to(tx + math.sin(lt + j) * 20 * s, ty + 120 * s, tx, ty + 220 * s, tx + 10 * s, ty + 300 * s); c.stroke()
    vbrush(c, "新栽杨柳三千里", 1700, 160, 80, (1, 0.94, 0.82), 1, lt, 10)
    vbrush(c, "引得春风度玉关", 220, 160, 80, (1, 0.94, 0.82), 1, lt - 0.8, 10)
    bokeh(c, lt, 26)

def S_sunset(c, lt, d, p, poem=True):
    sky(c, (0.18, 0.06, 0.04), (0.85, 0.40, 0.14))
    for k in range(5): line(c, [(0, 300 + k * 70), (W, 290 + k * 70)], 30, (1, 0.7, 0.4), 0.08)
    glow(c, 960, 620, 900, (1, 0.6, 0.3), 0.55); c.set_source_rgba(1, 0.9, 0.65, 0.95); c.arc(960, 620, 110, 0, 6.28); c.fill()
    mts(c, 760, (0.16, 0.06, 0.04), 6, 80, 200, 180)
    ground(c, 800, (0.08, 0.03, 0.02))
    back(c, lerp(960, 1000, p), 1060, 0.36, lt, hat='qing', lit=0, arms='none', wind=1.2, tail=False, cape_col=(0.62, 0.09, 0.06))
    if poem:
        vbrush(c, "身无半亩", 1620, 220, 100, (1, 0.94, 0.84), 1, lt, 8)
        vbrush(c, "心忧天下", 1480, 330, 100, (1, 0.94, 0.84), 1, lt - 0.6, 8)
        vbrush(c, "读破万卷", 420, 220, 100, (1, 0.94, 0.84), 1, lt - 1.4, 8)
        vbrush(c, "神交古人", 280, 330, 100, (1, 0.94, 0.84), 1, lt - 2.0, 8)
    bokeh(c, lt, 30)

def S_end(c, lt, d, p, hit=10):
    c.set_source_rgb(0.03, 0.02, 0.02); c.paint()
    bokeh(c, lt, 36)
    k = ease(lt / 1.2)
    th = hit * BP
    sc = 1 + (0.25 * math.exp(-(lt - th) * 6) if lt >= th else 0)
    c.save(); c.translate(960, 560); c.scale(sc, sc)
    glow(c, 0, -60, 600, (1, 0.6, 0.3), 0.25 * k)
    btext(c, "左宗棠", 0, 0, 220, (1, 0.94, 0.84), k, sp=40)
    c.restore()
    text(c, "1812 — 1885 · 收复新疆", 960, 680, 40, GOLD, ease((lt - 1.0) / 0.8), 'c')
    if lt >= th:
        ring(c, lt, th, 960, 480, 1100); sparks(c, lt, th, 960, 480, 120, 9, 1400)
        embers(c, lt, 80, a=0.8)

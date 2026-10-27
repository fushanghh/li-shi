from people import *
sky = Layer(0.1)
for i, (y, col) in enumerate([(0, P['jin2']), (260, P['huang']), (420, P['zhe'])]):
    sky.poly([(0, y), (W, y), (W, H), (0, H)], col, 3)
sun = Layer(0.15); sun.ell(1400, 300, 120, 120, P['zhu'])
far = Layer(0.3)
far.poly([(0, 560)] + [(x, 470 + 50 * math.sin(x / 140) + 20 * math.sin(x / 47)) for x in range(0, W + 1, 60)] + [(W, 560), (W, H), (0, H)], P['zhe2'], 3)
smoke = Layer(0.4)
for (x, y, r) in [(300, 470, 90), (420, 420, 120), (560, 460, 80), (1500, 440, 110), (1650, 470, 90), (1000, 400, 70)]:
    for k in range(4): smoke.ell(x + k * r * 0.5, y - k * r * 0.25, r * (1 - k * 0.15), r * 0.6 * (1 - k * 0.1), (1, 1, 1, 0.75) if MODE == 'macaron' else (0.25, 0.2, 0.17, 0.55))
ground = Layer(0.5); ground.poly([(0, 640)] + [(x, 630 + 10 * math.sin(x / 90)) for x in range(0, W + 1, 80)] + [(W, 640), (W, H), (0, H)], P['zhe'], 3)
rows = [Layer(0.6), Layer(0.8), Layer(1.0)]
sp = lambda L, a, b, c_: spear(L, a, b, c_, 250)
for ri, L in enumerate(rows):
    y = 700 + ri * 110; s = 0.45 + ri * 0.12
    for k in range(6):
        x = 90 + k * 120 + ri * 40
        person(L, x, y, s, 'soldier', armF=(0.35, -1.0), holdF=sp, step=0.6 * ((k + ri) % 2 * 2 - 1), lean=0.08)
        x2 = W - 90 - k * 120 - ri * 40
        person(L, x2, y, s, 'enemy', face=-1, armF=(0.35, -1.0), holdF=sp, step=0.6 * ((k + ri) % 2 * 2 - 1), lean=0.08)
    flag(L, 70 + ri * 60, y - 420 * s - 160, 420 * s + 160, P['zhu'], '唐', wave=ri)
    flag(L, W - 70 - ri * 60, y - 420 * s - 160, 420 * s + 160, P['zi'], '突', wave=ri + 1, left=True)
arrows = Layer(0.9)
for k in range(26):
    x0 = 300 + k * 52 + rng.uniform(-30, 30); y0 = 240 + 60 * math.sin(k * 1.3)
    a = -0.25 if k % 2 else 0.25; L_ = 70
    arrows.line([(x0, y0), (x0 + L_ * math.cos(a), y0 + L_ * math.sin(a))], P['mo'], 3)
    arrows.poly([(x0 + L_ * math.cos(a), y0 + L_ * math.sin(a) - 5), (x0 + (L_ + 14) * math.cos(a), y0 + (L_ + 14) * math.sin(a)), (x0 + L_ * math.cos(a), y0 + L_ * math.sin(a) + 5)], P['tie2'], 0.2)
hero = Layer(1.25)
person(hero, 1020, 990, 0.8, 'general', armF=(2.6, -0.5), holdF=lambda L, a, b, c_: sword(L, a, b, c_, 180), expr='angry', step=0.8, lean=0.12)
person(hero, 1300, 990, 0.8, 'enemy', face=-1, armF=(2.2, -0.4), holdF=lambda L, a, b, c_: sword(L, a, b, c_, 160), expr='shock', step=0.6, lean=-0.06)
spark = Layer(1.3); CX, CY = 1160, 600
for k in range(12):
    a = k / 12 * 6.28; spark.line([(CX + 20 * math.cos(a), CY + 20 * math.sin(a)), (CX + 70 * math.cos(a), CY + 70 * math.sin(a))], P['jin2'], 5)
top = Layer(1.4)
tag(top, '六三〇年·定襄', x=1800, y=560)
caption(top, '六三〇年，李靖带三千骑兵奇袭定襄', hl=('三千骑兵',))
seal(top, '破', 1560, 860, 150, 0.12)
compose([sky, sun, far, smoke, ground] + rows + [arrows, hero, spark, top], bg=P['zhe'], light=(0.5, 0.35), vign=0.6, glow=[(1160, 600, 200, 0.35)]).save('f3m.png')

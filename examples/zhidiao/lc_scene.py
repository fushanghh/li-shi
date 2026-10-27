from linchong import *
R = np.random.default_rng(7)
# 夜空：石青由深到浅，右下被火光映红
sky = Layer(0.05)
for y, col in [(0, '#16232b'), (380, '#1f3640'), (640, '#2f4a52')]:
    sky.poly([(0, y), (W, y), (W, H), (0, H)], col, 3)
glow = Layer(0.08)
for k in range(5): glow.ell(860, 720, 420 - k * 70, 260 - k * 40, (0.72, 0.30, 0.15, 0.10 + 0.04 * k))
# 远山三层，山顶覆雪
def hills(L, base, amp, f, col, seed, snow=True):
    pts = [(x, base - amp * (0.6 + 0.4 * math.sin(x / f + seed)) - amp * 0.35 * math.sin(x / (f * 0.37) + seed * 2)) for x in range(-40, W + 81, 40)]
    L.poly([(-40, H)] + pts + [(W + 40, H)], col, 3)
    if snow:
        for i in range(1, len(pts) - 1):
            if pts[i][1] < pts[i - 1][1] and pts[i][1] < pts[i + 1][1]:
                x, y = pts[i]; L.poly([(x - 70, y + 50), (x - 30, y + 8), (x, y - 2), (x + 34, y + 10), (x + 76, y + 56), (x + 30, y + 36), (x - 10, y + 52)], P['xuan'], 1.4)
h1 = Layer(0.15); hills(h1, 560, 150, 160, '#3a5560', 1)
h2 = Layer(0.25); hills(h2, 700, 110, 120, '#2a434c', 3)
# 远处草料场在烧
fire = Layer(0.3)
for k, (x, w) in enumerate([(760, 120), (900, 150), (1010, 90)]):
    fire.poly([(x - w / 2, 780), (x - w / 2, 730), (x, 690), (x + w / 2, 730), (x + w / 2, 780)], P['mo'], 1.0)
for k in range(14):
    x = 720 + k * 25 + R.uniform(-10, 10); h = R.uniform(70, 180)
    fire.poly([(x - 24, 735), (x - 10, 735 - h * 0.6), (x, 735 - h), (x + 12, 735 - h * 0.55), (x + 24, 735)], [P['zhu'], P['huang'], P['zhu2']][k % 3], 2.0)
for k in range(8):
    x = 740 + k * 40; fire.poly([(x - 9, 732), (x, 732 - R.uniform(40, 80)), (x + 9, 732)], P['jin2'], 1.0)
smoke = Layer(0.32)
for k in range(7): smoke.ell(880 - k * 40, 640 - k * 50, 50 + k * 12, 22 + k * 5, (0.55, 0.5, 0.47, 0.35 - k * 0.03))
# 山神庙（中景左侧）+ 老松
temple = Layer(0.5)
temple.poly([(70, 900), (70, 760), (420, 760), (420, 900)], P['zhe2'], 1.2)
temple.poly([(190, 900), (190, 800), (300, 800), (300, 900)], P['mo'], 1.0)
temple.ell(245, 850, 26, 30, (0.95, 0.65, 0.25, 0.9))   # 门内一盏残火
temple.poly([(150, 728), (340, 728), (340, 770), (150, 770)], P['mo2'], 0.6)
temple.text('山神庙', 245, 760, 30, P['jin2'])
roof(temple, 245, 735, 440, 70, P['mo2'], P['zhu2'])
temple.poly([(10, 680), (120, 640), (245, 630), (370, 640), (480, 680), (420, 690), (245, 668), (70, 690)], P['bai'], 2.2)  # 屋顶积雪
pine = Layer(0.55)
pine.poly([(500, 900), (512, 600), (530, 600), (544, 900)], P['mo2'], 1.5)
for k in range(5):
    y = 560 + k * 70; w = 90 + k * 30
    pine.poly([(520 - w, y + 40), (520, y - 40), (520 + w, y + 40)], P['lv2'], 2.0)
    pine.poly([(520 - w * 0.8, y + 10), (520, y - 40), (520 + w * 0.7, y + 6), (520, y - 10)], P['bai'], 1.5)
# 雪地层层堆叠
g1 = Layer(0.6); g1.poly([(0, 900)] + [(x, 890 + 18 * math.sin(x / 110)) for x in range(0, W + 1, 60)] + [(W, H), (0, H)], P['xuan2'], 3)
g2 = Layer(0.75); g2.poly([(0, 1080)] + [(x, 1070 + 30 * math.sin(x / 160 + 1)) for x in range(0, W + 1, 60)] + [(W, H), (0, H)], P['xuan'], 3)
for k in range(5):  # 雪上脚印
    g2.ell(150 + k * 70, 1180 + k * 22, 12, 6, P['xuan3'])
# 林冲
hero = Layer(1.0); linchong(hero, 590, 1330, 1.55, wind=60)
sp = Layer(1.05); draw_spear_for(sp, 590, 1330, 1.55, wind=60)
# 风雪：斜飞的纸雪 + 墨色风线
snow = Layer(1.2)
for _ in range(220):
    x, y = R.uniform(0, W), R.uniform(0, H); r = R.uniform(2, 7)
    snow.ell(x, y, r, r * 0.8, (0.97, 0.95, 0.9, R.uniform(0.6, 1)), amp=0.3)
for _ in range(14):
    x, y = R.uniform(0, W), R.uniform(80, H - 200); l = R.uniform(120, 260)
    snow.line([(x, y), (x - l, y + l * 0.28)], P['xuan'], R.uniform(1.5, 3), 0.55)
top = Layer(1.3)
tag(top, '风雪山神庙', x=W - 80, y=70)
seal(top, '林冲', 120, 120, 120, -0.06)
compose([sky, glow, h1, h2, smoke, fire, temple, pine, g1, g2, hero, sp, snow, top], bg='#16232b', light=(0.6, 0.45), vign=0.5,
        glow=[(860, 700, 260, 0.18)]).save('lc_scene.png')

from people import *
def ridge(L, x0, x1, ybase, peaks, col, h, seed):
    r = np.random.default_rng(seed); pts = [(x0, ybase)]
    xs = np.linspace(x0, x1, peaks * 2 + 1)
    for i, x in enumerate(xs): pts.append((x + r.normal(0, 8), ybase - (h * r.uniform(0.6, 1.0) if i % 2 else h * 0.25)))
    pts.append((x1, ybase)); L.poly(pts, col, 2.0)
# 地图纸
base = Layer(0.1)
base.poly([(40, 40), (W - 40, 50), (W - 50, H - 40), (50, H - 50)], P['xuan'], 3)
sea = Layer(0.25)
river = Layer(0.3)
pts = [(1500, 60), (1480, 220), (1560, 380), (1500, 560), (1580, 720), (1520, 880), (1560, 1030)]
up = [(x - 16, y) for x, y in pts]; dn = [(x + 16, y) for x, y in pts][::-1]
river.poly(up + dn, P['qing2'], 3)
mt = [Layer(0.35), Layer(0.5), Layer(0.65)]
ridge(mt[0], 80, 700, 380, 6, P['lv2'], 150, 1); ridge(mt[0], 1620, 1880, 330, 3, P['lv2'], 120, 2)
ridge(mt[1], 120, 620, 420, 5, P['lv'], 110, 3); ridge(mt[1], 1640, 1860, 380, 2, P['lv'], 90, 4)
ridge(mt[2], 160, 520, 450, 4, P['zhe'], 70, 5); ridge(mt[2], 1660, 1840, 410, 2, P['zhe'], 60, 6)
ridge(mt[0], 60, 560, 900, 5, P['lv2'], 120, 7); ridge(mt[1], 100, 480, 930, 4, P['zhe'], 80, 8)
# 行军金线 + 地名
lab = Layer(0.4)
route = [(1750, 470), (1600, 560), (1420, 640), (1300, 700)]
for i in range(len(route) - 1):
    (x0, y0), (x1, y1) = route[i], route[i + 1]
    for u in np.arange(0, 1, 0.08): lab.ell(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 4, 4, P['jin'], amp=0.2)
lab.poly([(1300, 680), (1260, 702), (1300, 722)], P['zhu'], 0.6)
for (x, y, s) in [(1750, 470, '太原'), (300, 640, '陇西')]:
    lab.ell(x, y, 9, 9, P['zhu']); lab.text(s, x, y + 46, 34, P['mo'])
lab.text('关  中', 760, 330, 64, P['zhe2'], a=0.55); lab.text('河  东', 1760, 620, 54, P['zhe2'], a=0.55); lab.text('黄河', 1440, 300, 30, P['qing2'], vertical=True)
# 立起来的城池：折痕底座
fold = Layer(0.45)
fold.poly([(760, 760), (1180, 760), (1240, 830), (700, 830)], P['xuan3'], 1.5)
fold.line([(760, 760), (1180, 760)], P['zhe2'], 2, 0.6)
city_b = Layer(0.8)
wall(city_b, 760, 1180, 560, 760, P['xuan3'], P['zhe2'])
city_b.poly([(860, 470), (1080, 470), (1080, 560), (860, 560)], P['zhu2'], 1.0, holes=[[(880 + k * 50, 490), (910 + k * 50, 490), (910 + k * 50, 540), (880 + k * 50, 540)] for k in range(4)])
roof(city_b, 970, 470, 300, 70, tiers=2)
city_b.poly([(920, 760), (920, 680), (970, 640), (1020, 680), (1020, 760)], P['mo'], 1.0)   # 门洞
city_b.poly([(945, 600), (995, 600), (995, 630), (945, 630)], P['mo'], 0.5); city_b.text('长安', 970, 624, 22, P['jin2'])
flag(city_b, 785, 430, 130, P['huang'], '隋', wave=0, left=True); flag(city_b, 1155, 430, 130, P['huang'], '隋', wave=1)
guards = Layer(0.95)
for x in [820, 870, 1070, 1120]:
    person(guards, x, 548, 0.26, 'soldier', armF=(0.2, -1.6), holdF=lambda L, a, b, c_: spear(L, a, b, c_, 260))
army = Layer(1.1)
flag(army, 1470, 500, 330, P['zhu'], '唐', wave=2)
for k in range(5): person(army, 1250 + k * 46, 830, 0.42, 'soldier', face=-1, armF=(0.2, -1.6), holdF=lambda L, a, b, c_: spear(L, a, b, c_, 260), step=0.5)
top = Layer(1.3)
tag(top, '公元六一七年·长安', x=110, y=90)
caption(top, '地图一折，城池立起：李渊从太原一路打到长安', hl=('长安',))
seal(top, '入关', 1700, 900, 130, 0.1)
compose([base, sea, river] + mt + [lab, fold, city_b, guards, army, top], bg=P['mo2'], light=(0.5, 0.45), vign=0.7, glow=[(970, 520, 260, 0.25)]).save('f2m.png')

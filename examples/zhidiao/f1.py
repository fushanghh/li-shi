from people import *
bg = Layer(0.2); bg.poly([(0, 760), (W, 740), (W, H), (0, H)], P['xuan2'], 3)
for i in range(6): bg.line([(80 + i * 300, 762), (60 + i * 300, H)], P['xuan3'], 2, 0.5)
mid = Layer(0.6)
roles = [('emperor', dict(armF=(0.9, -1.2), expr='calm')), ('official', dict(armF=(0.5, -1.4), holdF=tablet, expr='calm')),
         ('general', dict(armF=(0.3, -1.9), holdF=lambda L, x, y, a: spear(L, x, y, a), expr='angry')),
         ('lady', dict(armF=(0.6, -1.0), expr='smile')), ('soldier', dict(armF=(0.2, -1.6), holdF=lambda L, x, y, a: spear(L, x, y, a, 280))),
         ('enemy', dict(armF=(2.5, -0.5), holdF=lambda L, x, y, a: sword(L, x, y, a), expr='angry')), ('farmer', dict(armF=(0.2, -0.4), expr='shock'))]
names = ['帝王', '文臣', '大将', '仕女', '兵卒', '敌将', '百姓']
for i, (r, kw) in enumerate(roles):
    x = 170 + i * 265; person(mid, x, 820, 1.08, r, **kw)
    mid.text(names[i], x, 900, 40, P['mo'])
top = Layer(1.0)
top.text('纸雕山河 · 人物定妆', 120, 110, 58, P['mo'], anchor='l')
top.text('中等身量 · 矿物色纸片 · 关节金铆钉 · 镂空纹样', 122, 165, 30, P['zhe2'], anchor='l', bold=False)
seal(top, '定妆', 1760, 130, 120)
compose([bg, mid, top], light=(0.45, 0.2), vign=0.45).save('f1.png')

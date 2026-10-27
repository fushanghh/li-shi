from linchong import *
bg = Layer(0.2); bg.poly([(0, 820), (W, 800), (W, H), (0, H)], P['xuan2'], 3)
mid = Layer(0.7); linchong(mid, 760, 960, 1.3, wind=40)
fr = Layer(0.8); draw_spear_for(fr, 760, 960, 1.3, wind=40)
top = Layer(1.0)
top.text('水浒 · 林冲', 120, 110, 62, P['mo'], anchor='l')
top.text('豹子头 · 八十万禁军教头', 122, 165, 32, P['zhe2'], anchor='l', bold=False)
notes = [('白范阳毡笠 · 红缨', 1240, 250), ('豹头环眼 · 燕颔虎须', 1240, 370), ('脸上金印：刺配沧州', 1240, 470), ('花枪挑酒葫芦', 1240, 600), ('石青披风 · 北风吹向身后', 1240, 720), ('白绑腿 · 皂色短打', 1240, 830)]
for t, x, y in notes:
    top.line([(x - 60, y - 14), (x - 14, y - 14)], P['zhu'], 4); top.text(t, x, y, 36, P['mo'], anchor='l')
seal(top, '林冲', 1760, 130, 130)
compose([bg, mid, fr, top], light=(0.4, 0.2), vign=0.45).save('lc_sheet.png')

# 镜头函数：s(c, lt, d) → 标记列表；lt 镜头内秒
from bgs import *

def B(lt): return lt / BEAT                    # 镜头内拍数
def stepk(lt, b0, dur=1.0): return ease((B(lt) - b0) / dur)   # 第 b0 拍开始的 0→1
def blink(t, ph=0): return 1 if (t * 0.7 + ph) % 3.1 < 0.12 else 0
def walkx(x0, lt, speed): return x0 + speed * lt
def wph(lt, off=0): return (lt / (2 * BEAT) + off) % 1     # 一拍一步

def paste(c, key, fn):
    c.set_source_surface(bg_cached(key, fn), 0, 0); c.paint()

def fall(c, x0, y0, x1, y1, k, draw):
    if k <= 0 or k >= 1: return
    x = lerp(x0, x1, k); y = lerp(y0, y1, k * k)
    c.save(); c.translate(x, y); c.rotate(k * 2); draw(c); c.restore()

def hb_small(c):
    shape(c, [(-20, -28), (20, -28), (20, 28), (-20, 28)], hx('c8322a'), 2.2, n=1); ell(c, 0, -6, 8, 8, hx('e6b84a'), 1.4)

# ---------- 现代礼金台 ----------
GUEST_Q = [dict(male=True, hair='short', body='suit', jacket=hx('3a3f4a'), shoe=hx('2a2420')),
           dict(hair='bob', body='dress', bot=hx('3f7f6a'), belt=hx('e0b040'), shoe=hx('c8322a')),
           dict(male=True, hair='short', body='suit', jacket=hx('6a5040'), tie=hx('3f6a8a'), age=1, shoe=hx('2a2420')),
           dict(hair='bob', body='dress', bot=hx('c86a8a'), belt=hx('f6f1e6'), shoe=hx('3a2a20'))]

def hall_scene(c, lt, drops, front=None, t=None):
    t = lt if t is None else t
    paste(c, 'hall', bg_hall); dyn_hall(c, t)
    # 后排宾客（坐在圆桌旁，动作错相位）
    for i, (x, y) in enumerate(((150, 780), (260, 790), (470, 760), (570, 770), (1370, 760), (1470, 770), (1690, 780), (1800, 790))):
        o = GUEST_Q[i % 4]
        fig(c, x, y, 230, dict(nsh=0.5 + 0.3 * math.sin(t * 2 + i), nel=1.0, head=0.06 * math.sin(t * 1.5 + i)), t, outline=False, flip=i % 2 == 0, sit='chair', mouth='open' if math.sin(t * 4 + i * 2) > 0.7 else 'smile', **o)
    # 记账的人（礼金台后）
    w = math.sin(t * 9) * 0.08
    fig(c, 1440, 900, 440, dict(nsh=0.9 + w, nel=1.1, fsh=0.6, fel=1.0, head=0.25), t, flip=True, hair='bob', body='dress', bot=hx('b5302a'), belt=hx('e0b040'), sit='chair', near=p_brush)
    gift_table2(c, t, drops)
    # 排队
    for i, x in enumerate((700, 480, 260)):
        o = GUEST_Q[(i + 1) % 4]
        fig(c, x, 960, 560, dict(nsh=0.05, nel=0.6, fsh=0.1, fel=0.9, head=0.08 * math.sin(t * 1.2 + i), bob=4 * math.sin(t * 2 + i)), t, blink=blink(t, i), near=p_hongbao if i == 0 else None, **o)
    return []

def gift_table2(c, t, drops):
    rect(c, 1060, 760, 1780, 790, hx('c8322a')); shape(c, [(1060, 790), (1780, 790), (1800, 1060), (1040, 1060)], hx('b5302a'), 2.6, n=1)
    for k in range(11): ink(c, [(1080 + k * 68, 800), (1070 + k * 70, 1050)], 4, hx('9a2620'), 3, 2)
    font(c, 'LXGW WenKai', 72, True); c.set_source_rgb(*hx('f2c14e')); c.move_to(1330, 950); c.show_text('礼金台')
    rect(c, 1110, 630, 1290, 762, hx('c8322a')); rect(c, 1150, 626, 1250, 638, hx('3a1a14'))
    font(c, SERIF, 76, True); tw = c.text_extents('囍')[4]; c.set_source_rgb(*hx('f2c14e')); c.move_to(1200 - tw / 2, 730); c.show_text('囍')
    shape(c, [(1340, 760), (1440, 744), (1540, 760), (1540, 768), (1340, 768)], hx('f6eedb'), 2.2, n=1); ink(c, [(1440, 744), (1440, 766)], 2, LINE, 1, 2)
    rect(c, 1336, 766, 1544, 776, hx('c8322a'), 1.6)
    rect(c, 1620, 600, 1710, 760, hx('f6f1e6')); rect(c, 1632, 616, 1698, 682, hx('2c2c34'), 1.4)
    rr = random.Random(9)
    for i in range(8):
        for j in range(8):
            if rr.random() < 0.5: c.set_source_rgb(*hx('f6f1e6')); c.rectangle(1635 + i * 8, 619 + j * 8, 7, 7); c.fill()
    label(c, '扫码随礼', 1665, 716, 20, hx('8e2c26'), bold=True)

def s_hook(c, lt, d):
    m = []
    paste(c, 'hall', bg_hall); dyn_hall(c, lt)
    for i, (x, y) in enumerate(((150, 780), (260, 790), (470, 760), (570, 770), (1370, 760), (1470, 770), (1690, 780), (1800, 790))):
        o = GUEST_Q[i % 4]
        fig(c, x, y, 230, dict(nsh=0.5 + 0.3 * math.sin(lt * 2 + i), nel=1.0, head=0.06 * math.sin(lt * 1.5 + i)), lt, outline=False, flip=i % 2 == 0, sit='chair', mouth='open' if math.sin(lt * 4 + i * 2) > 0.7 else 'smile', **o)
    fig(c, 1440, 900, 440, dict(nsh=0.9 + math.sin(lt * 9) * 0.08, nel=1.1, fsh=0.6, fel=1.0, head=0.25), lt, flip=True, hair='bob', body='dress', bot=hx('b5302a'), belt=hx('e0b040'), sit='chair', near=p_brush)
    gift_table2(c, lt, 0)
    for i, x in enumerate((560, 340, 120)):
        o = GUEST_Q[(i + 1) % 4]
        fig(c, x, 960, 540, dict(nsh=0.05, nel=0.6, fsh=0.1, fel=0.9, head=0.08 * math.sin(lt * 1.2 + i), bob=4 * math.sin(lt * 2 + i)), lt, blink=blink(lt, i), **o)
    # 前面的人：每两拍投一个红包
    b = B(lt); cyc = (b % 2) / 2; n = int(b // 2)
    reach = math.sin(min(1, cyc * 2) * math.pi) if cyc < 0.5 else 0
    out = fig(c, 860, 960, 600, dict(nsh=0.2 + 1.1 * reach, nel=0.3 - 0.2 * reach, fsh=0.1, fel=0.8, head=-0.05 + 0.1 * reach), lt, blink=blink(lt), mouth='smile',
              near=p_hongbao if cyc < 0.25 else None, **GUEST_Q[0])
    hx_, hy_ = out['hand_n']
    if 0.25 <= cyc < 0.5: fall(c, hx_, hy_, 1200, 640, (cyc - 0.25) / 0.25, hb_small)
    k = min(4, int((b - 0.5) // 2) + 1) if b > 0.5 else 0
    if k: m.append(num('¥ %d' % (200 * k), 360, 200, 120, 1, RED, 1 + 0.25 * max(0, 1 - ((b - 0.5) % 2) * 3)))
    m.append(num('本月第 3 场', 360, 80, 52, 1, INK, 1))
    return m

def s_book(c, lt, d):
    paste(c, 'hall', bg_hall); c.set_source_rgba(0.15, 0.08, 0.04, 0.55); c.paint()
    rows = [('张伟', '贰佰'), ('李娜', '伍佰'), ('王磊', '捌佰'), ('刘洋', '贰佰'), ('陈静', '壹仟'), ('赵强', '伍佰'), ('孙丽', '叁佰'), ('周杰', '陆佰')]
    k = stepk(lt, 0, 1.2); ledger_card(c, k, rows[:max(1, min(8, int(B(lt) * 1.2)))])
    m = []
    q = pop_at(lt, BEAT * 5)
    if q: m.append(num('？', 1660, 380, 260, 1, RED, q))
    return m

def s_title(c, lt, d):
    paper_bg(c, 'f0e2c0')
    k = pop_at(lt, 0, 0.5)
    beams(c, 960, 470, lt, 14, 1100, (1, .9, .6), 0.12 * k)
    c.save(); c.translate(960, 470); c.scale(k, k)
    ell(c, 0, 0, 640, 300, hx('f6ecd0'), 4); ell(c, 0, 0, 610, 274, None, 3, col=hx('c9a24a')); ell(c, 0, 0, 590, 258, None, 1.6)
    for sd in (-1, 1):
        pts = [(sd * 560, 120), (sd * 620, 0), (sd * 560, -120)] + spiral(sd * 520, -140, 30, 0, 1.0, sd, 10)[1:]
        c.set_source_rgb(*hx('c9a24a')); ribbon_path(c, dense(pts, 4), lambda q: 10 * (1 - q) + 2); c.fill()
    title(c, '随份子', 0, -70, 170, fill=hx('b5302a'), stroke=hx('f6ecd0'), sw=14, track=30)
    title(c, '从哪儿来', 0, 110, 110, fill=INK, stroke=hx('f6ecd0'), sw=10, track=24)
    c.restore()
    sparks(c, 960, 470, (lt - 0.05) / 0.9, 20, R=700)
    m = []
    if lt > BEAT * 3: m.append(num('从“货财曰赙”到今天的红包', 960, 860, 50, ease((lt - BEAT * 3) / 0.5), hx('6b4528'), 1))
    return m

# ---------- 周 ----------
ZG = [dict(male=True, hair='guan', body='robe', top=hx('e9dcc0'), bot=hx(b), belt=hx('2c2622'), beard=bd) for b, bd in (('5a4a3a', 1), ('3f5a6a', 0), ('6a4a3a', 1), ('4a5a4a', 0), ('7a5a3a', 1))]
MOURN = dict(male=True, hair='mourn', body='mourn', top=hx('eee6d2'), bot=hx('ddd2b8'), belt=hx('b8a888'), trim=None, shoe=hx('b8a888'))

def zhou_family(c, lt, x0=1000, n=3, recv=0):
    for i in range(n):
        x = x0 + i * 170
        fig(c, x, 900, 520 - i * 20, dict(nsh=0.6 + recv * 0.6 if i == 0 else 0.5, nel=1.6 - recv * 1.0 if i == 0 else 1.8, fsh=0.5, fel=1.8, head=0.25 - 0.05 * math.sin(lt + i), body=-0.1), lt,
            flip=True, sit='kneel', eyes='closed' if i else None, **MOURN)

def s_zhou1(c, lt, d):
    paste(c, 'zhou', bg_zhou); dyn_zhou(c, lt)
    zhou_family(c, lt, 1100, 3)
    props = [p_bolt, p_coins, p_bolt, p_coins]
    sp = 120
    for i in range(4):
        x = walkx(-120 - i * 220, lt, sp)
        fig(c, x, 920 + (i % 2) * 20, 560, mix(walk_pose(wph(lt, i * 0.25), 0.8), dict(nsh=0.7, nel=0.9), 1), lt, near=props[i], blink=blink(lt, i), **ZG[i])
    return [tag('丧家', (1100, 560), 'R')] if lt > 1 else []

def s_zhou2(c, lt, d):
    paste(c, 'zhou', bg_zhou); dyn_zhou(c, lt)
    k = stepk(lt, 3, 2)
    zhou_family(c, lt, 1080, 2, recv=k)
    bow = math.sin(min(1, B(lt) / 3) * math.pi / 2) * 0.22
    give = k < 0.6
    fig(c, 760, 930, 600, dict(nsh=0.9 + 0.3 * k, nel=0.4, fsh=0.9, fel=0.4, body=bow, head=0.1), lt, near=p_bolt if give else None, blink=blink(lt), **ZG[0])
    if not give:
        c.save(); c.translate(980, 760); c.rotate(-0.1); p_bolt(c); c.restore()
    fig(c, 420, 930, 580, mix(walk_pose(wph(lt), 0.4), dict(nsh=0.6, nel=1.0), 1), lt, near=p_coins, **ZG[1])
    return []

def s_zhou3(c, lt, d):
    paper_bg(c, 'e8dcc0')
    bamboo_card(c, lt / (BEAT * 3), ['货财曰赙', '舆马曰赗', '衣服曰襚', '玩好曰赠'], hl='赙')
    m = [num('《荀子·大略》', 960, 860, 52, ease(lt / 0.6), hx('6b4528'), 1)]
    q = pop_at(lt, BEAT * 5)
    if q: m.append(num('赙 = 送钱帮丧', 1560, 300, 64, 1, RED, q))
    return m

# ---------- 汉 ----------
HG = [dict(male=True, hair='guan', body='robe', top=hx('ede2c8'), bot=hx(b), belt=hx('2c2622'), beard=bd) for b, bd in (('3f5a7a', 1), ('6a3a2a', 0), ('4a6a4a', 1), ('7a6a3a', 1), ('5a3a5a', 0))]
LIUBANG = dict(male=True, hair='guan', body='robe', top=hx('f0e4c6'), bot=hx('a8402a'), belt=hx('2c2622'), trim=hx('e0b040'), beard=1.2)
XIAOHE = dict(male=True, hair='guan', body='robe', top=hx('e9dcc0'), bot=hx('2f4e6a'), belt=hx('2c2622'), beard=0.8)
LVGONG = dict(male=True, hair='guan', body='robe', top=hx('ede2c8'), bot=hx('5a4a3a'), belt=hx('c9a24a'), beard=1.4, age=1, hairc=hx('d8d2c6'))

def s_han1(c, lt, d):
    paste(c, 'han', bg_han); dyn_han(c, lt)
    lowseat_crowd(c, lt, 11, 640, 980, 1800, 6, 260)
    bowk = max(0, math.sin(B(lt) * math.pi / 2)) * 0.25
    o = fig(c, 1120, 650, 420, dict(nsh=0.9, nel=0.6, fsh=0.9, fel=0.6, body=bowk), lt, flip=True, blink=blink(lt), mouth='smile', **LVGONG)
    for i in range(5):
        x = walkx(-100 - i * 200, lt, 110)
        fig(c, x, 930 + (i % 2) * 18, 540, mix(walk_pose(wph(lt, i * 0.3), 0.8), dict(nsh=0.6, nel=1.0), 1), lt, near=p_coins, blink=blink(lt, i), **HG[i])
    return [tag('吕公', o['head'], 'L')] if lt > 0.6 else []

def plaque(c, x, y, text, k=1):
    c.save(); c.translate(x, y); c.scale(1, ease(k))
    rect(c, -50, -10, 50, 60 + len(text) * 70, hx('6b4528'), 2.6); rect(c, -40, 0, 40, 50 + len(text) * 70, hx('e2c48e'), 1.6)
    font(c, 'LXGW WenKai', 56, True)
    for j, ch in enumerate(text): c.set_source_rgb(*INK); tw = c.text_extents(ch)[4]; c.move_to(-tw / 2, 70 + j * 70); c.show_text(ch)
    c.restore()

def s_han2(c, lt, d):
    paste(c, 'han', bg_han); dyn_han(c, lt)
    plaque(c, 1420, 120, '进不满千钱', stepk(lt, 0, 1.5))
    rect(c, 820, 760, 1180, 780, hx('6b4528')); rect(c, 830, 780, 850, 880, hx('5a3a22')); rect(c, 1150, 780, 1170, 880, hx('5a3a22'))
    for k in range(6): rect(c, 860 + k * 22, 700, 876 + k * 22, 760, hx('d9bf86'), 1.4)
    pt = stepk(lt, 4, 1)
    o = fig(c, 1080, 930, 600, dict(nsh=0.9 + 0.5 * pt, nel=0.4 - 0.9 * pt, fsh=0.9, fel=1.0, head=0.08 * pt), lt, flip=True, near=p_brush if pt < 0.5 else None, blink=blink(lt), mouth='open' if 4 < B(lt) < 6 else 'closed', **XIAOHE)
    sh = stepk(lt, 4.5, 1)
    fig(c, 560 - 100 * sh, 940, 580, dict(nsh=0.9 - 0.6 * sh, nel=0.6, fsh=0.4, fel=0.6, head=-0.1 * sh, body=0.1 * sh), lt, near=p_coins, brow=sh, **HG[1])
    m = [tag('萧何', o['head'], 'R')] if lt > 0.5 else []
    q = pop_at(lt, BEAT * 5)
    if q: m.append(num('坐堂下！', 400, 300, 90, 1, RED, q))
    return m

def s_han3(c, lt, d):
    paste(c, 'han', bg_han); dyn_han(c, lt)
    b = B(lt)
    fig(c, 1300, 930, 580, dict(nsh=0.6, nel=0.6, fsh=0.5, fel=0.6, head=0.05), lt, flip=True, eyes='wide' if b > 6 else None, mouth='open' if b > 6 else 'closed', **XIAOHE)
    if b < 3:   # 摊开空手
        sh = math.sin(min(1, b / 1.5) * math.pi / 2)
        o = fig(c, 640, 940, 620, dict(nsh=0.3 + 0.9 * sh, nel=1.4 * sh, fsh=0.3 + 0.8 * sh, fel=1.3 * sh, head=-0.1 * sh), lt, mouth='smile', blink=blink(lt), **LIUBANG)
    else:
        wr = math.sin(b * math.pi * 2) * 0.12 if b < 6 else 0
        o = fig(c, 640, 940, 620, dict(nsh=1.2 + wr, nel=0.4, fsh=1.0, fel=0.9, head=0.15), lt, near=p_brush, far=p_ye, mouth='smile', **LIUBANG)
    m = [tag('刘邦', o['head'], 'L')] if lt > 0.4 else []
    if b < 3 and b > 1: m.append(num('0 钱', 640, 250, 90, 1, INK, pop_at(lt, BEAT)))
    q = pop_at(lt, BEAT * 6, 0.3)
    if q:
        m.append(num('贺钱万', 1000, 330, 200, 1, RED, q)); sparks(c, 1000, 330, (lt - BEAT * 6) / 0.8, 24, R=420)
        if lt - BEAT * 6 < 0.3: m.append(shake(10))
    return m

def s_han4(c, lt, d):
    paste(c, 'han', bg_han); dyn_han(c, lt)
    b = B(lt)
    x = max(980, 1500 - 200 * lt)
    if x > 980: o2 = fig(c, x, 930, 580, mix(walk_pose(wph(lt * 1.6), 1.2), dict(nsh=0.9, nel=0.6), 0.5), lt, flip=True, eyes='wide', mouth='open', **LVGONG)
    else:
        bw = math.sin(min(1, (b - 4) / 1.5) * math.pi / 2) * 0.35 if b > 4 else 0
        o2 = fig(c, 980, 930, 580, dict(nsh=1.0, nel=0.6, fsh=1.0, fel=0.6, body=bw), lt, flip=True, mouth='smile', **LVGONG)
    o = fig(c, 560, 940, 620, dict(nsh=0.1, nel=0.6, fsh=-0.2, fel=0.4, head=-0.08), lt, mouth='smile', blink=blink(lt), **LIUBANG)
    # 后来：吕雉
    m = []
    if b > 6:
        k = ease((b - 6) / 1.5)
        fig(c, 1300, 930, 560, dict(nsh=0.6, nel=1.6, fsh=0.5, fel=1.6, head=0.1), lt, flip=True, hair='gaoji', body='skirt', top=hx('f4ecda'), bot=hx('8a3a5a'), pibo=C['pink'], wind=0.3, mouth='smile')
        m.append(tag('吕公之女', (1290, 560), 'R'))
    return m

# ---------- 敦煌 ----------
CHAI = dict(hair='gaoji', pibo=C['pink'])
NUN = dict(hair='nun', body='skirt', top=hx('d9c7a4'), bot=hx('8a5a3a'), bot2=hx('6b4228'), belt=hx('6b4228'), kasaya=hx('a0522d'), trim=hx('c9a24a'))
DHW = [dict(hair='gaoji', top=hx('efe2c8'), bot=hx(b), pibo=hx(p), flower=hx(f)) for b, p, f in (('9a4a3a', 'e7c27a', 'f2f0e4'), ('3f6a8a', 'e6aaa5', 'e0b040'), ('6a7a3a', 'd98c8c', 'd9706a'), ('7a4a6a', 'b9cba0', 'f2f0e4'), ('b06a3a', '8fb0c8', 'd9706a'))]

def jar_p(g):
    ink(g, [(-16, 30), (0, 10), (16, 30)], 4, LINE, 3, 4)
    shape(g, [(-30, 40), (30, 40), (44, 90), (30, 130), (-30, 130), (-44, 90)], hx('7a4a2e'), 2.4)
    shape(g, [(-22, 70), (22, 70), (22, 100), (-22, 100)], hx('f1e2bb'), 1.8, n=1); label(g, '油', 0, 85, 22, LINE, bold=True)
def basket_p(g):
    ink(g, [(-40, 30), (0, -6), (40, 30)], 5, hx('8a5a30'), 3, 4)
    shape(g, [(-60, 30), (60, 30), (48, 100), (-48, 100)], hx('c9a06a'), 2.4, n=1)
    for k in range(5): ink(g, [(-50 + k * 25, 34), (-40 + k * 20, 96)], 1.6, LINE, 0.5, 3)
    shape(g, [(-56, 32), (-20, 6), (24, 4), (56, 32)], hx('f3ead6'), 2, n=4)
    for k in range(9): ell(g, -34 + k * 8, 14 + (k % 3) * 4, 3, 3, hx('e0b040'), 0)

def s_dh0(c, lt, d):
    paste(c, 'mogao', bg_mogao); dyn_mogao(c, lt)
    m = [num('莫高窟', 960, 150, 70, ease(lt / 0.8), GREEN, 1)]
    if lt > BEAT * 3: m.append(num('后周 · 公元959年', 960, 240, 48, ease((lt - BEAT * 3) / 0.5), INK, 1))
    return m

def s_dh1(c, lt, d):
    paste(c, 'yard', bg_yard); dyn_yard(c, lt)
    fig(c, 1440, 852, 510, dict(nsh=0.3, nel=0.8, fsh=0.1, fel=0.35, head=0.04 * math.sin(lt)), lt, flip=True, wind=0.1, blink=blink(lt, 1), **NUN)
    table_dh(c); oil_jar(c)
    x2 = min(420, walkx(150, lt, 70))
    fig(c, x2, 800, 430, walk_pose(wph(lt, 0.5), 0.7) if x2 < 420 else dict(nsh=0, nel=0.5, fsh=-0.3, fel=1.5), lt, far=basket_p, wind=0.5, blink=blink(lt, 2), **DHW[0])
    x = min(840, walkx(400, lt, 110))
    pose = walk_pose(wph(lt)) if x < 840 else dict(nsh=0.1, nel=0.4)
    pose.update(nel=0.35, fsh=-0.25, fel=1.6)
    o = fig(c, x, 884, 540, pose, lt, near=jar_p, far=basket_p, wind=0.6, blink=blink(lt), mouth='smile', **CHAI)
    m = []
    if lt > 0.5: m.append(tag('社人 · 柴家娘', o['head'], 'R'))
    if lt > BEAT * 4: m.append(tag('社官 · 尼功德进', (1440, 470), 'L'))
    return m

def scroll_card(c, k, lines, hl=()):
    w = 1100 * ease(k) + 40; x0 = 960 - w / 2
    rect(c, x0, 140, x0 + w, 780, hx('f3e6c4'), 2.6)
    for x in (x0 - 10, x0 + w - 10): rect(c, x, 120, x + 20, 800, hx('8a5a30'), 2)
    c.save(); c.rectangle(x0, 140, w, 640); c.clip()
    font(c, 'LXGW WenKai', 54, True); n = len(lines)
    for i, ln in enumerate(lines):
        cx = 960 + (n - 1) / 2 * 120 - i * 120
        for j, ch in enumerate(ln):
            c.set_source_rgb(*(RED if any(ch in h for h in hl) else INK)); tw = c.text_extents(ch)[4]; c.move_to(cx - tw / 2, 220 + j * 62); c.show_text(ch)
    c.restore()

def s_dh2(c, lt, d):
    paste(c, 'yard', bg_yard); c.set_source_rgba(0.2, 0.12, 0.05, 0.5); c.paint()
    scroll_card(c, lt / (BEAT * 2.5), ['显德六年己未岁', '正月三日', '女人社因兹新岁', '初来各发好意', '再立条件'], hl=('显德六年', '再立'))
    m = [num('敦煌文书 S.527', 960, 860, 46, ease(lt / 0.6), hx('f6ecd0'), 1)]
    return m

def card3(c, x, y, k, title_, amt, draw):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    rect(c, -120, -90, 120, 90, hx('f6eedb')); c.set_source_rgb(*C['gold']); c.set_line_width(3); c.rectangle(-110, -80, 220, 160); c.stroke()
    draw(c, -56, 0); label(c, title_, 40, -26, 36, LINE, bold=True); label(c, amt, 40, 28, 38, hx('8e2c26'), bold=True); c.restore()

def ic_oil(g, x, y): g.save(); g.translate(x, y - 64); g.scale(0.8, 0.8); jar_p(g); g.restore()
def ic_flour(g, x, y):
    shape(g, [(x - 30, y + 30), (x - 34, y - 20), (x - 10, y - 40), (x + 10, y - 40), (x + 34, y - 20), (x + 30, y + 30)], hx('f3ead6'), 2.2); ink(g, [(x - 14, y - 36), (x + 14, y - 36)], 4, hx('8a5a30'), 2, 3)
def ic_millet(g, x, y):
    shape(g, [(x - 34, y - 10), (x + 34, y - 10), (x + 26, y + 34), (x - 26, y + 34)], hx('c9a06a'), 2.2, n=1)
    for k in range(12): ell(g, x - 24 + (k % 6) * 10, y - 16 - (k // 6) * 8, 5, 5, hx('e0b040'), 1)

def s_dh3(c, lt, d):
    paste(c, 'yard', bg_yard); dyn_yard(c, lt)
    fig(c, 1440, 852, 510, dict(nsh=0.55, nel=1.25, fsh=0.1, fel=0.35), lt, flip=True, wind=0.1, **NUN)
    table_dh(c); oil_jar(c, 1060, 880)
    b = B(lt); tilt = stepk(lt, 1, 1.5)
    # 倒油
    o = fig(c, 820, 884, 540, dict(nsh=0.9 + 0.5 * tilt, nel=0.2, fsh=-0.25, fel=1.6, head=0.2), lt, far=basket_p, wind=0.4, mouth='smile', **CHAI)
    hx_, hy_ = o['hand_n']
    c.save(); c.translate(hx_, hy_); c.rotate(-1.6 * tilt); c.translate(0, -40); jar_p(c); c.restore()
    if tilt > 0.6:
        ink(c, [(hx_ + 60, hy_ + 20), (1040, 760), (1060, 740)], 8, hx('d9a63a'), 4, 6)
    for i in range(3):
        x = walkx(-200 - i * 200, lt, 90)
        fig(c, x, 880, 480, walk_pose(wph(lt, i * 0.3), 0.7), lt, outline=True, far=basket_p, near=jar_p if i % 2 else None, wind=0.4, blink=blink(lt, i), **DHW[i + 1])
    card3(c, 1500, 150, pop_at(lt, BEAT * 2), '油', '一合', ic_oil)
    card3(c, 1500, 350, pop_at(lt, BEAT * 3), '白面', '一斤', ic_flour)
    card3(c, 1500, 550, pop_at(lt, BEAT * 4), '粟', '一斗', ic_millet)
    m = []
    if b > 1: m.append(num('人各', 1240, 150, 80, 1, RED, pop_at(lt, BEAT * 1)))
    return m

def feast_women(c, lt, quarrel=0, scold=0):
    for i, (x, fl) in enumerate(((330, False), (620, False), (1300, True), (1560, True))):
        fig(c, x, 760, 300, dict(nsh=0.7 + 0.2 * math.sin(lt * 2 + i), nel=1.2, head=0.05 * math.sin(lt * 1.3 + i) + (0.2 * scold if True else 0)), lt, outline=False, flip=fl,
            sit='kneel', mouth='open' if (quarrel and math.sin(lt * 6 + i) > 0.4) else 'smile', eyes='wide' if scold else None, **DHW[(i + 2) % 5])

def s_dh4(c, lt, d):
    paste(c, 'feast', bg_feast); dyn_feast(c, lt)
    feast_women(c, lt, 1)
    for x in (480, 1440): low_table(c, x, 800, 260)
    b = B(lt)
    low_table(c, 960, 960, 320)
    hit = (b % 1); thr = math.sin(min(1, hit * 3) * math.pi / 2) if hit < 0.34 else 1 - (hit - 0.34)
    oL = fig(c, 700, 1010, 480, dict(nsh=1.3 * thr + 0.2, nel=0.2, fsh=0.4, fel=1.4, body=0.12 * thr, head=0.1), lt, sit='kneel', mouth='open', brow=1, **DHW[0])
    oR = fig(c, 1220, 1010, 480, dict(nsh=1.3 * (1 - thr) + 0.3, nel=0.2, fsh=0.4, fel=1.4, body=0.12 * (1 - thr), head=0.1), lt, sit='kneel', flip=True, mouth='open', brow=1, **DHW[1])
    m = []
    calls = ['叁！', '伍！', '七巧！', '八马！']
    i = int(b) % 4
    q = pop_at(lt, int(b) * BEAT, 0.25)
    if b > 1: m.append(num(calls[i], 560 if i % 2 == 0 else 1360, 380, 90, 1, RED, q))
    sp = stepk(lt, 6, 0.5)
    if sp > 0:
        c.save(); c.translate(960, 900); c.rotate(1.4 * sp); shape(c, [(-30, -10), (30, -10), (20, 14), (-20, 14)], hx('c9a06a'), 2.2, n=2); c.restore()
        for k in range(10): ell(c, 960 + k * 18 * sp, 920 + math.sin(k) * 10, 10 * sp, 5 * sp, hx('d9a63a'), 0)
        if lt - BEAT * 6 < 0.25: m.append(shake(6))
    return m

def s_dh5(c, lt, d):
    paste(c, 'feast', bg_feast); dyn_feast(c, lt)
    feast_women(c, lt, 0, 1)
    for x in (480, 1440): low_table(c, x, 800, 260)
    low_table(c, 960, 960, 320)
    pt = stepk(lt, 0.5, 1)
    o = fig(c, 1650, 1000, 560, dict(nsh=0.4 + 1.0 * pt, nel=0.1, fsh=0.1, fel=0.4, head=0.05), lt, flip=True, wind=0.1, mouth='open' if B(lt) < 4 else 'closed', brow=1, **NUN)
    fig(c, 700, 1010, 480, dict(nsh=0.5, nel=1.5, fsh=0.4, fel=1.5, head=0.35, body=0.2), lt, sit='kneel', brow=-1, **DHW[0])
    fig(c, 1220, 1010, 480, dict(nsh=0.5, nel=1.5, fsh=0.4, fel=1.5, head=0.35, body=0.2), lt, sit='kneel', flip=True, brow=-1, **DHW[1])
    m = [tag('社官', o['head'], 'L')]
    q = pop_at(lt, BEAT * 3, 0.3)
    if q:
        c.save(); c.translate(960, 330); c.scale(q, q)
        rect(c, -330, -100, 330, 100, hx('f3e6c4'), 4); rect(c, -316, -86, 316, 86, None, 2)
        title(c, '罚醴腻一筵', 0, -10, 84, fill=RED, stroke=hx('f3e6c4'), sw=6, track=10)
        label(c, '众社破用', 0, 60, 34, INK, bold=True); c.restore()
        if lt - BEAT * 3 < 0.25: m.append(shake(8))
    return m

# ---------- 明清 ----------
MG = [dict(male=True, hair='fangjin', body='robe', top=hx(a), bot=hx(a), belt=hx('2c2622'), trim=hx('e9dcc0'), beard=bd) for a, bd in (('3f6a8a', 1), ('6a5a7a', 0), ('5a7a5a', 1), ('8a5a3a', 0))]

def chair(c, x, yfeet, h, flip=False):
    u = h / 800; sd = -1 if flip else 1; sy = yfeet - 200 * u
    rect(c, x - sd * 100 * u - 14, sy - 300 * u, x - sd * 100 * u + 14, yfeet, hx('5a2e1e'))
    rect(c, x - 110 * u, sy, x + 110 * u + sd * 80 * u, sy + 22, hx('6b3a2a'))
    rect(c, x + sd * 150 * u - 10, sy + 22, x + sd * 150 * u + 10, yfeet, hx('5a2e1e'))
    rect(c, x - sd * 100 * u - 10, sy + 22, x - sd * 100 * u + 10, yfeet, hx('5a2e1e'))

def s_ming1(c, lt, d):
    paste(c, 'ming', bg_ming); dyn_ming(c, lt)
    b = B(lt)
    hold = 0 if b < 4 else 1
    chair(c, 640, 1000, 560); chair(c, 1280, 1000, 560, True)
    o1 = fig(c, 640, 1000, 560, dict(nsh=0.9, nel=1.2, fsh=0.4, fel=0.8), lt, sit='chair', mouth='open' if b < 3 else 'smile', blink=blink(lt), **MG[0])
    o2 = fig(c, 1280, 1000, 560, dict(nsh=1.0 + 0.2 * math.sin(lt * 8) * hold, nel=0.6, fsh=0.4, fel=0.8), lt, sit='chair', flip=True, near=p_brush if hold else None, mouth='smile', **MG[1])
    fig(c, 300, 1030, 600, dict(nsh=0.5, nel=0.8, head=0.05), lt, blink=blink(lt, 2), **MG[2])
    fig(c, 1650, 1030, 600, dict(nsh=0.5, nel=0.8, head=0.05), lt, flip=True, **MG[3])
    k = stepk(lt, 1, 1.5)
    fenzi_list(c, 960, 380, k, [('王兄', '五钱'), ('李兄', '三钱'), ('赵兄', '三钱')][:1 + int(max(0, b - 2) // 1.5)])
    return []

def s_ming2(c, lt, d):
    paper_bg(c, 'efe2c4')
    k = stepk(lt, 0, 1)
    c.save(); c.translate(960, 470); c.scale(1.2, 1.2); c.translate(-960, -470)
    fenzi_list(c, 680, 200, k, [('王兄', '五钱'), ('李兄', '三钱'), ('赵兄', '三钱'), ('钱兄', '二钱')])
    c.restore()
    m = []
    q = pop_at(lt, BEAT * 2); 
    if q: m.append(num('凑份子', 1400, 300, 110, 1, RED, q))
    q = pop_at(lt, BEAT * 3)
    if q: m.append(num('出份子', 1400, 480, 110, 1, RED, q))
    if lt > BEAT * 4: m.append(num('《牡丹亭》《儒林外史》', 1400, 650, 44, ease((lt - BEAT * 4) / 0.5), hx('6b4528'), 1))
    return m

# ---------- 红楼梦 ----------
JIAMU = dict(hair='grey', body='aoqun', top=hx('6a4a7a'), bot=hx('3a3050'), trim=hx('e0b040'), age=1, sit='chair')
FENGJIE = dict(hair='wanji', body='aoqun', top=hx('c8322a'), bot=hx('3f6a8a'), trim=hx('e0b040'), flower=hx('e0b040'))
LADIES = [dict(hair='wanji', body='aoqun', top=hx(a), bot=hx(b), trim=hx('e0b040'), age=ag) for a, b, ag in (('8a6a4a', '4a4a3a', 1), ('5a6a8a', '3a3a4a', 1), ('7a5a3a', '5a3a2a', 1))]
MAIDS = [dict(hair='wanji', body='aoqun', top=hx(a), bot=hx(b), trim=hx('f3ead6')) for a, b in (('8fb0a0', '5a7a6a'), ('d98c8c', '8a5a5a'), ('a9c39a', '6a7a5a'), ('e6c66a', '8a6a3a'))]

def s_hl1(c, lt, d):
    paste(c, 'jia', bg_jia); dyn_jia(c, lt)
    b = B(lt); r = stepk(lt, 1, 1)
    o = fig(c, 900, 760, 520, dict(nsh=0.5 + 1.0 * r, nel=0.6 - 0.4 * r, fsh=0.6, fel=1.0, head=0.05), lt, mouth='open' if 1 < b < 4 else 'smile', blink=blink(lt), **JIAMU)
    for i, x in enumerate((420, 560, 1500 + 120)):
        fig(c, x, 1000 if i < 2 else 1000, 580, dict(nsh=0.6, nel=1.6, fsh=0.5, fel=1.6, head=0.06 * math.sin(lt + i)), lt, flip=i == 2, blink=blink(lt, i), mouth='smile', **LADIES[i])
    of = fig(c, 1300, 1000, 600, dict(nsh=0.3 + 0.2 * math.sin(lt * 3), nel=1.2, fsh=0.6, fel=1.6, head=-0.1), lt, flip=True, mouth='smile', blink=blink(lt, 3), **FENGJIE)
    m = []
    if lt > 0.4: m.append(tag('贾母', o['head'], 'L'))
    if lt > BEAT * 3: m.append(tag('王熙凤', of['head'], 'R'))
    return m

def s_hl2(c, lt, d):
    paste(c, 'jia', bg_jia); dyn_jia(c, lt)
    fig(c, 900, 760, 520, dict(nsh=0.6, nel=0.6, fsh=0.6, fel=1.0), lt, mouth='smile', **JIAMU)
    rect(c, 760, 860, 1160, 880, hx('5a2218')); rect(c, 780, 880, 800, 1040, hx('4a1a14')); rect(c, 1120, 880, 1140, 1040, hx('4a1a14'))
    b = B(lt); n = 0; m = []
    who = [('贾母 二十两', 1), ('薛姨妈 二十两', 1), ('邢夫人 十六两', 1), ('王夫人 十六两', 1)]
    for i, (txt, _) in enumerate(who):
        q = pop_at(lt, BEAT * (1 + i * 1.5))
        if q:
            n += 4 if i < 2 else 3
            m.append(num(txt, 960 + (-560 if i % 2 == 0 else 560), 200 + (i // 2) * 170, 70, 1, RED if i < 2 else BLUE, q))
    silver_pile(c, 960, 850, n)
    for i, x in enumerate((420, 1500)):
        fig(c, x, 1030, 580, dict(nsh=0.9 if b > 1 + i * 3 else 0.6, nel=0.6, fsh=0.5, fel=1.6), lt, flip=i == 1, near=p_silver if b > 1 + i * 3 else None, mouth='smile', **LADIES[i])
    return m

def s_hl3(c, lt, d):
    paste(c, 'jia', bg_jia); dyn_jia(c, lt)
    fig(c, 900, 760, 520, dict(nsh=0.6, nel=0.6, fsh=0.6, fel=1.0), lt, mouth='smile', **JIAMU)
    rect(c, 760, 860, 1160, 880, hx('5a2218')); rect(c, 780, 880, 800, 1040, hx('4a1a14')); rect(c, 1120, 880, 1140, 1040, hx('4a1a14'))
    b = B(lt)
    silver_pile(c, 960, 850, 14 + min(7, int(b)))
    for i in range(4):
        x = min(700 - i * 0, walkx(-100 - i * 180, lt, 160))
        x = min(x, 680 - i * 170)
        fig(c, x, 1030, 520, walk_pose(wph(lt, i * 0.25), 0.7) if x < 680 - i * 170 else dict(nsh=0.9, nel=0.4), lt, near=p_silver, blink=blink(lt, i), mouth='smile', **MAIDS[i])
    fig(c, 1350, 1030, 600, dict(nsh=0.3, nel=1.0, fsh=0.6, fel=1.6, head=-0.1 + 0.05 * math.sin(lt * 3)), lt, flip=True, mouth='smile', **FENGJIE)
    return [num('人人有份', 1420, 230, 90, 1, RED, pop_at(lt, BEAT * 4))] if b > 4 else []

# ---------- 民国 ----------
MGG = [dict(male=True, hair='guapi', body='changshan', top=hx(a), bot=hx(a), bot2=tuple(v * 0.8 for v in hx(a)), shoe=hx('2a2420'), magua=hx(mg) if mg else None) for a, mg in (('4a6a7a', '2c2622'), ('7a6a5a', None), ('5a5a7a', '2c2622'), ('8a7a5a', None))]
ACCT = dict(male=True, hair='guapi', body='changshan', top=hx('5a6a6a'), bot=hx('5a6a6a'), shoe=hx('2a2420'), beard=0.6, age=1, sit='chair')

def s_mg1(c, lt, d):
    paste(c, 'minguo', bg_minguo); dyn_minguo(c, lt)
    b = B(lt)
    fig(c, 1340, 880, 520, dict(nsh=1.0 + 0.1 * math.sin(lt * 9), nel=0.7, fsh=0.8, fel=1.0, head=0.2), lt, flip=True, near=p_brush, blink=blink(lt), **ACCT)
    zhang_table(c, 1250, 800)
    for i in range(4):
        x = min(860 - i * 200, walkx(-200 - i * 200, lt, 160))
        moving = x < 860 - i * 200
        fig(c, x, 980, 580, walk_pose(wph(lt, i * 0.3), 0.8) if moving else dict(nsh=0.9 if i == 0 else 0.4, nel=0.5), lt, near=p_book if i != 1 else p_hongbao,
            blink=blink(lt, i), mouth='smile', **MGG[i])
    return [tag('账房先生', (1340, 420), 'R')] if lt > 1 else []

def s_mg2(c, lt, d):
    paste(c, 'minguo', bg_minguo); c.set_source_rgba(0.2, 0.08, 0.04, 0.5); c.paint()
    rows = [('王府', '大洋二元'), ('李宅', '大洋一元'), ('赵三爷', '大洋四元'), ('孙家', '大洋二元'), ('钱府', '大洋三元'), ('周家', '大洋一元')]
    ledger_card(c, stepk(lt, 0, 1), rows[:max(1, min(6, int(B(lt) * 1.5)))])
    m = []
    q = pop_at(lt, BEAT * 5)
    if q:
        m.append(num('有来有往', 1660, 420, 70, 1, RED, q))
    return m

# ---------- 今天 ----------
def s_md1(c, lt, d):
    paste(c, 'hall', bg_hall); dyn_hall(c, lt)
    fig(c, 1440, 900, 440, dict(nsh=0.9 + math.sin(lt * 9) * 0.08, nel=1.1, fsh=0.6, fel=1.0, head=0.25), lt, flip=True, hair='bob', body='dress', bot=hx('b5302a'), belt=hx('e0b040'), sit='chair', near=p_brush)
    gift_table2(c, lt, 0)
    r = stepk(lt, 1, 1)
    o = fig(c, 1360, 980, 620, dict(nsh=0.5 + 1.0 * r, nel=0.6 - 0.3 * r, fsh=0.4, fel=1.4, head=0.1 + 0.1 * r), lt, near=p_phone, blink=blink(lt), **GUEST_Q[1 + 1])
    m = []
    q = pop_at(lt, BEAT * 3, 0.3)
    if q:
        glow(c, 1665, 650, 140 * q, (1, .9, .5), 0.6)
        m.append(num('叮！+500', 1620, 420, 80, 1, RED, q))
    fig(c, 500, 980, 600, dict(nsh=1.0, nel=0.4, head=0.0), lt, near=p_hongbao, blink=blink(lt, 2), **GUEST_Q[1])
    return m

def s_md2(c, lt, d):
    paste(c, 'hall', bg_hall); c.set_source_rgba(0.35, 0.1, 0.06, 0.45); c.paint()
    b = B(lt)
    rr = random.Random(7)
    for i in range(16):   # 请柬飞落
        x = rr.uniform(100, 1820); y = (rr.uniform(-400, 0) + lt * rr.uniform(120, 220)) % 1300 - 200; a = lt * rr.uniform(-2, 2)
        c.save(); c.translate(x, y); c.rotate(a); rect(c, -50, -34, 50, 34, hx('c8322a')); label(c, '囍', 0, 0, 36, hx('f2c14e'), fam=SERIF, bold=True); c.restore()
    sweat = 0.06 * math.sin(lt * 20)
    o = fig(c, 960, 1040, 700, dict(nsh=0.9, nel=2.2, fsh=0.9, fel=2.2, head=0.25 + sweat, body=0.06), lt, brow=-1.2, mouth='open', male=True, hair='short', body='suit', jacket=hx('3a3f4a'), shoe=hx('2a2420'))
    vals = ['¥200', '¥500', '¥800', '¥1000', '¥2000']
    i = min(4, int(b // 1.5)); q = pop_at(lt, i * 1.5 * BEAT, 0.25)
    m = [num(vals[i], 960, 220, 150 + i * 20, 1, RED, q)]
    if i >= 3 and (lt - i * 1.5 * BEAT) < 0.2: m.append(shake(5 + i))
    return m

def s_md3(c, lt, d):
    paste(c, 'yard', bg_yard); dyn_yard(c, lt)
    c.set_source_rgba(1, 0.85, 0.5, 0.12); c.paint()
    fig(c, 1440, 852, 510, dict(nsh=0.55, nel=1.25, fsh=0.4, fel=1.0), lt, flip=True, wind=0.1, mouth='smile', **NUN)
    table_dh(c); oil_jar(c)
    for i in range(4):
        x = walkx(80 + i * 190, lt, 80) if i else walkx(260, lt, 80)
        fig(c, x, 880 + (i % 2) * 10, 500, walk_pose(wph(lt, i * 0.27), 0.7), lt, far=basket_p if i % 2 == 0 else None, near=jar_p if i % 2 else None, wind=0.5, mouth='smile', blink=blink(lt, i), **(CHAI if i == 0 else DHW[i]))
    return []

def s_end(c, lt, d):
    m = s_hook(c, lt, d)
    m = [x for x in m if not (x[0] == 'num')]
    k = ease((lt - BEAT * 6) / 1.0)
    if k > 0: m.append(num('随份子', 960, 300, 140, k, RED, 1))
    return m

import math, random
from head import *
from head import SC
from dy import *
from fx import t_ladder, horse_rider

WJ = dict(hatk='helmet', robe=(0.70, 0.20, 0.16), collar='round')     # 王坚
SONGB = dict(hatk='helmet', robe='soldier', collar='round')
YUJIE = dict(hatk='futou_song', robe='red_off', collar='round')
RAN = dict(hatk='fangjin', robe='blue', collar='v')
WATER = (0.62, 0.86, 1.0)
FIELD = (0.72, 0.92, 0.52)

S_YS = '《元史》卷三·宪宗纪'
S_SS = '《宋史》卷四百十六·余玠传'
S_JL = '据无名氏《钓鱼城记》（《四川通志》卷四十引）'
S_ZZ = '重庆市地方志办公室《独钓中原一座城》'

WP = MAPJ['wide']['pts']
LP = MAPJ['local']['pts']
DY = LP['钓鱼城']
ROUTE = ['六盘山', '散关', '汉中', '利州', '阆中', '合州']


def wp(k):
    return WP[k]


# ================================================================ 1 钩子（暮色+崖城）——第0帧标题即在
@shot(5.0, S_YS)
def s01(c, t):
    mesa_bg(c, t)
    fortress(c, 1250, 900, 0.95, 1.0, t)
    river_band(c, t, 880, 200)
    shore(c, 990)
    for i in range(4):
        cavalry(c, lerp(-150, 120 + i * 120, eout(seg(t, 0, 1.3))), 1040 + (i % 2) * 25, 0.5, t, run=t * 2 if t < 1.3 else 0)
    hit = t > 2.0
    if 1.8 < t < 2.1:
        bx = lerp(1250, 800, seg(t, 1.8, 2.05)); by = lerp(480, 820, seg(t, 1.8, 2.05))
        c.arc(bx, by, 20, 0, TAU); rgba(c, (0.62, 0.60, 0.58)); c.fill()
    rec(1.8, 'boom')
    mengge(c, 820, 1070, 0.8, t, expr='shock' if hit else 'calm', pose='hold' if hit else 'point', sw=hit, shake=0.15 if hit else 0)
    sticker(c, '啊？！', 980, 560, t, 2.1, 96, YEL, 0.12)
    stamp(c, '帝崩', 1600, 640, t, 2.9, 110, RED, -0.18)
    caption(c, t, '1259年，蒙古大汗蒙哥', '死在了一座小山城下', REDL, instant=True)


# ================================================================ 2 问题
@shot(5.0, S_ZZ)
def s02(c, t):
    mesa_bg(c, t)
    fortress(c, 1300, 900, 0.9, 1.0, t)
    river_band(c, t, 880, 200)
    shore(c, 990)
    bignum(c, '36', 560, 640, 260, t, 0.6, GOLDL, '年 · 1243—1279', usize=56)
    chibi(c, 1700, 1060, 0.75, **SONGB, expr='happy', pose='cheer', T=t, name='守军', label_pre='钓鱼城')
    sticker(c, '还没打下来', 640, 860, t, 1.6, 66, YEL, -0.08)
    caption(c, t, '这座城前后守了', '36年，凭什么？', GOLDL)


# ================================================================ 3 选址：冉氏兄弟（暖黄）
@shot(6.0, S_SS)
def s03(c, t):
    vgrad(c, 0, H, (0.40, 0.28, 0.18), (0.62, 0.46, 0.30))
    c.rectangle(0, 900, W, 180); rgba(c, (0.34, 0.24, 0.16)); c.fill()
    dust(c, t, 5, 30, (1, 0.9, 0.7), 0.3)
    p = seg(t, 0.4, 3.0)
    c.save(); c.translate(1300, 930); c.scale(1, 0.32)
    c.set_line_width(10); rgba(c, (0.98, 0.96, 0.90), 0.9)
    pts = [(-420 + i * 30, math.sin(i * 0.5) * 160 - 60) for i in range(int(29 * p))]
    if len(pts) > 1:
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.stroke()
    if p > 0.6:
        c.move_to(-120, -300); c.line_to(-60, -420); c.line_to(0, -300); c.close_path(); c.stroke()
        c.arc(-60, -360, 30, 0, TAU); c.stroke()
    c.restore()
    for i in range(2):
        chibi(c, 1400 + i * 400, 900, 0.8, **RAN, expr='calm' if t < 2.5 else 'happy', pose='point', T=t + i, name='冉琎' if i == 0 else '冉璞', label_pre='播州')
    chibi(c, 1060, 960, 0.85, **YUJIE, expr='shock' if t > 3 else 'calm', pose='hold', T=t, sw=t > 3, name='余玠', label_pre='四川制置使')
    sticker(c, '画地为图！', 1560, 220, t, 2.4, 70, YEL, -0.08)
    quote(c, t, 1.0, '以堊畫地為山川城池之形。', '兄弟俩用白土在地上画出山川、城池的样子。', S_SS, x=60, y=990, w=780)
    caption(c, t, '1243年前后，冉氏兄弟献策：', '城要筑在山上', GOLDL)


# ================================================================ 4 十万师
@shot(5.5, S_SS)
def s04(c, t):
    vgrad(c, 0, H, (0.40, 0.28, 0.18), (0.62, 0.46, 0.30))
    c.rectangle(0, 900, W, 180); rgba(c, (0.34, 0.24, 0.16)); c.fill()
    fortress(c, 1550, 900, 0.55, 1.0, t)
    bignum(c, '10万', 1550, 360, 150, t, 1.8, GOLDL, '大军也比不上', usize=48)
    chibi(c, 1080, 940, 0.85, **YUJIE, expr='happy', pose='cheer', T=t, name='余玠', label_pre='四川制置使')
    quote(c, t, 0.4, '蜀口形勝之地莫若釣魚山……積粟以守之，賢於十萬師遠矣。', '四川最险要的地方就是钓鱼山；在那儿存够粮食守着，比十万大军还管用。', S_SS, x=60, y=990, w=860, osize=40, psize=36)
    caption(c, t, '守住钓鱼山，', '顶得上十万兵', GOLDL)


# ================================================================ 5 三江环抱（真实高程）
@shot(6.0, S_JL)
def s05(c, t):
    cx, cy, vw = campath(t, [(0, 1573, 1211, 3146), (2.8, 1650, 1180, 2700)])
    f = mapview(c, 'local', cx, cy, vw, 1.0, 0.10)
    for i, (nm, px, py) in enumerate((('嘉陵江', 1888, 1040), ('渠江', 2525, 820), ('涪江', 600, 1082))):
        x, y = f(px, py)
        goldlabel(c, nm, x, y, fin(t, 0.5 + i * 0.45), 54, WATER)
        rec(0.5 + i * 0.45, 'pop')
    x, y = f(*DY)
    pin(c, x, y, t, 2.0, REDL, 16)
    if t > 2.0:
        goldlabel(c, '钓鱼城', x + 10, y + 95, fin(t, 2.1), 58, REDL)
    hx, hy = f(*LP['合州旧城'])
    if t > 2.6:
        goldlabel(c, '合州城', hx, hy + 80, fin(t, 2.6), 40, GREY)
    note(c, '底图：真实高程渲染（AWS Terrarium），蓝色为江面', t, 80, 1040)
    quote(c, t, 3.0, '山三面據宕渠、嘉陵二江……與涪江會同。', '山的三面靠着渠江、嘉陵江，又和涪江汇合。', S_JL, x=1060, y=990, w=820, osize=38, psize=34)
    caption(c, t, '答案先给：地形。', '三条江在这儿汇合', GOLDL)


# ================================================================ 6 三面据江
@shot(5.5, S_JL)
def s06(c, t):
    cx, cy, vw = campath(t, [(0, 1650, 1180, 2700), (1.8, DY[0] - 80, DY[1] - 90, 1450)])
    f = mapview(c, 'local', cx, cy, vw, 1.0, 0.10)
    x, y = f(*DY)
    pin(c, x, y, t, 0.0, REDL, 16)
    redcircle(c, x, y, 230, 190, t, 1.6)
    for i, (dx, dy_, nm) in enumerate(((0, -100 * 2, '北面·江'), (215 * 2, 0, '东面·江'), (0, 40 * 2, '南面·江'))):
        q = fin(t, 2.2 + i * 0.3)
        rec(2.2 + i * 0.3, 'pop')
        tx, ty = f(DY[0] + dx, DY[1] + dy_)
        tagbox(c, nm, tx, ty + 14, q, WATER, 42)
    tagbox(c, '西面·陆路', x - 400, y - 60, fin(t, 3.2), GOLDL, 40)
    quote(c, t, 0.8, '其東南北三面據江，皆峭壁懸巖。', '东、南、北三面都是江，岸边全是悬崖峭壁。', S_JL, x=60, y=1000, w=720, osize=42, psize=38)
    caption(c, t, '三面是江，', '敌人只能从一面来', GOLDL)


# ================================================================ 7 千仞悬崖
@shot(5.0, S_JL)
def s07(c, t):
    mesa_bg(c, t)
    fortress(c, 1250, 900, 1.05, 1.0, t)
    river_band(c, t, 880, 200)
    shore(c, 990)
    for i in range(3):
        x = lerp(200 + i * 150, 560 + i * 120, eout(seg(t, 0.2, 1.4)))
        cavalry(c, x, 1050, 0.55, t, run=t * 2 if t < 1.4 else 0)
    label(c, '峭壁', 1760, 620, t, 1.0, GOLDL, 52, 1620, 700)
    label(c, '大江', 900, 940, t, 1.4, WATER, 52)
    sticker(c, '马冲不上去！', 560, 600, t, 2.0, 78, YEL, -0.1)
    quote(c, t, 2.4, '其山髙千仞。', '山高得吓人，"千仞"是形容极高。', S_JL, x=1040, y=990, w=820)
    caption(c, t, '四周是悬崖，', '蒙古骑兵用不上', GOLDL)


# ================================================================ 8 八座城门
@shot(5.0, S_JL)
def s08(c, t):
    mesa_bg(c, t, ((0.10, 0.10, 0.16), (0.34, 0.26, 0.26)))
    FS = 0.95
    fortress(c, 960, 1010, FS, 1.0, t, flags=False)
    top = 1010 - 420 * FS
    for i in range(8):
        gx = 960 - 340 * FS + i * (680 * FS) / 7
        tt = 0.4 + i * 0.22
        p = back(seg(t, tt, tt + 0.3))
        if p <= 0.01:
            continue
        rec(tt, 'pop')
        c.save(); c.translate(gx, top - 120); c.scale(p, p)
        rr(c, -34, -40, 68, 70, 8); rgba(c, (0.62, 0.22, 0.16)); c.fill()
        c.move_to(-48, -40); c.line_to(0, -76); c.line_to(48, -40); c.close_path(); rgba(c, (0.24, 0.24, 0.30)); c.fill()
        c.arc(0, 10, 16, math.pi, 0); c.line_to(16, 30); c.line_to(-16, 30); c.close_path(); rgba(c, (0.12, 0.08, 0.06)); c.fill()
        text(c, str(i + 1), 0, -96, 40, WHITE, 1, align='c')
        c.restore()
    bignum(c, '8', 1660, 560, 200, t, 2.4, GOLDL, '座城门', usize=54)
    quote(c, t, 2.6, '城之門有八。', '这座城一共有八座城门。', S_JL, x=60, y=990, w=640)
    caption(c, t, '崖顶一圈城墙，', '八座城门把住各条山路', GOLDL)


# ================================================================ 9 天池
@shot(5.5, S_JL)
def s09(c, t):
    mesa_bg(c, t, ((0.16, 0.22, 0.24), (0.50, 0.56, 0.44)))
    fortress(c, 1150, 1060, 1.1, 1.0, t, walls=1.0, flags=False, inner=1.0)
    label(c, '天池', 1560, 400, t, 0.6, WATER, 50, 1500, 575)
    label(c, '水田', 800, 400, t, 1.0, FIELD, 50, 820, 575)
    sticker(c, '大旱也不干', 1700, 300, t, 2.2, 62, YEL, 0.08)
    quote(c, t, 1.4, '因溝為池……名曰天池，泉水汪洋，旱亦不涸，池中魚鱉可掉舟舉網。', '把山沟围成水池叫天池，大旱也不干，池里的鱼鳖多到能划船撒网。', S_JL, x=60, y=990, w=1000, osize=40, psize=36)
    caption(c, t, '光险不够，还得有水：', '山顶有个天池', WATER)


# ================================================================ 10 小池+井（数据卡）
@shot(5.0, S_JL)
def s10(c, t):
    databg(c, t)
    panel(c, 200, 330, 680, 440, fin(t, 0.2), edge=WATER)
    panel(c, 1040, 330, 680, 440, fin(t, 0.6), edge=WATER)
    bignum(c, '13', 540, 560, 210, t, 0.4, WATER, '处小水池', usize=56)
    bignum(c, '92', 1380, 560, 210, t, 0.9, WATER, '眼水井', usize=56)
    for i in range(int(46 * eout(seg(t, 1.1, 2.4)))):
        cx, cy = 1110 + (i % 23) * 24, 710 + (i // 23) * 26
        c.arc(cx, cy, 8, 0, TAU); rgba(c, WATER, 0.8); c.fill()
    quote(c, t, 1.8, '又開小池十有三所，井九十二眼。', '又挖了十三处小水池、九十二眼井。', S_JL, x=200, y=990, w=1100)
    caption(c, t, '除了天池，还有：', '13个水池、92眼井', WATER)


# ================================================================ 11 春耕秋守
@shot(5.5, S_JL)
def s11(c, t):
    mesa_bg(c, t, ((0.16, 0.22, 0.24), (0.50, 0.56, 0.44)))
    c.rectangle(0, 860, W, 220); rgba(c, (0.40, 0.48, 0.26)); c.fill()
    autumn = t > 2.6
    for i in range(3):
        x = 900 + i * 300
        chibi(c, x, 980, 0.75, **(SONGB if autumn else dict(hatk='douli', robe='brown', collar='v')), expr='happy' if not autumn else 'angry',
              pose='hold' if not autumn else 'raise', prop='basket' if not autumn else 'sword', T=t + i)
    tagbox(c, '春：出城种地' if not autumn else '秋：收粮守城', 1200, 420, 1.0, FIELD if not autumn else REDL, 60)
    rec(2.6, 'pop')
    quote(c, t, 0.4, '春則出屯四野以耕以耘，秋則收糧運薪以戰以守。', '春天出城去种地，秋天收了粮、运了柴，回城打仗守城。', S_JL, x=60, y=990, w=700, osize=40, psize=36)
    caption(c, t, '城里的人', '春天种地，秋天打仗', FIELD)


# ================================================================ 12 攻方：补给线漫长（广域路线）
@shot(6.0, S_YS)
def s12(c, t):
    cx, cy, vw = campath(t, [(0, 850, 470, 1700), (3.6, 850, 1100, 1700)])
    f = mapview(c, 'wide', cx, cy, vw, 1.0, 0.12)
    pts = [f(*wp(k)) for k in ROUTE]
    dashroute(c, pts, seg(t, 0.4, 3.6), (0.95, 0.25, 0.2), 7, 1.0, t)
    for i, k in enumerate(ROUTE):
        x, y = pts[i]
        tt = 0.4 + i * 0.6
        pin(c, x, y, t, tt, REDL if k == '合州' else (0.95, 0.95, 0.95), 13)
        if t > tt:
            goldlabel(c, '钓鱼城' if k == '合州' else k, x + 120, y + 16, fin(t, tt + 0.05), 40, REDL if k == '合州' else GREY)
    bignum(c, '≈700', 1500, 420, 140, t, 3.6, REDL, '公里（图上直线折算）', usize=40)
    quote(c, t, 1.4, '軍四萬，號十萬，分三道而進：帝由隴州入散關。', '蒙古军四万人，号称十万，分三路进攻；蒙哥亲自从陇州进散关入川。', S_YS, x=1120, y=990, w=760, osize=38, psize=34)
    caption(c, t, '1258年蒙哥从六盘山南下，', '粮草全靠翻山运', REDL, bsize=96)


# ================================================================ 13 代价对比 vs 守方能耗（数据卡）
@shot(6.0, S_JL)
def s13(c, t):
    databg(c, t)
    panel(c, 120, 300, 800, 600, fin(t, 0.2), edge=REDL)
    panel(c, 1000, 300, 800, 600, fin(t, 0.8), edge=FIELD)
    text(c, '攻方·蒙军', 520, 390, 56, REDL, fin(t, 0.2), align='c', shadow=0)
    text(c, '守方·钓鱼城', 1400, 390, 56, FIELD, fin(t, 0.8), align='c', shadow=0)
    L = [('兵', '4万人（号称10万）'), ('路', '粮道约700公里（直线）'), ('马', '悬崖下骑兵难施展')]
    R = [('水', '天池+13池+92井'), ('粮', '山顶种田，春耕秋守'), ('守', '站在崖上以逸待劳')]
    for i, ((a1, b1), (a2, b2)) in enumerate(zip(L, R)):
        for (ch, s_, x, col, t0) in ((a1, b1, 180, REDL, 0.4 + i * 0.3), (a2, b2, 1060, FIELD, 1.2 + i * 0.3)):
            p = fin(t, t0)
            rec(t0, 'pop')
            y = 520 + i * 120
            c.arc(x + 40, y - 18, 40, 0, TAU); rgba(c, col, p); c.fill()
            text(c, ch, x + 40, y + 2, 46, INK, p, align='c', shadow=0)
            text(c, s_, x + 110, y + 2, 44, WHITE, p, shadow=0)
    sticker(c, '越打越贵', 520, 960, t, 2.6, 64, REDL, -0.06)
    sticker(c, '自给自足', 1400, 960, t, 3.0, 64, YEL, 0.06)
    caption(c, t, '一边千里运粮，一边就地种粮：', '拼的是谁耗得起', GOLDL, bsize=104)


# ================================================================ 14 1259 时间线
@shot(6.0, S_YS)
def s14(c, t):
    databg(c, t)
    items = [(0.0, '二月', '攻一字城', GOLDL), (0.2, '三月', '攻东新门', GOLDL), (0.4, '四月', '雷雨二十天', WATER),
             (0.6, '五月', '屡攻不克', REDL), (0.8, '六月', '夜登外城', REDL), (1.0, '七月', '帝崩', REDL)]
    timeline(c, t, 0.2, 260, 1660, 560, items)
    mengge(c, 620, 1050, 0.6, t, expr='angry', pose='point')
    chibi(c, 1320, 1050, 0.6, **WJ, expr='angry', pose='hold', T=t, name='王坚', label_pre='合州守将')
    caption(c, t, '1259年二月起，', '蒙军猛攻了五个多月')


# ================================================================ 15 大雷雨凡二十日
@shot(5.0, S_YS)
def s15(c, t):
    vgrad(c, 0, H, (0.10, 0.12, 0.18), (0.22, 0.26, 0.34))
    fortress(c, 1300, 900, 0.9, 0.85, t)
    river_band(c, t, 880, 200)
    shore(c, 990)
    rain(c, t, 0.55)
    for i in range(3):
        mongol(c, 300 + i * 180, 1060, 0.65, t + i, expr='sad', pose='hold')
    if int(t * 3) % 5 == 0:
        c.set_source_rgba(1, 1, 1, 0.22); c.paint()
    quote(c, t, 0.8, '夏四月丙子，大雷雨凡二十日。', '四月，雷雨一连下了二十天。', S_YS, x=1100, y=990, w=760)
    caption(c, t, '四月，老天也添乱：', '雷雨下了二十天', WATER)


# ================================================================ 16 梯折
@shot(5.5, S_YS)
def s16(c, t):
    vgrad(c, 0, H, (0.06, 0.07, 0.14), (0.16, 0.18, 0.30))
    fortress(c, 1200, 980, 1.0, 0.9, t, flags=False)
    rain(c, t, 0.35, 70)
    lx, ly = 760, 760
    ang = -0.35 if t < 2.2 else lerp(-0.35, 0.9, ease(seg(t, 2.2, 2.8)))
    c.save(); c.translate(lx, ly + 200); c.rotate(ang); t_ladder(c, 0, -230, 1.8); c.restore()
    if t > 2.2:
        rec(2.2, 'seal')
        sticker(c, '咔嚓！', 900, 470, t, 2.2, 96, YEL, -0.1)
    mongol(c, 520, 1060, 0.7, t, expr='shock' if t > 2.3 else 'angry', pose='raise', name='汪德臣', pre='蒙军都元帅')
    quote(c, t, 0.6, '遲明，遇雨，梯折，後軍不克進而止。', '天快亮时又下雨，梯子断了，后面的兵上不来，只好作罢。', S_YS, x=1060, y=990, w=820, osize=40, psize=36)
    caption(c, t, '六月夜里摸上外城，结果', '梯子断了', REDL)


# ================================================================ 17 帝崩
@shot(5.0, S_YS)
def s17(c, t):
    vgrad(c, 0, H, (0.10, 0.07, 0.07), (0.24, 0.14, 0.12))
    dust(c, t, 3, 40, (1, 0.8, 0.6), 0.3)
    bignum(c, '52', 1450, 560, 220, t, 0.6, REDL, '岁', usize=70)
    stamp(c, '崩于钓鱼山', 1450, 840, t, 1.6, 80, RED, -0.12)
    quote(c, t, 0.8, '癸亥，帝崩于釣魚山，壽五十有二。', '七月癸亥这天，蒙哥死在钓鱼山，享年五十二岁。', S_YS, x=60, y=990, w=900)
    caption(c, t, '1259年七月，', '大汗死在钓鱼山下', REDL)


# ================================================================ 18 死因两说
@shot(6.0, '《元史》卷三 / 据《钓鱼城记》')
def s18(c, t):
    vgrad(c, 0, H, (0.20, 0.13, 0.12), (0.36, 0.22, 0.18))
    mengge(c, 960, 1000, 0.9, t, expr='sad', pose='hold', sw=True, shake=0.1)
    panel(c, 100, 330, 660, 380, fin(t, 0.4))
    text(c, '正史《元史》', 430, 420, 46, GOLDL, fin(t, 0.4), align='c', shadow=0)
    text(c, '六月"帝不豫"', 430, 520, 54, WHITE, fin(t, 0.6), align='c', shadow=0)
    text(c, '白话：大汗病了', 430, 620, 40, GREY, fin(t, 0.8), align='c', shadow=0)
    panel(c, 1160, 330, 660, 380, fin(t, 1.4), edge=REDL)
    text(c, '方志《钓鱼城记》', 1490, 420, 46, REDL, fin(t, 1.4), align='c', shadow=0)
    text(c, '"为炮风所震，因成疾"', 1490, 520, 50, WHITE, fin(t, 1.6), align='c', shadow=0)
    text(c, '白话：被炮震伤后病倒', 1490, 620, 40, GREY, fin(t, 1.8), align='c', shadow=0)
    sticker(c, '两说并存', 1720, 290, t, 2.4, 70, YEL, 0.06)
    caption(c, t, '他怎么死的？史书说法不一：', '病死，还是炮伤？', GOLDL)


# ================================================================ 19 鱼饼故事①：桅杆偷看
@shot(5.5, S_JL)
def s19(c, t):
    mesa_bg(c, t)
    fortress(c, 1450, 900, 0.85, 1.0, t)
    river_band(c, t, 880, 200)
    mast_tower(c, 620, 1000, 0.8, 1.0, t, climb=seg(t, 0.5, 3.0))
    label(c, '桥楼+桅杆', 300, 640, t, 0.6, GOLDL, 46)
    sticker(c, '城里还有水吗？', 960, 430, t, 2.0, 62, YEL, 0.08)
    quote(c, t, 1.0, '築臺建橋樓，樓上接桅，欲觀城內之水有無。', '搭起高台楼，楼上再接一根桅杆，想爬上去看城里还有没有水。', S_JL, x=1040, y=990, w=840, osize=40, psize=36)
    caption(c, t, '据《钓鱼城记》：蒙军搭高桅杆，', '想偷看城里有没有水')


# ================================================================ 20 鱼饼故事②：一炮+送鱼饼
@shot(6.0, S_JL)
def s20(c, t):
    mesa_bg(c, t, ((0.20, 0.14, 0.12), (0.50, 0.34, 0.24)))
    fortress(c, 1450, 900, 0.85, 1.0, t, flags=False)
    river_band(c, t, 880, 200)
    shore(c, 990)
    trebuchet(c, 1200, 900 - 0.85 * 420 - 20, 0.7, 1.0, fire=seg(t, 0.3, 0.7))
    rec(0.3, 'boom')
    mast_tower(c, 520, 1000, 0.7, 1.0, t, climb=1.0, fling=seg(t, 0.8, 1.8))
    chibi(c, 1650, 900 - 0.85 * 420 - 20, 0.6, **SONGB, expr='happy', pose='raise', T=t, name='守军', label_pre='钓鱼城')
    for i in range(2):
        u = seg(t, 1.8 + i * 0.25, 2.8 + i * 0.25)
        if u > 0:
            bigfish(c, lerp(1600, 680 + i * 200, eout(u)), lerp(420, 960 + i * 30, eout(u)) - math.sin(u * math.pi) * 200, 0.55, 1.0, rot=-0.2 + i * 0.3, T=t)
    bread(c, 780, 1050, 8, 0.8, fin(t, 2.8))
    bignum(c, '30', 380, 470, 110, t, 2.2, GOLDL, '斤鲜鱼×2', usize=38)
    quote(c, t, 2.6, '爾北兵可烹鮮食餅，再守十年亦不可得也。', '你们北兵拿去煮鱼吃饼吧，我们再守十年，你们也打不下来！', S_JL, x=1000, y=990, w=880, osize=38, psize=34)
    caption(c, t, '守军一炮打飞了人，又扔下鲜鱼和面饼：', '城里不缺吃喝！', GOLDL, bsize=104)


# ================================================================ 21 1279 开城：前后36年
@shot(6.0, S_ZZ)
def s21(c, t):
    endbg(c, t)
    p = eout(seg(t, 0.3, 2.4))
    rr(c, 260, 520, 1400, 56, 28); rgba(c, (0.25, 0.25, 0.30)); c.fill()
    rr(c, 260, 520, 1400 * p, 56, 28); rgba(c, GOLD); c.fill()
    text(c, '1243 筑城', 260, 660, 46, WHITE, fin(t, 0.3))
    text(c, '1279 开城', 1660, 660, 46, WHITE, fin(t, 2.4), align='r')
    x59 = 260 + 1400 * (16 / 36)
    if t > 1.2:
        c.move_to(x59, 500); c.line_to(x59, 596); rgba(c, REDL); c.set_line_width(6); c.stroke()
        text(c, '1259 蒙哥死', x59, 476, 42, REDL, fin(t, 1.2), align='c')
    bignum(c, '36', 600, 900, 170, t, 2.4, GOLDL, '年', usize=60)
    chibi(c, 1560, 1055, 0.62, hatk='helmet', robe=(0.36, 0.30, 0.46), collar='round', expr='sad', pose='hold', T=t, name='王立', label_pre='守将')
    tagbox(c, '南宋已亡·以不屠城为条件开城', 1130, 900, fin(t, 3.0), GOLDL, 42)
    rec(3.0, 'pop')
    caption(c, t, '直到1279年南宋已亡才开城，', '前后整整36年', GOLDL)


# ================================================================ 22 总结+互动
@shot(6.0)
def s22(c, t):
    endbg(c, t)
    items = [('江', '三面环江', WATER), ('崖', '千仞峭壁', GOLDL), ('粮', '有水有田', FIELD)]
    for i, (ch, sub, col) in enumerate(items):
        x = 480 + i * 480
        p = back(seg(t, 0.3 + i * 0.3, 0.6 + i * 0.3))
        if p <= 0.01:
            continue
        rec(0.3 + i * 0.3, 'pop')
        c.save(); c.translate(x, 560); c.scale(p, p)
        c.arc(0, 0, 140, 0, TAU); rgba(c, (0.14, 0.09, 0.08)); c.fill_preserve(); rgba(c, col); c.set_line_width(6); c.stroke()
        text(c, ch, 0, 58, 160, col, 1, align='c', shadow=0)
        c.restore()
        text(c, sub, x, 790, 50, WHITE, p, align='c')
    q = fin(t, 2.6, 0.4)
    if q > 0.01:
        rr(c, 360, 860, 1200, 120, 16); c.set_source_rgba(0.10, 0.07, 0.06, 0.9 * q); c.fill_preserve(); rgba(c, GOLDL, q); c.set_line_width(3); c.stroke()
        text(c, '如果你是蒙哥，这座城你会怎么打？', 960, 940, 54, GOLDL, q, align='c', shadow=0)
        rec(2.6, 'pop')
    text(c, '评论区说说', 960, 1040, 36, GREY, fin(t, 3.2), align='c', shadow=0)
    caption(c, t, '险地 + 自给 = 耗不垮：', '地形用到了极致', GOLDL)


SCENES = SC

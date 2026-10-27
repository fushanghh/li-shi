from nj import *

SCENES = []
NOTE = "地图为示意"


def scene(D, caps=(), src=None, bg='none', spot=(1300, 600, 650), sfx=(), counter=None, cam=None, note=NOTE):
    def deco(fn):
        s_ = (note + "　" if note else "") + (src or "")
        SCENES.append(dict(D=D, caps=list(caps), src=s_.strip("　"), bg=bg, spot=spot,
                           fn=fn, sfx=list(sfx), counter=counter, cam=cam or (960, 540, 1.0, 1.0), cx=90, cy=80))
        return fn
    return deco


def chapter(num, a, b):
    @scene(2.8, [(0.05, num, 'l'), (0.2, a, 'b'), (0.7, b, 's')], bg='dark', spot=(960, 540, 900), sfx=[(0.15, 'boom', .45)],
           cam=(960, 540, 1.0, 1.06), note=None)
    def ch(c, t):
        rgba(c, GOLD, 0.9 * fin(t, 0.3)); c.rectangle(520, 700, 880 * ease(seg(t, 0.3, 1.0)), 4); c.fill()
    SCENES[-1]['cx'], SCENES[-1]['cy'] = 520, 330
    return ch


def mc(t, D, a, b, t0=0.0, t1=None):
    u = ease(seg(t, t0, t1 if t1 is not None else D))
    return tuple(lerp(x, y, u) for x, y in zip(a, b))


CITY = (118.758, 32.056, 2300)      # whole city, framed to the right
CITYW = (118.770, 32.058, 2900)
CITY2 = (118.735, 32.072, 3200)


def base_city(c, t, view, wall=1.0, wall_a=1.0, lakes=True, riv=True, bright=0.25):
    k = nmap(c, *view, bright=bright)
    if riv: rivers(c, k, 1.0)
    if lakes: lake(c, k)
    if wall_a > 0: wallline(c, k, wall, wall_a)
    return k


# 1 ============================================================ hook
@scene(9.0, [(0.0, "北京故宫，[方方正正]。"), (1.8, "南京明城墙，却歪歪扭扭，"), (3.4, "像一只{粽子}。", 'b')],
       bg='dark', spot=(1000, 700, 900), sfx=[(0.3, 'chime', .4), (1.8, 'riserS', .3), (3.4, 'boom', .5)], note=None)
def s1(c, t):
    fc_plan(c, 560, 690, 440, fin(t, 0.2), ease(seg(t, 0.2, 1.6)), t)
    bigtag(c, "北京故宫", 560, 1000, 50, t - 0.8, GOLDT)
    nj_plan(c, 1380, 690, 500, fin(t, 1.8), ease(seg(t, 1.8, 4.0)))
    bigtag(c, "南京明城墙", 1380, 1000, 50, t - 2.6, GOLDT)


# 2 ============================================================ the wall
@scene(9.0, [(0.0, "这圈城墙，周长[35.267公里]，"), (2.0, "开了[13座城门]。"), (3.8, "却找不到一条[笔直的边]。")],
       src="周长据2005年测绘", sfx=[(0.2, 'riser', .3), (2.0, 'ticks', .4), (3.8, 'seal', .6)])
def s2(c, t):
    k = base_city(c, t, mc(t, 9, (118.770, 32.056, 2700), CITY), ease(seg(t, 0.0, 2.6)))
    for i, (nm, lo, la) in enumerate(GATES):
        tt = t - 2.0 - i * 0.12
        mdot(c, lo, la, k, fin(tt, 0, 0.2), 9)
    c.restore()


# 3 ============================================================ dates
@scene(8.0, [(0.0, "公元1366年动工，"), (1.5, "朱元璋这时[还没称帝]。"), (3.2, "到1393年才全部完工，前后[28年]。")],
       bg='dark', spot=(1200, 640, 900), sfx=[(0.2, 'boom', .45), (3.2, 'boom', .45), (5.0, 'seal', .6)], note=None,
       src=None)
def s3(c, t):
    bignum(c, "1366", 700, 720, 230, t, 0.1)
    bignum(c, "1393", 1500, 720, 230, t, 3.2)
    if t > 3.2:
        arrow(c, 930, 640, 1240 * 1.0, 640, GOLDL, fin(t, 3.4), 7, 26)
    if t > 4.6:
        text2(c, "28 年", 1090, 880, 110, t - 4.6, REDT, 1, 'c', 0.05, 0.25, FONT_X)


# 4 ============================================================ Zhu Sheng
@scene(11.0, [(0.0, "谋士朱升给他献过九个字："), (1.6, "“高筑墙，广积粮，缓称王。”", 'q'),
              (4.4, "白话：先把城墙修高，把粮食囤足，", 's'), (6.2, "{别急着当皇帝}。", 's')],
       src="《明史·朱升传》", note=None, sfx=[(1.6, 'brush', .4), (6.2, 'seal', .8)], cam=(1150, 640, 1.15, 1.3))
def s4(c, t):
    bg_q(c, t, 860, 0.8)
    wall(c, 0, W, 860, 150, 1.0, towers=(250, 1700), lit=0.6)
    sperson(c, 1450, 1000, 1.35, 'mingemp', 1.0, -1, 'stand')
    bigtag(c, "朱元璋", 1450, 560, 52, t - 0.4, GOLDT)
    sperson(c, 1050, 1000, 1.25, 'mingoff', 1.0, 1, 'bow' if 1.4 < t < 4.0 else 'hold')
    bigtag(c, "朱升", 1050, 590, 52, t - 0.8, GOLDT)
    for i, ch_ in enumerate("墙粮王"):
        if t > 1.8 + i * 0.6:
            seal(c, ch_, 760 + i * 170, 990, 0.8, fin(t, 1.8 + i * 0.6, 0.25))


# 5 ============================================================ misunderstanding: palace city is square
@scene(10.0, [(0.0, "先说一个误会："), (1.3, "故宫，对应的是南京的[宫城]。"), (3.4, "而南京的宫城，[也是方的]。", 'm')],
       sfx=[(1.3, 'whoosh', .4), (3.4, 'seal', .7)])
def s5(c, t):
    k = base_city(c, t, mc(t, 10, CITY, (118.806, 32.040, 1300), 0, 3.0))
    a1 = fin(t, 1.6)
    poly(c, rect_pts(HUANG), k, (0.9, 0.5, 0.2), 0.10 * a1, GOLDL, a1, 3)
    a2 = fin(t, 2.6)
    poly(c, rect_pts(GONG), k, (0.85, 0.15, 0.1), 0.45 * a2, (1, 0.6, 0.45), a2, 4)
    mlabel(c, "宫城", (GONG[0] + GONG[2]) / 2, (GONG[1] + GONG[3]) / 2, k, fin(t, 3.0), 44, (1, 0.95, 0.85), t=t - 3.0)
    mlabel(c, "皇城", HUANG[0] + 0.0045, HUANG[1] + 0.003, k, fin(t, 2.0), 38, GOLDT, False, t - 2.0)
    c.restore()


# 6 ============================================================ four walls
@scene(10.5, [(0.0, "明初南京，一共有[四重城墙]："), (1.8, "宫城、皇城、京城、外郭。"), (3.8, "方的在里面，"), (5.0, "{歪的}，是外面这两圈。")],
       sfx=[(1.8, 'ticks', .35), (5.0, 'thud', .6)])
def s6(c, t):
    k = nmap(c, *mc(t, 10.5, (118.806, 32.040, 1300), (118.790, 32.058, 2950), 0, 3.6), bright=0.25)
    rivers(c, k); lake(c, k)
    poly(c, rect_pts(HUANG), k, (0.9, 0.5, 0.2), 0.10, GOLDL, 1, 3)
    poly(c, rect_pts(GONG), k, (0.85, 0.15, 0.1), 0.45, (1, 0.6, 0.45), 1, 4)
    wallline(c, k, 1.0, 1.0, 8)
    o = ease(seg(t, 2.6, 5.0))
    gstroke(c, partial(P(OUTER), o), k, 5, (1, 0.85, 0.55), GOLDL, 1, [14, 12])
    if t > 4.6:
        mlabel(c, "京城", 118.770, 32.040, k, fin(t, 4.6), 46, TXT, True, t - 4.6)
        mlabel(c, "外郭（约60公里）", 118.900, 32.040, k, fin(t, 5.4), 40, GOLDT, True, t - 5.4)
    c.restore()


CH1 = chapter("原因一", "旧城拆不得", "城里早就住满了人")


# 8 ============================================================ old city
@scene(10.0, [(0.0, "南京城西南，是[南唐以来的旧城]。"), (1.8, "秦淮河两岸，挤满了人家和店铺。"), (3.8, "全拆了重建？{代价太大}。")],
       sfx=[(0.6, 'shimmer', .35), (1.8, 'coins', .3), (3.8, 'thud', .6)])
def s8(c, t):
    k = nmap(c, *mc(t, 10, (118.762, 32.040, 1700), (118.766, 32.036, 1450)), bright=0.25)
    rivers(c, k, 1.0, ease(seg(t, 1.6, 3.4)))
    a = fin(t, 0.4)
    poly(c, OLD, k, (0.95, 0.65, 0.25), 0.12 * a, (1, 0.75, 0.4), a, 4, [16, 10])
    houses(c, k, ease(seg(t, 1.8, 4.0)), 170)
    mlabel(c, "旧城", 118.7725, 32.0440, k, fin(t, 0.9), 52, GOLDT, True, t - 0.9)
    mlabel(c, "秦淮河", 118.7730, 32.0175, k, fin(t, 2.4), 36, TXT, False, t - 2.4, dy=-10)
    c.restore()


# 9 ============================================================ wrap old city
@scene(9.0, [(0.0, "朱元璋的办法是——"), (1.4, "新城墙把旧城[整个包进去]，"), (3.4, "旧城往哪拐，城墙就[跟着拐]。")],
       sfx=[(1.4, 'riser', .35), (3.4, 'seal', .6)])
def s9(c, t):
    k = nmap(c, *mc(t, 9, (118.766, 32.036, 1450), (118.762, 32.050, 2000)), bright=0.25)
    rivers(c, k)
    poly(c, OLD, k, (0.95, 0.65, 0.25), 0.12, (1, 0.75, 0.4), 1, 4, [16, 10])
    houses(c, k, 1.0, 170)
    # southern & western stretch of wall hugging old city: indices from 聚宝门 backwards (west side)
    seg_pts = P(list(reversed(WALL[25:])) + [WALL[0], WALL[1], WALL[2], WALL[3]])
    pr = ease(seg(t, 1.4, 4.6))
    # draw from 聚宝门 both directions
    west = P(list(reversed(WALL[25:])))
    east = P(WALL[0:4])
    gstroke(c, partial(east, pr), k, 9, (1, 0.96, 0.86), GOLDL, 1)
    gstroke(c, partial(west, pr), k, 9, (1, 0.96, 0.86), GOLDL, 1)
    mlabel(c, "旧城", 118.7725, 32.0440, k, 1, 52, GOLDT, True)
    c.restore()


CH2 = chapter("原因二", "新皇宫放哪儿", "旧城里塞不下")


# 11 ============================================================ Yanque lake
@scene(11.0, [(0.0, "旧城里，塞不下一座新皇宫。"), (1.8, "宫城只好放到城东、[钟山]脚下，"), (3.8, "{填平燕雀湖}来盖。", 'm')],
       src="“迁三山，填燕雀”为民间说法", sfx=[(1.8, 'whoosh', .4), (3.8, 'rumble', .6), (6.0, 'seal', .6)])
def s11(c, t):
    k = nmap(c, *mc(t, 11, (118.790, 32.045, 2300), (118.818, 32.046, 1500), 0, 3.4), bright=0.25)
    rivers(c, k)
    poly(c, OLD, k, (0.95, 0.65, 0.25), 0.10, (1, 0.75, 0.4), 0.7, 3, [16, 10])
    fill = ease(seg(t, 4.0, 6.4))
    lp = ellipse_pts(*YANQUE)
    path(c, P(lp), True); rgba(c, lerpc((0.06, 0.08, 0.11), (0.55, 0.42, 0.22), fill), 0.95 * fin(t, 1.0)); c.fill()
    gstroke(c, P(lp), k, 3, (1, 0.9, 0.65), GOLDL, fin(t, 1.0) * (1 - 0.6 * fill), None, True)
    if t < 6.0:
        mlabel(c, "燕雀湖", YANQUE[0], YANQUE[1] + 0.001, k, fin(t, 1.2) * (1 - fin(t, 5.4)), 40, (0.75, 0.88, 1), False, t - 1.2)
    a2 = fin(t, 6.0)
    poly(c, rect_pts(GONG), k, (0.85, 0.15, 0.1), 0.5 * a2, (1, 0.6, 0.45), a2, 4)
    mlabel(c, "宫城", (GONG[0] + GONG[2]) / 2, (GONG[1] + GONG[3]) / 2, k, a2, 42, (1, 0.95, 0.85), t=t - 6.0)
    mlabel(c, "钟山", 118.842, 32.060, k, fin(t, 2.0), 46, GOLDT, True, t - 2.0)
    c.restore()


# 12 ============================================================ bulge & axis
@scene(10.0, [(0.0, "皇宫在东，城墙只好[向东鼓出一大块]。"), (2.0, "正门正阳门，也不在南墙正中。"), (3.8, "全城[没有一条居中的中轴线]。")],
       sfx=[(0.4, 'riser', .3), (2.0, 'tick', .5), (3.8, 'seal', .6)])
def s12(c, t):
    k = base_city(c, t, mc(t, 10, (118.790, 32.050, 2400), CITY), 1.0, 0.55)
    poly(c, rect_pts(HUANG), k, (0.9, 0.5, 0.2), 0.10, GOLDL, 1, 3)
    poly(c, rect_pts(GONG), k, (0.85, 0.15, 0.1), 0.45, (1, 0.6, 0.45), 1, 4)
    gstroke(c, partial(P(WALL[3:12]), ease(seg(t, 0.4, 2.0))), k, 11, (1, 0.98, 0.9), GOLDL, 1)
    mdot(c, 118.8115, 32.0232, k, fin(t, 2.0), 12)
    mlabel(c, "正阳门", 118.8115, 32.0232, k, fin(t, 2.2), 38, GOLDT, False, t - 2.2, dy=64)
    ax = ease(seg(t, 2.4, 3.8))
    x0, y0 = ll(118.8143 + 0.004, 32.0232)
    x1, y1 = ll(118.8143 + 0.004, 32.0232 + 0.04 * ax)
    if ax > 0:
        c.set_dash([18 / k, 10 / k]); rgba(c, REDL, 0.95); c.set_line_width(5 / k); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke(); c.set_dash([])
    if t > 3.8:   # geometric middle of city
        xm, _ = ll(118.7865, 32.0)
        _, ya = ll(0, 32.0132); _, yb = ll(0, 32.098)
        c.set_dash([10 / k, 12 / k]); rgba(c, (1, 1, 1), 0.6 * fin(t, 3.8)); c.set_line_width(3 / k)
        c.move_to(xm, ya); c.line_to(xm, yb); c.stroke(); c.set_dash([])
        mlabel(c, "城的中间", 118.7865, 32.0560, k, fin(t, 4.2), 36, TXT, False, t - 4.2)
        mlabel(c, "皇宫中轴", 118.8330, 32.0330, k, fin(t, 4.6), 36, REDT, False, t - 4.6)
    c.restore()


CH3 = chapter("原因三", "让山水当城墙", "能借的险，全借上")


# 14 ============================================================ four directions
@scene(12.0, [(0.0, "后人这样概括南京城墙的位置："), (1.6, "“东傍钟山，西据石头，", 'q'), (3.4, "南凭秦淮，北控后湖。”", 'q'),
              (5.6, "白话：山和水，都被拉来[当城防]。", 's')],
       sfx=[(1.6, 'chime', .3), (2.5, 'chime', .3), (3.4, 'chime', .3), (4.3, 'chime', .3), (5.6, 'seal', .6)])
def s14(c, t):
    k = base_city(c, t, mc(t, 12, CITY, CITY2, 0, 2.0), 1.0, 0.8, True, True)
    mlabel(c, "钟山", *HILLS["钟山"], k, fin(t, 1.6), 50, GOLDT, True, t - 1.6)
    mlabel(c, "石头城", *HILLS["石头城"], k, fin(t, 2.5), 46, GOLDT, True, t - 2.5)
    mlabel(c, "秦淮河", 118.7770, 32.0060, k, fin(t, 3.4), 46, GOLDT, True, t - 3.4)
    mlabel(c, "后湖（玄武湖）", 118.8010, 32.0930, k, fin(t, 4.3), 42, GOLDT, True, t - 4.3)
    hl = fin(t, 3.4)
    gstroke(c, P(QH_OUT), k, 6, (1, 0.95, 0.75), GOLDL, hl)
    if t > 4.3:
        gstroke(c, P(XWLAKE), k, 6, (1, 0.95, 0.75), GOLDL, fin(t, 4.3), None, True)
    mlabel(c, "长江", 118.712, 32.095, k, fin(t, 0.6), 50, (0.85, 0.92, 1), False, t - 0.6)
    c.restore()


# 15 ============================================================ ridge section
@scene(11.0, [(0.0, "城墙尽量[骑在山冈上]："), (1.8, "敌人得先爬山，再攀墙。"), (3.8, "湖和河，就是现成的[护城河]。")],
       note="示意图", sfx=[(0.4, 'thud', .5), (1.8, 'clash', .35), (3.8, 'pour', .4)], cam=(960, 620, 1.0, 1.08))
def s15(c, t):
    bg_day(c, t, 900, 0.5, False)
    rgba(c, (0.30, 0.26, 0.18)); c.rectangle(0, 900, W, H - 900); c.fill()
    # left: plain wall
    wallblock(c, 430, 900, 150, 170, fin(t, 0.2))
    dim(c, 560, 900, 560, 730, "墙高", fin(t, 0.6), t - 0.6, GOLDL, 40)
    # right: ridge wall
    ridge_section(c, 980, 1880, 900, 300, fin(t, 0.4))
    wallblock(c, 1430, 600, 150, 170, fin(t, 0.6))
    dim(c, 1590, 900, 1590, 430, "山＋墙", fin(t, 1.0), t - 1.0, GOLDL, 40)
    # climbing enemies
    if t > 1.8:
        u = ease(seg(t, 1.8, 5.0))
        for j in range(3):
            x = 1080 + j * 60 + 160 * u; y = 900 - 300 * max(0, 1 - ((x - 1430) / 450) ** 2) ** 0.8
            sperson(c, x, y + 4, 0.55, 'soldier', fin(t, 1.8 + j * 0.2), 1, walk=t * 5)
    # moat water at left
    if t > 3.8:
        a = fin(t, 3.8)
        rgba(c, (0.25, 0.50, 0.70), 0.9 * a); c.rectangle(200, 900, 140, 30 * a + 10); c.fill()
        rgba(c, (0.25, 0.50, 0.70), 0.9 * a); c.rectangle(920, 900, 120, 30 * a + 10); c.fill()
        bigtag(c, "护城河", 600, 1010, 44, t - 4.0, GOLDT)
    bigtag(c, "平地", 430, 650, 46, t - 0.4, TXT)
    bigtag(c, "山冈", 1300, 840, 46, t - 0.8, TXT)


# 16 ============================================================ hypothetical square
@scene(11.0, [(0.0, "要是硬画一个[正方形]呢？"), (1.8, "北边，{会把玄武湖切成两半}；"), (3.6, "西北，{狮子山、石头城}被甩在城外，"), (5.4, "成了敌人的[制高点]。")],
       sfx=[(0.3, 'whoosh', .4), (1.8, 'clash', .4), (3.6, 'clash', .4), (5.4, 'thud', .6)])
def s16(c, t):
    k = base_city(c, t, mc(t, 11, CITY, CITY2, 0, 2.0), 1.0, 0.35)
    x0, y0, x1, y1 = SQUARE
    sq = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    gstroke(c, partial(P(sq), ease(seg(t, 0.3, 1.8))), k, 7, (1, 0.55, 0.45), REDL, 1, [22, 12])
    for i, (lo, la, nm) in enumerate(((118.7990, 32.0780, None), (118.7480, 32.1010, "狮子山"), (118.7395, 32.0560, "石头城"))):
        tt = 1.8 + i * 1.8 if i < 2 else 4.4
        if t > tt:
            x, y = ll(lo, la)
            c.save(); c.translate(x, y); c.scale(1 / k, 1 / k); cross(c, 0, 0, 1.0, fin(t, tt)); c.restore()
            if nm: mlabel(c, nm, lo, la, k, fin(t, tt + 0.2), 40, GOLDT, False, t - tt - 0.2, dy=80)
    c.restore()


CH4 = chapter("原因四", "盯住长江", "危险从江上来")


# 18 ============================================================ Lion hill
@scene(11.0, [(0.0, "城北这一段，一路往西北伸，"), (1.8, "把江边的[狮子山]圈进城里。"), (3.8, "站上山头，江面来船[一览无余]。")],
       sfx=[(0.3, 'riser', .35), (1.8, 'seal', .6), (3.8, 'shimmer', .4)])
def s18(c, t):
    k = nmap(c, *mc(t, 11, CITY, (118.752, 32.108, 1700), 0, 3.0), bright=0.25)
    rivers(c, k); lake(c, k)
    wallline(c, k, 1.0, 0.5)
    wallline(c, k, ease(seg(t, 0.3, 2.6)), 1.0, 12, NORTH_IDX)
    mlabel(c, "狮子山", *HILLS["狮子山"], k, fin(t, 1.9), 46, GOLDT, True, t - 1.9)
    mlabel(c, "长江", 118.727, 32.110, k, fin(t, 1.0), 50, (0.85, 0.92, 1), False, t - 1.0)
    if t > 3.8:   # sight lines to river
        a = fin(t, 3.8)
        x0, y0 = ll(*HILLS["狮子山"])
        for ang in (-0.9, -0.55, -0.2):
            L_ = 260 * ease(seg(t, 3.8, 5.0))
            c.set_dash([10 / k, 8 / k]); rgba(c, GOLDL, 0.85 * a); c.set_line_width(3 / k)
            c.move_to(x0, y0); c.line_to(x0 - L_ * math.cos(ang), y0 + L_ * math.sin(ang) * 0.9); c.stroke(); c.set_dash([])
    c.restore()


# 19 ============================================================ Longwan 1360
@scene(11.0, [(0.0, "1360年，朱元璋就在这一带，"), (1.6, "设伏大败[陈友谅]的水军。"), (3.6, "他太清楚：南京的威胁，{从江上来}。")],
       src="龙湾之战，见《明史·太祖本纪》", sfx=[(0.3, 'boom', .45), (1.6, 'clash', .5), (3.6, 'thud', .6)])
def s19(c, t):
    k = nmap(c, 118.752, 32.108, 1700, bright=0.25)
    rivers(c, k); lake(c, k)
    wallline(c, k, 1.0, 0.5)
    wallline(c, k, 1.0, 1.0, 12, NORTH_IDX)
    # enemy fleet arrows coming downriver
    u = ease(seg(t, 0.4, 3.0))
    for j in range(4):
        lo = 118.690 + 0.05 * u + j * 0.006; la = 32.060 + 0.045 * u + j * 0.004
        x, y = ll(lo, la)
        rgba(c, REDL, 0.95 * fin(t, 0.4 + j * 0.1))
        c.save(); c.translate(x, y); c.rotate(-0.85); c.scale(1 / k, 1 / k)
        c.move_to(26, 0); c.line_to(-18, -12); c.line_to(-10, 0); c.line_to(-18, 12); c.close_path(); c.fill(); c.restore()
    if t > 1.6:
        x, y = ll(118.735, 32.103)
        c.save(); c.translate(x, y); c.scale(1 / k, 1 / k)
        swords(c, 0, 0, 1.3, fin(t, 1.6)); c.restore()
        mlabel(c, "龙湾", 118.735, 32.103, k, fin(t, 1.8), 42, REDT, False, t - 1.8, dy=-80)
    mlabel(c, "狮子山", *HILLS["狮子山"], k, 1, 40, GOLDT, False, dy=60)
    c.restore()


# 20 ============================================================ zhuicheng
@scene(10.0, [(0.0, "学界普遍认为，城北在修建中[改过线、扩过建]。"), (2.2, "玄武湖边一段废弃的“赘城”，"), (4.0, "就是被[改掉的旧线]留下的痕迹。")],
       src="见《南京城墙》研究（杨国庆等）", sfx=[(0.3, 'brush', .4), (2.2, 'tick', .5), (4.0, 'seal', .6)])
def s20(c, t):
    k = nmap(c, *mc(t, 10, (118.765, 32.085, 1700), (118.790, 32.070, 1250)), bright=0.25)
    rivers(c, k); lake(c, k)
    wallline(c, k, 1.0, 1.0, 10)
    a = fin(t, 2.2)
    zc = [(118.7965, 32.0650), (118.7925, 32.0652), (118.7905, 32.0655)]
    gstroke(c, P(zc), k, 9, (1, 0.6, 0.45), REDL, a * (0.7 + 0.3 * math.sin(t * 5)))
    mlabel(c, "赘城", 118.7930, 32.0652, k, fin(t, 2.5), 40, REDT, False, t - 2.5, dy=70)
    mlabel(c, "玄武湖", 118.8005, 32.0780, k, fin(t, 0.6), 40, (0.85, 0.92, 1), False, t - 0.6)
    c.restore()


CH5 = chapter("那北京呢", "为什么是方的", "换个地方，答案就变了")


# 22 ============================================================ China map
@scene(12.0, [(0.0, "北京坐落在[华北平原]，一马平川，"), (2.0, "又有元大都方正的街道打底，"), (4.0, "修成方形，[最省事]。"),
              (6.4, "南京却被{山、湖、长江}团团围住。")],
       src="地形据公开高程数据", sfx=[(0.3, 'riser', .35), (2.0, 'ticks', .35), (4.0, 'seal', .6), (6.4, 'thud', .55)])
def s22(c, t):
    view = mc(t, 12, (115.2, 39.3, 1500), (117.6, 32.6, 1500), 4.4, 7.0)
    k = cmap(c, *view)

    def lab(s_, lo, la, a, size, col, bar, tt, dy=0):
        x, y = cll(lo, la)
        c.save(); c.translate(x, y + dy / k); c.scale(1 / k, 1 / k)
        fnt(c, size, FONT_X); w_ = c.text_extents(s_)[4]
        if bar and a > 0:
            rgba(c, GOLDL, 0.9 * a)
            for yy in (-size * 1.05, size * 0.32): c.rectangle(-w_ / 2 - 26, yy, w_ + 52, 3); c.fill()
        text2(c, s_, 0, 0, size, tt, col, a, 'c', 0.03, 0.22, FONT_X)
        c.restore()

    for nm, lo, la, t0 in (("北京", 116.40, 39.90, 0.2), ("南京", 118.79, 32.06, 6.0)):
        a = fin(t, t0)
        x, y = cll(lo, la)
        rgba(c, GOLDL, 0.3 * a); c.arc(x, y, 30 / k, 0, 6.283); c.fill()
        rgba(c, (1, 0.97, 0.9), a); c.arc(x, y, 12 / k, 0, 6.283); c.fill()
        lab(nm, lo, la, a, 56, TXT, True, t - t0, dy=-60)
    lab("华北平原", 116.6, 37.8, fin(t, 0.8), 54, GOLDT, False, t - 0.8)
    lab("长江", 117.2, 31.3, fin(t, 6.4), 48, (0.85, 0.92, 1), False, t - 6.4)
    lab("黄河", 114.0, 35.2, fin(t, 3.0), 44, (0.85, 0.92, 1), False, t - 3.0)
    c.restore()


# 23 ============================================================ Beijing copied Nanjing
@scene(11.0, [(0.0, "后来朱棣修北京宫殿，照的正是南京："), (1.8, "“规制悉如南京，而高敞壮丽过之。”", 'q'),
              (4.6, "白话：格局全照南京，只是[更高、更大]。", 's')],
       src="《明太宗实录》卷232", note=None, sfx=[(1.8, 'brush', .4), (4.6, 'seal', .7)], cam=(960, 640, 1.05, 1.15))
def s23(c, t):
    bg_q(c, t, 900, 0.9)
    mhall(c, 520, 920, 0.62, fin(t, 0.3), 0.2, 5, True, None)
    bigtag(c, "南京宫殿", 520, 1010, 48, t - 0.5, GOLDT)
    mhall(c, 1400, 920, 0.86, fin(t, 1.8), 0.4, 5, True, None)
    bigtag(c, "北京宫殿", 1400, 1010, 48, t - 2.0, GOLDT)
    if t > 1.8: arrow(c, 860, 760, 1000, 760, GOLDL, fin(t, 2.0), 7, 26)


# 24 ============================================================ summary
@scene(11.0, [(0.0, "所以，南京城墙歪，"), (1.2, "不是修歪了，"), (2.4, "而是[一处一处算出来的]。", 'm')],
       bg='dark', spot=(960, 700, 900), note=None, sfx=[(3.6, 'seal', .5), (4.3, 'seal', .5), (5.0, 'seal', .5), (5.7, 'seal', .5)])
def s24(c, t):
    for i, (ch_, lab) in enumerate((("旧", "包住旧城"), ("宫", "皇宫偏东"), ("山", "依山傍水"), ("江", "控扼长江"))):
        tt = t - 3.6 - i * 0.7
        if tt > 0: badge(c, 420 + i * 360, 700, ch_, lab, fin(tt, 0, 0.2), tt)


# 25 ============================================================ ending
@scene(10.0, [(0.0, "这圈墙修了[28年]，"), (1.6, "六百多年后，还剩约[25公里]，"), (3.6, "仍是世界上现存[最长]的古代城墙。")],
       src="数据：南京市文化和旅游局、维基百科", sfx=[(0.3, 'riser', .35), (1.6, 'chime', .4), (3.6, 'boom', .5)])
def s25(c, t):
    k = base_city(c, t, mc(t, 10, CITYW, CITY), 1.0, 1.0)
    for i, (nm, lo, la) in enumerate(GATES):
        mdot(c, lo, la, k, 1, 8)
    c.restore()

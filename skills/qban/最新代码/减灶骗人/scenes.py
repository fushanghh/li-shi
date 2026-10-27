import math, random
from head import *
from head import SC
from dy import mapview, MAPJ, maplabel, pin, dashroute, campath
from ml import *
from fx import horse_rider

SUN = dict(hatk='hanguan', robe=(0.24, 0.34, 0.56), collar='v')          # 孙膑（齐）
PANG = dict(hatk='hanguan', robe='han_red', collar='v')                   # 庞涓（魏）
WEI = dict(hatk='helmet', robe=(0.66, 0.22, 0.18), collar='round')        # 魏兵
QI = dict(hatk='helmet', robe=(0.24, 0.34, 0.56), collar='round')         # 齐兵
BLUE = (0.65, 0.88, 1.0)

S_SJ = '《史记》卷六十五·孙子吴起列传'
S_SJX = '《史记》卷六十五 · 画面为示意'
S_IL = '画面为示意'
WP = MAPJ['wide']['pts']
QY = 1000   # quote bottom (keeps clear of footer)


def wp(k):
    return WP[k]


def sun_in_cart(c, x, yb, s, t, expr='calm', pose='hold', roll=0.0, name='孙膑', pre='齐国军师'):
    chibi(c, x, yb - 95 * s, s * 0.85, **SUN, expr=expr, pose=pose, T=t, name=name, label_pre=pre)
    cart(c, x, yb, s, 1.0, t, roll, cover=False)


def camp(c, t):
    vgrad(c, 0, H, (0.20, 0.16, 0.24), (0.56, 0.36, 0.26))
    c.rectangle(0, 860, W, 220); rgba(c, (0.34, 0.26, 0.18)); c.fill()
    dust(c, t, 6, 30, (1, 0.85, 0.6), 0.25)


def warm(c, t):
    vgrad(c, 0, H, (0.36, 0.24, 0.16), (0.58, 0.42, 0.28))
    c.rectangle(0, 900, W, 180); rgba(c, (0.30, 0.21, 0.14)); c.fill()
    dust(c, t, 5, 30, (1, 0.9, 0.7), 0.3)


def zao_rows(c, t, x0, y0, n, cols=4, dx=150, dy=80, s=0.7, shown=None, fire=True):
    """n stoves in a grid; `shown` = how many still visible (fades extras)"""
    for j in range(n):
        a = 1.0 if shown is None else clamp(shown - j)
        if a > 0.01:
            zao(c, x0 + (j % cols) * dx + (j // cols % 2) * dx * 0.4, y0 + (j // cols) * dy, s, a, t + j, fire=fire)


def bubble(c, x, y, w, h, a=1.0, tail=(0, 0)):
    if a <= 0.01:
        return
    rr(c, x - w / 2, y - h / 2, w, h, h * 0.4)
    c.set_source_rgba(0.98, 0.96, 0.90, a); c.fill()
    for k, r in enumerate((16, 10)):
        c.arc(lerp(x, tail[0], 0.45 + k * 0.3), lerp(y + h / 2, tail[1], 0.45 + k * 0.3), r, 0, TAU); c.fill()


def chart(c, t, x0, y0, w, h, vals, labs, t0=0.4, a=1.0, col=REDL):
    """declining line chart; vals in 万"""
    p = fin(t, t0 - 0.2)
    rgba(c, (0.85, 0.85, 0.9), 0.6 * p * a); c.set_line_width(3)
    c.move_to(x0, y0); c.line_to(x0, y0 + h); c.line_to(x0 + w, y0 + h); c.stroke()
    vmax = 11.0
    pts = [(x0 + 80 + i * (w - 160) / (len(vals) - 1), y0 + h - v / vmax * h) for i, v in enumerate(vals)]
    prog = seg(t, t0, t0 + 1.6)
    dashroute(c, pts, prog, col, 6, a, 0)
    for i, ((x, y), v, lb) in enumerate(zip(pts, vals, labs)):
        ti = t0 + i * 0.8
        q = pop(t, ti)
        if q <= 0.01:
            continue
        rec(ti, 'ding')
        c.arc(x, y, 12 * q, 0, TAU); rgba(c, col, a); c.fill()
        otext(c, '%g万' % v, x, y - 30, 58 * q, GOLDL if i == 0 else REDL, a, align='c')
        text(c, lb, x, y0 + h + 52, 38, WHITE, a * q, align='c', shadow=0)


def card(c, x, y, w, h, title, a=1.0, col=GOLD):
    panel(c, x, y, w, h, a, edge=col)
    rr(c, x, y, w, 70, 14); c.set_source_rgba(col[0], col[1], col[2], 0.22 * a); c.fill()
    text(c, title, x + w / 2, y + 50, 40, col, a, align='c', shadow=0)


def mapbase(c, t, cx=980, cy=640, vw=1500, dark=0.0):
    return mapview(c, 'wide', cx, cy, vw, 1.0, dark)


# ================================================================ 1 钩子：庞涓数灶（第0帧标题）
@shot(5.0, S_SJX)
def s01(c, t):
    camp(c, t)
    stage = 0 if t < 1.3 else (1 if t < 2.4 else 2)
    shown = [12, 6, 3][stage] + (1 - fin(t, [0, 1.3, 2.4][stage], 0.4)) * ([0, 6, 3][stage])
    zao_rows(c, t, 1000, 900, 12, 4, 200, 60, 0.7, shown)
    for k, (s_, t0) in enumerate((('10万', 0.0), ('5万', 1.3), ('3万', 2.4))):
        if k == stage:
            panel(c, 1180, 560, 460, 190, 1.0)
            text(c, '第%d天 · 灶' % (k + 1), 1410, 610, 34, GREY, 1, align='c', shadow=0)
            if t0 == 0.0:
                otext(c, s_, 1410, 720, 104, GOLDL, 1, align='c')
            else:
                bignum(c, s_, 1410, 720, 104, t, t0, REDL)
    happy = t > 2.6
    chibi(c, 520, 990, 0.9, **PANG, expr='laugh' if happy else 'calm', pose='cheer' if happy else 'point', T=t, jump=12 * abs(math.sin(t * 6)) if happy else 0,
          name='庞涓', label_pre='魏将')
    sticker(c, '齐军跑了一大半！', 620, 470, t, 2.6, 70, YEL, -0.08)
    caption(c, t, '孙膑每天少挖灶，', '庞涓为什么信了？', GOLDL, instant=True)


# ================================================================ 2 答案：信息不对称
@shot(5.5)
def s02(c, t):
    databg(c, t)
    card(c, 110, 360, 820, 620, '孙膑手里', fin(t, 0.2), BLUE)
    card(c, 990, 360, 820, 620, '庞涓手里', fin(t, 0.2), REDL)
    for i, s_ in enumerate(('齐军真实兵力', '庞涓看不起齐军', '庞涓追多快', '马陵的地形')):
        tagbox(c, s_, 380, 500 + i * 110, pop(t, 0.5 + i * 0.3), BLUE, 44); rec(0.5 + i * 0.3, 'pop')
    tagbox(c, '灶的数量', 1250, 500, pop(t, 1.9), REDL, 44); rec(1.9, 'pop')
    for i in range(3):
        tagbox(c, '？？？', 1250, 610 + i * 110, pop(t, 2.2 + i * 0.15) * 0.6, GREY, 44)
    chibi(c, 760, 960, 0.6, **SUN, expr='happy', pose='hold', T=t)
    chibi(c, 1640, 960, 0.6, **PANG, expr='calm' if t < 2.6 else 'shock', pose='hold', T=t)
    sticker(c, '只有一张牌', 1560, 560, t, 2.6, 60, YEL, 0.1)
    caption(c, t, '答案先给：', '信息不对称', GOLDL, bsize=120)


# ================================================================ 3 庞涓只有一个指标
@shot(5.5, S_SJ)
def s03(c, t):
    databg(c, t)
    card(c, 680, 330, 1140, 640, '庞涓的情报：每天的灶数', fin(t, 0.1), REDL)
    chart(c, t, 780, 480, 940, 340, [10, 5, 3], ['第一天', '第二天', '第三天'], 0.5)
    chibi(c, 340, 980, 0.9, **PANG, expr='calm' if t < 2.5 else 'laugh', pose='point', T=t, name='庞涓')
    srcbox(c, '《史记》', '十万灶→五万灶→三万灶', 700, 985, fin(t, 2.6), 30)
    caption(c, t, '他手里只有一个数据：', '灶，一天比一天少', REDL)


# ================================================================ 4 证据原文
@shot(5.5, S_SJ)
def s04(c, t):
    camp(c, t)
    for i, (d, k) in enumerate((('第一天', 12), ('第二天', 6), ('第三天', 3))):
        x0 = 1150 + i * 300
        p = fin(t, 0.3 + i * 0.4)
        if p <= 0.01:
            continue
        rec(0.3 + i * 0.4, 'pop')
        panel(c, x0 - 140, 330, 280, 470, p)
        text(c, d, x0, 390, 40, WHITE, p, align='c', shadow=0)
        for j in range(k):
            zao(c, x0 - 70 + (j % 2) * 140, 470 + (j // 2) * 52, 0.45, p, t + j)
    redcircle(c, 1750, 560, 150, 260, t, 2.0)
    quote(c, t, 0.8, '使齊軍入魏地為十萬灶，明日為五萬灶，又明日為三萬灶。', '孙膑让齐军进魏国第一天挖十万个灶，第二天五万，第三天只挖三万。', S_SJ, x=60, y=QY, w=860, osize=40, psize=36)
    caption(c, t, '证据就在《史记》里：', '十万、五万、三万', GOLDL)


# ================================================================ 5 推理链：灶少＝人少
@shot(5.0, S_IL)
def s05(c, t):
    warm(c, t)
    zao(c, 380, 640, 1.3, fin(t, 0.2), t)
    arrow(c, 560, 600, 760, 600, GOLDL, 1, 8, eout(seg(t, 0.6, 1.0)))
    for i in range(6):
        q = pop(t, 0.9 + i * 0.08)
        if q > 0.01:
            ped_x = 860 + (i % 3) * 110; ped_y = 560 + (i // 3) * 140
            c.arc(ped_x, ped_y - 40, 26 * q, 0, TAU); rgba(c, CREAM); c.fill()
            c.move_to(ped_x - 36 * q, ped_y + 60); c.line_to(ped_x - 24 * q, ped_y - 12); c.line_to(ped_x + 24 * q, ped_y - 12); c.line_to(ped_x + 36 * q, ped_y + 60); c.close_path()
            rgba(c, (0.30, 0.38, 0.58)); c.fill()
    tagbox(c, '一个灶 = 一群吃饭的人', 960, 840, fin(t, 1.4), GOLDL, 44)
    arrow(c, 1250, 600, 1420, 600, REDL, 1, 8, eout(seg(t, 2.0, 2.4)))
    otext(c, '灶少', 1560, 590, 90, REDL, fin(t, 2.4), align='c'); rec(2.4, 'pop')
    otext(c, '＝人少', 1600, 700, 90, REDL, fin(t, 2.7), align='c')
    sticker(c, '听着很科学', 1560, 860, t, 3.0, 64, YEL, -0.08)
    caption(c, t, '他的推理看起来很合理：', '灶少，就是人少', GOLDL)


# ================================================================ 6 先入为主：齐号为怯
@shot(5.5, S_SJ)
def s06(c, t):
    camp(c, t)
    chibi(c, 1400, 980, 1.0, **PANG, expr='calm', pose='hold', T=t, name='庞涓')
    bubble(c, 980, 470, 520, 180, fin(t, 0.5), (1300, 640))
    if t > 0.5:
        text(c, '齐军 = 胆小鬼', 980, 495, 62, INK, fin(t, 0.7), align='c', shadow=0)
    stamp(c, '偏见', 1260, 390, t, 1.2, 64, RED, 0.18)
    quote(c, t, 1.6, '彼三晉之兵素悍勇而輕齊，齊號為怯。', '魏国这些兵向来凶悍，看不起齐军，齐军出了名的胆小。', S_SJ, x=60, y=QY, w=900, osize=40, psize=36)
    caption(c, t, '他心里早有答案：', '齐军胆小，迟早要逃', REDL)


# ================================================================ 7 三天少七成
@shot(5.0, S_IL)
def s07(c, t):
    databg(c, t)
    bignum(c, '10万', 470, 640, 150, t, 0.3, GOLDL, '第一天')
    arrow(c, 720, 600, 1060, 600, REDL, 1, 10, eout(seg(t, 0.7, 1.1)))
    text(c, '三天', 890, 560, 44, WHITE, fin(t, 0.8), align='c', shadow=0)
    bignum(c, '3万', 1300, 640, 150, t, 1.1, REDL, '第三天')
    bignum(c, '−70%', 1180, 900, 120, t, 1.8, REDL)
    sticker(c, '跟我想的一模一样！', 600, 880, t, 2.4, 66, YEL, -0.06)
    caption(c, t, '三天少了七成，', '正好对上他的猜想', REDL)


# ================================================================ 8 我固知齐军怯 = 确认偏误
@shot(5.5, S_SJ)
def s08(c, t):
    camp(c, t)
    zao_rows(c, t, 1260, 840, 3, 3, 200, 0, 0.75, fire=False)
    chibi(c, 1500, 840, 0.95, **PANG, expr='laugh', pose='cheer', T=t, jump=10 * abs(math.sin(t * 5)), name='庞涓')
    tagbox(c, '只看自己想看的', 1500, 250, pop(t, 2.4), REDL, 50); rec(2.4, 'pop')
    quote(c, t, 0.5, '我固知齊軍怯，入吾地三日，士卒亡者過半矣。', '我本来就知道齐军胆小，进我国才三天，士兵就逃了一大半！', S_SJ, x=60, y=QY, w=900, osize=40, psize=36)
    caption(c, t, '一个“固”字露了底：', '我早就知道！', GOLDL)


# ================================================================ 9 孙膑反用预期
@shot(5.5, S_IL)
def s09(c, t):
    camp(c, t)
    sun_in_cart(c, 520, 980, 1.0, t, expr='happy', pose='point')
    zao_rows(c, t, 1150, 920, 6, 3, 210, 70, 0.8, 6 - 3 * ease(seg(t, 1.0, 2.0)))
    tagbox(c, '假信号', 1450, 760, pop(t, 1.6), REDL, 52); rec(1.6, 'pop')
    sticker(c, '你想看什么，\n我就演什么', 1350, 380, t, 2.4, 64, YEL, -0.06)
    caption(c, t, '孙膑反过来利用这份偏见：', '给他想要的“证据”', GOLDL)


# ================================================================ 10 信号成本
@shot(5.5, S_IL)
def s10(c, t):
    databg(c, t)
    card(c, 140, 360, 760, 560, '齐军造假', fin(t, 0.2), BLUE)
    card(c, 1020, 360, 760, 560, '庞涓信错', fin(t, 0.2), REDL)
    zao(c, 520, 560, 0.9, fin(t, 0.4), t, fire=False)
    text(c, '少挖几个坑', 520, 690, 46, WHITE, fin(t, 0.6), align='c', shadow=0)
    bignum(c, '≈0', 520, 840, 110, t, 0.9, BLUE, '成本')
    text(c, '押上全部精锐', 1400, 560, 52, WHITE, fin(t, 1.6), align='c', shadow=0)
    bignum(c, '全军', 1400, 760, 130, t, 2.0, REDL, '代价')
    caption(c, t, '造假几乎不花钱，', '信错却要拿命赔', REDL)


# ================================================================ 11 弃步兵，轻锐倍日并行
@shot(5.5, S_SJ)
def s11(c, t):
    vgrad(c, 0, H, (0.30, 0.18, 0.18), (0.62, 0.40, 0.26))
    c.rectangle(0, 900, W, 180); rgba(c, (0.36, 0.26, 0.18)); c.fill()
    for i in range(4):
        chibi(c, 1180 + i * 160, 900, 0.45, **WEI, expr='sad', pose='hold', T=t + i)
    for i in range(4):
        x = lerp(200 + i * 220, 2500 + i * 220, seg(t, 0.2 + i * 0.1, 4.8 + i * 0.1))
        horse_rider(c, x, 1050 + (i % 2) * 15, 0.6, 1.0, run=t * 3, flagc=(0.80, 0.22, 0.18))
    tagbox(c, '步兵：被扔下', 1420, 650, fin(t, 1.0), GREY, 44)
    tagbox(c, '轻锐：两天路一天赶', 1500, 380, fin(t, 1.4), REDL, 44)
    quote(c, t, 1.8, '乃棄其步軍，與其輕銳倍日并行逐之。', '于是扔下步兵，只带轻装精锐，两天的路一天赶完，拼命追。', S_SJ, x=60, y=QY - 40, w=900, osize=40, psize=36)
    caption(c, t, '庞涓扔下步兵，', '带轻锐昼夜狂追', REDL)


# ================================================================ 12 兵法警告
@shot(5.0, S_SJ)
def s12(c, t):
    databg(c, t)
    bignum(c, '100里', 560, 560, 170, t, 0.3, REDL, '急行争利 → 主将栽跟头', usize=44)
    bignum(c, '50里', 1360, 560, 170, t, 0.9, GOLDL, '急行争利 → 只到一半人', usize=44)
    quote(c, t, 1.5, '百里而趣利者蹶上將，五十里而趣利者軍半至。', '为抢先机急行一百里，主将会栽跟头；急行五十里，只有一半人能赶到。', S_SJ, x=60, y=QY, w=1300, osize=40, psize=36)
    caption(c, t, '孙膑引的兵法早说过：', '追得越急，越要出事', GOLDL)


# ================================================================ 13 算速度：时间轴
@shot(6.0, S_SJ)
def s13(c, t):
    vgrad(c, 0, H, (0.16, 0.14, 0.26), (0.40, 0.26, 0.24))
    x0, x1, y = 200, 1720, 560
    rgba(c, WHITE, 0.8); c.set_line_width(6); c.move_to(x0, y); c.line_to(x1, y); c.stroke()
    marks = [(0.0, '清晨', GOLDL), (0.5, '正午', GOLDL), (1.0, '暮（天黑）', REDL)]
    for k, (u, s_, col) in enumerate(marks):
        x = lerp(x0, x1, u); q = pop(t, 0.2 + k * 0.25)
        c.arc(x, y, 14 * q, 0, TAU); rgba(c, col); c.fill(); rec(0.2 + k * 0.25, 'pop')
        text(c, s_, x, y + 80, 44, col, q, align='c', shadow=0)
    # sun sinking
    su = ease(seg(t, 0.6, 3.6))
    sx = lerp(x0, x1, su); sy = 430 - math.sin(su * math.pi) * 90 + su * 40
    glow(c, sx, sy, 90, (1.0, lerp(0.85, 0.45, su), 0.3), 0.6)
    c.arc(sx, sy, 34, 0, TAU); rgba(c, (1.0, lerp(0.85, 0.50, su), 0.30)); c.fill()
    # Pang's cavalry along the line
    hx = lerp(x0, x1, ease(seg(t, 0.6, 3.6)))
    horse_rider(c, hx, y - 30, 0.32, 1.0, run=t * 3, flagc=(0.80, 0.22, 0.18))
    maplabel(c, '马陵', x1, y - 200, fin(t, 3.4), 46, REDL)
    tagbox(c, '倍日并行：速度可推算', 1420, 780, fin(t, 1.6), BLUE, 44)
    quote(c, t, 2.2, '孫子度其行，暮當至馬陵。', '孙膑估算庞涓的行军速度：天黑时，他正好赶到马陵。', S_SJ, x=60, y=QY, w=900)
    caption(c, t, '他追得越急，越好算：', '天黑正好到马陵', BLUE)


# ================================================================ 14 地图：马陵在哪（有争议）
@shot(6.0, '地形：AWS Terrarium 高程 · 河道为今河道示意')
def s14(c, t):
    cx, cy, vw = campath(t, [(0, 930, 533, 1780), (5.8, 940, 540, 1700)])
    f = mapbase(c, t, cx, cy, vw)
    g = cairo.LinearGradient(0, 0, 0, 340); g.add_color_stop_rgba(0, 0.05, 0.05, 0.07, 0.75); g.add_color_stop_rgba(1, 0.05, 0.05, 0.07, 0)
    c.set_source(g); c.rectangle(0, 0, W, 340); c.fill()
    dl, lz = f(*wp('大梁')), f(*wp('临淄'))
    for k, (x, y) in (('大梁', dl), ('临淄', lz)):
        pin(c, x, y, t, 0.2, GOLDL)
        maplabel(c, {'大梁': '大梁（魏都）', '临淄': '临淄（齐都）'}[k], x, y + 62, fin(t, 0.3), 38, GOLDL)
    for i, (k, dx, dy) in enumerate((('大名说', -150, -55), ('莘县说', 150, -55), ('郯城说', 0, -60))):
        x, y = f(*wp(k))
        pin(c, x, y, t, 0.9 + i * 0.45, REDL)
        maplabel(c, '马陵？' + k, x + dx, y + dy, fin(t, 1.0 + i * 0.45), 36, REDL)
    rr(c, 1170, 40, 710, 170, 10); rgba(c, (0.07, 0.07, 0.09), 0.9); c.fill_preserve(); rgba(c, GOLDD); c.set_line_width(2); c.stroke()
    text(c, '约前342年（一说前341年）', 1200, 92, 38, WHITE, 1, shadow=0)
    text(c, '马陵位置有争议：', 1200, 140, 32, GOLDL, 1, shadow=0)
    text(c, '河北大名 / 山东莘县 / 山东郯城', 1200, 184, 32, GOLDL, 1, shadow=0)
    caption(c, t, '马陵到底在哪？', '至今有好几种说法', GOLDL)


# ================================================================ 15 窄道剖面
@shot(5.5, S_SJ)
def s15(c, t):
    nightvalley(c, t, moon=False)
    slopes(c, 1.0, gap=lerp(900, 520, ease(seg(t, 0.0, 1.2))))
    label(c, '路窄：大军挤成一条线', 960, 560, t, 1.2, GOLDL, 44)
    label(c, '两侧险隘', 380, 420, t, 1.6, REDL, 48)
    label(c, '两侧险隘', 1540, 420, t, 1.6, REDL, 48)
    quote(c, t, 2.2, '馬陵道陜，而旁多阻隘，可伏兵。', '马陵的路很窄，两边全是险要地形，正好埋伏兵马。', S_SJ, x=60, y=QY, w=760)
    caption(c, t, '第三步：选地形', '路窄、两边险、能藏兵', REDL)


# ================================================================ 16 树上写字
@shot(5.5, S_SJ)
def s16(c, t):
    nightvalley(c, t)
    slopes(c)
    pe = seg(t, 0.3, 1.4)
    tree(c, 1150, 900, 0.95, 1.0, peel=max(pe, 0.001), writing=seg(t, 1.6, 2.6))
    chibi(c, 1520, 1000, 0.7, **QI, expr='calm', pose='hold', prop='brush' if t > 1.4 else 'sword', T=t, name='齐兵')
    quote(c, t, 1.8, '斫大樹白而書之曰：龐涓死于此樹之下。', '削掉一棵大树的皮露出白木，在上面写：庞涓死在这棵树下。', S_SJ, x=60, y=QY, w=800, osize=40, psize=36)
    caption(c, t, '路边一棵大树，', '削皮写下一行字', GOLDL)


# ================================================================ 17 万弩夹道
@shot(5.5, S_SJ)
def s17(c, t):
    nightvalley(c, t)
    slopes(c)
    tree(c, 960, 900, 0.8, 1.0)
    rnd = random.Random(4)
    for i in range(16):
        side = -1 if i % 2 == 0 else 1
        k = i // 2
        x = 960 + side * (380 + k * 70 + rnd.uniform(-20, 20)); y = 420 + k * 70
        if fin(t, 0.3 + i * 0.06) > 0.01:
            crossbowman(c, x, y, 0.55, t, fin(t, 0.3 + i * 0.06), 1.0, side=-side)
    bignum(c, '10000', 1480, 230, 100, t, 1.4, GOLDL, '张弩', usize=36)
    quote(c, t, 2.0, '令齊軍善射者萬弩，夾道而伏，期曰：暮見火舉而俱發。', '让一万名善射的弩手埋伏在道路两边，约好：天黑看见火光，一齐放箭。', S_SJ, x=60, y=QY, w=780, osize=40, psize=36)
    caption(c, t, '两边埋伏一万弩手：', '看见火光就放箭', REDL)


# ================================================================ 18 点火
@shot(5.5, S_SJ)
def s18(c, t):
    nightvalley(c, t)
    slopes(c)
    lit = seg(t, 2.0, 2.4)
    tree(c, 1250, 900, 0.9, 1.0, lit=lit)
    x, wk, _ = walk2(t, 600, 1000, 0.0, 1.6)
    chibi(c, x, 1000, 0.85, **PANG, expr='calm' if t < 2.6 else 'shock', pose='hold' if t < 2.0 else 'point', T=t, walk=wk, sw=t > 2.6, name='庞涓')
    if t > 2.0:
        torch(c, x + 100, 740, 1.0, 1.0, t)
        rec(2.0, 'fire')
    redcircle(c, 1250, 540, 90, 230, t, 2.6)
    sticker(c, '火光 = 信号', 1560, 330, t, 2.6, 64, REDL, 0.08)
    quote(c, t, 0.6, '龐涓果夜至斫木下，見白書，乃鑽火燭之。', '庞涓果然夜里赶到树下，看见白木上有字，就点火照着看。', S_SJ, x=60, y=QY, w=780, osize=40, psize=36)
    caption(c, t, '他亲手点亮了', '伏兵等的信号', REDL)


# ================================================================ 19 万弩齐发
@shot(5.0, S_SJ)
def s19(c, t):
    nightvalley(c, t)
    slopes(c)
    tree(c, 1250, 900, 0.9, 1.0, lit=1.0)
    chibi(c, 1000, 1000, 0.85, **PANG, expr='shock', pose='raise', T=t, sw=True, shake=0.4)
    torch(c, 1100, 740, 1.0, 1.0, t)
    rec(0.4, 'boom')
    arrows(c, t, 300, 300, 960, 800, 50, seg(t, 0.3, 0.9), 1.0, 1)
    arrows(c, t, 1620, 300, 960, 800, 50, seg(t, 0.3, 0.9), 1.0, 2)
    quote(c, t, 1.0, '讀其書未畢，齊軍萬弩俱發，魏軍大亂相失。', '字还没读完，齐军一万张弩一齐发射，魏军大乱，彼此失散。', S_SJ, x=60, y=QY, w=780, osize=40, psize=36)
    caption(c, t, '字还没读完——', '万弩齐发', REDL, bsize=130)


# ================================================================ 20 结局
@shot(5.5, S_SJ)
def s20(c, t):
    vgrad(c, 0, H, (0.08, 0.05, 0.06), (0.22, 0.11, 0.10))
    dust(c, t, 3, 40, (1, 0.7, 0.5), 0.3)
    chibi(c, 1450, 1000, 0.95, **PANG, expr='sad', pose='hold', T=t, name='庞涓')
    sticker(c, '遂成竖子之名！', 1450, 380, t, 0.8, 76, REDL, -0.06)
    quote(c, t, 1.2, '龐涓自知智窮兵敗，乃自剄，曰：遂成豎子之名！', '庞涓知道自己计穷兵败，拔剑自刎，临死说：倒让这小子出了名！', S_SJ, x=60, y=QY, w=1000, osize=40, psize=36)
    caption(c, t, '一个数据看走眼，', '庞涓兵败自刎', REDL)


# ================================================================ 21 博弈总结
@shot(6.0)
def s21(c, t):
    vgrad(c, 0, H, (0.32, 0.22, 0.16), (0.20, 0.13, 0.10))
    c.rectangle(0, 900, W, H - 900); rgba(c, (0.16, 0.11, 0.08)); c.fill()
    dust(c, t, 4, 40, (1, 0.85, 0.6), 0.25)
    items = [('信', '摸清他信什么', GOLDL), ('演', '演给他看', REDL), ('算', '算好在哪等他', BLUE)]
    for i, (ch, sub, col) in enumerate(items):
        x = 480 + i * 480
        t0 = 0.3 + i * 0.4
        p = back(seg(t, t0, t0 + 0.3))
        if p <= 0.01:
            continue
        rec(t0, 'pop')
        c.save(); c.translate(x, 600); c.scale(p, p)
        c.arc(0, 0, 150, 0, TAU); rgba(c, (0.14, 0.09, 0.08)); c.fill_preserve(); rgba(c, col); c.set_line_width(6); c.stroke()
        text(c, ch, 0, 60, 170, col, 1, align='c', shadow=0)
        c.restore()
        text(c, sub, x, 860, 50, WHITE, p, align='c')
        if i < 2:
            arrow(c, x + 170, 600, x + 300, 600, GOLDL, p, 8, p)
    caption(c, t, '孙膑赢的不是兵多，', '是比庞涓更懂庞涓', GOLDL)


# ================================================================ 22 现代类比
@shot(6.0, S_IL)
def s22(c, t):
    databg(c, t, (0.14, 0.17, 0.22))
    # phone
    px, py = 420, 340
    rr(c, px, py, 380, 640, 40); rgba(c, (0.10, 0.10, 0.12)); c.fill()
    rr(c, px + 18, py + 40, 344, 560, 18); rgba(c, (0.95, 0.94, 0.90)); c.fill()
    rr(c, px + 50, py + 80, 280, 200, 14); rgba(c, (0.80, 0.70, 0.55)); c.fill()
    text(c, '★★★★★', px + 190, py + 340, 46, (0.95, 0.65, 0.10), 1, align='c', shadow=0)
    text(c, '已售', px + 70, py + 430, 34, (0.4, 0.4, 0.4), 1, shadow=0)
    otext(c, '10万+', px + 150, py + 440, 70, REDL, 1)
    redcircle(c, px + 200, py + 420, 190, 70, t, 0.6)
    sticker(c, '刷出来的？', px + 330, py + 40, t, 1.2, 64, YEL, 0.1)
    # arrow to lesson
    arrow(c, 860, 650, 1020, 650, GOLDL, 1, 8, eout(seg(t, 1.6, 2.0)))
    for i, s_ in enumerate(('这个数字，谁能造假？', '造假要花多少钱？', '还有别的证据吗？')):
        tagbox(c, s_, 1430, 520 + i * 120, pop(t, 2.0 + i * 0.35), GOLDL if i == 0 else WHITE, 46); rec(2.0 + i * 0.35, 'pop')
    caption(c, t, '今天也一样：', '只盯一个数字，最容易被带偏', GOLDL, bsize=100)


# ================================================================ 23 互动
@shot(5.0)
def s23(c, t):
    camp(c, t)
    zao_rows(c, t, 1150, 860, 3, 3, 200, 0, 0.9)
    chibi(c, 640, 960, 0.9, **PANG, expr='calm', pose='hold', T=t, name='如果你是庞涓')
    sticker(c, '？', 820, 560, t, 0.6, 120, YEL, 0.1)
    tagbox(c, '还该查哪个数据？', 1400, 560, pop(t, 1.2), GOLDL, 56); rec(1.2, 'pop')
    text(c, '评论区说说', 1400, 700, 44, GREY, fin(t, 1.8), align='c', shadow=0)
    caption(c, t, '看到灶越来越少，', '你会追吗？', GOLDL)


SCENES = SC

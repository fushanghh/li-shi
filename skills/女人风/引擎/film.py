# 随份子从哪儿来 —— 主渲染
import sys, os, json, math
from scenes import *

KEYS = {'hall': bg_hall, 'zhou': bg_zhou, 'han': bg_han, 'mogao': bg_mogao, 'yard': bg_yard, 'feast': bg_feast, 'ming': bg_ming, 'jia': bg_jia, 'minguo': bg_minguo}

# (场景函数, 行1, 行2, 镜头(z0,z1,cx,cy), 段落, 最少半小节)
SHOTS = [
    (s_hook, '这个月第三场婚礼', '份子钱又随出去[r]八百[/r]', (1.0, 1.06, 900, 560), 'intro', 4),
    (s_book, '可你想过没有', '随份子 到底是从哪儿来的？', (1.0, 1.04, 960, 480), 'intro', 4),
    (s_title, '', '', (1.0, 1.0, 960, 540), 'title', 4),
    (s_zhou1, '最早的“份子”', '出现在[r]丧礼[/r]上', (1.0, 1.05, 900, 600), 'zhou', 4),
    (s_zhou2, '亲友送钱、送布', '帮主家把丧事办下来', (1.12, 1.2, 860, 640), 'zhou', 4),
    (s_zhou3, '这就叫“赙”', '《荀子》说：[r]货财曰赙[/r]', (1.0, 1.03, 960, 480), 'zhou', 4),
    (s_han1, '秦朝末年 [g]沛县[/g]', '吕公摆酒 全县豪杰都来贺', (1.0, 1.05, 960, 560), 'han', 4),
    (s_han2, '萧何管收礼 定了规矩', '不满[r]一千钱[/r] 只能坐堂下', (1.06, 1.12, 900, 600), 'han', 4),
    (s_han3, '刘邦一个钱没带', '却在名帖上写：[r]贺钱万[/r]', (1.06, 1.14, 860, 600), 'han', 5),
    (s_han4, '吕公大惊 亲自出门迎他', '后来还把女儿嫁给了他', (1.0, 1.06, 960, 600), 'han', 4),
    (s_dh0, '一千年后 五代的[g]敦煌[/g]', '份子有了白纸黑字的规矩', (1.0, 1.08, 960, 500), 'dh', 4),
    (s_dh1, '一群女人结了个社', '叫[g]女人社[/g] 有事一起扛', (1.0, 1.05, 900, 560), 'dh', 4),
    (s_dh2, '显德六年正月初三', '她们重新立下[g]社条[/g]', (1.0, 1.04, 960, 480), 'dh', 4),
    (s_dh3, '社里谁家有红白事', '每人出[r]油一合 面一斤 粟一斗[/r]', (1.0, 1.04, 960, 560), 'dh', 5),
    (s_dh4, '社条还管酒品', '席上划拳吵闹、不听劝的……', (1.0, 1.08, 960, 680), 'feast', 4),
    (s_dh5, '罚她请全社', '再吃一桌[r]酒席[/r]！', (1.0, 1.05, 1000, 600), 'feast', 4),
    (s_ming1, '到了[g]明清[/g] 谁家办事', '亲友就一起[r]凑份子[/r]', (1.0, 1.05, 960, 560), 'ming', 4),
    (s_ming2, '“份子”这个词', '就是这时候流行开的', (1.0, 1.03, 960, 480), 'ming', 4),
    (s_hl1, '《红楼梦》里 贾母起头', '给凤姐凑份子过生日', (1.0, 1.05, 960, 540), 'hl', 4),
    (s_hl2, '贾母、薛姨妈各二十两', '邢夫人、王夫人各十六两', (1.0, 1.04, 960, 560), 'hl', 5),
    (s_hl3, '上到老太太 下到丫头', '[r]人人都出一份[/r]', (1.0, 1.05, 960, 600), 'hl', 4),
    (s_mg1, '清末民国 红白喜事', '门口专设[g]礼账[/g] 请先生记', (1.0, 1.05, 960, 580), 'mg', 4),
    (s_mg2, '今天你随我多少', '下回我照着[r]还[/r]回去', (1.0, 1.04, 960, 480), 'mg', 4),
    (s_md1, '到了今天', '份子成了红包 成了扫码', (1.0, 1.06, 1100, 600), 'md', 4),
    (s_md2, '数越随越大', '成了不少人的[r]人情负担[/r]', (1.0, 1.1, 960, 540), 'md', 4),
    (s_md3, '可份子本来的意思', '是[r]一家有事 大家帮一把[/r]', (1.0, 1.05, 900, 560), 'end', 5),
    (s_end, '随出去的不只是钱', '还有[r]人情[/r]', (1.06, 1.0, 900, 560), 'end', 6),
]
WIPE_AT = {3, 6, 10, 14, 16, 18, 21, 23, 25}   # 段落起点：画面内翻纸转场

def plan():
    T = []; t = 0
    for i, s in enumerate(SHOTS):
        n = plain_len(s[1]) + plain_len(s[2]); need = n / 4.5 + 1.5 if n else 3.5
        halves = max(s[5], math.ceil(need / HALF))
        T.append((t, halves * HALF)); t += halves * HALF
    return T, t

T0, TOTAL = plan()

def cam_clamp(z, cx, cy):
    hw = SW / (2 * z); hh = SH / (2 * z)
    return min(max(cx, hw), SW - hw), min(max(cy, hh), SH - hh)

def render(t, out=None):
    i = max(j for j, (a, d) in enumerate(T0) if a <= t + 1e-6); a, d = T0[i]; lt = t - a
    fn, l1, l2, (z0, z1, cx, cy), sec, _ = SHOTS[i]
    s, c = surf(); c.set_source_rgb(*hx('efe2c4')); c.paint()
    marks = fn(c, lt, d) or []; s.flush()
    F = cairo.ImageSurface(cairo.FORMAT_RGB24, FW, FH); g = cairo.Context(F)
    z = lerp(z0, z1, ease(lt / d)); ccx, ccy = cam_clamp(z, cx, cy)
    sh = 0
    for mk in marks:
        if mk[0] == 'shake': sh = max(sh, mk[1])
    dx = math.sin(t * 90) * sh; dy = math.cos(t * 77) * sh
    def S2F(x, y): return ((x - ccx) * z + SW / 2) * SC + dx, ((y - ccy) * z + SH / 2) * SC + SY + dy
    g.save(); g.rectangle(0, SY, FW, 812); g.clip()
    g.translate(dx, SY + dy); g.scale(SC, SC); g.translate(SW / 2, SH / 2); g.scale(z, z); g.translate(-ccx, -ccy)
    g.set_source_surface(s, 0, 0); g.paint(); g.restore()
    # 转场：段落起点 0.35s 纸幕从右向左揭开
    if i in WIPE_AT and lt < 0.4:
        k = ease(lt / 0.4); xe = FW * k
        g.save(); g.rectangle(0, SY, FW, 812); g.clip()
        pts = [(xe + math.sin(y * 0.02) * 30, y) for y in range(SY, SY + 820, 20)]
        g.move_to(FW + 10, SY); [g.line_to(*p) for p in pts]; g.line_to(FW + 10, SY + 820); g.close_path(); g.set_source_rgb(*hx('f3e6c4')); g.fill_preserve()
        g.restore()
        ink(g, pts, 10, hx('c9a24a'), 3, 2)
    # 标记
    for mk in marks:
        if mk[0] == 'tag':
            x, y = S2F(*mk[2]); name_tag(g, mk[1], x, y, mk[3], min(1, lt / 0.3))
        elif mk[0] == 'num':
            _, text, x, y, size, a, col, pop = mk
            if pop > 0: X, Y = S2F(x, y); big_num(g, text, X, Y, size * SC * 1.15, a, col, pop)
    g.set_source_surface(frame_base(), 0, 0); g.paint()
    fa = min(1, lt / 0.25, (d - lt) / 0.2)
    subtitle(g, l1, l2, fa)
    F.flush()
    if out: F.write_to_png(out)
    return F

def to_rgb(F):
    import numpy as np
    a = np.frombuffer(F.get_data(), np.uint8).reshape(FH, F.get_stride() // 4, 4)[:, :FW, :3]
    return a[:, :, ::-1].tobytes()

if __name__ == '__main__':
    import subprocess, argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--part', type=int, default=0); ap.add_argument('--parts', type=int, default=1)
    ap.add_argument('--sheet', action='store_true'); ap.add_argument('--frac', type=float, default=0.7); ap.add_argument('--shots', default='')
    ap.add_argument('--still', type=float, default=-1)
    A = ap.parse_args()
    os.makedirs('out', exist_ok=True)
    json.dump({'T0': T0, 'TOTAL': TOTAL, 'BPM': BPM, 'secs': [s[4] for s in SHOTS], 'names': [s[0].__name__ for s in SHOTS]}, open('out/timing.json', 'w'))
    if A.still >= 0: render(A.still, 'out/still.png'); sys.exit()
    if A.sheet:
        from PIL import Image
        ids = [int(x) for x in A.shots.split(',')] if A.shots else range(len(SHOTS))
        ims = []
        for i in ids:
            a, d = T0[i]; F = render(a + d * A.frac); im = Image.frombytes('RGB', (FW, FH), to_rgb(F)).resize((480, 360)); ims.append(im)
        cols = 4; rows = (len(ims) + cols - 1) // cols; sheet = Image.new('RGB', (480 * cols, 360 * rows), 'white')
        for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 480, (k // cols) * 360))
        sheet.save('out/sheet.jpg', quality=85); sys.exit()
    N = int(round(TOTAL * FPS)); per = math.ceil(N / A.parts); f0 = A.part * per; f1 = min(N, f0 + per)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', f'out/part{A.part}.mp4'], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(to_rgb(render(f / FPS)))
        if f % 100 == 0: print(A.part, f, f1, flush=True)
    p.stdin.close(); p.wait()

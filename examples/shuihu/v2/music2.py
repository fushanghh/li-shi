"""v2 配乐 + 音效：多音色分段编曲（A 小调），随镜头切换段落，带混响与压缩"""
import numpy as np, wave, math
from render import SHOTS, STARTS, EVENTS, TOTAL, B

SR = 44100
N = int((TOTAL + 3) * SR)
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)       # 干声
RV = np.zeros(N)                        # 混响送
KENV = np.zeros(N)                      # 底鼓包络（侧链）
SFXL = np.zeros(N); SFXR = np.zeros(N)

def T(n): return np.arange(n) / SR
def put(sig, t0, g=1.0, pan=0.0, rev=0.0, sfx=False):
    i = int(t0 * SR)
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    j = min(N, i + len(sig)); s = sig[:j - i] * g
    l = math.cos((pan + 1) * math.pi / 4) * 1.41; r = math.sin((pan + 1) * math.pi / 4) * 1.41
    if sfx: SFXL[i:j] += s * l; SFXR[i:j] += s * r
    else: L[i:j] += s * l; R[i:j] += s * r
    if rev: RV[i:j] += s * rev
def fft_filt(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    if hi: X *= 1 / (1 + (f / hi) ** 4)
    if lo: X *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))
def env_adsr(n, a=0.01, d=0.1, s=0.7, r=0.1):
    t = T(n); dur = n / SR
    e = np.where(t < a, t / a, np.where(t < a + d, 1 - (1 - s) * (t - a) / d, s))
    rel = np.clip((dur - t) / r, 0, 1); return e * rel
def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def saw(f, n, det=0.0):
    t = T(n); ph = (f * (1 + det) * t) % 1.0; return 2 * ph - 1

C = {}
def cache(key, fn):
    if key not in C: C[key] = fn()
    return C[key]

# ---------- 打击乐 ----------
def kick(): t = T(int(.35 * SR)); f = 42 + 130 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8) * 1.1 + fft_filt(rng.standard_normal(len(t)), 1000, 6000) * np.exp(-t * 200) * 0.3
def snare(): t = T(int(.25 * SR)); return fft_filt(rng.standard_normal(len(t)), 800, 9000) * np.exp(-t * 16) * 0.8 + np.sin(2 * np.pi * 185 * t) * np.exp(-t * 22) * 0.6
def clap():
    n = int(.25 * SR); s = np.zeros(n)
    for k, d in enumerate((0, .012, .024)): i = int(d * SR); s[i:] += fft_filt(rng.standard_normal(n - i), 900, 5000) * np.exp(-T(n - i) * (60 if k < 2 else 14))
    return s * 0.7
def hat(o=False): t = T(int((.25 if o else .05) * SR)); return fft_filt(rng.standard_normal(len(t)), 7000) * np.exp(-t * (12 if o else 80)) * 0.5
def shaker(): t = T(int(.08 * SR)); return fft_filt(rng.standard_normal(len(t)), 5000) * np.sin(np.pi * t / .08) * 0.35
def taiko(f=62): t = T(int(.9 * SR)); ff = f * (1 + 0.6 * np.exp(-t * 25)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 5) * 1.2 + fft_filt(rng.standard_normal(len(t)), 100, 1500) * np.exp(-t * 18) * 0.5
def tom(f): t = T(int(.4 * SR)); ff = f * (1 + 0.4 * np.exp(-t * 30)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 9)
def wood(f=1100): t = T(int(.12 * SR)); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 45) * 0.6
def crash(): t = T(int(2.2 * SR)); return fft_filt(rng.standard_normal(len(t)), 3000) * np.exp(-t * 2.0) * 0.45
def revcym(d): x = crash()[:int(d * SR)][::-1]; return x * np.linspace(0, 1, len(x)) ** 2
def riser(d):
    n = int(d * SR); t = T(n); x = rng.standard_normal(n)
    out = np.zeros(n); seg = 2048
    for i in range(0, n, seg):
        k = i / n; out[i:i + seg] = fft_filt(x[i:i + seg], 300 + 5000 * k ** 2, 1200 + 9000 * k ** 2)[:len(out[i:i + seg])]
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * 0.25
    return (out * 0.6 + tone) * (t / d) ** 1.5

# ---------- 旋律乐器 ----------
def pluck(m, dur=1.4, bright=0.6):
    f = mf(m); n = int(dur * SR); p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p); buf = np.convolve(buf, [bright, 1 - bright], 'same')
    out = np.empty(n); idx = 0
    b = buf.copy()
    for i in range(n):
        out[i] = b[idx]; nxt = (idx + 1) % p; b[idx] = 0.5 * (b[idx] + b[nxt]) * 0.997; idx = nxt
    t = T(n); return out * np.exp(-t * 1.6) + np.sin(2 * np.pi * f * t) * np.exp(-t * 5) * 0.25
def dizi(m, dur, m_prev=None):
    n = int(dur * SR); t = T(n); f0 = mf(m)
    fp = mf(m_prev) if m_prev else f0
    f = f0 + (fp - f0) * np.exp(-t * 30)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.15) / 0.2, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    br = fft_filt(rng.standard_normal(n), 1500, 6000) * 0.12
    return (s + br) * env_adsr(n, 0.04, 0.1, 0.8, 0.12) * 0.5
def erhu(m, dur):
    n = int(dur * SR); t = T(n); f = mf(m)
    vib = 1 + 0.01 * np.sin(2 * np.pi * 6 * t) * np.clip(t / 0.3, 0, 1)
    ph = np.cumsum(f * vib) / SR; s = 2 * (ph % 1) - 1
    s = fft_filt(s, 300, 3000)
    return s * env_adsr(n, 0.12, 0.1, 0.85, 0.2) * 0.5
def pad(ms, dur, bright=900):
    n = int(dur * SR); s = np.zeros(n)
    for m in ms:
        for d in (-0.004, 0.0, 0.005): s += saw(mf(m), n, d)
    s = fft_filt(s, 60, bright) / (len(ms) * 3)
    return s * env_adsr(n, 0.3, 0.2, 0.9, 0.4)
def choir(ms, dur):
    n = int(dur * SR); t = T(n); s = np.zeros(n)
    for m in ms:
        for d in (-0.003, 0.003): s += saw(mf(m), n, d) * (1 + 0.3 * np.sin(2 * np.pi * 4.5 * t))
    a = fft_filt(s, 500, 900) + fft_filt(s, 1000, 1400) * 0.5
    return a / len(ms) * env_adsr(n, 0.25, 0.2, 0.9, 0.4) * 0.8
def strings_stac(m, dur=0.18):
    n = int(dur * SR); s = saw(mf(m), n) + saw(mf(m), n, 0.006)
    return fft_filt(s, 150, 3500) * env_adsr(n, 0.005, 0.06, 0.4, 0.05) * 0.35
def tremolo(ms, dur):
    n = int(dur * SR); t = T(n); s = pad(ms, dur, 2500)
    return s * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 13 * t)))
def brass(ms, dur=0.45):
    n = int(dur * SR); t = T(n); s = np.zeros(n)
    for m in ms:
        for d in (-0.006, 0, 0.007): s += saw(mf(m), n, d)
    bright = fft_filt(s, 100, 3500) * np.exp(-t * 7); dark = fft_filt(s, 80, 900)
    return (bright + dark * 0.6) / (len(ms) * 3) * env_adsr(n, 0.01, 0.1, 0.6, 0.1) * 1.4
def bass(m, dur, kind='pluck'):
    n = int(dur * SR); t = T(n); f = mf(m)
    sub = np.sin(2 * np.pi * f * t)
    s = sub + fft_filt(saw(f, n), 40, 700) * 0.6
    e = np.exp(-t * (6 if kind == 'pluck' else 1.2)) if kind != 'hold' else env_adsr(n, 0.02, 0.1, 0.9, 0.1)
    return s * e * 0.6
def bell(m, dur=2.0):
    n = int(dur * SR); t = T(n); f = mf(m)
    return sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dcy) for r, a, dcy in [(1, 1, 2.5), (2.76, .5, 4), (5.4, .25, 6), (8.9, .1, 9)]) * 0.3
def gliss(start_m, n_notes=10, up=True, dt=0.035):
    sc = [0, 2, 4, 7, 9]; out = np.zeros(int((n_notes * dt + 1.5) * SR))
    for i in range(n_notes):
        m = start_m + sc[i % 5] + 12 * (i // 5) if up else start_m - sc[i % 5] - 12 * (i // 5)
        s = cache(('pl', m, 1.2), lambda: pluck(m, 1.2)); j = int(i * dt * SR); out[j:j + len(s)] += s[:len(out) - j] * 0.6
    return out

# ---------- 和声 / 主题 ----------
A = 57  # A3
PROG = [[A, A + 3, A + 7], [A - 4, A, A + 3], [A - 2, A + 2, A + 5], [A - 5, A - 1, A + 2]]   # Am F G E(m)
ROOT = [A - 12, A - 16, A - 14, A - 17]
THEME = [(69, 2), (72, 1), (74, 1), (76, 3), (79, 1), (76, 1), (74, 1), (72, 1), (74, 1), (69, 4),
         (72, 2), (74, 1), (76, 1), (81, 3), (79, 1), (76, 1), (74, 1), (72, 1), (71, 1), (69, 4)]
SAD = [(76, 2), (74, 1), (72, 1), (71, 3), (69, 1), (72, 2), (71, 1), (69, 1), (64, 4)]
PENTA = [57, 60, 62, 64, 67, 69, 72, 74, 76, 79, 81]

MODE = {'open1': 'intro', 'face': 'intro', 'open3': 'intro2', 'drill': 'march', 'temple1': 'light', 'temple2': 'stop', 'temple_fight': 'fight',
        'fist': 'tension', 'temple_back': 'sad', 'street': 'mystery', 'hall_walk': 'mystery', 'gq': 'stop', 'surround': 'build', 'hall_fight': 'fight2',
        'drop': 'tension', 'seal': 'hit', 'road': 'sad', 'bound': 'tension', 'staff_down': 'build', 'lu_land': 'heroic', 'lu_fight': 'heavy', 'free': 'warm',
        'to_cz': 'warm', 'manor': 'light', 'duel': 'duel', 'cheer': 'light', 'snow1': 'night', 'snow2': 'night', 'fire': 'tension', 'overhear': 'tension',
        'no_retreat': 'build', 'burst': 'climax', 'k_chabo': 'climax', 'k_fuan': 'climax', 'k_crowd': 'climax', 'lq_run': 'tension', 'finisher': 'finisher',
        'after': 'heroic', 'lake': 'night2', 'drink': 'night2', 'end': 'theme', 'card': 'outro'}

beat_list = []
for s, st in zip(SHOTS, STARTS):
    for b in range(int(round(s.beats))): beat_list.append((st + b * B, MODE[s.name], b, s.beats, s.name))

theme_pos = {'i': 0}; sad_pos = {'i': 0}
def theme_note(seq, pos, gb):
    """按全局拍取主题音"""
    tot = sum(d for _, d in seq); x = gb % tot; acc = 0
    for m, d in seq:
        if acc <= x < acc + d: return (m, d) if x == acc else None
        acc += d
    return None

K, SN, CL, HC, HO, SH = kick(), snare(), clap(), hat(), hat(True), shaker()
for gi, (tg, mode, lb, nb, name) in enumerate(beat_list):
    bar = gi // 4; bi = gi % 4; ch = PROG[bar % 4]; rt = ROOT[bar % 4]
    def kk(t, g=1.0):
        put(K, t, g); i = int(t * SR); KENV[i:i + int(0.25 * SR)] = np.maximum(KENV[i:i + int(0.25 * SR)], np.linspace(1, 0, int(0.25 * SR))[:len(KENV[i:i + int(0.25 * SR)])])
    if mode in ('intro',):
        if bi == 0: put(pad(ch, 4 * B, 700), tg, 0.5, 0, 0.4); put(bass(rt, 4 * B, 'hold'), tg, 0.5)
        if lb % 2 == 0: put(taiko(), tg, 0.7, -0.2, 0.3)
        m = theme_note(THEME, 0, gi)
        if m: put(dizi(m[0], m[1] * B * 0.98), tg, 0.42, 0.15, 0.5)
    elif mode == 'intro2':
        if bi == 0: put(pad(ch, 4 * B, 1000), tg, 0.5, 0, 0.4); put(bass(rt, 4 * B, 'hold'), tg, 0.5)
        if lb >= 2: kk(tg); put(SN, tg + B / 2, 0.35); [put(HC, tg + k * B / 4, 0.18, 0.4) for k in range(4)]
        if lb >= 5: [put(SN, tg + k * B / 4, 0.15 + 0.08 * k, 0.1) for k in range(4)]
        for k in range(4): put(cache(('pl', ch[k % 3] + 12, .6), lambda: pluck(ch[k % 3] + 12, .6)), tg + k * B / 4, 0.25, -0.3, 0.3)
    elif mode == 'march':
        kk(tg); put(taiko(70), tg, 0.6, 0, 0.2)
        put(SN if bi % 2 else HC, tg + B / 2, 0.4 if bi % 2 else 0.2)
        for k in range(2): put(strings_stac(ch[(bi + k) % 3] + 12), tg + k * B / 2, 0.7, -0.35, 0.2)
        if bi == 0: put(bass(rt, 2 * B), tg, 0.7); put(pad(ch, 4 * B, 1200), tg, 0.35, 0, 0.3)
        if bi == 2: put(bass(rt, 2 * B), tg, 0.6)
        if lb in (4, 8, 12): put(brass([m + 12 for m in ch], 0.6), tg, 0.8, 0, 0.3); put(crash(), tg, 0.6, 0.3)
        m = theme_note(THEME, 0, gi)
        if m and lb >= 8: put(dizi(m[0], m[1] * B * 0.98), tg, 0.4, 0.2, 0.5)
    elif mode == 'light':
        if bi in (0, 2): kk(tg, 0.6)
        put(wood(1200 if bi % 2 else 900), tg + B / 2, 0.5, 0.4); put(SH, tg + B / 4, 1, -0.4); put(SH, tg + 3 * B / 4, 1, -0.4)
        if bi == 0: put(bass(rt, B), tg, 0.6); put(pad(ch, 4 * B, 800), tg, 0.25, 0, 0.3)
        if bi == 2: put(bass(rt + 7, B), tg, 0.5)
        for k, m in enumerate([PENTA[(gi * 3 + k * 2) % 6 + 4] for k in range(2)]):
            put(cache(('pl', m, 1.0), lambda: pluck(m, 1.0)), tg + k * B / 2, 0.38, 0.25, 0.4)
    elif mode == 'stop':
        if lb == 0: put(taiko(55), tg, 1.0); put(brass([m + 12 for m in ch], 0.8), tg, 0.9, 0, 0.4); put(crash(), tg, 0.5)
        if lb == nb - 1: put(revcym(B), tg, 0.6)
    elif mode in ('fight', 'fight2', 'climax', 'duel', 'heavy'):
        hard = mode in ('fight2', 'climax')
        if mode == 'heavy':
            if bi in (0, 2): kk(tg); put(taiko(52), tg, 0.8)
            if bi in (1, 3): put(CL, tg, 0.6); put(SN, tg, 0.4)
        else:
            kk(tg)
            if hard or bi in (0, 2): kk(tg + B / 2, 0.55) if hard and bi in (1, 3) else None
            if bi % 2: put(SN, tg, 0.55); put(CL, tg, 0.35)
            for k in range(4 if hard else 2): put(HC, tg + k * B / (4 if hard else 2), 0.22, 0.45)
            if mode == 'duel': put(wood(1300), tg + 3 * B / 4, 0.4, -0.5)
        if hard and bi == 3: [put(tom(140 - k * 25), tg + k * B / 4, 0.5, -0.4 + k * 0.25) for k in range(4)] if (bar % 2) else None
        # 贝斯：8 分 / 16 分
        div = 4 if hard else 2
        for k in range(div): put(bass(rt + (12 if k % 2 and hard else 0), B / div * 0.95), tg + k * B / div, 0.5)
        # 琵琶轮指 / 古筝琶音
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24]
        for k in range(4):
            m = arp[(k + gi) % 4]
            put(cache(('pl', m, .5), lambda: pluck(m, .5, 0.8)), tg + k * B / 4, 0.24, -0.3 + 0.2 * (k % 2), 0.25)
        if bi == 0: put(pad(ch, 4 * B, 1400 if hard else 1000), tg, 0.3, 0, 0.3)
        if bi == 0 and hard: put(choir([m + 12 for m in ch], 4 * B), tg, 0.35, 0, 0.5)
        if bi == 0 and lb % 4 == 0: put(brass([m + 12 for m in ch], 0.5), tg, 0.6, 0, 0.3)
        if mode == 'climax' or mode == 'fight2':
            m = theme_note(THEME, 0, gi)
            if m: put(dizi(m[0] + 12, m[1] * B * 0.98), tg, 0.3, 0.2, 0.5)
    elif mode == 'tension':
        if bi == 0: put(tremolo([A + 12, A + 13], 4 * B), tg, 0.35, 0.3, 0.4); put(bass(A - 24, 4 * B, 'hold'), tg, 0.5)
        if bi in (0, 2): kk(tg, 0.6); put(K, tg + 0.18, 0.4)
        put(cache(('pl', 81, .8), lambda: pluck(81, .8)), tg + B / 2, 0.15, 0.5, 0.6) if bi == 3 else None
    elif mode == 'sad':
        if bi == 0: put(pad(ch, 4 * B, 700), tg, 0.45, 0, 0.5); put(bass(rt, 4 * B, 'hold'), tg, 0.45)
        m = theme_note(SAD, 0, gi)
        if m: put(erhu(m[0], m[1] * B), tg, 0.5, 0.1, 0.6)
        if bi == 0 or bi == 2: put(taiko(48), tg, 0.35)
        put(cache(('pl', ch[bi % 3] + 12, 1.2), lambda: pluck(ch[bi % 3] + 12, 1.2)), tg, 0.2, -0.3, 0.5)
    elif mode == 'mystery':
        if bi == 0: put(pad([A, A + 3, A + 6], 4 * B, 600), tg, 0.4, 0, 0.5); put(bass(A - 12, 4 * B, 'hold'), tg, 0.4)
        for k in range(2):
            m = [A, A + 3, A + 6, A + 3][(bi * 2 + k) % 4] + 12
            put(cache(('pl', m, .7), lambda: pluck(m, .7)), tg + k * B / 2, 0.3, 0.3, 0.4)
        put(SH, tg + B / 2, 0.8, -0.4)
        if bi == 0: kk(tg, 0.5)
    elif mode == 'build':
        prog = (lb + 1) / nb
        put(SN, tg, 0.2 + 0.4 * prog); put(SN, tg + B / 2, 0.2 + 0.4 * prog)
        if prog > 0.5: put(SN, tg + B / 4, 0.3 * prog); put(SN, tg + 3 * B / 4, 0.3 * prog)
        if lb == 0: put(riser(nb * B), tg, 0.5, 0, 0.3); put(tremolo([A, A + 7], nb * B), tg, 0.3, 0, 0.4); put(bass(A - 24, nb * B, 'hold'), tg, 0.4)
        kk(tg, 0.5 + 0.4 * prog)
    elif mode == 'hit':
        if lb == 0: put(taiko(45), tg + 0.5 * B, 1.1); put(brass([A, A + 3, A + 7, A + 12], 1.5), tg + 0.5 * B, 0.9, 0, 0.6); put(crash(), tg + 0.5 * B, 0.7)
        if lb == 0: put(pad([A - 12, A - 5], 3 * B, 500), tg + 0.5 * B, 0.4, 0, 0.6)
    elif mode == 'heroic':
        kk(tg); put(taiko(58), tg, 0.6)
        if bi % 2: put(SN, tg, 0.45); put(CL, tg, 0.3)
        for k in range(2): put(HC, tg + k * B / 2, 0.2, 0.4)
        if bi == 0: put(brass([m + 12 for m in ch], 1.0), tg, 0.7, 0, 0.4); put(choir([m + 12 for m in ch], 4 * B), tg, 0.4, 0, 0.5); put(bass(rt, 4 * B, 'hold'), tg, 0.5)
        m = theme_note(THEME, 0, gi)
        if m: put(dizi(m[0] + 12, m[1] * B * 0.98), tg, 0.35, 0.2, 0.5)
    elif mode == 'warm':
        if bi in (0, 2): kk(tg, 0.6)
        if bi in (1, 3): put(CL, tg, 0.3)
        put(SH, tg + B / 2, 0.7, -0.3)
        if bi == 0: put(pad(ch, 4 * B, 1000), tg, 0.35, 0, 0.4); put(bass(rt, 2 * B), tg, 0.55)
        if bi == 2: put(bass(rt + 7, 2 * B), tg, 0.45)
        m = theme_note(THEME, 0, gi)
        if m: put(dizi(m[0], m[1] * B * 0.98), tg, 0.42, 0.15, 0.5)
    elif mode in ('night', 'night2'):
        if bi == 0: put(pad(ch, 4 * B, 600), tg, 0.35, 0, 0.6); put(bass(rt, 4 * B, 'hold'), tg, 0.3)
        if bi % 2 == 0:
            m = PENTA[(gi * 5) % 7 + 3]; put(cache(('pl', m, 2.0), lambda: pluck(m, 2.0)), tg, 0.32, 0.3 - 0.6 * (gi % 2), 0.7)
        if mode == 'night2':
            m = theme_note(SAD, 0, gi)
            if m: put(dizi(m[0], m[1] * B), tg, 0.35, 0.1, 0.7)
    elif mode == 'finisher':
        if lb == 0: put(riser(2.5 * B), tg, 0.6, 0, 0.3); put(revcym(2.5 * B), tg, 0.6); put(tremolo([A + 12, A + 19], 2.5 * B), tg, 0.35, 0, 0.5); put(bass(A - 24, 2.5 * B, 'hold'), tg, 0.4)
        if lb >= 3:
            kk(tg); put(taiko(55), tg, 0.7)
            if bi % 2: put(SN, tg, 0.5)
            if lb == 3: put(brass([A + 12, A + 15, A + 19, A + 24], 1.5), tg - 0.5 * B, 0.9, 0, 0.5); put(choir([A + 12, A + 15, A + 19], 4 * B), tg - 0.5 * B, 0.5, 0, 0.6)
            m = theme_note(THEME, 0, gi)
            if m: put(dizi(m[0] + 12, m[1] * B), tg, 0.35, 0.2, 0.5)
    elif mode == 'theme':
        if bi in (0, 2): kk(tg, 0.8)
        if bi in (1, 3): put(SN, tg, 0.4)
        put(HC, tg + B / 2, 0.2, 0.4)
        if bi == 0: put(pad(ch, 4 * B, 1000), tg, 0.4, 0, 0.5); put(bass(rt, 4 * B, 'hold'), tg, 0.5); put(choir([m + 12 for m in ch], 4 * B), tg, 0.3, 0, 0.5)
        m = theme_note(THEME, 0, gi)
        if m: put(dizi(m[0], m[1] * B * 0.98), tg, 0.5, 0.1, 0.5)
        if lb == 0: put(gliss(69, 12), tg, 0.6, -0.3, 0.5)
    elif mode == 'outro':
        if bi == 0: put(pad(ch, 4 * B, 900), tg, 0.35, 0, 0.6); put(bass(rt, 4 * B, 'hold'), tg, 0.35)
        m = PENTA[(gi * 3) % 6 + 5]; put(bell(m + 12, 1.6), tg, 0.45, 0.3 - 0.6 * (gi % 2), 0.6)
        if lb < 8 and bi in (0, 2): kk(tg, 0.5)

# ---------- 音效 ----------
def boom(): t = T(int(1.2 * SR)); f = 34 + 70 * np.exp(-t * 7); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5) * 1.2 + fft_filt(rng.standard_normal(len(t)), None, 500) * np.exp(-t * 5) * 0.5
def hit():
    t = T(int(.3 * SR)); body = np.sin(2 * np.pi * np.cumsum(55 + 140 * np.exp(-t * 45)) / SR) * np.exp(-t * 12)
    slap = fft_filt(rng.standard_normal(len(t)), 600, 6000) * np.exp(-t * 40) * 0.8; return body + slap
def whoosh(d=0.5):
    n = int(d * SR); t = T(n); x = rng.standard_normal(n); out = np.zeros(n); seg = 1024
    for i in range(0, n, seg):
        k = i / n; c = 500 + 2500 * math.sin(k * math.pi); out[i:i + seg] = fft_filt(x[i:i + seg], c * 0.6, c * 1.6)[:len(out[i:i + seg])]
    return out * np.sin(np.pi * t / d) ** 2 * 1.1
def swish(): return whoosh(0.22) * 1.2
def metal(fs, d=1.0, dec=5):
    t = T(int(d * SR)); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (dec + f / 900)) for f in fs) / len(fs) + fft_filt(rng.standard_normal(len(t)), 3000) * np.exp(-t * 40) * 0.5
def gong():
    t = T(int(4 * SR)); parts = [(98, 1), (147, .7), (205, .5), (263, .4), (351, .3), (462, .2), (590, .15)]
    return sum(a * np.sin(2 * np.pi * f * (1 + 0.012 * np.exp(-t * 1.5)) * t) * np.exp(-t * (0.6 + f / 900)) for f, a in parts) * 0.5 * np.clip(t / 0.02, 0, 1)
def crashfx(): t = T(int(1.6 * SR)); return fft_filt(rng.standard_normal(len(t)), None, 3000) * np.exp(-t * 2.6) * 0.8 + np.pad(boom(), (0, max(0, len(t) - int(1.2 * SR))))[:len(t)] * 0.8
def crack():
    n = int(.35 * SR); s = np.zeros(n)
    for k in range(8): i = int(rng.uniform(0, .25) * SR); s[i:i + 300] += rng.standard_normal(300) * np.exp(-np.arange(300) / 50)
    return fft_filt(s, 1200) * 1.6
def thunder():
    t = T(int(2.5 * SR)); x = fft_filt(rng.standard_normal(len(t)), None, 400) * (np.exp(-t * 1.5) + 0.6 * np.exp(-((t - .5) ** 2) * 20)); return x * 2.2 + crack()[:len(t)].sum() * 0
def voice(pitches, dur=0.13, gap=0.16, vowel=(700, 1100)):
    n = int((len(pitches) * gap + 0.3) * SR); out = np.zeros(n)
    for i, f in enumerate(pitches):
        m = int(dur * SR); t = T(m); s = saw(f, m) * np.sin(np.pi * t / dur)
        s = fft_filt(s, vowel[0] * .7, vowel[0] * 1.3) + fft_filt(s, vowel[1] * .8, vowel[1] * 1.2) * 0.6
        j = int(i * gap * SR); out[j:j + m] += s
    return out * 1.4
def cheer():
    n = int(1.2 * SR); out = np.zeros(n)
    for k in range(14):
        f = rng.uniform(150, 320); s = voice([f], rng.uniform(.2, .4), .1, (rng.uniform(600, 800), rng.uniform(1000, 1300)))
        j = int(rng.uniform(0, .6) * SR); out[j:j + len(s)] += s[:n - j] * 0.3
    return out + fft_filt(rng.standard_normal(n), 400, 3000) * np.exp(-T(n) * 2) * 0.15
def snowstep(): t = T(int(.14 * SR)); return fft_filt(rng.standard_normal(len(t)), 800, 4000) * np.exp(-t * 30) * (1 + rng.random(len(t))) * 0.35
def step(): t = T(int(.12 * SR)); return fft_filt(rng.standard_normal(len(t)), None, 500) * np.exp(-t * 40) * 0.8
def thud(): t = T(int(.4 * SR)); return np.sin(2 * np.pi * np.cumsum(50 + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 10) + fft_filt(rng.standard_normal(len(t)), None, 800) * np.exp(-t * 20) * 0.5
def fire():
    n = int(4 * B * SR); s = fft_filt(rng.standard_normal(n), None, 300) * 0.6
    for k in range(160): i = int(rng.uniform(0, 4 * B - .01) * SR); s[i:i + 160] += rng.standard_normal(160) * np.exp(-np.arange(160) / 25) * rng.uniform(.3, 1)
    return s * np.minimum(1, T(n) / 0.3) * np.minimum(1, (4 * B - T(n)) / 0.6)
def wind(d=8 * B):
    n = int(d * SR); x = fft_filt(rng.standard_normal(n), 150, 900)
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.3 * T(n) + 1); return x * lfo * np.minimum(1, T(n)) * np.minimum(1, (d - T(n)) / 1.5) * 1.6
def heartbeat(): t = T(int(.5 * SR)); b1 = np.sin(2 * np.pi * 50 * t) * np.exp(-t * 20); b2 = np.roll(b1, int(.18 * SR)) * 0.7; return (b1 + b2) * 1.4
def shatter():
    n = int(1.2 * SR); out = fft_filt(rng.standard_normal(n), 2500) * np.exp(-T(n) * 5) * 0.6
    for k in range(25):
        f = rng.uniform(2500, 7000); m = int(.3 * SR); j = int(rng.uniform(0, .4) * SR)
        out[j:j + m] += np.sin(2 * np.pi * f * T(m)) * np.exp(-T(m) * 18) * 0.25
    return out + boom()[:n] * 0.6
def arrow(): t = T(int(.7 * SR)); return np.sin(2 * np.pi * np.cumsum(2400 - 1400 * t / .7) / SR) * np.sin(np.pi * t / .7) * 0.3 + whoosh(.7) * 0.4
def gulp(): t = T(int(.25 * SR)); return np.sin(2 * np.pi * np.cumsum(300 - 200 * t / .25) / SR) * np.exp(-t * 14) * 0.6
def breath(): t = T(int(.6 * SR)); return fft_filt(rng.standard_normal(len(t)), 400, 2500) * np.sin(np.pi * t / .6) * 0.25
def shimmer(): t = T(int(1.4 * SR)); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 2.5) for f in (1760, 2217, 2637, 3520)) * 0.18
def tension(): return tremolo([A + 12, A + 13, A + 19], 2 * B) * 0.6
def grab(): t = T(int(.15 * SR)); return fft_filt(rng.standard_normal(len(t)), 300, 2500) * np.exp(-t * 30) * 0.7
def tremble(): t = T(int(2 * B * SR)); return np.sin(2 * np.pi * 45 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * 0.4
def mx(*a):
    n = max(len(x) for x in a); o = np.zeros(n)
    for x in a: o[:len(x)] += x
    return o
def stab(): return mx(metal([1900, 2700, 3800], .5, 9) * 0.6, hit() * 0.8)
def laugh(): return voice([260, 240, 225, 210], 0.12, 0.15, (750, 1150))
def bigimpact(): return mx(boom() * 1.3, crashfx() * 0.6)

FX = {'hit': (hit, .9, .3), 'whoosh': (whoosh, .7, .3), 'swish': (swish, .6, .2), 'stamp': (boom, 1.1, .3), 'boom': (lambda: taiko(50), .9, .3), 'title': (lambda: taiko(58), .7, .3),
      'land': (boom, 1.1, .2), 'gong': (gong, .7, .6), 'clang': (lambda: metal([820, 1250, 1880, 2650, 3400], .9), .55, .4), 'crash': (crashfx, .9, .3), 'crack': (crack, .9, .2),
      'wood': (wood, .5, .2), 'step': (step, .5, 0), 'snowstep': (snowstep, .5, 0), 'whip': (lambda: fft_filt(rng.standard_normal(int(.1 * SR)), 2500) * np.exp(-T(int(.1 * SR)) * 50) * 1.4, .7, .2),
      'fire': (fire, .6, .2), 'wind': (wind, .45, .2), 'laugh': (laugh, .6, .3), 'flip': (lambda: whoosh(.3), .6, .2), 'shimmer': (shimmer, .6, .6), 'thunder': (thunder, .9, .4),
      'taiko': (lambda: taiko(66), .7, .2), 'thud': (thud, .8, .2), 'tremble': (tremble, .6, 0), 'tension': (tension, .6, .4), 'cheer': (cheer, .6, .3), 'heartbeat': (heartbeat, .9, 0),
      'shatter': (shatter, .8, .4), 'stab': (stab, .9, .3), 'arrow': (arrow, .7, .4), 'gulp': (gulp, .7, .1), 'breath': (breath, .6, .2), 'grab': (grab, .6, .1), 'bigimpact': (bigimpact, 1.1, .4),
      'riser': (lambda: np.zeros(10), 0, 0), 'flash': (shimmer, .4, .5)}
fxc = {}
for tg, k in EVENTS:
    if k not in FX: print('no fx', k); continue
    fn, g, rv = FX[k]
    if k in ('hit', 'whoosh', 'swish', 'crack', 'step', 'snowstep', 'cheer', 'laugh'): sig = fn()
    else:
        if k not in fxc: fxc[k] = fn()
        sig = fxc[k]
    put(sig, tg, g, rng.uniform(-0.3, 0.3), rv, sfx=True)
    if k in ('hit', 'stab', 'land', 'bigimpact', 'stamp'):
        i = int(tg * SR); KENV[i:i + int(.3 * SR)] = np.maximum(KENV[i:i + int(.3 * SR)], np.linspace(1, 0, int(.3 * SR))[:len(KENV[i:i + int(.3 * SR)])])

# ---------- 混音 ----------
duck = 1 - 0.45 * KENV
mL = L * duck; mR = R * duck
# 混响（合成 IR，FFT 卷积）
ir_n = int(2.4 * SR); irt = T(ir_n)
irL = rng.standard_normal(ir_n) * np.exp(-irt * 2.6); irR = rng.standard_normal(ir_n) * np.exp(-irt * 2.6)
irL[:int(.02 * SR)] = 0; irR[:int(.025 * SR)] = 0
def conv(x, h):
    n = len(x) + len(h); nf = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(h, nf), nf)[:len(x)]
rv_in = fft_filt(RV, 200, 6000)
revL = conv(rv_in, irL) * 0.035; revR = conv(rv_in, irR) * 0.035
outL = mL * 0.62 + SFXL * 0.8 + revL; outR = mR * 0.62 + SFXR * 0.8 + revR
# 末尾淡出
outL = outL[:int(TOTAL * SR)]; outR = outR[:int(TOTAL * SR)]
fade = int(2.0 * SR); outL[-fade:] *= np.linspace(1, 0, fade); outR[-fade:] *= np.linspace(1, 0, fade)
pk = np.percentile(np.abs(np.concatenate([outL, outR])), 99.8) + 1e-9
outL = np.tanh(outL / pk * 0.95) * 0.9; outR = np.tanh(outR / pk * 0.95) * 0.9
st = np.stack([outL, outR], 1)
w = wave.open('lin_v2_audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
print('audio ok', len(outL) / SR)

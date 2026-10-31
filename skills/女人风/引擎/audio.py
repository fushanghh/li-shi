# 随份子从哪儿来 —— 自写古风配乐（D 宫五声，112 BPM）+ 音效
import json, math, numpy as np, soundfile as sf, subprocess
SR = 44100
J = json.load(open('out/timing.json')); T0 = J['T0']; TOTAL = J['TOTAL']; SECS = J['secs']; BPM = J['BPM']
BEAT = 60 / BPM; BAR = BEAT * 4
N = int((TOTAL + 2.5) * SR)
mus = np.zeros((N, 2)); sfx = np.zeros((N, 2))
rng = np.random.default_rng(1)

def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def add(buf, t, x, pan=0.0, g=1.0):
    i = int(t * SR)
    if i >= N or i + len(x) <= 0: return
    if i < 0: x = x[-i:]; i = 0
    x = x[:N - i]
    l = math.cos((pan + 1) * math.pi / 4); r = math.sin((pan + 1) * math.pi / 4)
    buf[i:i + len(x), 0] += x * g * l * 1.414; buf[i:i + len(x), 1] += x * g * r * 1.414

def env(n, a, d):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d); return e

def lp(x, k=0.3):   # 一阶低通
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += k * (x[i] - acc); y[i] = acc
    return y

from scipy.signal import lfilter, butter
def bp(x, lo, hi, o=2):
    b, a = butter(o, [lo / (SR / 2), hi / (SR / 2)], 'band'); return lfilter(b, a, x)
def hp(x, f, o=2):
    b, a = butter(o, f / (SR / 2), 'high'); return lfilter(b, a, x)
def lpf(x, f, o=2):
    b, a = butter(o, f / (SR / 2), 'low'); return lfilter(b, a, x)

# ---------------- 乐器 ----------------
def zheng(m, dur=1.2, vel=0.5, slide=False):
    f = mtof(m); n = int((dur + 0.6) * SR); t = np.arange(n) / SR
    fr = f * (1 - 0.03 * np.exp(-t / 0.05)) if slide else f
    ph = 2 * np.pi * np.cumsum(np.ones(n) * fr) / SR if slide else 2 * np.pi * f * t
    x = np.zeros(n)
    for h, (amp, dec) in enumerate(((1, 1.4), (0.55, 0.8), (0.35, 0.5), (0.22, 0.35), (0.12, 0.25), (0.08, 0.18)), 1):
        x += amp * np.sin(ph * h + h) * np.exp(-t / (dec * (1.4 if f < 300 else 1.0)))
    x *= np.minimum(1, t / 0.003)
    nz = hp(rng.normal(0, 1, int(0.012 * SR)), 2000) * 0.3; x[:len(nz)] += nz
    return x * vel * 0.35

def dizi(m, dur, vel=0.5, grace=None):
    f = mtof(m); n = int((dur + 0.08) * SR); t = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.6 * t) * np.minimum(1, np.maximum(0, (t - 0.18) / 0.3))
    fr = np.full(n, f) * vib
    if grace is not None:
        gn = int(0.06 * SR); fr[:gn] = mtof(grace)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    x = np.sin(ph) + 0.32 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph) + 0.05 * np.sin(4 * ph)
    e = np.minimum(1, t / 0.035) * np.minimum(1, np.maximum(0, (dur + 0.08 - t)) / 0.08)
    br = bp(rng.normal(0, 1, n), 1500, 6000) * 0.10 * (0.4 + 0.6 * np.exp(-t / 0.1))
    return (x * 0.5 + br) * e * vel * 0.32

def suona(m, dur, vel=0.5):
    f = mtof(m); n = int((dur + 0.05) * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(np.full(n, f) * (1 + 0.008 * np.sin(2 * np.pi * 6 * t))) / SR
    x = sum((1 / k) * np.sin(k * ph) for k in range(1, 9))
    x = bp(x, 500, 4000) * np.minimum(1, t / 0.02) * np.minimum(1, np.maximum(0, dur + 0.05 - t) / 0.05)
    return x * vel * 0.18

def bass(m, dur=0.9, vel=0.6):
    f = mtof(m); n = int((dur + 0.3) * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t / 0.5) * np.minimum(1, t / 0.004)
    return x * vel * 0.45

def pad(ms, dur, vel=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * mtof(m) * t + k) + 0.2 * np.sin(4 * np.pi * mtof(m) * t) for k, m in enumerate(ms))
    e = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    return x * e * vel * 0.06

def tanggu(vel=0.8, f0=120):
    n = int(0.6 * SR); t = np.arange(n) / SR
    f = f0 * (0.55 + 0.45 * np.exp(-t / 0.05)); ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / 0.22) + hp(rng.normal(0, 1, n), 800) * np.exp(-t / 0.01) * 0.3
    return x * vel * 0.8

def bangzi(vel=0.6, f=1700):
    n = int(0.12 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.7 * t)) * np.exp(-t / 0.025) * vel * 0.4

def cha(vel=0.5, d=0.25):
    n = int(d * 3 * SR); t = np.arange(n) / SR
    return hp(rng.normal(0, 1, n), 5000) * np.exp(-t / d) * vel * 0.35

def gong(vel=1.0):
    n = int(4 * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * t * (1 - 0.03 * (1 - np.exp(-t / 0.8)))) * np.exp(-t / d) for f, a, d in ((110, 1, 2.5), (163, .6, 1.8), (232, .5, 1.5), (317, .35, 1.0), (450, .2, .7)))
    x += hp(rng.normal(0, 1, n), 2000) * np.exp(-t / 0.4) * 0.15
    return x * vel * 0.5

def frame_drum(vel=0.6, low=True):
    n = int(0.4 * SR); t = np.arange(n) / SR
    if low: x = np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.18)
    else: x = bp(rng.normal(0, 1, n), 900, 4000) * np.exp(-t / 0.04)
    return x * vel * 0.7

# ---------------- 旋律 ----------------
TA = [(69, 1), (71, .5), (69, .5), (66, 1), (64, 1), (62, 1.5), (64, .5), (66, 1), (69, 1), (71, 1), (74, 1), (71, .5), (69, .5), (66, 1), (64, 2), (62, 2)]
TB = [(74, 1), (71, .5), (74, .5), (76, 1), (74, 1), (71, 1), (69, 1), (66, 1), (69, 1), (71, .5), (69, .5), (66, 1), (64, 1), (66, 1), (69, 3), (None, 1)]
TC = [(69, .5), (None, .5), (69, .5), (71, .5), (74, .5), (None, .5), (71, .5), (69, .5), (66, .5), (69, .5), (None, .5), (66, .5), (64, 1), (None, 1),
      (62, .5), (64, .5), (66, .5), (69, .5), (71, .5), (None, .5), (74, 1), (76, .5), (74, .5), (71, .5), (69, .5), (66, 1), (None, 1)]
TD = [(71, 1.5), (74, .5), (71, 1), (69, 1), (66, 2), (64, 1), (66, 1), (69, 1.5), (71, .5), (69, 1), (66, 1), (71, 4)]   # 西域味：以 B 为中心
CHORDS = [(50, [62, 66, 69]), (47, [59, 62, 66]), (52, [64, 69, 71]), (45, [57, 62, 64])]   # D, Bm, Em(五声), A

def play_mel(t0, mel, bars_avail, inst='dizi', oct=0, vel=0.5, orn=True, pan=0.1):
    t = t0; end = t0 + bars_avail * BAR; i = 0
    while t < end - 1e-6:
        m, d = mel[i % len(mel)]; dd = min(d * BEAT, end - t)
        if m is not None:
            if inst == 'dizi': add(mus, t, dizi(m + oct, dd * 0.95, vel, grace=(m + oct + 2) if (orn and d >= 1 and i % 3 == 0) else None), pan)
            elif inst == 'suona': add(mus, t, suona(m + oct, dd * 0.9, vel), pan)
            else: add(mus, t, zheng(m + oct, dd + 0.4, vel, slide=(i % 4 == 0)), pan)
        t += d * BEAT; i += 1

# ---------------- 段落 ----------------
def sec_range(name):
    idx = [i for i, s in enumerate(SECS) if s == name]
    a = T0[idx[0]][0]; b = T0[idx[-1]][0] + T0[idx[-1]][1]; return a, b

def bars(a, b): return int(round((b - a) / BAR))

def groove(a, b, style):
    nb = bars(a, b)
    for k in range(nb):
        t = a + k * BAR; root, ch = CHORDS[k % 4]
        if style in ('intro', 'han', 'ming', 'hl', 'md', 'mg', 'end_full'):
            add(mus, t, bass(root, 0.9, 0.6), 0); add(mus, t + 2 * BEAT, bass(root + 7, 0.9, 0.45), 0)
        if style == 'zhou':
            add(mus, t, bass(root - 12 + 12, 2.0, 0.5), 0)
            add(mus, t, tanggu(0.6, 80), -0.1)
            for j in range(4): add(mus, t + j * BEAT, zheng(ch[j % 3] - 12, 1.0, 0.25), -0.3)
            add(mus, t, pad(ch, BAR, 0.8), 0)
            continue
        if style == 'intro':
            for j in range(8): add(mus, t + j * BEAT / 2, zheng([62, 69, 74, 76, 78, 76, 74, 69][j] + (ch[0] - 62 if k % 2 else 0), 0.5, 0.22), -0.3)
            add(mus, t + BEAT, bangzi(0.4), 0.4); add(mus, t + 3 * BEAT, bangzi(0.4), 0.4)
        if style in ('han',):
            for j in range(8): add(mus, t + j * BEAT / 2, bangzi(0.35 if j % 2 else 0.55, 1500 if j % 2 else 1900), 0.4)
            for bt in (0, 1.5, 2, 3.5): add(mus, t + bt * BEAT, tanggu(0.55, 130), -0.1)
            for j in range(4): add(mus, t + j * BEAT, zheng(ch[j % 3], 0.4, 0.3), -0.3)
        if style == 'dh':
            for bt, low in ((0, 1), (1, 0), (1.5, 0), (2, 1), (2.5, 1), (3, 0)): add(mus, t + bt * BEAT, frame_drum(0.6, low), -0.1)
            for j in range(16): add(mus, t + j * BEAT / 4, zheng([71, 74, 76, 78][j % 4] - 12, 0.25, 0.16), -0.35)
            add(mus, t, pad([59, 66, 71], BAR, 0.8), 0); add(mus, t, bass(47, 1.5, 0.5), 0)
        if style == 'feast':
            for j in range(16): add(mus, t + j * BEAT / 4, tanggu(0.25 + 0.3 * (j % 4 == 0), 150), -0.1)
            for j in range(32): add(mus, t + j * BEAT / 8, zheng([71, 74][(j // 8) % 2], 0.12, 0.12), 0.3)
            add(mus, t + BEAT, cha(0.4, 0.15), 0.3); add(mus, t + 3 * BEAT, cha(0.4, 0.15), 0.3)
            add(mus, t, bass(47, 0.5, 0.6), 0); add(mus, t + 2 * BEAT, bass(54, 0.5, 0.5), 0)
        if style in ('ming', 'hl'):
            for j in range(8): add(mus, t + j * BEAT / 2, zheng([ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]][j], 0.5, 0.2), -0.35)
            add(mus, t + BEAT, bangzi(0.3), 0.4); add(mus, t + 3 * BEAT, bangzi(0.3), 0.4)
            add(mus, t, pad(ch, BAR, 0.6), 0)
            if style == 'hl': add(mus, t, tanggu(0.35, 110), 0); add(mus, t + 2.5 * BEAT, tanggu(0.25, 110), 0)
        if style == 'mg':
            for bt in (0, 1, 2, 2.5, 3): add(mus, t + bt * BEAT, tanggu(0.5, 140), -0.1)
            add(mus, t + BEAT, cha(0.5, 0.2), 0.3); add(mus, t + 3 * BEAT, cha(0.5, 0.2), 0.3)
            for j in range(8): add(mus, t + j * BEAT / 2, bangzi(0.3, 1800), 0.4)
        if style == 'md':
            for bt in (0, 1.5, 2, 3, 3.5): add(mus, t + bt * BEAT, tanggu(0.6, 100), -0.1)
            add(mus, t + BEAT, cha(0.45, 0.12), 0.3); add(mus, t + 3 * BEAT, cha(0.45, 0.12), 0.3)
            for j in range(8): add(mus, t + j * BEAT / 2, zheng(ch[j % 3] + (12 if j >= 4 else 0), 0.4, 0.22), -0.35)
        if style == 'end_solo':
            add(mus, t, pad(ch, BAR, 0.9), 0)
            for j in range(4): add(mus, t + j * BEAT, zheng(ch[j % 3], 1.2, 0.18), -0.3)
        if style == 'end_full':
            for j in range(8): add(mus, t + j * BEAT / 2, zheng([62, 69, 74, 76, 78, 76, 74, 69][j] + (ch[0] - 62 if k % 2 else 0), 0.5, 0.22), -0.3)
            add(mus, t, tanggu(0.45, 110), 0); add(mus, t + 2 * BEAT, tanggu(0.35, 110), 0); add(mus, t + BEAT, bangzi(0.35), 0.4); add(mus, t + 3 * BEAT, bangzi(0.35), 0.4)
            add(mus, t, pad(ch, BAR, 0.6), 0)

a, b = sec_range('intro'); groove(a, b, 'intro'); play_mel(a, TA, bars(a, b), 'dizi', 0, 0.42)
a, b = sec_range('title'); add(mus, a, gong(1.0), 0); add(mus, a, tanggu(1.0, 90), 0); add(mus, a + BEAT * 0.5, tanggu(0.7, 90), 0); add(mus, a, cha(0.8, 0.6), 0.2)
for k in range(bars(a, b)): add(mus, a + k * BAR, pad([50, 57, 62, 66], BAR, 1.0), 0)
play_mel(a + BAR, TA[-2:], 1, 'dizi', 0, 0.4)
a, b = sec_range('zhou'); groove(a, b, 'zhou'); play_mel(a + BAR, TA, bars(a, b) - 1, 'dizi', -12, 0.5)
a, b = sec_range('han'); groove(a, b, 'han'); play_mel(a, TC, bars(a, b), 'zheng', 0, 0.55)
add(mus, a, cha(0.6, 0.3), 0)
a, b = sec_range('dh'); groove(a, b, 'dh'); play_mel(a + BAR, TD, bars(a, b) - 1, 'dizi', 0, 0.5); add(mus, a, gong(0.6), 0)
a, b = sec_range('feast'); groove(a, b, 'feast'); play_mel(a, TC, bars(a, b), 'dizi', 12, 0.35, orn=False)
a, b = sec_range('ming'); groove(a, b, 'ming'); play_mel(a, TA, bars(a, b), 'dizi', 0, 0.45)
a, b = sec_range('hl'); groove(a, b, 'hl'); play_mel(a, TB + TA, bars(a, b), 'dizi', 0, 0.5)
a, b = sec_range('mg'); groove(a, b, 'mg'); play_mel(a, TC, bars(a, b), 'suona', 0, 0.55)
a, b = sec_range('md'); groove(a, b, 'md'); play_mel(a, TB, bars(a, b), 'dizi', 0, 0.5)
a, b = sec_range('end')
i25 = SECS.index('end'); mid = T0[i25][0] + T0[i25][1]
groove(a, mid, 'end_solo'); play_mel(a, TA, bars(a, mid), 'dizi', 0, 0.5)
groove(mid, b, 'end_full'); play_mel(mid, TB[:8] + [(69, 1), (66, 1), (64, 1), (62, 5)], bars(mid, b), 'dizi', 0, 0.5)
add(mus, b - BEAT * 0.01, gong(0.9), 0); add(mus, b, pad([50, 57, 62, 66], 2.4, 1.0), 0)

# ---------------- 音效 ----------------
def noise(d): return rng.normal(0, 1, int(d * SR))
def rustle(d=0.3, v=0.5):
    x = bp(noise(d), 2000, 8000); t = np.arange(len(x)) / SR; return x * (0.5 + 0.5 * np.abs(np.sin(t * 60))) * np.exp(-t / (d / 2)) * v * 0.3
def thump(v=0.6):
    n = int(0.2 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * 140 * t) * np.exp(-t / 0.05) + lpf(rng.normal(0, 1, n), 1200) * np.exp(-t / 0.03) * 0.5) * v * 0.6
def coin(v=0.5, f=2600):
    n = int(0.5 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t / (0.15 / k)) for k in (1, 1.52, 2.31)) * v * 0.15
def ding(v=0.6):
    n = int(0.8 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2093 * t * (t > 0.09))) * np.exp(-t / 0.3) * v * 0.25
def pop(v=0.5):
    n = int(0.12 * SR); t = np.arange(n) / SR; f = 400 + 900 * t / 0.12; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.04) * v * 0.5
def whoosh(d=0.4, v=0.5):
    x = noise(d); t = np.arange(len(x)) / SR; e = np.sin(np.pi * t / d) ** 2; return bp(x, 400, 3000) * e * v * 0.4
def scratch(d=0.6, v=0.4):
    x = bp(noise(d), 3000, 9000); t = np.arange(len(x)) / SR; return x * (0.3 + 0.7 * (np.sin(t * 2 * np.pi * 7) > 0)) * v * 0.18
def step(v=0.3):
    n = int(0.1 * SR); t = np.arange(n) / SR; return lpf(rng.normal(0, 1, n), 900) * np.exp(-t / 0.025) * v
def murmur(d, v=0.25):
    x = bp(noise(d), 250, 1600); t = np.arange(len(x)) / SR
    m = 0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * t) * np.sin(2 * np.pi * 0.7 * t + 1); return x * m * np.minimum(1, np.minimum(t, d - t) / 0.3) * v * 0.25
def wind(d, v=0.3):
    x = lpf(noise(d), 600); t = np.arange(len(x)) / SR; return x * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t)) * np.minimum(1, np.minimum(t, d - t) / 0.5) * v * 0.6
def clack(v=0.5):
    n = int(0.08 * SR); t = np.arange(n) / SR; return bp(rng.normal(0, 1, n), 800, 3000) * np.exp(-t / 0.012) * v
def splash(v=0.5):
    x = bp(noise(0.6), 600, 5000); t = np.arange(len(x)) / SR; return x * np.exp(-t / 0.15) * v * 0.4
def pour(d=1.2, v=0.4):
    x = bp(noise(d), 300, 1500); t = np.arange(len(x)) / SR; return x * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t + np.sin(t * 13))) * np.minimum(1, np.minimum(t, d - t) / 0.1) * v * 0.4
def stamp(v=0.8): return thump(v) + cha(0.3, 0.1)[:int(0.2 * SR)].copy().resize(int(0.2 * SR)) if False else thump(v)
def bells(v=0.3):
    n = int(0.6 * SR); t = np.arange(n) / SR; return sum(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.2) for f in (2200, 3100, 3900)) * v * 0.1
def heartbeat(v=0.6):
    return np.concatenate([tanggu(v, 55)[:int(0.25 * SR)], tanggu(v * 0.7, 55)[:int(0.35 * SR)]])
def firecracker(d=1.2, v=0.5):
    x = np.zeros(int(d * SR))
    for k in range(40):
        i = int(rng.uniform(0, d - 0.05) * SR); b = hp(rng.normal(0, 1, int(0.03 * SR)), 1500) * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.006); x[i:i + len(b)] += b
    return x * v * 0.5
def abacus(v=0.5):
    n = int(0.05 * SR); t = np.arange(n) / SR; return bp(rng.normal(0, 1, n), 2500, 6000) * np.exp(-t / 0.006) * v

def at(i, beats=0.0): return T0[i][0] + beats * BEAT
def shot(name): return J['names'].index(name)
WIPES = [3, 6, 10, 14, 16, 18, 21, 23, 25]
for i in WIPES: add(sfx, at(i) - 0.05, whoosh(0.45, 0.6), 0.2)

i = shot('s_hook'); add(sfx, at(i), murmur(T0[i][1] + T0[i + 1][1], 0.8), 0)
for k in range(4):
    add(sfx, at(i, k * 2 + 0.2), rustle(0.25, 0.6), 0.3); add(sfx, at(i, k * 2 + 1.0), thump(0.5), 0.4); add(sfx, at(i, k * 2 + 1.0), coin(0.5), 0.3)
i = shot('s_book'); add(sfx, at(i), rustle(0.5, 0.8), 0); add(sfx, at(i, 1), scratch(1.5, 0.6), 0.2); add(sfx, at(i, 5), pop(0.6), 0.3)
i = shot('s_title'); add(sfx, at(i), whoosh(0.6, 0.8), 0)
for name in ('s_zhou1', 's_zhou2'):
    i = shot(name); add(sfx, at(i), wind(T0[i][1], 0.8), 0)
    for k in range(int(T0[i][1] / BEAT)): add(sfx, at(i, k), step(0.25), -0.3)
add(sfx, at(shot('s_zhou2'), 3), rustle(0.6, 0.8), 0)
i = shot('s_zhou3')
for k in range(4): add(sfx, at(i, k * 0.75), clack(0.6), 0)
add(sfx, at(i, 5), pop(0.6), 0.3)
i = shot('s_han1'); add(sfx, at(i), murmur(T0[i][1] * 2, 0.9), 0)
for k in range(int(T0[i][1] / BEAT)): add(sfx, at(i, k), step(0.25), -0.3); add(sfx, at(i, k + 0.5), coin(0.15, 3000), -0.3)
i = shot('s_han2'); add(sfx, at(i), clack(0.6), 0.3); add(sfx, at(i, 1), scratch(2.0, 0.6), 0.3); add(sfx, at(i, 5), pop(0.7), -0.3)
i = shot('s_han3'); add(sfx, at(i), whoosh(0.4, 0.5), -0.2); add(sfx, at(i, 1), pop(0.5), -0.2); add(sfx, at(i, 3), scratch(2.8, 0.7), -0.2)
add(sfx, at(i, 6), tanggu(1.0, 70), 0); add(sfx, at(i, 6), cha(0.9, 0.5), 0); add(sfx, at(i, 6), gong(0.5), 0)
i = shot('s_han4'); add(sfx, at(i), murmur(T0[i][1], 0.9), 0)
for k in range(10): add(sfx, at(i, k * 0.5), step(0.35), 0.3)
add(sfx, at(i, 6), bells(0.6), 0)
i = shot('s_dh0'); add(sfx, at(i), wind(T0[i][1], 1.0), 0)
for k in range(8): add(sfx, at(i, k), bells(0.35), 0.4)
i = shot('s_dh1')
for k in range(int(T0[i][1] / BEAT)): add(sfx, at(i, k), step(0.2), 0)
i = shot('s_dh2'); add(sfx, at(i), rustle(0.8, 0.9), 0); add(sfx, at(i, 2), scratch(2.5, 0.5), 0)
i = shot('s_dh3'); add(sfx, at(i, 1.5), pour(1.6, 0.8), 0.2)
for k in (2, 3, 4): add(sfx, at(i, k), pop(0.6), 0.4)
i = shot('s_dh4'); add(sfx, at(i), murmur(T0[i][1], 1.0), 0)
for k in range(1, int(T0[i][1] / BEAT)): add(sfx, at(i, k), clack(0.7), (-0.4 if k % 2 else 0.4))
add(sfx, at(i, 6), clack(1.0), 0); add(sfx, at(i, 6.05), splash(0.8), 0)
i = shot('s_dh5'); add(sfx, at(i, 3), thump(1.0), 0); add(sfx, at(i, 3), cha(0.5, 0.2), 0); add(sfx, at(i, 0.5), whoosh(0.3, 0.4), 0.3)
i = shot('s_ming1'); add(sfx, at(i, 1), rustle(0.6, 0.7), 0); add(sfx, at(i, 4), scratch(1.5, 0.5), 0.3)
i = shot('s_ming2'); add(sfx, at(i, 2), pop(0.6), 0.3); add(sfx, at(i, 3), pop(0.6), 0.3)
i = shot('s_hl1'); add(sfx, at(i), murmur(T0[i][1], 0.6), 0)
i = shot('s_hl2')
for k in range(4): add(sfx, at(i, 1 + k * 1.5), coin(0.6, 2300), (-0.4 if k % 2 == 0 else 0.4)); add(sfx, at(i, 1 + k * 1.5 + 0.1), coin(0.4, 2700), 0)
i = shot('s_hl3')
for k in range(int(T0[i][1] / BEAT)): add(sfx, at(i, k), coin(0.35, 2500 + 100 * (k % 3)), 0); add(sfx, at(i, k), step(0.15), -0.3)
i = shot('s_mg1'); add(sfx, at(i), firecracker(1.6, 0.7), -0.5); add(sfx, at(i), murmur(T0[i][1], 0.8), 0); add(sfx, at(i, 2), scratch(2, 0.5), 0.3)
i = shot('s_mg2'); add(sfx, at(i), rustle(0.5, 0.8), 0)
for k in range(12): add(sfx, at(i, k * 0.5), abacus(0.6), 0.3)
add(sfx, at(i, 5), pop(0.6), 0.3)
i = shot('s_md1'); add(sfx, at(i), murmur(T0[i][1], 0.7), 0); add(sfx, at(i, 3), ding(0.8), 0.4); add(sfx, at(i, 3.1), coin(0.5), 0.4)
i = shot('s_md2')
for k in range(5): add(sfx, at(i, k * 1.5), pop(0.5 + 0.1 * k), 0); add(sfx, at(i, k * 1.5), coin(0.4), 0)
for k in range(0, int(T0[i][1] / BEAT), 1): add(sfx, at(i, k), heartbeat(0.5), 0)
i = shot('s_md3'); add(sfx, at(i), wind(T0[i][1], 0.5), 0)
for k in range(int(T0[i][1] / BEAT)): add(sfx, at(i, k), step(0.15), 0)
i = shot('s_end'); add(sfx, at(i), murmur(T0[i][1], 0.6), 0)
for k in range(3): add(sfx, at(i, k * 2 + 0.2), rustle(0.25, 0.5), 0.3); add(sfx, at(i, k * 2 + 1.0), thump(0.4), 0.4); add(sfx, at(i, k * 2 + 1.0), coin(0.4), 0.3)

mix = mus * 0.9 + sfx * 0.8
mix = mix[:int((TOTAL + 0.0) * SR)]
fade = int(1.5 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix /= max(1e-6, np.abs(mix).max()) / 0.9
sf.write('out/raw.wav', mix.astype(np.float32), SR)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/raw.wav', '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-ar', '44100', 'out/mix.wav'], check=True)
print('ok', TOTAL)

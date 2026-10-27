import numpy as np, wave
from film import EVENTS, TOTAL, STARTS, SCENES, B

SR = 44100
N = int((TOTAL + 2.5) * SR)
rng = np.random.default_rng(7)
music = np.zeros(N); drums = np.zeros(N); sfx = np.zeros(N)

def T(n): return np.arange(n) / SR
def add(buf, t0, sig, g=1.0):
    i = int(t0 * SR)
    if i >= N: return
    j = min(N, i + len(sig)); buf[i:j] += sig[:j - i] * g
def lp(x, a):  # 一阶低通
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def lpf(x, cut):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[f > cut] *= np.exp(-(f[f > cut] - cut) / (cut * 0.3)); return np.fft.irfft(X, len(x))
def hpf(x, cut):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[f < cut] *= (f[f < cut] / cut) ** 2; return np.fft.irfft(X, len(x))
def bpf(x, lo, hi): return hpf(lpf(x, hi), lo)

# ---------- 音色 ----------
def kick(): t = T(int(.32 * SR)); f = 45 + 110 * np.exp(-t * 28); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def snare():
    t = T(int(.22 * SR)); n = bpf(rng.standard_normal(len(t)), 900, 7000) * np.exp(-t * 18)
    return n * 0.8 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * 0.6
def hat(): t = T(int(.06 * SR)); return hpf(rng.standard_normal(len(t)), 7000) * np.exp(-t * 70)
def tom(f=95): t = T(int(.5 * SR)); ff = f * (1 + 0.5 * np.exp(-t * 20)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 6)
def pluck(freq, dur=1.2, bright=0.5):
    n = int(dur * SR); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    t = T(n); return out * np.exp(-t * 2.2) + np.sin(2 * np.pi * freq * t) * np.exp(-t * 6) * 0.3
def pad(freq, dur):
    t = T(int(dur * SR)); s = sum(np.sin(2 * np.pi * freq * k * t + k) / k for k in range(1, 7))
    env = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4); return lpf(s, 900) * env
def bass(freq, dur): t = T(int(dur * SR)); s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t); return s * np.exp(-t * 3)

# D 小调五声
def nf(semi): return 293.66 * 2 ** (semi / 12)
SCALE = [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24]

# ---------- 段落强度 ----------
def section(tg):
    for (n, nb, f), st in zip(SCENES, STARTS):
        if st <= tg < st + nb * B: return n, tg - st
    return 'end', 0
sil = [t for t, k in EVENTS if k == 'silence']
def silent(tg): return any(0 <= tg - s < B for s in sil)

nbeats = int(TOTAL / B) + 4
roots = [0, 0, -2, -5, -7, -7, -5, -2]  # D D C A G G A C (相对)
mel_rng = np.random.default_rng(3)
cache = {}
def pl(semi, dur=1.0):
    k = (semi, dur)
    if k not in cache: cache[k] = pluck(nf(semi), dur)
    return cache[k]
K, S_, H_ = kick(), snare(), hat()
for i in range(nbeats):
    tg = i * B
    if tg >= TOTAL: break
    sec, tl = section(tg)
    if silent(tg): continue
    bar, bi = divmod(i, 4)
    calm = sec in ('shenmiao',) and tl < 8 * B or sec == 'card' and tl > 12 * B
    heavy = sec in ('kill', 'baihu', 'yuemiao', 'yezhu', 'hong', 'open')
    # 鼓
    if not calm:
        if bi in (0, 2) or (heavy and bi == 3): add(drums, tg, K, 1.0)
        if bi in (1, 3): add(drums, tg, S_, 0.55)
        for h in range(2): add(drums, tg + h * B / 2, H_, 0.25 if h else 0.18)
        if heavy and sec == 'kill': add(drums, tg + B / 2, K, 0.6)
    # 贝斯 + 铺底
    r = roots[bar % 8]
    if bi == 0:
        add(music, tg, bass(nf(r - 24), 4 * B), 0.55)
        add(music, tg, pad(nf(r - 12), 4 * B), 0.12)
    elif bi == 2 and not calm:
        add(music, tg, bass(nf(r - 24), 2 * B), 0.4)
    # 旋律：古筝扫弦，每拍 1-2 个音
    if bar % 2 == 0 or heavy:
        k = mel_rng.integers(0, 6) + (2 if heavy else 0)
        add(music, tg, pl(SCALE[min(10, k)]), 0.32)
        if mel_rng.random() < 0.5 and not calm:
            add(music, tg + B / 2, pl(SCALE[min(10, max(0, k + mel_rng.integers(-2, 3)))]), 0.22)
    if calm and bi == 0:
        add(music, tg, pl(SCALE[mel_rng.integers(3, 8)], 2.0), 0.35)

# ---------- 音效 ----------
def boom(): t = T(int(1.0 * SR)); f = 38 + 60 * np.exp(-t * 8); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4) + lpf(rng.standard_normal(len(t)), 400) * np.exp(-t * 6) * 0.5
def taiko(): return tom(70) * 1.2 + lpf(rng.standard_normal(int(.5 * SR)), 1200) * np.exp(-T(int(.5 * SR)) * 15) * 0.4
def hit():
    t = T(int(.25 * SR)); return np.sin(2 * np.pi * np.cumsum(60 + 90 * np.exp(-t * 40)) / SR) * np.exp(-t * 14) + bpf(rng.standard_normal(len(t)), 300, 5000) * np.exp(-t * 35) * 0.7
def whoosh(d=0.45):
    n = int(d * SR); t = T(n); x = rng.standard_normal(n); env = np.sin(np.pi * t / d) ** 2
    return bpf(x, 400, 3500) * env * 0.8
def gong():
    t = T(int(3.5 * SR)); parts = [(110, 1), (163, .6), (231, .5), (297, .35), (402, .25), (523, .15)]
    s = sum(a * np.sin(2 * np.pi * f * (1 - 0.01 * np.exp(-t)) * t) * np.exp(-t * (0.8 + f / 600)) for f, a in parts)
    return s * 0.6
def clang():
    t = T(int(.8 * SR)); s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, d in [(820, 5), (1240, 6), (1870, 8), (2630, 10), (3400, 12)])
    return s * 0.35 + hpf(rng.standard_normal(len(t)), 3000) * np.exp(-t * 40) * 0.4
def crash():
    t = T(int(1.4 * SR)); return lpf(rng.standard_normal(len(t)), 2500) * np.exp(-t * 3) * 0.8 + np.pad(boom(), (0, len(t) - int(SR)))[:len(t)] * 0.8
def crack():
    n = int(.3 * SR); s = np.zeros(n)
    for k in range(6): i = int(rng.uniform(0, .2) * SR); s[i:i + 200] += rng.standard_normal(200) * np.exp(-np.arange(200) / 40)
    return hpf(s, 1500) * 1.5
def wood(f=1050): t = T(int(.12 * SR)); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.48 * t)) * np.exp(-t * 45)
def step(): t = T(int(.12 * SR)); return lpf(rng.standard_normal(len(t)), 400) * np.exp(-t * 40)
def whip(): t = T(int(.12 * SR)); return hpf(rng.standard_normal(len(t)), 2500) * np.exp(-t * 50) * 1.2
def fire_s():
    n = int(4 * B * SR); s = lpf(rng.standard_normal(n), 300) * 0.5
    for k in range(120):
        i = int(rng.uniform(0, 4 * B - .01) * SR); s[i:i + 150] += rng.standard_normal(150) * np.exp(-np.arange(150) / 25) * rng.uniform(.3, 1)
    env = np.minimum(1, T(n) / 0.3) * np.minimum(1, (4 * B - T(n)) / 0.5); return s * env
def wind():
    d = 8 * B; n = int(d * SR); x = lpf(rng.standard_normal(n), 600)
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.35 * T(n)); env = np.minimum(1, T(n) / 1.0) * np.minimum(1, (d - T(n)) / 1.5)
    return x * lfo * env * 1.4
def laugh(): s = np.zeros(int(.9 * SR)); [s.__setitem__(slice(int(k * .16 * SR), int(k * .16 * SR) + int(.12 * SR)), wood(900 - k * 90)) for k in range(4)]; return s
def shimmer(): t = T(int(1.2 * SR)); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 3) for f in (1760, 2217, 2637, 3520)) * 0.2

LIB = {'hit': (hit, .9), 'whoosh': (whoosh, .7), 'stamp': (boom, 1.0), 'boom': (taiko, .9), 'title': (taiko, .8), 'land': (boom, 1.0),
       'gong': (gong, .8), 'clang': (clang, .8), 'crash': (crash, .9), 'crack': (crack, .8), 'wood': (wood, .5), 'step': (step, .6),
       'whip': (whip, .7), 'fire': (fire_s, .7), 'wind': (wind, .5), 'laugh': (laugh, .6), 'flip': (lambda: whoosh(.3), .6), 'flash': (shimmer, .6)}
cacheS = {}
for tg, k in EVENTS:
    if k not in LIB: continue
    fn, g = LIB[k]
    if k in ('hit', 'whoosh', 'crack', 'fire', 'wind'):
        sig = fn()
    else:
        if k not in cacheS: cacheS[k] = fn()
        sig = cacheS[k]
    add(sfx, tg, sig, g)

# 静音拍：音乐与鼓压低
for s in sil:
    i, j = int(s * SR), int((s + B) * SR)
    music[i:j] *= np.linspace(0.15, 0.05, j - i); drums[i:j] = 0

mix = music * 0.7 + drums * 0.55 + sfx * 0.75
fade = int(2.0 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix[:int(TOTAL * SR)]
mix = np.tanh(mix / (np.percentile(np.abs(mix), 99.7) + 1e-9) * 0.9) * 0.89
out = (mix * 32767).astype(np.int16)
w = wave.open('lin_audio.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
print('audio', len(out) / SR)

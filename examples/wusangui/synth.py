import numpy as np, math
SR=44100; rng=np.random.default_rng(5); B=60/90; A=62
def T(n): return np.arange(n) / SR
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

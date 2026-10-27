import numpy as np, wave, sys
sys.argv = ['x']
from render import SCENES, STARTS, TOTAL

SR = 48000
N = int((TOTAL + 0.5) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.RandomState(7)


def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e


def lp(x, k):
    # simple one-pole lowpass, k in (0,1): smaller = darker
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += k * (x[i] - acc); y[i] = acc
    return y


def hp(x, k):
    return x - lp(x, k)


def add(t, sig, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[:N - i] * gain
    L[i:i + len(sig)] += sig * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * (1 + min(0, pan))


def noise(dur):
    return rng.randn(int(dur * SR))


# --- sound designs (precomputed bank)
def mk_tick():
    n = int(0.18 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 2400 * t) * env(n, 0.001, 0.025) * 0.5
    s += hp(noise(0.18), 0.5) * env(n, 0.001, 0.012) * 0.4
    return s


def mk_swish(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    x = noise(dur)
    sh = np.sin(np.pi * t / dur) ** 2
    y = lp(hp(x, 0.08), 0.35) * sh
    return y * 0.5


def mk_whoosh(dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    x = noise(dur)
    sh = (t / dur) ** 1.5 * np.exp(-((t / dur) ** 6) * 3)
    sh = np.sin(np.pi * (t / dur) ** 0.7) ** 2
    y = lp(x, 0.06) * sh
    return y / (np.abs(y).max() + 1e-9) * 0.6


def mk_thud(f=70, dur=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    fr = f * (1 + 1.5 * np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    s = np.sin(ph) * env(n, 0.002, 0.16)
    s += lp(noise(dur), 0.15) * env(n, 0.001, 0.03) * 0.8
    return s * 0.9


def mk_seal():
    s = mk_thud(90, 0.5)
    n = len(s)
    s += lp(hp(noise(0.5), 0.2), 0.5) * env(n, 0.001, 0.04) * 0.5
    return s


def mk_chime(f=880, dur=2.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for m, a, d in ((1, 1, 0.9), (2.76, 0.45, 0.4), (5.4, 0.25, 0.2), (8.93, 0.12, 0.1)):
        s += a * np.sin(2 * np.pi * f * m * t + m) * env(n, 0.002, d)
    return s * 0.28


def mk_boom(dur=2.5):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 48 * t * (1 + 0.6 * np.exp(-t / 0.08))) * env(n, 0.005, 0.7)
    s += lp(noise(dur), 0.02) * env(n, 0.01, 0.5) * 3
    return s / np.abs(s).max() * 0.9


def mk_riser(dur=2.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 180 + 500 * (t / dur) ** 2
    ph = 2 * np.pi * np.cumsum(f) / SR
    sh = (t / dur) ** 2 * (1 - np.exp(-(dur - t) / 0.05))
    s = (np.sin(ph) * 0.4 + np.sin(ph * 1.5) * 0.2) * sh
    s += lp(noise(dur), 0.1) * sh * 0.4
    return s * 0.5


def mk_creak(dur=2.4):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 160 + 60 * np.sin(2 * np.pi * 0.7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = (ph / (2 * np.pi)) % 1.0 * 2 - 1
    am = (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t)) * np.sin(np.pi * t / dur) ** 0.5
    s = lp(saw, 0.08) * am * 0.35
    s += mk_whoosh(dur)[:n] * 0.6
    return s


def mk_clash():
    n = int(0.9 * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for f, a in ((1850, 1), (2630, 0.7), (3720, 0.5), (5100, 0.3)):
        s += a * np.sin(2 * np.pi * f * t) * env(n, 0.0005, 0.18)
    s += hp(noise(0.9), 0.3) * env(n, 0.0005, 0.02) * 1.5
    return s * 0.18


def mk_fire(dur):
    n = int(dur * SR)
    base = lp(noise(dur), 0.03) * 0.5
    cr = np.zeros(n)
    for k in range(int(dur * 18)):
        i = rng.randint(0, n - 2000)
        L_ = rng.randint(200, 1200)
        cr[i:i + L_] += hp(rng.randn(L_), 0.4) * np.exp(-np.arange(L_) / (L_ / 5)) * rng.uniform(0.3, 1)
    t = np.arange(n) / SR
    fade = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.0)
    return (base + cr * 0.6) * fade * 0.5


def mk_rumble(dur=1.8):
    n = int(dur * SR); t = np.arange(n) / SR
    s = lp(noise(dur), 0.01) * 6 * np.sin(np.pi * t / dur)
    s += np.sin(2 * np.pi * 38 * t) * 0.3 * np.sin(np.pi * t / dur)
    # wood groan
    f = 90 + 20 * t
    s += lp(((np.cumsum(f) / SR) % 1 * 2 - 1), 0.05) * 0.25 * np.sin(np.pi * t / dur)
    return s * 0.5


def mk_brush(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 3.2 * t) ** 2
    return lp(hp(noise(dur), 0.3), 0.5) * am * 0.12


def mk_pour(dur=1.8):
    n = int(dur * SR); s = np.zeros(n)
    for k in range(int(dur * 260)):
        i = rng.randint(0, n - 600)
        s[i:i + 300] += hp(rng.randn(300), 0.5) * np.exp(-np.arange(300) / 40) * rng.uniform(0.1, 0.5)
    t = np.arange(n) / SR
    return s * np.sin(np.pi * t / dur) * 0.35


def mk_shimmer(dur=1.6):
    s = np.zeros(int(dur * SR))
    for k, f in enumerate((1320, 1760, 2093, 2637)):
        c = mk_chime(f, dur - k * 0.12)
        i = int(k * 0.12 * SR); s[i:i + len(c)] += c * 0.45
    return s


B = dict(tick=mk_tick(), swish=mk_swish(), whoosh=mk_whoosh(), thud=mk_thud(), seal=mk_seal(),
         chime=mk_chime(880), chimeL=mk_chime(587, 2.5), boom=mk_boom(), riser=mk_riser(2.0), riserS=mk_riser(1.0),
         creak=mk_creak(), clash=mk_clash(), rumble=mk_rumble(), pour=mk_pour(), shimmer=mk_shimmer(),
         book=mk_thud(130, 0.3))



def mk_coins():
    out = np.zeros(int(1.2 * SR))
    for k in range(7):
        c_ = mk_chime(rng.uniform(2200, 3600), 0.5) * rng.uniform(0.3, 0.6)
        i = int(rng.uniform(0, 0.7) * SR); out[i:i + len(c_)] += c_[:len(out) - i]
    return out


def mk_gallop(dur=3.0):
    out = np.zeros(int(dur * SR)); h = mk_thud(110, 0.25) * 0.5
    t = 0.0
    while t < dur - 0.3:
        for d in (0, 0.07, 0.16):
            i = int((t + d) * SR); out[i:i + len(h)] += h[:len(out) - i]
        t += 0.42
    tt = np.arange(len(out)) / SR
    return out * np.minimum(1, tt / 0.6) * np.minimum(1, (dur - tt) / 0.6)


def mk_ticks():
    out = np.zeros(int(1.6 * SR)); tk = mk_tick()
    for k in range(14):
        i = int(k * 0.09 * SR); out[i:i + len(tk)] += tk[:len(out) - i] * 0.5
    return out


def mk_lock():
    s_ = mk_thud(160, 0.3) * 0.6
    cl = mk_clash()[:int(0.3 * SR)] * 0.6
    out = np.zeros(int(0.5 * SR)); out[:len(s_)] += s_; out[int(0.05 * SR):int(0.05 * SR) + len(cl)] += cl
    return out


B['coins'] = mk_coins(); B['gallop'] = mk_gallop(); B['ticks'] = mk_ticks(); B['lock'] = mk_lock()
def mk_cry(dur=1.6):
    t = np.arange(int(dur * SR)) / SR
    f = 430 + 60 * np.sin(2 * np.pi * 5.5 * t) + 80 * np.sin(2 * np.pi * 0.9 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    sig = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph))
    am = (0.5 + 0.5 * np.sin(2 * np.pi * 1.6 * t - 1.5)) ** 1.5
    return sig * am * np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.2) * 0.35


B['cry'] = mk_cry()
B['brush'] = mk_brush(2.5); B['fire'] = mk_fire(5.0)


def mk_drip():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 900 + 1400 * (1 - np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.001, 0.05) * 0.6


B['drip'] = mk_drip()


def mk_growl(dur=1.1):
    t = np.arange(int(dur * SR)) / SR
    f = 70 + 40 * np.sin(2 * np.pi * 3 * t) + 30 * t
    ph = 2 * np.pi * np.cumsum(f) / SR
    am = (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t)) * np.sin(np.pi * t / dur)
    s = lp(((ph / (2 * np.pi)) % 1 * 2 - 1), 0.05) * am
    s += lp(noise(dur), 0.03) * am * 1.5
    return s / (np.abs(s).max() + 1e-9) * 0.7


B['growl'] = mk_growl(); B['drum'] = mk_thud(52, 0.9)

for i, sc in enumerate(SCENES):
    if i > 0:
        add(STARTS[i] - 0.25, B['whoosh'], 0.35)
    for cap in sc['caps']:
        add(STARTS[i] + cap[0], B['swish'], 0.18, -0.2)
    for (t0, nm, g) in sc['sfx']:
        add(STARTS[i] + t0, B[nm], g, pan=float(np.sin(t0 * 3)) * 0.3)

m = np.stack([L, R], 1)
m = m / (np.abs(m).max() + 1e-9) * 0.89
pcm = (m * 32767).astype(np.int16)
with wave.open('sfx.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', TOTAL)

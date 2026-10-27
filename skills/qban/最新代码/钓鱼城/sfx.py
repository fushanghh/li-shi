import numpy as np, wave, sys
from scipy.signal import lfilter
sys.argv = ['x']
import render
SR = 48000
N = int((render.TOTAL + 0.5) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.RandomState(7)

def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def lp(x, k): return lfilter([k], [1, -(1 - k)], x)
def hp(x, k): return x - lp(x, k)
def noise(d): return rng.randn(int(d * SR))
def add(t, sig, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i] * g
    L[i:i + len(sig)] += sig * (1 - max(0, pan)); R[i:i + len(sig)] += sig * (1 + min(0, pan))
def tone(f, d, a=0.002, dec=0.1, fm=None):
    n = int(d * SR); t = np.arange(n) / SR
    fr = f if fm is None else f * (1 + fm * np.exp(-t / 0.04))
    ph = 2 * np.pi * np.cumsum(np.ones(n) * fr) / SR
    return np.sin(ph) * env(n, a, dec)

def tick():
    return tone(2600, 0.12, 0.001, 0.02) * 0.35 + hp(noise(0.12), 0.5) * env(int(0.12 * SR), 0.001, 0.01) * 0.25
def pop():
    s = tone(520, 0.25, 0.002, 0.07, fm=0.8) * 0.6
    return s + tone(1040, 0.25, 0.002, 0.04) * 0.2
def boom():
    s = tone(60, 0.8, 0.003, 0.22, fm=1.6) * 0.9
    return s + lp(noise(0.8), 0.12) * env(int(0.8 * SR), 0.001, 0.05) * 0.6
def swish(d=0.28):
    n = int(d * SR); t = np.arange(n) / SR
    y = lp(hp(noise(d), 0.1), 0.3) * np.sin(np.pi * t / d) ** 2
    return y / (np.abs(y).max() + 1e-9) * 0.35
def sticker():
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 700 + 900 * (t / 0.3)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.08) * 0.35
    return s
def paper():
    d = 0.35; n = int(d * SR)
    y = hp(noise(d), 0.3) * env(n, 0.01, 0.09)
    return y / (np.abs(y).max() + 1e-9) * 0.25
def ding():
    return (tone(1320, 1.0, 0.001, 0.35) * 0.35 + tone(1980, 1.0, 0.001, 0.2) * 0.15)
def seal():
    return tone(90, 0.5, 0.002, 0.12, fm=1.0) * 0.8 + lp(noise(0.5), 0.3) * env(int(0.5 * SR), 0.001, 0.03) * 0.5
def scribble():
    d = 0.45; n = int(d * SR); t = np.arange(n) / SR
    y = hp(noise(d), 0.25) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)) * np.sin(np.pi * t / d)
    return y / (np.abs(y).max() + 1e-9) * 0.18
def gong():
    s = sum(tone(f, 2.5, 0.005, 0.9) * a for f, a in ((110, 0.6), (165, 0.3), (231, 0.25), (330, 0.12)))
    return s + boom() .__array__()[:int(2.5 * SR)].copy() * 0 if False else s

def fire():
    n = noise(1.6); s = lp(n, 0.08) * env(len(n), 0.2, 1.2) * 0.5
    for k in range(25):
        i = rng.randint(0, len(s) - 2000); s[i:i + 600] += hp(noise(600 / SR), 0.6) * env(600, 0.0005, 0.004) * 0.8
    return s * 0.6
def gongk():
    return sum(tone(f, 1.2, 0.002, 0.35) * a for f, a in ((620, 0.5), (930, 0.3), (1410, 0.2))) * 0.8
BANK = dict(fire=fire(), gongk=gongk(), tick=tick(), pop=pop(), boom=boom(), cut=swish(), sticker=sticker(), paper=paper(), ding=ding(),
            seal=seal(), scribble=scribble())
G = dict(fire=0.7, gongk=0.8, tick=0.5, pop=0.8, boom=0.9, cut=0.6, sticker=0.7, paper=0.8, ding=0.6, seal=1.0, scribble=0.8)
evs = render.events()
for t, k in evs:
    add(t, BANK[k], G[k], pan=rng.uniform(-0.2, 0.2))
add(0.0, gong(), 0.7); add(0.0, BANK['boom'], 1.0)
mx = max(np.abs(L).max(), np.abs(R).max())
L /= mx / 0.85; R /= mx / 0.85
st = np.stack([L, R], 1)
w = wave.open('sfx.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
print('events', len(evs), 'dur', N / SR)

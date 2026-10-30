import numpy as np, wave
from render import L, starts, dur, TOTAL, CLIMAX
from kit import parse
SR = 44100; N = int(SR * (TOTAL + 0.5))
rng = np.random.default_rng(1)
Lc = np.zeros(N); Rc = np.zeros(N)
def add(sig, t, pan=0.0, g=1.0):
    i = int(t * SR)
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    if n <= 0: return
    Lc[i:i + n] += sig[:n] * g * (1 - pan * 0.6); Rc[i:i + n] += sig[:n] * g * (1 + pan * 0.6)
def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def lp(x, k):
    y = np.copy(x)
    for _ in range(k): y = np.convolve(y, np.ones(8) / 8, 'same')
    return y
def hp(x): return x - lp(x, 2)
def noise(d): return rng.standard_normal(int(d * SR))

def tick():
    n = int(.05 * SR); return hp(rng.standard_normal(n)) * env(n, .0003, .006) * .10
def whoosh(d=.6, g=.16):
    x = noise(d); t = tt(d); e = np.sin(np.pi * t / d) ** 2; return lp(x, 4) * e * g
def ding(f=1320, g=.12):
    t = tt(1.4); return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.7 * t)) * env(len(t), .002, .4) * g
def chime(f=880):
    return sum(ding(f * m, .06) for m in (1, 1.5, 2.0))
def boom(d=2.5, f0=55, g=1.0):
    t = tt(d); body = np.sin(2 * np.pi * (f0 + 60 * np.exp(-t * 8)) * t) * env(len(t), .002, .7)
    nz = lp(noise(d), 6) * env(len(t), .001, .25)
    return (body * .9 + nz * .6) * g
def impact(g=1.0):
    t = tt(1.2); body = np.sin(2 * np.pi * (48 + 120 * np.exp(-t * 20)) * t) * env(len(t), .001, .35)
    crack = hp(noise(1.2)) * env(len(t), .0005, .05)
    return (body + crack * .7) * g
def gong(f=98, d=5, g=.5):
    t = tt(d)
    s = sum(a * np.sin(2 * np.pi * f * m * t * (1 + .002 * np.sin(t * 5))) for m, a in [(1, 1), (2.02, .5), (2.76, .35), (3.9, .2), (5.4, .12)])
    return s * env(len(t), .01, 1.4) * g
def bell(f=440, d=5, g=.35):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * m * t) for m, a in [(1, 1), (2.76, .4), (5.4, .2), (8.9, .08)])
    return s * env(len(t), .003, 1.6) * g
def shatter(g=1.0):
    d = 2.2; x = np.zeros(int(d * SR))
    x += hp(noise(d)) * env(len(x), .001, .18) * .8
    for k in range(70):
        st = int(rng.uniform(0, 1.6) * SR); m = int(.08 * SR); f = rng.uniform(2500, 7000)
        x[st:st + m] += np.sin(2 * np.pi * f * np.arange(m) / SR) * env(m, .0005, .02) * rng.uniform(.1, .35) * np.exp(-st / SR * 1.5)
    return x * g
def riser(d=2.0, g=.35):
    t = tt(d); f = 200 + 1600 * (t / d) ** 2
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * .3 + lp(noise(d), 2) * .5
    return s * (t / d) ** 2 * g
def heartbeat(g=.7):
    t = tt(.35); b = np.sin(2 * np.pi * 50 * t) * env(len(t), .003, .07)
    out = np.zeros(int(.6 * SR)); out[:len(b)] += b; out[int(.18 * SR):int(.18 * SR) + len(b)] += b * .7
    return out * g
def applause(d=4, g=.5):
    n = int(d * SR); x = np.zeros(n)
    for k in range(int(d * 260)):
        i = rng.integers(0, n - 800); x[i:i + 600] += hp(rng.standard_normal(600)) * np.exp(-np.arange(600) / 70) * rng.uniform(.2, 1)
    t = np.arange(n) / SR; return x * np.minimum(1, t / .4) * np.minimum(1, (d - t) / 1.0) * g * .25
def rain(d, g=.18):
    x = lp(noise(d), 1) * .3; n = len(x)
    for k in range(int(d * 90)):
        i = rng.integers(0, n - 400); x[i:i + 300] += hp(rng.standard_normal(300)) * np.exp(-np.arange(300) / 30) * rng.uniform(.3, 1)
    t = np.arange(n) / SR; return x * np.minimum(1, t / .5) * np.minimum(1, (d - t) / .5) * g
def drone(d, f=60, g=.25):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.01 * t) + .3 * lp(noise(d), 8)
    return s * np.minimum(1, t / 1) * np.minimum(1, (d - t) / 1) * g
def siren(d=3, g=.18):
    t = tt(d); f = 500 + 250 * np.sin(2 * np.pi * .4 * t); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / .5) * np.minimum(1, (d - t) / .5) * g
def horn(d=2.2, g=.3):
    t = tt(d); s = sum(np.sin(2 * np.pi * f * t) for f in (110, 165, 220)) / 3; return s * np.minimum(1, t / .2) * np.minimum(1, (d - t) / .4) * g
def chalk(d=1.2, g=.10):
    x = hp(noise(d)); t = tt(d); m = (np.sin(2 * np.pi * 9 * t) > 0) * 1.0; return x * lp(m, 6) * g
def rustle(d=.8, g=.2):
    t = tt(d); return lp(hp(noise(d)), 1) * np.sin(np.pi * t / d) * g
def step(g=.25):
    t = tt(.15); return lp(noise(.15), 3) * env(len(t), .001, .03) * g
def murmur(d, g=.12):
    n = int(d * SR); x = lp(noise(d), 10) * 3
    t = np.arange(n) / SR; return x * (0.6 + 0.4 * np.sin(t * 3)) * np.minimum(1, t / .6) * np.minimum(1, (d - t) / .6) * g

S = {x[0]: (starts[i], dur[i]) for i, x in enumerate(L)}
def at(key, off=0.0): return S[key][0] + off
def D(key): return S[key][1]

# 1 打字机 + 转场
for i, x in enumerate(L):
    st = starts[i]; sub = x[4]
    if x[0] not in CLIMAX and i > 0: add(whoosh(.5, .10), st - .35)
    k = 0
    for line in sub.split('|'):
        for ch, m in parse(line):
            add(tick(), st + k / 15.0, rng.uniform(-.3, .3), 1.0 if x[0] not in CLIMAX else 1.6); k += 1
    if x[3] is not None: add(ding(1180, .07), st + .3, -.5)
# 2 场景音效
add(applause(4.5, .35), at('open', .2)); add(gong(98, 5, .35), at('open', .1))
add(bell(330, 5, .25), at('open3', 1.0))
add(chime(660), at('title', .2)); add(boom(3, 45, .5), at('title', .6)); add(bell(220, 6, .3), at('title', .6))
add(ding(990, .08), at('born', .5))
for k in range(6): add(step(.15), at('tsinghua', .3 + k * .55), -.2)
add(drone(D('war'), 70, .2), at('war')); add(boom(2.5, 40, .7), at('war', 1.2), .2); add(boom(2, 50, .5), at('war', 2.6), -.3)
for k in range(10): add(step(.12), at('flee', .2 + k * .45), rng.uniform(-.4, .4))
add(rain(D('lianda') + .5, .22), at('lianda', -.2)); add(chalk(1.6), at('lianda', .2), -.4)
add(siren(D('alarm'), .14), at('alarm', 0)); add(drone(D('alarm'), 90, .12), at('alarm'))
add(drone(D('alarm2'), 55, .15), at('alarm2'))
add(horn(2.4, .32), at('ship', .5)); add(rain(D('ship'), .05), at('ship'))
add(chalk(1.4), at('chicago', .2), .3); add(murmur(D('chicago'), .06), at('chicago'))
add(bell(523, 4, .18), at('deng49', D('deng49') * .58)); add(boom(2, 60, .25), at('deng49', D('deng49') * .58))
add(horn(3.0, .25), at('deng50', .4))
add(chime(784), at('princeton', 1.0))
for k in range(3): add(chalk(1.0, .09), at('ym', k * .7), .3)
add(chime(1046), at('ym', D('ym') * .62))
add(chime(880), at('mirror', .2)); add(chime(1318), at('mirror', 1.2))
add(drone(D('ask'), 48, .2), at('ask')); add(impact(.4), at('ask', 1.2))
# 高潮蓄力：心跳越来越快
tst = at('test'); td = D('test')
t0 = tst + .3; gap = .9
while t0 < tst + td + .1:
    add(heartbeat(.6), t0); t0 += gap; gap = max(.32, gap * .82)
add(drone(td + D('crack'), 40, .25), tst)
add(riser(D('crack') + .2, .45), at('crack', -.1))
add(impact(.5), at('crack', 1.0)); add(impact(.4), at('crack', 1.35))
add(shatter(1.0), at('shatter', 0)); add(boom(3, 38, 1.0), at('shatter', 0)); add(impact(.8), at('shatter', 0))
add(impact(.9), at('shock', 0)); add(boom(2.5, 45, .6), at('shock', .05))
for k in range(4): add(impact(.35), at('shock', .2 + k * .2), (k - 1.5) / 2)
add(riser(.6, .3), at('prize', -.05)); add(boom(3.5, 42, 1.0), at('prize', .5)); add(gong(110, 5, .5), at('prize', .5)); add(applause(4, .5), at('prize', .7))
add(impact(.9), at('ages', 0)); add(impact(.9), at('ages', .9)); add(applause(3, .35), at('ages', .2))
add(applause(4.5, .6), at('king', 1.0)); add(bell(659, 4, .25), at('king', 1.0))
add(boom(4, 36, 1.1), at('first', 0)); add(gong(82, 6, .7), at('first', 0)); add(impact(1.0), at('first', 0)); add(applause(5, .6), at('first', .3))
# 归来
add(boom(4, 30, .9), at('bomb', .2)); add(drone(D('bomb'), 35, .3), at('bomb')); add(rustle(.6), at('bomb', 1.4))
add(drone(D('return'), 120, .08), at('return')); add(whoosh(2.5, .15), at('return', .2))
add(murmur(D('reunion'), .10), at('reunion'))
add(drone(D('airport'), 140, .06), at('airport')); add(ding(740, .07), at('airport', 1.3))
add(murmur(D('letter'), .08), at('letter')); for_k = None
for k in range(4): add(step(.18), at('letter', .1 + k * .3), .5)
add(rustle(.9, .25), at('letter', 1.3))
add(rustle(1.2, .22), at('letter2', .1)); add(bell(392, 6, .22), at('letter2', 1.5))
add(heartbeat(.4), at('tears', .4)); add(heartbeat(.35), at('tears', 1.6)); add(chime(523), at('tears', 2.2))
for k in range(5): add(step(.14), at('hospital', .2 + k * .35), .3)
add(gong(73, 7, .45), at('flowers', D('flowers') * .7))
add(murmur(D('home'), .03), at('home')); add(ding(880, .06), at('home', 1.5))
add(heartbeat(.5), at('citizen', 1.2)); add(chime(659), at('citizen', 1.4))
add(chime(587), at('hundred', .8)); add(chime(880), at('hundred', 2.5))
add(bell(196, 8, .45), at('gone', .3))
add(chime(523), at('end', .5)); add(bell(392, 6, .25), at('end', D('end') * .8))
add(shatter(.35), at('end2', 0)); add(chime(784), at('end2', 1.2)); add(gong(98, 7, .5), at('end2', 2.6))

m = np.max(np.abs(np.stack([Lc, Rc]))); Lc = np.tanh(2.2 * Lc / m) / np.tanh(2.2) * 0.9; Rc = np.tanh(2.2 * Rc / m) / np.tanh(2.2) * 0.9
fade = np.ones(N); fade[-SR:] = np.linspace(1, 0, SR); Lc *= fade; Rc *= fade
d = (np.stack([Lc, Rc], 1) * 32767).astype(np.int16)
w = wave.open('sfx.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close(); print('ok', TOTAL)

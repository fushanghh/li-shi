"""样片配乐+音效+配音混音（全部程序合成，配音用 edge-tts XiaoyiNeural +18%）"""
import numpy as np, wave, subprocess, os
VO_DIR = os.environ.get('VO_DIR', '../vo')
SR = 44100; DUR = 10.0; N = int(SR*DUR)
mix = np.zeros(N); vo_bus = np.zeros(N)
rng = np.random.default_rng(1)
def tt(d): return np.arange(int(SR*d))/SR
def env(n, a=.005, r=.1):
    e = np.ones(n); na = max(1, int(a*SR)); nr = min(n, int(r*SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr)**2; return e
def put(buf, x, t0, g=1.0):
    i = int(t0*SR); j = min(N, i+len(x))
    if j > i: buf[i:j] += g*x[:j-i]
def nf(m): return 440*2**((m-69)/12)
def pluck(f, d=.25, br=6):
    t = tt(d); x = sum((1/k)*np.sin(2*np.pi*f*k*t)*np.exp(-t*br*k*.7) for k in range(1, 6))
    return x*env(len(t), .002, .05)
def bass(f, d=.2):
    t = tt(d); x = np.sin(2*np.pi*f*t)+.3*np.sign(np.sin(2*np.pi*f*t)); return .5*x*np.exp(-t*7)*env(len(t), .003, .04)
def kick():
    t = tt(.18); f = 120*np.exp(-t*25)+45; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*18)
def snare():
    t = tt(.15); return (rng.normal(0, 1, len(t))*.6+np.sin(2*np.pi*190*t)*.5)*np.exp(-t*25)
def hat():
    t = tt(.05); return rng.normal(0, 1, len(t))*np.exp(-t*90)*.25
# ---------- 欢快 BGM 130BPM（C大调 oompah） ----------
BPM = 130; b = 60/BPM
CH = [(48, [60, 64, 67]), (53, [60, 65, 69]), (55, [59, 62, 67]), (48, [60, 64, 67])]
MEL = [72, 76, 79, 76, 77, 74, 72, 74, 76, 79, 81, 79, 77, 76, 74, 71]
def bgm_section(t0, t1, transpose=0, minor=False, rate=1.0):
    bb = b/rate; i = 0; t = t0
    while t < t1-1e-6:
        root, tri = CH[(i//8) % 4]
        if minor: tri = [n-1 if n % 12 in (4, 9) else n for n in tri]
        if i % 2 == 0:
            put(mix, bass(nf(root+transpose-12 if i % 4 == 0 else root+transpose-5)), t, .5); put(mix, kick(), t, .55 if i % 4 == 0 else .3)
        else:
            for n in tri: put(mix, pluck(nf(n+transpose), .18, 9), t, .09)
            put(mix, snare(), t, .22 if i % 4 == 3 else 0)
        put(mix, hat(), t+bb/4, .5)
        m = MEL[i % 16]+transpose
        if minor and m % 12 in (4, 9): m -= 1
        put(mix, pluck(nf(m), .22, 7), t, .16)
        i += 1; t += bb/2
bgm_section(0.0, 2.5)
bgm_section(2.5, 5.0, transpose=1, rate=1.12)     # 怒：升半音加速
# 哀：BGM 断掉 → 悲伤长号 wah-wah-wah-waaah
def trombone(f, d, vib=False):
    t = tt(d); fm = f*(1+(.03*np.sin(2*np.pi*6*t) if vib else 0))
    ph = 2*np.pi*np.cumsum(fm)/SR
    x = sum((1/k**.8)*np.sin(k*ph) for k in range(1, 9))
    wah = .5+.5*np.minimum(1, t/.08); return .25*x*wah*env(len(t), .02, .12)
for k, (m, d) in enumerate(((58, .32), (57, .32), (56, .32), (55, 1.0))):
    put(mix, trombone(nf(m), d, vib=(k == 3)), 5.9+k*.36, .9)
bgm_section(7.5, 10.0, transpose=0, rate=1.0)
# ---------- 音效 ----------
def ding():
    t = tt(.6); return (np.sin(2*np.pi*1568*t)+.5*np.sin(2*np.pi*2350*t))*np.exp(-t*7)*.5
def boing():
    t = tt(.4); f = 180+400*(1-np.exp(-t*12))+30*np.sin(2*np.pi*18*t); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*5)*.6
def whoosh(d=.35):
    x = rng.normal(0, 1, int(SR*d)); t = tt(d); k = np.sin(np.pi*t/d)**2
    y = np.convolve(x, np.ones(30)/30, 'same'); return y*k*1.6
def buzzer():
    t = tt(.5); return .35*np.sign(np.sin(2*np.pi*110*t))*env(len(t), .005, .05)
def beep():
    t = tt(.12); return .3*np.sin(2*np.pi*2000*t)*env(len(t), .002, .03)
def popsfx():
    t = tt(.08); f = 900-6000*t; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*40)*.5
def hiss(d=1.0):
    x = rng.normal(0, 1, int(SR*d)); x = x-np.convolve(x, np.ones(8)/8, 'same'); return x*env(len(x), .05, .3)*.25
def tada():
    y = np.zeros(int(SR*.8))
    for k, m in enumerate((72, 76, 79, 84)):
        p = pluck(nf(m), .6, 3); i = int(k*.06*SR); y[i:i+len(p)] += p[:len(y)-i]
    return y*.5
def scratch():
    t = tt(.25); f = 300+900*np.abs(np.sin(2*np.pi*4*t)); return (np.sin(2*np.pi*np.cumsum(f)/SR)*.4+rng.normal(0, .3, len(t)))*env(len(t), .005, .05)
def glitch():
    t = tt(.06); return np.sign(np.sin(2*np.pi*60*t))*.25*rng.uniform(.5, 1, len(t))
put(mix, ding(), .45); put(mix, boing(), .95); put(mix, whoosh(), 2.0, .9)
put(mix, scratch(), 2.48, .8); put(mix, beep(), 2.75); put(mix, buzzer(), 3.0); put(mix, hiss(1.2), 3.3)
put(mix, scratch(), 4.95, .8); put(mix, popsfx(), 5.5, 1.2)
for k in range(9): put(mix, popsfx(), 5.62+k*.07, .5)
put(mix, whoosh(.6), 7.45, .9); put(mix, tada(), 8.1)
LOOPS = [(1.20, 2.04, .28), (3.55, 4.75, .30), (6.20, 7.10, .30), (9.00, 9.88, .22)]
for a, bnd, wl in LOOPS:
    t = a
    while t < bnd-1e-6: put(mix, glitch(), t, .8); t += wl
# ---------- 配音 ----------
def load(i):
    w = wave.open(f'{VO_DIR}/{i}.wav'); x = np.frombuffer(w.readframes(w.getnframes()), np.int16)/32768; return x
v = {i: load(i) for i in range(1, 8)}
put(vo_bus, v[1], .15)
for t0 in (1.2, 1.48, 1.76): put(vo_bus, v[2], t0)          # 冲冲冲（鬼畜复读）
put(vo_bus, v[3], 2.55)
for t0 in (3.62, 3.92, 4.22): put(vo_bus, v[4], t0)          # 网…网…网
put(vo_bus, v[3][int(.45*SR):], 4.5)                          # 网卡了？！
put(vo_bus, v[5], 5.05)
put(vo_bus, v[6], 7.55)
for t0 in (9.0, 9.44): put(vo_bus, v[7], t0, .9)
# 侧链压低 BGM
envv = np.convolve(np.abs(vo_bus), np.ones(2000)/2000, 'same'); duck = 1-.55*np.clip(envv*12, 0, 1)
out = mix*duck*.55+vo_bus*1.25
out = np.tanh(out*1.1)*.92
out[-int(.15*SR):] *= np.linspace(1, 0, int(.15*SR))
w = wave.open('../mix.wav', 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
print('ok', np.abs(out).max())

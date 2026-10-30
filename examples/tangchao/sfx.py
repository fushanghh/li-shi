import json, numpy as np, soundfile as sf
SR = 48000
E = json.load(open('events.json')); N = int((E['total'] + 0.5) * SR)
out = np.zeros(N)
rng = np.random.default_rng(1)
def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def tone(f, dur, d, f2=None):
    n = int(dur * SR); t = np.arange(n) / SR
    ff = f if f2 is None else np.linspace(f, f2, n)
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * env(n, 0.003, d)
def noise(dur, d, lp=0.2):
    from scipy.signal import lfilter
    n = int(dur * SR); x = rng.standard_normal(n); y = lfilter([lp], [1, lp - 1], x)
    return y * env(n, 0.01, d) / (np.abs(y).max() + 1e-9)
def bp_noise(dur, a, d, lp):
    x = noise(dur, d, lp); return x
S = {
 'pop': tone(700, 0.15, 0.05, 1300) * 0.35,
 'ding': (tone(1568, 0.8, 0.35) + 0.5 * tone(2350, 0.8, 0.2)) * 0.22,
 'tick': (tone(2093, 0.25, 0.08) + 0.3 * tone(3136, 0.25, 0.05)) * 0.16,
 'thud': (tone(110, 0.6, 0.18, 55) * 0.8 + np.pad(noise(0.3, 0.05, 0.08), (0, int(0.3*SR))) * 0.4) * 0.8,
 'drum': (tone(80, 1.2, 0.4, 50) + np.pad(noise(0.6, 0.15, 0.05), (0, int(0.6*SR))) * 0.4) * 0.7,
 'whoosh': noise(0.5, 0.25, 0.06) * np.sin(np.linspace(0, np.pi, int(0.5 * SR))) * 0.35,
 'swish': noise(0.25, 0.12, 0.1) * np.sin(np.linspace(0, np.pi, int(0.25 * SR))) * 0.18,
 'paper': noise(0.35, 0.12, 0.6) * 0.18,
 'whack': (noise(0.2, 0.04, 0.5) * 0.6 + tone(220, 0.2, 0.05, 120) * 0.6) * 0.8,
 'boing': tone(300, 0.6, 0.3, 700) * 0.3 * (1 + 0.3 * np.sin(np.arange(int(0.6 * SR)) / SR * 2 * np.pi * 12)),
 'fire': noise(4.0, 3.0, 0.3) * 0.08,
}
for t, k in E['ev']:
    s = S[k]; i = int(t * SR); j = min(N, i + len(s)); out[i:j] += s[:j - i]
# 极轻室内底噪
out += noise(N / SR, 1e9, 0.02)[:N] * 0.01
out = np.clip(out / max(1, np.abs(out).max() / 0.9), -1, 1)
sf.write('sfx.wav', np.stack([out, out], 1), SR)
print('ok', N / SR)

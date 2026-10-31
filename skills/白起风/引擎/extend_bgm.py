# 按拍网格拼接加长 BGM。改 PIECES 为 [(起拍, 止拍或None), ...]，跳接点要落在 16 拍乐句头上。
import numpy as np, soundfile as sf
BP = 0.4285587; T0 = 0.2017227          # 用 beats.py 的输出替换
PIECES = [(0, 156), (96, 156), (156, None)]   # 白起样片：中段副歌多接一遍，88s→116s
TAIL = 2.2
y, sr = sf.read('bgm_src.wav')
T = lambda k: 0 if k == 0 else T0 + k * BP
segs = [y[int(round(T(a) * sr)):(int(round(T(b) * sr)) if b is not None else len(y))] for a, b in PIECES]
xf = int(0.012 * sr); r = np.linspace(0, 1, xf)[:, None]; out = segs[0]
for z in segs[1:]: out = np.concatenate([out[:-xf], out[-xf:] * (1 - r) + z[:xf] * r, z[xf:]])
out = np.concatenate([out, np.zeros((int(TAIL * sr), 2))]); sf.write('bgm_ext.wav', out, sr); print(len(out) / sr, 's')

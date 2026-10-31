# 用法: python3 beats.py 原视频或音频  → 打印 BPM、拍网格(T0,BP)、每拍能量(找乐段/静音拍)，并导出 bgm_src.wav
# 依赖: pip install librosa soundfile
import sys, subprocess, numpy as np, librosa
src = sys.argv[1]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-vn', '-ac', '2', '-ar', '44100', 'bgm_src.wav'], check=True)
y, sr = librosa.load('bgm_src.wav', sr=22050, mono=True)
_, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
k = np.arange(len(beats)); BP, T0 = np.polyfit(k, beats, 1)
print(f'BPM={60/BP:.2f}  BP={BP:.7f}  T0={T0:.7f}  拍数={len(beats)}  时长={len(y)/sr:.2f}s')
r = librosa.feature.rms(y=y, hop_length=256)[0]; tt = librosa.frames_to_time(np.arange(len(r)), sr=sr, hop_length=256)
e = np.array([r[(tt >= T0 + i * BP) & (tt < T0 + (i + 1) * BP)].mean() for i in range(len(beats))]); e /= e.max()
print('每拍能量(<0.5 = 安静/停顿拍，适合放静默镜头):')
print(' '.join(f'{i}:{v:.1f}' for i, v in enumerate(e)))

import sys, subprocess
from film import *
part, nparts = int(sys.argv[1]), int(sys.argv[2])
nf = int(TOTAL * FPS); a = nf * part // nparts; b = nf * (part + 1) // nparts
ff = subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
     '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',f'part{part}.mp4'], stdin=subprocess.PIPE)
for i in range(a, b):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(i / FPS, s); s.flush()
    ff.stdin.write(bytes(s.get_data()))
ff.stdin.close(); ff.wait(); print('done', part)

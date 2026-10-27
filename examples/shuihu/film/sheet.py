import sys
from film import *
from PIL import Image
step=float(sys.argv[1]) if len(sys.argv)>1 else 2
t0=float(sys.argv[2]) if len(sys.argv)>2 else 0
t1=float(sys.argv[3]) if len(sys.argv)>3 else TOTAL
ims=[]; tg=t0
while tg<t1:
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); render(tg,s)
    im=Image.frombuffer('RGBA',(W,H),bytes(s.get_data()),'raw','BGRA',0,1).convert('RGB').resize((270,360))
    ims.append((tg,im)); tg+=step*B
cols=8; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*270,rows*360))
from PIL import ImageDraw
for i,(tg,im) in enumerate(ims):
    ImageDraw.Draw(im).text((4,4),'%.1f b%.0f'%(tg,tg/B),fill='white'); sh.paste(im,((i%cols)*270,(i//cols)*360))
sh.save(sys.argv[4] if len(sys.argv)>4 else 'sheet.jpg',quality=80)
print(TOTAL,len(EVENTS))

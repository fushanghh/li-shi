import sys, time
from render import *
from PIL import Image, ImageDraw
step=float(sys.argv[1]); t0=float(sys.argv[2]); t1=float(sys.argv[3]); out=sys.argv[4]
t1=min(t1,TOTAL)
ims=[]; tg=t0; st=time.time()
while tg<t1:
    s=render(tg); im=Image.frombuffer('RGBA',(W,H),bytes(s.get_data()),'raw','BGRA',0,1).convert('RGB').resize((270,360))
    ImageDraw.Draw(im).text((4,4),'%.2f %s'%(tg,SHOTS[shot_at(tg)[0]].name),fill='white'); ims.append(im); tg+=step
print('per frame', (time.time()-st)/len(ims), 'TOTAL', TOTAL)
cols=8; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*270,rows*360))
for i,im in enumerate(ims): sh.paste(im,((i%cols)*270,(i//cols)*360))
sh.save(out,quality=82)

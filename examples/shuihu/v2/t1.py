from chars import *
import cairocffi as cairo
from PIL import Image
s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); gs=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H)
c=cairo.Context(s); gc=cairo.Context(gs)
for cc in (c,gc): cc.set_line_cap(1); cc.set_line_join(1)
p=P(c,gc); g=p.g
p.rect(0,STAGE_T,W,SH,'BG')
p.rect(0,880,W,STAGE_B-880,'BLK')
L=[('lin','heroic'),('lin','thrust'),('lin','guard'),('soldier','guard'),('lu','smash'),('gq','point'),('wife','pray'),('gyn','fan'),('thug','palm'),('cop','raiseO'),('hong','blockH'),('lin','sweepL')]
for i,(k,po) in enumerate(L):
    x=110+(i%6)*175; gy=500 if i<6 else 880
    o=figure(p,g,x,gy,0.62,1,po,k,t=0.3)
impact(p,g,700,300,0.1,0.0,0.6)
chrome(p,(0,'八十万禁军教头，','一杆红缨枪 镇京城',(),hl('一杆红缨枪 镇京城','镇京城')),t=5)
counter(p,g,'禁军','×80万',1,0)
a=composite(s,gs)
Image.frombuffer('RGBA',(W,H),a.tobytes(),'raw','BGRA',0,1).convert('RGB').save('t1.png')

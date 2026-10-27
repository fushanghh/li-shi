from lib import *
s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s); c.set_line_cap(1); c.set_line_join(1); p=P(c)
stage_bg(p); ground(p)
kinds=[('lin','stand'),('lin','thrust'),('gyn','fan'),('thug','punch'),('guard','guard'),('gq','point'),('lu','swing'),('cop','raise'),('wife','pray'),('hong','chop')]
for i,(k,po) in enumerate(kinds):
    x=100+(i%5)*210; gy=520 if i<5 else 880
    figure(p,x,gy,0.85,1,po,k)
frame_chrome(p,'八十万禁军教头，','一杆红缨枪 镇京城',(),hl('一杆红缨枪 镇京城','镇京城'),t=5,cap_t0=0)
counter(p,'禁军','×80万',1,0)
s.write_to_png('t1.png')

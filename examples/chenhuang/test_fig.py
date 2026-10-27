from fig import *
s=surf();c=cairo.Context(s);rect(c,0,0,W,H,'#3a2c1c')
items=[('qinsol','stand','calm','closed',None),('chen','hoe_up','angry','open','hoe'),('wu','sword','angry','closed','sword'),('qinoff','read','calm','closed','bamboo'),
('chu','shout','angry','open','flag'),('tangoff','hands','sad','frown',None),('tangsol','point','calm','closed','spear'),('huang','sword','proud','closed','gsword'),
('hsol','cheer','angry','open','spear'),('woman','cower','fear','open',None),('farmer','kneel','sad','frown',None),('salt','stand2','calm','closed',None),('huangrobe','sit','proud','closed',None),('emp','kowtow','sad','closed',None),('qinsol2',walk(.1,run=True),'fear','open',None),('qinoff','dead','calm','closed',None)]
for i,(o,p,e,m,w) in enumerate(items):
    x=110+(i%8)*230;y=480+(i//8)*480
    person(c,x,y,300,o,p,1,e,m,weapon=w)
horse(c,1700,1060,180,1,0.3,rider='huang')
s.write_to_png('tf.png')

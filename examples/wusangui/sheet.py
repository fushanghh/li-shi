import sys
from PIL import Image
P_='h_'
bs=sys.argv[2:];n=4
ims=[Image.open(f'{P_}{b}.png').convert('RGB').resize((480,270)) for b in bs]
s=Image.new('RGB',(480*n,270*((len(ims)+n-1)//n)),'white')
for i,im in enumerate(ims):s.paste(im,((i%n)*480,(i//n)*270))
s.save(sys.argv[1],quality=80)

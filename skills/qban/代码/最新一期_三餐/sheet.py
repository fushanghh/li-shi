import sys
from PIL import Image
fs=sys.argv[2:]; out=sys.argv[1]
im=Image.new('RGB',(1920,1080))
for i,f in enumerate(fs[:4]):
    a=Image.open(f).convert('RGB').resize((960,540)); im.paste(a,((i%2)*960,(i//2)*540))
im.save(out)

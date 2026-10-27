import sys
from PIL import Image
fs = sys.argv[2:]; out = sys.argv[1]
cols = 2; rows = (len(fs) + 1) // 2
S = Image.new('RGB', (960 * cols, 540 * rows))
for i, f in enumerate(fs):
    S.paste(Image.open(f).convert('RGB').resize((960, 540)), ((i % 2) * 960, (i // 2) * 540))
S.save(out)

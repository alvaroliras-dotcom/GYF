# Hoja de revisión: todas las piezas sobre crema y sobre berenjena
from PIL import Image, ImageDraw
import os, sys
ns = sorted(f[:-4] for f in os.listdir('master') if f.endswith('.png'))
W = 300; cols = 5; rows = (len(ns) + cols - 1) // cols
c = Image.new('RGB', (W * cols, W * rows * 2), (245, 241, 236))
d = ImageDraw.Draw(c)
for i, n in enumerate(ns):
    im = Image.open('master/' + n + '.png').resize((W, W), Image.LANCZOS)
    x, y = (i % cols) * W, (i // cols) * W * 2
    c.paste(im, (x, y), im)
    bg = Image.new('RGB', (W, W), (28, 18, 25)); bg.paste(im, (0, 0), im); c.paste(bg, (x, y + W))
    d.text((x + 6, y + 4), n, fill=(90, 80, 85))
c.save(sys.argv[1] if len(sys.argv) > 1 else 'hoja.jpg', quality=85)

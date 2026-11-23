import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

SRC = '/home/user/RCR-Rive-Sud/assets/media/epipen-enfant.webp'
OUT = 'epipen-enfant-en.png'
FD = 'fonts/'  # Nunito, Nunito Sans, Baloo 2 from Google Fonts (OFL)

img = np.array(Image.open(SRC).convert('RGB'))
H, W = img.shape[:2]


def font(name, size, wght=None):
    f = ImageFont.truetype(FD + name, size)
    if wght:
        f.set_variation_by_axes([wght])
    return f


def lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def box_mask(box, pred):
    x0, y0, x1, y1 = box
    m = np.zeros((H, W), np.uint8)
    m[y0:y1, x0:x1] = pred(img[y0:y1, x0:x1].astype(int)).astype(np.uint8) * 255
    return m


navy_px = lambda a: (lum(a) < 150) & (a[..., 0] < 130)
masks = [
    box_mask((440, 50, 815, 192), navy_px),                  # headline in yellow pill
    box_mask((980, 85, 1205, 175), navy_px),                 # step 1
    box_mask((980, 280, 1232, 445), navy_px),                # step 2
    box_mask((980, 505, 1200, 665), navy_px),                # step 3
    box_mask((980, 725, 1255, 855), navy_px),                # step 4
    box_mask((655, 668, 815, 775), navy_px),                 # yellow tag
    box_mask((95, 790, 600, 915), lambda a: (lum(a) > 170) & (a[..., 2] > 150)),  # "Tu peux le faire !"
]
mask = np.maximum.reduce(masks)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
clean = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)

reg = img[90:170, 990:1150].reshape(-1, 3)
NAVY = tuple(int(v) for v in np.median(reg[lum(reg) < 80], axis=0))
print('navy', NAVY)

im = Image.fromarray(clean).convert('RGBA')
d = ImageDraw.Draw(im)


def lines(x, y, txt, f, fill, lh, anchor='la'):
    for i, t in enumerate(txt):
        d.text((x, y + i * lh), t, font=f, fill=fill, anchor=anchor)


def rotated_text(center, txt_lines, f, fill, lh, angle, stroke=0):
    w = int(max(d.textlength(t, font=f) for t in txt_lines)) + 40
    h = lh * len(txt_lines) + 40
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i, t in enumerate(txt_lines):
        ld.text((w / 2, 20 + i * lh), t, font=f, fill=fill, anchor='ma')
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(layer, (int(center[0] - layer.width / 2), int(center[1] - layer.height / 2)))


step = font('Nunito.ttf', 35, 800)
lines(990, 88, ['Pull off', 'the cap.'], step, NAVY, 41)
lines(990, 284, ['Hold the', 'EpiPen tight', 'on the side', 'of your thigh.'], step, NAVY, 40)
lines(990, 512, ['Press hard', 'and hold for', '10 seconds.'], step, NAVY, 42)
lines(990, 733, ['Call 911', 'and ask for', 'medical help.'], step, NAVY, 41)

tag = font('Nunito.ttf', 27, 750)
lines(734, 674, ['On the side', 'of the thigh,', 'mid-thigh'], tag, NAVY, 32, anchor='ma')

head = font('Baloo2.ttf', 58, 800)
rotated_text((622, 112), ['An EpiPen', 'is easy!'], head, NAVY, 54, 6)

cheer = font('Baloo2.ttf', 66, 800)
rotated_text((345, 852), ['You can do it!'], cheer, (255, 255, 255), 66, 7)

im = im.convert('RGB')
im.save(OUT)
im.save(OUT.replace('.png', '.webp'), 'WEBP', quality=88, method=6)

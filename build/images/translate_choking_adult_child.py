import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

SRC = '/home/user/RCR-Rive-Sud/assets/media/desobstruction-adulte-enfant.webp'
OUT = 'desobstruction-adulte-enfant-en.png'
FD = 'fonts/'  # Nunito, Nunito Sans, Baloo 2 from Google Fonts (OFL)

img = np.array(Image.open(SRC).convert('RGB'))
H, W = img.shape[:2]


def font(size, wght, wdth=88):
    f = ImageFont.truetype(FD + 'NunitoSans.ttf', size)
    f.set_variation_by_axes([wght, wdth, 12, 520])
    return f


def lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def box_mask(box, pred):
    x0, y0, x1, y1 = box
    m = np.zeros((H, W), np.uint8)
    m[y0:y1, x0:x1] = pred(img[y0:y1, x0:x1].astype(int)).astype(np.uint8) * 255
    return m


def med(box, pred):
    x0, y0, x1, y1 = box
    r = img[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    return tuple(int(v) for v in np.median(r[pred(r)], axis=0))


white = lambda a: lum(a) > 200
dark = lambda a: lum(a) < 150

BLUE_T = med((50, 170, 670, 200), lambda a: lum(a) < 90)
GREEN_T = med((765, 170, 1390, 200), lambda a: lum(a) < 110)
BLUE_N = med((112, 240, 360, 270), lambda a: lum(a) < 90)
GREEN_N = med((830, 240, 1055, 270), lambda a: lum(a) < 110)
print(BLUE_T, GREEN_T, BLUE_N, GREEN_N)

masks = [
    box_mask((180, 20, 580, 140), white), box_mask((905, 20, 1275, 140), white),
    box_mask((40, 162, 685, 207), dark), box_mask((755, 162, 1400, 207), dark),
    box_mask((105, 232, 365, 310), dark), box_mask((498, 225, 698, 297), dark), box_mask((430, 297, 698, 332), dark),
    box_mask((820, 232, 1060, 310), dark), box_mask((1183, 225, 1408, 297), dark), box_mask((1133, 297, 1408, 332), dark),
]
mask = np.maximum.reduce(masks)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
clean = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)
im = Image.fromarray(clean)
d = ImageDraw.Draw(im)

WHITE = (255, 255, 255)
big = font(64, 850, 90)
sub = font(37, 600, 88)
d.text((378, 26), 'Adult', font=big, fill=WHITE, anchor='ma')
d.text((378, 92), '(and child past puberty)', font=sub, fill=WHITE, anchor='ma')
d.text((1090, 26), 'Child', font=big, fill=WHITE, anchor='ma')
d.text((1090, 92), '(1 year to puberty)', font=sub, fill=WHITE, anchor='ma')

line = font(30, 750, 86)
d.text((362, 168), 'Conscious person with severe obstruction', font=line, fill=BLUE_T, anchor='ma')
d.text((1079, 168), 'Conscious person with severe obstruction', font=line, fill=GREEN_T, anchor='ma')

b = font(31, 800, 86)
r = font(21.5, 520, 84)
for x, col in [(114, BLUE_N), (831, GREEN_N)]:
    d.text((x, 238), '5 back blows', font=b, fill=col)
    d.text((x, 276), '(between shoulder blades)', font=r, fill=col)
for cx, col in [(585, BLUE_N), (1290, GREEN_N)]:
    d.text((cx, 230), '5 abdominal', font=b, fill=col, anchor='ma')
    d.text((cx, 263), 'thrusts', font=b, fill=col, anchor='ma')
    d.text((cx, 301), '(Heimlich manoeuvre)', font=r, fill=col, anchor='ma')

im.save(OUT)
im.save(OUT.replace('.png', '.webp'), 'WEBP', quality=88, method=6)

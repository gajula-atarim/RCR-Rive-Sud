import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

SRC = '/home/user/RCR-Rive-Sud/assets/media/epipen-cuisse-adulte.webp'
OUT = 'epipen-cuisse-adulte-en.png'
FD = 'fonts/'  # Nunito Sans variable fonts from Google Fonts (OFL)

img = np.array(Image.open(SRC).convert('RGB'))
H, W = img.shape[:2]


def font(name, size, wght, wdth=100, ytlc=520):
    f = ImageFont.truetype(FD + name, size)
    f.set_variation_by_axes([wght, wdth, 12, ytlc])
    return f


def text_mask(box, pred):
    """Mask of text pixels inside box (x0,y0,x1,y1) selected by pred(rgb array)->bool."""
    x0, y0, x1, y1 = box
    m = np.zeros((H, W), np.uint8)
    reg = img[y0:y1, x0:x1].astype(int)
    m[y0:y1, x0:x1] = pred(reg).astype(np.uint8) * 255
    return m


def lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


masks = []
# step cards: dark navy text on white
for box in [(1048, 108, 1232, 198), (1048, 285, 1268, 395), (1048, 458, 1282, 548), (1048, 628, 1268, 722)]:
    masks.append(text_mask(box, lambda a: lum(a) < 170))
# bubble: white text on navy
masks.append(text_mask((696, 248, 916, 382), lambda a: lum(a) > 110))
# yellow box: navy italic text on yellow
masks.append(text_mask((1012, 805, 1405, 892), lambda a: lum(a) < 150))
# title: white + yellow text on navy
masks.append(text_mask((34, 700, 660, 888), lambda a: (lum(a) > 120)))

mask = np.maximum.reduce(masks)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
clean = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)

im = Image.fromarray(clean)
d = ImageDraw.Draw(im)
NAVY = (16, 33, 66)
# sample navy text colour from step 1 original
reg = img[115:190, 1055:1225].reshape(-1, 3)
dark = reg[lum(reg) < 90]
if len(dark):
    NAVY = tuple(int(v) for v in np.median(dark, axis=0))
reg = img[780:880, 40:640].reshape(-1, 3)
yel = reg[(reg[:, 0] > 180) & (reg[:, 1] > 150) & (reg[:, 2] < 120)]
YELLOW = tuple(int(v) for v in np.median(yel, axis=0)) if len(yel) else (245, 200, 40)
print('navy', NAVY, 'yellow', YELLOW)

step = font('NunitoSans.ttf', 27, 680, 84)


def lines(x, y, txt, f, fill, lh, anchor='la'):
    for i, t in enumerate(txt):
        d.text((x, y + i * lh), t, font=f, fill=fill, anchor=anchor)


lines(1057, 108, ['Remove', 'the safety cap.'], step, NAVY, 29)
lines(1057, 284, ['Place the tip', 'against the outer', 'side of the thigh,', 'mid-thigh.'], step, NAVY, 26.5)
lines(1057, 458, ['Press firmly', 'and hold for', '10 seconds.'], step, NAVY, 28)
lines(1057, 628, ['Call 911', 'and ask for', 'medical help.'], step, NAVY, 29)

bub = font('NunitoSans.ttf', 31, 780, 84)
lines(806, 264, ['Outer side', 'of the thigh,', 'mid-thigh'], bub, (255, 255, 255), 37, anchor='ma')

yf = font('NunitoSans-Italic.ttf', 35, 760, 84)
lines(1207, 806, ['Learning the right steps', 'can save a life!'], yf, NAVY, 38, anchor='ma')

t1 = font('NunitoSans.ttf', 55, 780, 86)
t2 = font('NunitoSans.ttf', 55, 860, 86)
reg = font('NunitoSans.ttf', 24, 500, 90)
d.text((42, 706), 'EpiPen', font=t1, fill=(255, 255, 255))
w = d.textlength('EpiPen', font=t1)
d.text((42 + w + 1, 709), '\u00ae', font=reg, fill=(255, 255, 255))
w2 = d.textlength('\u00ae', font=reg)
d.text((42 + w + w2 + 13, 706), 'injection', font=t1, fill=(255, 255, 255))
lines(42, 772, ['into the side of the thigh,', 'mid-thigh'], t2, YELLOW, 54)

im.save(OUT)
im.save(OUT.replace('.png', '.webp'), 'WEBP', quality=88, method=6)

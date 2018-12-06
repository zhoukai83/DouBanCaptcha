from PIL import Image

from PIL import ImageFilter
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

WHITE_EXPAND = (255, 255, 255, 255)
BLACK_EXPAND = (0, 0, 0, 255)


def pre(img, threshold=10):
    width, height = img.size

    pixdata = img.load()

    for i in range(0, width):
        for j in range(0, height):
            p = pixdata[i, j]
            r, g, b = p
            if r > threshold or g > threshold or b > threshold:
                pixdata[i, j] = BLACK
            else:
                pixdata[i, j] = WHITE

    # img = img.filter(ImageFilter.MedianFilter())
    return img
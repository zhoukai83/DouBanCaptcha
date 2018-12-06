from PIL import Image, ImageFilter
import ocr


BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

WHITE_EXPAND = (255, 255, 255, 255)
BLACK_EXPAND = (0, 0, 0, 255)


# 二值化算法
def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


# 去除干扰线算法
def depoint(img):  # input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            if pixdata[x, y - 1] > 245:
                count = count + 1
            if pixdata[x, y + 1] > 245:
                count = count + 1
            if pixdata[x - 1, y] > 245:
                count = count + 1
            if pixdata[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x, y] = 255
    return img


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

    return img


def remove_noise(img, window=1):
    """ 中值滤波移除噪点
    """
    pixdata = img.load()

    if window == 1:
        # 十字窗口
        window_x = [1, 0, 0, -1, 0]
        window_y = [0, 1, 0, 0, -1]
    elif window == 2:
        # 3*3矩形窗口
        window_x = [-1, 0, 1, -1, 0, 1, 1, -1, 0]
        window_y = [-1, -1, -1, 1, 1, 1, 0, 0, 0]

    width, height = img.size
    for i in range(width):
        for j in range(height):
            box = []
            black_count, white_count = 0, 0
            for k in range(len(window_x)):
                d_x = i + window_x[k]
                d_y = j + window_y[k]
                try:
                    d_point = pixdata[d_x, d_y]
                    if d_point == BLACK:
                        box.append(1)
                    else:
                        box.append(0)
                except IndexError:
                    pixdata[i, j] = WHITE
                    continue

            box.sort()
            if len(box) == len(window_x):
                mid = box[int(len(box) / 2)]
                if mid == 1:
                    pixdata[i, j] = BLACK_EXPAND
                else:
                    pixdata[i, j] = WHITE_EXPAND
    return img


# 判断像素点是黑点还是白点
def getflag(img, x, y):
    tmp_pixel = img.getpixel((x, y))
    if tmp_pixel > 228:  # 白点
        tmp_pixel = 0
    else:  # 黑点
        tmp_pixel = 1
    return tmp_pixel


# 黑点个数
def sum_9_region(img, x, y):
    width = img.width
    height = img.height
    flag = getflag(img, x, y)
    # 如果当前点为白色区域,则不统计邻域值
    if flag == 0:
        return 0
    # 如果是黑点
    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            total = getflag(img, x, y + 1) + getflag(img, x + 1, y) + getflag(img, x + 1, y + 1)
            return total
        elif x == width - 1:  # 右上顶点
            total = getflag(img, x, y + 1) + getflag(img, x - 1, y) + getflag(img, x - 1, y + 1)
            return total
        else:  # 最上非顶点,6邻域
            total = getflag(img, x - 1, y) + getflag(img, x - 1, y + 1) + getflag(img, x, y + 1) \
                    + getflag(img, x + 1, y) \
                    + getflag(img, x + 1, y + 1)
            return total
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            total = getflag(img, x + 1, y) + getflag(img, x + 1, y - 1) + getflag(img, x, y - 1)
            return total
        elif x == width - 1:  # 右下顶点
            total = getflag(img, x, y - 1) + getflag(img, x - 1, y) + getflag(img, x - 1, y - 1)
            return total
        else:  # 最下非顶点,6邻域
            total = getflag(img, x - 1, y) + getflag(img, x + 1, y) + getflag(img, x, y - 1) + getflag(img, x - 1,
                                                                                                       y - 1) + getflag(
                img, x + 1, y - 1)
            return total
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            total = getflag(img, x, y - 1) + getflag(img, x, y + 1) + getflag(img, x + 1, y - 1) + getflag(img, x + 1,
                                                                                                           y) + getflag(
                img, x + 1, y + 1)
            return total
        elif x == width - 1:  # 右边非顶点
            total = getflag(img, x, y - 1) + getflag(img, x, y + 1) + getflag(img, x - 1, y - 1) + getflag(img, x - 1,
                                                                                                           y) + getflag(
                img, x - 1, y + 1)
            return total
        else:  # 具备9领域条件的
            total = getflag(img, x - 1, y - 1) + getflag(img, x - 1, y) + getflag(img, x - 1, y + 1) + getflag(img, x,
                                                                                                               y - 1) \
                    + getflag(img, x, y + 1) + getflag(img, x + 1, y - 1) + getflag(img, x + 1, y) + getflag(img, x + 1,
                                                                                                             y + 1)
            return total

def greyimg(image):
	width = image.width
	height = image.height
	box = (0, 0, width, height)
	imgnew = image.crop(box)
	for i in range(0, height):
		for j in range(0, width):
			num = sum_9_region(image, j, i)
			if num < 2:
				imgnew.putpixel((j, i), 255)  # 设置为白色
			else:
				imgnew.putpixel((j, i), 0)  # 设置为黑色
	return imgnew

def get_bin_table():
	threshold = 80
	table = []
	for ii in range(256):
		if ii < threshold:
			table.append(0)
		else:
			table.append(1)
	return table

def toGrey(im):
	imgry = im.convert('L')  # 转化为灰度图
	table = get_bin_table()
	out = imgry.point(table, '1')
	return out

if __name__ == '__main__':
    import configparser
    import time

    is_show_image = True

    config = configparser.ConfigParser()
    config.read('config/configure.conf', encoding='utf-8')

    t = time.clock()
    for x in range(1, 2):
        # image = Image.open(f"./captcha/captcha_000{x}.jpg")
        image = Image.open(f"./captcha_output/captcha_sub_0013.jpg")
        # image.show()

        image = pre(image, 30)
        if is_show_image:
            image.show()

        # image = toGrey(image)
        # image.show()
        image = image.convert('L')  # 转化为灰度图
        image = greyimg(image)
        if is_show_image:
            image.show()

        # image = fall(image)
        # image.show()

        # image = remove_noise(image)
        # image.show()

        # image = depoint(image)
        # image.show()

        image = image.filter(ImageFilter.MedianFilter())
        if is_show_image:
            image.show()

        text = ocr.ocr_img_text(image, config)
        print(x, text)
        # print("baidu", ocr.ocr_img_baidu(Image.open(f"./captcha/captcha_000{x}.jpg")))

    print('用时: {0}'.format(time.clock() - t))

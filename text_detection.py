import cv2 as cv


def __filter_box(cnt):
    x, y, w, h = cv.boundingRect(cnt)
    # rect = cv.minAreaRect(cnt)
    # if debug:
    #     print(x, y, w, h, cv.contourArea(cnt), rect)
    if 100 < cv.contourArea(cnt) < 700:  # and 15 < h < 40 and 10 < w < 40:
        return x, y, x + w, y + h

    return None


def detect(image_path, debug=False):
    img = cv.imread(image_path)
    if debug:
        cv.namedWindow("Image")
        cv.imshow("Image", img)

    img2 = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    ret, thresh1 = cv.threshold(img2, 50, 255, cv.THRESH_BINARY)

    white = cv.countNonZero(thresh1)
    black = thresh1.shape[0] * thresh1.shape[1] - white
    # print(white, black)

    if white < black:
        binarize_img = thresh1
    else:
        binarize_img = cv.bitwise_not(thresh1)

    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
    dilated = cv.dilate(binarize_img, kernel, iterations=1)

    _, contours, hierarchy = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    candidate_boxes = [__filter_box(cnt) for cnt in contours]
    candidate_boxes = list(filter(lambda box: box, candidate_boxes))

    x_min = 250
    y_min = 40
    x_max = 0
    y_max = 0
    for box in candidate_boxes:
        if box[0] < x_min:
            x_min = box[0]

        if box[1] < y_min:
            y_min = box[1]

        if box[2] > x_max:
            x_max = box[2]

        if box[3] > y_max:
            y_max = box[3]

        if debug:
            print(box, x_min, y_min, x_max, y_max)
            # cv.imshow(str(index), binarize_img[y:box[3], x:box[2]])

    # result = cv.rectangle(dilated, (x_min, y_min), (x_max, y_max), (255, 0, 0), 1)
    # if x_max - x_min > 70:
    corp = img[y_min: y_max, x_min: x_max]
    # else:
    #     corp = img

    if debug:
        cv.imshow("thresh1", thresh1)
        cv.imshow("binarize", binarize_img)
        cv.imshow("dilated", dilated)
        cv.imshow("final", corp)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return corp






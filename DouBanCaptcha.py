import text_detection
import ocr
from PIL import Image
import image_process
import cv2 as cv


def __ocr_img_text(image, english_words):
    text = ocr.ocr_img_text(image)
    if len(text) >= 4:
        is_words = text in english_words
    else:
        is_words = False

    return is_words, text


def __get_image_text(index, english_words):
    try:
        result = text_detection.detect(f"captcha\\captcha_{str(index).zfill(4)}.jpg", debug=False)
        cv.imwrite(f"captcha_output\\captcha_sub_{str(index).zfill(4)}.jpg", result)
        image = Image.fromarray(result)
        is_words, text = __ocr_img_text(image, english_words)

        if not is_words:
            image = image_process.pre(image, 37)
            image.save(f"captcha_pre\\captcha_sub_{str(index).zfill(4)}.jpg")
            is_words, text = __ocr_img_text(image, english_words)

        return_obj = {"index": index, "text": text, "is_words": is_words}
        print(return_obj)
        return return_obj
    except Exception as ex:
        print(index, ex)
    return {"index": index, "text": "unknow", "is_words": False}


def main():
    with open("words_alpha.txt") as word_file:
        english_words = set(word.strip().lower() for word in word_file)

    results = [__get_image_text(index, english_words) for index in range(1, 31)]
    print(len([result for result in results if result["is_words"]]))


if __name__ == "__main__":
    main()

import pytesseract
# from aip import AipOcr
import io
from PIL import Image
import configparser
# from aip import AipOcr
import io

def ocr_img_text(image):
    config = configparser.ConfigParser()
    config.read('config/configure.conf', encoding='utf-8')
    pytesseract.pytesseract.tesseract_cmd = config.get("tesseract", "tesseract_cmd")
    tessdata_dir_config = config.get("tesseract", "tessdata_dir_config")
    region_text = pytesseract.image_to_string(image, lang='eng', config=tessdata_dir_config)
    return region_text


def ocr_img_baidu(image):
    config = configparser.ConfigParser()
    config.read('config/configure.conf', encoding='utf-8')
    # 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
    """ 你的 APPID AK SK """
    APP_ID = config.get('baidu_api', 'APP_ID')
    API_KEY = config.get('baidu_api', 'API_KEY')
    SECRET_KEY = config.get('baidu_api', 'SECRET_KEY')

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    image_data = img_byte_arr.getvalue()
    # base64_data = base64.b64encode(image_data)
    response = client.basicGeneral(image_data)
    print(response)
    words_result = response['words_result']

    texts = [x['words'] for x in words_result]
    print(texts)
    return texts
import re
import requests
import pytesseract
from fake_useragent import UserAgent
from PIL import Image


def get_captcha(login_url):
    login_html = s.get(login_url, headers=headers).content
    # print(login_html)

    # try:
    # captcha_img_url = re.findall(
    #     r'<img style="CURSOR: pointer" onclick="exchangePic(this)" height="23" title="点击刷新" src="(.*?)" width="58" align="absMiddle" border="0">', login_html)[0]
    # print(captcha_img_url)

    image = Image.open('Image.png')
    captcha_code = pytesseract.image_to_string(image)

    Image._show(image)

    print(captcha_code)


if __name__ == '__main__':
    s = requests.session()
    ua = UserAgent()

    headers = {'User-Agent': ua.random}

    login_url = "https://fin-tester.com/tcm/login.action?opID=toLogin"

    get_captcha(login_url)

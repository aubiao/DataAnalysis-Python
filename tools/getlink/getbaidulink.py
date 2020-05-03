import re
import requests
import pandas as pd
from fake_useragent import UserAgent


def getlink():
    url = 'https://www.baidu.com/'
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    resp = requests.get(url, headers)
    data = resp.text
    urls = re.findall(r'href="(http.*?)"', data)

    df = pd.DataFrame()

    df['url'] = urls[:1000]
    df.to_csv('TestUrls.csv', index=None)

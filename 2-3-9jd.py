import re
import json
import requests
from fake_useragent import UserAgent


def printjson(data):
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    print(json_str)


def getdata(json_url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    data = requests.get(json_url, headers=headers)
    print(data.text)

    # re_data = re.findall('pcMianShaAreaList\(({.*})\)', data.text)[0]
    # json_data = json.loads(re_data)

    # miaoshaList = json_data['miaoShaList']
    # print(miaoshaList)
    # print(len(miaoshaList))
    # printjson(miaoshaList)


if __name__ == '__main__':
    json_url = 'https://api.m.jd.com/api?appid=o2_channels&functionId=pcSeckillListHistory&client=pc&clientVersion=1.0.0&callback=pcSeckillListHistory&jsonp=pcSeckillListHistory&_=1588321655579'

    getdata(json_url)

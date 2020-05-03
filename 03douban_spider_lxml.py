# 豆瓣已开启反爬，问题待解决（目前只能通过模拟网页登录）
import requests
import chardet
import re
import pandas as pd
import time
import pickle
import json
import urllib.robotparser
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# 获取headers
def get_headers():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return headers


# 检查是否允许爬取数据
def robot_check(robotstxt_url, headers, url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robotstxt_url)
    rp.read()
    result = rp.can_fetch(headers['User-Agent'], url)

    return result


# 获取代理IP
def get_proxies():
    proxies = {
        'http': '125.88.74.122:84',
        'http': '123.84.13.240:8118',
        'https': '94.240.33.242:3128',
    }

    return proxies


def get_cookie_from_net(login_url):
    payload = {
        "ck": "",
        "name": username,
        "password": password,
        "remember": "true",
        "ticket": ""
    }

    data = s.post(login_url, headers=headers, data=payload).json()
    if data['status'] == "success":
        print("登录成功！")
    else:
        print("登录失败！", data)

    html = s.get('https://www.douban.com/people/144783640/')

    if html.status_code == 200:
        print("提交表单登录，成功获取cookies...")
    else:
        print("登录失败，status_code = ", html.status_code)
    # with open('login.txt', 'w') as f:
    #     f.write(str(html))
    # with open('cookies' + username + '.douban', 'wb') as f:
    #     cookie_dict = requests.utils.dict_from_cookiejar(s.cookies)
    #     pickle.dump(cookie_dict, f)

    return s.cookies


# 从cookie文件获取cookie
def get_cookie_from_file():
    # cookies = None
    # if os.path.exists('cookies' + username + '.douban'):
    with open('cookies' + username + '.douban', 'rb') as f:
        cookie_dict = pickle.load(f)
        cookies = requests.utils.cookiejar_from_dict(cookie_dict)
    print("解析文件，成功提取cookies...")

    return cookies


# 请求数据
def get_data(url, num_retries=3):
    try:
        data = requests.get(url, headers=headers)

        # 编码
        charset = chardet.detect(data.content)
        data.encoding = charset['encoding']
    except requests.exceptions.ConnectionError as e:
        print('请求错误，URL', url)
        print('错误详情：', e)
        data = None
    except:
        print('未知错误，url:', url)
        data = None

    if (data is not None) and (500 <= data.status_code < 600):
        if num_retries > 0:
            print("服务器错误，正在重试...")
            time.sleep(1)
            num_retries -= 1
            get_data(url, num_retries)

    return data


# 解析数据
def parse_data(data):
    if data is None:
        return None
    soup = BeautifulSoup(data.text, 'lxml')

    # 处理数据
    books_left = soup.find('ul', {'class': 'cover-col-4 clearfix'})
    books_left = books_left.find_all('li')

    books_right = soup.find('ul', {'class': 'cover-col-4 pl20 clearfix'})
    books_right = books_right.find_all('li')

    books = list(books_left) + list(books_right)

    img_urls = []
    titles = []
    ratings = []
    authors = []
    details = []
    for book in books:
        # 图书封面url
        img_url = book.find_all('a')[0].find('img').get('src')
        img_urls.append(img_url)

        # 图书标题
        title = book.find_all('a')[1].get_text()
        titles.append(title)

        # 评价分数
        rating = book.find('p', {'class': 'rating'}).get_text()
        rating = rating.replace('\n', '').replace(' ', '')
        ratings.append(rating)

        # 作者及出版信息
        author = book.find('p', {'class': 'color-gray'}).get_text()
        author = author.replace('\n', '').replace(' ', '')
        authors.append(author)

        # 图书简介
        detail = book.find_all('p')[2].get_text()
        detail = detail.replace('\n', '').replace(' ', '')
        details.append(detail)

    # print('img_urls', img_urls)
    # print('titles', titles)
    # print('ratings', ratings)
    # print('authors', authors)
    # print('details', details)
    return img_urls, titles, ratings, authors, details


# 解析用户信息数据
def parse_user_data(html):
    soup = BeautifulSoup(html.text, 'lxml')
    info = soup.find('div', {'class': 'info'})
    data = info.find_all('h1')[0].get_text()

    return data


# 存储数据
def sava_data(img_urls, titles, ratings, authors, details):
    result = pd.DataFrame()
    result['img_urls'] = img_urls
    result['titles'] = titles
    result['ratings'] = ratings
    result['authors'] = authors
    result['details'] = details
    result.to_csv('result.csv', index=None)


# 开始爬取
def run():
    print('爬取数据开始...')
    url = 'https://book.douban.com/latest'
    robotstxt_url = 'https://book.douban.com/robots.txt'

    if robot_check(robotstxt_url, headers, url):
        data = get_data(url)

        img_urls, titles, ratings, authors, details = parse_data(data)
        sava_data(img_urls, titles, ratings, authors, details)
    else:
        print(url, ":不允许爬取数据...")
    print('爬取数据结束...')


def login_and_get_data():
    print("获取cookies...")
    try:
        s.cookies = get_cookie_from_file()
    # if s.cookies is None:
    except:
        print("从文件获取cookies失败...\n正在尝试提交表单登录以获取...")
        s.cookies = get_cookie_from_net(
            "https://accounts.douban.com/j/mobile/login/basic")


# html = s.get('https://www.douban.com/people/144783640/', headers=headers)
# with open('html.txt', 'w') as f:
#     f.write(html.text)
# print(html.text)
# data = parse_user_data(html)
# print(data)


if __name__ == '__main__':
    s = requests.session()
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    username = "15989546438"
    password = "a15914710451"

    # run()
    login_and_get_data()

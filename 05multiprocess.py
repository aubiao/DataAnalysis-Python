import time
import requests
import concurrent
from concurrent import futures
import pandas as pd
import threading
from multiprocessing import Pool
from tools import getlink


# 装饰器
def gettime(func):
    def warapper(*args, **kwargs):
        print("="*50)
        print(func.__name__, 'Start...')
        starttime = time.time()
        func(*args)
        endtime = time.time()
        spendtime = endtime - starttime
        print(func.__name__, "End...")
        print("Spend", spendtime, "s totally")
        print("="*50)
    return warapper


# 取网址
def get_urls_from_file(n):
    df = pd.read_csv('TestUrls.csv')
    urls = list(df['url'][:n])

    return urls


# 请求网页获取数据
def getdata(url, retries=3):
    headers = {}
    try:
        html = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError as e:
        html = None

    if (html != None and 500 <= html.status_code < 600 and retries):
        retries -= 1
        getdata(url, retries)
        data = html.text
    else:
        data = None

    return data


# 串行
@gettime
def Mynormal():
    for url in urls:
        getdata(url)


# 进程池
@gettime
def MyprocessPool(num=10):
    pool = Pool(num)
    results = pool.map(getdata, urls)
    pool.close()
    pool.join()
    return results


# 多线程
@gettime
def Mymultithread(max_threads=10):
    def urls_process():
        while True:
            try:
                url = urls.pop()
            except IndexError:
                break
            data = getdata(url, retries=3)
    threads = []

    while int(len(threads) < max_threads) and len(urls):
        thread = threading.Thread(target=urls_process)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


# 线程池
@gettime
def Myfutures(num_of_max_works=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_of_max_works) as excutor:
        excutor.map(getdata, urls)


if __name__ == '__main__':
    getlink.gethao123link.getlink()

    urls = get_urls_from_file(10)
    Mynormal()
    MyprocessPool(10)
    Mymultithread(10)
    Myfutures(10)

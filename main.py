import requests
import chardet

data = requests.get('http://www.baidu.com')

charset = chardet.detect(data.content)  #检测编码

print(charset)

data.encoding = charset['encoding']

print(data.text)

import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Douban():
    def __init__(self):
        self.url = "https://www.douban.com/"
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.setting.userAgent"] = (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0")
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', desired_capabilities=dcap)

    def log_in(self):
        self.driver.get(self.url)
        time.sleep(3)  # 睡3分钟，等待页面加载
        # self.driver.save_screenshot("0.jpg")
        iframe = self.driver.find_element_by_tag_name("iframe")
        self.driver.switch_to.frame(iframe)

        self.driver.find_element_by_class_name('account-tab-account').click()

        self.driver.find_element_by_id('username').send_keys("15989546438")
        self.driver.find_element_by_id('password').send_keys("a15914710451")
        # 点击登陆
        self.driver.find_element_by_class_name("btn-account").click()
        time.sleep(2)
        # self.driver.save_screenshot("douban.jpg")
        # 输出登陆之后的cookies
        print('cookies: ', self.driver.get_cookies())

    # def __del__(self):
    #     '''调用内建的析构方法，在程序退出的时候自动调用
    #     类似的还可以在文件打开的时候调用close，数据库链接的断开
    #     '''
    #     self.driver.quit()


if __name__ == "__main__":
    douban = Douban()  # 实例化
    douban.log_in()  # 之后调用登陆方法

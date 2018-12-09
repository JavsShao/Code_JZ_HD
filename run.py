import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 基本配置文件
EMAIL = 'javs_shao@163.com'
PASSWORD = 'QWERTY1234'
BORDER = 6
INIT_LEFT = 60

class CrackGeetest(object):
    def __init__(self):
        '''
        初始化
        '''
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def __del__(self):
        '''
        关闭浏览器
        :return:
        '''
        self.browser.close()

    def open(self):
        '''
        打开网页输入用户名和密码
        :return:
        '''
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_position(self):
        '''
        获取验证码位置
        :return: 验证码位置元组
        '''
        img = self.wait.until((EC.presence_of_element_located(By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)
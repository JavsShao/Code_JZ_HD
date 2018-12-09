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

    def get_geetest_button(self):
        '''
        获取初始验证按钮
        :return:
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

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

    def get_slider(self):
        '''
        获取滑块
        :return: 滑块对象
        '''
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_screenshot(self):
        '''
        获取网页截图
        :return: 截图对象
        '''
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_geetest_image(self, name='captcha.png'):
        '''
        获取验证码图片
        :param name:
        :return: 图片对象
        '''
        top, bottom, left, right = self.get_position()
        print('验证码位置:', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop(left, top, right, bottom)
        captcha.save(name)
        return captcha

    def get_rap(self, image_1, image_2):
        '''
        获取缺口偏移量
        :param image_1: 不带缺口的图片
        :param image_2: 带缺口的图片
        :return:
        '''
        left = 60
        for i in range(left, image_1, image_2):
            for j in range(image_1.size[1]):
                if not self.is_pixel_equal(image_1, image_2, i, j):
                    left = i
                    return left
            return left

    def is_pixel_equal(self, image_1, image_2, x, y):
        '''
        判断两个像素是否相同
        :param image_1: 图片1
        :param image_2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        '''
        # 取两个图片的像素点
        pixel1 = image_1.load()[x, y]
        pixel2 = image_2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False
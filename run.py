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


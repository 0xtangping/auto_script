from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from playsound import playsound
import mail

from selenium.webdriver.common.action_chains import ActionChains






def check_change():
    global source
    source = ''
    url = 'https://micdrop.pepsi.com/'
    browser.get(url)

    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    while 1:
        # 清理缓存
        browser.delete_all_cookies()
        browser.refresh()
        browser.implicitly_wait(3)
        time.sleep(4)
        target = hash(browser.page_source)
        if target != source:
            playsound('alert.mp3')
            mail.send('cola', 'nft alert')
        source = target




# 1. 调用邮箱文件
# 2. selenium参数设置
# 3. 调用sign_up()
# 4. 注册后的信息写入文件
def main():
    global browser
    n = 0
    ua = UserAgent()
    agent = ua.chrome
    options = Options()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 避免一些无关紧要的报错
    options.add_argument('--user-agent={}'.format(agent))
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--start-maximized')  # 窗口最大化，感觉不太需要
    options.add_argument('--window-size=1920,1080')  # 设置窗口大小
    options.add_argument('--headless')          # 后台运行，可注释掉查看自动注册流程
    browser = webdriver.Chrome(chrome_options=options)
    # try:
    check_change()
    # except Exception:
    #     print('网页加载不出来')


if __name__ == "__main__":
    main()

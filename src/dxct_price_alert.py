from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from playsound import playsound
import mail

from selenium.webdriver.common.action_chains import ActionChains






def check_price():
    url = 'https://market.dnaxcat.io/nft/cat?element=Water,Fire&type=Brave&summon_times=0,1&sort=price_low'
    code = ''
    browser.get(url)

    windows = browser.window_handles


    while 1:
        # 清理缓存
        browser.delete_all_cookies()
        try:
            browser.refresh()

            browser.switch_to.window(windows[-1])
            browser.implicitly_wait(5)
            price = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/a[1]/div[2]/div[3]/span[1]').text
            style = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/a[1]/div[1]/div[2]').get_attribute('style')

            print(price)

            if float(price) < 1.3 and (style.find('6e27815b8698ea49f35bfdb8b3bd6776') != -1 or style.find('69e7194949c1d89cd94cdbe6b58da853') != -1):
                playsound('alert.mp3')
                mail.send(price)
        except Exception:
            print('网页加载不出来')


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
    # options.add_argument('--headless')          # 后台运行，可注释掉查看自动注册流程
    browser = webdriver.Chrome(chrome_options=options)
    check_price()



if __name__ == "__main__":
    main()

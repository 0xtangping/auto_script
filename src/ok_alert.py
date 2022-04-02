from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from playsound import playsound
import mail

from selenium.webdriver.common.action_chains import ActionChains






def check():
    url = 'https://www.okex.com/trade-margin/axs-usdt'
    code = ''
    browser.get(url)

    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    browser.implicitly_wait(5)
    time.sleep(5)


    while 1:
        # 清理缓存
        # browser.delete_all_cookies()
        try:
            # buy_amount = browser.find_element_by_xpath('//*[@id="leftPoForm"]/div[6]/div/div/span[2]').text
            sell_amount = browser.find_element_by_xpath('//*[@id="rightPoForm"]/div[6]/div/div/span[2]').text.split('.')[0]

            if int(sell_amount) > 10:
                mail.send('axs_alert', sell_amount)
                playsound('alert.mp3')

            # print(buy_amount)
            print(sell_amount)
            print('-----')
            # browser.refresh()


            time.sleep(5)
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
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 避免一些无关紧要的报错
    # options.add_argument('--user-agent={}'.format(agent))
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--start-maximized')  # 窗口最大化，感觉不太需要
    # options.add_argument('--window-size=1920,1080')  # 设置窗口大小
    options.add_argument(r"user-data-dir=C:\Users\liuqiang\AppData\Local\Google\Chrome\User Data")   # 把数据传入程序
    options.add_argument('–profile-directory=Profile 7')
    # options.add_argument('--headless')          # 后台运行，可注释掉查看自动注册流程
    browser = webdriver.Chrome(chrome_options=options)
    check()
#     	C:\Users\liuqiang\AppData\Local\Google\Chrome\User Data\Profile 7



if __name__ == "__main__":
    main()

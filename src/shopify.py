from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import csv
import random
from fake_useragent import UserAgent
from random_words import RandomWords
from random_words import RandomNicknames
from selenium.webdriver.common.action_chains import ActionChains


# 获取邮箱
def get_mails(path):
    mails = set()
    with open(path) as file_object:
        for line in file_object:
            mail = line.strip().split("----")[0]
            if len(mail) > 0:
                mails.add(mail)
    return mails


def get_store_name():
    rw = RandomWords()
    name = rw.random_word() + rw.random_word() + str(random.randint(100, 999))
    return name


def sign_up(mail, pwd, name):
    global first_name, last_name, apartment, phone
    url = 'https://www.shopify.com/signup'
    code = ''
    browser.get(url)

    windows = browser.window_handles

    # 清理缓存
    browser.delete_all_cookies()
    try:
        browser.switch_to.window(windows[-1])
        browser.implicitly_wait(5)
        time.sleep(2)
        browser.find_element_by_id('0_signup_email').send_keys(mail)
        time.sleep(2)
        browser.find_element_by_id("0_signup_password").send_keys(pwd)
        time.sleep(2)
        browser.find_element_by_id("0_signup_shop_name").send_keys(name)
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="SignupPageSignup"]/div[5]/button').click()

        # chrome浏览器兼容
        time.sleep(10)
        browser.implicitly_wait(10)
        browser.switch_to.window(windows[-1])
        browser.find_element_by_xpath("//*[@id=\"app\"]/div/div/div/button/span/span").click()

        # 跳过问卷调查
        time.sleep(5)
        browser.implicitly_wait(5)
        browser.switch_to.window(windows[-1])
        browser.find_element_by_xpath(
            "//*[@id=\"AppFrameMain\"]/div/div/div[1]/div/footer/div/div[2]/div/button/span/span").click()

        # 填写详细信息
        time.sleep(2)
        browser.implicitly_wait(2)
        browser.switch_to.window(windows[-1])
        rn = RandomNicknames()

        first_name = rn.random_nick(gender='u')
        last_name = rn.random_nick(gender='u')
        apartment = get_store_name()
        phone = str(212) + str(random.randint(1000000, 9999999))
        time.sleep(2)

        k1 = browser.find_element_by_name('account_setup[firstName]')
        ActionChains(browser).double_click(k1).perform()  # 鼠标双击
        k1.send_keys(first_name)
        time.sleep(2)
        k2 = browser.find_element_by_name('account_setup[lastName]')
        ActionChains(browser).double_click(k2).perform()  # 鼠标双击
        k2.send_keys(last_name)
        time.sleep(2)
        browser.find_element_by_name('account_setup[address1]').send_keys("Manhattan")
        time.sleep(2)
        browser.find_element_by_name('account_setup[address2]').send_keys(apartment)
        time.sleep(2)
        browser.find_element_by_name('account_setup[city]').send_keys("New York")
        time.sleep(2)
        browser.find_element_by_name('account_setup[zip]').send_keys("10166")
        time.sleep(2)
        browser.find_element_by_name('account_setup[phone]').send_keys(phone)
        time.sleep(2)
        Select(browser.find_element_by_name('account_setup[country]')).select_by_visible_text("United States")
        time.sleep(2)
        Select(browser.find_element_by_name('province')).select_by_visible_text("New York")
        time.sleep(2)
        browser.find_element_by_xpath(
            "//*[@id=\"AppFrameMain\"]/div/div/div[2]/div/footer/div[1]/div[2]/button/span/span").click()

        time.sleep(10)
        browser.implicitly_wait(10)
        browser.switch_to.window(windows[-1])
        browser.find_element_by_xpath("//*[@id=\"app\"]/div/div/div/button/span/span").click()

        time.sleep(20)
    except Exception:
        print('网页加载不出来')
        time.sleep(600)
        name = get_store_name()
        sign_up(mail, pwd, name)

    return [mail, pwd, name, first_name, last_name, apartment, phone]


# 1. 调用邮箱文件
# 2. selenium参数设置
# 3. 调用sign_up()
# 4. 注册后的信息写入文件
def main():
    global browser
    n = 0
    for mail in get_mails("./mail.txt"):  # 设置注册ID范围，程序中断需要手动修改起始位置...
        pwd = mail + '123'
        store_name = get_store_name()

        t = time.time()
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
        # 调用sign_up函数注册
        user = sign_up(mail, pwd, store_name)
        f = open('./shopify.csv', 'a', newline='')
        writer = csv.writer(f)
        f.seek(0, 2)
        writer.writerow(user)
        f.close()
        n = n + 1
        print('Time now：{0}'.format(time.strftime("%Y%m%d %X", time.localtime())))
        print('注册第 "{}"个用时：{:.2f} 秒'.format(n, time.time() - t), end='\n---------------------')
        browser.quit()
        time.sleep(600)


if __name__ == "__main__":
    main()

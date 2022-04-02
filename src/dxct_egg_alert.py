import time

from fake_useragent import UserAgent
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mail

water_egg_price = 0.98
fire_egg_price = 0.98
light_egg_price = 0.7
parent_flag = 2


def check_egg(classinfo, price_threshold):
    param = ''
    cycle_num = 0
    while 1:
        # url = 'https://market.dnaxcat.io/nft/cat?type=Egg&element=Light&sort=price_low&page=2'
        url = 'https://market.dnaxcat.io/nft/cat?type=Egg&element=' + classinfo + '&sort=price_low' + param
        browser.get(url)
        browser.implicitly_wait(10)
        time.sleep(3)
        windows = browser.window_handles
        # try:
        browser.switch_to.window(windows[-1])

        for num in range(1, 25):
            picture_xpath = '//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/a[' + str(
                num) + ']/div[1]/div[3]'
            picture = browser.find_element_by_xpath(picture_xpath).get_attribute('style')
            price_xpath = '//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/a[' + str(
                num) + ']/div[2]/div[3]/span[1]'
            egg_price = float(browser.find_element_by_xpath(price_xpath).text)
            print(egg_price)
            if classinfo == 'Water' and picture.find('water2.png') != -1 and egg_price < water_egg_price:
                egg_url = browser.find_element_by_xpath(picture_xpath[:-14]).get_attribute('href')
                check_parent('water', egg_url, egg_price)
                print('water')

            if classinfo == 'Fire' and picture.find('fire4.png') != -1 and egg_price < fire_egg_price:
                egg_url = browser.find_element_by_xpath(picture_xpath[:-14]).get_attribute('href')
                check_parent('fire', egg_url, egg_price)
                print('fire')

            if classinfo == 'Light' and picture.find('light8.png') != -1 and egg_price < light_egg_price:
                egg_url = browser.find_element_by_xpath(picture_xpath[:-14]).get_attribute('href')
                check_parent('light', egg_url, egg_price)
                print('light')

        cycle_num = cycle_num + 1
        param = '&page=' + str(cycle_num)
        price = browser.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/a[24]/div[2]/div[3]/span[1]').text
        if float(price) > price_threshold:
            break

    # except Exception:
    #     print('网页加载不出来')


def check_parent(classinfo, egg_url, egg_price):
    global skill
    skill = ''
    browser2.get(egg_url)
    browser2.implicitly_wait(8)

    print(egg_url)
    for parent in range(1, 3):
        parent_url = browser2.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div/div/div[2]/div/div/div[2]/section[2]/div[2]/a[' + str(
                parent) + ']').get_attribute('href')
        print(parent_url)
        browser3.get(parent_url)
        time.sleep(3)
        parent_text = browser3.page_source
        check_skill(classinfo, parent_text)
    title = 'dxct蛋预警'
    content = classinfo + ';' + skill + ';' + str(egg_price) + ';' + egg_url

    if skill != '' and skill.count('&') >= parent_flag:
        print(content)
        playsound('alert.mp3')
        # mail.send(title, content)


def check_skill(classinfo, text):
    global skill
    if classinfo == 'water':
        if text.find('Lucky pompon') != -1:
            skill += 'Lucky pompon & '
        elif text.find('Key of Star') != -1:
            skill += 'Key of Star & '
    elif classinfo == 'fire':
        if text.find('Blast Gloves') != -1:
            skill += 'Blast Gloves & '
    elif classinfo == 'light':
        if text.find('Holy Code') != -1:
            skill += 'Holy Code & '
        elif text.find('Key of Star') != -1:
            skill += 'Key of Star & '


# 1. 调用邮箱文件
# 2. selenium参数设置
# 3. 调用sign_up()
# 4. 注册后的信息写入文件
def main():
    global browser
    global browser2
    global browser3

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
    browser2 = webdriver.Chrome(chrome_options=options)
    browser3 = webdriver.Chrome(chrome_options=options)
    while 1:
        try:
            check_egg('Water', water_egg_price)
            check_egg('Fire', fire_egg_price)
            check_egg('Light', light_egg_price)
        except Exception:
            print('网页加载不出来')


if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

plt.rcParams['font.sans-serif'] = ['SimHei']  # 或者使用 'MS Gothic' 或其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 初始化计数器
pn1 = 1   # 此为要爬取的视频页数总量
pn = 1   # 起始视频页数
play_count = []
play_time = []

def driver_get():
    global pn
    # 初始化WebDriver（确保已安装对应的WebDriver）
    driver = webdriver.Chrome()  # 或者使用其他浏览器的WebDriver
    driver.get(url = 'https://space.bilibili.com/example/video?tid=0&pn=' + str(pn) + '&keyword=&order=pubdate') # 此为要爬取的B站UP主的视频页，可根据实际情况更改'example'为UP主的UID

    try:
        # 等待特定元素加载完成
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'list-item'))
        WebDriverWait(driver, 15).until(element_present) # 15秒超时，可根据实际情况调整

        # 获取页面源代码
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # 查找数据
        li_tags = soup.find_all('li', class_='list-item clearfix fakeDanmu-item')
        for li in li_tags:
            data_aid = li.get('data-aid')
            play_count2 = li.find('div', class_='meta')
            play_count3 = play_count2.find('span', class_='play')
            play_count1 = play_count3.find('span').get_text(strip=True)
            play_time1 = li.find('span', class_='time').get_text(strip=True)
            print(f"BV号: {data_aid}, 播放数: {play_count1}, 发布时间: {play_time1}")
            play_time.append(play_time1)
            match = re.search(r'(\d+(\.\d+)?)(亿|万)?', play_count1) # 使用正则表达式提取播放量，包括纯数字、"万"和"亿"
            if match:
                play_count_str = match.group(0)
                # 处理播放量数值转换
                if "亿" in play_count_str:
                    play_count.append(float(play_count_str.replace("亿", "")) * 10000 * 10000)
                elif "万" in play_count_str:
                    play_count.append(float(play_count_str.replace("万", "")) * 10000)
                else:
                    play_count.append(int(play_count_str))

    finally:
        driver.quit()
        pn += 1
for i in range(pn1):
    driver_get()
# 逆序排列数据
play_time.reverse()
play_count.reverse()

# 绘制统计图
plt.figure(figsize=(10, 5))
plt.plot(play_time, play_count, marker='o', linestyle='-', color='b')
plt.xlabel('发布时间')
plt.ylabel('播放量')
plt.title('视频播放量随发布时间的变化统计图')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

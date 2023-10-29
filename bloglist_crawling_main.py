#Step 0. 필요한 모듈과 라이브러리를 로딩합니다.
import sys # 시스템
import os  # 시스템
from selenium.webdriver.common.by import By
import pandas as pd  # 판다스 : 데이터분석 라이브러리
import numpy as np   # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup    # html 데이터를 전처리
from selenium import webdriver   # 웹 브라우저 자동화
from selenium.webdriver.common.keys import Keys
# import chromedriver_autoinstaller # 크롬 드라이버 자동설치

import time    # 서버와 통신할 때 중간중간 시간 지연. 보통은 1초
from tqdm import tqdm_notebook   # for문 돌릴 때 진행상황을 %게이지로 알려준다.

# 워닝 무시
import warnings
warnings.filterwarnings('ignore')

query_txt = sys.argv[1]
driver = webdriver.Chrome()

url_list = []
title_list = []
for i in range(1,50):
    
    driver.get('https://section.blog.naver.com/Search/Post.naver?pageNo='+str(i)+"&rangeType=ALL&orderBy=sim&keyword="+query_txt)
    time.sleep(1)

    # URL_raw 크롤링 시작
    articles = ".desc_inner"
    article_raw = driver.find_elements(By.CSS_SELECTOR, articles)

    if  len(article_raw)==0:
        break

    # article_raw[0].text

    # article_raw[0].get_attribute('href')

    # 크롤링한 url 정제 시작
    for article in article_raw:
        url = article.get_attribute('href')
        url = url[:8] +"m."+url[8:]
        print(url)
        url_list.append(url)
    time.sleep(1)

    # 제목 크롤링 시작
    for article in article_raw:
        title = article.text
        title_list.append(title)

        print(title)
    time.sleep(1)

    if  i%30==0:
        df = pd.DataFrame({'url':url_list, 'title':title_list})
        print(df)
        df.to_excel("bloglist/"+query_txt+".xlsx", encoding='utf-8-sig')

print("")
print('url갯수: ', len(url_list))
print('title갯수: ', len(title_list))

df = pd.DataFrame({'url':url_list, 'title':title_list})
print(df)

df.to_excel("bloglist/"+query_txt+".xlsx", encoding='utf-8-sig')



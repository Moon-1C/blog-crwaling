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

query_txt = input('1.크롤링할 키워드는 무엇입니까?: ')

# Step 1. 크롬 웹브라우저 실행
# chrome_path = chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
# 사이트 주소는 네이버
driver.get('http://www.naver.com')
time.sleep(1)  # 2초간 정지

# Step 2. 네이버 검색창에 "검색어" 검색
element = driver.find_element(By.ID,"query")
element.send_keys(query_txt)  # query_txt는 위에서 입력한 키워드
element.submit() # 검색어 제출
time.sleep(0.1)

# 'VIEW' 클릭
driver.find_element(By.LINK_TEXT,"VIEW").click( )
time.sleep(0.1)
# '옵션' 클릭
driver.find_element(By.LINK_TEXT,"옵션").click( )
time.sleep(0.1)

# 스크롤을 밑으로 내려주는 함수
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, 99999999)")
    time.sleep(0.5)

# n: 스크롤할 횟수 설정
n = 20  # 스크롤 1번 당 글 30개씩 화면에 보여짐
i = 0
while i < n: # 이 조건이 만족되는 동안 반복 실행
    scroll_down(driver) # 스크롤 다운
    i = i+1
    time.sleep(0.5)

# 블로그 글 url들 수집
url_list = []
title_list = []

# URL_raw 크롤링 시작
articles = ".title_link._cross_trigger"
article_raw = driver.find_elements(By.CSS_SELECTOR, articles)

# article_raw[0].text

# article_raw[0].get_attribute('href')

# 크롤링한 url 정제 시작
for article in article_raw:
    url = article.get_attribute('href')
    url = url[:8] +"m."+url[8:]
    print(url)
    url_list.append(url)
#time.sleep(1)

# 제목 크롤링 시작
for article in article_raw:
    title = article.text
    title_list.append(title)

    print(title)



print("")
print('url갯수: ', len(url_list))
print('title갯수: ', len(title_list))

df = pd.DataFrame({'url':url_list, 'title':title_list})
print(df)

df.to_excel(query_txt+".xlsx", encoding='utf-8-sig')
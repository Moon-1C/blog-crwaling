import sys
import os
import pandas as pd
import numpy as np
import utils


#Step 0. 필요한 모듈과 라이브러리를 로딩합니다.
import sys # 시스템
import os  # 시스템
from selenium.webdriver.common.by import By
import pandas as pd  # 판다스 : 데이터분석 라이브러리
import numpy as np   # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup    # html 데이터를 전처리
from selenium import webdriver   # 웹 브라우저 자동화

import time    # 서버와 통신할 때 중간중간 시간 지연. 보통은 1초
from tqdm import notebook   # for문 돌릴 때 진행상황을 %게이지로 알려준다.


xl_file=sys.argv[1]

# "url_list.xlsx" 불러오기

url_load = pd.read_excel("bloglist/"+xl_file)
url_load = url_load.drop("Unnamed: 0", axis=1)  # 불필요한 칼럼 삭제


driver = webdriver.Chrome()


dict = {}    # 전체 크롤링 데이터를 담을 그릇

# 수집할 글 갯수 정하기
number = len(url_load)



for i in notebook.tqdm(range(0, number)):
    # 글 띄우기
    url = url_load['url'][i]
    
    driver = webdriver.Chrome()

    driver.get(url)   # 글 띄우기
    
    # 크롤링
    # 예외 처리
    try : 
        

        # 내용 크롤링
        overlays = ".se-component.se-text.se-l-default"                                 
        contents = driver.find_elements(By.CSS_SELECTOR,overlays)    # contents

        content_list = []
        for content in contents:
            content_list.append(content.text)
 
       # content_str = ' '.join(content_list)                         # content_str
        result= utils.extract_important_words(content_list)
        print(result)

        # 각각의 글은 dict라는 딕셔너리에 담기게 됩니다.
        dict[i] = result
        
        # 크롤링이 성공하면 글 제목을 출력하게 되고,
        print(i)

        # 글 하나 크롤링 후 크롬 창을 닫습니다.
        driver.close() 
    
    # 에러나면 현재 크롬창을 닫고 다음 글(i+1)로 이동합니다.
    except:
        
        print("에러",i)
        driver.close()
        time.sleep(0.01)
        continue
    
    # 중간,중간에 파일로 저장하기
    if i==2 or i == number//4 or number//2 or number//4*3:
        # 판다스로 만들기
        import pandas as pd
        result_df = pd.DataFrame.from_dict(dict, 'index')

        # 저장하기
        result_df.to_excel("content/"+xl_file, encoding='utf-8-sig')
        time.sleep(3)
        
print('수집한 글 갯수: ', len(dict))
print(dict)
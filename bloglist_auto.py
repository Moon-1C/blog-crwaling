import pandas as pd 
import sys # 시스템
import subprocess



url_load = pd.read_excel("여행지.xlsx")
print(url_load)

for i in range(0,len(url_load)):
    url = url_load['여행지'][i]
    print(url)

    subprocess.call("bloglist_crawling_main.py " + url, shell=True)
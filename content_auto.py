import pandas as pd 
import sys # 시스템
import subprocess
import os

dir = './bloglist'
files = os.listdir(dir)


for file in files :

    url_load = pd.read_excel(dir+"/"+file)
    print(url_load)

    subprocess.call("content_crawling.py " +file, shell=True)


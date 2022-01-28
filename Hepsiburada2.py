# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 16:01:43 2022

@author: Hp
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np
import lxml.html
import csv
import pandas as pd
import time 
import random

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
linkler = []  
for i in range(1,3):
    url='https://www.hepsiburada.com/lufian?sayfa='
    sayfa = url+str(i)
    linkler.append(sayfa)
linkler
#Out[3]: Sayfalama kısmındaki linkleri elde ettim. 
#['https://www.hepsiburada.com/lufian?sayfa=1',
# 'https://www.hepsiburada.com/lufian?sayfa=2']

   
linkler1=[]
for i in range(len(linkler)):
    tree = requests.get(linkler[i], headers = headers)
    print(f'FIRAT KABAN ; {linkler[i]}')
    soup = BeautifulSoup(tree.content, 'html.parser')
    st3 = soup.find_all("li",attrs={"data-index":"1"})
    for a in range(len(st3)):
      linkler1.append(st3[a].a.get('href'))
for j in range(len(linkler1)):
     linkler1[j] = "https://www.hepsiburada.com"+linkler1[j]
#ürün linkleri alındı 
# ürün linki : https://www.hepsiburada.com/lufian-brando-erkek-corap-lacivert-p-HBCV00000TV7DI

_link = []
kelime = '-yorumlari'
for deneme1 in linkler1:
    _link.append([deneme1, deneme1 + kelime])

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

ratings = []
for urls in _link:
    url = urls[0]
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    rating = soup.find("div", attrs={"id":"comments-container"})
    if rating is None:
        continue
    rating = rating.text.strip()
    if rating == "":
        continue
    ratings.append([url, rating.split(" ")[0]])

def get_rating_count(ratings, product_url):
    for rating in ratings:
        if rating[0] == product_url:
            return int(rating[1])
    return None

comments = []
for urls in _link:
    url = urls[0]  # Product link
    curl = urls[1] # Comments link
    rating_count = get_rating_count(ratings, url)
    if rating_count == None: # No comment
        comments.append([url, [""]])
        continue
    page_count = int((rating_count/25)+1)
    page_count = 2 if page_count == 1 else page_count
    all_comments = []
    for page in range(1, page_count):
        response = requests.get(curl + "?sayfa=" + str(page), headers=headers)
        tree = lxml.html.fromstring(response.text)
        page_comments = [comment.text for comment in tree.xpath("//div[@class='hermes-ReviewCard-module-34AJ_']/div[@class='hermes-ReviewCard-module-3Y36S']/div[@class='hermes-ReviewCard-module-2dVP9']/span")]
        for comment in page_comments:
            all_comments.append(comment)
    comments.append([url, all_comments])
    
df = pd.DataFrame(comments, columns=["Ürün Linki", "Yorumlar"])
df.to_excel(r'C:/Users/Hp/Desktop/Hepsiburadaa.xlsx',index=False)

konum = 'C:/Users/Hdfp/Desktop/Hepsiburadaa'
df.to_csv(konum +'.csv', sep='|', index=False)

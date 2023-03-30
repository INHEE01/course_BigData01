from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time
import re

# - 각 매장의 [매장이름, 시/도, 군/구, 주소] 네 가지 정보 가져오기
# Example URL : https://www.kyochon.com/shop/domestic.asp?sido1=1&sido2=1&txtsearch=
# 파라미터 정리 : sido1=1&sido2=1 -> 앞에 sido1 -> 서울 / 경북 ... 시도 정보 (1 ~ 17) / sido2 -> 구 정보 ()
# 1 ->  1 ~ 25 / 2 -> 1 ~ 16 / 3 -> 1 ~ 8 / 4 -> 1 ~ 10 / 대구 5 -> 1 ~ 5 / 대전 6 -> 1 ~ 5
# 울산 7 -> 1 ~ 5 / 세종 8 -> 1 ~ 16 / 경기 9 -> 1 ~ 44 / 강원 10 -> 18 / 충주 11 -> 15
# 충남 12 -> 17 / 전북 13 -> 15 /  전남 14 -> 22 / 경북 15 -> 24 / 경남 16 -> 22
# 제주 17 -> 2
# 배열로 만들어서 처리할 것.
#
# Web HTML 정보
# <div class="shopSchList"> 안에 매장 리스트가 있음.

def wCrawling(result):
  s2 = [0, 25, 16, 8, 10, 5, 5, 5, 16, 44, 18, 15, 17, 15, 22, 24, 22, 2] # parameter sido2 에 대한 정보

  for sido1 in range(1, 18):
    for sido2 in range(1, s2[sido1]+1):
      time.sleep(1)
      url = 'https://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' %(sido1, sido2)
      print(url)
      html = urllib.request.urlopen(url)
      SoupUrl = BeautifulSoup(html, 'html.parser')
      tag_name = SoupUrl.find('ul', attrs={'class':'list'}) # ul class="list" 를 찾는다.
 
      for store in tag_name.find_all('li'):
        if len(store) <= 3:
          break

        store_name = store.find('strong').get_text()
        store_sido = store.find('em').get_text().split(' ')[0]
        store_gungu = store.find('em').get_text().split(' ')[1]
        store_addr1 = store.find('em').get_text()
        address_regex = re.compile(r'\(.+\)')
        match_addr = address_regex.search(store_addr1)
        # 정규 표현식을 통한 주소 추출
        # 도로명주소가 존재한다면 도로명주소를 가져오고, 도로명주소가 존재하지 않는다면 그냥 주소를 가져와서 store_addr 변수에 저장.
        if match_addr:
          store_addr = match_addr.group().strip('()')
        else:
          start_index = store_addr1.index("(")
          end_index = store_addr1.index(")")
          addr = store_addr1[:start_index] + store_addr1[end_index+1:]
          store_addr = addr.strip()

        result.append([store_name] + [store_sido] + [store_gungu] + [store_addr])
        

def main():
  result = []
  wCrawling(result)
  Wcrawling_tbl = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'address'))
  Wcrawling_tbl.to_csv('C:/Users/raven/git/course_BigData01/ihBigData/Data/KyoChon.csv', encoding='cp949', mode='w', index=True)
  del result[:]

if __name__ == '__main__':
  main()
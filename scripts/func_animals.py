import requests
import re
from bs4 import BeautifulSoup
import datetime as dt 
# if문 통과시켜야하므로, bool객체 반환시킴
def check(id):
  try : 
    int(id)
    result = True
  except : 
    print('이상 발견')
    result = False
  return result    
# https://www.animal.go.kr/front/awtis/protection/protectionDtl.do?desertionNo=441553202203131
def moveUrl(id):
  if isinstance(id, str):
    url = 'https://www.animal.go.kr/front/awtis/protection/protectionDtl.do?desertionNo='+ id
  else : 
    print('이상 발견')
  return url

def kindClean(kind):
  splited = kind.replace('[', '').split(']')
  small_kind = splited[1].strip()
  return small_kind

def colorClean(color):
  color_splited = color.split('.')
  color_list = [ color.strip() for color in color_splited ]
  color = ';'.join(color_list)
  return color

def sexClean(sex):
  sex = re.sub('[^ ㄱ-ㅣ가-힣+]', '' , sex).strip()
  return sex

def cleanAge(age_weight):
  replaced = age_weight.replace('\r\n', '').replace(' ', '')
  splited = replaced.split(')')
  year = splited[0].split('(')[0].strip()
  try : 
    # int형 변환
    year = int(year)
    x = dt.datetime.now()
    current_year = x.year
    estimated_age = current_year - year 
    estimated_age =  int(estimated_age)
  except : 
    # int형 변환이 안 되면 추정 안되는 것이므로, 정보없음(0)으로 취급
    estimated_age = 0 
  return estimated_age

def getCity(authority):
  splited = authority.split(' ')
  city = splited[0].strip()
  print("#city : ", city)
  return city


def getSegInfo(id):
  url = moveUrl(id)
  item_res = requests.get(url)
  item_soup = BeautifulSoup(item_res.text, "html.parser")
  img_url = item_soup.select('img.photoArea')[0].get('src')
  table = item_soup.select_one('table')
  td_list = table.select('td')
  td_list = [ td.text.strip() for td in td_list]
  print("len>> ", len(td_list))
  print(td_list)
  if len(td_list) == 17 :
      kind = td_list[1]
      color = td_list[2]
      sex = td_list[3]
      age_weight = td_list[4]
      spot = td_list[5]
      reception_date = td_list[6]
      character = td_list[8]  
      center = td_list[14]
      call = td_list[15]
      location = td_list[16]
      small_kind = kindClean(kind)
      color = colorClean(color)
      sex = sexClean(sex)
      year = cleanAge(age_weight)
      
  if len(td_list) == 16 :
      kind = td_list[2]
      color = td_list[3]
      sex = td_list[4]
      age_weight = td_list[5]
      spot = td_list[6]
      reception_date = td_list[7]
      character = td_list[9]  
      center = td_list[13]
      call = td_list[14]
      location = td_list[15]
      small_kind = kindClean(kind)
      color = colorClean(color)
      sex = sexClean(sex)
      year = cleanAge(age_weight)
  return  url , img_url, small_kind, color, sex, year,  spot, reception_date, character,center, call, location

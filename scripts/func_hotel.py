import requests
import re
from bs4 import BeautifulSoup
import datetime as dt 

def mapping(text):
  rank2int = {
    '강력추천' : 5,
    '최고' : 4,
    '우수함' : 3,
    '매우좋음' : 2,
    '좋음' : 5,
    '정보없음' : 0
  }
  mapped_val = rank2int[text]
  return mapped_val


def checkScore(score_text):
  if score_text.startswith('이용') or score_text.endswith('평점'):
    score_text = '정보없음'
  else :
    splited = score_text.split(' ')
    score_text = ''.join(splited) 
  
  score_int = mapping(score_text)
  return score_int


def checkNone(list_obj):
  if len(list_obj) == 0 :
    result = '정보없음'
  else :
    print(list_obj[0])
    if list_obj[0] == None :
      print('none')
      result = '정보없음'
    else : 
      result = list_obj[0].text.strip()
  return result

def getReviewNum(review_num):
  review_num = checkNone(review_num)
  review_num = re.sub(r'[^0-9]', '', review_num)
  try :
      review_num = int(review_num)
  except : 
      review_num = 0 
  return review_num

# ========  only for KoreaHotel Model ========================
def checkKRNone(list_obj):
  print(len(list_obj), type(list_obj))
  if (len(list_obj) == 0) :
    result = '정보없음'
  else :
    print("##", list_obj[0])
    if list_obj[0] == None :
      result = '정보없음'
    else :
      result = list_obj[0].strip()
  return result


def getKRReviewNum(review_num):
  review_num = checkKRNone(review_num)
  review_num = re.sub(r'[^0-9]', '', review_num)
  try :
      review_num = int(review_num)
  except : 
      review_num = 0 
  return review_num

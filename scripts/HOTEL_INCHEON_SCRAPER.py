import requests
import re
from bs4 import BeautifulSoup
from pet.models import HotelCategory, SGIHotel
from scripts.HOTEL_URL import HOTEL_INCHEON
from scripts.func_hotel import checkNone, checkScore, getReviewNum

def run():
    base_url = 'https://www.booking.com'
    INCHEON_URL =  HOTEL_INCHEON
    res = requests.get(INCHEON_URL)
    soup = BeautifulSoup(res.text, "html.parser")
    contents = soup.find_all('div',class_='sr__card_content')
    imgs = soup.find_all('div',class_='sr__card_photo')
    
    for img, item in zip(imgs, contents):
        img_url = img.select('a > img')[0].get('src').strip()
        print("# img : ", img_url)
        link = item.select('header')[0].find("a")["href"] 
        link = base_url + link
        print("link : ", link)
        name = item.select('h3 > span')[0].text.strip()
        print(name)
        location = item.select('p > span')[0].text.strip()
        print(location)
        explain = item.select('div > p')[0].text.strip()
        print(explain)
        score_list = item.select('div.bui-review-score__title')
        score = checkNone(score_list)
        score = checkScore(score)
        print("score : ", score)
        review_num = item.select('div.bui-review-score__text')
        review_num = getReviewNum(review_num)
        print("# review_num:", review_num )
        print("------------------------------")

        category = HotelCategory.objects.get(name='인천')
        db_link_cnt = SGIHotel.objects.filter( sgi_hotel_link__iexact = link).count()
        if (db_link_cnt == 0 ) :
            print("저장")
            SGIHotel(category = category, sgi_hotel_link = link, sgi_hotel_img_url =  img_url, sgi_hotel_name = name, sgi_hotel_location  = location, sgi_hotel_explain  = explain, sgi_hotel_score = score, sgi_hotel_review_num  = review_num ).save()
        else : print("## 중복된 값")


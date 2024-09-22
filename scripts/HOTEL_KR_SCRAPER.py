import requests
import re
from bs4 import BeautifulSoup
from pet.models import HotelCategory, KoreaHotel
from scripts.HOTEL_URL import HOTEL_KOREA
from scripts.func_hotel import  getKRReviewNum

def run():
    korea_url = HOTEL_KOREA
    res = requests.get(korea_url)

    soup = BeautifulSoup(res.text, "html.parser")
    
    top10_list = soup.find_all("div", class_ = "bui-card bui-card--media bui-u-bleed@small theme-landing-property-card__container")

    contents = soup.find_all('div',class_='sr__card_content')
    imgs = soup.find_all('div',class_='sr__card_photo')

    for hotel in top10_list:
        # top10 url
        img_url = hotel.select('img')[0].get('src')
        link = hotel.find("a", class_ = "bui-card__header_full_link_wrap").get('href')

        # top10 name 
        name = hotel.select('img')[0].get('alt').strip()

        # address
        location = hotel.find_all('meta')[1].get('content').strip()

        # description
        explain = hotel.find("p" , class_ = "bui-card__text theme-landing-property-card__description theme-landing-property-card__description--truncated").text.strip()

        # review score
        score = hotel.find('span', class_ = "review-score-badge").text.strip()
        score = float(score)

        # # review rank 
        # rank = hotel.find('span', class_ = "review-score-widget__text").text.strip()

        # review num
        review_num = hotel.find('span', class_ = "review-score-widget__subtext").text.strip()
        review_num = getKRReviewNum(review_num)


        print("# img : ", img_url, type(img_url))
        print("# link : ", link, type(link))
        print("# name : ", name, type(name))
        print("# addr : ", location, type(location))
        print("# explain : ", explain, type(explain) )
        print("# score, rank, review_num : ", score, review_num )
        print("# score, rank, review_num : ", type(score),  type(review_num) )
        print("_________________________________________________________________________")

        
        category = HotelCategory.objects.get(name='전국')
        db_link_cnt = KoreaHotel.objects.filter( kh_hotel_link__iexact = link).count()
        if (db_link_cnt == 0 ) :
            KoreaHotel(category = category, kh_img_url = img_url, kh_hotel_link = link, kh_hotel_name = name, kh_hotel_location = location, kh_hotel_explain = explain,  kh_hotel_score = score, kh_hotel_review_num = review_num ).save()
            print("저장")       
        else : print("## 중복된 값")
import requests
import re
from bs4 import BeautifulSoup
# 모델 전 
# from data_crawl.models import Animals, AnimalCategory
from scripts.func_animals import check,  getSegInfo
from scripts.ANIMALS_URL import GYEONGGI_URL
from pet.models import AnimalCategory, Animals, SaveAnimalCategory

def run():
    for i in range(1,6):
        # 경기도 URL
        url = GYEONGGI_URL + str(i)
        item_res = requests.get(url)
        item_soup = BeautifulSoup(item_res.text, "html.parser")
        list_area = item_soup.select('ul.list')
        list_area = list_area[1]
        atag_list = list_area.select('a.moreBtn')

        for tag in atag_list :
            print(tag)
            print('###############')
            info = tag.get('onclick')
            print(info)
            info_splited = info.split("'")
            if check(info_splited[1]):
                id = info_splited[1].strip()
                print(id)
                url , img_url, small_kind, color, sex, year,  spot, reception_date, character,center, call, location = getSegInfo(id)
                print(url , img_url, small_kind, color, sex, year,  spot, reception_date, character,center, call, location)
                print('############################################')
            else : 
                print('정보없음')
            category = SaveAnimalCategory.objects.get(name='경기도')
            db_link_cnt = Animals.objects.filter(animals_animals_url__iexact = url).count()
            if (db_link_cnt == 0 ) :
                    Animals( animals_category = category , animals_animals_url=url, animals_img_url = img_url, animals_small_kind=small_kind, animals_color=color, animals_sex=sex, animals_year=year, animals_spot=spot, animals_reception_date=reception_date,  animals_character=character, animals_center=center,animals_call=call, animals_location=location).save()
                    print("저장")
            else : print("## 중복된 값")

from django.views.generic import TemplateView
from django.views.generic import CreateView #새로룬 레코드 생성을 위한 폼 뷰 보임. 테이블 레코드 생성
from django.urls import reverse_lazy
from .forms import CreateUserForm
from pet.models import PetPost, RecommendPost, ShowoffPost, KoreaHotel, Animals, NewsScrap
from Account.models import Account
from django.shortcuts import render, redirect
from django.db import models
from datetime import datetime
from itertools import chain

class HomeView(TemplateView):
    template_name = "home.html"
    

#계정 생성 처리 부분
class UserCreateView(CreateView):
    form_class = CreateUserForm #forms.py에 정의 되어 있는 form 클래스
    template_name = 'registration/register.html' #보여질 template(html파일)파일 이름.
    #form에 입력 된 내용에 에러가 없고, 테이블 레코드 생성이 완료된 후 이동할 url 지정
    #success_url 역시 CreateView 상속 안에 있는 내용으로 만약 계정 생성이 성공할 경우 어느 페이지로 넘길건지에 대한 정보를 담음
    success_url = reverse_lazy('register_done') #url패턴 전달 인자, urls.py 모듈이 메모리 로딩 된 후에 실행

#계정 생성 완료됐다는 페이지 이동
class UserCreateDoneTV(TemplateView):
    #템플릿만 넘기면 됨. 데이터를 입력하거나 가져올 필요가 없음.
    template_name = 'registration/register_done.html' #보여질 템플릿 파일 이름.
    
    
class NaverMap(TemplateView):
    template_name = 'naver_map.html'
    

class NaverMapCenter(TemplateView):
    template_name = 'naver_map_center.html'
    
def home_view(request):    
    if PetPost.objects.count() != 0:
        post_list1 = PetPost.objects.values_list().order_by('-created_at')[:3]
        post_list2 = RecommendPost.objects.values_list().order_by('-created_at')[:3]
        post_list3 = ShowoffPost.objects.values_list().order_by('-created_at')[:3]
        # post_list = post_list1.union(post_list2).union(post_list3)
        # post_list1 = list(chain(post_list1, post_list2, post_list3))
        post_list = []
        for i in post_list1:
            post_list.append(i)
        for i in post_list2:
            post_list.append(i)
        for i in post_list3:
            post_list.append(i)
        #print(post_list)
        #print()
        #print(sorted(post_list, key = lambda x : x[3], reverse=True)[:3])
        #print()
        #print(post_list)
        # print()
        # print(type(post_list[0]))
        # print(KoreaHotel.objects.all().order_by("kh_hotel_score").reverse()[:3])
        # print()
        # print(NewsScrap.objects.all()[:3])
        author_list = []
        for i in sorted(post_list, key = lambda x : x[3], reverse=True)[:3]:
            print(Account.object.values().filter(uid__contains=i[6])[0]["username"])
            author_list.append(Account.object.values().filter(uid__contains=i[6])[0]["username"])
            print(author_list)
            
        
        content = {
            "post_list" : zip(sorted(post_list, key = lambda x : x[3], reverse=True)[:5], author_list),
            "hotel_list" : KoreaHotel.objects.all().order_by("kh_hotel_score").reverse()[:3],
            "save_animal_list" : Animals.objects.all()[:5],
            "news_list" : NewsScrap.objects.all()[:3]
        }
    else:
        #print("no")
        content = {
            "post_list" : None,
            "hotel_list" : KoreaHotel.objects.all().order_by("kh_hotel_score").reverse()[:3],
            "save_animal_list" : Animals.objects.all()[:5],
            "news_list" : NewsScrap.objects.all()[:3]
        }
    return render(request,"home.html" ,content)


# [(6, '정보공유 수정 test', '<p>정보공유 수정 test</p><p><img src="/media/django-summernote/2022-12-22/f66b0cce-e0c1-4563-b423-02b4e781c95d.png" style="width: 668px;"><br></p>', datetime.datetime(2022, 12, 22, 12, 29, 54, 192892, tzinfo=datetime.timezone.utc),
#   datetime.datetime(2022, 12, 22, 13, 48, 12, 995164, 
# tzinfo=datetime.timezone.utc), 
#   '', UUID('25c95a82-b275-4863-8b0d-2bf1a4a678e5'), 1),
#  (5, 'no_head_image_test', '<p>ㅇ누일마ㅓㅣㅓ</p><p>ㄴㅇ럼ㄴ일맞더;ㅁ</p><p>ㅇㄴ라ㅓㅁㄴ이라머</p><p>ㅁㅇㅍ뫙ㄹ몯<img src="/media/django-summernote/2022-12-22/2fcf7c9b-3e26-4b3b-aaac-9633119385b5.png" style="width: 1252px;"></p>', datetime.datetime(2022, 12, 22, 6, 19, 18, 710309, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 12, 22, 6, 19, 18, 710309, tzinfo=datetime.timezone.utc), '', UUID('25c95a82-b275-4863-8b0d-2bf1a4a678e5'), 1), (1, '추천용품 수정 테스트', '<p>추천용품 수정 테스트입니다</p><p><img src="/media/django-summernote/2022-12-22/465c815a-b07a-48dd-8687-c04b93f779bc.png" style="width: 1252px;"><br></p>', datetime.datetime(2022, 12, 22, 12, 55, 28, 531127, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 12, 22, 13, 49, 41, 811565, tzinfo=datetime.timezone.utc), '', UUID('25c95a82-b275-4863-8b0d-2bf1a4a678e5'), 
# 4), (1, '내새끼 최고야 수정 test', '<p>쭈아아아아압 수정</p><p><img src="/media/django-summernote/2022-12-22/c33fb6a7-20e6-4155-976a-2e1cc165a102.gif" style="width: 500px;"><br></p>', datetime.datetime(2022, 12, 22, 13, 12, 34, 892846, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 12, 22, 13, 51, 10, 580148, tzinfo=datetime.timezone.utc), 'pet/images/2022/12/22/a1.png', UUID('25c95a82-b275-4863-8b0d-2bf1a4a678e5'), 2)]
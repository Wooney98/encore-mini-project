
from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import User
from Account.models import Account

#slug field는 타입이 slug인 columns을 지정할 수 있다.
#slug는 사람이 읽을 수 있는 텍스트로 고유 url을 만들고 싶을 때 주로 사용한다.
#카테고리 테이블 지정
class AnimalCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode = True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url_board(self):
        return f'/pet/board/{self.slug}/'
    
    def get_absolute_url_recommend(self):
        return f'/pet/recommend/{self.slug}/'
    
    def get_absolute_url_show_off(self):
        return f'/pet/mybaby/{self.slug}/'
    
    
    class Meta:
        verbose_name_plural = "Animal_Category"
        

class PostCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Post_Category"

# Create your models here.
class PetPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #메인 이미지 지정 column
    thumnail = models.ImageField(upload_to='pet/images/%Y/%m/%d/', blank=True)
    author = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    
    category = models.ForeignKey(AnimalCategory, null = True, blank=True, on_delete=models.CASCADE)
    post_category = models.ForeignKey(PostCategory, null=True, blank=True, on_delete=models.CASCADE)
    #업로드한 파일의 이름을 가져옴
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    #업로드한 파일의 확장자를 가져옴
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #제일 뒤에 있는 값이 확장자
    
    def get_absolute_url(self):
        return f'/pet/board/{self.pk}/'


    def __str__(self):
        return f'{self.title} --- {self.author} ---- {self.created_at}'
    
    class Meta:
        verbose_name_plural='Pet_Post'
    
    
#-----------------------------승천이형------------------------------#
# --------------------------------------------------------------#
class NewsScrap(models.Model):
    news_top_image = models.CharField(max_length=200)
    news_title = models.CharField(max_length=200)
    news_content = models.TextField()
    news_udate = models.CharField(max_length=200,null=True)
    news_link = models.CharField(max_length=200)
    news_authors = models.CharField(max_length=100, null=True)
    def __str__(self,):
        return f"{self.news_title}--{self.news_content}--{self.news_link}"
    def get_absolute_url(self):
        return f'/pet/news/{self.pk}/'
    class Meta:
        verbose_name_plural='News_scrap'
    
#-----------------------------모아------------------------------#
# --------------------------------------------------------------#
# 보호중 동물 모델
class SaveAnimalCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/animal/category/{self.slug}/'
    class Meta:
        verbose_name_plural='save_animal_location_categories'

        
class Animals(models.Model): 
    animals_category = models.ForeignKey(SaveAnimalCategory, null=True, blank=False, on_delete=models.CASCADE)
    animals_animals_url = models.SlugField(max_length=255, unique=True, null=True,  allow_unicode=True)
    animals_img_url = models.CharField(max_length=255)
    animals_small_kind = models.CharField(max_length=200)
    animals_color = models.CharField(max_length=200)
    animals_sex = models.CharField(max_length=200)
    
    animals_year = models.IntegerField()
    animals_spot = models.CharField(max_length=200)
    animals_reception_date  = models.CharField(max_length=200)
    animals_character = models.CharField(max_length=200)  
    animals_center = models.CharField(max_length=200)
    animals_call = models.CharField(max_length=200)
    animals_location = models.CharField(max_length=200)

    def get_absolute_url(self):
        return f'/pet/animal_detail/{self.pk}/'
    
    def __str__(self):
        return f'{self.animals_img_url}'
    
    class Meta:
        verbose_name_plural='Animals_save'
        
        

# 반려동물 동반 호텔
class HotelCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/pet/hotel/category/{self.slug}/'
    class Meta:
        verbose_name_plural='hotel_categories'


class KoreaHotel(models.Model):
    category= models.ForeignKey(HotelCategory, null=True, blank=False, on_delete=models.CASCADE)
    kh_img_url = models.CharField(max_length=255)
    kh_hotel_link = models.CharField(max_length=255)
    kh_hotel_name = models.CharField(max_length=50)
    kh_hotel_location = models.CharField(max_length=50)
    kh_hotel_explain = models.TextField()
    kh_hotel_score = models.FloatField()
    kh_hotel_review_num = models.IntegerField()
    
    def get_absolute_url(self):
        return f'/pet/hotel_detail/{self.pk}/'
    
    def __str__(self):
        return f'{self.kh_hotel_name}'

    class Meta:
        verbose_name_plural='Korea_Hotel'

class SGIHotel(models.Model):
    category= models.ForeignKey(HotelCategory, null=True, blank=False, on_delete=models.CASCADE)
    sgi_hotel_link = models.CharField(max_length=255)
    sgi_hotel_img_url = models.CharField(max_length=255)
    sgi_hotel_name = models.CharField(max_length=50)
    sgi_hotel_location = models.CharField(max_length=50)
    sgi_hotel_explain = models.TextField()
    sgi_hotel_score  = models.IntegerField()
    sgi_hotel_review_num = models.IntegerField()
    
    def get_absolute_url(self):
        return f'/pet/hotel_detail/{self.pk}/'
    
    def __str__(self):
        return f'{self.sgi_hotel_name}'
    
    class Meta:
        verbose_name_plural='SGI_Hotel'
    
#---------------------------정훈이형----------------------------#
# --------------------------------------------------------------#
#용품추천 게시판
class RecommendPost(models.Model):
    #게시판 제목
    title = models.CharField(max_length=200, null=False)
    #게시글
    content = models.TextField()
    #게시글 생성 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    #게시글 업데이트 날짜
    updated_at = models.DateTimeField(auto_now=True)
    #대표 이미지
    thumnail = models.ImageField(upload_to='pet/images/%Y/%m/%d/',blank = True)
    #게시글 작성자
    author = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    #동물카테고리
    category = models.ForeignKey(AnimalCategory,blank=True,null=True, on_delete= models.CASCADE)
    post_category = models.ForeignKey(PostCategory, null=True, blank=True, on_delete=models.CASCADE)
    
        #업로드한 파일의 이름을 가져옴
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    #업로드한 파일의 확장자를 가져옴
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #제일 뒤에 있는 값이 확장자
    
    def get_absolute_url(self):
        return f'/pet/recommend/{self.pk}/'

    def __str__(self):
        return f'{self.title} -- {self.author} --- {self.created_at}'
    
    class Meta:
        verbose_name_plural='Recommend_Post'

#내새끼 자랑
class ShowoffPost(models.Model):
        #게시판 제목
    title = models.CharField(max_length=200, null=False)
    #게시글
    content = models.TextField()
    #게시글 생성 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    #게시글 업데이트 날짜
    updated_at = models.DateTimeField(auto_now=True)
    #대표 이미지
    thumnail = models.ImageField(upload_to='pet/images/%Y/%m/%d/',blank = True)
    #게시글 작성자
    author = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    #동물카테고리
    category = models.ForeignKey(AnimalCategory,blank=True,null=True, on_delete= models.CASCADE)
    post_category = models.ForeignKey(PostCategory, null=True, blank=True, on_delete=models.CASCADE)
            #업로드한 파일의 이름을 가져옴
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    #업로드한 파일의 확장자를 가져옴
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #제일 뒤에 있는 값이 확장자
    
    def get_absolute_url(self):
        return f'/pet/mybaby/{self.pk}/'


    def __str__(self):
        return f'{self.title} -- {self.author} --- {self.created_at}'
    
    class Meta:
        verbose_name_plural='Show_Off_Post'
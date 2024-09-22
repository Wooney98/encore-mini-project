from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name="pet"
urlpatterns = [
    path('create_post/',views.PetPostCreate.as_view(), name="create_post"),
    path('board/', views.BoardView.as_view(), name="board"),
    path('board/<int:pk>/', views.PetPostDetail.as_view(), name='post_deatil'),
    path('board/update_post/<int:pk>/',views.PetPostUpdate.as_view(), name = 'post_update'),
    path('board/<str:slug>/', views.pet_post_category_page), 
    
    path('animal/', views.AnimalView.as_view(), name="animal"),
    path('animal_detail/<int:pk>/', views.AnimalDetailView.as_view(), name="animal_detail"),
    path('hotel/', views.HotelView.as_view(), name="hotel"),
    path('hotel_detail/<int:pk>/', views.HotelDetailView.as_view(), name="hotel_detail"),
    path('hotel/category/<str:slug>/', views.hotel_category_page),
    path('mybaby/', views.ShowOffPostList.as_view(), name="mybaby"),
    path('mybaby/create_post/',views.ShowoffPostCreate.as_view(), name="mybaby_create_post"),
    path('mybaby/<int:pk>/', views.ShowoffPostDetail.as_view(), name="mybaby_detail"),
    path('mybaby/update_post/<int:pk>/',views.ShowOffPostUpdate.as_view(), name = 'mybaby_update'),
    path('mybaby/<str:slug>/', views.show_off_post_category_page), 
    
    path('recommend/', views.RecommendList.as_view(), name="recommend"),
    path('recommend/create_post/',views.RecommendPostCreate.as_view(), name="recommend_create_post"),
    path('recommend/<int:pk>/', views.RecommendPostDetail.as_view(), name="recommend_detail"),
    path('recommend/update_post/<int:pk>/',views.RecommendPostUpdate.as_view(), name = 'recommend_update'),
    path('recommend/<str:slug>/', views.recommend_post_category_page), 
    
    path('news/', views.NewsList.as_view(), name="news_list"),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name="news_detail"),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
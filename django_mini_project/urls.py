"""django_mini_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import HomeView, home_view
from .views import UserCreateView, UserCreateDoneTV, NaverMap, NaverMapCenter
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', HomeView.as_view(), name="home"),
    path('', home_view, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    #계정 생성 완료됐다는 메세지 보여줌
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name = 'register_done'),
    path('naver_map/hospital', NaverMap.as_view(), name="naver_map"),
    path('naver_map/center', NaverMapCenter.as_view(), name="naver_map_center"),
    path('summernote/', include('django_summernote.urls')),
    path('Account/', include('Account.urls')),
    path('pet/', include('pet.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
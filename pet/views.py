from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import PetPost, AnimalCategory, NewsScrap, SaveAnimalCategory, Animals, HotelCategory, KoreaHotel, SGIHotel, PostCategory
from .models import RecommendPost, ShowoffPost
from django.core.exceptions import PermissionDenied
from .forms import PostForm, RecommendPostForm, ShowoffPostForm

class BoardView(ListView):
    template_name = "pet/boards.html"
    model = PetPost
    ordering = '-pk' #postlist 데이터 랜더링 시 pk 순서대로 내림차순으로 랜더링된다.
    paginate_by = 10 #pagination을 할 때 한 페이지당 몇개의 데이터를 보이게 할 지 설정한다.
    def get_context_data(self, **kwargs):
        #다른 객체(데이터)들도 context에 넣어 보내고 싶다면 get_context_data 메서드를 구현하는 것으로 해결할 수 있다.
        #get_context_data는 dict 형식으로 반환되기 때문에 일반적인 context에는 PostList의 모든 데이터가 담겨져 있고
        #그 뒤에 key값과 value로 원하는 형식의 데이터를 넣으면 된다.
        context = super(BoardView,self).get_context_data()
        context['categories'] = AnimalCategory.objects.all()
        context['no_category_post_count'] = PetPost.objects.filter(category=None).count()
        return context
        
    
    
class PetPostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PetPost
    form_class = PostForm
    template_name = 'pet/pet_tip_post.html'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_authenticated

    def form_valid(self,form):
        current_user = self.request.user #사용자 정보 가져옴
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser): #인증된 사용자인지 체크
            form.instance.author = current_user #form 즉 post 제작 form의 소유자를 해당 사용자로 지정한다
            form.instance.post_category = PostCategory.objects.get(name='pet_post')
            #print(f"category - {form.data.get('category')}")
            if form.data.get('category') is "":
                form.instance.category = AnimalCategory.objects.get(name = "etc")
            #여기서 response는 변수이다. 입력한 form의 입력값들이 다 검증되었는지 저장한다
            response =  super(PetPostCreate, self).form_valid(form) #PostCreate를 이용해 form에 들어온 내용들이 모두 해당 데이터필드에 맞게 지정되면 저장한다.
            return response #DB에 저장
        
        else:
            return redirect('pet/board') #아니면 blog 페이지로 이동

class PetPostDetail(DetailView):
    #CBV 방식 view 작성에서 DetailView 상속 받기 때문에 template 파일 이름을 post_detail.html로 하면, template_name 변수는 생략해도 됨
    #규칙이기 때문에 규칙에 어긋하면 적용이 되지 않음.
    model = PetPost
    template_name = 'pet/board_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PetPostDetail,self).get_context_data()
        context['categories'] = AnimalCategory.objects.all()
        context['no_category_post_count'] = PetPost.objects.filter(category=None).count()
        return context
    
    
class PetPostUpdate(LoginRequiredMixin, UpdateView):
    model = PetPost
    form_class = PostForm
    # fields = ['title','hook_text','content','head_image','file_upload','category','tags']
    template_name = 'pet/post_update_form.html'
    #얘는 접속이 get인지 post인지 확인. get이면 포스트 update form 보여주고 post이면 form의 저장된 내용을 검증하고 통과되면 DB에 저장하는 역할
    #여기서는 만약 권한이 없으면 GET이든 POST이든 둘다 막아버림
    def dispatch(self, request, *args, **kwargs):
        #현재 접속한 user가 인증되었고 user가 해당 게시글의 소유자이면
        if request.user.is_authenticated and request.user == self.get_object().author: 
            return super(PetPostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self,form):
        current_user = self.request.user #사용자 정보 가져옴
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser): #인증된 사용자인지 체크
            form.instance.author = current_user #form 즉 post 제작 form의 소유자를 해당 사용자로 지정한다
            #여기서 response는 변수이다. 입력한 form의 입력값들이 다 검증되었는지 저장한다
            form.instance.post_category = PostCategory.objects.get(name='pet_post')
            #print(f"category - {form.data.get('category')}")
            if form.data.get('category') is "":
                form.instance.category = AnimalCategory.objects.get(name = "etc")
            response =  super(PetPostUpdate, self).form_valid(form) #PostCreate를 이용해 form에 들어온 내용들이 모두 해당 데이터필드에 맞게 지정되면 저장한다.
            return response #DB에 저장
        
        else:
            return redirect('pet/') #아니면 blog 페이지로 이동
        
    
#category끼리만 모아서 따로 페이지를 만들어주는 기능.
def pet_post_category_page(request, slug):
    print(slug)
    if slug == 'no_category':
        category = "미분류"
        post_list = PetPost.objects.filter(category=None)
    else:
        category = AnimalCategory.objects.get(slug=slug)
        post_list = PetPost.objects.filter(category=category).order_by("-created_at")
    
    return render(request, 'pet/boards.html',
                {
                    'slug' : slug,
                    'petpost_list': post_list, #해당 카테고리 정보들만 저장
                    'categories' : AnimalCategory.objects.all(), #전체 데이터 저장
                    #카테고리 없을 시 갯수 가져옴
                    'no_category_post_count' : PetPost.objects.filter(category=None).count(), #카테고리 없으면 갯수 지정
                    'category' : category #지정된 카테고리
                }
            )
    
class NewsList(ListView):
    model = NewsScrap
    template_name = 'pet/news_list.html'
    paginate_by = 10 # 페이지네이션 기능 활성화

class NewsDetail(DetailView):
    model = NewsScrap
    template_name = "pet/news_detail.html"

class AnimalView(ListView):
    model = Animals
    template_name = "pet/animal.html"
    paginate_by = 10
    ordering = '-pk'

class AnimalDetailView(DetailView):
    model = Animals
    template_name = "pet/animal_detail.html"
    context_object_name = 'animals'
    def get_context_data(self, **kwargs):
        context = super(AnimalDetailView,self).get_context_data()
        context['categories'] = SaveAnimalCategory.objects.all()
        return context

class HotelView(ListView):
    template_name = "pet/hotel.html"
    model = KoreaHotel
    paginate_by = 10
    ordering = '-kh_hotel_score'
    def get_context_data(self, **kwargs):
        #다른 객체(데이터)들도 context에 넣어 보내고 싶다면 get_context_data 메서드를 구현하는 것으로 해결할 수 있다.
        #get_context_data는 dict 형식으로 반환되기 때문에 일반적인 context에는 PostList의 모든 데이터가 담겨져 있고
        #그 뒤에 key값과 value로 원하는 형식의 데이터를 넣으면 된다.
        context = super(HotelView,self).get_context_data()
        context['categories'] = HotelCategory.objects.all()
        return context
    
def hotel_category_page(request, slug):
    print(slug)
    if slug == "전국":
        category = HotelCategory.objects.get(slug=slug)
        post_list = KoreaHotel.objects.all().order_by("-kh_hotel_score")
        all_post = "전국"
    elif slug == 'no_category':
        category = "미분류"
        post_list = SGIHotel.objects.filter(category=None)
        all_post = "전국아님"
    else:
        category = HotelCategory.objects.get(slug=slug)
        post_list = SGIHotel.objects.filter(category=category).order_by("-sgi_hotel_score")
        all_post = "전국아님"
    print(post_list)
    return render(request, 'pet/hotel_sgi.html',
                {
                    'slug' : slug,
                    'hotel_list': post_list, #해당 카테고리 정보들만 저장
                    'categories' : HotelCategory.objects.all(), #전체 데이터 저장
                    #카테고리 없을 시 갯수 가져옴
                    'no_category_post_count' : KoreaHotel.objects.filter(category=None).count(), #카테고리 없으면 갯수 지정
                    'category' : category, #지정된 카테고리
                    'all_post' : all_post
                }
            )
    

class HotelDetailView(DetailView):
    model = KoreaHotel
    template_name = "pet/hotel_detail.html"
    def get_context_data(self, **kwargs):
        context = super(HotelDetailView, self).get_context_data()
        context['categories'] = HotelCategory.objects.all()
        return context

class NewsView(TemplateView):
    template_name = "pet/news.html"


class RecommendPostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = RecommendPost
    form_class = RecommendPostForm
    template_name = 'pet/pet_tip_post.html'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_authenticated

    def form_valid(self,form):
        current_user = self.request.user #사용자 정보 가져옴
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser): #인증된 사용자인지 체크
            form.instance.author = current_user #form 즉 post 제작 form의 소유자를 해당 사용자로 지정한다
            form.instance.post_category = PostCategory.objects.get(name='recommend_post')
            if form.data.get('category') is "":
                form.instance.category = AnimalCategory.objects.get(name = "etc")
            #여기서 response는 변수이다. 입력한 form의 입력값들이 다 검증되었는지 저장한다
            response =  super(RecommendPostCreate, self).form_valid(form) #PostCreate를 이용해 form에 들어온 내용들이 모두 해당 데이터필드에 맞게 지정되면 저장한다.
            return response #DB에 저장
        
        else:
            return redirect('pet/recommend') #아니면 blog 페이지로 이동

class RecommendList(ListView):
    template_name = "pet/recommend.html"
    model = RecommendPost
    paginate_by = 10
    ordering = '-pk'
    def get_context_data(self, **kwargs):
        #다른 객체(데이터)들도 context에 넣어 보내고 싶다면 get_context_data 메서드를 구현하는 것으로 해결할 수 있다.
        #get_context_data는 dict 형식으로 반환되기 때문에 일반적인 context에는 PostList의 모든 데이터가 담겨져 있고
        #그 뒤에 key값과 value로 원하는 형식의 데이터를 넣으면 된다.
        context = super(RecommendList,self).get_context_data()
        context['categories'] = AnimalCategory.objects.all()
        context['no_category_post_count'] = RecommendPost.objects.filter(category=None).count()
        return context

class RecommendPostDetail(DetailView):
    #CBV 방식 view 작성에서 DetailView 상속 받기 때문에 template 파일 이름을 post_detail.html로 하면, template_name 변수는 생략해도 됨
    #규칙이기 때문에 규칙에 어긋하면 적용이 되지 않음.
    model = RecommendPost
    template_name = 'pet/recommend_detail.html'
    def get_context_data(self, **kwargs):
        context = super(RecommendPostDetail,self).get_context_data()
        context['categories'] = AnimalCategory.objects.all()
        context['no_category_post_count'] = RecommendPost.objects.filter(category=None).count()
        return context

class RecommendPostUpdate(LoginRequiredMixin, UpdateView):
    model = RecommendPost
    form_class = RecommendPostForm
    # fields = ['title','hook_text','content','head_image','file_upload','category','tags']
    template_name = 'pet/post_update_form.html'
    #얘는 접속이 get인지 post인지 확인. get이면 포스트 update form 보여주고 post이면 form의 저장된 내용을 검증하고 통과되면 DB에 저장하는 역할
    #여기서는 만약 권한이 없으면 GET이든 POST이든 둘다 막아버림
    def dispatch(self, request, *args, **kwargs):
        #현재 접속한 user가 인증되었고 user가 해당 게시글의 소유자이면
        if request.user.is_authenticated and request.user == self.get_object().author: 
            return super(RecommendPostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self,form):
        current_user = self.request.user #사용자 정보 가져옴
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser): #인증된 사용자인지 체크
            form.instance.author = current_user #form 즉 post 제작 form의 소유자를 해당 사용자로 지정한다
            #여기서 response는 변수이다. 입력한 form의 입력값들이 다 검증되었는지 저장한다
            form.instance.post_category = PostCategory.objects.get(name='recommend_post')
            if form.data.get('category') is "":
                form.instance.category = AnimalCategory.objects.get(name = "etc")
            response =  super(RecommendPostUpdate, self).form_valid(form) #PostCreate를 이용해 form에 들어온 내용들이 모두 해당 데이터필드에 맞게 지정되면 저장한다.
            return response #DB에 저장
        
        else:
            return redirect('pet/') #아니면 blog 페이지로 이동


def recommend_post_category_page(request, slug):
    if slug == 'no_category':
        category = "미분류"
        post_list = RecommendPost.objects.filter(category=None)
    else:
        category = AnimalCategory.objects.get(slug=slug)
        post_list = RecommendPost.objects.filter(category=category).order_by("-created_at")
    
    return render(request, 'pet/recommend.html',
                {
                    'slug' : slug,
                    'recommendpost_list': post_list, #해당 카테고리 정보들만 저장
                    'categories' : AnimalCategory.objects.all(), #전체 데이터 저장
                    #카테고리 없을 시 갯수 가져옴
                    'no_category_post_count' : RecommendPost.objects.filter(category=None).count(), #카테고리 없으면 갯수 지정
                    'category' : category #지정된 카테고리
                }
            )

class ShowoffPostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ShowoffPost
    form_class = ShowoffPostForm
    template_name = 'pet/pet_tip_post.html'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_authenticated

    def form_valid(self,form):
        current_user = self.request.user #사용자 정보 가져옴
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser): #인증된 사용자인지 체크
            form.instance.author = current_user #form 즉 post 제작 form의 소유자를 해당 사용자로 지정한다
            form.instance.post_category = PostCategory.objects.get(name='show_off_post')
            if form.data.get('category') is "":
                form.instance.category = AnimalCategory.objects.get(name = "etc")
            #여기서 response는 변수이다. 입력한 form의 입력값들이 다 검증되었는지 저장한다
            response =  super(ShowoffPostCreate, self).form_valid(form) #PostCreate를 이용해 form에 들어온 내용들이 모두 해당 데이터필드에 맞게 지정되면 저장한다.
            return response #DB에 저장
        
        else:
            return redirect('pet/mybaby') #아니면 blog 페이지로 이동

class ShowOffPostList(ListView):
    template_name = "pet/show_off.html"
    model = ShowoffPost
    paginate_by = 10
    ordering = '-pk'
    def get_context_data(self, **kwargs):
        #다른 객체(데이터)들도 context에 넣어 보내고 싶다면 get_context_data 메서드를 구현하는 것으로 해결할 수 있다.
        #get_context_data는 dict 형식으로 반환되기 때문에 일반적인 context에는 PostList의 모든 데이터가 담겨져 있고
        #그 뒤에 key값과 value로 원하는 형식의 데이터를 넣으면 된다.
        context = super(ShowOffPostList,self).get_context_data()
        context['categories'] = AnimalCategory.objects.all()
        context['no_category_post_count'] = ShowoffPost.objects.filter(category=None).count()
        return context

class ShowoffPostDetail(DetailView):
    #CBV 방식 view 작성에서 DetailView 상속 받기 때문에 template 파일 이름을 post_detail.html로 하면, template_name 변수는 생략해도 됨
    #규칙이기 때문에 규칙에 어긋하면 적용이 되지 않음.
    model = ShowoffPost
    template_name = 'pet/show_off_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ShowoffPostDetail,self).get_context_data()
        context['categories'] = AnimalCategory.objects.all()
        context['no_category_post_count'] = ShowoffPost.objects.filter(category=None).count()
        return context

class ShowOffPostUpdate(LoginRequiredMixin, UpdateView):
    model = ShowoffPost
    form_class = ShowoffPostForm
    # fields = ['title','hook_text','content','head_image','file_upload','category','tags']
    template_name = 'pet/post_update_form.html'
    #얘는 접속이 get인지 post인지 확인. get이면 포스트 update form 보여주고 post이면 form의 저장된 내용을 검증하고 통과되면 DB에 저장하는 역할
    #여기서는 만약 권한이 없으면 GET이든 POST이든 둘다 막아버림
    def dispatch(self, request, *args, **kwargs):
        #현재 접속한 user가 인증되었고 user가 해당 게시글의 소유자이면
        if request.user.is_authenticated and request.user == self.get_object().author: 
            return super(ShowOffPostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self,form):
        current_user = self.request.user #사용자 정보 가져옴
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser): #인증된 사용자인지 체크
            form.instance.author = current_user #form 즉 post 제작 form의 소유자를 해당 사용자로 지정한다
            #여기서 response는 변수이다. 입력한 form의 입력값들이 다 검증되었는지 저장한다
            form.instance.post_category = PostCategory.objects.get(name='show_off_post')
            if form.data.get('category') is "":
                form.instance.category = AnimalCategory.objects.get(name = "etc")
            response =  super(ShowOffPostUpdate, self).form_valid(form) #PostCreate를 이용해 form에 들어온 내용들이 모두 해당 데이터필드에 맞게 지정되면 저장한다.
            return response #DB에 저장
        
        else:
            return redirect('pet/') #아니면 blog 페이지로 이동
        
def show_off_post_category_page(request, slug):
    if slug == 'no_category':
        category = "미분류"
        post_list = ShowoffPost.objects.filter(category=None)
    else:
        category = AnimalCategory.objects.get(slug=slug)
        post_list = ShowoffPost.objects.filter(category=category).order_by('-created_at')
    
    return render(request, 'pet/show_off.html',
                {
                    'slug' : slug,
                    'showoffpost_list': post_list, #해당 카테고리 정보들만 저장
                    'categories' : AnimalCategory.objects.all(), #전체 데이터 저장
                    #카테고리 없을 시 갯수 가져옴
                    'no_category_post_count' : ShowoffPost.objects.filter(category=None).count(), #카테고리 없으면 갯수 지정
                    'category' : category #지정된 카테고리
                }
            )
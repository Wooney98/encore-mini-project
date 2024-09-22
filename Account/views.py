from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView
from Account.models import Account
from django.contrib.auth.hashers import check_password
from .forms import CheckPasswordForm
from django.contrib.auth import logout
from pet.models import PetPost, RecommendPost, ShowoffPost
class UserView(TemplateView):
    model = Account
    template_name = 'account/view.html'
    #print(f"Account : {Account}")

def get_user_write_post(request):
    print(request.user.uid)
    model = Account
    if PetPost.objects.count() != 0 or RecommendPost.object.count() != 0 or ShowoffPost.object.count() != 0:
        post_list1 = PetPost.objects.filter(author_id=request.user.uid).values_list().order_by('-created_at')[:3]
        post_list2 = RecommendPost.objects.filter(author_id=request.user.uid).values_list().order_by('-created_at')[:3]
        post_list3 = ShowoffPost.objects.filter(author_id=request.user.uid).values_list().order_by('-created_at')[:3]
        post_list = []
        for i in post_list1:
            post_list.append(i)
        for i in post_list2:
            post_list.append(i)
        for i in post_list3:
            post_list.append(i)
        content = {
            "write_post" : sorted(post_list, key = lambda x : x[3], reverse=True)[:5],
            "model" : model
        }
    else:
        content = {
            "write_post" : None,
            "model" : model
        }
    return render(request,"account/view.html" ,content)
    
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            context = {}
            return render(request, 'accounts/delete_success.html', context)
    
def userDelete(request):
	user = request.user
	user.delete()
	logout(request)
	context = {}
	return render(request, 'account/delete_user.html', context)
#회원가입을 위한 form 생성
#Django에 미리 정의된 form import 해서 사용
from django.contrib.auth.forms import UserCreationForm
#User는 Django가 제공하는 model DB
from django.contrib.auth.models import User
from django import forms #Django에서 제공하는 입력 form. Field를 사용할 때 사용
from django.contrib.auth import get_user_model
from Account.models import Account

#Django에 정의되어 있는 form 상속받아서 사용. 
class CreateUserForm(UserCreationForm):
    #email만 Field form으로 가져와서 사용. 나머지는 django의 forms를 사용한다.
    email = forms.EmailField(required=True, help_text="Required. please Add a valid email") #required는 필수로 넣어야 하는 필드로 지정한다.
    
    #연결 시킬 데이터 모델을 대입하면 된다. fields는 데이터 모델의 속성들을 의미한다.
    class Meta:
        model = Account #Django에서 제공하는 DB Model
        fields = ("email", "username", "password1", "password2") #password1은 password 입력, password2는 비밀번호 확인 차 재입력
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = "email을 ID로 사용합니다."
        self.fields['username'].widget.attrs['placeholder'] = "커뮤니티에서 사용될 nickname입니다."
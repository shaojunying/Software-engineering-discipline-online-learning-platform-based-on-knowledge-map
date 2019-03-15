from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

#用户只有在登录后才能看到一些内容
@login_required
def index(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 建立新数据对象但是不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存User对象
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
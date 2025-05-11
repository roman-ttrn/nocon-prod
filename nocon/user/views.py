from time import sleep

from django.contrib.auth.hashers import check_password
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .utils.email import *
from .forms import *

#@ratelimit(key='ip', rate='10/h', block=True)
#@ratelimit(key='post:email', rate='10/h', block=True)
@csrf_protect
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    username=username
                )
            except User.DoesNotExist:
                print('no such user')
                messages.error(request, 'There is no such user.')
                return redirect('login_user')

            if not check_password(password, user.password):
                print('wrong password')
                messages.error(request, 'Wrong password.')
                return redirect('login_user')

            # Сгенерировать 12-значный код
            code = generate_secure_token()

            # Сохраняем в сессии
            request.session['verify_user_id'] = user.id
            request.session['verify_code'] = code
            request.session.set_expiry(600)  # 10 минут на подтверждение

            # Отправка письма
            send_verification_code(email, code)

            return redirect('confirm_email')

        return render(request, 'user/login_user.html')
    
    return redirect('main')


#@ratelimit(key='ip', rate='10/h', block=True)  # Лимит по IP (шире)
#@ratelimit(key='post:code', rate='10/h', block=True)
@csrf_protect
def confirm_email(request):
    if not request.user.is_authenticated:

        if request.method == 'POST':
            input_code = request.POST.get('code')
            saved_code = request.session.get('verify_code')
            user_id = request.session.get('verify_user_id')

            if not saved_code or not user_id:
                messages.error(request, 'Session has expired. Try again.')
                return redirect('login_user')

            if input_code != saved_code:
                messages.error(request, 'Wrong verification code.')
                sleep(2)
                return redirect('confirm_email')

            user = User.objects.get(id=user_id)
            login(request, user)

            # Чистим сессию
            request.session.set_expiry(None)
            del request.session['verify_code']
            del request.session['verify_user_id']

            return redirect('main')

        return render(request, 'user/confirm_email.html')
    
    return redirect('main')

@csrf_protect
def logout_user(req):
    logout(req)
    return redirect('home')

@csrf_protect
def profile(req):
    if req.user.is_authenticated:
        return render(req, 'user/profile.html', {'profile': req.user.profile})
    return redirect('home')

@csrf_protect
def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile

        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')  # имя url для страницы профиля
        else:
            user_form = UserForm(instance=user)
            profile_form = ProfileForm(instance=profile)

        return render(request, 'user/edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })
    return redirect('home')

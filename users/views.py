from django.shortcuts import render, HttpResponseRedirect
from products.models import Basket
from django.contrib import auth, messages
from django.urls import reverse

from users.forms import UserLogin, UserRegistration, UserProfileForm
# Create your views here.
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLogin()
    context = {'form': form}
    return render(request, 'users/login.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistration(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistration()
    context = {'form': form}
    return render(request, 'users/registration.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserProfileForm(instance=request.user)

    baskets = Basket.objects.filter(user=request.user)

    context = {'title': 'Store - Профиль',
               'form': form,
               'baskets': baskets,
               }
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

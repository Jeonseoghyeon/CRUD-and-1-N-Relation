from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            auth_login(request,authenticated_user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/form.html',context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/form.html',context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('articles:index')

def profile(request,username):
    User = get_user_model()
    profile_user = User.objects.get(username=username)
    context = {
        'profile_user' : profile_user
    }
    return render(request,'accounts/profile.html',context)

def follow(request,username):
    User = get_user_model()
    me = request.user
    you = User.objects.get(username=username)

    if me == you:
        return redirect('accounts:profile',username)
    else:
        if me in you.followers.all():
            you.followers.remove(me)
        else:
            you.followers.add(me)

        return redirect('accounts:profile',username)
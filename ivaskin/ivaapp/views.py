from django.shortcuts import render, get_object_or_404, redirect
from .models import App, Forclient, Tag, Reviews
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import ReviewsForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def ind(request):
    props = App.objects.all()
    clients = Forclient.objects.all()
    tags = Tag.objects.all()
    reviews = Reviews.objects.all()
    context = {
        'props': props,
        'clients': clients,
        'tags': tags,
        'reviews': reviews,
    }
    return render(request, 'ivaapp/index.html', context) 


def desc(request, description_id):
    desc = get_object_or_404(Forclient, pk=description_id)
    # proc = Forclient.objects.all
    return render(request, 'ivaapp/description.html', {'desc': desc})

def signup_user(request):
    if request.method == 'GET':
        return render(request,'ivaapp/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'ivaapp/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'Такое имя уже существует'})
        else:
            return render(request, 'ivaapp/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def login_user(request):
    if request.method == 'GET':
        return render(request, 'ivaapp/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ivaapp/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('index')

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('index')  # или куда нужно
    else:
        form = ReviewsForm()
    return render(request, 'ivaapp/add_review.html', {'form': form})
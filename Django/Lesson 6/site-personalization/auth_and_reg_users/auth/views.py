from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(
        request,
        'home.html'
    )


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=my_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def auth_login(request):
    context = {}
    if request.POST:
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {
                'login_error': 'Данный пользователь не найден! Повторите попытку'
            }
    return render(
        request,
        'registration/login.html',
        context
    )


def logout_view(request):
    logout(request)
    return redirect('home')


def password_reset(request):
    return render(
        request,
        'registration/password_reset.html'
    )

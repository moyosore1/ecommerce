from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import guest
# Create your views here.


@guest
def register_user(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Successfully created account for ', username)
            return redirect('login')

    return render(request, 'user/register.html', {'form': form})


@guest
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully authenticated')
            return redirect('Store-home')
        else:
            messages.error(request, 'Incorrect credentials')
            return redirect('login')

    return render(request, 'user/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')
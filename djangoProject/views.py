from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout


def absolute_home(request):
    return render(request, "pre_user/home.html")


def login_view(request):
    message_error = None
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.data.get('username')
            password = form.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('home:show_stocks')
            else:
                message_error = "Oops! something went wrong"
    context = {
        'form': form,
        "message_error": message_error,
    }
    return render(request, 'user/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('absolute_home')

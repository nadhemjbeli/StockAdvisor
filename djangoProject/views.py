from django.shortcuts import render, redirect

from home.models import Profile
from home.decorators import unauthenticated_user
from .forms import NewUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from home.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@unauthenticated_user
def signup_view(request):
    message_error = None
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("home:show_stocks")

        else:
            # for msg in form.error_messages:
            #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
            message_error = 'Oops !! something went wrong'
            context = {
                "form": form, 'message_error': message_error
            }
            return render(request=request,
                          template_name="user/signup.html",

                          context=context,)
    form = NewUserForm
    context = {
        "form": form,
        'message_error': message_error
    }

    return render(request=request,
                  template_name="user/signup.html",
                  context={"form": form})

@unauthenticated_user
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

# def login_view(request):
#     message_error = None
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 if request.GET.get('next'):
#                     return redirect(request.GET.get('next'))
#                 else:
#                     return redirect('home:show_stocks')
#             else:
#                 message_error = "Oops! something went wrong"
#         else:
#             messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request=request,
#                   template_name="user/login.html",
#                   context={"form": form, 'message_error': message_error})

@unauthenticated_user
def absolute_home(request):
    return render(request, "pre_user/home.html")


@login_required
def profile(request):
    user = request.user
    print(user.first_name)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('absolute_home')

from django.shortcuts import render, redirect


from home.decorators import unauthenticated_user
from .forms import NewUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

@unauthenticated_user
def signup_view(request):
    message_error = None
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
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


def logout_view(request):
    logout(request)
    return redirect('absolute_home')

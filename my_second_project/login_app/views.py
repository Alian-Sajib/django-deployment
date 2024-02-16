from django.shortcuts import render
from login_app.forms import UserForm, UserInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from login_app.models import UserInfo


# Create your views here.
def index(request):
    dict = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        dict.update({"user_basic_info": user_basic_info, "user_more_info": user_more_info})
    return render(request, "login_app/index.html", context=dict)


def login_page(request):
    return render(request, "login_app/login_page.html", context={})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("login_app:index"))
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse("Invalid username and/or password")
    else:
        return HttpResponseRedirect(reverse("login_app:login_page"))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_app:login_page"))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user_info = user_info_form.save(
                commit=False
            )  # store the data but not save in the database
            user_info.user = user
            if "profile_pic" in request.FILES:
                user_info.profile_pic = request.FILES["profile_pic"]
            user_info.save()
            registered = True

    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    dict = {
        "user_form": user_form,
        "user_info_form": user_info_form,
        "registered": registered,
    }
    return render(request, "login_app/register.html", context=dict)

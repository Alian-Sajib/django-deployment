from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from App_login.forms import SignUpForm, UserProfileChange

# Create your views here.
def sign_up(request):
    registered = False
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
    dict = {"form": form, "registered": registered}
    return render(request, "App_login/signup.html", context=dict)


def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
    return render(request, "App_login/login.html", context={"form": form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def profile(request):
    return render(request, "App_login/profile.html",context={})

@login_required
def profile_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == "POST":
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
    return render(request, "App_login/profile_change.html", context={"form": form})

@login_required
def pass_change(request):
    changed = False
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            changed =True
    return render(request, "App_login/pass_change.html", context={"form": form,'changed':changed})

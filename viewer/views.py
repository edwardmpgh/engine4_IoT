from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

from engine4_iot import settings
from .forms import UserForm, ProfileForm


# Authentication Functions
def login_base(request):
    next = request.GET.get('next', '/viewer')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    print('here')
    return render(request, "registration/login.html", {'redirect_to': next})


def logout_base(request):
    logout(request)
    return HttpResponseRedirect(reverse('viewer_index'))


def signup(request):

    # set the user and profile forms
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)

    # check if the request is a post form the form
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            # save the user and profile information to the database
            user = user_form.save()
            # set the user password
            user.set_password(user.password)
            user.save()
            # save the user profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # login the user
            username = user_form.cleaned_data.get('username')
            pw = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pw)
            login(request, user)
            # send them to the home page
            return HttpResponseRedirect(reverse('viewer_index'))

    # render the signup page
    context = dict(
        user_form=user_form,
        profile_form=profile_form,
    )
    return render(request, 'registration/signup.html', context)


# User view functions
@login_required
def index(request):

    current_user = request.user

    return HttpResponse('Hi')


def change_setting(request):

    return HttpResponseRedirect(reverse('viewer_index'))

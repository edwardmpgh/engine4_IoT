from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from engine4_iot import settings
from .forms import UserForm, ProfileForm
from controller.models import Device, Sensor, SensorType, Event

# chart functions
def chart_co(data):
    pass


def chart_co2(data):
    pass


def chart_smoke(data):
    pass

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

    # check if the request is a post form the form
    if request.method == 'POST':
        if user_form.is_valid():
            # save the user and profile information to the database
            user = user_form.save()
            # set the user password
            user.set_password(user.password)
            user.save()

            # login the user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # send them to the home page
            return HttpResponseRedirect(reverse('viewer_index'))

    # render the signup page
    context = dict(
        user_form=user_form,
    )
    return render(request, 'registration/signup.html', context)


# User view functions
@login_required
def index(request):

    current_user = request.user

    context = dict(
        fullname=current_user.first_name + ' ' + current_user.last_name,
    )

    # get the user's list of sensors
    devices = Device.objects.filter(user=current_user, active=True, trash=False)
    sensors = Sensor.objects.filter(device__in=devices).order_by('device__location')

    context['sensors'] = sensors

    return render(request, 'viewer/index.html', context)


def change_setting(request):

    return HttpResponseRedirect(reverse('viewer_index'))

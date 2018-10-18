from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def index(request):

    current_user = request.user

    return HttpResponse('Hi')


def change_setting(request):

    return HttpResponseRedirect(reverse('viewer_index'))

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect


#@login_reqired
def index(request):

    current_user = request.user

    return HttpResponse('Hi')


def change_setting(request):

    return HttpResponseRedirect(reverse('viewer_index'))

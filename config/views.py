from django.http import HttpResponseNotFound
from django.shortcuts import render


def pageNotFound(request, exception):
    return HttpResponseNotFound(render(request, 'ads/404.html', status=404))
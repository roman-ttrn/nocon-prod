from django.shortcuts import render, redirect
from django.http import JsonResponse
from user.models import Post


def home(req):
    if not req.user.is_authenticated:
        return render(req, 'nocon/home.html')
    return redirect('main')

def health(req):
    return JsonResponse({'status': 'ok'})
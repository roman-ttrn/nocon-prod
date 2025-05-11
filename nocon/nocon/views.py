from django.shortcuts import render, redirect
def home(req):
    if not req.user.is_authenticated:
        return render(req, 'nocon/home.html')
    return redirect('main')

from django.shortcuts import render

def error_404(request):
    data = {}
    return render(request,'projectx_app/error_404.html', data)

def error_500(request):
    data = {}
    return render(request,'projectx_app/error_500.html', data)

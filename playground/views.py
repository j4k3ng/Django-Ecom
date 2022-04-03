from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    x = calculate()
    return render(request, 'hello.html', {'name': 'Mosh'})

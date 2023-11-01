from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def hello_world(request):
    x = 1
    y = 2
    # return HttpResponse("Hello World!")
    return render(request, "hello_world.html", {"name": "Janus"})

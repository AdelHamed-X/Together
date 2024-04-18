from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Message, Topic


def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, 'main/home.html', context)

def room(request):
    return

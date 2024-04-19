from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Message, Topic


def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    
    return render(request, 'main/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}

    return render(request, 'main/room.html', context)

def create_room(request):
    context = {}
    return render(request, 'main/room_form.html', context)

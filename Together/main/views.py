from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Message, Topic
from .room_form import RoomForm


def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    
    return render(request, 'main/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}

    return render(request, 'main/room.html', context)

def create_room(request):
    form = RoomForm()
    context = {'form': form}
    return render(request, 'main/room_form.html', context)

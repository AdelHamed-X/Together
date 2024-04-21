from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Message, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .room_form import RoomForm


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('Username').lower()
        password = request.POST.get('Password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, 'Username or Password is not correct')
        else:
            login(request, user)
            return redirect('home')
        
    context ={}
    return render(request, 'main/user_login.html', context)

def UserLogout(request):
    logout(request)
    return redirect('login')

def UserRegisteration(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'An error occurred during registeration!')

    context = {'form': form}
    return render(request, 'main/registeration_form.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q)
    )

    topics = Topic.objects.all()

    rooms_count = rooms.count()

    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count}
    
    return render(request, 'main/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}

    return render(request, 'main/room.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        room = RoomForm(request.POST)
        if room.is_valid():
            room.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'main/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'main/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room': room}
    return render(request, 'main/delete.html', context)


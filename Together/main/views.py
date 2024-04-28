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
from .room_form import UserForm


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
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    topics = Topic.objects.all()

    rooms_count = rooms.count()

    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count,
               "room_messages": room_messages}
    
    return render(request, 'main/home.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    persons = room.participants.all()

    # List all messages and order them
    room_messages = room.message_set.all().order_by(
        '-created_at'
    )
    # Get the message from the request, save it and show it
    if request.method == 'POST':
        message = Message.objects.create(
            room=room,
            body=request.POST.get('body'),
            user=request.user
        )
        message.save()
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'persons': persons
    }
    return render(request, 'main/room.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room_id = message.room.id
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'main/delete.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('desription')
        )
        return redirect('home')

    context = {
        'form': form,
        'topics': topics
    }
    return render(request, 'main/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You can only edit your rooms!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')
    context = {'form': form, 'room': room, 'topics': topics}
    return render(request, 'main/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'main/delete.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    rooms = user.room_set.all()
    context = {
        'user': user,
        'topics': topics,
        'room_messages': room_messages,
        'rooms': rooms
    }
    return render(request, 'main/profile.html', context)

@login_required(login_url='login')
def update_profile(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'main/update-user.html', context)

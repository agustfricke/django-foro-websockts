from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from . models import Room, Like, Message
from users.models import User
from . forms import RoomForm

@login_required
def like_room(request):
    user = request.user
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room_obj = Room.objects.get(id=room_id)

        if user in room_obj.like.all():
            room_obj.like.remove(user)
        else:
            room_obj.like.add(user)

        like, created = Like.objects.get_or_create(user=user, room_id=room_id)

        if not created:
            if like.value == 'Like':
                like.value == 'Unlike'
            else:
                like.value == 'Like'
        like.save()
    return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

@login_required
def search(request):
    query = request.GET.get('query', '')
    rooms = Room.objects.filter(name__icontains=query)
    return render(request, 'core/search.html', {'query':query, 'rooms':rooms})

@login_required
def delete_room(request, pk):
    room = Room.objects.get(pk=pk)
    if request.user == room.user:
        room.delete()
        messages.success(request, 'Room deleted!')
        return redirect('my_profile')
    else:
        messages.success(request, 'Ups... You dont own this room!')
        return redirect('home')

@login_required
def update_room(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(request.POST or None, instance=room)
    if request.user == room.user:
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated!')
            return redirect('my_profile')
    else:
        messages.success(request, 'Ups... You dont own this room!')
        return redirect('home')
    return render(request, 'core/update_room.html', {'form':form})

@login_required
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.user = request.user
            room.save()
            messages.success(request, 'Room Created!')
            return redirect('home')
        else:
            messages.success(request, 'Ups... there was a problem!')
    return render(request, 'core/create_room.html', {'form':form})

@login_required
def room(request, pk):
    room = Room.objects.get(pk=pk)
    m = Message.objects.filter(room=room)
    return render(request, 'core/room.html', {'room':room, 'm':m})

@login_required
def home(request):
    user = request.user
    users = User.objects.exclude(username=user.username)
    filtro = users[0:5]
    likes = user.like.all()

    rooms = Room.objects.all()

    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/home.html', {'page_obj':page_obj, 'filtro':filtro, 'likes':likes})
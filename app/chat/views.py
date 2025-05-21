from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Message

from .models import *

def chat(req, room_id):
    if not req.user.is_authenticated:
        return redirect('home')

    room = get_object_or_404(ChatRoom, id=room_id)
    msgs = Message.objects.filter(room=room).order_by('timestamp')[:100]

    # Проверка: является ли пользователь участником
    if req.user not in room.participants.all():
        return redirect('chat_list')  # или 403

    return render(req, 'chat/chat.html', {'room': room, 'msgs': msgs})

def load_messages(request, room_id):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 50))

    # Проверка: является ли пользователь участником
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.participants.all():
        return JsonResponse({'error': 'Access denied'}, status=403)

    messages = Message.objects.filter(room_id=room_id).order_by('-timestamp')[offset:offset+limit]
    serialized = [
        {
            'username': m.sender.username,
            'message': m.content,
            'timestamp': m.timestamp.strftime('%H:%M')
        }
        for m in messages
    ]
    return JsonResponse(serialized, safe=False)

def chat_list(req):
    if req.user.is_authenticated:
        chats = req.user.rooms.all()
        return render(req, 'chat/chat_list.html', {'chats': chats})
    return redirect('home')

def users_list(req):
    if not req.user.is_authenticated:
        return redirect('home')
    profiles = User.objects.exclude(id=req.user.id)
    return render(req, 'chat/users_list.html', {'profiles': profiles})

def add_chat(request):
    if not request.user.is_authenticated:
        return redirect('home')

    other_user_id = request.POST.get('user_id')
    if not other_user_id:
        return redirect('chat_list')

    # Получаем второго пользователя за один запрос
    other_user = get_object_or_404(User, id=other_user_id)
    
    # Проверяем существующий чат между пользователями
    existing_chat = ChatRoom.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).distinct().first()

    if existing_chat:
        return redirect('chat', room_id=existing_chat.id)

    # Создаем новый чат
    new_chat = ChatRoom.objects.create(
        name=f"{request.user.username[:15]} & {other_user.username[:15]}"
    )
    new_chat.participants.set([request.user, other_user])
    print('chat created!')

    return redirect('chat', room_id=new_chat.id)

import json
from django.http import JsonResponse
from .models import ChatMessage, Profile,Friend
from django.shortcuts import  render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import  logout
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .froms import ChatMessageForm
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, name=name, phone=phone)
        return redirect('login')
    
    return render(request, 'auth/register.html')

def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    return  render(request,'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user=request.user.profile
    friends = user.friends.all()  # Fetch all friends of this profile
    context = {'user': user, 'friends': friends}   
    return render(request,'mychat/index.html',context)

def details(request, pk):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user.profile
    profile = friend.profile  # Ensure this is a valid Profile instance

    chats = ChatMessage.objects.filter(
            (Q(msg_sender=user) & Q(msg_recevier=profile)) | (Q(msg_sender=profile) & Q(msg_recevier=user))
        ).order_by('id')
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_recevier=user, seen=False)
    rec_chats.update(seen=True)
    form = ChatMessageForm()

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_recevier = profile  # Make sure this is correctly set to the friend's profile
            chat_message.save()
            return redirect("details", pk=friend.profile.id)

    context = {"friend": friend, "form": form, "user": user, "profile": profile,"chats":chats,"num":rec_chats.count()}
    return render(request, 'mychat/chatpage.html', context)


def sentMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)

    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_recevier=profile, seen=False)

    # Return the new chat message body as JSON response
    return JsonResponse({"body": new_chat_message.body}, safe=False)

def receivedMessage(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)

    chats = ChatMessage.objects.filter(msg_sender=profile, msg_recevier=user, seen=False)
    messages = []

    for chat in chats:
        messages.append({
            "body": chat.body,
            "timestamp": chat.msg_sender_time.strftime('%I:%M %p')  # Format timestamp correctly
        })
        
        # Mark messages as seen
        chat.seen = True
        chat.save()
        
    return JsonResponse(messages, safe=False)

def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []

    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender=friend.profile, msg_recevier=user, seen=False)
        arr.append(chats.count())

    return JsonResponse(arr, safe=False)



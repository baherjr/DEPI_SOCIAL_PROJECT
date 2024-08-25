from django.shortcuts import render, redirect, get_object_or_404
from .models import LinkeeUser, Profile, Friend
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as logger, logout as outer
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Comment, Post
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger(request, user)
            print(request.user)
            return redirect("linkee")
        else:
            print("Username or Password does not match...")
            return redirect("login")

    return render(request, "sign_in.html")

def register(request):
    if request.method == "POST":
        fullname = request.POST["fullname"]
        username = request.POST["username"]
        email = request.POST["email"]
        birth_date = request.POST["birthdate"]
        pass1 = request.POST['password']
        pass2 = request.POST["password2"]
        if pass1 == pass2:
            if LinkeeUser.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken.')
                return redirect('register')
            elif LinkeeUser.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken.')
                return redirect('register')
            else:
                first_name, last_name = fullname.split(' ', 1) if ' ' in fullname else (fullname, '')
                user = LinkeeUser.objects.create_user(
                    username=username,
                    email=email,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=birth_date
                )
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                messages.success(request, 'Your account has been created successfully.')
                return redirect('login')
        else:
            messages.info(request, 'Passwords are not matching.')
            return redirect('register')
    else:
        return render(request, "register.html")

@login_required
def home_page(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {'user': user, 'profile':profile}
    return render(request, 'homeFeed.html', context)

@login_required
def logout(request):
    outer(request)
    return redirect('login')

@login_required
def profile_page(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {'user': user, 'profile':profile}
    return render(request, "profile.html",context=context)



@login_required
def friend_requests(request):
    user = request.user
    pending_requests = Friend.objects.filter(user=user, friend_status='Pending')
    friend_data = []
    for request in pending_requests:
        friend = request.friend
        friend_data.append({
            'profile_picture': friend.profile.profileimg.url,
            'first_name': friend.first_name,
            'last_name': friend.last_name,
            'username': friend.username,
            'friend_id': friend.id,
        })
    return JsonResponse({'pending_requests': friend_data})


@login_required
def handle_friend_request(request, request_friend_id, action):
    # Adjust the field name according to your model
    friend_request = get_object_or_404(Friend, friend_id=request_friend_id)
    if action == 'accept':
        friend_request.friend_status = 'Accepted'
        friend_request.save()
        # Create a reverse friend connection
        Friend.objects.create(
            user=friend_request.friend,
            friend=friend_request.user,
            friend_status='Accepted'
        )
    elif action == 'reject':
        friend_request.friend_status = 'Rejected'
        friend_request.save()
    return redirect('profile')

@login_required
def view_friends(request):
    user = request.user
    accepted_friend_requests = Friend.objects.filter(user=user, friend_status='Accepted')
    friend_data = []
    for request in accepted_friend_requests:
        friend = request.friend
        friend_data.append({
            'profile_picture': friend.profile.profileimg.url,
            'first_name': friend.first_name,
            'last_name': friend.last_name,
            'username': friend.username,
            'id': friend.username
        })
    return JsonResponse({'friends': friend_data})


@login_required
def get_friend_count(request):
    user = request.user
    accepted_friend_requests = Friend.objects.filter(user=user, friend_status='Accepted')
    friend_count = accepted_friend_requests.count()
    return JsonResponse({'friend_count': friend_count})




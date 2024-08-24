from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Post, Comment, Like
from user.models import LinkeeUser
from django.http import JsonResponse
from datetime import datetime, timezone, timedelta
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

@login_required
def view_my_posts(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')

    posts_data = []
    for post in posts:
        now = datetime.now(timezone.utc)
        time_difference = now - post.created_at

        if time_difference < timedelta(minutes=1):
            # If less than a minute, show "Just now"
            created_at_display = "Just now"
        elif time_difference < timedelta(hours=1):
            # If less than an hour, show minutes passed
            minutes_passed = int(time_difference.total_seconds() // 60)
            created_at_display = f"{minutes_passed} minutes ago"
        elif time_difference < timedelta(hours=24):
            # If less than 24 hours, show hours passed
            hours_passed = int(time_difference.total_seconds() // 3600)
            created_at_display = f"{hours_passed} hours ago"
        else:
            # If more than 24 hours, show days passed
            days_passed = time_difference.days
            created_at_display = f"{days_passed} days ago"
        user_liked = Like.objects.filter(post=post, user=user).exists()
        posts_data.append({
            'post_id': post.id,
            'post_content': post.postContent,
            'avatar_url': user.profile.profileimg.url if user.profile.profileimg else '/path/to/default/avatar.png',
            'username': user.get_full_name(),
            'handle': user.username,
            'like_count': Like.objects.filter(post=post).count(),
            'comment_count': Comment.objects.filter(post=post).count(),
            'created_at': created_at_display,
            'user_liked': user_liked,
        })

    return JsonResponse({'posts': posts_data})


@login_required
def view_feed(request):
    user = request.user

    # Step 1: Identify friends
    friends = LinkeeUser.objects.filter(
        Q(friend_requests_sent__friend_status='Accepted') |
        Q(friend_requests_received__friend_status='Accepted')
    )

    # Step 2: Retrieve posts from the user and their friends
    posts = Post.objects.filter(Q(user=user) | Q(user__in=friends)).order_by('-created_at')

    posts_data = []
    now = datetime.now(timezone.utc)  # Use Django's timezone-aware now

    for post in posts:
        time_difference = now - post.created_at

        # Step 3: Format the timestamp
        if time_difference < timedelta(minutes=1):
            created_at_display = "Just now"
        elif time_difference < timedelta(hours=1):
            minutes_passed = int(time_difference.total_seconds() // 60)
            created_at_display = f"{minutes_passed} minute{'s' if minutes_passed != 1 else ''} ago"
        elif time_difference < timedelta(hours=24):
            hours_passed = int(time_difference.total_seconds() // 3600)
            created_at_display = f"{hours_passed} hour{'s' if hours_passed != 1 else ''} ago"
        else:
            days_passed = time_difference.days
            created_at_display = f"{days_passed} day{'s' if days_passed != 1 else ''} ago"

        post_user = post.user
        profile = getattr(post_user, 'profile', None)  # Safely get the profile
        user_liked = Like.objects.filter(post=post, user=user).exists()
        # Step 4: Compile the post data
        posts_data.append({
            'post_id': post.id,
            'post_content': post.postContent,
            'avatar_url': profile.profileimg.url if profile and profile.profileimg else '/path/to/default/avatar.png',
            'username': post_user.get_full_name() or post_user.username,
            'handle': post_user.username,
            'like_count': Like.objects.filter(post=post).count(),
            'comment_count': Comment.objects.filter(post=post).count(),
            'created_at': created_at_display,
            'user_liked': user_liked,
        })

    # Step 5: Return the JSON response
    return JsonResponse({'posts': posts_data})

@login_required
@csrf_protect
def create_post(request):
    if request.method == 'POST':
        post_content = request.POST.get('postContent', '')
        if post_content:
            Post.objects.create(user=request.user, postContent=post_content)
    return redirect('linkee')


@login_required
def add_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    like_count = Like.objects.filter(post=post).count()
    return JsonResponse({
        'liked': liked,
        'like_count': like_count,
    })


@login_required
def add_comment(request, post_id):
    pass
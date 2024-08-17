from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login





def index(request):
    return render(request, 'accounts/index.html')

class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        users_list = [model_to_dict(user) for user in users]
        return JsonResponse(users_list, safe=False)

class UserDetailView(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            return JsonResponse(model_to_dict(user))
        except User.DoesNotExist:
            return HttpResponse(status=404)

class GroupListView(View):
    def get(self, request):
        groups = Group.objects.all()
        groups_list = [model_to_dict(group) for group in groups]
        return JsonResponse(groups_list, safe=False)

class GroupDetailView(View):
    def get(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
            return JsonResponse(model_to_dict(group))
        except Group.DoesNotExist:
            return HttpResponse(status=404)

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')

        # Search in users
        user_results = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

        # Search in groups
        group_results = Group.objects.filter(
            Q(name__icontains=query)
        )

        context = {
            'users': user_results,
            'groups': group_results,
            'query': query
        }

        return render(request, 'accounts/search_results.html', context)
    

class CreateUserView(View):
    def post(self, request):
        # Parse data from request
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        return JsonResponse({'message': 'User created successfully', 'user_id': user.id})


class LoginView(View):
    def post(self, request):
        # Parse data from request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'user_id': user.id})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
        


from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import UserProfile, Group

@require_http_methods(["GET"])
def user_list(request):
    Users = UserProfile.objects.all()
    data = [{"id": user.id, "username": user.username, "email": user.email} for user in Users]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def user_detail(request, pk):
    try:
        user = UserProfile.objects.get(pk=pk)
        data = {"id": user.id, "username": user.username, "email": user.email}
        return JsonResponse(data)
    except UserProfile.DoesNotExist:
        return HttpResponse(status=404)

@require_http_methods(["GET"])
def group_list(request):
    groups = Group.objects.all()
    data = [{"id": group.id, "name": group.name} for group in groups]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def group_detail(request, pk):
    try:
        group = Group.objects.get(pk=pk)
        data = {"id": group.id, "name": group.name}
        return JsonResponse(data)
    except Group.DoesNotExist:
        return HttpResponse(status=404)
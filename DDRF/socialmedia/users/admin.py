from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'Fname', 'Lname')
    search_fields = ('email', 'Fname', 'Lname')
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Note
from django.contrib.auth.admin import UserAdmin


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'owner')
    readonly_fields = ('id',)

admin.site.register(Note, NoteAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
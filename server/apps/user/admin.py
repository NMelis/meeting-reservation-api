from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from server.apps.user.models import User


@admin.register(User)
class UserCustomAdmin(UserAdmin):
    pass

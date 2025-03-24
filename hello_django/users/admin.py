from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, FriendRequest


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    change_form = CustomUserChangeForm
    model = CustomUser
    list_display = ("first_name", "last_name", "email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email",)


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['status', 'to_user', 'from_user']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
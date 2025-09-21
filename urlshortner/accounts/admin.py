from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP
from django.utils import timezone


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("phone", "username", "full_name", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "gender")
    search_fields = ("phone", "username", "full_name", "email")
    ordering = ("-id",)
    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("username", "full_name", "email", "bio", "age", "gender", "last_login")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "username", "age", "password1", "password2"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "created_at", "expires_at", "is_expired", "attempts")
    list_filter = ("created_at", "expires_at")
    search_fields = ("phone", "code")
    readonly_fields = ("created_at",)
    ordering = ("-id",)

    @admin.display(boolean=True, description="Expired?")
    def is_expired(self, obj: OTP):
        return timezone.now() > obj.expires_at

from django.contrib import admin
from django.utils import timezone
from .models import ShortLink

@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ("code", "owner", "original_url", "click_count", "is_active", "expires_at", "expired")
    list_filter = ("is_active", "created_at", "expires_at")
    search_fields = ("code", "original_url", "owner__phone", "owner__full_name")
    readonly_fields = ("created_at", "click_count")
    ordering = ("-id",)
    actions = ["expire_now"]

    @admin.display(boolean=True, description="Expired?")
    def expired(self, obj: ShortLink):
        return bool(obj.expires_at and timezone.now() > obj.expires_at)

    @admin.action(description="Expire selected links now")
    def expire_now(self, request, queryset):
        queryset.update(expires_at=timezone.now())
from django.db import models
from accounts.models import User
from django.utils import timezone
import string, secrets


CHARSET = string.ascii_letters + string.digits

class ShortLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='links')
    original_url = models.URLField()
    code = models.CharField(max_length=10, unique=True, db_index=True)
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["owner", "-id"]),
        ]

    def __str__(self):
        return f"{self.code} -> {self.original_url}"

    @staticmethod
    def generate_unique_code(length=6):
        charset = string.ascii_letters + string.digits
        while True:
            code = ''.join(secrets.choice(charset) for _ in range(length))
            if not ShortLink.objects.filter(code=code).exists():
                return code

    def is_expired(self):
        return bool(self.expires_at and timezone.now() > self.expires_at)
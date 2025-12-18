import hashlib
import secrets

from accounts.models import User
from django.db import models


class WearOSIntegration(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="wearos_integration"
    )
    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(24)[:32]

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def set_token(self, token: str):
        self.token_hash = self.hash_token(token)

    def check_token(self, token: str) -> bool:
        return self.token_hash == self.hash_token(token)

    def __str__(self):
        return f"WearOSIntegration({self.user.username})"

    class Meta:
        verbose_name = "WearOS連携"
        verbose_name_plural = "WearOS連携一覧"


class HeartRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="heartrates")
    bpm = models.PositiveIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.bpm} bpm @ {self.timestamp}"

    class Meta:
        verbose_name = "心拍数"
        verbose_name_plural = "心拍数一覧"

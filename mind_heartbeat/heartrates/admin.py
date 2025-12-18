from django.contrib import admin

from .models import HeartRate, WearOSIntegration


@admin.register(WearOSIntegration)
class WearOSIntegrationAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__username",)
    readonly_fields = ("user", "token_hash", "created_at", "updated_at")


@admin.register(HeartRate)
class HeartRateAdmin(admin.ModelAdmin):
    list_display = ("user", "bpm", "timestamp")
    search_fields = ("user__username",)

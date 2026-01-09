from django.urls import path

from .views import (
    CreateWearOSIntegrationView,
    DeleteWearOSIntegrationView,
    DetailWearOSIntegrationView,
    DetailWearOSIntegrationWithTokenView,
    HeartRateReceiveView,
)

app_name = "heartrates"
urlpatterns = [
    path(
        "integration/create/",
        CreateWearOSIntegrationView.as_view(),
        name="create-wearos-integration",
    ),
    path(
        "integration/detail/",
        DetailWearOSIntegrationView.as_view(),
        name="detail-wearos-integration",
    ),
    path(
        "integration/detail/<str:token>/",
        DetailWearOSIntegrationWithTokenView.as_view(),
        name="detail-wearos-integration-with-token",
    ),
    path(
        "integration/delete/",
        DeleteWearOSIntegrationView.as_view(),
        name="delete-wearos-integration",
    ),
    path(
        "api/heartrate/receive/",
        HeartRateReceiveView.as_view(),
        name="heartrate-receive",
    ),
]

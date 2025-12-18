from django.urls import path

from .views import HeartRateReceiveView, WearOSAuthView

urlpatterns = [
    path("api/wearos-auth/", WearOSAuthView.as_view(), name="wearos-auth"),
    path(
        "api/heartrate-receive/",
        HeartRateReceiveView.as_view(),
        name="heartrate-receive",
    ),
]

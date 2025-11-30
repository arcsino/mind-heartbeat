from django.urls import path

from .views import (
    FeelingCreateView,
    FeelingDeleteView,
    FeelingDetailView,
    FeelingGraphView,
    FeelingsListView,
    FeelingUpdateView,
    IndexView,
)

app_name = "feelings"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("feeling/list/", FeelingsListView.as_view(), name="list"),
    path("feeling/graph/", FeelingGraphView.as_view(), name="graph"),
    path("feeling/create/", FeelingCreateView.as_view(), name="create"),
    path("feeling/<uuid:pk>/", FeelingDetailView.as_view(), name="detail"),
    path("feeling/<uuid:pk>/update/", FeelingUpdateView.as_view(), name="update"),
    path("feeling/<uuid:pk>/delete/", FeelingDeleteView.as_view(), name="delete"),
]

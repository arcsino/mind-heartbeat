from django.urls import path

from .views import (
    DeleteUserView,
    LoginAPIView,
    LoginView,
    LogoutAPIView,
    LogoutView,
    NicknameUpdateView,
    PasswordChangeAPIView,
    PasswordChangeView,
    ProfileView,
    SignupView,
    UserDeleteAPIView,
    UserDetailAPIView,
    UserRegistrationAPIView,
    UserUpdateAPIView,
)

app_name = "accounts"
urlpatterns = [
    # page views
    # Any user can access.
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    # Authenticated users only can access.
    path("profile/", ProfileView.as_view(), name="profile"),
    path("nickname-update/", NicknameUpdateView.as_view(), name="nickname-update"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete/", DeleteUserView.as_view(), name="delete"),
    # API views
    # Any user can access.
    path(route="api/registration/", view=UserRegistrationAPIView.as_view()),
    path(route="api/login/", view=LoginAPIView.as_view()),
    # Authenticated users only can access.
    path(route="api/detail/", view=UserDetailAPIView.as_view()),
    path(route="api/update/", view=UserUpdateAPIView.as_view()),
    path(route="api/password-change/", view=PasswordChangeAPIView.as_view()),
    path(route="api/logout/", view=LogoutAPIView.as_view()),
    path(route="api/delete/", view=UserDeleteAPIView.as_view()),
]

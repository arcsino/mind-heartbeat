from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import LoginForm, NicknameUpdateForm, PasswordChangeForm, SignupForm
from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class SignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "アカウントを作成しました。")
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("feelings:index")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class NicknameUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/nickname_update.html"
    form_class = NicknameUpdateForm
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "ニックネームを変更しました。")
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        messages.success(self.request, "パスワードを変更しました。")
        return super().form_valid(form)


class LogoutView(View):
    template_name = "accounts/logout.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        messages.success(request, "ログアウトしました。")
        return redirect(reverse_lazy("accounts:login"))


class DeleteUserView(LoginRequiredMixin, View):
    template_name = "accounts/delete.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "アカウントを削除しました。")
        return redirect(reverse_lazy("feelings:index"))


class UserRegistrationAPIView(generics.CreateAPIView):
    """User registration view."""

    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                data={
                    "message": "ユーザ登録に成功しました。",
                    "user": UserRegistrationSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """User login view."""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            return Response(
                data={
                    "message": "ログインに成功しました。",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(generics.RetrieveAPIView):
    """User detail view."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            data={
                "message": "ユーザ情報の取得に成功しました。",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UserUpdateAPIView(generics.UpdateAPIView):
    """User update view."""

    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                data={
                    "message": "ユーザ情報の更新に成功しました。",
                    "user": UserUpdateSerializer(instance).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeAPIView(generics.UpdateAPIView):
    """User password change view."""

    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                data={"message": "パスワードの変更に成功しました。"},
                status=status.HTTP_200_OK,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """User logout view."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.session.clear()
        return Response(
            data={"message": "ログアウトに成功しました。"},
            status=status.HTTP_200_OK,
        )


class UserDeleteAPIView(generics.DestroyAPIView):
    """User delete view."""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={"message": "ユーザの削除に成功しました。"},
            status=status.HTTP_200_OK,
        )

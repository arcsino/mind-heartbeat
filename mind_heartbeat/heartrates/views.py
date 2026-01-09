from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import HeartRate, WearOSIntegration
from .serializers import HeartRateSerializer


def get_user_integration(user):
    """指定ユーザーのWearOSIntegrationを1件取得"""
    return WearOSIntegration.objects.filter(user=user).first()


class CreateWearOSIntegrationView(CreateView):
    """WearOS連携作成ビュー。作成時のみトークン付きでリダイレクト。"""

    model = WearOSIntegration
    template_name = "heartrates/create-wearos-integration.html"
    fields = []

    def get(self, request, *args, **kwargs):
        if get_user_integration(request.user):
            return redirect("heartrates:detail-wearos-integration")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        token = getattr(self, "_created_token", None)
        if token:
            return reverse_lazy(
                "heartrates:detail-wearos-integration-with-token",
                kwargs={"token": token},
            )
        return reverse_lazy("heartrates:detail-wearos-integration")

    def form_valid(self, form):
        form.instance.user = self.request.user
        token = WearOSIntegration.generate_token()
        form.instance.set_token(token)
        self._created_token = token
        return super().form_valid(form)


class DetailWearOSIntegrationView(DetailView):
    """WearOS連携詳細ビュー（トークン非表示）"""

    model = WearOSIntegration
    template_name = "heartrates/detail-wearos-integration.html"

    def get_object(self, queryset=None):
        return get_user_integration(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_token"] = False
        return context


class DetailWearOSIntegrationWithTokenView(DetailView):
    """WearOS連携詳細ビュー（トークン表示）"""

    model = WearOSIntegration
    template_name = "heartrates/detail-wearos-integration.html"

    def get_object(self, queryset=None):
        return get_user_integration(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.kwargs.get("token")
        context["show_token"] = bool(token)
        context["token"] = token
        return context


class DeleteWearOSIntegrationView(LoginRequiredMixin, DeleteView):
    model = WearOSIntegration
    template_name = "heartrates/delete-wearos-integration.html"
    success_url = reverse_lazy("heartrates:create-wearos-integration")

    def get_object(self, queryset=None):
        # ログインユーザーの連携のみ削除可能
        return WearOSIntegration.objects.filter(user=self.request.user).first()


class HeartRateReceiveView(GenericAPIView):
    """WearOSデバイスから心拍数データを受信するAPIビュー（トークン認証）"""

    serializer_class = HeartRateSerializer

    def post(self, request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return Response(
                {"error": "認証トークンが必要です。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token = token.replace("Bearer ", "")
        try:
            integration = WearOSIntegration.objects.get(
                token_hash=WearOSIntegration.hash_token(token)
            )
            user = integration.user
            if not integration.is_connected:
                integration.is_connected = True
                integration.save()
        except WearOSIntegration.DoesNotExist:
            return Response(
                {"error": "無効なトークンです。"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bpm = serializer.validated_data["bpm"]
            timestamp = serializer.validated_data["timestamp"]
            HeartRate.objects.create(user=user, bpm=bpm, timestamp=timestamp)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

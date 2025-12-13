from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

User = get_user_model()


class SignupForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
            }
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
            }
        )


class NicknameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("nickname",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nickname"].widget.attrs.update(
            {
                "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
            }
        )


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
                }
            )

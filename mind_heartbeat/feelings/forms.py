from django import forms

from .models import Feeling


class FeelingForm(forms.ModelForm):
    class Meta:
        model = Feeling
        fields = ("stamp", "comment", "felt_at")
        widgets = {
            "felt_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stamp"].widget.attrs.update(
            {
                "class": "form-select form-control",
            }
        )
        self.fields["comment"].widget.attrs.update(
            {
                "class": "form-control",
                "rows": 5,
            }
        )
        self.fields["comment"].required = False

from django import forms

from .models import Feeling


class FeelingForm(forms.ModelForm):
    class Meta:
        model = Feeling
        fields = ("stamp", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stamp"].widget.attrs.update(
            {
                "class": "form-control form-select block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition"
            }
        )
        self.fields["comment"].widget.attrs.update(
            {
                "class": "form-control block w-full rounded-lg border border-gray-300 shadow-sm focus:ring-blue-400 focus:border-blue-400 transition",
                "rows": 5,
            }
        )
        self.fields["comment"].required = False

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import BooleanField, ModelForm

from ads.models import Ad, ExchangeProposal


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class CustomRegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]


class CustomLoginForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        fields = ("username", "password")


class AdForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Ad
        exclude = ("id", "user", "created_at")


class ExchangeProposalForm(StyleFormMixin, ModelForm):
    class Meta:
        model = ExchangeProposal
        exclude = ("id", "created_at", "status")

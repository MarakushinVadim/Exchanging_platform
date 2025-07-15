from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import BooleanField, ModelForm
# from django.forms.utils import flatatt
# from django.utils.html import format_html

from ads.models import Ad, ExchangeProposal


# class Tags(forms.TextInput):
#     input_type = 'text'
#     def render(self, name, value, attrs=None):
#         attrs = dict(self.attrs, **attrs) if attrs else self.attrs
#         final_attrs = dict(attrs, type=self.input_type, name=name)
#         return format_html('input {} >', flatatt(final_attrs))
#
#     class Media:
#         css = {
#             'all': ('sstyle.css',)
#         }


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        if user:
            self.fields["ad_sender"].queryset = Ad.objects.filter(user=user)
            self.fields["ad_receiver"].queryset = Ad.objects.exclude(user=user)

class ExchangeProposalUpdateForm(ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ("status", )
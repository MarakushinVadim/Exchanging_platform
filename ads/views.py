from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseNotFound
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)

from ads.forms import (
    AdForm,
    CustomRegistrationForm,
    CustomLoginForm,
    ExchangeProposalForm,
)
from ads.models import Ad, ExchangeProposal
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse_lazy




class OwnerMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.ad = get_object_or_404(Ad, pk=kwargs["pk"])
        except Ad.DoesNotExist:
            messages.error(request, "Объявление не найдено")
            return redirect("ads:ad_list")

        if self.ad.user != request.user:
            messages.error(request, "У вас нет прав на редактирование этого объявления")
            return redirect("ads:ad_list")

        return super().dispatch(request, *args, **kwargs)


class BaseView(TemplateView):
    template_name = "ads/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_authenticated"] = self.request.user.is_authenticated
        return context


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = CustomRegistrationForm
    template_name = "ads/register.html"
    success_url = reverse_lazy("ads:home")
    success_message = "Регистрация прошла успешно!"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Автоматически логиним пользователя
        return response


class CustomLoginView(LoginView):
    template_name = "ads/login.html"
    success_url = reverse_lazy("ads:home")
    success_message = "Вход выполнен"
    form_class = CustomLoginForm

    def get_success_url(self):
        return self.success_url


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy("ads:home")

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdListView(ListView):
    model = Ad


class AdUpdateView(OwnerMixin, UpdateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy("ads:home")


class AdDetailView(LoginRequiredMixin, DetailView):
    model = Ad


class AdDeleteView(OwnerMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy("ads:home")

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)

        except self.model.DoesNotExist:
            messages.error(request, "Объект не найден")
            return redirect(self.success_url)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Объявление успешно удалено")
        return response


class ExchangeProposalListView(ListView):
    model = ExchangeProposal


class ExchangeProposalCreateView(CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    success_url = reverse_lazy("ads:home")


class ExchangeProposalDetailView(DetailView):
    model = ExchangeProposal


class ExchangeProposalUpdateView(UpdateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    success_url = reverse_lazy("ads:home")


class ExchangeProposalDeleteView(DeleteView):
    model = ExchangeProposal
    success_url = reverse_lazy("ads:home")

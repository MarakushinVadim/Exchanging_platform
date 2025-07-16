from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseForbidden
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.db.models import Q

from ads.forms import (
    AdForm,
    CustomRegistrationForm,
    CustomLoginForm,
    ExchangeProposalForm, ExchangeProposalUpdateForm,
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
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        condition = self.request.GET.get("condition")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Ad.objects.order_by("category").values_list("category", flat=True).distinct()

        context["selected_category"] = self.request.GET.get('category')
        context['selected_status'] = self.request.GET.get('status')
        page = self.request.GET.get('page')
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        try:
            ads = paginator.page(page)
        except PageNotAnInteger:
            ads = paginator.page(1)
        except EmptyPage:
            ads = paginator.page(paginator.num_pages)

        context['ads'] = ads
        context['paginator'] = paginator

        return context

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

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        ads_user = ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user))
        context_data["object_list"] = ads_user
        return context_data


class ExchangeProposalCreateView(CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    success_url = reverse_lazy("ads:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ExchangeProposalDetailView(DetailView):
    model = ExchangeProposal


class ExchangeProposalUpdateView(UpdateView):
    model = ExchangeProposal
    form_class = ExchangeProposalUpdateForm
    success_url = reverse_lazy("ads:home")

    def dispatch(self, request, *args, **kwargs):
        offer = self.get_object()
        if offer.ad_receiver.user == request.user or offer.ad_sender.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Доступ запрещен")

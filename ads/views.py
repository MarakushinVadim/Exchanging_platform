from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from ads.forms import AdForm, CustomRegistrationForm, CustomLoginForm
from ads.models import Ad
from django.contrib.auth.views import LoginView


class BaseView(TemplateView):
    template_name = "ads/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class RegisterView(SuccessMessageMixin, CreateView):
    form_class = CustomRegistrationForm
    template_name = 'ads/register.html'
    success_url = reverse_lazy('ads:home')
    success_message = 'Регистрация прошла успешно!'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Автоматически логиним пользователя
        return response

class CustomLoginView(LoginView):
    template_name = 'ads/login.html'
    success_url = reverse_lazy('ads:home')
    success_message = 'Вход выполнен'
    form_class = CustomLoginForm

    def get_success_url(self):
        return self.success_url


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('ads:home')


    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdListView(ListView):
    model = Ad
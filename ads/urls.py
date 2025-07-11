from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from ads.apps import AdsConfig
from ads.views import BaseView, AdCreateView, RegisterView, CustomLoginView

app_name = AdsConfig.name

urlpatterns = [
    path('', BaseView.as_view(), name='home', kwargs={'template_name': 'base.html'}),
    path('ad_create/', AdCreateView.as_view(), name='ad_create'),

    path('register/', RegisterView.as_view(template_name='ads/register.html'), name='register'),
    path("login/", CustomLoginView.as_view(template_name='ads/login.html'), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy('ads:login')), name="logout")
]
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from ads.apps import AdsConfig
from ads.views import (
    BaseView,
    AdCreateView,
    RegisterView,
    CustomLoginView,
    AdListView,
    AdUpdateView,
    AdDetailView,
    ExchangeProposalCreateView,
    ExchangeProposalListView,
    ExchangeProposalDetailView,
    AdDeleteView, accept_proposal, reject_proposal,
)

app_name = AdsConfig.name

urlpatterns = [
    path("", BaseView.as_view(), name="home", kwargs={"template_name": "base.html"}),
    path("ad_create/", AdCreateView.as_view(), name="ad_create"),
    path(
        "register/",
        RegisterView.as_view(template_name="ads/register.html"),
        name="register",
    ),
    path(
        "login/", CustomLoginView.as_view(template_name="ads/login.html"), name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("ads:login")),
        name="logout",
    ),
    path("ad_list/", AdListView.as_view(), name="ad_list"),
    path("<int:pk>/ad_update", AdUpdateView.as_view(), name="ad_update"),
    path("ad_detail/<int:pk>", AdDetailView.as_view(), name="ad_detail"),
    path("<int:pk>/ad_delete", AdDeleteView.as_view(), name="ad_delete"),
    path(
        "exchange_proposal_create/<int:pk>",
        ExchangeProposalCreateView.as_view(),
        name="exchange_proposal_create",
    ),
    path(
        "exchange_proposal_list",
        ExchangeProposalListView.as_view(),
        name="exchange_proposal_list",
    ),
    path(
        "exchange_proposal_detail/<int:pk>",
        ExchangeProposalDetailView.as_view(),
        name="exchange_proposal_detail",
    ),
    path('proposal/<int:proposal_id>/accept/', accept_proposal, name='accept_proposal'),
    path('proposal/<int:proposal_id>/reject/', reject_proposal, name='reject_proposal'),
]

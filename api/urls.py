from django.urls import path

from . import views

from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"

urlpatterns = [
    path("login/", views.SolanaAuthView.as_view()),
    path("refresh_token/", TokenRefreshView.as_view()),
    path("ping/", views.PingView.as_view()),
    path("validate_key/", views.ValidateKeyView.as_view()),
    path("check_nft/", views.CheckNftView.as_view()),
]
from django.urls import path

from . import views


app_name = "api"

urlpatterns = [
    path("modules/", views.ListModules.as_view()),
    path('user/', views.DetailUser.as_view()),
    path("news/", views.ListNews.as_view()),
    path("updates/", views.ListUpdates.as_view()),
    path("login/", views.SolanaAuthView.as_view()),
    path("ping/", views.PingView.as_view()),
    path("validate_key/", views.ValidateKeyView.as_view()),
    path("check_nft/", views.CheckNftView.as_view()),
    path("check_transaction/", views.CheckTransactionView.as_view())
]
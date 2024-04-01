from django.urls import path

from . import views


app_name = "api"

urlpatterns = [
    path("modules/", views.ListModules.as_view()),
    path('user/', views.DetailUser.as_view()),
    path("news/", views.ListNews.as_view()),
    path("updates/", views.ListUpdates.as_view()),
    path("login/", views.solana_auth),
    path("ping/", views.ping),
    path("confirm_transaction/", views.check_transaction_commitment),
    path("validate_key/", views.validate_key)
]
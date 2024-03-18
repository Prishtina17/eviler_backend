from django.urls import path

from . import views


app_name = "api"

urlpatterns = [
    path("modules/", views.ListModules.as_view()),
    path('user/<user_id>', views.get_user_data),
    path("news/", views.ListNews.as_view()),
    path("updates/", views.ListUpdates.as_view()),
    path("login/", views.solana_auth),
    path("login/redirect/", views.discord_login_redirect),
    path("ping/", views.ping)
]
from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("modules/", views.get_modules),
    path('user/<user_id>', views.get_user_data),
    path("news/<current_last_new_id>", views.get_next_news),
    path("updates/", views.get_last_update),
    path("login/", views.discord_login),
    path("login/redirect/", views.discord_login_redirect)


]
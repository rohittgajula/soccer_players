from django.urls import path
from .views import LoginView, user_details, register_user, toggle_favorite, list_favorite


urlpatterns = [
  path("", user_details, name='user-detail'),
  path("register/", register_user, name='register-user'),
  path("login/", LoginView.as_view({'post': 'create'}), name='login'),

  path("<uuid:public_id>/toggle_favorite/", toggle_favorite, name='toggil_favorite'),
  path("<uuid:public_id>/list_favorite/", list_favorite, name='list_favorite'),
]
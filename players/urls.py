from django.urls import path
from . import views


urlpatterns = [
  path("players/", views.player_list, name='players-list'),

  # for locust
  path("player-ids/", views.player_ids, name='player_ids'),
]


# 1 task - count all player objects - count_players
# 2 task - update player db - update_players_from_json

from .models import Player
from celery import shared_task
from datetime import datetime
import json
import os
from django.conf import settings
from django.db import transaction
import logging

@shared_task
def count_players():
  count = Player.objects.count()
  return f"Number of players : {count}"

# converting datefield into string
def parse_data(date_str):
  if date_str:
    try:
      return datetime.strptime(date_str, "%b %d, %Y")
    except:
      return None
  else:
    None


@shared_task
def update_players_from_json():
    json_file_path = os.path.join(settings.BASE_DIR, 'player_data.json')

    try:
      with open(json_file_path, "r") as fp:
        player_data = json.load(fp)

      with transaction.atomic():
    
        for player in player_data:
          player['date_of_birth'] = parse_data(player.get("date_of_birth"))
          player['contract_expires'] = parse_data(player.get("contract_expires"))
          player['joined_date'] = parse_data(player.get("joined_date"))
          Player.objects.update_or_create(
            id = player['id'],
            defaults=player
          )
      return "Sucess : Player object updated."
    except Exception as e:
      return f"Error updating players : {e}"
      

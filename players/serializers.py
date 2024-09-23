

from rest_framework import serializers
from .models import Player


class PlayersSerializer(serializers.ModelSerializer):

  class Meta:
    model = Player
    fields = ['id', 'name', 'age', 'market_value', 'caps', 'main_position', 'citizenship', 'international_goals']



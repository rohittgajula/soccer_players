from django.db import models

class Player(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=250)
  age = models.IntegerField(null=True)
  jersey_number = models.IntegerField(null=True)
  place_of_birth = models.CharField(max_length=250, null=True)
  place_of_birth_title = models.CharField(max_length=250, null=True)
  place_of_birth_flag = models.URLField(null=True)
  date_of_birth = models.DateField(null=True)
  height = models.FloatField(null=True)
  foot = models.CharField(max_length=150, null=True)
  citizenship = models.JSONField(null=True)
  citizenship_flag = models.JSONField(null=True)
  headshot = models.URLField(null=True)
  club = models.CharField(max_length=150)
  club_logo = models.URLField(null=True, max_length=250)
  main_position = models.CharField(null=True, max_length=250)
  other_positions = models.JSONField(null=True)
  national_team = models.CharField(max_length=250, null=True)
  national_team_flag = models.URLField(null=True)
  caps = models.IntegerField(null=True)
  international_goals = models.IntegerField(null=True)
  market_value = models.IntegerField(null=True)
  league_name = models.CharField(max_length=250, null=True)
  league_level = models.CharField(max_length=250, null=True)
  league_logo = models.URLField(null=True, max_length=250)
  joined_date = models.DateField(null=True)
  contract_expires = models.DateField(null=True)
  agency_info = models.JSONField(null=True)
  club_stats = models.JSONField(null=True)
  national_team_stats = models.JSONField(null=True)
  current_season_stats = models.JSONField(null=True)


  class Meta:
    ordering = [
      models.F("market_value").desc(nulls_last=True),         # making null values go bottom
      models.F("caps").desc(nulls_last=True)
    ]
    indexes = [
      models.Index(fields=['id', 'market_value'])
    ]

  def __str__(self):
    return f'{self.name} - {self.id}'



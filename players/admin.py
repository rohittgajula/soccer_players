from django.contrib import admin
from .models import Player

#admin.site.register(Player)
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

  def formatted_market_value(self, obj):
    if obj.market_value is not None:
      return f'{obj.market_value:,}'
    else:
      "N/A"

  formatted_market_value.short_description = "Market Value"

  list_display = ['id', 'name', 'age', 'caps', 'formatted_market_value', 'league_name', 'league_level']
  search_fields = ['id', 'name']
  list_filter = ['league_name']

  # for player individual detail modfication.
  fieldsets = (
        (
            'Personal Info',{
                'fields': ("name","date_of_birth","place_of_birth", "citizenship","age", "place_of_birth_flag")
            }
        ),
        
        (
            'Professional Info', {
                'fields': ("club","national_team","caps", "international_goals","market_value", "main_position")
            }
        ),
        
        (
            'Additional Info', {
                'fields': ("agency_info","club_stats","national_team_stats", "current_season_stats")
            } 
        )
        
    )

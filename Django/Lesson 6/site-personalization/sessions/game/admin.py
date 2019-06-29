from django.contrib import admin

from .models import Player, PlayerGameInfo, Game

admin.site.register(PlayerGameInfo)
admin.site.register(Player)
admin.site.register(Game)
__author__ = 'leif'

from django.contrib import admin
from game_models import Achievement, Category, CurrentGame, Page
from game_models import UserProfile, HighScore, PlayerAchievement, Level

admin.site.register(Achievement)
admin.site.register(Category)
admin.site.register(CurrentGame)
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(HighScore)
admin.site.register(PlayerAchievement)
admin.site.register(Level)
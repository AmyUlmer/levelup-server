from django.db import models


class Game(models.Model):
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    min_age = models.IntegerField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
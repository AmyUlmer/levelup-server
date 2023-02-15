from django.db import models


class Game(models.Model):
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    estimated_time = models.DecimalField(max_digits=2, decimal_places=1)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
from django.db import models


class Event(models.Model):
    organizing_gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    date_of_event = models.DateField()
    start_time = models.TimeField()
    attendees = models.ManyToManyField("Gamer", through="attendee")
    

from django.db import models


class Event(models.Model):
    organizing_gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    date_of_event = models.DateField()
    start_time = models.TimeField()
    attendees = models.ManyToManyField("Gamer", through="EventGamer",related_name="event_gamer")
    
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

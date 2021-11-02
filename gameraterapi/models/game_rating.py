from django.db import models
from django.db.models.deletion import CASCADE

class GameRating(models.Model):
    game = models.ForeignKey("Game", on_delete=CASCADE)
    rater = models.ForeignKey("Rater", on_delete=CASCADE)
    rating = models.FloatField()
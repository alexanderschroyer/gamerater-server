from django.db import models

class Picture(models.Model):
    """picture model"""
    rater = models.ForeignKey("Rater", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    image = models.ImageField()
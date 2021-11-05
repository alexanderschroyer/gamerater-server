from django.db import models

class Game(models.Model):
    """game model"""
    rater = models.ForeignKey("Rater", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time_to_play = models.CharField(max_length=50)
    age_recommendation = models.IntegerField()
    created_on = models.DateField()

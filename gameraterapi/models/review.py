from django.db import models

class Review(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    rater = models.ForeignKey("Rater", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateField()
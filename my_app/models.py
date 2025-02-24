from django.db import models

# Create your models here.


class Workout(models.Model):
    exercise = models.CharField(max_length=100)  # e.g., "Running"
    duration = models.IntegerField()             # e.g., 30 (minutes)
    date = models.DateField(auto_now_add=True)   # Today’s date

    def __str__(self):
        return f"{self.exercise} ({self.duration} mins)"
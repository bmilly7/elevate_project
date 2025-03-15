from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #link to user
    exercise = models.CharField(max_length=100)  # e.g., "Running"
    duration = models.IntegerField()             # e.g., 30 (minutes)
    date = models.DateField(auto_now_add=True)   # Today’s date

    def __str__(self):
        return f"{self.exercise} ({self.duration} mins) by {self.user.username}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the logged-in user
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    height = models.FloatField(null=True, blank=True)  # In inches or cm, your choice
    weight = models.FloatField(null=True, blank=True)  # In lbs or kg
    birthday = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
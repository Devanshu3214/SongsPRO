from django.db import models
from django.utils import timezone

class Data(models.Model): # Corrected the class name to start with uppercase and inherit from models.Model
    song = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(default=0000, blank=True)  # Corrected the default value to an integer
    artist = models.CharField(max_length=40, blank=True)
    genre = models.CharField(max_length=40, blank=True)
    rating = models.IntegerField(default=0)  # Corrected the default value to an integer
    created_by = models.CharField(max_length=40, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)
    export_to_csv = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.song
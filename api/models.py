from django.db import models

class ShortURL(models.Model):
    url = models.URLField(max_length=1000)
    short_url = models.CharField(max_length=100, unique=True)
    hit_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.short_url} >> {self.url}"


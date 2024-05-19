from django.db import models


class History(models.Model):
    text = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=12)
    bg_color = models.CharField(max_length=12)
    video_len = models.FloatField()
    add_time = models.DateTimeField(auto_now_add=True)


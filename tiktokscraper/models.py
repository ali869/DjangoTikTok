from django.db import models


# Create your models here.


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=256)
    is_saved = models.BooleanField(default=False)
    is_valid_hashtag = models.BooleanField(default=False)

    def __str__(self):
        return self.hashtag_name


class StatsData(models.Model):
    hashtag_name = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='hashtag')
    hashtag_id = models.IntegerField()
    view_count = models.IntegerField()
    video_count = models.IntegerField()
    is_commerce = models.BooleanField(null=True, blank=True)

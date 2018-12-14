import datetime
from django.db import models
from django.utils import timezone


class Post(models.Model):
    subject = models.CharField(max_length=255, unique=True)
    post_age = models.DurationField(verbose_name='post age', default=datetime.timedelta)
    created_at = models.DateTimeField(verbose_name='created at')
    modified_at = models.DateTimeField(verbose_name='modified at')
    hacker_news_url = models.URLField(verbose_name="hacker news url", name="hacker_news_url")
    upvotes = models.IntegerField(verbose_name="number of upvotes")
    comments = models.IntegerField(verbose_name="number of comments")
    is_read = models.BooleanField(verbose_name='is read', default=False)
    is_deleted = models.BooleanField(verbose_name='is deleted', default=False)

    def save(self, *args, **kwargs):
        """
        Overriding save to avoid created_at being updated again and again
        """
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Post, self).save(*args, **kwargs)

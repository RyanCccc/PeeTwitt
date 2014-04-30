from django.db import models
from pee_user.models import PeeUser
from django.utils import formats


class ReplyManager(models.Manager):
    def new_reply(
        self,
        author,
        tweet_pk,
        reply_content,
    ):
        tweet = Tweet.objects.get(pk=tweet_pk)
        reply = Reply.objects.create(
                author=author,
                tweet=tweet,
                content=reply_content,
            )
        tweet.has_new_reply = True
        tweet.save()
        return reply

# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(PeeUser)
    content = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    has_new_reply = models.BooleanField(default=False)

    def get_timestamp_str(self):
        return formats.date_format(self.timestamp, "DATETIME_FORMAT")

class Reply(models.Model):
    author = models.ForeignKey(PeeUser)
    tweet = models.ForeignKey(Tweet)
    content = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ReplyManager()
    class Meta:
        ordering = ['timestamp']

    def get_timestamp_str(self):
        return formats.date_format(self.timestamp, "DATETIME_FORMAT")
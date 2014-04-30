from datetime import datetime
from django.db import models
from pee_user.models import PeeUser


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
        return get_timestamp_str(self.timestamp)

    def set_timestamp_by_str(self, datetime_str):
        self.timestamp = get_timestamp(datetime_str)
        self.save()

class Reply(models.Model):
    author = models.ForeignKey(PeeUser)
    tweet = models.ForeignKey(Tweet)
    content = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ReplyManager()
    class Meta:
        ordering = ['timestamp']

    def get_timestamp_str(self):
        return get_timestamp_str(self.timestamp)

    def set_timestamp_by_str(self, datetime_str):
        self.timestamp = get_timestamp(datetime_str)
        self.save()

def get_timestamp_str(timestamp, detail=False):
    if detail:
        return timestamp.strftime('%B %d, %Y, %H:%M:%S')
    return timestamp.strftime('%B %d, %Y, %H:%M')

def get_timestamp(datetime_str, detail=False):
    if detail:
        return datetime.strptime(datetime_str, '%B %d, %Y, %H:%M:%S')
    return datetime.strptime(datetime_str, '%B %d, %Y, %H:%M')
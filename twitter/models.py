from django.db import models
from django.contrib.auth.models import User
from django.db.models import F


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_if_not_exists(cls, names):
        tags = []
        for name in names:
            try:
                tag = cls.objects.get(name=name)
            except cls.DoesNotExist:
                tag = Tag(name=name)
                tag.save()
            tags.append(tag)

        return tags


class Tweet(models.Model):
    tweet_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'tweet #{self.pk}'

    def make_vote(self, user, direction):
        try:
            vote = Vote.objects.get(tweet=self, voter=user)
        except Vote.DoesNotExist:
            vote = Vote(tweet=self, voter=user)

        if not direction == vote.direction:
            if vote.direction == 0:  # default value - not voted yet
                self.score = F('score') + direction
            else:  # voted before
                self.score = F('score') + direction * 2
            vote.direction = direction
        else:
            self.score = F('score') - vote.direction
            vote.direction = 0

        vote.save()
        self.save()
        self.refresh_from_db()
        return {'updated_score': self.score, 'direction': vote.direction}


class Vote(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    direction = models.IntegerField(default=0, choices=[(-1, -1), (0, 0), (1, 1)])

    @classmethod
    def get_vote_direction(cls, tweet, user):
        try:
            direction = cls.objects.get(tweet=tweet, voter=user).direction
        except cls.DoesNotExist:
            direction = 0
        return direction

    def __str__(self):
        return f'vote by {self.voter.username} on tweet {self.tweet.pk}'


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    text = models.TextField()

    def __str__(self):
        return f'comment by {self.author.username} on tweet {self.tweet.pk}'







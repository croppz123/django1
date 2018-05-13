from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from dj1.settings import MAX_TAG_LENGTH


class Tag(models.Model):
    name = models.CharField(max_length=MAX_TAG_LENGTH)

    @classmethod
    def get_or_create_from_list(cls, names):
        tags = []
        for name in names:
            tag, created = cls.objects.get_or_create(name=name)
            tags.append(tag)

        return tags

    def __str__(self):
        return self.name


class Tweet(models.Model):
    tweet_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def score(self):
        return sum([vote.direction for vote in self.vote_set.all()])

    @classmethod
    def get_decorated_list(cls, active_user_id, **filters):
        return cls.objects.all().filter(**filters).order_by('-pub_date') \
            .annotate(num_comments=Count('comment')) \
            .extra(select={'direction': 'SELECT direction FROM twitter_vote '
                                        'WHERE twitter_tweet.id = twitter_vote.tweet_id '
                                        'AND twitter_vote.voter_id = %s'},
                   select_params=(active_user_id,))

    def make_vote(self, user, direction):
        vote, created = Vote.objects.get_or_create(tweet=self, voter=user)

        if direction == vote.direction:
            vote.direction = 0
        else:
            vote.direction = direction

        vote.save()
        return {'updated_score': self.score, 'direction': vote.direction}

    def __str__(self):
        return f'tweet #{self.pk} by {self.author}'


class Vote(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    direction = models.IntegerField(default=0, choices=[(-1, -1), (0, 0), (1, 1)])

    @classmethod
    def get_vote_direction(cls, tweet, user):
        try:
            return cls.objects.get(tweet=tweet, voter=user).direction
        except cls.DoesNotExist:
            return 0

    def __str__(self):
        return f'vote by {self.voter.username} on tweet {self.tweet.pk}'


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return f'comment by {self.author.username} on tweet {self.tweet.pk}'

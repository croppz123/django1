from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from twitter.models import Tag, Tweet, Vote, Comment


class TagTestCase(TestCase):

    def setUp(self):
        Tag.objects.create(name="123")

    def test_tag_creation(self):
        """non-existent tags are correctly created"""
        tag_names = ['123', 'onion', 'yolo']
        tags = Tag.get_or_create_from_list(tag_names)
        for tag_name, tag in zip(tag_names, tags):
            self.assertEqual(tag.name, tag_name, 'tag names are being set correctly')
            self.assertIsInstance(tag, Tag, 'newly created tags are instances of Tag class')

    def test_tag_string(self):
        """tags are correctly converted to strings"""
        tag = Tag.objects.create(name='123')
        self.assertEqual(str(tag), '123')

    def tearDown(self):
        pass


class TweetTestCase(TestCase):

    def setUp(self):
        self.users = {
            'author': User.objects.create(username='author'),
            'user1': User.objects.create(username='user1'),
            'user2': User.objects.create(username='user2'),
            'user3': User.objects.create(username='user3'),
        }

        self.tweet = Tweet(author=self.users['author'], tweet_text='aaa', pub_date=timezone.now())
        self.tweet.save()

    def test_score(self):
        """tweet score is correctly calculated"""
        votes = [
            Vote.objects.create(voter=self.users['user1'], tweet=self.tweet, direction=0),
            Vote.objects.create(voter=self.users['user2'], tweet=self.tweet, direction=0),
            Vote.objects.create(voter=self.users['user3'], tweet=self.tweet, direction=0),
        ]
        self.tweet.vote_set.set(votes)

        self.assertEqual(self.tweet.score, 0)

        new_directions = [-1, 1, 1]
        for vote, direction in zip(votes, new_directions):
            vote.direction = direction
            vote.save()

        self.assertEqual(self.tweet.score, sum(new_directions))

    def test_decorating_list(self):
        pass  # TODO

    def test_voting(self):
        """tweet voting works as intended"""
        user = self.users['user1']

        result = self.tweet.make_vote(user, 1)
        self.assertTrue(result['created'], 'voting for the first time creates new vote')
        self.assertEqual(result['direction'], 1, 'voting sets vote direction correctly')
        self.assertEqual(result['updated_score'], 1, 'score is correctly updated')

        result = self.tweet.make_vote(user, 1)
        self.assertFalse(result['created'], 'subsequent votes do not create new vote instances')
        self.assertEqual(result['direction'], 0, 'subsequent vote with same direction sets direction to 0')
        self.assertEqual(result['updated_score'], 0, 'score is correctly updated')

        result = self.tweet.make_vote(user, 1)
        self.assertFalse(result['created'], 'subsequent votes do not create new vote instances')
        self.assertEqual(result['direction'], 1, 'voting sets new vote direction correctly')
        self.assertEqual(result['updated_score'], 1, 'score is correctly updated')

        result = self.tweet.make_vote(user, -1)
        self.assertFalse(result['created'], 'subsequent votes do not create new vote instances')
        self.assertEqual(result['direction'], -1, 'voting sets new vote direction correctly')
        self.assertEqual(result['updated_score'], -1, 'score is correctly updated')

    def tearDown(self):
        pass


class CommentTestCase(TestCase):

    def setUp(self):
        tweet_author = User.objects.create(username='tweet_author')
        self.tweet = Tweet.objects.create(author=tweet_author,
                                          pub_date=timezone.now(),
                                          tweet_text='aaaa')

        self.comment_author = User.objects.create(username='comment_author')
        self.comment = Comment.objects.create(author=self.comment_author,
                                              pub_date=timezone.now(),
                                              tweet=self.tweet,
                                              text='abcd')

    def test_comment_string(self):
        """comments are correctly converted to strings"""
        expected_string = f'comment by comment_author on tweet {self.tweet.pk}'
        self.assertEqual(str(self.comment), expected_string)

    def tearDown(self):
        pass

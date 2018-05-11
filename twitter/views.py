import re

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from el_pagination.decorators import page_template

from .models import Tweet, Comment, Tag, Vote


@page_template('twitter/tweet_list_page.html')
def index(request, template='twitter/index.html', extra_context=None):
    tweets = Tweet.objects.all().order_by('-pub_date')\
        .annotate(num_comments=Count('comment'))\
        .extra(select={'direction': 'SELECT direction FROM twitter_vote '
                                    'WHERE twitter_tweet.id = twitter_vote.tweet_id '
                                    'AND twitter_vote.voter_id = %s'},
               select_params=(request.user.id, ))

    context = {'header': 'LATEST TWEETS', 'tweets': tweets, 'user': request.user}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def detail(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if request.user.is_authenticated:
        tweet.direction = Vote.get_vote_direction(tweet=tweet, user=request.user)
    else:
        tweet.direction = 0
    context = {'tweet': tweet}
    return render(request, 'twitter/detail.html', context)


@login_required
def new(request):
    author = request.user
    text = request.POST['text'] + ' '
    pub_date = timezone.now()
    tweet = Tweet(author=author, pub_date=pub_date, tweet_text=text)
    tweet.save()
    tags_raw = re.findall(r"#(\w+)\s", text)
    tag_list = Tag.get_or_create_if_not_exists(tags_raw)
    print(tag_list)
    tweet.tags.add(*tag_list)
    return HttpResponseRedirect(reverse('twitter:index'))


@login_required
def upvote(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    response = tweet.make_vote(request.user, 1)
    return JsonResponse(response)


@login_required
def downvote(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    response = tweet.make_vote(request.user, -1)
    return JsonResponse(response)


@login_required
def add_comment(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    author = request.user
    text = request.POST['text']
    pub_date = timezone.now()
    comment = Comment(author=author, pub_date=pub_date, text=text, tweet=tweet)
    comment.save()
    return HttpResponseRedirect(reverse('twitter:detail', args=(pk,)))


@login_required
def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.author == request.user:
        tweet.delete()
        success = True
    else:
        success = False
    return JsonResponse({'success': success})


@page_template('twitter/tweet_list_page.html')
def tags(request, tagname, template='twitter/tags.html', extra_context=None):
    tag = get_object_or_404(Tag, name=tagname)
    tweets = Tweet.objects.all().filter(tags=tag).order_by('-pub_date') \
        .annotate(num_comments=Count('comment')) \
        .extra(select={'direction': 'SELECT direction FROM twitter_vote '
                                    'WHERE twitter_tweet.id = twitter_vote.tweet_id '
                                    'AND twitter_vote.voter_id = %s'},
               select_params=(request.user.id,))

    context = {'tagname': tagname.upper(), 'tweets': tweets, 'user': request.user}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


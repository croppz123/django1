import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from el_pagination.decorators import page_template

from dj1.settings import MAX_TAG_LENGTH, TAG_REGEX
from .models import Tweet, Comment, Tag, Vote


@page_template('twitter/tweet_list_page.html')
def index(request, template='twitter/index.html', extra_context=None):
    tweets = Tweet.get_decorated_list(request.user.id)
    context = {'tweets': tweets,
               'user': request.user}

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
    text = request.POST['text'] + ' '
    tweet = Tweet(author=request.user,
                  pub_date=timezone.now(),
                  tweet_text=text)
    tweet.save()

    tags_raw = re.findall(TAG_REGEX, text)
    tags_filtered = filter(lambda tag: len(tag) <= MAX_TAG_LENGTH, tags_raw)
    tag_list = Tag.get_or_create_from_list(tags_filtered)
    tweet.tags.add(*tag_list)

    tweet.num_comments = 0
    template = loader.get_template('twitter/tweet.html')
    div_render = template.render({'tweet': tweet, 'detailed_view': 0}, request)
    return JsonResponse({'success': True, 'div': div_render})


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
    comment = Comment(tweet=get_object_or_404(Tweet, pk=pk),
                      author=request.user,
                      pub_date=timezone.now(),
                      text=request.POST['text'])
    comment.save()
    return HttpResponseRedirect(reverse('twitter:detail', args=(pk,)))


@login_required
def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.author == request.user or request.user.is_superuser:
        tweet.delete()
        success = True
    else:
        success = False
    return JsonResponse({'success': success})


@page_template('twitter/tweet_list_page.html')
def tags(request, tagname, template='twitter/tags.html', extra_context=None):
    tag = get_object_or_404(Tag, name=tagname)
    tweets = Tweet.get_decorated_list(request.user.id, tags=tag)
    context = {'tagname': tagname.upper(),
               'tweets': tweets,
               'user': request.user}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)




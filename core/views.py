from collections import Counter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from el_pagination.decorators import page_template

from core.models import Profile
from twitter.models import Tweet


def index(request):
    return render(request, 'index.html', {})


@page_template('twitter/tweet_list_page.html')
def profile(request, username, template='profile.html', extra_context=None):
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(author=user).order_by('-pub_date')\
        .annotate(num_comments=Count('comment'))\
        .extra(select={'direction': 'SELECT direction FROM twitter_vote '
                                    'WHERE twitter_tweet.id = twitter_vote.tweet_id '
                                    'AND twitter_vote.voter_id = %s'},
               select_params=(request.user.id, ))
    tags = Counter([f'#{tag.name} ' for tweet in tweets for tag in tweet.tags.all()]).most_common(20)
    context = {'user': user, 'tweets': tweets, 'tags': tags}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@login_required
def remove_avatar(request):
    request.user.profile.avatar.delete(save=True)
    request.user.profile.avatar = Profile.DEFAULT_AVATAR
    request.user.profile.save()
    return JsonResponse({'success': True})

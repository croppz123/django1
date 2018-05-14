from collections import Counter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from el_pagination.decorators import page_template

from core.forms import ProfileForm
from core.models import Profile
from twitter.models import Tweet
from dj1.settings import DEFAULT_AVATAR_PATH

def index(request):
    return render(request, 'index.html', {})


def my_profile(request):
    return profile(request, username=request.user.username)


@page_template('twitter/tweet_list_page.html')
def profile(request, username=" ", template='profile/view.html', extra_context=None):
    user = get_object_or_404(User, username=username)
    tweets = Tweet.get_decorated_list(request.user.id, author=user)
    tags = Counter([f'#{tag.name} ' for tweet in tweets for tag in tweet.tags.all()]).most_common(20)
    context = {'user': user, 'tweets': tweets, 'tags': tags}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@login_required
def profile_edition(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            profile.name = request.POST['name']
            profile.city = request.POST['city']
            profile.country = request.POST['country']
            profile.birth_date = request.POST['birth_date']
            profile.bio = request.POST['bio']
            profile.save()
            return HttpResponseRedirect(reverse('core:my_profile'))
    else:
        form = ProfileForm(instance=request.user.profile)
        context = {'form': form}
        return render(request, 'profile/edition.html', context)


@login_required
def remove_avatar(request):
    request.user.profile.avatar.delete(save=True)
    request.user.profile.avatar = DEFAULT_AVATAR_PATH
    request.user.profile.save()
    return JsonResponse({'success': True})

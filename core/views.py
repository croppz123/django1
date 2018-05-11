from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from core.models import Profile


def index(request):
    return render(request, 'index.html', {})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})


@login_required
def remove_avatar(request):
    request.user.profile.avatar.delete(save=True)
    request.user.profile.avatar = Profile.DEFAULT_AVATAR
    request.user.profile.save()
    return JsonResponse({'success': True})

import re

from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from dj1.settings import TAG_REGEX

register = template.Library()


def create_hashtag_link(tag):
    url = reverse('twitter:tags', args=(tag, ))
    return f'#<a href="{url}" class="text-warning">{tag}</a> '


@register.filter(name='hash')
def hashtag_links(tweet_text):
    return mark_safe(re.sub(TAG_REGEX, lambda t: create_hashtag_link(t.group(1)), escape(tweet_text)))

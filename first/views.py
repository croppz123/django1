from django.shortcuts import render, get_object_or_404
from .models import Article


# noinspection PyUnresolvedReferences
def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    context = {'year': year, 'article_list': a_list}
    return render(request, 'news/year_archive.html', context)


# noinspection PyUnresolvedReferences
def month_archive(request, year, month):
    a_list = Article.objects.filter(pub_date__year=year, pub_date__month=month)
    context = {'year': year, 'month': month, 'article_list': a_list}
    return render(request, 'news/month_archive.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, 'news/article_detail.html', context)

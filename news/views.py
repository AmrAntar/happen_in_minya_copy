from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Category, NewsPost, Item
from taggit.models import Tag
import random
import requests
import json
from bs4 import BeautifulSoup
import parser


# Create your views here.

def get_link():
    url = "https://www.youm7.com/Section/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B9%D8%A7%D8%AC%D9%84%D8%A9/65/1"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    data = soup.find_all('div', attrs={'class': 'bigOneSec'})
    for link in data:
        yield link.contents[3].find('h3').text
        # yield link.contents[3].find('span').text


def home(request):
    news_api_request = requests.get('http://newsapi.org/v2/top-headlines?sources=google-news-sa&apiKey=704ecfbeed0b49fe9761d9dc4c039adf')
    api = json.loads(news_api_request.content)

    categories = Category.objects.all()
    posts = NewsPost.objects.all()
    tags = Tag.objects.all()
    videos = Item.objects.all()

    queryset2 = NewsPost.tags.annotate(num_tags=Count('taggit_taggeditem_items')).order_by('-num_tags')

    # show_all_tag = Tag.objects.annotate(num_tags=Count('taggit_taggeditem_items')).all()
    # all = NewsPost.objects.filter(tags__name__in=show_all_tag.all()).count()

    # fo = NewsPost.objects.aggregate(Count('tags'))

    # accedent = NewsPost.objects.filter(tags__name__in=["حوادث"]).count()
    # gov = NewsPost.objects.filter(tags__name__in=["محافظات"]).count()
    # spo = NewsPost.objects.filter(tags__name__in=["رياضه"]).count()
    # polotic = NewsPost.objects.filter(tags__name__in=["سياسه"]).count()

    minya = posts.filter(category=1)
    egypt = posts.filter(category=2)
    sport = posts.filter(category=3)
    articles = posts.filter(category=4)
    teckno = posts.filter(category=5)
    art = posts.filter(category=6)
    culture = posts.filter(category=7)

    # get recent post
    all_post = NewsPost.objects.all()
    recent_post = all_post[:7]

    # get random post
    all_post = list(NewsPost.objects.all())
    random_post = random.sample(all_post, 7)

    # get random news from bs4
    all_random_news = list(get_link())
    dododo = random.sample(all_random_news, 10)

    # random articles
    artc = list(articles.all())
    rand_articles = random.sample(artc, 3)

    # random teckno
    teck = list(teckno.all())
    rand_tecknology = random.sample(teck, 3)

    # random Art
    a = list(art.all())
    rand_art = random.sample(a, 3)

    # random Culture
    c = list(culture.all())
    rand_culture = random.sample(c, 3)

    context = {
        'categories': categories,
        'posts': posts,
        'minya': minya,
        'egypt': egypt,
        'sport': sport,
        'teckno': teckno,
        'articles': articles,
        'videos': videos,
        'recent_post': recent_post,
        'random_post': random_post,
        'rand_articles': rand_articles,
        'rand_tecknology': rand_tecknology,
        'rand_art': rand_art,
        'rand_culture': rand_culture,

        'all_random_news': dododo,

        'tags': tags,
        'queryset2': queryset2,
        'api': api,
    }
    return render(request, 'news/home_page.html', context)


def show_category_tab(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    posts = NewsPost.objects.all()

    videos = Item.objects.all()

    # get recent post
    all_post = NewsPost.objects.all()
    recent_post = all_post[:6]

    # get random post
    all_post = list(NewsPost.objects.all())
    random_post = random.sample(all_post, 6)

    if category_slug:
        posts = NewsPost.objects.all()
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)


    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context = {
        'posts': posts,
        'categories': categories,
        'category': category,
        'page': page,
        'recent_post': recent_post,
        'random_post': random_post,
        'main': 'الرئيسيه',
        'videos': videos,
    }
    return render(request, 'news/tab_page.html', context)


def post_detail(request, post_slug):
    posts = get_object_or_404(NewsPost, slug=post_slug)
    categories = Category.objects.all()

    all_post = list(NewsPost.objects.exclude(slug=post_slug))
    like_post = random.sample(all_post, 4)

    # get recent post
    all_post = NewsPost.objects.all()
    recent_post = all_post[:6]

    # get random post
    all_post = list(NewsPost.objects.all())
    random_post = random.sample(all_post, 6)


    session_key = 'count_views_{}'.format(posts.pk)
    if not request.session.get(session_key, False):
        posts.views += 1
        posts.save()
        request.session[session_key] = True

    # related posts by tags:
    similar_posts = posts.tags.similar_objects()[:6]

    context = {
        'posts': posts,
        'categories': categories,
        'like_post': like_post,
        'similar_posts': similar_posts,
        'recent_post': recent_post,
        'random_post': random_post,
        'main': 'الرئيسيه',

    }
    return render(request, 'news/post_detail.html', context)


def display_taged_post(request, tag_slug=None):
    categories = Category.objects.all()

    tags = Tag.objects.all()

    queryset2 = NewsPost.tags.annotate(num_tags=Count('taggit_taggeditem_items')).order_by('-num_tags')


    # get recent post
    all_post = NewsPost.objects.all()
    recent_post = all_post[:3]

    # get random post
    all_post = list(NewsPost.objects.all())
    random_post = random.sample(all_post, 3)

    # top common tag
    # YourModel.tags.most_common()
    # YourModel.tags.most_common()[:10]

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = NewsPost.objects.filter(tags__in=[tag])

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'posts': posts,
        'page ': page,
        'recent_post': recent_post,
        'random_post': random_post,
        'tag': tag,
        'main': 'الرئيسيه',
        'tags': tags,
        'queryset2': queryset2,

    }
    return render(request, 'news/display_taged_post.html', context)


def search_post(request):
    categories = Category.objects.all()
    posts = NewsPost.objects.all()
    query = request.GET.get('q')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()

    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    context = {
        'query': query,
        'categories': categories,
        'posts': posts,
        'page': page,
        'main': 'الرئيسيه',
    }
    return render(request, 'news/search_page.html', context)


def login(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }
    return render(request, 'news/login.html', context)



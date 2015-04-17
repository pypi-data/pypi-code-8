from django import template

# Models
from news.app.news.models import News

# Tag register
register = template.Library()


def latest_news(context, category_slug, count):
    news = News.objects.filter(category__slug=category_slug, published=True).order_by('-created_at')[:count]

    context = {
        "news": news,
        "category_slug": category_slug,
        "request": context["request"]
    }

    return context

register.inclusion_tag('news/templatetags/latest_news.html', takes_context=True)(latest_news)


def highlight_news(context, count):
    news = News.objects.filter(published=True, highlight=True).order_by('-created_at')[:count]

    context = {
        "news": news,
        "request": context["request"]
    }

    return context

register.inclusion_tag('news/templatetags/highlight_news.html', takes_context=True)(highlight_news)
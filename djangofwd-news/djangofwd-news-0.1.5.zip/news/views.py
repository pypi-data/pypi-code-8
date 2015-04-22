from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

# Models
from models import News, Category, Gallery


class NewsList(ListView):
    queryset = News.objects.filter(published=True).order_by('-created_at')
    context_object_name = 'news'
    template_name = 'news/news_list.html'


class NewsDetail(DetailView):
    model = News
    context_object_name = 'article'
    template_name = 'news/news_detail.html'


class NewsListCategories(View):
    template_name = 'news/categories/news_list_categories.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(published=True)

        context = {
            'categories': categories
        }

        return render(request, self.template_name, context)


class NewsListCategory(View):
    template_name = 'news/categories/news_list_category.html'

    def get(self, request, slug, *args, **kwargs):
        news = News.objects.filter(category__slug=slug, published=True).order_by('-created_at')

        context = {
            'news': news
        }

        return render(request, self.template_name, context)


class NewsDetailCategory(DetailView):
    queryset = News.objects.filter(published=True)
    context_object_name = 'article'
    template_name = 'news/categories/news_detail_category.html'
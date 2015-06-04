# -*- coding: utf-8 -*-

import json
import datetime
import urllib2

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings as conf
from django.contrib.sites.models import Site
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
from django.template.defaultfilters import slugify

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin

from disqusapi import DisqusAPI
from BeautifulSoup import BeautifulSoup

import models as mymodels
import forms as myforms


class BaseMeta(object):

    def get_context_data(self, **kwargs):
        context = super(BaseMeta, self).get_context_data(**kwargs)

        current_site = Site.objects.get_current()

        try:
            tit = conf.RBLOG_SITE_TITLE
        except:
            tit = _('Blog')

        try:
            desc = conf.RBLOG_SITE_DESCRIPTION
        except:
            tit = _('This is the blog')

        try:
            keyw = conf.RBLOG_SITE_KEYWORDS
        except:
            keyw = _('these, are, keywords')

        context.update({
            'current_site': current_site.domain,
            'title': tit,
            'description': desc,
            'keywords': keyw,
        })
        return context


class BlogIndexView(BaseMeta, ListView):

    template_name = "rblog/index.html"
    context_object_name = "myposts"
    cache_timeout = 600
    paginate_by = 2

    def get_queryset(self):
        timenow = datetime.datetime.now()
        return mymodels.Post.objects.filter(
            status=1,
            creation_date__lte=timenow).order_by('-creation_date')


class LinkblogIndexView(ListView):

    template_name = "rblog/index.html"
    context_object_name = "myposts"
    paginate_by = 200

    def get_queryset(self):
        timenow = datetime.datetime.now()
        return mymodels.Post.objects.filter(
            status=1,
            ptype='link',
            creation_date__lte=timenow).order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super(LinkblogIndexView, self).get_context_data(**kwargs)
        context.update({
            'title': _('Linkblog'),
            'description': _('Interesting links I\'ve found'),
        })
        return context


class PostDetailView(BaseMeta, DetailView):

    template_name = "rblog/detail.html"
    context_object_name = "mypost"

    def get_object(self):
        self.obj = get_object_or_404(mymodels.Post, slug=self.kwargs['slug'],
                                     status=1)
        self.obj.hits = self.obj.hits + 1
        permalink = self.request.build_absolute_uri()
        # if DISQUS_SYNC is True it tries to fill thread_id vía Disqus API
        try:
            if conf.DISQUS_SYNC:
                if not self.obj.thread_id:
                    try:
                        api = DisqusAPI(conf.DISQUS_API_SECRET,
                                        conf.DISQUS_API_PUBLIC)
                        dq_response = api.threads.details(
                            forum=conf.DISQUS_WEBSITE_SHORTNAME,
                            thread='link:%s' % permalink)
                        self.obj.thread_id = dq_response['id']
                    except:
                        pass
                    try:
                        api = DisqusAPI(conf.DISQUS_API_SECRET,
                                        conf.DISQUS_API_PUBLIC)
                        dq_response = api.threads.details(
                            forum=conf.DISQUS_WEBSITE_SHORTNAME,
                            thread='link:%s' % permalink)
                        self.obj.thread_id = dq_response['id']
                    except:
                        pass
        except:
            pass
        self.obj.save()
        return self.obj

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = mymodels.Comments.objects.filter(
            thread_id=self.obj.thread_id, thread_id__isnull=False)
        context.update({
            'comments': comments,
        })
        return context

    def render_to_response(self, context):
        if self.obj.redirect:
            return redirect(self.obj.redirect)
        return super(PostDetailView, self).render_to_response(context)


class PostLinkAdd(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):

    model = mymodels.Post
    form_class = myforms.LinkForm
    success_url = '/'

    def form_valid(self, form):
        if self.request.is_ajax() and self.request.method == 'POST':
            link = json.loads(self.request.POST.get('link', None))
            soup = BeautifulSoup(urllib2.urlopen(link))
            try:
                title = soup.title.string
            except:
                title = 'No title'
            try:
                desc = soup.findAll(attrs={"name": "description"})[0]['content']
            except:
                desc = 'No description available'

            post = mymodels.Post(
                title=title,
                slug=slugify(title),
                text=desc,
                creation_date=datetime.datetime.now(),
                canonical=link,
                ptype='link',
                user=self.request.user)
            post.save()
            return HttpResponse(1)


class PostTempView(DetailView):

    template_name = "rblog/detail.html"
    context_object_name = "mypost"

    def get_object(self):
        self.obj = get_object_or_404(mymodels.Post,
                                     slug=self.kwargs['slug'],
                                     status=0)
        return self.obj


class PostsWithTag(BaseMeta, ListView):

    template_name = "rblog/index.html"
    context_object_name = "myposts"
    paginate_by = 20

    def get_queryset(self):
        tag = [self.kwargs['tag']]
        myposts = mymodels.Post.objects.filter(tags__name__in=tag)
        datetimenow = datetime.datetime.now()
        return myposts.all().filter(
            status=1,
            creation_date__lte=datetimenow).order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super(PostsWithTag, self).get_context_data(**kwargs)
        context.update({
            'tag': self.kwargs['tag'],
        })
        return context


class PostsByDate(BaseMeta, ListView):

    template_name = "rblog/index.html"
    context_object_name = "myposts"
    paginate_by = 20

    def get_queryset(self):
        return mymodels.Post.objects.all().filter(
            status=1,
            creation_date__lte=datetime.datetime.now(),
            creation_date__month=self.kwargs['month'],
            creation_date__year=self.kwargs['year']).order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super(PostsByDate, self).get_context_data(**kwargs)
        myarch = u"%s.%s" % (str(self.kwargs['month']),
                             str(self.kwargs['year']))
        context.update({
            'archive': myarch,
            'month': str(self.kwargs['month']),
            'byear': str(self.kwargs['year']),
        })
        return context


class AJAXArchive(ListView):

    template_name = "rblog/archive.html"
    model = mymodels.Post

    def get_context_data(self, **kwargs):
        context = super(AJAXArchive, self).get_context_data(**kwargs)
        datetimenow = datetime.datetime.now()
        first_post = mymodels.Post.objects.all().filter(
            status=1,
            creation_date__lte=datetimenow).order_by('creation_date')[0]
        year_ini = int(first_post.creation_date.strftime("%Y"))
        year_hoy = datetime.datetime.now().year
        mes_hoy = datetime.datetime.now().month
        meses = [_('January'), _('February'), _('March'), _('April'), _('May'),
                 _('June'), _('July'), _('August'), _('September'),
                 _('October'), _('November'), _('December')]
        years = range(year_ini, year_hoy+1)

        results = dict()
        for j in range(year_ini, year_hoy+1):
            for i in range(1, 13):
                num = mymodels.Post.objects.filter(
                    creation_date__year=j,
                    creation_date__month=i).count()
                results[j, i] = num

        context.update({
            'first_post': first_post,
            'year_ini': year_ini,
            'mes_hoy': mes_hoy,
            'meses': meses,
            'years': years,
            'year_hoy': year_hoy,
            'results': results,
        })
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['rblog/archive_ajax.html']
        else:
            return ['rblog/archive.html']


class BlogSitemap(Sitemap):

    changefreq = "never"
    priority = 0.5

    def items(self):
        timenow = datetime.datetime.now()
        return mymodels.Post.objects.filter(
            status=1,
            ptype='post',
            creation_date__lte=timenow).order_by('-creation_date')

    def lastmod(self, obj):
        return obj.creation_date

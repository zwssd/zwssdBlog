"""zwssdBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
    Examples:
        Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
        Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
        Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
        """
from django.contrib import admin
from django.urls import path
from zwssdBlog.view import output
from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.urls import reverse
from django.contrib import admin
from zblog.models import Article, News, Category, Column

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['index-view', 'news-view']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'article-is-top': GenericSitemap(
        {
            'queryset': Article.objects.filter(
                status=0, is_top=True
            ).all(),
            'date_field': 'pub_time'
        },
        priority=1.0,
        changefreq='daily'
    ),
    'article-is-not-top': GenericSitemap(
        {
            'queryset': Article.objects.filter(status=0).all(),
            'date_field': 'pub_time'
        },
        priority=0.8,
        changefreq='daily'
    ),
    'news': GenericSitemap(
        {
            'queryset': News.objects.all(),
            'data_field': 'pub_time'
        },
        priority=0.6,
        changefreq='daily'
    ),
    'category': GenericSitemap(
        {
            'queryset': Category.objects.all()
        },
        priority=0.9,
        changefreq='daily'
    ),
    'column': GenericSitemap(
        {
            'queryset': Column.objects.all()
        },
        priority=0.9,
        changefreq='daily'
    ),
    'static': StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('output/', output),
    path('', include('zblog.urls')),
    url(r'', include('zcomments.urls')),
    url(r'', include('zuser.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

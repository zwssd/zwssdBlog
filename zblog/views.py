# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.views.generic import View, TemplateView, ListView, DetailView
from django.conf import settings
from django.core.cache import caches
from django.db.models import Q
from zblog.models import Article, Category, Carousel, Column, Nav, News
from zcomments.models import comments
from zsystem.models import Link
import logging

# 缓存
try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']

# logger
logger = logging.getLogger(__name__)

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 网站标题等内容
            context['website_title'] = settings.WEBSITE_TITLE
            context['website_welcome'] = settings.WEBSITE_WELCOME
            # 热门文章
            context['hot_article_list'] = \
                Article.objects.order_by("-view_times")[0:10]
            # 导航条
            context['nav_list'] = Nav.objects.filter(status=0)
            # 最新评论
            context['latest_comment_list'] = \
                comments.objects.order_by("-create_time")[0:10]
            # 友情链接
            context['links'] = Link.objects.order_by('create_time').all()
            colors = ['primary', 'success', 'info', 'warning', 'danger']
            for index, link in enumerate(context['links']):
                link.color = colors[index % len(colors)]
            # 用户未读消息数
            user = self.request.user
            if user.is_authenticated():
                context['notification_count'] = \
                    user.to_user_notification_set.filter(is_read=0).count()
        except Exception as e:
            logger.error(u'[BaseMixin]加载基本信息出错')

        return context

class ArticleView(BaseMixin, DetailView):
    queryset = Article.objects.filter(Q(status=0) | Q(status=1))
    template_name = 'zblog/article.html'
    context_object_name = 'article'
    slug_field = 'en_title'

    def get(self, request, *args, **kwargs):
        # 统计文章的访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        self.cur_user_ip = ip

        en_title = self.kwargs.get('slug')
        # 获取15*60s时间内访问过这篇文章的所有ip
        visited_ips = cache.get(en_title, [])

        # 如果ip不存在就把文章的浏览次数+1
        if ip not in visited_ips:
            try:
                article = self.queryset.get(en_title=en_title)
            except Article.DoesNotExist:
                logger.error(u'[ArticleView]访问不存在的文章:[%s]' % en_title)
                raise Http404
            else:
                article.view_times += 1
                article.save()
                visited_ips.append(ip)

            # 更新缓存
            cache.set(en_title, visited_ips, 15*60)

        return super(ArticleView, self).get(request, *args, **kwargs)

class TagView(BaseMixin, ListView):
    template_name = 'blog/tag.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUMBER

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        article_list = \
            Article.objects.only('tags').filter(tags__icontains=tag, status=0)

        return article_list
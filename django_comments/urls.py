# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django_comments.plugins import plugin_pool


class URLConf(object):
    def __init__(self, codename):
        self.plugin = plugin_pool.get_plugin(codename)

    def get_urls(self):
        return self.plugin.get_urlpatterns()


def comments_urlpatterns():
    found_urlpatterns = []
    for plugin in plugin_pool.get_all_plugins():
        found_urlpatterns += URLConf(plugin).get_urls()
    return found_urlpatterns


urlpatterns = comments_urlpatterns()
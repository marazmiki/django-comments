# coding: utf-8

from django_comments.plugins import plugin_pool


class URLConf(object):
    """
    Comment URLConf class
    """

    def __init__(self, codename):
        """
        The class constructor
        """
        self.plugin = plugin_pool.get_plugin(codename)

    def get_urls(self):
        """
        Returns plugin URL patterns
        """
        return self.plugin.get_urlpatterns()


def comments_urlpatterns():
    """
    Returns list of all urls
    """
    return [url for urls in plugin_pool.get_all_plugins() for url in URLConf(c).get_urls()]


urlpatterns = comments_urlpatterns()

from django.conf.urls.defaults import patterns, url
from django.core.exceptions import ImproperlyConfigured

class Comment(object):
    """
    """

    def __init__(self, request=None):
        """
        """
        self.request = request

    def get_urls(self):
        return patterns('comments.views',
            url('^create/$', 'create', name='comments_create'),
            url('^reply/(?P<parent_id>\d)/$',  'reply',  name='comments_reply'),
        )

    def get_form(self):
        """
        """
        raise NotImplementedError('get_form')

    def get_model(self):
        """
        """
        raise NotImplementedError('get_model')

    def queryset(self):
        """
        """
        raise NotImplementedError('queryset')

    def on_success_postsave(self, comment):
        """
        """
        raise NotImplementedError('on_success')

    def on_success_presave(self, form, comment):
        """
        """
        raise NotImplementedError('on_success_before_save')

    def on_failure(self, form):
        """
        """
        raise NotImplementedError('on_failure')

    def on_get_request(self):
        """
        """
        raise NotImplementedError('on_get_request')

def get_plugin(request=None, scheme=None):
    plugin = Comment(request)

    if type(plugin) is not Comment:
        raise ImproperlyConfigured('Is not a plugin')
    return plugin
from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.comments.forms import CommentForm
from django.contrib.comments.urls import urlpatterns
from django_comments.plugins import BasePlugin

class DjangoCommentPlugin(BasePlugin):
    """
    Default comments plugin.

    It uses from native `django.contrib.comments` application
    and not uses `django-comments` features.

    """
    codename = 'django'
    content_object_field = 'content_object'

    def __init__(self, *args, **kwargs):
        """
        The class constructor
        """
        super(DjangoCommentPlugin, self).__init__(*args, **kwargs)
        app = 'django.contrib.comments'

        if app not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.append(app)

    def get_model(self, request):
        """
        Returns the comment model class
        """
        return Comment

    def get_form(self, request):
        """
        Returns the comment model form class
        """
        return CommentForm

    def get_urlpatterns(self):
        """
        Returns set of urlconf in standart 'urlpatterns' format
        """
        return urlpatterns
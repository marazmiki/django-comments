from warnings import warn
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from reusable.comments.tests import TestCase
from reusable.comments.plugins import get_plugin, CommentPlugin
from reusable.comments_plugins.guest import GuestCommentPlugin

class PluginTest(TestCase):
    def test_get_plugin_without_arguments(self):
        assert isinstance(get_plugin(), GuestCommentPlugin)

    def test_get_plugin_with_default_schema(self):
        assert isinstance(get_plugin('default'), GuestCommentPlugin)
        
    def test_get_plugin_with_non_existant_schema(self):           
        def raise_exception():
            p = get_plugin('a.b.c')
            print p

        self.assertRaises(ImproperlyConfigured, raise_exception)
        #warn('Implement later')

    #def get_form(self, request=None):
    #def get_model(self):
    #def queryset(self, content_object):
    #def on_success_before_save(self, request, form, comment):
    #def on_success(self, request, form, comment):
    #def on_failure(self, request, form):
    #def on_get_request(self, request, form, content_object, parent_comment=None):

#def get_plugin(scheme='default'):

# -*- coding: utf-8 -*-

from comments.models import CommentSettings

def get_settings_for_object(object):
    try:
        return CommentSettings.objects.get_for_object(object)[0]
    except (IndexError, CommentSettings.DoesNotExist):
        return CommentSettings()
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from mptt import register as mptt_register, registry as mptt_registry

# --------------------------------------------------------------------------- #

class CommentPlugin(object):
    """
    Базовый класс плагина к системе комментирования

    """
    def get_form(self):
        """
        Возвращает объект формы для отправки комментария, которую будет
        использовать плагин.

        Возвращает:
          * Объект django.db.models.ModelForm
        """
        raise NotImplementedError('Please implement get_form() function')

    def get_model(self):
        """
        Возвращает объект модели комментариев, которую будет
        использовать плагин.

        Возвращает:
          * Объект django.db.models.Model
        """
        raise NotImplementedError('Please implement get_model() function')

    def on_success(self, request, form, comment):
        """
        Обработчик, вызываемый после успешного создании комментария

        Принимает следующие параметры:
          * request
          * form
          * comment

        Возвращает:
          * Объект HttpResponse
        """
        raise NotImplementedError('Please implement on_success hook')

    def on_failure(self, request, form):
        """
        Обработчик, вызываемый при ошибке создании комментария

        Принимает следующие параметры:
          * request
          * form
          * content_object

        Возвращает:
          * Объект HttpResponse
        """
        raise NotImplementedError('Please implement on_failure hook')

    def on_get_request(self, request, form, content_object):
        """
        Обработчик, вызываемый в случае запроса страницы создания
        комментария методом GET

        Принимает следующие параметры:
          * request
          * form
          * content_object

        Возвращает:
          * Объект HttpResponse
        """
        raise NotImplementedError('Please implement on_get_request hook')

# --------------------------------------------------------------------------- #

def str_to_class(str):
    """
    Импортирует модуль по адресу, указанному во входящей строке и
    возвращает его
    
    Принимает следующие аргументы:
      * str

    Возвращает:
      * module
    """
    package, attribute = str.rsplit('.', 1)
    return getattr(__import__(package, globals(), locals(), ['']), attribute)

# --------------------------------------------------------------------------- #

def get_plugin(scheme='default'):
    """
    Возвращает класс плагина, соответствующего заданной схеме
    
    Принимает следущие аргументы:
      * scheme

    Возвращает:
      * class
    """
    class_name = 'comments.plugins.guest.GuestCommentPlugin'

    try:
        plugin = str_to_class(class_name)()

    except AttributeError, e:
        raise ImproperlyConfigured(
            'Class %s not found' % class_name
        )

    if not isinstance(plugin, CommentPlugin):
        raise ImproperlyConfigured(
            'Object is not a CommentPlugin instance' % scheme
        )

    return plugin

# --------------------------------------------------------------------------- #

def register(model):
    """
    Регистрирует модель плагина

    Принимает следущие аргументы:
      * django.db.models.Model
    """
    if model not in mptt_registry:
        mptt_register(model,
            parent_attr        = 'parent_comment',
            order_insertion_by = ['date_created', ],
        )

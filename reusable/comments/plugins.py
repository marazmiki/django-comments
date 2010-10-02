# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from mptt import register as mptt_register, registry as mptt_registry

# --------------------------------------------------------------------------- #

class CommentPlugin(object):
    """
    Базовый класс плагина к системе комментирования

    """
    def get_form(self, request=None):
        """
        Возвращает объект формы для отправки комментария, которую будет
        использовать плагин.

        Принимает следующие параметры:
          * request Объект django.http.HttpRequest

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

    def queryset(self, content_object):
        """
        Возвращает QuerySet для получения дерева комментариев к
        объекту content_object

        Принимает следующие параметры:
          * content_object

        Возвращает:
          * Объект django.db.models.query.QuerySet
        """
        return self.get_model().objects.get_for_object(content_object)#.order_by('tree_id', 'lft', 'date_created')

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

    def on_get_request(self, request, form, content_object, parent_comment=None):
        """
        Обработчик, вызываемый в случае запроса страницы создания
        комментария методом GET

        Принимает следующие параметры:
          * request
          * form
          * content_object
          * parent_comment

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
    class_name = 'reusable.comments_plugins.guest.GuestCommentPlugin' # @FIXIT

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

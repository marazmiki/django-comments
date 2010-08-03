# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from comments.plugins import get_plugin

# --------------------------------------------------------------------------- #

def create(request, content_object, parent_comment=None, scheme='default'):
    """
    Помощник, реализующий общую логику создания комментария.
    
    Получает необходимые классы модели и формы, выполняет валидацию,
    в случае успеха создаёт объект комментария. Вне зависимости от исхода
    вызывает обработчики плагина
    
    Принимает следующие аргументы:
      * request
      * parent_id
      * scheme

    Возвращает:
      * Объект HttpResponse    
    """
    plugin = get_plugin(scheme)
    CommentForm = plugin.get_form()

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.remote_addr   = request.META.get('REMOTE_ADDR')
            comment.forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            if parent_comment:
                comment.insert_at(parent_comment,
                    position = 'last-child',
                    commit   = False,
                )

            comment.save()
            return plugin.on_success(request, form, comment)

        else:
            return plugin.on_failure(request, form)

    else:
        form = CommentForm(initial={'redirect_to': ''})
        return plugin.on_get_request(request, form, content_object, parent_comment)

# --------------------------------------------------------------------------- #

def new(request, scheme='default'):
    """
    Отображение, обслуживающее страницу создания комментария.

    Принимает следующие аргументы:
      * request
      * scheme

    Возвращает:
      * Объект HttpResponse
    """
    content_type = request.POST.get('content_type')
    object_id    = request.POST.get('object_id')

    # N.B. Обратите внимание: получение параметров content_type и object_id
    #      из словаря POST приводят к тому, что при GET-запросе на страницу 
    #      создания нового комментария будет генерироваться ошибка 404.
    #      И это вполне нормальное поведение.

    return create(request,
        content_object = get_object_or_404(
            get_object_or_404(ContentType, pk=content_type).model_class(),
            pk = object_id,
        ),
        scheme = scheme
    )
    
# --------------------------------------------------------------------------- #

def reply(request, parent_id, scheme='default'):
    """
    Отображение, обслуживающее страницу создания комментария.

    Принимает следующие аргументы:
      * request
      * parent_id
      * scheme

    Возвращает:
      * Объект HttpResponse
    """
    plugin = get_plugin(scheme)
    parent = get_object_or_404(plugin.get_model(), pk=parent_id)

    return create(request,
        content_object = parent.content_object,
        parent_comment = parent,
        scheme         = scheme,
    )
# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.http import HttpResponse, Http404
from comments.forms import CommentForm, ReplyForm
from comments.models import Comment, LastReadedComment
from comments.utils import get_settings_for_object, update_last_readed_comment

def create(request, parent_id=None):
    """
    Post a new comment
    """
    def get_parent():
        """
        Returns parent comment if reply required
        """
        return get_object_or_404(Comment, pk=parent_id) if parent_id else None

    def get_object():
        """
        Returns instance of object which will be commented
        """
        if parent:
            object = parent.content_object

        else:
            ct = request.POST.get('content_type')
            op = request.POST.get('object_pk')

            try:
                ctype  = get_object_or_404(ContentType, pk=ct)
                model  = ctype.model_class()
                object = get_object_or_404(model, pk=op)
            except:
                raise Http404('Wrong content object')

        return object

    def get_form():
        """
        Creates form instance
        """
        if request.method == 'GET' and parent:
            redirect_to = request.META.get('HTTP_REFERER', '/')

        else:
            redirect_to = request.POST.get('redirect_to', '/')
        
        form = ReplyForm if parent else CommentForm
        init = dict(initial={'redirect_to':redirect_to})

        return form(request.POST,**init)     \
            if request.method == 'POST'      \
            else form(**init)

    parent = get_parent()
    form   = get_form()
    result = dict()
    object = get_object()

    if request.method == 'POST':
        # Gets object specified comments settings
        settings = get_settings_for_object(object)

        if not settings.enabled:
            raise Http404('Comment for this object is disabled')

        # Valdiate the form
        valid  = form.is_valid()

        # Add success flag into template context
        result.update(success=valid)

        if valid:
            comment = form.save(commit=False)
            comment.parent_comment = parent
            comment.content_object = object
            comment.remote_addr    = request.META.get('REMOTE_ADDR')
            comment.forwarded_for  = request.META.get('HTTP_X_FORWARDRED_FOR')
            comment.is_approved    = not settings.premoderate

            # Makes reply if parent comment specified
            if parent:
                comment.insert_at(parent, position='last-child', commit=False)

            comment.save()

            if request.user.is_authenticated():
                update_last_readed_comment(request.user, object)

            if request.is_ajax():
                result.update(
                    comment = render_to_string('comments/item.html',{'comment': comment, }, context_instance=RequestContext(request)),
                    parent_id = parent.pk if parent else None,
                    comment_id = comment.pk,
                )

                return HttpResponse(simplejson.dumps(result))

            else:
                url = request.POST.get('redirect_to') or '/'
                return redirect(url)

        else:
            errors=dict()
            for f in form.errors:
                errors[f] = unicode(form.errors[f])
            result.update(errors=errors)

            if request.is_ajax():
                return HttpResponse(simplejson.dumps(result))

    # Add form instance into template context
    result.update(form=form, parent=parent, object=object)

    return render_to_response('comments/create.html', result,
        context_instance=RequestContext(request)
    )
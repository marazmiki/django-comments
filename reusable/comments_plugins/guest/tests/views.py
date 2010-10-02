# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType
from reusable.comments.plugins import get_plugin
from reusable.comments.tests import CommentViewTest, client, reverse
from reusable.comments.tests.models import ContentObject

# --------------------------------------------------------------------------- #

class TestCase(CommentViewTest):
    """
    Базовый класс, содержащий вспомогательные методы тестирования
    """
    def get_full_valid_data(self):
        """
        Возвращает словарь, соответствующий верно заполненной форме
        """
        return dict(
            author       = 'John Joe',
            email        = 'johndoe@31337h4x0rs.org',
            website      = 'http://google.com/',
            content      = 'It is just a test, dude',
            object_id    = self.object.pk,
            content_type = ContentType.objects.get_for_model(self.object).pk,
        )

    def get_data_exclude_fields(self, *fields):
        """
        Исключает из полностью заполненной формы поля, перечиленные в аргументе
        и возвращет новый словарь
        """
        data = self.get_full_valid_data()
        for field in fields:
            if field in data: del data[field]
        return data

# --------------------------------------------------------------------------- #

class GuestNewViewTest(TestCase):
    """
    Набор тестов для отображения comments.views.new
    """
    view_name = 'comments_new'

    def setUp(self):
        super(GuestNewViewTest, self).setUp()
        self.object = ContentObject.objects.create(title='Content Object #1')
        self.plugin = get_plugin('default')
        self.count  = self.plugin.get_model().objects.\
            get_for_object(self.object).count

    def comment_not_posted_because_file_is_empty(self, field):
        """
        Помощник, выполняющий проверку, что комментарий не создаётся,
        если не указано поле field
        """
        data = self.get_data_exclude_fields(field)
        resp = self.post(data)

        self.assertEquals(0, self.count())
        self.assertTrue('form' in resp.context)
        self.assertTrue(field in resp.context['form'].errors)       

    def ajax_comment_not_posted_because_file_is_empty(self, field):
        """
        Помощник, выполняющий проверку, что комментарий не создаётся,
        если не указано поле field при отправке формы через Ajax
        """
        data = self.get_data_exclude_fields(field)

        resp = self.ajax_post(data)
        json = simplejson.loads(resp.content)

        self.assertEquals(0, self.count())
        self.assertFalse(json['success'])
        self.assertTrue(field in json['errors'])   


    def test_comment_posted_successfully_if_form_is_valid(self):
        """
        Проверяет, создаётся ли комментарий про полностью правильно
        заполненной форме
        """
        self.assertEquals(0, self.count())

        resp = self.post(self.get_full_valid_data())
        self.assertEquals(302, resp.status_code)
        self.assertEquals(1, self.count())

    def test_ajax_comment_posted_successfully_if_form_is_valid(self):
        """
        Проверяет, создаётся ли комментарий про полностью правильно
        заполненной форме, переданной через Ajax
        """
        self.assertEquals(0, self.count())

        resp = self.ajax_post(self.get_full_valid_data())
        json = simplejson.loads(resp.content)

        self.assertEquals(200, resp.status_code)
        self.assertEquals(1, self.count())
        self.assertTrue(json['success'])
        self.assertTrue('comment' in json)

    def test_comment_not_posted_because_author_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указано имя автора
        """
        self.comment_not_posted_because_file_is_empty('author')

    def test_comment_not_posted_because_email_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указан email автора
        """
        self.comment_not_posted_because_file_is_empty('email')


    def test_ajax_comment_not_posted_because_author_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указано имя автора
        при отправке комментария через Ajax
        """
        self.ajax_comment_not_posted_because_file_is_empty('author')

    def test_ajax_comment_not_posted_because_email_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указан email автора
        при отправке комментария через Ajax
        """
        self.ajax_comment_not_posted_because_file_is_empty('email')

# --------------------------------------------------------------------------- #

class GuestReplyViewTest(TestCase):
    view_name = 'comments_reply'

    def setUp(self):
        self.client = client.Client()
        self.object = ContentObject.objects.create(title='Content Object #1')
        self.plugin = get_plugin('default')

        model = self.plugin.get_model()

        self.count  = model.objects.get_for_object(self.object).count
        self.parent = model.objects.create(
            author  = 'John Doe',
            email   = 'anonymous@topsecret.com',
            website = 'http://google.com/',
            content = 'This is just a test, dude', 
            content_object = self.object,            
        )

        self.url = reverse(self.view_name, args=[self.parent.pk])
        
    def reply_not_posted_because_file_is_empty(self, field):
        """
        Помощник, выполняющий проверку, что ответ на комментарий не
        создаётся, если не указано поле field
        """
        data = self.get_data_exclude_fields(field)
        resp = self.post(data)

        self.assertEquals(1, self.count())
        self.assertTrue('form' in resp.context)
        self.assertTrue(field in resp.context['form'].errors)      

    def ajax_reply_not_posted_because_file_is_empty(self, field):
        """
        Помощник, выполняющий проверку, что ответ на комментарий не
        создаётся, если не указано поле field при отправке формы через Ajax
        """
        data = self.get_data_exclude_fields(field)

        resp = self.ajax_post(data)
        json = simplejson.loads(resp.content)

        self.assertEquals(1, self.count())
        self.assertFalse(json['success'])
        self.assertTrue('errors' in json)
        self.assertTrue(field in json['errors'])     

    def test_comment_posted_successfully_if_form_is_valid(self):
        """
        Проверяет, создаётся ли комментарий про полностью правильно
        заполненной форме
        """
        self.assertEquals(1, self.count())

        resp = self.post(self.get_full_valid_data())

        self.assertEquals(302, resp.status_code)
        self.assertEquals(2, self.count())
        
    def test_comment_not_posted_because_author_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указано имя автора
        """
        self.reply_not_posted_because_file_is_empty('author')

    def test_comment_not_posted_because_email_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указан email автора
        """
        self.reply_not_posted_because_file_is_empty('email')

    def test_ajax_comment_not_posted_because_author_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указано имя автора
        при отправке формы через Ajax
        """
        self.ajax_reply_not_posted_because_file_is_empty('author')

    def test_ajax_comment_not_posted_because_email_is_empty(self):
        """
        Проверяет, что комментарий не создаётся, если не указан email автора
        при отправке формы через Ajax
        """
        self.ajax_reply_not_posted_because_file_is_empty('email')        
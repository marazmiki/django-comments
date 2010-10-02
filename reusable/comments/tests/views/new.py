# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, client
from reusable.comments.tests.models import ContentObject 

# --------------------------------------------------------------------------- #

class NewViewTest(TestCase):
    url = reverse('comments_new')

    def setUp(self):
        self.client = client.Client()
        self.object = ContentObject.objects.create(title='Test')

    def post(self, data=dict()):
        data.update(
            content_type = ContentType.objects.get_for_model(self.object).pk,
            object_id    = self.object.pk,
        )

        return self.client.post(self.url, data)

    def test_404_if_makes_GET_request(self):
        resp = self.client.get(self.url)
        self.assertEquals(404, resp.status_code)

    def test_200_if_makes_POST_request(self):
        resp = self.post()
        self.assertEquals(200, resp.status_code)
        

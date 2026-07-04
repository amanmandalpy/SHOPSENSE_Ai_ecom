from django.test import TestCase
from seo.models import UrlRedirect

class SEOTestCase(TestCase):
    def test_url_redirect(self):
        UrlRedirect.objects.create(old_path='/old/', new_path='/new/', is_permanent=True)
        response = self.client.get('/old/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, '/new/')

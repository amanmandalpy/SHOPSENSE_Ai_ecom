from django.test import TestCase
from analytics.models import PlatformEvent, EventType
from analytics.services import AnalyticsService

class AnalyticsTestCase(TestCase):
    def test_log_event(self):
        AnalyticsService.log_event(EventType.SEARCH, metadata={'q': 'test'})
        self.assertEqual(PlatformEvent.objects.count(), 1)
        event = PlatformEvent.objects.first()
        self.assertEqual(event.event_type, EventType.SEARCH)
        self.assertEqual(event.metadata['q'], 'test')

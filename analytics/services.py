from .models import PlatformEvent, EventType

class AnalyticsService:
    @staticmethod
    def log_event(event_type, user=None, session_key=None, metadata=None):
        PlatformEvent.objects.create(
            event_type=event_type,
            user=user if user and getattr(user, 'is_authenticated', False) else None,
            session_key=session_key,
            metadata=metadata or {}
        )

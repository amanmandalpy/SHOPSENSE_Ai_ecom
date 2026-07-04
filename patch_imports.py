import os

# Fix imports for AffiliateRedirectService
def replace_import(file_path):
    full_path = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', file_path)
    with open(full_path, 'r') as f: content = f.read()
    content = content.replace("from affiliate.services.redirect_service import AffiliateRedirectService", "from affiliate.redirect_service import AffiliateRedirectService")
    with open(full_path, 'w') as f: f.write(content)

replace_import('affiliate/views.py')
replace_import('tracking/tests.py')

# Restore AnalyticsService
old_analytics_service = """
class AnalyticsService:
    @staticmethod
    def log_event(event_type, user=None, metadata=None):
        from analytics.models import PlatformEvent
        if metadata is None: metadata = {}
        PlatformEvent.objects.create(
            event_type=event_type,
            user=user if getattr(user, 'is_authenticated', False) else None,
            metadata=metadata
        )
"""

with open(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce\analytics\services.py', 'a') as f:
    f.write(old_analytics_service)

print("Imports fixed.")

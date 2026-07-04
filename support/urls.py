from django.urls import path
from .views import HelpCenterView, SupportContactView

urlpatterns = [
    path('', HelpCenterView.as_view(), name='support_home'),
    path('contact/', SupportContactView.as_view(), name='support_contact'),
]

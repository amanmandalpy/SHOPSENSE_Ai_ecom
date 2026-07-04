from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from .models import UrlRedirect

class UrlRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        try:
            redirect_obj = UrlRedirect.objects.get(old_path=path)
            if redirect_obj.is_permanent:
                return HttpResponsePermanentRedirect(redirect_obj.new_path)
            else:
                return HttpResponseRedirect(redirect_obj.new_path)
        except UrlRedirect.DoesNotExist:
            pass
            
        return self.get_response(request)

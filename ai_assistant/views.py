from django.shortcuts import render
from django.views import View
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .services import RecommendationService

@method_decorator(ratelimit(key='ip', rate='10/m', block=True), name='dispatch')
class AskAIAssistantView(View):
    def get(self, request):
        return render(request, 'ai_assistant/chat.html')

    def post(self, request):
        query = request.POST.get('query', '').strip()
        context = {'query': query}
        
        if query:
            # Using Mock provider by default so UI renders properly during validation 
            service = RecommendationService(provider_name='mock')
            response_data = service.get_recommendations(query, user=request.user)
            if "error" in response_data:
                context['error'] = response_data['error']
            else:
                context['ai_response'] = response_data
                
        return render(request, 'ai_assistant/chat.html', context)

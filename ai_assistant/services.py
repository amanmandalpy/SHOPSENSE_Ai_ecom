import time
import json
from .models import AILog, PromptTemplate, PromptCategory
from .providers import MockProvider, OpenAIProvider, GeminiProvider, AnthropicProvider
from search.services import execute_search
from merchant_products.models import MerchantProduct
from .scoring import ShoppingScoreService, ValueBadgeService

class PromptBuilderService:
    @staticmethod
    def build_prompt(user_query, product_data):
        template = PromptTemplate.objects.filter(category=PromptCategory.RECOMMENDATION, is_active=True).first()
        if not template:
            system_prompt = (
                "You are the ShopSense AI Shopping Assistant. "
                "Analyze the provided products against the user's query and return a raw JSON payload with exactly this structure: "
                '{"recommended_products": ["id1", "id2"], "pros_cons": {"id1": {"pros": [], "cons": []}}, "buying_guide": "text", "reason": "text"}'
            )
        else:
            system_prompt = template.content
            
        # Inject context
        context = f"User Query: {user_query}\n\nAvailable Products Context:\n"
        for p in product_data:
            context += f"ID: {p['id']}, Name: {p['name']}, Price: {p['price']}, Brand: {p['brand']}\n"
            
        return system_prompt, context

class RecommendationService:
    def __init__(self, provider_name='mock'):
        if provider_name == 'openai':
            self.provider = OpenAIProvider()
        elif provider_name == 'gemini':
            self.provider = GeminiProvider()
        elif provider_name == 'anthropic':
            self.provider = AnthropicProvider()
        else:
            self.provider = MockProvider()
            
    def get_recommendations(self, user_query, user=None):
        if not user_query or len(user_query) < 3:
            return {"error": "Query too short."}
            
        start_time = time.time()
        
        # 1. Fetch real product data via Search Module
        search_results = execute_search(user_query)[:10]
        
        if not search_results:
            return {"error": "No products found matching your criteria. Try adjusting your query."}
            
        product_data = []
        for p in search_results:
            best_listing = p.merchant_listings.first()
            if best_listing:
                product_data.append({
                    'id': str(best_listing.pk),
                    'name': p.name,
                    'brand': p.brand.name if p.brand else 'Unknown',
                    'price': str(best_listing.current_price)
                })
                
        # 2. Build AI Prompt
        system_prompt, user_prompt = PromptBuilderService.build_prompt(user_query, product_data)
        
        # 3. Request LLM Inference
        try:
            raw_response = self.provider.generate_response(system_prompt, user_prompt)
            parsed = json.loads(raw_response)
        except Exception as e:
            return {"error": f"AI Parsing Error: {str(e)}"}
            
        # 4. Map JSON IDs to real DB Objects and compute scores
        recommended_listings = []
        for list_id in parsed.get("recommended_products", []):
            try:
                listing = MerchantProduct.objects.select_related('product', 'store').get(pk=list_id)
                score = ShoppingScoreService.calculate_score(listing)
                badges = ValueBadgeService.get_badges(score, listing.current_price)
                
                recommended_listings.append({
                    'listing': listing,
                    'score': score,
                    'badges': badges,
                    'pros_cons': parsed.get("pros_cons", {}).get(list_id, {})
                })
            except MerchantProduct.DoesNotExist:
                continue
                
        parsed['mapped_recommendations'] = recommended_listings
        
        # 5. Log the interaction for analytics
        processing_time = int((time.time() - start_time) * 1000)
        AILog.objects.create(
            user=user if user and user.is_authenticated else None,
            user_query=user_query,
            llm_provider=self.provider.__class__.__name__,
            prompt_used=system_prompt + "\n\n" + user_prompt,
            response_content=raw_response,
            processing_time_ms=processing_time
        )
        
        from analytics.services import AnalyticsService
        from analytics.models import EventType
        AnalyticsService.log_event(EventType.AI_QUERY, user=user, metadata={'query': user_query})
        
        return parsed

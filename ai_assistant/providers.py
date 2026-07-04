import abc
import json

class LLMProviderInterface(abc.ABC):
    @abc.abstractmethod
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        pass

class OpenAIProvider(LLMProviderInterface):
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        # Expected integration: import openai; openai.ChatCompletion.create(...)
        raise NotImplementedError("OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")

class GeminiProvider(LLMProviderInterface):
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        # Expected integration: import google.generativeai as genai
        raise NotImplementedError("Gemini API key not configured. Set GEMINI_API_KEY environment variable.")

class AnthropicProvider(LLMProviderInterface):
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        # Expected integration: import anthropic
        raise NotImplementedError("Anthropic API key not configured.")

class MockProvider(LLMProviderInterface):
    """
    A smart mock provider for Sprint Validation to test parsing logic without keys.
    """
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        # Extract the first two product IDs from the prompt to mock a real recommendation
        lines = user_prompt.split('\n')
        product_ids = []
        for line in lines:
            if line.startswith('ID: '):
                pid = line.split(',')[0].replace('ID: ', '').strip()
                product_ids.append(pid)
                
        rec_ids = product_ids[:2] if product_ids else []
        
        response = {
            "recommended_products": rec_ids,
            "pros_cons": {
                pid: {"pros": ["Premium build quality", "Great performance"], "cons": ["Higher price bracket"]}
                for pid in rec_ids
            },
            "buying_guide": "Based on your query, here is an AI analysis. Prioritize models with higher RAM and SSD storage if performance is key. Always check active coupons for the best effective price.",
            "reason": "These products match your budget constraints while offering the strongest specs."
        }
        return json.dumps(response)

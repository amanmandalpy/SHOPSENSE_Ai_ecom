from decimal import Decimal
from offers.services import calculate_best_savings

class ShoppingScoreService:
    @staticmethod
    def calculate_score(merchant_listing):
        """
        Calculates a Shopping Score from 0-100 based on discounts and price dynamics.
        """
        score = 50 # Baseline starting score
        
        savings = calculate_best_savings(merchant_listing)
        discount_percentage = 0
        original = savings['original_price']
        effective = savings['final_effective_price']
        
        if original and original > 0:
            discount_percentage = ((original - effective) / original) * 100
            
        # Add up to 40 points for extreme discounts
        discount_points = min(40, int(discount_percentage * Decimal('1.5')))
        score += discount_points
        
        # Bonus for best sellers
        if merchant_listing.product.is_best_seller:
            score += 10
            
        # Ensure hard constraints [0, 100]
        return max(0, min(100, score))

class ValueBadgeService:
    @staticmethod
    def get_badges(shopping_score, current_price):
        badges = []
        if shopping_score >= 85:
            badges.append("Editor's Choice")
            
        if shopping_score >= 70:
            badges.append("Best Value")
            
        if current_price < Decimal('1500.00') and shopping_score >= 60:
            badges.append("Best Budget")
            
        if current_price > Decimal('10000.00') and shopping_score >= 75:
            badges.append("Best Premium")
            
        return badges

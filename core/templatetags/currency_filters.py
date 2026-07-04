from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'AED': 'AED',
    'SGD': 'S$',
}

@register.filter
def currency_symbol(currency_code):
    """Convert currency code like 'INR' to its symbol '₹'"""
    return CURRENCY_SYMBOLS.get(str(currency_code).upper(), str(currency_code))

@register.filter
def inr(value):
    """Format a number as Indian Rupee: ₹1,23,456.00"""
    try:
        value = float(value)
        # Indian number formatting (lakhs/crores system)
        s = f"{value:,.2f}"
        return f"₹{s}"
    except (ValueError, TypeError):
        return f"₹{value}"

import re

class NormalizationService:
    @staticmethod
    def normalize(raw_data):
        """
        Normalizes raw feed data into a standard format.
        """
        normalized = {
            'sku': NormalizationService._extract(raw_data, ['sku', 'id', 'item_id', 'product_id']),
            'product_name': NormalizationService._extract(raw_data, ['title', 'name', 'product_name']),
            'brand_name': NormalizationService._extract(raw_data, ['brand', 'manufacturer']),
            'category_name': NormalizationService._extract(raw_data, ['category', 'product_category']),
            'description': NormalizationService._extract(raw_data, ['description', 'desc', 'summary']),
            'price': NormalizationService._extract_price(raw_data, ['price', 'current_price', 'sale_price']),
            'original_price': NormalizationService._extract_price(raw_data, ['mrp', 'original_price', 'list_price']),
            'currency': NormalizationService._extract(raw_data, ['currency']) or 'INR',
            'stock': NormalizationService._extract_stock(raw_data, ['stock', 'availability', 'quantity']),
            'url': NormalizationService._extract(raw_data, ['url', 'link', 'product_url']),
            'image_url': NormalizationService._extract(raw_data, ['image', 'image_url', 'picture', 'thumbnail']),
        }
        return normalized

    @staticmethod
    def _extract(data, keys):
        for key in keys:
            # Case insensitive search
            for data_key in data.keys():
                if data_key.lower().strip() == key:
                    val = data[data_key]
                    if val is not None:
                        return str(val).strip()
        return None

    @staticmethod
    def _extract_price(data, keys):
        val = NormalizationService._extract(data, keys)
        if val:
            # Remove currency symbols and commas
            val = re.sub(r'[^\d.]', '', val)
            try:
                return float(val)
            except ValueError:
                pass
        return None

    @staticmethod
    def _extract_stock(data, keys):
        val = NormalizationService._extract(data, keys)
        if val:
            val_lower = val.lower()
            if val_lower in ['in stock', 'instock', 'available', 'yes', 'true', '1']:
                return 'IN_STOCK'
            elif val_lower in ['out of stock', 'outofstock', 'unavailable', 'no', 'false', '0']:
                return 'OUT_OF_STOCK'
            # Check if it's a number
            try:
                if int(val) > 0:
                    return 'IN_STOCK'
                else:
                    return 'OUT_OF_STOCK'
            except ValueError:
                pass
        return 'IN_STOCK' # Default

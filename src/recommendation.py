import pandas as pd
import numpy as np

class PricingEngine:
    """
    Real-time recommendation engine for dynamic pricing based on 
    market conditions and inventory.
    """
    
    def __init__(self, base_price, unit_cost):
        self.base_price = base_price
        self.unit_cost = unit_cost
        
    def recommend_price(self, context):
        """
        Recommends a price based on input variables and business rules.
        
        context keys:
            - inventory_level: int
            - is_holiday: bool
            - competitor_price: float
            - day_of_week: int
        """
        inventory_threshold = 100
        suggested_price = self.base_price
        
        # Rule 1: High Demand / Holiday Premium
        if context.get('is_holiday'):
            suggested_price *= 1.10
            
        # Rule 2: Low Inventory / High Demand (Price up)
        if context.get('inventory_level', 500) < 50:
            suggested_price *= 1.05
            
        # Rule 3: Excess Inventory (Clearance)
        if context.get('inventory_level', 0) > 1000:
            suggested_price *= 0.85
            
        # Rule 4: Competitor Match
        comp_price = context.get('competitor_price')
        if comp_price and comp_price < suggested_price:
            # Match if it doesn't go below cost + 5%
            min_allowable = self.unit_cost * 1.05
            suggested_price = max(comp_price, min_allowable)
            
        # Final Floor check
        suggested_price = max(suggested_price, self.unit_cost * 1.02)
        
        return {
            'recommended_price': round(suggested_price, 2),
            'expected_volume_lift': self._estimate_lift(suggested_price),
            'logic_applied': "Business Rules + Competitor Indexing"
        }
        
    def _estimate_lift(self, price):
        """
        Stub for volume lift estimation.
        In production, this would call the Elasticity model.
        """
        price_diff = (price / self.base_price) - 1
        # Simple assumption: -2.0 elasticity
        return round(-2.0 * price_diff * 100, 2)

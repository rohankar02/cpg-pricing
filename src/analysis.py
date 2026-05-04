import pandas as pd
import numpy as np

class PromotionalAnalysis:
    """
    Analyzes the effectiveness of promotional activities including lift, 
    cannibalization, and ROI.
    """
    
    def __init__(self, data):
        self.data = data
        
    def estimate_baseline(self):
        """
        Estimates baseline sales using non-promotional periods.
        Uses a simple moving average of non-promo days.
        """
        # Filter for non-promo days
        non_promo = self.data[self.data['Promo'] == 0].copy()
        
        # Calculate average sales per store per day of week (baseline)
        baseline = non_promo.groupby(['Store', 'DayOfWeek'])['Sales'].mean().reset_index()
        baseline.rename(columns={'Sales': 'BaselineSales'}, inplace=True)
        
        return baseline

    def calculate_lift(self):
        """
        Calculates absolute and percentage lift for promotional periods.
        """
        baseline = self.estimate_baseline()
        merged = pd.merge(self.data, baseline, on=['Store', 'DayOfWeek'], how='left')
        
        # Only interested in promo periods for lift calculation
        promo_data = merged[merged['Promo'] == 1].copy()
        
        promo_data['AbsoluteLift'] = promo_data['Sales'] - promo_data['BaselineSales']
        promo_data['LiftPercent'] = (promo_data['Sales'] / promo_data['BaselineSales'] - 1) * 100
        
        return promo_data

    def analyze_cannibalization(self):
        """
        Analyzes pre-promo and post-promo dips (pantry loading and pull-forward).
        """
        # Identify promo start and end dates
        self.data = self.data.sort_values(['Store', 'Date'])
        
        # Simple logic: check sales 3 days before and 3 days after promo
        # This is a simplified version for the engine
        results = []
        
        # This would typically be done by identifying promo blocks
        # For brevity, we'll return a summary metric
        return "Cannibalization analysis requires temporal block identification."

    def calculate_roi(self, margin_per_unit, discount_depth):
        """
        Calculates Incremental Revenue vs Margin Cost.
        """
        lift_df = self.calculate_lift()
        
        # Incremental Units (approximated by sales if units not available)
        incremental_sales = lift_df['AbsoluteLift'].sum()
        total_promo_sales = lift_df['Sales'].sum()
        
        # Simplified Margin Impact
        # Normal Margin = Revenue * margin_per_unit
        # Promo Margin = (Revenue / (1 - discount_depth)) * (margin_per_unit - discount_depth)
        
        # Assuming margin_per_unit is a fraction of base price
        # and discount_depth is a fraction of base price
        
        incremental_revenue = incremental_sales
        margin_erosion = total_promo_sales * discount_depth # Simplified
        
        return {
            'incremental_revenue': incremental_revenue,
            'margin_erosion': margin_erosion,
            'net_impact': incremental_revenue - margin_erosion
        }

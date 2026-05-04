import pandas as pd
import numpy as np
from scipy.optimize import minimize
import statsmodels.api as sm

class StrategicPricingEngine:
    """
    CPG Pricing Engine for Promotional Lift & Elasticity Optimization.
    Developed for retail category management and margin optimization.
    """

    def __init__(self, scanner_data='data/train.csv', store_metadata='data/store.csv'):
        self.raw = pd.read_csv(scanner_data, low_memory=False)
        self.meta = pd.read_csv(store_metadata)
        self.df = self._preprocess(self.raw, self.meta)

    def _preprocess(self, raw, meta):
        df = pd.merge(raw, meta, on='Store')
        df['Date'] = pd.to_datetime(df['Date'])
        # Filter for operational days and valid transaction records
        return df[(df['Open'] == 1) & (df['Sales'] > 0)].copy()

    def get_promotional_lift(self):
        """Quantifies incremental volume driven by trade promotions."""
        # Baseline sales established via non-promo period mean (DOW-adjusted)
        baseline = self.df[self.df['Promo'] == 0].groupby('DayOfWeek')['Sales'].mean()
        
        promo_days = self.df[self.df['Promo'] == 1].copy()
        promo_days['expected'] = promo_days['DayOfWeek'].map(baseline)
        
        incremental_units = promo_days['Sales'].sum() - promo_days['expected'].sum()
        lift_factor = (promo_days['Sales'].sum() / promo_days['expected'].sum()) - 1
        
        return {
            "incremental_volume": int(incremental_units),
            "lift_percent": round(lift_factor * 100, 2)
        }

    def estimate_price_elasticity(self, store_id=1):
        """
        Calculates Price Elasticity of Demand.
        
        Logic for interview:
        We look at how much sales (Quantity) change when the Price changes.
        In a 'Log-Log' model, the result tells us the % change in volume 
        for every 1% change in price.
        """
        store_data = self.df[self.df['Store'] == store_id].copy()
        
        # We assume a 20% discount during promotional periods
        store_data['price_index'] = np.where(store_data['Promo'] == 1, 0.8, 1.0)
        
        # Transform data to logarithms
        log_quantity = np.log(store_data['Sales'])
        log_price = np.log(store_data['price_index'])
        
        # Build the statistical model
        X_variables = sm.add_constant(log_price)
        regression_model = sm.OLS(log_quantity, X_variables).fit()
        
        # The 'Elasticity' is the coefficient of the price variable
        self.elasticity = regression_model.params.iloc[1]
        return round(self.elasticity, 4)

    def optimize_margin(self, unit_cost_ratio=0.6, base_price=10.0):
        """
        Finds the price point that maximizes total profit.
        
        Logic for interview: 
        1. We predict volume based on the price.
        2. Profit = (Price - Cost) * Volume.
        3. We use an optimizer to find the price where Profit is highest.
        """
        if not hasattr(self, 'elasticity'):
            self.estimate_price_elasticity()

        unit_cost = base_price * unit_cost_ratio

        def calculate_negative_profit(current_price):
            # Step A: How much volume will we sell at this price?
            # Ratio of new price to old price
            price_ratio = current_price / base_price
            # Volume change based on elasticity
            volume_factor = price_ratio ** self.elasticity
            
            # Step B: What is our margin per unit?
            margin_per_unit = current_price - unit_cost
            
            # Step C: Total Profit
            total_profit = volume_factor * margin_per_unit
            
            # We return negative because the 'minimize' tool looks for the lowest value
            return -total_profit

        # Optimization constrained to +/- 30% of current base price
        search_range = [(base_price * 0.7, base_price * 1.3)]
        result = minimize(calculate_negative_profit, x0=base_price, bounds=search_range)
        
        return {
            "optimal_price": round(result.x[0], 2),
            "margin_impact": round(-result.fun, 4)
        }

if __name__ == "__main__":
    engine = StrategicPricingEngine()
    print(f"Trade Promotion Lift: {engine.get_promotional_lift()['lift_percent']}%")
    print(f"Price Elasticity (S1): {engine.estimate_price_elasticity()}")
    print(f"Optimization Index: {engine.optimize_margin()['optimal_price_index']}")

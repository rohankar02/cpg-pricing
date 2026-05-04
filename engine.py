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
        """Computes price elasticity using a constant-elasticity log-log model."""
        store_data = self.df[self.df['Store'] == store_id].copy()
        
        # Proxy price architecture: 20% promotional discount depth
        store_data['price_index'] = np.where(store_data['Promo'] == 1, 0.8, 1.0)
        
        log_q = np.log(store_data['Sales'])
        log_p = np.log(store_data['price_index'])
        
        # OLS regression where the coefficient is the direct elasticity
        X = sm.add_constant(log_p)
        model = sm.OLS(log_q, X).fit()
        
        self.elasticity = model.params.iloc[1]
        return round(self.elasticity, 4)

    def optimize_margin(self, unit_cost_ratio=0.6, base_price=1.0):
        """Identifies the profit-maximizing price point based on volume sensitivity."""
        if not hasattr(self, 'elasticity'):
            self.estimate_price_elasticity()

        # Profit = [k * P^e] * [P - Cost]
        def _profit(p):
            predicted_volume = (p / base_price) ** self.elasticity
            margin = p - (base_price * unit_cost_ratio)
            return -(predicted_volume * margin)

        # Optimization constrained to +/- 30% of current base price
        res = minimize(_profit, x0=base_price, bounds=[(base_price * 0.7, base_price * 1.3)])
        
        return {
            "optimal_price_index": round(res.x[0], 3),
            "projected_margin_improvement": round(-res.fun, 4)
        }

if __name__ == "__main__":
    engine = StrategicPricingEngine()
    print(f"Trade Promotion Lift: {engine.get_promotional_lift()['lift_percent']}%")
    print(f"Price Elasticity (S1): {engine.estimate_price_elasticity()}")
    print(f"Optimization Index: {engine.optimize_margin()['optimal_price_index']}")

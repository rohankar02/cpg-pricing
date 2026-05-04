import pandas as pd
import numpy as np
from scipy.optimize import minimize
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

class RetailOptimizationEngine:
    """
    Unified engine for CPG Pricing and Promotional Analytics.
    Integrates elasticity modeling, lift decomposition, and optimization.
    """
    
    def __init__(self, train_path='data/train.csv', store_path='data/store.csv'):
        self.data = self._load_data(train_path, store_path)
        self.elasticity_model = None
        
    def _load_data(self, train_path, store_path):
        train = pd.read_csv(train_path, low_memory=False)
        store = pd.read_csv(store_path)
        df = pd.merge(train, store, on='Store')
        df['Date'] = pd.to_datetime(df['Date'])
        return df[df['Open'] != 0]

    def analyze_promo_performance(self, store_id=None):
        """Quantifies promotional lift and baseline sales."""
        df = self.data if store_id is None else self.data[self.data['Store'] == store_id]
        
        # Segment baseline (non-promo) vs promo
        baseline = df[df['Promo'] == 0].groupby(['DayOfWeek'])['Sales'].mean()
        promo_days = df[df['Promo'] == 1].copy()
        
        promo_days['Baseline'] = promo_days['DayOfWeek'].map(baseline)
        promo_days['Lift'] = promo_days['Sales'] - promo_days['Baseline']
        promo_days['Lift_Pct'] = (promo_days['Sales'] / promo_days['Baseline'] - 1) * 100
        
        stats = {
            'avg_lift_pct': promo_days['Lift_Pct'].mean(),
            'total_incremental_sales': promo_days['Lift'].sum(),
            'promo_count': len(promo_days)
        }
        return stats, promo_days

    def fit_elasticity_model(self, store_id=1):
        """Fits a log-log regression to determine price elasticity."""
        df = self.data[self.data['Store'] == store_id].copy()
        df = df[df['Sales'] > 0]
        
        # Simulating price depth based on Promo flag (standard proxy)
        df['Price'] = np.where(df['Promo'] == 1, 8.0, 10.0) 
        
        # Log-Log Transform
        df['log_q'] = np.log(df['Sales'])
        df['log_p'] = np.log(df['Price'])
        
        X = sm.add_constant(df[['log_p', 'DayOfWeek']])
        model = sm.OLS(df['log_q'], X).fit()
        
        self.elasticity = model.params['log_p']
        return self.elasticity, model

    def optimize_pricing(self, unit_cost=6.0, base_price=10.0):
        """Uses elasticity to find the profit-maximizing price point."""
        if not hasattr(self, 'elasticity'):
            self.fit_elasticity_model()
            
        # Objective: Maximize Profit = Volume * (Price - Cost)
        # Volume = k * Price ^ Elasticity
        def objective(p):
            volume = 1000 * (p / base_price)**self.elasticity
            profit = volume * (p - unit_cost)
            return -profit # Minimize negative profit
            
        res = minimize(objective, base_price, bounds=[(unit_cost * 1.1, base_price * 1.5)])
        
        return {
            'optimal_price': res.x[0],
            'expected_margin': -res.fun,
            'elasticity_coefficient': self.elasticity
        }

    def run_full_diagnostic(self):
        """Runs the entire suite and prints a business report."""
        print("="*50)
        print("RETAIL ANALYTICS DIAGNOSTIC REPORT")
        print("="*50)
        
        # Promo Lift
        lift_stats, _ = self.analyze_promo_performance()
        print(f"Promotion Effectiveness:")
        print(f" - Average Volume Lift: {lift_stats['avg_lift_pct']:.2f}%")
        print(f" - Total Incremental Sales: {lift_stats['total_incremental_sales']:,.0f} units")
        
        # Elasticity
        elas, _ = self.fit_elasticity_model(store_id=1)
        print(f"\nPrice Sensitivity (Store 1):")
        print(f" - Elasticity Coefficient: {elas:.4f}")
        
        # Optimization
        opt = self.optimize_pricing()
        print(f"\nPricing Recommendation:")
        print(f" - Recommended Price: £{opt['optimal_price']:.2f}")
        print(f" - Strategy: {'Premium' if opt['optimal_price'] > 10 else 'Volume-Driven'}")
        print("="*50)

if __name__ == "__main__":
    engine = RetailOptimizationEngine()
    engine.run_full_diagnostic()

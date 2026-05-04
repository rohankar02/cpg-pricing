import pandas as pd
import numpy as np
from scipy.optimize import minimize
import statsmodels.api as sm

class PricingOptimizer:
    """
    CPG Pricing & Promotion Engine
    Designed for: Promotional Lift Analysis & Optimal Price Discovery
    """

    def __init__(self, data_path='data/train.csv', store_path='data/store.csv'):
        # Load and combine retail scanner data
        train = pd.read_csv(data_path, low_memory=False)
        stores = pd.read_csv(store_path)
        self.df = pd.merge(train, stores, on='Store')
        
        # Data Cleaning: focus on active days with valid sales
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df[(self.df['Open'] == 1) & (self.df['Sales'] > 0)]

    def calculate_promotional_lift(self):
        """
        MODULE 1: Promotional Effectiveness
        Calculates the incremental volume driven by promotions.
        """
        # 1. Establish Baseline (Sales when no promo is active)
        # We group by DayOfWeek to account for natural weekly seasonality
        baseline_sales = self.df[self.df['Promo'] == 0].groupby('DayOfWeek')['Sales'].mean()
        
        # 2. Compare Promo days against Baseline
        promo_data = self.df[self.df['Promo'] == 1].copy()
        promo_data['baseline_expected'] = promo_data['DayOfWeek'].map(baseline_sales)
        
        # 3. Calculate Lift Metrics
        total_promo_sales = promo_data['Sales'].sum()
        total_baseline_sales = promo_data['baseline_expected'].sum()
        
        lift_percent = (total_promo_sales / total_baseline_sales - 1) * 100
        incremental_units = total_promo_sales - total_baseline_sales
        
        return {
            "lift_percentage": round(lift_percent, 2),
            "incremental_sales_volume": round(incremental_units, 0)
        }

    def estimate_price_elasticity(self, store_id=1):
        """
        MODULE 2: Price Elasticity Modeling
        Uses Log-Log Regression to find the Price Elasticity of Demand.
        Interpretation: A 1% change in price leads to a 'Beta'% change in volume.
        """
        # Filter for specific store
        store_df = self.df[self.df['Store'] == store_id].copy()
        
        # Feature Engineering: 
        # Since price isn't direct, we proxy it: 10.0 base, 8.0 during Promo (20% discount)
        store_df['price'] = np.where(store_df['Promo'] == 1, 8.0, 10.0)
        
        # Log Transformations (Standard for Constant Elasticity Models)
        log_q = np.log(store_df['Sales'])
        log_p = np.log(store_df['price'])
        
        # Add Constant (Intercept) and fit OLS Regression
        X = sm.add_constant(log_p)
        model = sm.OLS(log_q, X).fit()
        
        # The coefficient of log_p is the Elasticity
        self.elasticity = model.params.iloc[1]
        return round(self.elasticity, 4)

    def find_optimal_price(self, unit_cost=6.0):
        """
        MODULE 3: Profit Optimization
        Calculates the price point that maximizes Total Profit.
        Profit = [Volume at Price P] * [Price P - Unit Cost]
        """
        if not hasattr(self, 'elasticity'):
            self.estimate_price_elasticity()

        # Define the Profit Function to maximize
        def profit_function(price):
            base_price = 10.0
            base_volume = 1000 # Reference volume
            
            # Predict Volume using Elasticity formula: V = k * P^e
            predicted_volume = base_volume * (price / base_price)**self.elasticity
            margin = price - unit_cost
            
            return -(predicted_volume * margin) # Negative for minimization

        # Use Scipy to find the optimal price within a reasonable range
        result = minimize(profit_function, x0=10.0, bounds=[(unit_cost * 1.1, 15.0)])
        
        return {
            "optimal_price": round(result.x[0], 2),
            "estimated_profit_max": round(-result.fun, 2)
        }

if __name__ == "__main__":
    # Initialize Engine
    engine = PricingOptimizer()
    
    # 1. Analysis
    lift = engine.calculate_promotional_lift()
    print(f"Promo Lift: {lift['lift_percentage']}%")
    
    # 2. Modeling
    elasticity = engine.estimate_price_elasticity()
    print(f"Price Elasticity: {elasticity}")
    
    # 3. Optimization
    opt = engine.find_optimal_price()
    print(f"Recommended Price: £{opt['optimal_price']}")

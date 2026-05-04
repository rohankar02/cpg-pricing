import pandas as pd
import numpy as np
import statsmodels.api as sm

class StrategicPricingEngine:
    """
    Advanced Retail Analytics Suite: Promotional Lift & Price Elasticity
    Integrates regression-based elasticity modeling with margin simulation.
    """

    def __init__(self, data_path='data/train.csv', meta_path='data/store.csv'):
        # 1. Ingest scanner data and store metadata
        train = pd.read_csv(data_path, low_memory=False)
        meta = pd.read_csv(meta_path)
        
        # 2. Merge and pre-process for temporal analysis
        self.df = pd.merge(train, meta, on='Store')
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df[(self.df['Open'] == 1) & (self.df['Sales'] > 0)]

    def analyze_promo_lift(self):
        """
        Quantifies the incremental impact of trade promotions.
        Uses a Day-of-Week adjusted baseline to isolate organic demand.
        """
        # Baseline = mean sales per DayOfWeek during non-promo periods
        baseline = self.df[self.df['Promo'] == 0].groupby('DayOfWeek')['Sales'].mean()
        
        promo_days = self.df[self.df['Promo'] == 1].copy()
        promo_days['expected'] = promo_days['DayOfWeek'].map(baseline)
        
        lift = (promo_days['Sales'].sum() / promo_days['expected'].sum() - 1) * 100
        return round(lift, 2)

    def model_price_elasticity(self, store_id=1):
        """
        Estimates elasticity using a Regression-based approach.
        We use a Log-Log OLS model to capture constant price elasticity.
        Interpretation: The coefficient 'Beta' represents the % volume change 
        for a 1% price change.
        """
        subset = self.df[self.df['Store'] == store_id].copy()
        
        # Feature Engineering: Price proxy (Promo=1 implies 20% discount architecture)
        subset['price_index'] = np.where(subset['Promo'] == 1, 0.8, 1.0)
        
        # Log Transformations for Elasticity Modeling
        log_q = np.log(subset['Sales'])
        log_p = np.log(subset['price_index'])
        
        # Statistical Regression: Log(Quantity) ~ Log(Price) + Seasonality(DayOfWeek)
        # Adding DayOfWeek controls for weekly fluctuations
        X = sm.add_constant(pd.concat([log_p, subset['DayOfWeek']], axis=1))
        model = sm.OLS(log_q, X).fit()
        
        # Extract the coefficient for the price variable
        self.elasticity = model.params.iloc[1]
        return round(self.elasticity, 4)

    def optimize_price_architecture(self, unit_cost=6.0, base_price=10.0):
        """
        Identifies the optimal price point to maximize margin.
        Uses a simulation-based grid search over the predicted demand curve.
        """
        if not hasattr(self, 'elasticity'):
            self.model_price_elasticity()

        base_volume = self.df[self.df['Promo'] == 0]['Sales'].mean()
        
        simulation_results = []
        
        # Scenario Modeling: Test price points from -30% to +30% of base
        for test_price in np.arange(base_price * 0.7, base_price * 1.3, 0.1):
            # 1. Predict volume using the derived elasticity coefficient
            price_ratio = test_price / base_price
            predicted_volume = base_volume * (price_ratio ** self.elasticity)
            
            # 2. Calculate Profitability
            margin = test_price - unit_cost
            total_profit = predicted_volume * margin
            
            simulation_results.append({'price': test_price, 'profit': total_profit})
            
        # Select the price point that maximizes total margin
        best_scenario = max(simulation_results, key=lambda x: x['profit'])
        return {
            "optimal_price": round(best_scenario['price'], 2),
            "elasticity_coefficient": round(self.elasticity, 4)
        }

if __name__ == "__main__":
    engine = StrategicPricingEngine()
    print(f"I. Promotional Lift (DOW-Adjusted): {engine.analyze_promo_lift()}%")
    print(f"II. Price Elasticity (Regression-Based): {engine.model_price_elasticity()}")
    opt = engine.optimize_price_architecture()
    print(f"III. Recommended Price: £{opt['optimal_price']}")

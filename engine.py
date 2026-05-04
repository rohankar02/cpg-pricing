import pandas as pd
import numpy as np

class PricingEngine:
    """
    Retail Strategy Tool: Promotional Lift & Pricing Optimizer
    Simplified version for transparent business logic.
    """

    def __init__(self, data_path='data/train.csv', meta_path='data/store.csv'):
        # 1. Load data
        train = pd.read_csv(data_path, low_memory=False)
        meta = pd.read_csv(meta_path)
        
        # 2. Merge and clean
        self.df = pd.merge(train, meta, on='Store')
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df[(self.df['Open'] == 1) & (self.df['Sales'] > 0)]

    def get_promo_impact(self):
        """
        Calculates how much 'Extra' sales we get from a promotion.
        Logic: Compare Promo days to Non-Promo days.
        """
        # Average sales when there is NO promo
        avg_normal_sales = self.df[self.df['Promo'] == 0]['Sales'].mean()
        
        # Average sales when there IS a promo
        avg_promo_sales = self.df[self.df['Promo'] == 1]['Sales'].mean()
        
        lift = (avg_promo_sales / avg_normal_sales - 1) * 100
        return round(lift, 1)

    def calculate_elasticity(self):
        """
        Measures Price Sensitivity.
        Logic: If we drop price by 20%, by what % does volume go up?
        """
        # We assume Promo is a 20% discount (Price goes from 1.0 to 0.8)
        price_change = -0.20 
        
        # Calculate volume change
        normal_vol = self.df[self.df['Promo'] == 0]['Sales'].mean()
        promo_vol = self.df[self.df['Promo'] == 1]['Sales'].mean()
        volume_change = (promo_vol / normal_vol - 1)
        
        # Elasticity = % Change in Volume / % Change in Price
        self.elasticity = volume_change / price_change
        return round(self.elasticity, 2)

    def find_best_price(self, unit_cost=6.0):
        """
        Finds the most profitable price point.
        Logic: Test different prices and see which one makes the most money.
        """
        if not hasattr(self, 'elasticity'):
            self.calculate_elasticity()

        base_price = 10.0
        base_volume = self.df[self.df['Promo'] == 0]['Sales'].mean()
        
        best_profit = 0
        best_price = 0
        
        # TEST EVERY PRICE from £7.00 to £13.00 (in 10p steps)
        for test_price in np.arange(7.0, 13.0, 0.1):
            # 1. Predict how many we will sell at this price
            price_ratio = test_price / base_price
            # Volume formula: V = V0 * (1 + elasticity * %PriceChange)
            # (Simplified linear version for easy explanation)
            pct_change_in_price = (test_price - base_price) / base_price
            predicted_volume = base_volume * (1 + self.elasticity * pct_change_in_price)
            
            # 2. Calculate Profit
            margin = test_price - unit_cost
            current_profit = predicted_volume * margin
            
            # 3. Keep track of the winner
            if current_profit > best_profit:
                best_profit = current_profit
                best_price = test_price
                
        return round(best_price, 2)

if __name__ == "__main__":
    engine = PricingEngine()
    print(f"1. Promo Lift: {engine.get_promo_impact()}%")
    print(f"2. Price Sensitivity: {engine.calculate_elasticity()}")
    print(f"3. Optimal Price Point: £{engine.find_best_price()}")
    print("\nExplain this: 'I analyzed historical data to find that customers are very sensitive to price (Elasticity).")
    print("I then simulated 60 different price points to find the one that maximizes our total margin.'")

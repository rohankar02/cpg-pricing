import numpy as np
from scipy.optimize import minimize

class PromoOptimizer:
    """
    Optimizes promotional frequency and depth to maximize margin.
    """
    
    def __init__(self, elasticity, base_price, base_volume, unit_cost):
        self.elasticity = elasticity
        self.base_price = base_price
        self.base_volume = base_volume
        self.unit_cost = unit_cost
        
    def predict_volume(self, new_price):
        """
        Predicts volume based on price elasticity.
        V1 = V0 * (P1/P0) ^ elasticity
        """
        volume = self.base_volume * (new_price / self.base_price) ** self.elasticity
        return volume

    def calculate_profit(self, price):
        """
        Calculates total profit at a given price point.
        """
        volume = self.predict_volume(price)
        margin = price - self.unit_cost
        return volume * margin

    def find_optimal_discount(self):
        """
        Finds the discount depth that maximizes profit.
        """
        # Objective function to minimize (negative profit)
        objective = lambda p: -self.calculate_profit(p)
        
        # Constraints: Price must be between 50% and 100% of base price
        bounds = [(self.base_price * 0.5, self.base_price)]
        
        result = minimize(objective, self.base_price * 0.8, bounds=bounds)
        
        optimal_price = result.x[0]
        optimal_discount = (1 - optimal_price / self.base_price) * 100
        
        return {
            'optimal_price': optimal_price,
            'optimal_discount_percent': optimal_discount,
            'max_profit': -result.fun
        }

    def run_scenario(self, discount_depth=0.15):
        """
        Runs a specific promo scenario.
        """
        promo_price = self.base_price * (1 - discount_depth)
        predicted_volume = self.predict_volume(promo_price)
        profit = predicted_volume * (promo_price - self.unit_cost)
        
        return {
            'discount_depth': discount_depth,
            'predicted_volume': predicted_volume,
            'expected_profit': profit
        }

    def run_scenarios(self):
        """
        Runs the specific scenarios requested by business.
        """
        scenarios = {
            "Base Case (20% Discount)": self.run_scenario(discount_depth=0.20),
            "Scenario 1 (15% Discount)": self.run_scenario(discount_depth=0.15),
            "Scenario 2 (Higher Volume/Lower Discount)": self.run_scenario(discount_depth=0.10)
        }
        return scenarios

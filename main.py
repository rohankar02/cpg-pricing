import pandas as pd
import numpy as np
from src.analysis import PromotionalAnalysis
from src.modeling import PriceElasticityModel
from src.optimization import PromoOptimizer
from src.recommendation import PricingEngine

def load_and_preprocess():
    """Loads and merges the Rossmann dataset."""
    train = pd.read_csv('data/train.csv', low_memory=False)
    store = pd.read_csv('data/store.csv')
    
    # Merge and simple cleaning
    df = pd.merge(train, store, on='Store')
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter for open stores and non-zero sales
    df = df[(df['Open'] != 0) & (df['Sales'] > 0)]
    
    return df

def run_pipeline():
    print("--- CPG Pricing & Promo Engine ---")
    
    # 1. Load Data
    data = load_and_preprocess()
    print(f"Loaded {len(data)} observations.")
    
    # 2. Promotional Analysis
    analyzer = PromotionalAnalysis(data)
    lift_results = analyzer.calculate_lift()
    avg_lift = lift_results['LiftPercent'].mean()
    print(f"Average Promotional Lift: {avg_lift:.2f}%")
    
    # 3. Price Elasticity
    modeler = PriceElasticityModel(data)
    # Estimate elasticity for Store 1
    store1_results = modeler.fit_elasticity(segment_col='Store', segment_val=1)
    elasticity = store1_results['elasticity']
    print(f"Price Elasticity for Store 1: {elasticity:.4f}")
    
    # 4. Optimization
    # Assume base price 10, volume 1000, cost 6
    optimizer = PromoOptimizer(elasticity=elasticity, base_price=10.0, 
                               base_volume=1000, unit_cost=6.0)
    opt_results = optimizer.find_optimal_discount()
    print(f"Optimal Discount Depth: {opt_results['optimal_discount_percent']:.2f}%")
    
    # 5. Dynamic Pricing Recommendation
    engine = PricingEngine(base_price=10.0, unit_cost=6.0)
    context = {
        'inventory_level': 1200,
        'is_holiday': True,
        'competitor_price': 8.50
    }
    rec = engine.recommend_price(context)
    print(f"Recommended Price for Current Context: £{rec['recommended_price']}")
    print(f"Logic: {rec['logic_applied']}")

if __name__ == "__main__":
    run_pipeline()

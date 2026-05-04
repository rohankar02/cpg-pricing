import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from engine import StrategicPricingEngine

# Set professional plotting style
plt.style.use('ggplot')
sns.set_palette("viridis")

def generate_insights():
    """
    Generates strategic visualizations for the Pricing Engine results.
    """
    engine = StrategicPricingEngine()
    
    # 1. Model Elasticity and Run Optimization
    elasticity = engine.model_price_elasticity(store_id=1)
    opt = engine.optimize_price_architecture(unit_cost=6.0, base_price=10.0)
    
    # 2. Simulate Demand Curve Data
    prices = np.arange(7.0, 14.0, 0.1)
    base_vol = engine.df[engine.df['Promo'] == 0]['Sales'].mean()
    
    volumes = [base_vol * ((p / 10.0) ** elasticity) for p in prices]
    profits = [v * (p - 6.0) for p, v in zip(prices, volumes)]
    
    # --- VIZ 1: Demand Curve ---
    plt.figure(figsize=(10, 6))
    plt.plot(prices, volumes, color='tab:blue', linewidth=2, label='Demand Curve')
    plt.axvline(x=10.0, color='gray', linestyle='--', label='Current Price (£10)')
    plt.axvline(x=opt['optimal_price'], color='tab:green', linestyle='-', linewidth=2, label=f'Optimal Price (£{opt["optimal_price"]})')
    
    plt.title('Demand Curve: Volume vs Price Sensitivity', fontsize=14)
    plt.xlabel('Price (£)', fontsize=12)
    plt.ylabel('Projected Volume (Units)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('visualizations/demand_curve.png')
    print("✓ Saved demand_curve.png")

    # --- VIZ 2: Profit Optimization ---
    plt.figure(figsize=(10, 6))
    plt.plot(prices, profits, color='tab:green', linewidth=2, label='Profit Function')
    plt.fill_between(prices, profits, color='tab:green', alpha=0.1)
    plt.scatter(opt['optimal_price'], max(profits), color='red', zorder=5, label='Max Profit Point')
    
    plt.title('Profit Optimization: Finding the Mathematical Sweet Spot', fontsize=14)
    plt.xlabel('Price (£)', fontsize=12)
    plt.ylabel('Total Projected Margin (£)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('visualizations/profit_optimization.png')
    print("✓ Saved profit_optimization.png")

    # --- VIZ 3: Promo Lift ---
    lift = engine.analyze_promo_lift()
    plt.figure(figsize=(8, 6))
    categories = ['Baseline (Organic)', 'Promotional (Trade)']
    values = [100, 100 + lift] # Indexed for visualization
    
    sns.barplot(x=categories, y=values, palette=['#95a5a6', '#2ecc71'])
    plt.title(f'Promotional Lift Analysis: +{lift}% Incremental Volume', fontsize=14)
    plt.ylabel('Indexed Volume (Base=100)', fontsize=12)
    plt.savefig('visualizations/promo_lift.png')
    print("✓ Saved promo_lift.png")

if __name__ == "__main__":
    import os
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')
    
    print("Generating strategic visualizations...")
    generate_insights()
    print("\nVisualizations complete. Files available in the /visualizations folder.")

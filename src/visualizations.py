import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_elasticity(price_points, volumes, optimal_price=None):
    """
    Plots the demand curve and highlights the optimal price.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=price_points, y=volumes, marker='o', label='Demand Curve')
    
    if optimal_price:
        plt.axvline(x=optimal_price, color='r', linestyle='--', label=f'Optimal Price: £{optimal_price:.2f}')
        
    plt.title('Demand Curve & Price Elasticity Visualization')
    plt.xlabel('Price (£)')
    plt.ylabel('Projected Volume')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_promo_lift(promo_sales, baseline_sales):
    """
    Visualizes lift vs baseline.
    """
    labels = ['Baseline Sales', 'Promo Sales']
    values = [baseline_sales, promo_sales]
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=labels, y=values, palette='viridis')
    plt.title('Promotional Lift Comparison')
    plt.ylabel('Sales Volume')
    
    lift = (promo_sales / baseline_sales - 1) * 100
    plt.annotate(f'+{lift:.1f}% Lift', xy=(1, promo_sales), ha='center', va='bottom', fontsize=12, fontweight='bold')
    plt.show()

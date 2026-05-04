import pandas as pd
import numpy as np
from scipy.optimize import minimize
import statsmodels.api as sm
import warnings

warnings.filterwarnings('ignore')

class RetailEngine:
    def __init__(self, data_path='data/train.csv', store_path='data/store.csv'):
        # Merge datasets on 'Store' and filter for operational records
        self.raw = pd.read_csv(data_path, low_memory=False)
        self.stores = pd.read_csv(store_path)
        self.df = pd.merge(self.raw, self.stores, on='Store')
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df[self.df['Open'] == 1]

    def lift_analysis(self, sid=None):
        data = self.df if sid is None else self.df[self.df['Store'] == sid]
        # Baseline = mean sales per DayOfWeek during non-promo periods
        base_map = data[data['Promo'] == 0].groupby('DayOfWeek')['Sales'].mean().to_dict()
        
        promo = data[data['Promo'] == 1].copy()
        promo['baseline'] = promo['DayOfWeek'].map(base_map)
        promo['incremental'] = promo['Sales'] - promo['baseline']
        
        return {
            'lift_pct': (promo['Sales'].sum() / promo['baseline'].sum() - 1) * 100,
            'total_incremental': promo['incremental'].sum(),
            'observations': len(promo)
        }

    def compute_elasticity(self, sid=1):
        # Extract store data and simulate price variation (Promo=1 -> 20% discount)
        subset = self.df[(self.df['Store'] == sid) & (self.df['Sales'] > 0)].copy()
        subset['price'] = np.where(subset['Promo'] == 1, 8.0, 10.0)
        
        # Log-log regression for constant elasticity
        y, X = np.log(subset['Sales']), sm.add_constant(np.log(subset['price']))
        model = sm.OLS(y, X).fit()
        
        self.beta = model.params.iloc[1]
        return self.beta

    def optimize(self, cost=6.0, base_p=10.0):
        if not hasattr(self, 'beta'): self.compute_elasticity()
        
        # Profit = k * P^beta * (P - cost)
        func = lambda p: -( (p/base_p)**self.beta * (p - cost) )
        res = minimize(func, base_p, bounds=[(cost*1.05, base_p*1.5)])
        
        return {'opt_price': res.x[0], 'coeff': self.beta}

    def report(self):
        print(f"--- RETAIL OPTIMIZATION SUITE ---")
        l = self.lift_analysis()
        print(f"System Lift: {l['lift_pct']:.1f}%")
        
        e = self.compute_elasticity(sid=1)
        print(f"Price Elasticity (S1): {e:.3f}")
        
        o = self.optimize()
        print(f"Rec Price: £{o['opt_price']:.2f}")

if __name__ == '__main__':
    RetailEngine().report()

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder

class PriceElasticityModel:
    """
    Builds log-log regression models to estimate price elasticity of demand.
    """
    
    def __init__(self, data):
        self.data = data.copy()
        
    def prepare_features(self):
        """
        Feature engineering for elasticity modeling.
        Simulates price depth if not present.
        """
        # Ensure Sales > 0 for log transformation
        self.data = self.data[self.data['Sales'] > 0].copy()
        
        # Simulate Price if not present (Rossmann specific)
        # Assuming a base price of 10 and 20% discount during promos
        if 'Price' not in self.data.columns:
            self.data['Price'] = 10.0
            self.data.loc[self.data['Promo'] == 1, 'Price'] = 8.0
            
        # Log transformations
        self.data['log_sales'] = np.log(self.data['Sales'])
        self.data['log_price'] = np.log(self.data['Price'])
        
        return self.data

    def fit_elasticity(self, segment_col=None, segment_val=None):
        """
        Fits log-log regression: log(Sales) = b0 + b1*log(Price) + ...
        b1 is the price elasticity.
        """
        df = self.prepare_features()
        
        if segment_col and segment_val:
            df = df[df[segment_col] == segment_val]
            
        if df.empty:
            return None
            
        # Independent variables
        X = df[['log_price', 'Promo', 'DayOfWeek']]
        X = sm.add_constant(X)
        y = df['log_sales']
        
        model = sm.OLS(y, X).fit()
        
        elasticity = model.params['log_price']
        
        return {
            'elasticity': elasticity,
            'model_summary': model.summary(),
            'params': model.params
        }

    def segment_elasticity(self, column='StoreType'):
        """
        Calculates elasticity for different segments (e.g., Store types).
        """
        segments = self.data[column].unique()
        results = {}
        
        for seg in segments:
            res = self.fit_elasticity(column, seg)
            if res:
                results[seg] = res['elasticity']
                
        return results

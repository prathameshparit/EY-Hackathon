# Importing dependancies
import numpy as np
import pandas as pd

# Generating Dummy Data
np.random.seed(0)  # for reproducibility

# Sample size
n_samples = 1000

# Dummy features
market_trend = np.random.choice(['positive', 'neutral', 'negative'], n_samples)
competitor_pricing = np.random.choice(['high', 'medium', 'low'], n_samples)
supply_demand = np.random.choice(['high_supply_low_demand', 'balanced', 'low_supply_high_demand'], n_samples)

# Randomly generated target variable (price_fluctuation_factor)
price_fluctuation_factor = np.random.uniform(0.8, 1.5, n_samples)

# Creating DataFrame
data = pd.DataFrame({
    'Market_Trend': market_trend,
    'Competitor_Pricing': competitor_pricing,
    'Supply_Demand': supply_demand,
    'Price_Fluctuation_Factor': price_fluctuation_factor
})

# data.head()
data.to_csv('pricing_data.csv')
# Importing dependanices
import joblib
import pandas as pd

from datetime import datetime
from PriceFluctuation import PriceFluctuationModel


class PricingCalculator:
    def __init__(self, base_price, model='model_price_fluctuation.pkl'):
        # Initialization
        self.model_filename = model
        model = PriceFluctuationModel()

        self.base_price = base_price
        self.model = model  # Instance of PriceFluctuationModel
        self.price_fluctuation_factor = 1  # Initial value

    def update_price_fluctuation_factor(self, market_trend, competitor_pricing, supply_demand):
        """
        Updates the price fluctuation factor based on current market conditions.

        :param market_trend: Current market trend.
        :param competitor_pricing: Current competitor pricing.
        :param supply_demand: Current supply-demand balance.
        """
        
        self.model.load_model(self.model_filename)
        encoder = joblib.load('encoder_price_fluctuation.pkl')
        sample_input = pd.DataFrame({
            'Market_Trend': [market_trend],
            'Competitor_Pricing': [competitor_pricing],
            'Supply_Demand': [supply_demand]
        })

        self.price_fluctuation_factor = self.model.predict(sample_input, encoder)[0]

    def calculate_seasonal_factor(self, current_month=None):
        if not current_month: current_month = datetime.now().month
        seasonal_factors = {
            1: 1.1, 2: 1.05, 3: 1.0, 4: 1.0, 5: 1.1, 6: 1.15, 7: 1.2,
            8: 1.15, 9: 1.05, 10: 1.0, 11: 1.2, 12: 1.3
        }
        return seasonal_factors.get(current_month, 1)

    def calculate_final_price(self, current_month=None):
        """
        Calculates the final price based on the base price, seasonal factor, and price fluctuation factor.
        """
        seasonal_factor = self.calculate_seasonal_factor(current_month)
        return self.base_price * seasonal_factor * self.price_fluctuation_factor


if __name__ == '__main__':
    # # Features
    # features = {
    #     'market_trend': ['positive', 'neutral', 'negative'],
    #     'competitor_pricing': ['high', 'medium', 'low'],
    #     'supply_demand': ['high_supply_low_demand', 'balanced', 'low_supply_high_demand']
    # }

    # Example of using PricingCalculator with the model
    model = 'model_price_fluctuation.pkl'
    base_price = 100
    pricing_calculator = PricingCalculator(base_price, model)

    # Update the price fluctuation factor based on market conditions
    pricing_calculator.update_price_fluctuation_factor('positive', 'high', 'low_supply_high_demand')
    # print(pricing_calculator.price_fluctuation_factor)

    # Calculate the final price
    final_price = pricing_calculator.calculate_final_price(1)
    print(final_price)
    # 127.40234375000001

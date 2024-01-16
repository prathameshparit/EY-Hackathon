# Imporing dependancies
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class PriceFluctuationModel:
    def __init__(self):
        # The linear regression model
        self.model = None
        # One-hot encoder for categorical data
        self.encoder = OneHotEncoder(sparse=False)

    def save_model(self, filename):
        # Save the trained model to a file
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        # Load the model from a file
        self.model = joblib.load(filename)

    def train(self, X, y, model_filename='model_price_fluctuation.pkl'):
        # Check if the model file exists to avoid retraining
        try:
            self.load_model(model_filename)
            print("Model loaded from file.")
        except FileNotFoundError:
            print("Training new model.")
            # One-hot encoding for categorical features
            X_encoded = self.encoder.fit_transform(X)
            joblib.dump(self.encoder, 'encoder_price_fluctuation.pkl')
            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=0)
            # Initialize and train the model
            self.model = LinearRegression()
            self.model.fit(X_train, y_train)
            # Save the trained model
            self.save_model(model_filename)
            # Evaluate the model
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            return mse

    # def predict(self, input_features):
    #     # One-hot encoding for the input features
    #     input_encoded = self.encoder.transform(input_features)
    #     # Predict and return the output
    #     return self.model.predict(input_encoded)
        
    def predict(self, input_features, encoder):
        # Ensure input_features is a DataFrame
        if not isinstance(input_features, pd.DataFrame):
            raise ValueError("Input features should be a pandas DataFrame")

        # One-hot encoding for the input features
        input_encoded = encoder.transform(input_features)
        # Predict and return the output
        return self.model.predict(input_encoded)
    

if __name__ == '__main__':
    # Creating an instance of the PriceFluctuationModel
    model = PriceFluctuationModel()
    data = pd.read_csv('pricing_data.csv')

    # Prepare data for training
    # feature_columns = ['Market_Trend', 'Competitor_Pricing', 'Supply_Demand']
    # X = data[feature_columns]
    # y = data['Price_Fluctuation_Factor']

    # # Train the model and get the mean squared error
    # mse = model.train(X, y)
    # print(f'Mean Squared Error: {mse}')

    # Example
    model_filename = 'model_price_fluctuation.pkl'
    model.load_model(model_filename)
    encoder = joblib.load('encoder_price_fluctuation.pkl')
    sample_input = pd.DataFrame({
        'Market_Trend': ['positive'],
        'Competitor_Pricing': ['medium'],
        'Supply_Demand': ['balanced']
    })

    prediction = model.predict(sample_input, encoder)[0]
    print(prediction)

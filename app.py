# ---------------------------------- Inventory Stock Prediction Individual Product --------------------------------------

from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import json

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained XGBoost model and preprocessing steps
model = joblib.load('xgb_model_new.pkl')

# Define the preprocessing steps
numerical_cols = ['buying_price', 'selling_price', 'bought_quantity', 'current_quantity']
categorical_cols = ['product_name']  # Replace with your actual categorical columns

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

@app.route('/IM_products')
def items():
    json_data = read_json_file('stock_data.json')
    return render_template('items.html', json_data=json_data)

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

@app.route('/get_product/<int:product_id>')
def get_product(product_id):
    products = read_json_file('stock_data.json')
    product = [product for product in products if product["id"] == product_id]
    return jsonify(product)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        input_data = request.json

        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data], columns=['buying_price', 'selling_price', 'bought_quantity', 'current_quantity', 'rate_of_returns', 'shelf_life', 'turnover_rate', 'supplier_lead_time', 'transportation_cost', 'previous_restock_time'])

        # Make predictions
        predictions = model.predict(input_df)

        # Return predictions as JSON
        return jsonify({'predictions': predictions.tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/list")
def list():
    df = pd.read_csv('inventory_management.csv')
    data = df.to_dict(orient='records')
    return render_template('list.html', data=data)

# if __name__ == '__main__':
#     app.run(debug=True)


# -------------------------------- Inventory Place or Not Data ----------------------------------

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_image = db.Column(db.String(255))
    product_name = db.Column(db.String(255), nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    payment = db.Column(db.String(50), nullable=False)
    product_description = db.Column(db.Text)

@app.route('/inventory_order_data')
def inventory_order_data():
    orders = Order.query.all()
    return render_template('inventory_order_data.html', orders=orders)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        new_order = Order(
            product_image=request.form['product_image'],
            product_name=request.form['product_name'],
            customer_name=request.form['customer_name'],
            price=float(request.form['price']),
            quantity=int(request.form['quantity']),
            category=request.form['category'],
            address=request.form['address'],
            phone=request.form['phone'],
            email=request.form['email'],
            payment=request.form['payment'],
            product_description=request.form['product_description']
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_order.html')

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Order.query.get(product_id)
    if product:
        return render_template('product_details.html', product=product)
    else:
        return "Product not found", 404




# ----------------------------- Vendor Data ------------------------------------------
    

from flask import Flask, render_template
import csv

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

@app.route('/vendor_risk_data')
def vendor_data():
    data = read_csv('vendorManagement.csv')
    print(data[0])
    return render_template('vendor_data.html', data=data)

# --------------------------- Dashboards ---------------------------------------------------


@app.route('/inventory_management_dashboard')
def inventory_management_dashboard():
    inventory_data = [
        {
            "name": "Inventory Stock", "children": [
                {"name": "Men's Clothing", "children": [
                    {"name": "Shirts", "value": 50000},
                    {"name": "Trousers", "value": 40000},
                    {"name": "Jackets", "value": 35000},
                    {"name": "Suits", "value": 45000},
                    {"name": "Hoodies", "value": 38000},
                    {"name": "Sweaters", "value": 32000},
                    {"name": "Jeans", "value": 42000},
                ]},
                {"name": "Women's Clothing", "children": [
                    {"name": "Dresses", "value": 60000},
                    {"name": "Skirts", "value": 35000},
                    {"name": "Blouses", "value": 48000},
                    {"name": "Coats", "value": 42000},
                    {"name": "Leggings", "value": 30000},
                    {"name": "Scarves", "value": 25000},
                    {"name": "Handbags", "value": 35000},
                ]},
                {"name": "Children's Clothing", "children": [
                    {"name": "T-shirts", "value": 30000},
                    {"name": "Jeans", "value": 25000},
                    {"name": "Shorts", "value": 20000},
                    {"name": "Dresses", "value": 28000},
                    {"name": "Sweatpants", "value": 18000},
                    {"name": "Hats", "value": 15000},
                    {"name": "Shoes", "value": 22000},
                ]}
            ]
        }
    ]
    
    return render_template('inventory_management_dashboard.html', inventory_data=inventory_data)


@app.route('/')
def main_dashboard():
    return render_template('main_dashboard.html')

@app.route('/product_display_dashboard')
def product_display_dashboard():
    return render_template('product_display_dashboard.html')



# ------------------------------ Dynamic Pricing -------------------------------------

import json
from flask import Flask, render_template, request, jsonify
from PricingCalculator import PricingCalculator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, SelectField

# Define the form class
class InputForm(FlaskForm):
    month_index = SelectField('Month', choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], validators=[DataRequired()])
    market_trend = SelectField('Market Trend', choices=[('neutral', 'Neutral'), ('positive', 'Positive'), ('negative', 'Negative')], validators=[DataRequired()])
    competitor_pricing = SelectField('Competitor Pricing', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[DataRequired()])
    supply_demand = SelectField('Supply Demand', choices=[('high_supply_low_demand', 'High Supply Low Demand'), ('balanced_supply_demand', 'Balanced Supply Demand'), ('low_supply_high_demand', 'Low Supply High Demand')], validators=[DataRequired()])
    submit = SubmitField('Submit')

app.config['SECRET_KEY'] = '#inwei233' 


@app.route('/landing_page', methods=['GET', 'POST'])
def landing_page():
    return render_template('landing_page.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('index2.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    form = InputForm()
    if form.validate_on_submit():
        # Extracting data from the form
        month = form.month_index.data
        marketTrend = form.market_trend.data
        competitorPricing = form.competitor_pricing.data
        supplyDemand = form.supply_demand.data

        # Your existing logic
        base_price, curr_month = 1000, int(month)
        model = 'model_price_fluctuation.pkl'
        pricing_calculator = PricingCalculator(base_price, model)

        # Update the price fluctuation factor based on market conditions
        pricing_calculator.update_price_fluctuation_factor(marketTrend, competitorPricing, supplyDemand)

        # Reading the products.json file
        with open('products.json', 'r') as file:
            products = json.load(file)
        
        # Update prices in the JSON data
        for category in products:
            for product in products[category]:
                original_price = float(product['price'])
                pricing_calculator.base_price = original_price
                final_price = round(pricing_calculator.calculate_final_price(curr_month), 3)
                product['price'] = str(final_price)

        # # Returning JSON response
        # return jsonify({'result': products})
    else:
        with open('products.json', 'r') as file:
            products = json.load(file)

        # Initializations
        pricing_calculator = PricingCalculator(1000, 'model_price_fluctuation.pkl')
        base_price, curr_month = 1000, int(4)
        model = 'model_price_fluctuation.pkl'

        # Update the price fluctuation factor based on market conditions
        pricing_calculator.update_price_fluctuation_factor('neutral', 'high', 'high_supply_low_demand')
        
        for category in products:
            for product in products[category]:
                original_price = float(product['price'])
                pricing_calculator.base_price = original_price
                final_price = round(pricing_calculator.calculate_final_price(curr_month), 3)
                product['price'] = str(final_price)

        return render_template('products.html', products=products, form=form)


    # Render the form page
    return render_template('products.html', form=form, products=products,)

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    input_value = data.get('inputValue', '')
    
    # Perform computation or processing on the input_value
    processed_result = input_value.upper()  # Example: Convert input to uppercase
    
    return jsonify(result=processed_result)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
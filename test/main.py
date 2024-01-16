from flask import Flask, render_template, jsonify
import csv
import ast

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file and extract data
    products = []
    with open('data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            product = {
                'image': row['image'],
                'name': row['product'],
                'labels': ast.literal_eval(row['labels']),
                'data': ast.literal_eval(row['data']),
                'forecast': ast.literal_eval(row['forecast'])
            }
            products.append(product)
    
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)

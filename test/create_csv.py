import csv
import random


image_link = ["https://rukminim2.flixcart.com/image/850/1000/xif0q/shirt/c/q/j/xxl-st2-vebnor-original-imagpv8n3qmhqctd.jpeg?q=90",
              "https://rukminim2.flixcart.com/image/850/1000/xif0q/shirt/8/d/0/40-pcsfsslph87984-peter-england-original-imags3ypgawut5qu.jpeg?q=90",
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkrU3iQtWnHMNSQE22u4BD8NT-8IS9sxphcAq0XfKJYHthm3F5RUOPwsrKb0Nj7sYnkn0&usqp=CAU",
              "https://rukminim1.flixcart.com/image/850/1000/xif0q/shirt/i/v/z/40-pcshlslfc35380-peter-england-original-imagsjhxhrwfdfmd.jpeg?q=90",
              "https://rukminim2.flixcart.com/image/850/1000/xif0q/shirt/h/j/1/39-pcshsslpq75235-peter-england-original-imagkphahgztpgzm.jpeg?q=90",
              "https://m.media-amazon.com/images/W/MEDIAX_792452-T2/images/I/717kxMoZiAL._AC_UY1100_.jpg",
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRceq4qyjk9HOMeEnDJ2L0ubbIxqmZxJrkpJ0HcEw6482RXIte7CNXsjPEa7kRX-6foFk&usqp=CAU",
              "https://img0.junaroad.com/uiproducts/18390000/zoom_0-1653983278.jpg",
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5h0tli8Bz0djI4HtC7dMsAtZ8laKg3Urnr8Bj7VfrsQhfClId1iAc2sGGOnZkxZCQUuY&usqp=CAU",
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHO3OvKE3nGRAB1CkYTBk8nAHOdFpQIZPrgomZaUay0LPwNk2tUuHpAhdIC8kxcNM58Pc&usqp=CAU",
              "https://rukminim2.flixcart.com/image/850/1000/xif0q/shirt/c/q/j/xxl-st2-vebnor-original-imagpv8n3qmhqctd.jpeg?q=90"]
# Function to generate random data for labels, data, and forecast
def generate_random_data():
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    data = [random.randint(1, 20) for _ in labels]  # Generating random integers between 1 and 20 for data
    forecast = random.randint(20, 30)  # Generating a random forecast value between 20 and 30
    return labels, data, forecast

# Specify the filename for the CSV file
filename = 'data.csv'

# Writing data to CSV file
with open(filename, 'w', newline='') as file:
    # Create a CSV writer object
    fieldnames = ['image', 'product', 'labels', 'data', 'forecast']  # Add 'forecast' to fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write the header to the CSV file
    writer.writeheader()
    
    # Write 10 rows of data to the CSV file
    for i in range(1, 11):
        labels, data, forecast = generate_random_data()  # Generate random data and forecast for each row
        writer.writerow({
            'image': str(image_link[i]),  # Placeholder link for simplicity
            'product': f'Product{i}',
            'labels': str(labels),  # Convert list to string representation
            'data': str(data),  # Convert list to string representation
            'forecast': forecast  # Add forecast value
        })
        
print(f"CSV file '{filename}' has been created successfully!")
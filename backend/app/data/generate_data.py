"""
Generate realistic dummy retail dataset (~50,000 rows) and save to CSV.
Fields:
- order_id, order_date, customer_id, customer_name, region, state, city,
  category, sub_category, product, sales, quantity, profit, discount,
  inventory, stock

Run: python generate_data.py
"""
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import random

NUM_ROWS = 50000
START_DATE = datetime(2020,1,1)

regions = ['North', 'South', 'East', 'West']
states = {
    'North': ['NY', 'PA', 'MA'],
    'South': ['TX', 'FL', 'GA'],
    'East': ['NJ', 'CT', 'MD'],
    'West': ['CA', 'WA', 'OR']
}

cities = {
    'NY': ['New York', 'Albany'], 'PA': ['Philadelphia','Pittsburgh'], 'MA': ['Boston','Springfield'],
    'TX': ['Houston','Dallas'], 'FL': ['Miami','Orlando'], 'GA': ['Atlanta','Augusta'],
    'NJ': ['Newark','Jersey City'], 'CT': ['Hartford','New Haven'], 'MD': ['Baltimore','Annapolis'],
    'CA': ['Los Angeles','San Francisco'], 'WA': ['Seattle','Spokane'], 'OR': ['Portland','Eugene']
}

categories = {
    'Apparel': ['Shirts','Pants','Shoes'],
    'Electronics': ['Phones','Computers','Accessories'],
    'Home': ['Kitchen','Decor','Furniture'],
    'Beauty': ['Skincare','Makeup','Fragrance']
}

products = {
    'Shirts': ['Classic Tee','Polo Shirt','Formal Shirt'],
    'Pants': ['Jeans','Chinos','Shorts'],
    'Shoes': ['Sneakers','Loafers','Boots'],
    'Phones': ['Smart X','Smart Y','Feature Z'],
    'Computers': ['Laptop A','Desktop B','Notebook C'],
    'Accessories': ['Charger','Headphones','Case'],
    'Kitchen': ['Knife Set','Pan','Blender'],
    'Decor': ['Vase','Frame','Rug'],
    'Furniture': ['Chair','Table','Sofa'],
    'Skincare': ['Moisturizer','Cleanser','Sunscreen'],
    'Makeup': ['Lipstick','Foundation','Mascara'],
    'Fragrance': ['Cologne','Perfume','Body Mist']
}

first_names = ['Alex','Taylor','Jordan','Morgan','Casey','Jamie','Riley','Sam','Dana','Cameron']
last_names = ['Smith','Johnson','Brown','Lee','Wilson','Garcia','Martinez','Davis','Lopez','Clark']

rows = []
for i in range(1, NUM_ROWS+1):
    order_id = f'ORD{i:06d}'
    order_date = START_DATE + timedelta(days=random.randint(0, 365*3))
    customer_id = f'CUST{random.randint(1,8000):05d}'
    customer_name = random.choice(first_names) + ' ' + random.choice(last_names)
    region = random.choices(regions, weights=[0.25,0.25,0.25,0.25])[0]
    state = random.choice(states[region])
    city = random.choice(cities[state])
    category = random.choice(list(categories.keys()))
    sub_category = random.choice(categories[category])
    product = random.choice(products[sub_category])
    quantity = np.random.poisson(2) + 1

    base_price = {
        'Apparel': 30, 'Electronics': 250, 'Home': 80, 'Beauty': 20
    }[category]
    price_variation = np.random.normal(loc=1.0, scale=0.5)
    sales = round(max(1.0, base_price * price_variation) * quantity, 2)
    discount = round(np.random.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2], p=[0.45,0.2,0.15,0.08,0.06,0.03,0.03]) ,2)
    profit_margin = np.random.uniform(0.05, 0.35)
    profit = round(sales * profit_margin * (1 - discount), 2)
    inventory = random.randint(0, 200)
    stock = max(0, inventory - random.randint(0, 50))

    rows.append({
        'order_id': order_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'customer_id': customer_id,
        'customer_name': customer_name,
        'region': region,
        'state': state,
        'city': city,
        'category': category,
        'sub_category': sub_category,
        'product': product,
        'sales': sales,
        'quantity': quantity,
        'profit': profit,
        'discount': discount,
        'inventory': inventory,
        'stock': stock
    })

df = pd.DataFrame(rows)
out_path = '..\\..\\..\\database\\sales_data.csv'
print(f'Saving {len(df)} rows to {out_path}')
# Ensure directory exists when running from this file's folder
df.to_csv(out_path, index=False)
print('Done')

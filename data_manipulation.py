from unicodedata import decimal
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('data/final_data.csv')
print(df)

# Calculate total sales (value * quantity) for each transaction
df['total_sales'] = round(df['price'] * df['quantity'],2)

#Calculate total sales amount per customer
total_sales_per_customer = df.groupby('customer_id')['total_sales'].sum()
print(total_sales_per_customer)
total_sales_per_customer.to_csv('data/total_sales_per_customer.csv')

#Calculate average order quantity per product
average_order_quantity_per_product = df.groupby('product_id')['quantity'].mean()
print(average_order_quantity_per_product)
average_order_quantity_per_product.to_csv('data/average_order_quantity_per_product.csv')

# Assuming sales_data is a DataFrame with columns 'product_id' and 'quantity'
top_selling_products = df.groupby('product_id')['quantity'].sum().sort_values(ascending=False).head(5)
print(top_selling_products)
top_selling_products.to_csv('data/top_selling_products.csv')

# Assuming sales_data is a DataFrame with columns 'customer_id' and 'quantity'
top_customers = df.groupby('customer_id')['quantity'].sum().sort_values(ascending=False).head(5)
print(top_customers)

# Convert 'order_date' to datetime
df['order_date'] = pd.to_datetime(df['order_date'])
df.to_csv('data/df_tot_sales.csv')

# Group sales data by month and calculate total sales for each month
monthly_sales = df.groupby(pd.Grouper(key='order_date', freq='M'))['quantity'].sum()   
print('monthly_sales',monthly_sales)

# Group sales data by quarter and calculate total sales for each quarter
quarterly_sales = df.groupby(pd.Grouper(key='order_date', freq='Q'))['quantity'].sum()

# Plot monthly sales
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='line', marker='o', linestyle='-')
plt.title('Monthly Sales Trends')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid(True)
# Save plot to file
plt.savefig('report/monthly_sales_trends.png')

# Plot quarterly sales
plt.figure(figsize=(10, 6))
quarterly_sales.plot(kind='bar', color='skyblue')
plt.title('Quarterly Sales Trends')
plt.xlabel('Quarter')
plt.ylabel('Total Sales')
# Customize x-axis ticks to display the start date of each quarter
plt.xticks(range(len(quarterly_sales.index)), quarterly_sales.index.strftime('%Y-%m-%d'), rotation=45)
plt.tight_layout()
# Save plot to file
plt.savefig('report/quarterly_sales_trends.png')


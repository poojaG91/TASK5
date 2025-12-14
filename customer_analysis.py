# ==============================
# CUSTOMER SALES ANALYSIS PROJECT
# ==============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# 1. DATA LOADING & EXPLORATION
# ------------------------------
customers = pd.read_csv("customer_churn.csv")
sales = pd.read_csv("sales_data (1).csv")

print("Customer Data Info:")
print(customers.info())
print("\nSales Data Info:")
print(sales.info())

print("\nMissing Values:")
print(customers.isnull().sum())
print(sales.isnull().sum())

# ------------------------------
# 2. DATA CLEANING & PREPARATION
# ------------------------------
customers.fillna("Unknown", inplace=True)
sales.fillna(0, inplace=True)

sales["order_date"] = pd.to_datetime(sales["Date"])
sales["total_amount"] = sales["Quantity"] * sales["price"]

# ------------------------------
# 3. DATA MERGING
# ------------------------------
data = pd.merge(sales, customers, on="customer_id", how="inner")

# ------------------------------
# 4. CUSTOMER ANALYSIS
# ------------------------------
customer_ltv = (
    data.groupby("customer_name")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

top_customers = customer_ltv.head(10)

# ------------------------------
# 5. SALES PATTERN ANALYSIS
# ------------------------------
data["month"] = data["order_date"].dt.to_period("M")

monthly_sales = (
    data.groupby("month")["total_amount"]
    .sum()
    .reset_index()
)

top_products = (
    data.groupby("product")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

# ------------------------------
# 6. ADVANCED ANALYSIS
# ------------------------------
# Pivot Table
pivot_table = pd.pivot_table(
    data,
    values="total_amount",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)

# Retention Rate
orders_per_customer = data.groupby("customer_id")["order_id"].nunique()
retention_rate = (
    orders_per_customer[orders_per_customer > 1].count()
    / orders_per_customer.count()
) * 100

# ------------------------------
# 7. VISUALIZATIONS (DASHBOARD)
# ------------------------------

# Monthly Sales Trend
plt.figure()
plt.plot(monthly_sales["month"].astype(str), monthly_sales["total_amount"])
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

# Top Customers
plt.figure()
plt.bar(top_customers["customer_name"], top_customers["total_amount"])
plt.xticks(rotation=90)
plt.title("Top 10 Customers by Revenue")
plt.xlabel("Customer")
plt.ylabel("Revenue")
plt.show()

# Best Selling Products
plt.figure()
top_products.head(10).plot(kind="bar")
plt.title("Top 10 Best-Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.show()

# Sales by Region
region_sales = data.groupby("region")["total_amount"].sum()
plt.figure()
region_sales.plot(kind="pie", autopct="%1.1f%%")
plt.title("Sales Distribution by Region")
plt.ylabel("")
plt.show()

# ------------------------------
# 8. FINAL REPORT OUTPUT
# ------------------------------
total_revenue = data["total_amount"].sum()
total_customers = data["customer_id"].nunique()
avg_order_value = data["total_amount"].mean()
top_customer = top_customers.iloc[0]

print("\nCUSTOMER SALES ANALYSIS REPORT")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Customers: {total_customers}")
print(f"Average Order Value: ${avg_order_value:,.2f}")
print(f"Top Customer: {top_customer['customer_name']} - ${top_customer['total_amount']:,.2f}")
print(f"Customer Retention Rate: {retention_rate:.2f}%")

print("\nPivot Table (Sales by Region and Product):")
print(pivot_table)

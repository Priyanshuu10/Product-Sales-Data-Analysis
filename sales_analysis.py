# -*- coding: utf-8 -*-
"""sales analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NIIhQik1Gup9dPe8AbHMkZu1NfEHvvPE
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Store user credentials dynamically
USER_CREDENTIALS = {}

# Set up new user credentials
def setup_new_user():
    print("No users found. Please create your first login credentials.")
    username = input("Create Username: ")
    password = input("Create Password: ")
    USER_CREDENTIALS[username] = password
    print(f"\nAccount created successfully! Welcome, {username}.\n")
    return True

# Add multiple users
def add_user():
    print("\nAdd a New User")
    username = input("Enter Username: ")
    if username in USER_CREDENTIALS:
        print("This username already exists.")
        return
    password = input("Enter Password: ")
    USER_CREDENTIALS[username] = password
    print(f"\nUser {username} added successfully.\n")

# Authenticate user with username and password
def authenticate_user():
    if not USER_CREDENTIALS:
        return setup_new_user()  # Creates a new user and returns True
    else:
        while True:
            print("Please log in to access the sales analysis system.")
            username = input("Username: ")
            password = input("Password: ")

            if USER_CREDENTIALS.get(username) == password:
                print(f"\nWelcome, {username}!")
                return True  # Successful login
            else:
                print("\nInvalid username or password. Please try again.")

# Load product data from CSV
def load_product_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("Error: The specified file was not found.")
        return None

# Display Product Data
def display_product_data(df):
    print("\nProduct Sales Report (Days 1 to 30):")
    print(df.to_string(index=False))

# Calculate Total Sales
def calculate_total_sales(df):
    daily_sales = df.loc[:, 'Day1':'Day30']
    prices = df['Price'].values
    total_sales = (daily_sales.values * prices[:, None]).sum()
    return total_sales

# Calculate Daily Totals, Averages, and Profit/Loss
def calculate_daily_stats(df):
    prices = df['Price'].values
    daily_sales = df.loc[:, 'Day1':'Day30']
    daily_totals = (daily_sales.values * prices[:, None]).sum(axis=0)
    daily_averages = daily_totals.mean()
    profit_loss = np.diff(daily_totals)
    return daily_totals, daily_averages, profit_loss

# Visualize Daily Sales Trend
def plot_daily_sales(daily_totals):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 31), daily_totals, marker='o', color='b', label='Daily Total Sales')
    plt.xlabel('Day')
    plt.ylabel('Total Sales (₹)')
    plt.title('Daily Sales Trend Over 30 Days')
    plt.legend()
    plt.show()

# Bar Graph of Daily Sales using Seaborn
def plot_bar_daily_sales(daily_totals):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=np.arange(1, 31), y=daily_totals, palette="viridis")
    plt.xlabel('Day')
    plt.ylabel('Total Sales (₹)')
    plt.title('Daily Sales Bar Graph Over 30 Days')
    plt.show()

# Option to Find Most and Least Selling Days
def find_extreme_days(daily_totals):
    most_selling_day = np.argmax(daily_totals) + 1
    least_selling_day = np.argmin(daily_totals) + 1
    return most_selling_day, least_selling_day

# Find Most Sold Items by Category
def find_most_sold_items(df):
    categories = df['Category'].unique()
    most_sold_items = {}
    for category in categories:
        cat_df = df[df['Category'] == category]
        sales_amount = (cat_df.loc[:, 'Day1':'Day30'].values * cat_df['Price'].values[:, None]).sum(axis=1)
        most_sold_item = cat_df.iloc[np.argmax(sales_amount)]['Item']
        most_sold_items[category] = most_sold_item
    return most_sold_items

# Inventory Analysis
def calculate_inventory(df, initial_stock):
    total_sold = df.loc[:, 'Day1':'Day30'].sum(axis=1)
    remaining_stock = initial_stock - total_sold
    df['Remaining Stock'] = remaining_stock
    return df[['Item', 'Remaining Stock']]

# Sales Forecasting (Simple Moving Average)
def sales_forecasting(daily_totals, window_size=3):
    rolling_avg = np.convolve(daily_totals, np.ones(window_size)/window_size, mode='valid')
    forecast = rolling_avg[-1]
    print(f"\nSales Forecast (next day, based on {window_size}-day moving average): ₹{forecast:.2f}")
    return forecast

# Profitability Analysis
def profitability_analysis(df, cost_price_percentage=0.6):
    prices = df['Price'].values
    cost_price = prices * cost_price_percentage
    daily_sales = df.loc[:, 'Day1':'Day30']
    total_sales_value = (daily_sales.values * prices[:, None]).sum().sum()
    total_cost = (daily_sales.values * cost_price[:, None]).sum().sum()
    profit = total_sales_value - total_cost
    profit_margin = (profit / total_sales_value) * 100
    print(f"\nTotal Profit: ₹{profit:.2f}")
    print(f"Profit Margin: {profit_margin:.2f}%")
    return profit, profit_margin

# Category Sales Analysis
def category_sales_analysis(df):
    category_totals = df.groupby('Category').apply(lambda x: (x.loc[:, 'Day1':'Day30'].values * x['Price'].values[:, None]).sum().sum())
    print("\nCategory Sales Analysis:")
    for category, total in category_totals.items():
        print(f"{category}: ₹{total}")
    return category_totals

def main():
    while True:
        if not authenticate_user():
            continue  # If authentication fails, prompt again

        # Load data from CSV
        df = load_product_data('product_sales.csv')
        if df is None:
            return  # Exit if data could not be loaded

        initial_stock = 500  # Assuming each product starts with 500 units

        # User Options
        while True:
            print("\nOptions:")
            print("1. Display Product Data")
            print("2. Calculate Total Sales")
            print("3. Show Daily Sales Trend")
            print("4. Find Most and Least Selling Days")
            print("5. Find Most Sold Items by Category")
            print("6. Calculate Inventory Levels")
            print("7. Sales Forecasting")
            print("8. Profitability Analysis")
            print("9. Category Sales Analysis")
            print("10. Show Daily Sales Bar Graph")
            print("11. Add New User")
            print("12. Log Out")
            print("0. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                display_product_data(df)
            elif choice == "2":
                total_sales = calculate_total_sales(df)
                print(f"\nTotal Sales: ₹{total_sales}")
            elif choice == "3":
                daily_totals, _, _ = calculate_daily_stats(df)
                plot_daily_sales(daily_totals)
            elif choice == "4":
                daily_totals, _, _ = calculate_daily_stats(df)
                most_selling_day, least_selling_day = find_extreme_days(daily_totals)
                print(f"\nMost Selling Day: Day {most_selling_day}")
                print(f"Least Selling Day: Day {least_selling_day}")
            elif choice == "5":
                most_sold_items = find_most_sold_items(df)
                print("\nMost Sold Items by Category:")
                for category, item in most_sold_items.items():
                    print(f"{category}: {item}")
            elif choice == "6":
                inventory_df = calculate_inventory(df, initial_stock)
                print("\nInventory Levels:")
                print(inventory_df)
            elif choice == "7":
                daily_totals, _, _ = calculate_daily_stats(df)
                sales_forecasting(daily_totals)
            elif choice == "8":
                profitability_analysis(df)
            elif choice == "9":
                category_sales_analysis(df)
            elif choice == "10":
                daily_totals, _, _ = calculate_daily_stats(df)
                plot_bar_daily_sales(daily_totals)
            elif choice == "11":
                add_user()  # Add a new user
            elif choice == "12":
                break  # Log out and prompt to re-authenticate
            elif choice == "0":
                print("Exiting system...")
                return  # Exit the entire system
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
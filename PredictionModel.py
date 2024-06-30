import pandas as pd
import joblib

# Load the dataset
data = pd.read_csv('/mnt/data/zomato0.csv')

# Preprocess the data
data['rate'] = data['rate'].str.replace('/5', '').astype(float)
data['approx_cost(for two people)'] = data['approx_cost(for two people)'].str.replace(',', '').astype(float)
data = data.dropna()

# Function to get the best location based on user inputs
def get_best_location(cuisine_type, rating, cost, book_table, online_order):
    # Convert boolean inputs to Yes/No
    book_table = 'Yes' if book_table else 'No'
    online_order = 'Yes' if online_order else 'No'
    
    # Filter the data based on the inputs
    filtered_data = data[
        (data['rest_type'].str.contains(cuisine_type, case=False, na=False)) &
        (data['rate'] >= rating) &
        (data['approx_cost(for two people)'] <= cost) &
        (data['book_table'] == book_table) &
        (data['online_order'] == online_order)
    ]
    
    if filtered_data.empty:
        return "No matching locations found."
    
    # Get the best location based on the highest rating
    best_location = filtered_data.loc[filtered_data['rate'].idxmax()]['location']
    return best_location

# Function to get the best cuisine type based on user inputs
def get_best_cuisine(location, rating, cost, book_table, online_order):
    # Convert boolean inputs to Yes/No
    book_table = 'Yes' if book_table else 'No'
    online_order = 'Yes' if online_order else 'No'
    
    # Filter the data based on the inputs
    filtered_data = data[
        (data['location'].str.contains(location, case=False, na=False)) &
        (data['rate'] >= rating) &
        (data['approx_cost(for two people)'] <= cost) &
        (data['book_table'] == book_table) &
        (data['online_order'] == online_order)
    ]
    
    if filtered_data.empty:
        return "No matching cuisines found."
    
    # Get the best cuisine type based on the highest rating
    best_cuisine = filtered_data.loc[filtered_data['rate'].idxmax()]['rest_type']
    return best_cuisine

# Example usage
if __name__ == "__main__":
    import sys
    
    # Get user inputs
    cuisine_type = input("Enter cuisine type: ")
    rating = float(input("Enter minimum rating: "))
    cost = int(input("Enter maximum cost for two people: "))
    book_table = input("Is table booking available (Yes/No)? ").strip().lower() == 'yes'
    online_order = input("Is online ordering available (Yes/No)? ").strip().lower() == 'yes'
    
    # Get the best location
    best_location = get_best_location(cuisine_type, rating, cost, book_table, online_order)
    print(f"Best location for the given criteria: {best_location}")
    
    # Get the best cuisine type
    location = input("Enter location: ")
    best_cuisine = get_best_cuisine(location, rating, cost, book_table, online_order)
    print(f"Best cuisine type for the given criteria: {best_cuisine}")

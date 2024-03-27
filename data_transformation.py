import requests
import pandas as pd
import concurrent.futures
import pandas as pd
from datetime import datetime


def fetch_user_data(url):
    """
    Fetches user data from the provided URL using the JSONPlaceholder API.

    Parameters:
    url (str): The URL to fetch user data from.

    Returns:
    pd.DataFrame: A DataFrame containing user data.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return pd.DataFrame()


def transform_and_merge_sales_data(sales_data, user_data):
    """
    Transforms and merges sales data with user data based on 'customer_id'.

    Parameters:
    sales_data (pd.DataFrame): DataFrame containing sales data.
    user_data (pd.DataFrame): DataFrame containing user data.

    Returns:
    pd.DataFrame: A DataFrame containing merged data.
    """
    # Merge DataFrames on 'customer_id'
    merged_df = pd.merge(user_data,sales_data, left_on='id', right_on='customer_id', how='inner')
    merged_df.to_csv('data/merged.csv',index=False)
    return merged_df

def fetch_weather_data(api_key, location):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': location,
        'appid': api_key,
    }
    response = requests.get(url, params=params)
    #print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for {location}. Status code: {response.status_code}")
        return None

def fetch_weather_data_for_row(row):
    api_key = '4543b87fa211b08efd7dc7e4b3006d36' 
    location = 'London'
    weather_data = fetch_weather_data(api_key, location)
    return weather_data

if __name__ == "__main__":
    start_time = datetime.now()
    # Fetch user data from the JSONPlaceholder API
    user_data_url = 'https://jsonplaceholder.typicode.com/users'
    user_data = fetch_user_data(user_data_url)
    print('-----user_data-----\n', user_data)
    
    # Simulated sales data (replace this with your actual sales data)
    sales_data_path = r'C:\Users\03063Y744\Downloads\AIQ - Data Engineer Assignment - Sales data.csv'
    sales_data = pd.read_csv(sales_data_path)
    print('-----sales_data-----\n', sales_data)
    
    # Transform and merge sales data with user data
    final_data = transform_and_merge_sales_data(sales_data, user_data)
    print('-----final_data-----\n', final_data)

    final_data['temperature'] = None
    final_data['weather_conditions'] = None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_weather_data_for_row, row): row for _, row in final_data.iterrows()}
        for future in concurrent.futures.as_completed(futures):
            row = futures[future]
            try:
                weather_data = future.result()
                if weather_data:
                    temperature = weather_data['main']['temp']
                    weather_conditions = weather_data['weather'][0]['description']
                    final_data.at[row.name, 'temperature'] = temperature
                    final_data.at[row.name, 'weather_conditions'] = weather_conditions
            except Exception as e:
                print(f"Error fetching weather data: {e}")
    
    final_data.to_csv('data/final_data.csv',index=False)
    end_time = datetime.now()
    process_time = end_time - start_time
    print(process_time)
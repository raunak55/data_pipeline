import pytest
import requests
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock
import sys
sys.path.append("..")
from methods.data_transformation import (fetch_user_data, transform_and_merge_sales_data,
                         fetch_weather_data, fetch_weather_data_for_row,
                         data_transformation_method)


# Mock response object for successful requests
class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


@pytest.fixture
def mock_requests_get():
    def mock_get(*args, **kwargs):
        if args[0].startswith('https://jsonplaceholder.typicode.com/users'):
            return MockResponse(200, [{'id': 1, 'name': 'User1'}, {'id': 2, 'name': 'User2'}])
        elif args[0].startswith('https://api.openweathermap.org/data/2.5/weather'):
            return MockResponse(200, {'main': {'temp': 15}, 'weather': [{'description': 'Cloudy'}]})
        else:
            return MockResponse(404, None)
    return mock_get


def test_fetch_user_data(mock_requests_get):
    with patch('requests.get', side_effect=mock_requests_get):
        url = 'https://jsonplaceholder.typicode.com/users'
        user_data = fetch_user_data(url)
        assert isinstance(user_data, pd.DataFrame)
        assert len(user_data) == 2


def test_transform_and_merge_sales_data():
    # Prepare sample dataframes
    sales_data = pd.DataFrame({'customer_id': [1, 2, 3], 'sales_amount': [100, 200, 300]})
    user_data = pd.DataFrame({'id': [1, 2], 'name': ['User1', 'User2']})

    # Call the function
    merged_data = transform_and_merge_sales_data(sales_data, user_data)

    # Check if the merged data has expected columns and rows
    assert isinstance(merged_data, pd.DataFrame)
    assert 'name' in merged_data.columns
    assert 'sales_amount' in merged_data.columns
    assert len(merged_data) == 2


def test_fetch_weather_data(mock_requests_get):
    with patch('requests.get', side_effect=mock_requests_get):
        api_key = 'test_api_key'
        location = 'test_location'
        weather_data = fetch_weather_data(api_key, location)
        assert weather_data == {'main': {'temp': 15}, 'weather': [{'description': 'Cloudy'}]}


def test_fetch_weather_data_for_row():
    # Prepare a sample row
    row = pd.Series({'id': 1, 'name': 'User1'})

    # Call the function
    weather_data = fetch_weather_data_for_row(row)

    # Check if weather data is fetched successfully
    assert weather_data == {'main': {'temp': 15}, 'weather': [{'description': 'Cloudy'}]}


def test_data_transformation_method(monkeypatch, tmp_path):
    # Set up mock data
    user_data = [{'id': 1, 'name': 'User1'}, {'id': 2, 'name': 'User2'}]
    sales_data = pd.DataFrame({'customer_id': [1, 2, 3], 'sales_amount': [100, 200, 300]})
    expected_final_data_length = 2

    # Mock fetch_user_data
    def mock_fetch_user_data(url):
        return pd.DataFrame(user_data)

    # Mock fetch_weather_data_for_row
    def mock_fetch_weather_data_for_row(row):
        return {'main': {'temp': 15}, 'weather': [{'description': 'Cloudy'}]}

    monkeypatch.setattr('your_module.fetch_user_data', mock_fetch_user_data)
    monkeypatch.setattr('your_module.fetch_weather_data_for_row', mock_fetch_weather_data_for_row)

    # Run the function
    data_transformation_method()

    # Check if files are generated
    assert (tmp_path / 'data/merged.csv').exists()
    assert (tmp_path / 'data/final_data.csv').exists()

    # Check if final data length matches expected
    final_data = pd.read_csv(tmp_path / 'data/final_data.csv')
    assert len(final_data) == expected_final_data_length

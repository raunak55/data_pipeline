# app.py

from methods.data_manipulation import manipulate_data
from methods.data_transformation import data_transformation_method
from methods.data_storage import load_data_sqlite

def main():
    data_transformation_method()
    manipulate_data()
    load_data_sqlite()

if __name__ == "__main__":
    main()

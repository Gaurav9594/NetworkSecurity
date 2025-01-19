import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging

load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

# Check the authentication and only valid package has been processed
# Certifi helps in setting secure HTTP question
# ca : certify authentication
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            # Read the CSV file into a DataFrame
            data = pd.read_csv(file_path)

            # Reset the index of the DataFrame
            data.reset_index(drop=True, inplace=True)

            # Convert the DataFrame to a JSON string (transpose the DataFrame first)
            json_data = data.T.to_json()

            # Parse the JSON string into a Python dictionary
            records_dict = json.loads(json_data)

            # Extract the values (each row as a dictionary)
            records = list(records_dict.values())  # .values() works on the parsed dictionary
            print(records)
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
    def insert_data_mongodb(self, records, database, collection):
        try:
            # Corrected: Removed the trailing commas
            self.database = database
            self.collection = collection
            self.records = records

            # MongoDB client initialization
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # Access the database and collection from self.mongo_client
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            # Insert data into the collection
            self.collection.insert_many(self.records)
            print(len(self.records))
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "KRISHAI"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)
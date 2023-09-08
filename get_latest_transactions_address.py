import requests
import json
from datetime import datetime
import pickle
import get_txn_model_input as gtmi
import pandas as pd

# Load transformer and model from the Pickle files
with open('transformer_add.pkl', 'rb') as f:
    transformer_add = pickle.load(f)

with open('model_add.pkl', 'rb') as f:
    model_add = pickle.load(f)

# Load transformer and model from the Pickle files
with open('transformer_txn.pkl', 'rb') as g:
    transformer_txn = pickle.load(g)

with open('model_txn.pkl', 'rb') as g:
    model_txn = pickle.load(g)

BASE_URL = "https://api.etherscan.io/api"
API_KEY = "6JXP5MQEZHAU2GE9AUTZGB9Y6STXE632YF"  # Replace with your Etherscan API key

def get_all_transactions_address(Address):
    params = {
        "module": "account",
        "action": "txlist",
        "address": Address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    required_keys = ['timestamp', 'hash', 'value', 'gasPrice']
    if data.get("message") == "OK":
        transactions = data["result"]
        
        # Initialize an empty list to store the transformed data
        transformed_data = []
        
        for d in transactions[-10:]:
            # Create a dictionary with your data
            input_data = gtmi.get_transaction_model_input(d['hash'])
            
            # Convert the dictionary into a DataFrame
            input_df = pd.DataFrame([input_data])
            
            # Apply the transformer to the DataFrame
            transformed_df = transformer_txn.transform(input_df)
            # Add the transformed data along with other information to the list
            transformed_data.append({
                'timestamp': datetime.utcfromtimestamp(int(d['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                'hash': d['hash'],
                'value': int(d['value']) / 10**18,
                'gasPrice': int(d['gasPrice']) / 10**18,
                'Prediction': model_txn.predict(transformed_df)[0]
            })
            print(transformed_data)
        
        return transformed_data
    else:
        print(f"Error fetching transactions for address {Address}")
        return []

# Check if the script is being run directly
if __name__ == '__main__':
    get_latest_transactions_address(Address)

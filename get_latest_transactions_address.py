import requests
import json
from datetime import datetime


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
    required_keys = ['timestamp', 'hash', 'value','gasPrice']
    if data.get("message") == "OK":
        transactions = data["result"]
        result = [{
            'timestamp': datetime.utcfromtimestamp(int(d['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S'),
            'hash': d['hash'],
            'value': int(d['value']) / 10**18,
            'gasPrice': int(d['gasPrice']) / 10**18,
        } for d in transactions[-50:]]

        
        return result
    else:
        print(f"Error fetching transactions for address {Address}")
        return []
        
# Check if the script is being run directly
if __name__ == '__main__':
    get_latest_transactions_address(Address)
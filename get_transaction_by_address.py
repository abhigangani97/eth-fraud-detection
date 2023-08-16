import requests
import json

BASE_URL = "https://api.etherscan.io/api"
API_KEY = "6JXP5MQEZHAU2GE9AUTZGB9Y6STXE632YF"  # Replace with your Etherscan API key

def get_transactions(Address):
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
    
    if data.get("message") == "OK":
        transactions = data["result"]
        return transactions
    else:
        print(f"Error fetching transactions for address {Address}")
        return []
        
# Check if the script is being run directly
if __name__ == '__main__':
    get_transaction(Address)
import requests
import json

BASE_URL = "https://api.etherscan.io/api"
API_KEY = "6JXP5MQEZHAU2GE9AUTZGB9Y6STXE632YF"

def get_transaction_by_hash(transaction_hash):
    params = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": transaction_hash,
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "message" in data and data["message"] == "OK":
        transaction = data["result"]
        return transaction
    elif "result" in data and data["result"]:  # In some cases, there might be no "message" but there is still valid "result"
        return data["result"]
    else:
        print(f"Error fetching transaction details for hash {transaction_hash}")
        return None
        
# Check if the script is being run directly
if __name__ == '__main__':
    get_transaction_by_hash(transaction_hash)
import requests
import json

BASE_URL = "https://api.etherscan.io/api"
API_KEY = "6JXP5MQEZHAU2GE9AUTZGB9Y6STXE632YF"  # Replace with your Etherscan API key

def get_hashes():
    params = {
        "module": "proxy",
        "action": "eth_getBlockByNumber",
        "tag": "latest",
        "boolean": "true",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    transactions = data.get('result', {}).get('transactions', [])
    return [tx['hash'] for tx in transactions[:10]]

# Check if the script is being run directly
if __name__ == '__main__':
    get_hashes()
import requests
import sys
import json

BASE_URL = "https://api.etherscan.io/api"
API_KEY = "6JXP5MQEZHAU2GE9AUTZGB9Y6STXE632YF"  # Replace with your Etherscan API key

def get_eth_balance(address):
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data['status'] == '1':
        wei_balance = int(data['result'])
        eth_balance = wei_balance / 1e18
        return eth_balance
    else:
        print("Error:", data['message'])
        return None

# Check if the script is being run directly
if __name__ == '__main__':
    if len(sys.argv) > 1:
        address = sys.argv[1]
        balance = get_eth_balance(address)
        print(balance)
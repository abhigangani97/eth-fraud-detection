import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

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
            'timestamp': datetime.utcfromtimestamp(int(d['timeStamp'])).strftime('%Y-%m-%d'),
            'hash': d['hash'],
            'value': int(d['value']) / 10**18,
            'gasPrice': int(d['gasPrice']) / 10**18,
        } for d in transactions[:]]

        return result
    else:
        print(f"Error fetching transactions for address {Address}")
        return []

def generate_transaction_count_plot(address_data):
    timestamps = [entry['timestamp'] for entry in address_data]
    unique_dates = sorted(set(timestamps))
    transaction_counts = [timestamps.count(date) for date in unique_dates]

    # Set the custom colors using a colormap
    background_color = 'black'
    text_color = 'white'
    cmap = plt.get_cmap('viridis')  # You can choose any colormap
    bar_colors = cmap(np.linspace(0, 1, len(unique_dates)))

    plt.figure(figsize=(15, 6), facecolor=background_color)
    ax = plt.gca()
    ax.set_facecolor(background_color)
    bars = plt.bar(unique_dates, transaction_counts, color=bar_colors)
    plt.xlabel('Date', color=text_color)
    plt.ylabel('Transaction Count', color=text_color)
    plt.title('Transaction Count Over Time', color=text_color)

    # Format x-axis labels for better readability
    if len(unique_dates) > 15:
        step = 5
    else:
        step = 1
    plt.xticks(range(0, len(unique_dates), step), unique_dates[::step], rotation=45, ha='right', color=text_color)
    plt.yticks(color=text_color)

    # Add a colorbar to show the mapping of colors
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=len(unique_dates)-1))
    sm.set_array([])  # Fake a scalar to create the colorbar
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Date Color')

    # Save the plot as bytes in memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=background_color)
    buffer.seek(0)

    # Encode the plot as base64
    plot_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return f"data:image/png;base64,{plot_base64}"

if __name__ == '__main__':
    # Example usage:
    transactions_data = get_all_transactions_address("example_address")
    transaction_count_plot = generate_transaction_count_plot(transactions_data)
    # You can return this plot in your route handler
    pass

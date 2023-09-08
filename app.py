import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request, jsonify
import get_latest_hash
import get_transaction_details as gtd
import get_address_details as gat
import get_add_model_input as gami
import get_txn_model_input as gtmi
import get_latest_transactions_address as glta
import get_plot as gp
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from io import BytesIO
import base64

app = Flask(__name__, static_url_path='/static')

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

def get_all_transactions_address(address):
    # Your get_all_transactions_address function code here
    pass

def get_datewise_transaction_count(transactions):
    # Your get_datewise_transaction_count function code here
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    address_details = None
    transaction_details = None
    transactions = None
    prediction_add = None
    prediction_txn = None
    attempted_address_check = False
    attempted_txn_check = False
    transaction_count_plot = None  # Initialize the variable for the transaction count plot

    if request.method == 'POST':
        if 'fetch_transactions' in request.form:
            transactions = get_latest_hash.get_hashes()
            return render_template('index.html', transactions=transactions)
        elif 'enter_hash' in request.form:
            attempted_txn_check = True
            transaction_hash = request.form['hash']
            transaction_details = gtd.get_transaction_details(transaction_hash)
            txn_input = gtmi.get_transaction_model_input(transaction_hash)
            txn_details_df = pd.DataFrame([txn_input])

            # Transform the data using the loaded transformer
            transformed_data_txn = transformer_txn.transform(txn_details_df)

            # Make a prediction using the loaded model
            prediction_txn = model_txn.predict(transformed_data_txn)[0]
            print("Prediction: ", prediction_txn)
            return render_template('index.html', transactions=transactions, transaction_details=transaction_details, prediction_txn=prediction_txn, attempted_txn_check=attempted_txn_check)

        elif 'enter_address' in request.form:
            attempted_address_check = True
            address = request.form['address']
            address_details = gat.get_address_details(address)
            address_input = gami.get_address_model_input(address)
            address_details_df = pd.DataFrame([address_input])

            # Transform the data using the loaded transformer
            transformed_data_add = transformer_add.transform(address_details_df)

            # Make a prediction using the loaded model
            prediction_add = model_add.predict(transformed_data_add)[0]
            print("Prediction: ", prediction_add)
            return render_template('index.html', transactions=transactions, address_details=address_details, prediction_add=prediction_add, attempted_address_check=attempted_address_check)

        elif 'enter_address_50' in request.form:
            address = request.form['address_50']
            past_50_transactions = glta.get_all_transactions_address(address)
            return render_template('index.html', past_50_transactions=past_50_transactions)

        elif 'generate_transaction_count' in request.form:  # Handle form submission for generating the transaction count graph
            address_for_graph = request.form['transaction_count_address']
            trans = gp.get_all_transactions_address(address_for_graph)
            print(trans)
            # Generate the transaction count plot here and save it as base64 data
            # You can use your existing logic to generate the plot and convert it to base64
            transaction_count_plot = gp.generate_transaction_count_plot(trans)

            return render_template('index.html', transaction_count_plot=transaction_count_plot)

    else:
        return render_template('index.html', transactions=transactions, address_details=address_details, transaction_details=transaction_details, transaction_count_plot=transaction_count_plot)

if __name__ == '__main__':
    app.run(debug=True)

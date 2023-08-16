from flask import Flask, render_template, request
import get_latest_hash
import get_transaction_details as gtd
import get_address_details as gat
import get_add_model_input as gami
import get_txn_model_input as gtmi
import pickle
import pandas as pd

app = Flask(__name__)

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


@app.route('/', methods=['GET', 'POST'])
def index():
    address_details = None
    transaction_details = None
    transactions = None
    prediction_add = None
    prediction_txn = None
    attempted_address_check = False
    attempted_txn_check = False

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
            return render_template('index.html', transactions=transactions, transaction_details=transaction_details, prediction_txn=prediction_txn,attempted_txn_check=attempted_txn_check)

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
            return render_template('index.html', transactions=transactions, address_details=address_details, prediction_add=prediction_add,attempted_address_check=attempted_address_check)

        else:
            return render_template('index.html', transactions=transactions, address_details=address_details, transaction_details=transaction_details, error_message="Invalid Address.")

    return render_template('index.html', transactions=transactions, address_details=address_details, transaction_details=transaction_details)

if __name__ == '__main__':
    app.run(debug=True)

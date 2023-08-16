import sys
import get_transaction_by_hash
import get_transaction_by_address
import get_ERC20
import get_ether_balance


def average_time_between_sent_txns(transactions, Address):
    timestamps = sorted([int(txn['timeStamp']) for txn in transactions if txn['from'].lower() == Address.lower()])
    avg_diff = sum(timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)) / max(len(timestamps)-1, 1) / 60
    return avg_diff


def average_time_between_rec_txns(transactions, Address):
    timestamps = sorted([int(txn['timeStamp']) for txn in transactions if txn['to'].lower() == Address.lower()])
    avg_diff = sum(timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)) / max(len(timestamps)-1, 1) / 60
    return avg_diff

def avg_ERC20_received_values(transactions, address):
    received_erc20_txns = [txn for txn in transactions if txn["to"].lower() == address.lower()]
    received_values = [int(txn["value"]) for txn in received_erc20_txns]
    return (sum(received_values) / len(received_values))/1e18 if received_values else 0
    
def avg_received_values(transactions, address):
    received_txns = [txn for txn in transactions if txn["to"].lower() == address.lower()]
    received_values = [int(txn["value"]) for txn in received_txns]
    return (sum(received_values) / len(received_values))/1e18 if received_values else 0
    
def get_transaction_model_input(hash_id):
    transaction = get_transaction_by_hash.get_transaction_by_hash(hash_id)
    if not transaction:
        return

    address = transaction["from"]
    transactions = get_transaction_by_address.get_transactions(address)
    tokens = get_ERC20.get_ERC20(address)
        
    # Computing details:
    nonce = int(transaction["nonce"], 16)
    gas = int(transaction["gas"], 16)
    gasprice = int(transaction["gasPrice"], 16)/1e18
    ether_balance = get_ether_balance.get_eth_balance(address)
    unq_rec_from_add = len(set(txn["from"] for txn in transactions if txn["to"].lower() == address.lower()))
    total_erc_txn = len(tokens)
    total_transactions = len(transactions)
    avg_min_sen_txns = average_time_between_sent_txns(transactions,address)
    avg_min_rec_txns = average_time_between_rec_txns(transactions,address)
    avg_val_recieved = avg_received_values(transactions,address)  
    unq_rec_from_add = len(set(txn["from"] for txn in transactions if txn["to"].lower() == address.lower()))
    unq_tkn_rec_from_add = len(set(txn["from"] for txn in tokens if txn["to"].lower() == address.lower()))
    unq_rec_tkn = len(set(txn["tokenName"] for txn in tokens if txn["to"].lower() == address.lower()))
    rec_txn = len([txn for txn in transactions if txn['to'].lower() == address.lower()])
    avg_tkn_rec = avg_ERC20_received_values(transactions,address)
    total_tkn_rec  = sum([int(txn['value']) for txn in tokens if txn["to"].lower() == address.lower()])/1e18 
    sent_txn = len([txn for txn in transactions if txn['from'].lower() == address.lower()])
    try:
        tim_diff_first_last = ((max(int(txn["timeStamp"]) for txn in transactions) - min(int(txn["timeStamp"]) for txn in transactions)) / 60)
    except ValueError:
        tim_diff_first_last = 0
    unq_rec_from_add_tkn = len(set(txn["from"] for txn in tokens if txn["to"].lower() == address.lower()))
    try:
        total_eth_rec = sum([int(txn['value']) for txn in transactions if txn['to'].lower() == address.lower()])/1e18
    except ValueError:
        total_eth_rec = 0
    try:
        total_eth_sent = sum([int(txn['value']) for txn in transactions if txn['from'].lower() == address.lower()])/1e18
    except ValueError:
        total_eth_sent = 0
    try:
        max_val_rec = max([int(txn['value']) for txn in transactions if txn["to"].lower() == address.lower()])/1e18
    except ValueError:
        max_val_rec = 0
    try:
        min_val_sent = min([int(txn['value']) for txn in transactions if txn["from"].lower() == address.lower()])/1e18
    except ValueError:
        min_val_sent = 0
    try:
        max_value_sent = max([int(txn['value']) for txn in transactions if txn["from"].lower() == address.lower()])/1e18
    except ValueError:
        max_value_sent = 0
    try:
        max_tkn_rec = max([int(txn['value']) for txn in tokens if txn["to"].lower() == address.lower()])/1e18
    except ValueError:
        max_tkn_rec = 0
    
    
    
    # Appending all details to DataFrame:
    transactional_details = {
        'Time Diff between first and last (Mins)' : tim_diff_first_last, 
        'Unique Received From Addresses' : unq_rec_from_add,
        'total transactions (including tnx to create contract' : total_transactions,
        'avg val received' : avg_val_recieved,
        ' ERC20 avg val rec' : avg_tkn_rec,
        'total ether balance' : ether_balance,
        'total ether received' : total_eth_rec,
        'Received Tnx' : rec_txn,
        'Sent tnx' : sent_txn,
        ' ERC20 uniq rec addr' : unq_rec_from_add_tkn,
        'Avg min between received tnx' : avg_min_rec_txns,
        ' Total ERC20 tnxs' : total_erc_txn,
        'Avg min between sent tnx' : avg_min_sen_txns,
        ' ERC20 total Ether received' : total_tkn_rec,
        'max value received ' : max_val_rec,
        ' ERC20 uniq rec contract addr' : unq_rec_tkn,
        'min val sent' : min_val_sent,
        'total Ether sent' : total_eth_sent,
        ' ERC20 max val rec' : max_tkn_rec,
        'max val sent' : max_value_sent,
        ' ERC20 uniq sent token name' :unq_tkn_rec_from_add ,
        'gas' : gas,
        'nonce' : nonce,
        'gasPrice' : gasprice
    }
    return transactional_details



# Check if the script is being run directly
if __name__ == '__main__':
    if len(sys.argv) > 1:
        hash_id = sys.argv[1]
        details = get_transaction_model_input(hash_id)
        print(details)
    else:
        print("No Address provided.")

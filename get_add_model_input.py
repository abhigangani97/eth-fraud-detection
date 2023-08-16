import sys
import get_transaction_by_hash
import get_transaction_by_address
import get_ERC20


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
    
def get_address_model_input(address):

    transactions = get_transaction_by_address.get_transactions(address)
    tokens = get_ERC20.get_ERC20(address)
        
    # Computing details:
    total_erc_txn = len(tokens)
    avg_min_sen_txns = average_time_between_rec_txns(transactions,address)
    avg_val_recieved = avg_received_values(transactions,address)  
    unq_rec_from_add = len(set(txn["from"] for txn in transactions if txn["to"].lower() == address.lower()))
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
        max_tkn_rec = max([int(txn['value']) for txn in tokens if txn["to"].lower() == address.lower()])/1e18
    except ValueError:
        max_tkn_rec = 0
    
    
    
    # Appending all details to DataFrame:
    transactional_details = {
        'Time Diff between first and last (Mins)' : tim_diff_first_last, 
        ' ERC20 uniq rec addr' : unq_rec_from_add_tkn,
        'total ether received' : total_eth_rec,
        ' Total ERC20 tnxs' : total_erc_txn,
        'Avg min between sent tnx' : avg_min_sen_txns,
        'avg val received' : avg_val_recieved,
        'Unique Received From Addresses' : unq_rec_from_add,
        ' ERC20 uniq rec contract addr' : unq_rec_tkn,
        'max value received ' : max_val_rec,
        'min val sent' : min_val_sent,
        'Received Tnx' : rec_txn,
        ' ERC20 avg val rec' : avg_tkn_rec,
        ' ERC20 max val rec' : max_tkn_rec,
        ' ERC20 total Ether received' : total_tkn_rec,
        'Sent tnx' : sent_txn
    }
    return transactional_details


# Check if the script is being run directly
if __name__ == '__main__':
    if len(sys.argv) > 1:
        address = sys.argv[1]
        details = get_address_model_input(address)
        print(details)
    else:
        print("No Address provided.")

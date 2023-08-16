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
    
    
def get_address_details(address):

    transactions = get_transaction_by_address.get_transactions(address)
    tokens = get_ERC20.get_ERC20(address)
        #Extracting existing details:

    # Computing new details:
    try:
        tim_diff_first_last = ((max(int(txn["timeStamp"]) for txn in transactions) - min(int(txn["timeStamp"]) for txn in transactions)) / 60)
    except ValueError:
        tim_diff_first_last = 0
    unq_rec_from_add = len(set(txn["from"] for txn in transactions if txn["to"].lower() == address.lower()))
    total_transactions = len(transactions)
    sent_txns = len([txn for txn in transactions if txn["from"].lower() == address.lower()])
    avg_min_rec_txns = average_time_between_sent_txns(transactions,address)    
    unq_rec_tkn = len(set(txn["tokenName"] for txn in tokens if txn["to"].lower() == address.lower()))
    total_erc_txn = len(tokens)
    rec_txn = len([txn for txn in transactions if txn['to'].lower() == address.lower()])
    try:
        total_eth_sent = sum([int(txn['value']) for txn in transactions if txn['from'].lower() == address.lower()])/1e18
    except ValueError:
        total_eth_sent = 0       
    avg_min_sen_txns = average_time_between_rec_txns(transactions,address)
    try:
        min_sent_val = min([int(txn['value']) for txn in transactions if txn["from"].lower() == address.lower()])/1e18
    except ValueError:
        min_sent_val = 0
    try:
        max_val_rec = max([int(txn['value']) for txn in transactions if txn["to"].lower() == address.lower()])/1e18
    except ValueError:
        max_val_rec = 0
    try:
        total_tkn_rec = sum(int(txn["value"]) for txn in tokens if txn["to"].lower() == address.lower()) / 1e18
    except ValueError:
        total_tkn_rec = 0
    try:
        min_val_rec = min([int(txn['value']) for txn in transactions if txn["to"].lower() == address.lower()])/1e18
    except ValueError:
        min_val_rec = 0
    try:
        max_val_sent = max([int(txn['value']) for txn in transactions if txn["from"].lower() == address.lower()])/1e18
    except ValueError:
        max_val_sent = 0
    avg_tkn_rec = avg_ERC20_received_values(transactions,address)
    try:
        total_tkn_sent = sum(int(txn["value"]) for txn in tokens if txn["from"].lower() == address.lower()) / 1e18
    except ValueError:
        total_tkn_sent = 0
    unq_add_sent =  len(set(txn["to"] for txn in transactions if txn["from"].lower() == address.lower()))
    try:
        min_tkn_rec = min([int(txn["value"]) for txn in tokens if txn["from"].lower() == address.lower()])/1e18
    except ValueError:
        min_tkn_rec = 0


    # Appending all details to DataFrame:
    transactional_details = {
        'Time between first and last transaction in minutes' : tim_diff_first_last, 
        'Unique recieved from address' : unq_rec_from_add,
        'Total transaction on address' : total_transactions,
        'Number of sent transactions' : sent_txns,
        'Average minutes between sent transactions' : avg_min_rec_txns,
        'Uniqe recieved from tokens': unq_rec_tkn,
        'Total tokens': total_erc_txn,
        'Total recieved transactions' : rec_txn,
        'Total ethereum sent' : total_eth_sent,
        'Average minutes betweeen sent transactions' :avg_min_sen_txns,
        'Minumum sent value':min_sent_val,
        'Maximum value recieved':max_val_rec,
        'Total ERC20 tokens recieved':total_tkn_rec,
        'Minimum value recieved':min_val_rec,
        'Maximum value recieved':max_val_sent,
        'Average ERC20 tokens recieved':avg_tkn_rec,
        'Total ERC 20 tokens sent':total_tkn_sent,
        'Unique sent to address':unq_add_sent,
        'Minimum tokens recieved':min_tkn_rec
    }
    return transactional_details



# Check if the script is being run directly
if __name__ == '__main__':
    if len(sys.argv) > 1:
        address = sys.argv[1]
        details = get_address_details(address)
        print(details)
    else:
        print("No Address provided.")

import sys
import get_transaction_by_hash


    
def get_transaction_details(transaction_hash):
    transaction = get_transaction_by_hash.get_transaction_by_hash(transaction_hash)
    if not transaction:
        return

    
    # Appending all details to DataFrame:
    transactional_details = transaction
    return transactional_details



if __name__ == '__main__':
    if len(sys.argv) > 1:
        transaction_hash = sys.argv[1]
        print(get_transaction_details(transaction_hash))

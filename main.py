import json
import hashlib
import os
from typing import Dict, List, Tuple

# Constants
MEMPOOL_DIR = "mempool"
DIFFICULTY_TARGET = "0000ffff00000000000000000000000000000000000000000000000000000000"
BLOCK_SPACE = 1_000_000  # Assuming a block size of 1MB for the example

# Functions
def is_transaction_valid(transaction: Dict) -> bool:
    # Implement your validation logic here. This is a placeholder logic.
    # A real validation would involve checking the transaction structure,
    # verifying digital signatures, etc.
    return True

def construct_block_header(coinbase_tx: str, txids: List[str]) -> str:
    # Construct the block header. Placeholder for the purposes of this example.
    # In a real situation, this would involve constructing the block header
    # with the previous hash, merkle root, timestamp, etc.
    return "block_header_placeholder"

def calculate_hash(block_header: str) -> str:
    # Calculate the SHA-256 hash of the block header
    return hashlib.sha256(block_header.encode('utf-8')).hexdigest()

def mine_block(block_header: str) -> Tuple[str, int]:
    nonce = 0
    while True:
        header_with_nonce = block_header + str(nonce)
        block_hash = calculate_hash(header_with_nonce)
        if int(block_hash, 16) < int(DIFFICULTY_TARGET, 16):
            return header_with_nonce, nonce
        nonce += 1

def select_transactions() -> List[str]:
    # Select valid transactions. Only select as many as fit in a block.
    txids = []
    block_size = len(construct_block_header("", txids))
    for filename in os.listdir(MEMPOOL_DIR):
        with open(os.path.join(MEMPOOL_DIR, filename), 'r') as file:
            transaction = json.load(file)
            tx_size = len(json.dumps(transaction))  # Simplistic tx size estimation
            if is_transaction_valid(transaction) and block_size + tx_size <= BLOCK_SPACE:
                txids.append(transaction['vin'][0]['txid'])
                block_size += tx_size
    return txids

# Main code
if __name__ == "__main__":
    try:
        # Serialize coinbase transaction (Placeholder)
        serialized_coinbase_tx = "coinbase_tx_placeholder"

        while True:
            # Select valid transactions and construct the block
            valid_txids = select_transactions()
            block_header = construct_block_header(serialized_coinbase_tx, valid_txids)
            
            # Mine the block
            final_block_header, nonce = mine_block(block_header)

            # Write the output file
            with open('output.txt', 'a') as output_file:  # Append mode
                output_file.write(f"Block mined with nonce {nonce}:\n")
                output_file.write(final_block_header + '\n')
                output_file.write(serialized_coinbase_tx + '\n')
                output_file.writelines('\n'.join(valid_txids) + '\n')
                output_file.write("\n")  # Separator between blocks
                
            # Optionally, you can break after a certain condition or pause
            # Here, we'll pause for a bit to simulate the time between blocks
            # time.sleep(60)  # Sleep for 1 minute (not active due to no import)

            # Remove processed transactions from the mempool
            for txid in valid_txids:
                tx_filename = txid + '.json'  # Assuming filename format
                os.remove(os.path.join(MEMPOOL_DIR, tx_filename))

            # Check if there are any transactions left to process
            if not os.listdir(MEMPOOL_DIR):
                break  # Exit the while loop if no transactions are left

    except KeyboardInterrupt:
        # Graceful exit if we want to stop the miner manually
        print("Mining stopped by user.")

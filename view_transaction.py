from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

tx_hash = "TON_HASH"

tx = w3.eth.get_transaction(tx_hash)

print(tx)
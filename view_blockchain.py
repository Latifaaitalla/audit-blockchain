from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

print("Connexion :", w3.is_connected())
print("Dernier bloc :", w3.eth.block_number)

latest_block = w3.eth.get_block("latest", full_transactions=True)

print("Hash du bloc :", latest_block.hash.hex())
print("Nombre de transactions :", len(latest_block.transactions))

for tx in latest_block.transactions:
    print("Transaction :", tx.hash.hex())
    print("From :", tx["from"])
    print("To :", tx["to"])
    print("Data :", tx["input"])
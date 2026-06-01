from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

address = Web3.to_checksum_address(
    "0xfe3b557e8fb62b89f4916b721be55ceb828dbd73"
)

print("Connexion :", w3.is_connected())

balance_wei = w3.eth.get_balance(address)
balance_eth = w3.from_wei(balance_wei, "ether")

print("Adresse :", address)
print("Solde Wei :", balance_wei)
print("Solde ETH :", balance_eth)
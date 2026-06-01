from web3 import Web3

# création d’un nouveau compte Ethereum
account = Web3().eth.account.create()

print("Adresse Ethereum :")
print(account.address)

print("\nClé privée :")
print(account.key.hex())
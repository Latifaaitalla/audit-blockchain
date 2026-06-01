from web3 import Web3
# Connexion Besu
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
if not w3.is_connected():
    raise Exception("Connexion Besu impossible")
# Compte Ethereum
private_key = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"
account = w3.eth.account.from_key(private_key)
sender = account.address
# Lire le hash
with open("data/hashes/transform_hash.txt", "r", encoding="utf-8") as f:
    hash_value = f.read().strip()
# Lire la signature
with open("data/hashes/transform_signature.txt", "r", encoding="utf-8") as f:
    signature = f.read().strip()
# Message à enregistrer
payload = f"""
HASH:{hash_value}
SIGNATURE:{signature}
AUDITOR:{sender}
"""
nonce = w3.eth.get_transaction_count(sender, "pending")
tx = {
    "nonce": nonce,
    "to": sender,
    "value": 0,
    "data": w3.to_hex(text=payload),
    "gas": 300000,
    "gasPrice": w3.to_wei(1, "gwei"),
    "chainId": w3.eth.chain_id
}
signed_tx = w3.eth.account.sign_transaction(
    tx,
    private_key
)
tx_hash = w3.eth.send_raw_transaction(
    signed_tx.raw_transaction
)
print("Transaction :", tx_hash.hex())
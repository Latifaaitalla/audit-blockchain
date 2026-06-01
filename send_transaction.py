from web3 import Web3
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
private_key = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"
sender = Web3.to_checksum_address(
    "0xfe3b557e8fb62b89f4916b721be55ceb828dbd73"
)
receiver = Web3.to_checksum_address(
    "0x627306090abaB3A6e1400e9345bC60c78a8BEf57"
)
nonce = w3.eth.get_transaction_count(sender)
tx = {
    "nonce": nonce,
    "to": receiver,
    "value": w3.to_wei(1, "ether"),
    "gas": 21000,
    "gasPrice": w3.to_wei(1, "gwei"),
    "chainId": w3.eth.chain_id,
}
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Transaction envoyée :")
print(w3.to_hex(tx_hash))
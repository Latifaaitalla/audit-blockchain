from eth_account import Account
from eth_account.messages import encode_defunct

# Lire le hash
with open("data/hashes/transform_hash.txt", "r", encoding="utf-8") as file:
    hash_value = file.read().strip()

# Lire la signature
with open("data/hashes/transform_signature.txt", "r", encoding="utf-8") as file:
    signature = file.read().strip()

# Préparer le message
message = encode_defunct(text=hash_value)

# Récupérer l'adresse du signataire
signer_address = Account.recover_message(
    message,
    signature=signature
)

print("Hash :", hash_value)
print("Signature :", signature)
print("Adresse récupérée :", signer_address)
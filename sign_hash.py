from eth_account import Account
from eth_account.messages import encode_defunct
import os

# Hash déjà généré du fichier transformé
hash_path = "data/hashes/transform_hash.txt"

# Fichier où sauvegarder la signature
signature_path = "data/hashes/transform_signature.txt"

# Clé privée du compte Ethereum de l'auditeur
private_key = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"

# Lire le hash
with open(hash_path, "r", encoding="utf-8") as file:
    hash_value = file.read().strip()

# Préparer le message à signer
message = encode_defunct(text=hash_value)

# Signer le hash
signed_message = Account.sign_message(message, private_key=private_key)

# Sauvegarder la signature
os.makedirs("data/hashes", exist_ok=True)

with open(signature_path, "w", encoding="utf-8") as file:
    file.write(signed_message.signature.hex())

print("Hash signé avec succès.")
print("Hash :", hash_value)
account = Account.from_key(private_key)
print("Adresse auditeur :", account.address)
print("Signature :", signed_message.signature.hex())
print("Signature sauvegardée dans :", signature_path)
import hashlib
import os

file_path = "data/rapport_financier.pdf"
hash_output = "data/hashes/pdf_hash.txt"

# Créer le dossier hashes s'il n'existe pas
os.makedirs("data/hashes", exist_ok=True)

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()

hash_value = calculate_sha256(file_path)

# Sauvegarde du hash
with open(hash_output, "w", encoding="utf-8") as file:
    file.write(hash_value)

print("Hash SHA-256 du rapport PDF :")
print(hash_value)

print("Hash sauvegardé dans :", hash_output)
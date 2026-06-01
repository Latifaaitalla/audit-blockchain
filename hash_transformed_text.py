import hashlib
import os

file_path = "data/texte_transforme.txt"
hash_output = "data/hashes/transform_hash.txt"

# Créer le dossier hashes s'il n'existe pas
os.makedirs("data/hashes", exist_ok=True)

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

hash_value = hashlib.sha256(text.encode("utf-8")).hexdigest()

# Sauvegarde du hash
with open(hash_output, "w", encoding="utf-8") as file:
    file.write(hash_value)

print("Hash SHA-256 du texte transformé :")
print(hash_value)

print("Hash sauvegardé dans :", hash_output)
import hashlib
import psycopg2
from web3 import Web3

# =========================
# Connexion à Besu
# =========================

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

if not w3.is_connected():
    raise Exception("Impossible de se connecter à Besu")

print("Connexion Besu : OK")

# =========================
# Génération du hash actuel
# =========================

file_path = "data/texte_transforme.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

current_hash = hashlib.sha256(
    content.encode("utf-8")
).hexdigest()

print("\nHash actuel :")
print(current_hash)

# =========================
# Connexion PostgreSQL
# =========================

conn = psycopg2.connect(
    host="localhost",
    database="audit_db",
    user="postgres",
    password="Latifa@2004",
    port="5432"
)

cursor = conn.cursor()

# =========================
# Récupération du tx_hash
# =========================

cursor.execute("""
SELECT tx_hash
FROM etl_hashes
WHERE etape = 'Transform'
ORDER BY id DESC
LIMIT 1;
""")

result = cursor.fetchone()

if not result:
    raise Exception("Aucune transaction blockchain trouvée")

tx_hash = result[0]

print("\nTransaction blockchain :")
print(tx_hash)

# =========================
# Lecture de la transaction blockchain
# =========================

tx = w3.eth.get_transaction(tx_hash)

# Données stockées dans la transaction
blockchain_data = tx["input"].hex()

# Suppression du préfixe 0x
if blockchain_data.startswith("0x"):
    blockchain_data = blockchain_data[2:]

# Conversion hex -> texte
blockchain_hash = bytes.fromhex(
    blockchain_data
).decode("utf-8")

# =========================
# Vérification d'intégrité
# =========================

print("\nRésultat de vérification :")

if current_hash == blockchain_hash:
    print("✓ Rapport intègre")
else:
    print("✗ Rapport modifié")

cursor.close()
conn.close()
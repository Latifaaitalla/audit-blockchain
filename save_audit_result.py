import hashlib
import psycopg2
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

# =========================
# Configuration
# =========================

REPORT_NAME = "rapport_financier.pdf"
FILE_TO_VERIFY = "data/texte_transforme.txt"

HASH_FILE = "data/hashes/transform_hash.txt"
SIGNATURE_FILE = "data/hashes/transform_signature.txt"

POSTGRES_PASSWORD = "Latifa@2004"

# =========================
# Connexion Besu
# =========================

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

if not w3.is_connected():
    raise Exception("Erreur : impossible de se connecter à Besu")

# =========================
# Hash actuel du fichier
# =========================

with open(FILE_TO_VERIFY, "r", encoding="utf-8") as file:
    content = file.read()

current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

# =========================
# Lecture hash officiel + signature
# =========================

with open(HASH_FILE, "r", encoding="utf-8") as file:
    stored_hash = file.read().strip()

with open(SIGNATURE_FILE, "r", encoding="utf-8") as file:
    signature = file.read().strip()

# =========================
# Vérification signature
# =========================

message = encode_defunct(text=stored_hash)

auditor_address = Account.recover_message(
    message,
    signature=signature
)

# =========================
# Statut d’intégrité
# =========================

if current_hash == stored_hash:
    integrity_status = "Valide"
else:
    integrity_status = "Modifié"

# =========================
# Récupération tx_hash blockchain
# =========================

conn = psycopg2.connect(
    host="localhost",
    database="audit_db",
    user="postgres",
    password=POSTGRES_PASSWORD,
    port="5432"
)

cursor = conn.cursor()

cursor.execute("""
SELECT tx_hash
FROM etl_hashes
WHERE etape = 'Transform'
ORDER BY id DESC
LIMIT 1;
""")

result = cursor.fetchone()
tx_hash = result[0] if result else None

# =========================
# Création table audit_results
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_results (
    id SERIAL PRIMARY KEY,
    report_name VARCHAR(255),
    hash_sha256 TEXT,
    tx_hash TEXT,
    auditor_address TEXT,
    signature TEXT,
    integrity_status VARCHAR(50),
    verification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# =========================
# Insertion résultat audit
# =========================

cursor.execute("""
INSERT INTO audit_results (
    report_name,
    hash_sha256,
    tx_hash,
    auditor_address,
    signature,
    integrity_status
)
VALUES (%s, %s, %s, %s, %s, %s);
""", (
    REPORT_NAME,
    current_hash,
    tx_hash,
    auditor_address,
    signature,
    integrity_status
))

conn.commit()

cursor.close()
conn.close()

print("Résultat d'audit enregistré dans PostgreSQL.")
print("Rapport :", REPORT_NAME)
print("Statut :", integrity_status)
print("Auditeur :", auditor_address)
print("Transaction blockchain :", tx_hash)
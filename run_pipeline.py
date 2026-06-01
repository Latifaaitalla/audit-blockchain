import sys
import os
import hashlib
import pdfplumber
import psycopg2
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

# =========================
# Vérifier le nom du rapport
# =========================

if len(sys.argv) < 2:
    print("Utilisation : python run_pipeline.py nom_rapport.pdf")
    sys.exit()

report_name = sys.argv[1]
pdf_path = os.path.join(
    "Data",
    "reports",
    report_name
)

if not os.path.exists(pdf_path):
    print("Erreur : fichier PDF introuvable :", pdf_path)
    sys.exit()

# =========================
# Dossiers de sortie
# =========================

base_name = os.path.splitext(report_name)[0]

os.makedirs("data/extracted", exist_ok=True)
os.makedirs("data/transformed", exist_ok=True)
os.makedirs("data/hashes", exist_ok=True)

extracted_path = f"data/extracted/{base_name}_extracted.txt"
transformed_path = f"data/transformed/{base_name}_transformed.txt"

pdf_hash_path = f"data/hashes/{base_name}_pdf_hash.txt"
extract_hash_path = f"data/hashes/{base_name}_extract_hash.txt"
transform_hash_path = f"data/hashes/{base_name}_transform_hash.txt"
signature_path = f"data/hashes/{base_name}_signature.txt"

# =========================
# Configuration
# =========================

POSTGRES_PASSWORD = "Latifa@2004"

PRIVATE_KEY = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

if not w3.is_connected():
    raise Exception("Connexion Besu impossible")

account = Account.from_key(PRIVATE_KEY)
sender = account.address

# =========================
# Fonction hash
# =========================

def sha256_file(path, binary=True):
    sha = hashlib.sha256()

    mode = "rb" if binary else "r"

    with open(path, mode, encoding=None if binary else "utf-8") as file:
        if binary:
            for block in iter(lambda: file.read(4096), b""):
                sha.update(block)
        else:
            sha.update(file.read().encode("utf-8"))

    return sha.hexdigest()

def save_text(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

# =========================
# 1. Hash PDF original
# =========================

pdf_hash = sha256_file(pdf_path, binary=True)
save_text(pdf_hash_path, pdf_hash)

# =========================
# 2. Extraction PDF
# =========================

text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

save_text(extracted_path, text)

# =========================
# 3. Hash texte extrait
# =========================

extract_hash = sha256_file(extracted_path, binary=False)
save_text(extract_hash_path, extract_hash)

# =========================
# 4. Transformation
# =========================

transformed_text = text.lower()
transformed_text = transformed_text.strip()
transformed_text = " ".join(transformed_text.split())

save_text(transformed_path, transformed_text)

# =========================
# 5. Hash texte transformé
# =========================

transform_hash = sha256_file(transformed_path, binary=False)
save_text(transform_hash_path, transform_hash)

# =========================
# 6. Signature numérique
# =========================

message = encode_defunct(text=transform_hash)
signed_message = Account.sign_message(message, private_key=PRIVATE_KEY)

signature = signed_message.signature.hex()
save_text(signature_path, signature)

# =========================
# 7. Connexion PostgreSQL
# =========================

conn = psycopg2.connect(
    host="localhost",
    database="audit_db",
    user="postgres",
    password=POSTGRES_PASSWORD,
    port="5432"
)

cursor = conn.cursor()

# =========================
# 8. Création des tables
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS rapports_financiers (
    id SERIAL PRIMARY KEY,
    nom_rapport VARCHAR(255),
    contenu TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS etl_hashes (
    id SERIAL PRIMARY KEY,
    report_name VARCHAR(255),
    etape VARCHAR(100),
    hash_sha256 TEXT,
    tx_hash TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

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
)
""")

# =========================
# 9. Stocker rapport transformé
# =========================

cursor.execute("""
INSERT INTO rapports_financiers (nom_rapport, contenu)
VALUES (%s, %s)
""", (report_name, transformed_text))

# =========================
# 10. Envoyer hash vers blockchain
# =========================

hashes = [
    ("PDF Original", pdf_hash),
    ("Extract", extract_hash),
    ("Transform", transform_hash)
]

transform_tx_hash = None

for etape, hash_value in hashes:
    nonce = w3.eth.get_transaction_count(sender, "pending")

    tx = {
        "nonce": nonce,
        "to": sender,
        "value": 0,
        "data": w3.to_hex(text=hash_value),
        "gas": 100000,
        "gasPrice": w3.to_wei(2, "gwei"),
        "chainId": w3.eth.chain_id
    }

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_hash_hex = w3.to_hex(tx_hash)

    if etape == "Transform":
        transform_tx_hash = tx_hash_hex

    cursor.execute("""
    INSERT INTO etl_hashes (report_name, etape, hash_sha256, tx_hash)
    VALUES (%s, %s, %s, %s)
    """, (report_name, etape, hash_value, tx_hash_hex))

    conn.commit()

# =========================
# 11. Vérification intégrité
# =========================

current_hash = sha256_file(transformed_path, binary=False)

if current_hash == transform_hash:
    integrity_status = "Valide"
else:
    integrity_status = "Modifié"

# =========================
# 12. Stocker résultat audit
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
VALUES (%s, %s, %s, %s, %s, %s)
""", (
    report_name,
    transform_hash,
    transform_tx_hash,
    sender,
    signature,
    integrity_status
))

conn.commit()

cursor.close()
conn.close()

print("Pipeline terminé avec succès.")
print("Rapport :", report_name)
print("Hash transformé :", transform_hash)
print("Signature :", signature)
print("Auditeur :", sender)
print("Statut :", integrity_status)
print("Transaction blockchain :", transform_tx_hash)
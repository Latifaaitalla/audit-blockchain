import psycopg2
from web3 import Web3
# Connexion à Besu
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
if not w3.is_connected():
    raise Exception("Erreur : impossible de se connecter à Besu")
print("Connexion Besu : OK")
# Compte Ethereum préfinancé Besu
private_key = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"
sender = Web3.to_checksum_address(
    "0xfe3b557e8fb62b89f4916b721be55ceb828dbd73"
)
# Connexion PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="audit_db",
    user="postgres",
    password="Latifa@2004",
    port="5432"
)
cursor = conn.cursor()
# Ajouter une colonne tx_hash si elle n'existe pas
cursor.execute("""
ALTER TABLE etl_hashes
ADD COLUMN IF NOT EXISTS tx_hash TEXT;
""")
conn.commit()
# Récupérer les hash qui ne sont pas encore envoyés à la blockchain
cursor.execute("""
SELECT id, etape, hash_sha256
FROM etl_hashes
WHERE tx_hash IS NULL;
""")
rows = cursor.fetchall()
if not rows:
    print("Aucun hash à envoyer vers la blockchain.")
else:
    for row in rows:
        hash_id, etape, hash_sha256 = row

        print(f"Envoi du hash de l'étape : {etape}")

        nonce = w3.eth.get_transaction_count(sender, "pending")

        tx = {
            "nonce": nonce,
            "to": sender,
            "value": 0,
            "data": w3.to_hex(text=hash_sha256),
            "gas": 100000,
            "gasPrice": w3.to_wei(1, "gwei"),
            "chainId": w3.eth.chain_id,
        }
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = w3.to_hex(tx_hash)
        print("Transaction envoyée :", tx_hash_hex)
        # Sauvegarder le hash de transaction dans PostgreSQL
        cursor.execute("""
        UPDATE etl_hashes
        SET tx_hash = %s
        WHERE id = %s;
        """, (tx_hash_hex, hash_id))
        conn.commit()
cursor.close()
conn.close()
print("Tous les hash ETL ont été envoyés vers la blockchain.")
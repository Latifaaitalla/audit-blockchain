import psycopg2

# Chemins des fichiers qui contiennent les hash déjà générés
pdf_hash_path = "data/hashes/pdf_hash.txt"
extract_hash_path = "data/hashes/extract_hash.txt"
transform_hash_path = "data/hashes/transform_hash.txt"

# Fonction pour lire un hash déjà généré
def read_hash(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()
# Lecture des hash existants
pdf_hash = read_hash(pdf_hash_path)
extract_hash = read_hash(extract_hash_path)
transform_hash = read_hash(transform_hash_path)
# Connexion PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="audit_db",
    user="postgres",
    password="Latifa@2004",
    port="5432"
)
cursor = conn.cursor()
# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS etl_hashes (
    id SERIAL PRIMARY KEY,
    etape VARCHAR(100),
    hash_sha256 TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
# Insertion des hash déjà générés
hashes = [
    ("PDF Original", pdf_hash),
    ("Extract", extract_hash),
    ("Transform", transform_hash)
]
for etape, hash_value in hashes:
    cursor.execute("""
    INSERT INTO etl_hashes (etape, hash_sha256)
    VALUES (%s, %s)
    """, (etape, hash_value))
conn.commit()
cursor.close()
conn.close()
print("Hash ETL existants stockés dans PostgreSQL avec succès.")
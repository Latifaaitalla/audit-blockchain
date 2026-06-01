import psycopg2

file_path = "data/texte_transforme.txt"

with open(file_path, "r", encoding="utf-8") as file:
    contenu = file.read()

conn = psycopg2.connect(
    host="localhost",
    database="audit_db",
    user="postgres",
    password="Latifa@2004",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rapports_financiers (
    id SERIAL PRIMARY KEY,
    nom_rapport VARCHAR(255),
    contenu TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
INSERT INTO rapports_financiers (nom_rapport, contenu)
VALUES (%s, %s)
""", ("rapport_financier.pdf", contenu))

conn.commit()

cursor.close()
conn.close()

print("Données chargées avec succès dans PostgreSQL.")
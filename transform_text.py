input_path = "data/texte_extrait.txt"
output_path = "data/texte_transforme.txt"

with open(input_path, "r", encoding="utf-8") as file:
    text = file.read()

# Transformations simples
text = text.lower()
text = text.strip()
text = " ".join(text.split())

with open(output_path, "w", encoding="utf-8") as file:
    file.write(text)

print("Transformation terminée.")
print("Fichier créé :", output_path)
import pdfplumber

pdf_path = "data/Rapport_financier.pdf"
output_path = "data/texte_extrait.txt"

text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

with open(output_path, "w", encoding="utf-8") as file:
    file.write(text)

print("Extraction terminée.")
print("Fichier créé :", output_path)
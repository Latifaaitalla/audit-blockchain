# Système Blockchain de Preuve de Provenance des Données pour les Rapports Financiers Audités

## Présentation du projet

Ce projet a pour objectif de mettre en place un système de preuve de provenance des données basé sur la blockchain afin de garantir l’intégrité, la traçabilité, l’authenticité et la non-répudiation des rapports financiers audités.

La solution repose sur l’intégration de plusieurs technologies :

* Python
* PostgreSQL
* Hyperledger Besu
* Ethereum
* SHA-256
* Signatures numériques
* Power BI

Le système permet d’enregistrer les empreintes numériques (hash) des différentes étapes du processus ETL dans une blockchain privée afin de fournir une preuve immuable des traitements réalisés sur les données.

---

# Architecture du système

```text
Rapport Financier (PDF)
            │
            ▼
      Pipeline ETL
            │
            ▼
      Hash SHA-256
            │
            ▼
   Signature Numérique
            │
            ▼
 Blockchain Hyperledger Besu
            │
            ▼
        PostgreSQL
            │
            ▼
          Power BI
```

---

# Fonctionnalités du projet

## Preuve de provenance des données

* Importation des rapports financiers PDF
* Extraction du contenu textuel
* Transformation des données
* Génération des empreintes SHA-256

## Intégration Blockchain

* Réseau privé Hyperledger Besu
* Enregistrement des hash dans la blockchain
* Traçabilité des transactions blockchain

## Vérification d’intégrité

* Vérification automatique des documents
* Détection des modifications non autorisées
* Validation basée sur la blockchain

## Mécanisme de non-répudiation

* Création de comptes Ethereum
* Génération de signatures numériques
* Vérification des signatures
* Authentification de l’auditeur

## Visualisation décisionnelle

* Centralisation des résultats dans PostgreSQL
* Création de tableaux de bord Power BI
* Suivi des opérations d’audit

---

# Structure du projet

```text
audit-blockchain/
│
├── Data/
│   ├── reports/
│   ├── extracted/
│   ├── transformed/
│   └── hashes/
│
├── create_account.py
├── run_pipeline.py
├── verify_from_blockchain.py
├── sign_hash.py
├── verify_signature.py
├── save_audit_result.py
│
├── requirements.txt
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# Prérequis

Avant d’exécuter le projet, les logiciels suivants doivent être installés :

* Python 3.10 ou supérieur
* Docker Desktop
* PostgreSQL
* Git

---

# Cloner le projet

```bash
git clone https://github.com/VOTRE_COMPTE/audit-blockchain.git

cd audit-blockchain
```

---

# Installation des dépendances Python

```bash
pip install -r requirements.txt
```

Ou manuellement :

```bash
pip install web3
pip install psycopg2-binary
pip install pdfplumber
pip install eth-account
```

---

# Démarrage de l’infrastructure

## Lancement avec Docker

```bash
docker-compose up -d
```

Vérification :

```bash
docker ps
```

Les conteneurs suivants doivent être actifs :

```text
besu-node
audit-postgres
```

---

# Configuration PostgreSQL

Base de données :

```text
audit_db
```

Paramètres par défaut :

```text
Utilisateur : postgres
Mot de passe : postgres
Port : 5432
```

---

# Ajout des rapports financiers

Déposer les rapports PDF dans :

```text
Data/reports/
```

Exemple :

```text
Data/reports/
├── rapport_financier_cosumar.pdf
├── Rapport_financier_ocp.pdf
├── Rapport_financier_Attijari_wafa_bank.pdf
```

---

# Exécution du pipeline complet

Le projet dispose d’un pipeline automatisé permettant d’exécuter l’ensemble du processus de preuve de provenance.

Pour traiter un rapport financier :

```bash
python run_pipeline.py rapport_financier_cosumar.pdf
```

Exemples :

```bash
python run_pipeline.py rapport_financier_cosumar.pdf

python run_pipeline.py Rapport_financier_ocp.pdf

python run_pipeline.py Rapport_financier_Attijari_wafa_bank.pdf
```

---

# Étapes exécutées automatiquement

Le pipeline réalise successivement :

1. Génération du hash du PDF original
2. Extraction du texte
3. Génération du hash du texte extrait
4. Transformation des données
5. Génération du hash du texte transformé
6. Signature numérique
7. Stockage dans PostgreSQL
8. Enregistrement dans la blockchain
9. Vérification d’intégrité
10. Sauvegarde des résultats d’audit

---

# Exemple de résultat

```text
Pipeline terminé avec succès

Rapport :
rapport_financier_cosumar.pdf

Hash :
3017105c796e9469070e14f9968e3d64...

Auditeur :
0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73

Statut :
Valide

Transaction Blockchain :
0x0c726318a0f2e579b4a5287e13836881...
```

---

# Tables PostgreSQL

## Rapports financiers

```sql
SELECT * FROM rapports_financiers;
```

## Hash ETL

```sql
SELECT * FROM etl_hashes;
```

## Résultats d’audit

```sql
SELECT * FROM audit_results;
```

---

# Vérification d’intégrité

Le système compare :

```text
Hash actuel du fichier
          VS
Hash stocké dans la blockchain
```

Résultats possibles :

```text
Valide
```

ou

```text
Modifié
```

---

# Mécanisme de non-répudiation

Chaque rapport est signé numériquement à l’aide de la clé privée Ethereum de l’auditeur.

Le système vérifie :

* l’identité du signataire ;
* la validité de la signature ;
* l’authenticité du hash enregistré.

Ce mécanisme garantit :

* l’authenticité ;
* la responsabilité ;
* la non-répudiation.

---

# Tableau de bord Power BI

Power BI se connecte directement à PostgreSQL afin de visualiser :

### Indicateurs clés (KPI)

* Nombre total de rapports audités
* Nombre de rapports valides
* Nombre de rapports modifiés
* Nombre de transactions blockchain

### Visualisations

* Répartition des statuts d’intégrité
* Historique des vérifications
* Activité des auditeurs
* Traçabilité blockchain

---

# Technologies utilisées

* Python
* PostgreSQL
* Hyperledger Besu
* Ethereum
* Web3.py
* SHA-256
* Docker
* Power BI

---

# Auteur

AIT ALLA Latifa et 
BOUZIANE Salma 

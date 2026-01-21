# APIs Gouvernementales Canadiennes et Portails CKAN
## Ressources pour le Projet Zero Obstacle

---

## 📊 PORTAILS OPEN DATA (CKAN)

### 1. Open Data Canada (Fédéral)
**URL** : https://open.canada.ca/data/  
**API** : https://open.canada.ca/data/api/3/  
**Type** : CKAN API  
**Documentation** : https://open.canada.ca/en/access-our-application-programming-interface-api

**Datasets Pertinents** :
- Prestations et programmes sociaux
- Données d'emploi et assurance-emploi
- Statistiques démographiques
- Formulaires gouvernementaux
- Données fiscales agrégées

**Exemple de Requête** :
```bash
# Rechercher des datasets sur les prestations
curl "https://open.canada.ca/data/api/3/action/package_search?q=benefits+OR+prestations&rows=10"

# Obtenir un dataset spécifique
curl "https://open.canada.ca/data/api/3/action/package_show?id=DATASET_ID"
```

**Utilisation pour Zero Obstacle** :
- Récupérer les critères d'admissibilité des programmes
- Télécharger les formulaires en format structuré
- Obtenir les montants de prestations à jour

---

### 2. Données Québec
**URL** : https://www.donneesquebec.ca/  
**API** : https://www.donneesquebec.ca/api/3/  
**Type** : CKAN API  
**Documentation** : https://www.donneesquebec.ca/fr/doc-api/

**Datasets Pertinents** :
- Programmes d'aide financière du Québec
- Données RAMQ (santé)
- Services sociaux et communautaires
- Aide financière aux études (AFE)

**Exemple de Requête** :
```bash
# Rechercher datasets québécois sur aide financière
curl "https://www.donneesquebec.ca/api/3/action/package_search?q=aide+financiere"
```

**Utilisation pour Zero Obstacle** :
- Compléter les données fédérales avec programmes provinciaux
- Règles d'admissibilité spécifiques au Québec

---

### 3. Ontario Open Data
**URL** : https://data.ontario.ca/  
**API** : https://data.ontario.ca/api/3/  
**Type** : CKAN API  
**Documentation** : https://data.ontario.ca/about

**Datasets Pertinents** :
- Services sociaux et communautaires Ontario
- Ontario Works (assistance sociale)
- RAFEO (aide financière étudiante)

---

### 4. BC Data Catalogue (Colombie-Britannique)
**URL** : https://catalogue.data.gov.bc.ca/  
**API** : https://catalogue.data.gov.bc.ca/api/3/  
**Type** : CKAN API  

---

## 🏛️ APIS GOUVERNEMENTALES FÉDÉRALES

### 1. Service Canada - API Web Services
**URL** : https://www.canada.ca/en/employment-social-development/programs/direct-deposit/api.html  
**Type** : REST API  
**Accès** : Public (certaines fonctions nécessitent authentification)

**Services Disponibles** :
- Vérification d'éligibilité à l'assurance-emploi
- Statut de demandes de prestations
- Information sur les programmes sociaux

**Documentation** :
- https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/ei-telephone-services.html

**Utilisation pour Zero Obstacle** :
- Vérification en temps réel de l'éligibilité
- Suivi de demandes

---

### 2. Agence du Revenu du Canada (ARC) - Mon dossier API
**URL** : https://www.canada.ca/en/revenue-agency/services/e-services/represent-a-client.html  
**Type** : Web Services (SOAP/REST)  
**Accès** : Nécessite autorisation et accréditation

**Services Disponibles** :
- Accès aux informations fiscales
- Calcul de l'Allocation canadienne pour enfants (ACE)
- Crédits d'impôt

**Note** : Nécessite inscription comme représentant autorisé. Pour MVP, utiliser données Open Data.

---

### 3. Jobs Bank API (Guichet Emplois)
**URL** : https://www.jobbank.gc.ca/api  
**Type** : REST API  
**Documentation** : Sur demande via https://www.jobbank.gc.ca/contact_us

**Services Disponibles** :
- Recherche d'emplois
- Information sur le marché du travail
- Programmes de formation

**Utilisation pour Zero Obstacle** :
- Suggestions d'emploi pour utilisateurs
- Information sur programmes de formation disponibles

---

### 4. Immigration, Réfugiés et Citoyenneté Canada (IRCC)
**URL** : https://www.canada.ca/en/immigration-refugees-citizenship/corporate/partners-service-providers/information-sharing-authorized-representatives.html  
**Type** : Web Services  
**Accès** : Nécessite autorisation

**Services Disponibles** :
- Vérification de statut d'immigration
- Éligibilité aux programmes d'immigration

**Note** : Pour MVP, utiliser données Open Data sur critères d'éligibilité.

---

## 🇨🇦 APIS PROVINCIALES

### Québec

#### 1. Retraite Québec - Services en ligne
**URL** : https://www.retraitequebec.gouv.qc.ca/  
**Type** : Services Web  
**Services** :
- Calcul de rente du RRQ
- Information sur régimes de retraite

#### 2. Revenu Québec - Services Web
**URL** : https://www.revenuquebec.ca/fr/services-en-ligne/  
**Type** : Services Web  
**Services** :
- Crédit d'impôt solidarité
- Allocation famille
- Soutien aux enfants

#### 3. Services Québec - Mon dossier citoyen
**URL** : https://www.quebec.ca/mon-dossier-citoyen  
**Services** :
- Accès centralisé aux services gouvernementaux québécois

---

### Ontario

#### 1. Ontario Works API
**Documentation** : Via portails municipaux (Toronto, Ottawa, etc.)  
**Services** :
- Information sur aide sociale
- Critères d'admissibilité

---

## 📄 APIS DE FORMULAIRES ET DOCUMENTS

### 1. Forms Service Canada
**URL** : https://catalogue.servicecanada.gc.ca/content/EForms/en/Index.html  
**Type** : Catalogue de formulaires PDF

**Utilisation pour Zero Obstacle** :
- Télécharger formulaires PDF officiels
- Parser et extraire champs avec pdfplumber
- Créer templates de préremplissage

**Formulaires Clés** :
- EI (Assurance-emploi) : formulaires série SC
- RPC (Régime de pensions du Canada) : formulaires série ISP
- SV (Sécurité de la vieillesse) : formulaires série OAS
- ACE (Allocation canadienne pour enfants) : RC66

---

### 2. Bibliothèque de formulaires ARC
**URL** : https://www.canada.ca/fr/agence-revenu/services/formulaires-publications.html  
**Type** : Catalogue PDF/HTML

**Formulaires Clés** :
- T1 (Déclaration de revenus)
- T4 (Relevé d'emploi)
- RC66 (Allocation canadienne pour enfants)

---

## 📊 APIS DE DONNÉES STATISTIQUES

### 1. Statistique Canada - API Web Data Service
**URL** : https://www.statcan.gc.ca/en/developers  
**API** : https://www150.statcan.gc.ca/t1/wds/rest/  
**Type** : REST API  
**Documentation** : https://www.statcan.gc.ca/en/developers/wds

**Données Disponibles** :
- Indicateurs économiques
- Données démographiques
- Taux de chômage
- Coût de la vie
- Seuils de faible revenu (pour calculs d'admissibilité)

**Exemple de Requête** :
```bash
# Obtenir données de population
curl "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriod?vectorIds=1&startRefPeriod=2020-01&endRefPeriod=2023-12"
```

**Utilisation pour Zero Obstacle** :
- Calculer seuils d'admissibilité basés sur revenu médian
- Contextualiser les montants de prestations

---

### 2. Portail géospatial du Canada
**URL** : https://gcgeo.gc.ca/  
**API** : WMS/WFS standards

**Utilisation** :
- Localiser bureaux Service Canada
- Calculer distances pour services en personne

---

## 🔍 APIS DE RECHERCHE ET NAVIGATION

### 1. Canada.ca Search API
**URL** : https://www.canada.ca/en/government/about/about-canada-ca.html  
**Type** : Search API (Adobe Search&Promote)

**Utilisation pour Zero Obstacle** :
- Recherche de pages pertinentes sur canada.ca
- Extraction de contenu officiel

---

### 2. CanLII API (Lois et Jurisprudence)
**URL** : https://www.canlii.org/en/tools/api_documentation.html  
**Type** : REST API  
**Accès** : Gratuit avec clé API

**Services** :
- Recherche de lois fédérales et provinciales
- Accès aux textes législatifs

**Utilisation pour Zero Obstacle** :
- Citer sources légales exactes
- Vérifier critères d'admissibilité dans la loi

**Exemple de Requête** :
```bash
curl "https://api.canlii.org/v1/caseBrowse/en/?api_key=YOUR_KEY"
```

---

## 🛠️ IMPLÉMENTATION RECOMMANDÉE

### Phase 1 : Open Data (Semaines 1-2)

**Bibliothèque Python** : `ckanapi`
```bash
pip install ckanapi
```

**Code Exemple** :
```python
from ckanapi import RemoteCKAN

# Connexion Open Data Canada
ckan_canada = RemoteCKAN('https://open.canada.ca/data')

# Rechercher datasets sur prestations
results = ckan_canada.action.package_search(
    q='benefits OR prestations',
    fq='organization:service-canada',
    rows=50
)

for dataset in results['results']:
    print(f"Dataset: {dataset['title']}")
    print(f"URL: {dataset['url']}")
    
    # Télécharger ressources
    for resource in dataset['resources']:
        if resource['format'].lower() in ['csv', 'json', 'xml']:
            # Télécharger et parser
            data = download_resource(resource['url'])
```

---

### Phase 2 : Statistique Canada API (Semaines 3-4)

**Bibliothèque Python** : `requests`
```python
import requests

def get_statcan_data(vector_id, start_date, end_date):
    """Récupère données Statistique Canada"""
    url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriod"
    params = {
        'vectorIds': vector_id,
        'startRefPeriod': start_date,
        'endRefPeriod': end_date
    }
    response = requests.get(url, params=params)
    return response.json()

# Exemple : Taux de chômage
unemployment_data = get_statcan_data(
    vector_id='14100287',  # Vecteur taux de chômage
    start_date='2023-01',
    end_date='2024-01'
)
```

---

### Phase 3 : Formulaires PDF (Semaines 5-6)

**Bibliothèque Python** : `pdfplumber`
```python
import pdfplumber
import requests

def download_and_parse_form(form_url):
    """Télécharge et parse formulaire PDF gouvernemental"""
    response = requests.get(form_url)
    
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        # Extraire texte
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        
        # Extraire champs de formulaire
        fields = []
        for page in pdf.pages:
            # pdfplumber peut extraire champs interactifs
            if hasattr(page, 'annots'):
                for annot in page.annots:
                    if annot.get('Subtype') == 'Widget':
                        fields.append({
                            'name': annot.get('T'),
                            'type': annot.get('FT'),
                            'value': annot.get('V')
                        })
        
        return {'text': text, 'fields': fields}

# Exemple : Formulaire EI
ei_form = download_and_parse_form(
    'https://catalogue.servicecanada.gc.ca/content/EForms/en/Detail.html?Form=INS3166'
)
```

---

### Phase 4 : CanLII pour Législation (Semaines 7-8)

**Code Exemple** :
```python
import requests

CANLII_API_KEY = "your_api_key"  # Obtenir sur https://www.canlii.org/en/info/api.html

def search_legislation(query):
    """Recherche lois canadiennes via CanLII"""
    url = "https://api.canlii.org/v1/legislation"
    headers = {'Authorization': f'Bearer {CANLII_API_KEY}'}
    params = {'search': query, 'language': 'fr'}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Exemple : Recherche loi sur l'assurance-emploi
ei_laws = search_legislation("Employment Insurance Act")
```

---

## 📋 CHECKLIST D'INTÉGRATION

### APIs Prioritaires (MVP)

- [ ] **Open Data Canada** - Datasets de prestations (GRATUIT)
- [ ] **Données Québec** - Programmes provinciaux (GRATUIT)
- [ ] **Statistique Canada** - Données démographiques (GRATUIT)
- [ ] **CanLII** - Textes législatifs (GRATUIT avec API key)
- [ ] **Catalogue de formulaires Service Canada** - PDFs officiels (GRATUIT)

### APIs Secondaires (Phase 2)

- [ ] **Ontario Open Data** - Programmes Ontario (GRATUIT)
- [ ] **BC Data Catalogue** - Programmes Colombie-Britannique (GRATUIT)
- [ ] **Portail géospatial** - Localisation services (GRATUIT)

### APIs Nécessitant Autorisation (Phase 3+)

- [ ] **ARC Web Services** - Données fiscales personnelles (AUTORISÉ)
- [ ] **IRCC Services** - Statut immigration (AUTORISÉ)
- [ ] **Service Canada API** - Vérification temps réel (AUTORISÉ)

---

## 🔐 GESTION DES CLÉS API

**Fichier `.env`** :
```bash
# APIs Publiques
CKAN_CANADA_URL=https://open.canada.ca/data/api/3
CKAN_QUEBEC_URL=https://www.donneesquebec.ca/api/3
STATCAN_API_URL=https://www150.statcan.gc.ca/t1/wds/rest

# APIs avec authentification
CANLII_API_KEY=your_canlii_api_key_here

# APIs futures (nécessitent accréditation)
# ARC_CLIENT_ID=
# ARC_CLIENT_SECRET=
# SERVICE_CANADA_API_KEY=
```

---

## 📊 DATASETS SPÉCIFIQUES RECOMMANDÉS

### Open Data Canada - Datasets Prioritaires

1. **Allocation canadienne pour enfants (ACE)**
   - ID: `af50a939-70c4-4f7f-99b7-f2fa463e63c7`
   - Format: CSV
   - Contenu: Montants par province, critères de revenu

2. **Assurance-emploi - Statistiques**
   - ID: `48c30936-96f8-4ee9-8a32-5169fdf8e569`
   - Format: CSV
   - Contenu: Taux de prestations, durée maximale

3. **Sécurité de la vieillesse - Montants**
   - ID: Rechercher "Old Age Security amounts"
   - Format: CSV/JSON
   - Contenu: Montants mensuels, seuils de récupération

4. **Régime de pensions du Canada**
   - ID: Rechercher "Canada Pension Plan"
   - Format: CSV
   - Contenu: Montants de rente, critères d'admissibilité

---

## 🚀 PROCHAINES ÉTAPES

### Semaine 1
1. Créer module `data_sources/ckan_client.py`
2. Implémenter connexion Open Data Canada
3. Tester téléchargement de 3 datasets prioritaires

### Semaine 2
4. Créer schéma base de données pour stocker datasets
5. Pipeline automatique de synchronisation quotidienne
6. Interface d'interrogation des données

### Semaine 3
7. Intégration Statistique Canada API
8. Calculs d'admissibilité basés sur seuils StatCan

### Semaine 4
9. Parser de formulaires PDF (pdfplumber)
10. Tests avec 5 formulaires courants

---

## 📚 RESSOURCES ADDITIONNELLES

### Documentation Officielle
- [Guide Open Data Canada](https://open.canada.ca/en/access-our-application-programming-interface-api)
- [CKAN API Documentation](https://docs.ckan.org/en/2.9/api/)
- [Statistique Canada Developers](https://www.statcan.gc.ca/en/developers)
- [CanLII API Docs](https://www.canlii.org/en/tools/api_documentation.html)

### Exemples de Code
- [ckanapi GitHub](https://github.com/ckan/ckanapi)
- [pdfplumber Examples](https://github.com/jsvine/pdfplumber/blob/stable/examples)

### Support Communautaire
- [Open Data Canada Forums](https://open.canada.ca/en/forms/contact-us)
- [Stack Overflow - CKAN tag](https://stackoverflow.com/questions/tagged/ckan)

---

**Document Version** : 1.0  
**Dernière Mise à Jour** : 2026-01-21  
**Auteur** : GitHub Copilot pour Zero Obstacle  
**Statut** : Prêt pour implémentation  

# E-Commerce Analytics & Customer Insights

**Explorative Datenanalyse (EDA) zur Identifikation von Umsatztreibern, B2B-Segmentierung und Optimierungshebeln entlang der Customer Journey.**

>  **Interaktive Ansicht:** Um die interaktiven Plotly-Graphen optimal zu betrachten, öffnen Sie dieses Notebook am besten über den folgenden Link: https://jupyterlite.github.io/demo/lab/index.html?path=02_eda.ipynb
**Interaktives Streamlit Dashboard**: https://e-commerceanalytics-h8b2coxhawpwsf6bq53j7r.streamlit.app/

---

## Zusammenfassung
Dieses Projekt analysiert das Nutzer- und Kaufverhalten eines **fiktiven E-Commerce-Shops** auf Basis von fünf mit einander verbundener Datensätze (Orders, Events, Users, Products, Reviews)

**Die wichtigsten Erkenntnisse:**

1.  **Strukturelles B2B-Potenzial & Klumpenrisiko:** Ca.**35%** des Gesamtumsatzes stammen von wenigen High Value Bestellungen. Diese Kunden kaufen selten, aber haben einen großen AOW *Empfehlung: Einführung eines dedizierten B2B-Partnerprogramms.*
2.  **Unerwartete saisonale Schwäche:**Im Q4 (Nov/Dez) sinkt der Umsatz deutlich – nicht wegen sinkender Warenkörbe, sondern durch geringere Kaufhäufigkeit.
3.  **Nutzen durch Werbung maximieren durch Conversion-basiertes Timing:** Während der höchste Traffic in der Mittagspause und abends stattfindet, liegen die echten Conversion-Peaks (bis zu 8 %) am Freitagmittag und am Wochenende. *Empfehlung: Punktgenaue Aussteuerung der Ad-Budgets auf diese Fenster.*
4.  **geringe Preiselastizität:** Die Korrelation zwischen Preis und Absatz ist nahe zu neutral(-0.06). *Empfehlung: Fokus auf Wertigkeit statt auf aggressive Rabatte.*
5.  **Retention-Herausforderungen:** Ca.**50 %** der Käufer besitzen keinen Account. Die Langzeit-Retention nach 24 Monaten liegt bei nur ca. 6 %. *Empfehlung: Optimierung des Sign-up-Prozesses.*

---

##  Datengrundlage & Methodik

Die Analyse basiert auf einem bereinigten Datensatz mit folgenden Dimensionen:
*   **Orders:** 20.000 Transaktionen
*   **Order_Items:** 43.525 Positionen
*   **Events:** 80.000 User-Interaktionen
*   **Products & Users:** 2.000 Produkte und 10.000 Nutzer-Profile
*   **Quelle:** Die Rohdaten für diese Analyse wurden von https://www.kaggle.com/datasets/abhayayare/e-commerce-dataset bezogen.
*   **Datengenerierung:** Synthetische generierung mit Python (Faker + NumPy + Pandas)
*   **Zeitraum:** Die Daten umfassen den Zeitraum von 2024.01 bis 2025.11

**Angewandte Methoden:**
*   Zeitreihen- & Saisonalitätsanalyse (Durchschnitt vs. Median)
*   Ausreißer-Erkennung (IQR-Methode zur B2B-Identifikation)
*   Kohortenanalyse (Retention Matrix)
*   Conversion Funnel & Heatmap-Analysen

---

##  Projektstruktur
```
├── data/ 
│    ├── raw/                   #Rohe Daten
│    └── processed/             #Aufbereitete Daten(Grundlage der EDA)     
├── notebooks/              
│   ├── 01_data_cleaning.ipynb   #Datenaufbereitung & ETL-Prozess
│   └── 02_eda.ipynb             #Hauptanalyse & Visualisierungen
├── src/                    
│   ├── data_loader.py       #Modularer Code für den Datenimport
│   └── data_prep.py         #Funktionen zur Datenaufbereitung
├── dashboard/
│   ├── powerbi_export       #Wichtigste Tabellen aus der EDA als CSV dateien
│   └── app.py               #Der Dashboard Code
├── README.md                #Projektdokumentation
└── requirements.txt         #Liste der benötigten Python-Pakete
```
---


## Installation

Um das Projekt lokal auszuführen und die interaktiven Graphen zu generieren, wird **Python 3.8+** benötigt.

### 1. Repository klonen
git clone [https://github.com/DEIN_USERNAME/ecommerce-analytics.git]

### 2. Virtuelle Umgebung erstellen
"python -m venv venv"

#### Umgebung aktivieren (Windows)
"venv\Scripts\activate"

#### Umgebung aktivieren (Mac/Linux)
"source venv/bin/activate"

### 3. Abhängigkeiten installieren
"pip install --upgrade pip"
"pip install -r requirements.txt"

### 4. Jupyter Notebook starten
#### Starte die Analyseumgebung mit folgendem Befehl:

"jupyter notebook"

---
## Kontakt


LinkedIn: https://www.linkedin.com/in/krish-arora-7b402729b/


E-Mail: krish.arora@tu-dortmund.de


---
## Über dieses Projekt



Dieses Projekt wurde eigenständig neben dem Studium in der Freizeit entwickelt, um praktische Erfahrungen in den Bereichen Data Analytics, Explorative Datenanalyse (EDA) und datengetriebene Entscheidungsfindung aufzubauen.

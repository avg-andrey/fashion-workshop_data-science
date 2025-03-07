# extract_concepts_nlp.py

"""
Script: extract_concepts_nlp.py

Descrizione:
Questo script estrae parole chiave significative dai dati arricchiti di moda utilizzando il modello NLP spaCy.
L’obiettivo è identificare concetti chiave associati a ogni capo d'abbigliamento, basandosi sulla descrizione della scena,
i materiali, i colori, gli elementi di design e il contesto culturale.

Lo script legge i dati arricchiti da `fashion_data_enriched.json`, applica il Natural Language Processing per estrarre le parole chiave
e salva i dati aggiornati in due formati:
1. **JSON** (`output-data/fashion_data_final.json`) - Per l'analisi avanzata dei dati.
2. **CSV** (`output-data/fashion_data_final.csv`) - Per un’analisi più semplice e diretta.

-------------------------------------------------------
Struttura del file JSON generato:
{
  "image_filename": "nome_file.jpg",
  "scene_description": "Descrizione generale della scena",
  "colors": ["Lista di colori principali"],
  "category": "Categoria del prodotto",
  "materials": ["Lista di materiali utilizzati"],
  "design_elements": ["Lista di elementi di design"],
  "cultural_context": "Analisi storico-culturale e significato del design",
  "keywords": ["Lista di parole chiave estratte"]
}
-------------------------------------------------------

Flusso di esecuzione:
1. **Caricamento del dataset**: Lettura dei dati da `input-data/fashion_data_enriched.json`.
2. **Pre-elaborazione del testo**:
   - Unisce più campi testuali in un’unica stringa per analizzare il contesto completo.
   - Rimuove stop words, articoli e parole di collegamento.
   - Esegue il lemmatization per ridurre le parole alla loro radice.
3. **Estrazione delle parole chiave**:
   - Utilizza spaCy per analizzare la struttura grammaticale del testo.
   - Filtra parole con meno di 3 caratteri e categorie grammaticali irrilevanti (articoli, preposizioni, congiunzioni, ecc.).
   - Rimuove duplicati per mantenere un insieme compatto di concetti chiave.
4. **Salvataggio dei dati**:
   - Il JSON viene aggiornato e salvato in `output-data/fashion_data_final.json`
   - Il CSV viene aggiornato con una colonna aggiuntiva `keywords` per facilitare l’analisi tabellare.

Prerequisiti:
- Il dataset `fashion_data_enriched.json` contenente dati arricchiti con contesto culturale.
- Il modello NLP di spaCy per l'italiano (`it_core_news_sm`) installato.
- Installazione delle librerie richieste (`spacy`, `json`, `csv`, `logging`).

Output:
- `output-data/fashion_data_final.json` (dati con parole chiave estratte)
- `output-data/fashion_data_final.csv` (estrazione tabellare con parole chiave)

Autore: [Inserisci il tuo nome]
Data: [Inserisci la data]
"""


import json
import logging
import csv
from pathlib import Path
import spacy

# Configurazione del logging (impostazione dei log)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Percorsi dei file (path settings)
INPUT_FILE = Path("input-data/fashion_data_enriched.json")
OUTPUT_JSON_FILE = Path("output-data/fashion_data_final.json")
OUTPUT_CSV_FILE = Path("output-data/fashion_data_final.csv")

# Caricamento del modello spaCy in italiano
nlp = spacy.load("it_core_news_sm")

# Parti del discorso da escludere (articoli, interiezioni, congiunzioni, ecc.)
EXCLUDED_POS = {"DET", "INTJ", "CCONJ", "SCONJ", "PART", "AUX", "ADP", "PUNCT", "SYM"}

def extract_keywords(text):
    """
    Estrae le parole chiave dal testo rimuovendo stop words, articoli, parole troppo corte (<3 caratteri) e parti del discorso indesiderate.
    """
    doc = nlp(text.lower())
    keywords = [
        token.lemma_ for token in doc
        if token.is_alpha and not token.is_stop
        and len(token.lemma_) >= 3
        and token.pos_ not in EXCLUDED_POS
    ]
    logging.debug(f"Parole chiave estratte: {keywords}")
    return keywords

def save_to_csv(data, filename):
    """
    Salva i dati finali in formato CSV per un'analisi diretta.
    Le liste (come keywords, colors, materials, design_elements) vengono convertite in stringhe separate da virgola.
    """
    try:
        with open(filename, "w", encoding="utf-8", newline="") as csvfile:
            fieldnames = [
                "image_filename",
                "scene_description",
                "colors",
                "category",
                "materials",
                "design_elements",
                "cultural_context",
                "keywords"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for item in data:
                row = {
                    "image_filename": item.get("image_filename", ""),
                    "scene_description": item.get("scene_description", ""),
                    "colors": ", ".join(item.get("colors", [])) if isinstance(item.get("colors", []), list) else item.get("colors", ""),
                    "category": item.get("category", ""),
                    "materials": ", ".join(item.get("materials", [])) if isinstance(item.get("materials", []), list) else item.get("materials", ""),
                    "design_elements": ", ".join(item.get("design_elements", [])) if isinstance(item.get("design_elements", []), list) else item.get("design_elements", ""),
                    "cultural_context": item.get("cultural_context", ""),
                    "keywords": ", ".join(item.get("keywords", [])) if isinstance(item.get("keywords", []), list) else item.get("keywords", "")
                }
                writer.writerow(row)
                logging.info(f"Dati CSV salvati per l'immagine: {item.get('image_filename', 'N/D')}")
        logging.info(f"Dati finali salvati in CSV in {filename}")
    except Exception as e:
        logging.error(f"Errore durante il salvataggio in CSV: {e}")

def process_fashion_data():
    """
    Processa il file JSON contenente le descrizioni degli abiti e aggiunge il campo 'keywords'.
    
    I dati finali vengono salvati sia in formato JSON che in formato CSV per l'analisi diretta.
    """
    try:
        logging.info(f"Lettura dei dati da {INPUT_FILE}...")
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            fashion_data = json.load(file)
        
        # Elaborazione di ogni elemento per estrarre le parole chiave
        for item in fashion_data:
            logging.info(f"Elaborazione dell'immagine: {item.get('image_filename', 'N/D')}")
            
            # Unisce i campi di testo per l'analisi
            text_data = [
                item.get("scene_description", ""),
                item.get("cultural_context", ""),
                ", ".join(item.get("colors", [])),
                item.get("category", ""),
                ", ".join(item.get("materials", [])),
                ", ".join(item.get("design_elements", []))
            ]
            full_text = " ".join(text_data)
            logging.debug(f"Testo per l'analisi: {full_text}")
            
            # Estrae le parole chiave e le aggiunge all'oggetto
            keywords = extract_keywords(full_text)
            item["keywords"] = list(set(keywords))  # Rimuove eventuali duplicati
            logging.info(f"Keywords aggiunte ({len(item['keywords'])}) per {item.get('image_filename', 'N/D')}")
        
        # Salvataggio dei dati finali in formato JSON
        with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(fashion_data, file, ensure_ascii=False, indent=4)
        logging.info(f"Dati finali salvati in JSON in {OUTPUT_JSON_FILE}")
        
        # Salvataggio dei dati finali in formato CSV per l'analisi diretta
        save_to_csv(fashion_data, OUTPUT_CSV_FILE)
        
    except Exception as e:
        logging.error(f"Errore durante l'elaborazione dei concetti: {e}")

if __name__ == "__main__":
    process_fashion_data()

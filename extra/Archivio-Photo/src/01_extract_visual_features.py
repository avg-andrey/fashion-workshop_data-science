# extract_visual_features.py

"""
Script: extract_visual_features.py

Descrizione:
Questo script estrae le caratteristiche visive delle immagini di moda utilizzando OpenAI GPT-4 Turbo.
Analizza le immagini in una cartella specificata, invia richieste all'API di OpenAI e genera una descrizione strutturata con informazioni su:

- **Descrizione della scena**
- **Colori principali**
- **Categoria del prodotto**
- **Materiali utilizzati**
- **Elementi di design**

Le informazioni estratte vengono salvate in due formati:
1. **JSON** (`output-data/fashion_data.json`) - Per la strutturazione e riutilizzo dei dati.
2. **CSV** (`output-data/fashion_data.csv`) - Per un'analisi tabellare diretta.

-------------------------------------------------------
Struttura del file JSON generato:
{
  "image_filename": "nome_file.jpg",
  "scene_description": "Descrizione generale della scena",
  "colors": ["colore1", "colore2", ...],
  "category": "Categoria identificata",
  "materials": ["materiale1", "materiale2", ...],
  "design_elements": ["elemento1", "elemento2", ...]
}
-------------------------------------------------------

Flusso di esecuzione:
1. **Caricamento della chiave API**: Lettura della chiave da `config/api_key.txt`.
2. **Creazione client OpenAI**: Inizializzazione del client OpenAI per l'invio delle richieste.
3. **Elaborazione immagini**:
   - Ricerca di file immagine in `../image-dataset/women-fashion/`
   - Conversione in Base64 e preparazione della richiesta API.
   - Invio della richiesta e ricezione della risposta in formato JSON.
4. **Salvataggio dei dati**:
   - Il JSON viene salvato in `output-data/fashion_data.json`
   - Il CSV viene aggiornato con le nuove informazioni.

Prerequisiti:
- Una chiave API OpenAI salvata in `config/api_key.txt`
- Un dataset di immagini salvato nella cartella `../image-dataset/women-fashion/`
- Installazione delle librerie richieste (`openai`, `json`, `csv`, `logging`)

Output:
- `output-data/fashion_data.json` (descrizioni dettagliate delle immagini in JSON)
- `output-data/fashion_data.csv` (estrazione tabellare per un'analisi più semplice)

Autore: [Inserisci il tuo nome]
Data: [Inserisci la data]
"""


import json
import os
import logging
import csv
import base64
from pathlib import Path
from openai import OpenAI

# Configurazione del logging (Configurazione dei log)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Percorsi dei file (Path settings)
API_KEY_PATH = Path("config/api_key.txt")
IMAGE_DIR = Path("../image-dataset/women-fashion")  # Cartella contenente le immagini
OUTPUT_DIR = Path("output-data")
OUTPUT_JSON_FILE = OUTPUT_DIR / "fashion_data.json"
OUTPUT_CSV_FILE = OUTPUT_DIR / "fashion_data.csv"


def load_api_key():
    """
    Carica la chiave API dal file specificato.
    """
    try:
        with open(API_KEY_PATH, "r", encoding="utf-8") as f:
            key = f.read().strip()
            logging.debug("Chiave API caricata correttamente.")
            return key
    except Exception as e:
        logging.error(f"Errore nel caricamento della chiave API: {e}")
        raise

def create_openai_client():
    """
    Crea e restituisce un'istanza del client OpenAI utilizzando la chiave API.
    """
    api_key = load_api_key()
    return OpenAI(api_key=api_key)

# Inizializzazione del client OpenAI
client = create_openai_client()

# Creazione della directory di output, se non esiste
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def save_to_json(data, filename):
    """
    Salva gli oggetti JSON in un file, mantenendo un array di oggetti.
    """
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        existing_data.append(data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        logging.info(f"Dati salvati in JSON per l'immagine: {data['image_filename']}")
    except Exception as e:
        logging.error(f"Errore durante il salvataggio in JSON: {e}")


def save_to_csv(data, filename):
    """
    Salva i dati in formato CSV per un'analisi diretta.
    Se il file non esiste, scrive l'header.
    Tutti i campi verranno sempre racchiusi tra virgolette per evitare problemi con caratteri speciali.
    """
    try:
        file_exists = os.path.exists(filename)
        with open(filename, "a", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["image_filename", "scene_description", "colors", "category", "materials", "design_elements"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL)
            # Scrive l'header se il file non esiste
            if not file_exists:
                writer.writeheader()
            # Prepara il dizionario per la riga CSV, gestendo eventuali chiavi mancanti
            row = {
                "image_filename": data.get("image_filename", ""),
                "scene_description": data.get("scene_description", ""),
                "colors": ", ".join(data.get("colors", [])) if isinstance(data.get("colors", []), list) else data.get("colors", ""),
                "category": data.get("category", ""),
                "materials": ", ".join(data.get("materials", [])) if isinstance(data.get("materials", []), list) else data.get("materials", ""),
                "design_elements": ", ".join(data.get("design_elements", [])) if isinstance(data.get("design_elements", []), list) else data.get("design_elements", "")
            }
            writer.writerow(row)
        logging.info(f"Dati salvati in CSV per l'immagine: {data['image_filename']}")
    except Exception as e:
        logging.error(f"Errore durante il salvataggio in CSV: {e}")


def extract_visual_features():
    """
    Elabora tutte le immagini nella cartella IMAGE_DIR, invia le richieste a GPT-4 e salva le descrizioni in formato JSON e CSV.
    """
    logging.debug(f"Verifica del percorso della cartella immagini: {IMAGE_DIR.resolve()}")

    if not IMAGE_DIR.exists():
        logging.error(f"Cartella {IMAGE_DIR} non trovata!")
        return

    # Seleziona solo i file immagine con estensioni valide
    image_files = list(IMAGE_DIR.glob("*"))
    image_files = [f for f in image_files if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]

    logging.debug(f"File trovati nella cartella: {[f.name for f in image_files]}")

    if not image_files:
        logging.info("Nessuna immagine da elaborare.")
        return

    logging.info(f"Trovate {len(image_files)} immagini da elaborare.")

    for image_path in image_files:
        # Legge e codifica l'immagine in base64
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            logging.debug(f"Immagine {image_path.name} codificata correttamente in base64.")
        except Exception as e:
            logging.error(f"Errore durante la codifica dell'immagine {image_path.name}: {e}")
            continue  # Salta il file se si verifica un errore

        # Costruisce il payload per la richiesta
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """
                            Analizza questa immagine di moda e genera una descrizione strutturata in formato JSON con i seguenti campi:
                            {
                              "scene_description": "Descrizione generale della scena.",
                              "colors": ["Lista di colori principali."],
                              "category": "Categoria del prodotto.",
                              "materials": ["Lista di materiali utilizzati."],
                              "design_elements": ["Lista di elementi di design."]
                            }
                            Rispondi solo con un JSON valido senza testo aggiuntivo.
                        """},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "model": "gpt-4-turbo",
            "max_tokens": 500
        }

        try:
            logging.info(f"Invio richiesta per l'immagine: {image_path.name}...")
            response = client.chat.completions.create(**payload)
            logging.info("Risposta ricevuta dall'API.")
            try:
                json_response = response.choices[0].message.content
                parsed_data = json.loads(json_response)
                parsed_data["image_filename"] = image_path.name  # Aggiunge il nome del file al JSON
                # Salva i dati in formato JSON
                save_to_json(parsed_data, OUTPUT_JSON_FILE)
                # Salva i dati in formato CSV per l'analisi diretta
                save_to_csv(parsed_data, OUTPUT_CSV_FILE)
            except json.JSONDecodeError:
                logging.error(f"Errore nel parsing del JSON: {json_response}")
        except Exception as e:
            logging.error(f"Errore durante l'analisi dell'immagine {image_path.name}: {e}")

if __name__ == "__main__":
    extract_visual_features()

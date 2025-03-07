# gen_cultural_context.py

"""
Script: gen_cultural_context.py

Descrizione:
Questo script arricchisce i dati di moda estratti da immagini aggiungendo un contesto culturale, storico e stilistico
utilizzando OpenAI GPT-3.5 Turbo. Per ogni capo d’abbigliamento analizzato, il modello fornisce informazioni sulla sua
origine, ispirazioni e rilevanza nel panorama della moda globale.

Lo script legge i dati di base dal file JSON (`fashion_data.json`), genera il contesto culturale per ogni elemento e
salva il risultato in due formati:
1. **JSON** (`output-data/fashion_data_enriched.json`) - Per la strutturazione avanzata dei dati.
2. **CSV** (`output-data/fashion_data_enriched.csv`) - Per un’analisi più semplice e diretta.

-------------------------------------------------------
Struttura del file JSON generato:
{
  "image_filename": "nome_file.jpg",
  "scene_description": "Descrizione generale della scena",
  "colors": ["colore1", "colore2", ...],
  "category": "Categoria identificata",
  "materials": ["materiale1", "materiale2", ...],
  "design_elements": ["elemento1", "elemento2", ...],
  "cultural_context": "Analisi storico-culturale e significato del design."
}
-------------------------------------------------------

Flusso di esecuzione:
1. **Caricamento della chiave API**: Lettura della chiave da `config/api_key.txt`.
2. **Creazione client OpenAI**: Inizializzazione del client OpenAI per l’invio delle richieste.
3. **Lettura del dataset**: Caricamento dei dati da `input-data/fashion_data.json`.
4. **Generazione del contesto culturale**:
   - Per ogni capo, viene analizzato il significato culturale, storico o stilistico.
   - Il modello identifica radici etniche, influenze di movimenti di moda o tecniche di design specifiche.
5. **Salvataggio dei dati**:
   - Il JSON viene aggiornato e salvato in `output-data/fashion_data_enriched.json`
   - Il CSV viene aggiornato per consentire un’analisi tabellare.

Prerequisiti:
- Una chiave API OpenAI salvata in `config/api_key.txt`
- Un dataset di immagini processato e salvato in `input-data/fashion_data.json`
- Installazione delle librerie richieste (`openai`, `json`, `csv`, `logging`)

Output:
- `output-data/fashion_data_enriched.json` (descrizioni arricchite con contesto culturale)
- `output-data/fashion_data_enriched.csv` (estrazione tabellare con il nuovo campo `cultural_context`)

Autore: [Inserisci il tuo nome]
Data: [Inserisci la data]
"""

import json
import logging
import csv
from pathlib import Path
from openai import OpenAI

# Configurazione del logging (impostazione dei log)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Percorsi dei file (path settings)
API_KEY_PATH = Path("config/api_key.txt")
INPUT_FILE = Path("input-data/fashion_data.json")
OUTPUT_JSON_FILE = Path("output-data/fashion_data_enriched.json")
OUTPUT_CSV_FILE = Path("output-data/fashion_data_enriched.csv")

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

def generate_cultural_context(item):
    """
    Genera il contesto culturale per un capo d’abbigliamento utilizzando GPT-3.5.
    
    Viene inviato un prompt con la descrizione del capo e viene restituito il contesto culturale.
    """
    prompt = f"""
    Basandoti sulla seguente descrizione di un capo d’abbigliamento, analizza il suo significato culturale, storico o stilistico.
    Indica se ha radici in una tradizione etnica o se il design è ispirato a un movimento di moda specifico.
    Considera il ruolo dei materiali e delle decorazioni nel contesto della moda globale.

    Descrizione del capo:
    {json.dumps(item, ensure_ascii=False, indent=4)}

    Restituisci un JSON con il seguente formato:
    {{
      "cultural_context": "Analisi storico-culturale e significato del design."
    }}
    """
    try:
        logging.info(f"Generazione del contesto culturale per: {item.get('image_filename', 'N/D')}...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        json_response = json.loads(response.choices[0].message.content)
        return json_response.get("cultural_context", "Informazioni non disponibili")
    except Exception as e:
        logging.error(f"Errore nell'analisi culturale di {item.get('image_filename', 'N/D')}: {e}")
        return "Errore nell'analisi"

def save_to_json(data, filename):
    """
    Salva un oggetto JSON in un file mantenendo un array di oggetti.
    Ogni volta il dato viene aggiunto all'array esistente.
    """
    try:
        if filename.exists():
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
        logging.info(f"Dati salvati in JSON per l'immagine: {data.get('image_filename', 'N/D')}")
    except Exception as e:
        logging.error(f"Errore durante il salvataggio in JSON: {e}")

def save_to_csv(data, filename):
    """
    Salva i dati in formato CSV per un'analisi diretta.
    Se il file non esiste, scrive l'header.
    """
    try:
        file_exists = filename.exists()
        with open(filename, "a", encoding="utf-8", newline="") as csvfile:
            fieldnames = [
                "image_filename",
                "scene_description",
                "colors",
                "category",
                "materials",
                "design_elements",
                "cultural_context"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL)
            # Scrive l'header se il file non esiste
            if not file_exists:
                writer.writeheader()
            row = {
                "image_filename": data.get("image_filename", ""),
                "scene_description": data.get("scene_description", ""),
                "colors": ", ".join(data.get("colors", [])) if isinstance(data.get("colors", []), list) else data.get("colors", ""),
                "category": data.get("category", ""),
                "materials": ", ".join(data.get("materials", [])) if isinstance(data.get("materials", []), list) else data.get("materials", ""),
                "design_elements": ", ".join(data.get("design_elements", [])) if isinstance(data.get("design_elements", []), list) else data.get("design_elements", ""),
                "cultural_context": data.get("cultural_context", "")
            }
            writer.writerow(row)
        logging.info(f"Dati CSV salvati per l'immagine: {data.get('image_filename', 'N/D')}")
    except Exception as e:
        logging.error(f"Errore durante il salvataggio in CSV: {e}")

def process_fashion_data():
    """
    Elabora il file JSON contenente le descrizioni degli abiti e aggiunge il contesto culturale.
    
    Per ogni elemento il contesto viene generato e salvato immediatamente sia in formato JSON che CSV.
    """
    try:
        logging.info(f"Lettura dei dati da {INPUT_FILE}...")
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            fashion_data = json.load(file)
        
        # Processa ogni elemento singolarmente, salvando immediatamente il risultato
        for item in fashion_data:
            # Genera e aggiunge il contesto culturale all'oggetto
            item["cultural_context"] = generate_cultural_context(item)
            # Salva il dato arricchito in JSON (append per ogni item)
            save_to_json(item, OUTPUT_JSON_FILE)
            # Salva il dato arricchito in CSV
            save_to_csv(item, OUTPUT_CSV_FILE)
        
    except Exception as e:
        logging.error(f"Errore nell'elaborazione del file: {e}")

# Avvio del processo
if __name__ == "__main__":
    process_fashion_data()

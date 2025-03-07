# build_graph_data.py

"""
Script: build_graph_data.py

Descrizione:
Questo script genera una mappa concettuale basata sulle parole chiave estratte dai dati sulla moda.
Utilizzando un modello di co-occorrenza, costruisce relazioni tra i concetti e genera una rappresentazione strutturata per l'analisi grafica.

Il risultato è un dataset che descrive le parole chiave più rilevanti e le loro connessioni in base alla loro frequenza nei dati.
Il grafo risultante può essere utilizzato per analizzare le connessioni semantiche tra i termini di moda.

-------------------------------------------------------
Struttura dei dati generati:
1. **JSON** (`output-data/graph-data.json`) - Contiene parole chiave e relazioni strutturate come segue:
{
  "keywords": {
    "moda": 90,
    "design": 85,
    "abito": 82,
    ...
  },
  "relations": [
    {"words": ["design", "moda"], "count": 81},
    {"words": ["abito", "moda"], "count": 79},
    {"words": ["abito", "design"], "count": 75},
    ...
  ]
}

2. **CSV**:
   - `output-data/graph_keywords.csv`: Contiene la lista delle parole chiave con la loro frequenza.
   - `output-data/graph_relations.csv`: Contiene le relazioni tra parole chiave con il relativo peso.

-------------------------------------------------------
Flusso di esecuzione:
1. **Caricamento dei dati**: Lettura di `fashion_data_final.json` che contiene parole chiave estratte con NLP.
2. **Analisi delle parole chiave**:
   - Conteggio della frequenza di ogni parola chiave.
   - Applicazione di un filtro per escludere parole con frequenza inferiore alla soglia (`min_keyword_frequency`).
3. **Costruzione delle relazioni**:
   - Creazione delle coppie di parole che co-occorrono nei record.
   - Filtraggio delle connessioni deboli eliminando quelle con peso inferiore a `min_edge_weight`.
   - Opzionale: Limitazione del numero massimo di connessioni per nodo (`max_edges_per_node`).
4. **Salvataggio dei dati**:
   - Esportazione dei dati filtrati in formato JSON e CSV.

-------------------------------------------------------
Parametri configurabili (`config/graph_setup.json`):
- `"min_keyword_frequency"`: Soglia minima di frequenza per includere una parola chiave nel grafo.
- `"min_edge_weight"`: Soglia minima per considerare una connessione tra due concetti.
- `"max_edges_per_node"`: Numero massimo di connessioni per ciascun nodo (opzionale).

Prerequisiti:
- Il dataset `fashion_data_final.json` deve essere generato precedentemente.
- Le librerie richieste (`json`, `csv`, `collections`, `itertools`).

Output:
- `output-data/graph-data.json` (struttura del grafo)
- `output-data/graph_keywords.csv` (frequenza delle parole chiave)
- `output-data/graph_relations.csv` (relazioni tra parole chiave)

Autore: [Inserisci il tuo nome]
Data: [Inserisci la data]
"""


import json
import logging
import csv
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

# Configurazione del logging (impostazione dei log)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Percorsi dei file
INPUT_FILE = Path("input-data/fashion_data_final.json")
OUTPUT_JSON_FILE = Path("output-data/graph-data.json")
OUTPUT_CSV_KEYWORDS = Path("output-data/graph_keywords.csv")
OUTPUT_CSV_RELATIONS = Path("output-data/graph_relations.csv")
SETTINGS_FILE = Path("config/graph_setup.json")

def load_settings(settings_path):
    """Carica le impostazioni dal file JSON."""
    try:
        with open(settings_path, "r", encoding="utf-8") as file:
            settings = json.load(file)
        logging.info(f"Impostazioni caricate da {settings_path}")
        return settings
    except Exception as e:
        logging.error(f"Errore nel caricamento delle impostazioni: {e}")
        return {}

def build_concept_map():
    """
    Costruisce la mappa dei concetti basata sulle parole chiave e le loro relazioni.
    Legge i parametri per la struttura del grafo dalla sezione "graph_structure" nelle impostazioni.
    """
    try:
        settings = load_settings(SETTINGS_FILE)
        # Lettura dei parametri per la struttura del grafo
        graph_structure = settings.get("graph_structure", {})
        min_keyword_frequency = graph_structure.get("min_keyword_frequency", 3)
        min_edge_weight = graph_structure.get("min_edge_weight", 1)
        max_edges_per_node = graph_structure.get("max_edges_per_node", None)  # Se None, non limitiamo

        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            fashion_data = json.load(file)
        logging.info(f"Record elaborati: {len(fashion_data)}")
        
        all_keywords = []  # Tutte le parole chiave dai record
        co_occurrences = Counter()  # Conta le co-occorrenze (coppie uniche)

        # Elaborazione di ogni record
        for idx, item in enumerate(fashion_data):
            keywords = item.get("keywords", [])
            all_keywords.extend(keywords)
            logging.debug(f"[{idx+1}/{len(fashion_data)}] {item.get('image_filename', 'N/A')}: trovate {len(keywords)} parole chiave: {keywords}")

            # Calcola le co-occorrenze (senza duplicati)
            unique_keywords = sorted(set(keywords))
            for word1, word2 in combinations(unique_keywords, 2):
                co_occurrences[(word1, word2)] += 1

        # Frequenza individuale delle parole chiave
        keyword_frequencies = Counter(all_keywords)
        logging.info(f"Totale parole chiave (con ripetizioni): {len(all_keywords)}")
        logging.info(f"Totale parole chiave uniche: {len(keyword_frequencies)}")
        top_keywords = keyword_frequencies.most_common(10)
        logging.info(f"Top-10 parole chiave: {top_keywords}")

        # Filtra le parole chiave in base alla frequenza minima
        filtered_keywords = {
            word: freq for word, freq in keyword_frequencies.items() if freq >= min_keyword_frequency
        }
        logging.info(f"Parole chiave che soddisfano il criterio ({min_keyword_frequency}): {len(filtered_keywords)}")

        # Costruisce la lista iniziale delle relazioni (considera solo parole chiave filtrate)
        initial_relations = [
            {"words": [w1, w2], "count": count}
            for (w1, w2), count in co_occurrences.items()
            if w1 in filtered_keywords and w2 in filtered_keywords
        ]
        logging.info(f"Relazioni iniziali trovate: {len(initial_relations)}")
        
        # Log del peso massimo e minimo delle relazioni prima del filtraggio
        if initial_relations:
            max_relation_weight = max(rel["count"] for rel in initial_relations)
            min_relation_weight = min(rel["count"] for rel in initial_relations)
            logging.info(f"Peso massimo delle relazioni prima del filtraggio: {max_relation_weight}")
            logging.info(f"Peso minimo delle relazioni prima del filtraggio: {min_relation_weight}")
        else:
            logging.warning("Nessuna relazione trovata prima del filtraggio!")

        # Filtra le relazioni in base al peso minimo
        filtered_relations = [
            rel for rel in initial_relations if rel["count"] >= min_edge_weight
        ]
        logging.info(f"Relazioni con peso >= {min_edge_weight}: {len(filtered_relations)}")
        if not filtered_relations:
            logging.warning(f"Tutte le relazioni sono state eliminate! Considera di abbassare min_edge_weight (attualmente {min_edge_weight}).")

        # Limita il numero di relazioni per ciascun nodo, se richiesto
        if max_edges_per_node is not None:
            node_edges = defaultdict(list)
            for rel in filtered_relations:
                w1, w2 = rel["words"]
                node_edges[w1].append((w2, rel["count"]))
                node_edges[w2].append((w1, rel["count"]))
            limited_relations = []
            for node, edges in node_edges.items():
                edges_sorted = sorted(edges, key=lambda x: x[1], reverse=True)[:max_edges_per_node]
                for target, count in edges_sorted:
                    pair = sorted([node, target])
                    if not any(sorted(rel["words"]) == pair for rel in limited_relations):
                        limited_relations.append({"words": pair, "count": count})
            filtered_relations = limited_relations
            logging.info(f"Relazioni limitate a {max_edges_per_node} per nodo: {len(filtered_relations)}")
        
        # Log delle prime 10 relazioni
        top_relations = sorted(filtered_relations, key=lambda x: x["count"], reverse=True)[:10]
        logging.info("Top-10 relazioni:")
        for rel in top_relations:
            logging.info(f"{rel['words'][0]} - {rel['words'][1]}: {rel['count']}")

        # Struttura finale dei dati
        graph_data = {
            "keywords": filtered_keywords,
            "relations": filtered_relations
        }

        with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(graph_data, file, ensure_ascii=False, indent=4)
        logging.info(f"Dati del grafo salvati in {OUTPUT_JSON_FILE}")

        save_graph_to_csv(filtered_keywords, filtered_relations)

    except Exception as e:
        logging.error(f"Errore nella costruzione della mappa dei concetti: {e}")

def save_graph_to_csv(keywords, relations):
    """
    Salva i dati del grafo in due file CSV:
      - Un file per le parole chiave con la frequenza.
      - Un file per le relazioni tra parole chiave.
    Tutti i campi sono racchiusi tra virgolette.
    """
    try:
        with open(OUTPUT_CSV_KEYWORDS, "w", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["word", "frequency"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for word, freq in keywords.items():
                writer.writerow({"word": word, "frequency": freq})
        logging.info(f"Dati delle parole chiave salvati in CSV in {OUTPUT_CSV_KEYWORDS}")

        with open(OUTPUT_CSV_RELATIONS, "w", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["word_pair", "count"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for rel in relations:
                word_pair = ", ".join(rel["words"])
                writer.writerow({"word_pair": word_pair, "count": rel["count"]})
        logging.info(f"Dati delle relazioni salvati in CSV in {OUTPUT_CSV_RELATIONS}")

    except Exception as e:
        logging.error(f"Errore durante il salvataggio in CSV: {e}")

if __name__ == "__main__":
    build_concept_map()

# 📌 Fashion Concept Graph: Analisi Semantica della Moda.

Questo progetto costruisce una mappa concettuale dei termini legati alla moda a partire da un dataset di immagini. Utilizzando NLP, analisi delle immagini e grafi, estraiamo informazioni chiave e creiamo visualizzazioni per analizzare le connessioni tra concetti di moda.

---

## 📂 Struttura del Progetto

```
📦 Workshop_DataScience_AI/extra/Archivio-Photo
├── 📂 docs                           # Documentazione e note di progetto
├── 📂 image-dataset                  # Dataset delle immagini di moda
├── 📂 src                            # Directory principale del codice
│   ├── 00_download_dataset.py         # Scarica il dataset da KaggleHub
│   ├── 01_extract_visual_features.py  # Estrae le caratteristiche visive delle immagini
│   ├── 02_gen_cultural_context.py     # Arricchisce i dati con il contesto culturale
│   ├── 03_extract_concepts_nlp.py     # Estrae parole chiave con NLP
│   ├── 04_build_graph_data.py         # Costruisce la struttura del grafo semantico
│   ├── 05_visualise_graph.py          # Genera visualizzazioni statiche e interattive del grafo
│   ├── 📂 config                      # Configurazione del progetto
│   │   ├── api_key.txt                # Chiave API OpenAI
│   │   ├── graph_setup.json           # Configurazione dei parametri del grafo
│   ├── 📂 input-data                 # Dati elaborati in ogni fase della pipeline
│   │   ├── fashion_data.json          # Dati estratti dalle immagini
│   │   ├── fashion_data_enriched.json  # Dati con contesto culturale
│   │   ├── fashion_data_final.json     # Dati con parole chiave estratte
│   │   ├── graph-data.json            # Struttura finale del grafo
│   │   ├── graph-data_full-graph.json  # Struttura completa del grafo senza filtri
│   ├── 📂 output-data                 # Risultati e visualizzazioni finali
│   │   ├── fashion_data.csv           # Dati estratti in formato tabellare
│   │   ├── fashion_data_enriched.csv  # Dati con contesto culturale (CSV)
│   │   ├── fashion_data_final.csv     # Dati finali con parole chiave estratte (CSV)
│   │   ├── graph-data.json            # Struttura del grafo generata
│   │   ├── graph_keywords.csv         # Lista delle parole chiave e frequenze
│   │   ├── graph_relations.csv        # Relazioni tra parole chiave
│   │   ├── graph-spring_layout_*.png     # Visualizzazione statica (Spring Layout)
│   │   ├── graph-kamada_kawai_layout_*.png  # Visualizzazione statica (Kamada-Kawai Layout)
│   │   ├── graph-circular_layout_*.png  # Visualizzazione statica (Circular Layout)
│   │   ├── interactive_graph_*.html    # Grafico interattivo Pyvis
├── README.md                           # Documentazione del progetto
├── requirements.txt                    # Dipendenze del progetto

```

---

## 🚀 Workflow del Progetto.

1. **Scaricamento del dataset** → `00_download_dataset.py`
2. **Analisi delle immagini con AI** → `01_extract_visual_features.py`
3. **Arricchimento con contesto culturale** → `02_gen_cultural_context.py`
4. **Estrazione di parole chiave con NLP** → `03_extract_concepts_nlp.py`
5. **Creazione della rete concettuale** → `04_build_graph_data.py`
6. **Visualizzazione dei dati** → `05_visualise_graph.py`

---

## 📜 Descrizione degli Script.

### 📥 00_download_dataset.py
Scarica un dataset di immagini di moda da KaggleHub e ne restituisce il percorso locale.

- **Input**: Nome del dataset KaggleHub
- **Output**: Percorso del dataset scaricato
- **Prerequisiti**: API Kaggle configurata

---

### 🎨 01_extract_visual_features.py
Estrae informazioni visive dalle immagini utilizzando GPT-4 Turbo.

- **Input**: Immagini di moda
- **Output**:
  - `fashion_data.json` (dati strutturati in JSON)
  - `fashion_data.csv` (formato tabellare CSV)
- **Informazioni Estratte**:
  - Descrizione della scena
  - Colori principali
  - Categoria del prodotto
  - Materiali utilizzati
  - Elementi di design

---

### 🌍 02_gen_cultural_context.py
Arricchisce i dati estratti con un'analisi del contesto culturale e stilistico.

- **Input**: `fashion_data.json`
- **Output**:
  - `fashion_data_enriched.json`
  - `fashion_data_enriched.csv`
- **Dati aggiunti**:
  - Analisi storico-culturale dell'abito
  - Influenze di moda e tradizioni etniche

---

### 🔠 03_extract_concepts_nlp.py
Utilizza spaCy per estrarre parole chiave significative dai dati.

- **Input**: `fashion_data_enriched.json`
- **Output**:
  - `fashion_data_final.json`
  - `fashion_data_final.csv`
- **Tecniche usate**:
  - Lemmatizzazione
  - Rimozione di stop words e parole di collegamento
  - Filtraggio delle parole chiave più rilevanti

---

### 🕸️ 04_build_graph_data.py
Costruisce la rete concettuale basata sulle parole chiave e le loro relazioni.

- **Input**: `fashion_data_final.json`
- **Output**:
  - `graph-data.json`
  - `graph_keywords.csv`
  - `graph_relations.csv`
- **Parametri configurabili** (`graph_setup.json`):
  - `min_keyword_frequency`: Soglia minima di frequenza per includere una parola chiave
  - `min_edge_weight`: Peso minimo per considerare una relazione
  - `max_edges_per_node`: Numero massimo di connessioni per ciascun nodo

---

### 📊 05_visualise_graph.py
Genera visualizzazioni statiche e interattive del grafo concettuale.

- **Input**: `graph-data.json`
- **Output**:
  - PNG con tre diversi layout (`spring`, `kamada_kawai`, `circular`)
  - HTML con grafico interattivo
- **Tecnologie usate**:
  - `networkx` e `matplotlib` per le visualizzazioni statiche
  - `pyvis` per il grafo interattivo

---

## 🔧 Prerequisiti.

🔹 **Librerie richieste**

```bash
pip install requirements.txt
python -m spacy download it_core_news_sm
```

🔹 **Configurazione API**

- **OpenAI**: Inserire la chiave API in `config/api_key.txt`
- **Kaggle**: Configurare il file `.kaggle/kaggle.json`

---

## 📌 Risultati e Output.

| File generato | Contenuto |
|--------------|----------|
| `fashion_data.json` | Caratteristiche estratte dalle immagini |
| `fashion_data_enriched.json` | Dati arricchiti con contesto culturale |
| `fashion_data_final.json` | Dati finali con parole chiave estratte |
| `graph-data.json` | Rete concettuale delle parole chiave |
| `graph_keywords.csv` | Frequenza delle parole chiave |
| `graph_relations.csv` | Relazioni tra parole chiave |
| `graph-spring_layout.png` | Visualizzazione statica (Spring Layout) |
| `graph-kamada_kawai_layout.png` | Visualizzazione statica (Kamada-Kawai Layout) |
| `graph-circular_layout.png` | Visualizzazione statica (Circular Layout) |
| `interactive_graph.html` | Grafico interattivo esplorabile |

---

## 👨‍💻 Contatti

Per domande o suggerimenti, crea un *issue* in questo repository o contatta **Andrey Golub** [(@aVg)](https://www.linkedin.com/in/andreygolub/).

---

## ⚠️ Disclaimer

Questo materiale è destinato esclusivamente a fini educativi e formativi. Gli esempi di codice e dati forniti sono puramente dimostrativi e non devono essere utilizzati in ambienti di produzione senza le dovute verifiche e personalizzazioni.
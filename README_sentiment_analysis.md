
# Analisi del Sentiment con HuggingFace

## Descrizione del Progetto

Questo script (`3_4_sentiment_analysis_hf.py`) esegue un'analisi del sentiment sui dati dei tweet utilizzando modelli pre-addestrati forniti da HuggingFace. Consente di identificare emozioni nei tweet (es. positive, negative) e registra statistiche sui risultati.

### Caratteristiche principali:
- Supporto per modelli di analisi del sentiment pre-addestrati.
- Elaborazione dei dati JSON contenenti tweet puliti.
- Calcolo delle statistiche delle emozioni (conteggio e percentuali).
- Compatibile con GPU (se disponibile) o CPU.

## Requisiti

- Python 3.7 o superiore
- Moduli Python:
  - `torch`
  - `transformers`
  - `json`
  - `logging`
  - `os`
  - `collections`

## Installazione

1. Installa i moduli richiesti eseguendo:
   ```bash
   pip install torch transformers
   ```
2. Assicurati che i dati di input siano già stati puliti utilizzando uno script come `03_tweets_data_cleaning.py`.

## Utilizzo

### Configurazione dei Percorsi dei File

1. Imposta il percorso del file di input contenente i tweet puliti:
   ```python
   input_file = "./input_data/03_tweets_dati_cleaned.json"
   ```
2. Configura i modelli e i relativi percorsi di output in questo formato:
   ```python
   models = {
       "MilaNLProc/feel-it-italian-sentiment": "./output_data/04_tweets_sentiment_analysis_feel_it.json",
       "neuraly/bert-base-italian-cased-sentiment": "./output_data/04_tweets_sentiment_analysis_bert_italian.json"
   }
   ```

### Esecuzione dello Script

1. Esegui lo script con:
   ```bash
   python 3_4_sentiment_analysis_hf.py
   ```

2. Lo script rileverà automaticamente se una GPU è disponibile e utilizzerà quella per l'elaborazione; in caso contrario, userà la CPU.

### Output

- **File di Output JSON**: Contiene i tweet con il sentiment rilevato, il punteggio associato e la data (se disponibile). Esempio:
  ```json
  [
      {
          "text": "Questo è un esempio di tweet.",
          "sentiment": "positive",
          "score": 0.9876,
          "date": "2025-01-01"
      }
  ]
  ```

- **Statistiche delle Emozioni**: Lo script registra nel log il conteggio e le percentuali delle emozioni rilevate.

### Esempio di Log

Ecco un esempio di log generato durante l'analisi:
```
INFO - Inizio analisi con il modello: MilaNLProc/feel-it-italian-sentiment
INFO - Risultato analisi: sentiment='positive', score=0.9876
INFO - Statistiche delle emozioni rilevate:
  - Positive: 10 tweet (50.00%)
  - Negative: 10 tweet (50.00%)
INFO - Analisi completata con il modello: MilaNLProc/feel-it-italian-sentiment.
```

## Contributi

Se desideri contribuire a questo progetto, apri una pull request o segnala eventuali problemi.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Per maggiori dettagli, consulta il file LICENSE.

---

**Nota**: Assicurati che i dati di input siano ben formattati e che i modelli specificati siano disponibili tramite HuggingFace.

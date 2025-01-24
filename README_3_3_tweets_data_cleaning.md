
# Pulizia dei Dati dei Tweet

## Descrizione del Progetto

Questo script Python (`03_tweets_data_cleaning.py`) è progettato per pre-elaborare e pulire i dati dei tweet, preparandoli per ulteriori analisi. Include funzionalità per rimuovere link, hashtag, menzioni, caratteri speciali e stop-words. Inoltre, rileva automaticamente la lingua del testo per garantire un'elaborazione linguistica appropriata.

### Caratteristiche principali:
- Pulizia del testo (rimozione di link, menzioni, hashtag, ecc.).
- Tokenizzazione e rimozione delle stop-words.
- Rilevamento della lingua del testo.
- Funzionalità di logging per tracciare le operazioni.
- Supporto per stop-words personalizzate.

## Requisiti

- Python 3.7 o superiore
- Moduli Python:
  - `nltk`
  - `langdetect`
  - `json`
  - `re`
  - `logging`
  - `os`
  - `sys`

## Installazione

1. Clona il repository o copia lo script nella tua directory locale.
2. Installa i moduli richiesti eseguendo il comando:
   ```bash
   pip install nltk langdetect
   ```
3. Scarica i dati necessari per NLTK eseguendo:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

## Utilizzo

### Esecuzione dello script

1. Configura i percorsi dei file JSON di input e output nelle seguenti variabili:
   ```python
   input_file = "./input_data/02_tweets_dati_sintetici.json"
   output_file = "./output_data/03_tweets_dati_cleaned.json"
   ```
2. Aggiungi stop-words personalizzate (opzionale):
   ```python
   custom_words = ["mybrandname", "altrotermine"]
   ```
3. Esegui lo script con il comando:
   ```bash
   python 03_tweets_data_cleaning.py
   ```

### File di Log

Tutte le operazioni verranno tracciate in un file di log denominato `03_data_cleaning.log`, che può essere trovato nella stessa directory dello script.

## Struttura dei File

- **Input JSON**: Deve contenere i dati dei tweet in un formato simile al seguente:
  ```json
  [
      {"text": "Esempio di tweet #hashtag", "date": "2025-01-01"},
      {"text": "Altro esempio di tweet @user", "date": "2025-01-02"}
  ]
  ```
- **Output JSON**: Conterrà i tweet puliti:
  ```json
  [
      {"text": "esempio di tweet hashtag", "date": "2025-01-01"},
      {"text": "altro esempio di tweet", "date": "2025-01-02"}
  ]
  ```
---

## Contatti

Per domande o suggerimenti, crea un *issue* in questo repository o contatta Andrey Golub ([@aVg](https://www.linkedin.com/in/andreygolub/)).

---

## Disclaimer

Questo materiale è destinato esclusivamente a fini educativi e formativi. Gli esempi di codice e dati forniti sono puramente dimostrativi e non devono essere utilizzati in ambienti di produzione senza le dovute verifiche e personalizzazioni.

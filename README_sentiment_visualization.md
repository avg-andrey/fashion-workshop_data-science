
# Visualizzazione dei Risultati della Sentiment Analysis

## Descrizione del Progetto

Questo script (`3_5_sentiment_analysis_visualization.py`) permette di analizzare e visualizzare graficamente i risultati della sentiment analysis eseguita su dati dei tweet. Genera grafici dettagliati e tabelle riassuntive per esplorare i sentimenti identificati nei dati.

### Caratteristiche principali:
- **Grafici di distribuzione**: sentimenti, tendenze temporali, parole più frequenti, ecc.
- **Word Cloud**: rappresentazione visiva delle parole più comuni per ciascun sentimento.
- **Analisi TF-IDF**: identifica le parole più impattanti.
- **Supporto per dati geografici** (se disponibili).
- **Esportazione tabelle riassuntive** in formato CSV.

## Requisiti

- Python 3.7 o superiore
- Moduli Python:
  - `json`
  - `logging`
  - `os`
  - `sys`
  - `argparse`
  - `datetime`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `wordcloud`
  - `sklearn`

## Installazione

1. Installa i moduli richiesti:
   ```bash
   pip install pandas matplotlib seaborn wordcloud scikit-learn
   ```

2. Assicurati che i dati di input provengano da uno script di sentiment analysis, come `3_4_sentiment_analysis_hf.py`.

## Utilizzo

### Configurazione e Esecuzione

1. Assicurati che il file JSON di input contenga i dati della sentiment analysis in questo formato:
   ```json
   [
       {"text": "Esempio di tweet", "sentiment": "positive", "score": 0.95, "date": "2025-01-01"},
       {"text": "Altro tweet", "sentiment": "negative", "score": 0.87, "date": "2025-01-02"}
   ]
   ```

2. Esegui lo script specificando il percorso del file JSON di input:
   ```bash
   python 3_5_sentiment_analysis_visualization.py <percorso_del_file_input>
   ```

3. I risultati saranno salvati in una cartella temporanea all'interno di `./visualizations`.

### Output Generato

Lo script produce i seguenti file nella cartella di output:
- **Grafici**:
  - Distribuzione dei sentimenti (`sentiment_distribution_<model_name>.png`)
  - Tendenze temporali (`temporal_distribution_<model_name>.png`)
  - Word Cloud (`wordcloud_<sentiment>_<model_name>.png`)
  - Probabilità di sentiment (`sentiment_probabilities_<model_name>.png`)
  - Distribuzione geografica (`geographical_distribution_<model_name>.png`)
  - Top-10 parole più frequenti (`top10_words_<model_name>.png`)
  - Parole più impattanti (`most_impactful_words_<sentiment>_<model_name>.png`)
  - Tendenze dei sentimenti (`sentiment_trend_analysis_<model_name>.png`)
  
- **Tabelle**:
  - Tabelle riassuntive dei sentimenti in formato CSV (`sentiment_summary_<model_name>.csv`).

### Esempio di Visualizzazione

Ecco alcune delle visualizzazioni generate dallo script:
1. **Distribuzione dei Sentimenti**: grafico a barre che mostra il conteggio per ciascun sentimento.
2. **Word Cloud**: rappresentazione visiva delle parole più comuni.
3. **Tendenze Temporali**: grafico a linee che mostra l'andamento dei sentimenti nel tempo.

## Contributi

Se desideri contribuire a questo progetto, apri una pull request o segnala eventuali problemi.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Per maggiori dettagli, consulta il file LICENSE.

---

**Nota**: Assicurati che i dati JSON di input siano ben formattati e che il file di output sia accessibile.

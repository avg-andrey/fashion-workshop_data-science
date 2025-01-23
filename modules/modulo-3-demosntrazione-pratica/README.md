# Modulo 3: Dimostrazione Pratica del Caso d'Uso Selezionato

## Introduzione

Benvenuti al **Modulo 3: Dimostrazione Pratica del Caso d'Uso Selezionato**. In questo modulo, metteremo in pratica quanto appreso nei moduli precedenti attraverso un caso d'uso concreto: l'analisi dei sentimenti degli utenti sui social media relativi a un brand specifico. Questo esercizio vi aiuterà a comprendere come utilizzare i dati di sentiment analysis per migliorare le strategie di marketing e gestire la reputazione online.

## Struttura del Workshop

Il workshop è suddiviso in sei parti principali:

1. [Home](../../README.md)
2. [Modulo 1: Introduzione](../modulo-1-introduzione/README.md)
   - [1.2. L'importanza di Big Data e AI Analytics nella moda](../modulo-1-introduzione/README.md#12-limportanza-di-big-data-e-ai-analytics-nella-moda)
3. [Modulo 2: I Use-Case principali nel FashionTech](../modulo-2-use-case-principali/README.md)
   - [2.2. Macro-Use-Case in Fashion Tech](../modulo-2-use-case-principali/README.md#22-macro-use-case-in-fashion-tech)
   - [2.3. Ruoli di Big Data e Modelli di Machine Learning](../modulo-2-use-case-principali/README.md#23-ruoli-di-big-data-e-modelli-di-machine-learning)
4. [Modulo 3: Dimostrazione Pratica](../modulo-3-demosntrazione-pratica/README.md)
5. [Modulo 4: Follow-up per Scenario Realizzato](../modulo-4-follow-up/README.md)
6. [Modulo 5: Conclusione e Discussione](../modulo-5-conclusione-discussione/README.md)
7. [Glossario](../glossario/README.md)

---


## 3.1. Descrizione dell’Obiettivo

- **Obiettivo**: Analizzare i sentimenti degli utenti sui social media relativi a un brand specifico.
- **Valore**: Comprendere l’opinione pubblica per migliorare la strategia di marketing e gestire la reputazione online.

## 3.2. Raccolta dei Dati (Esempio con Twitter API)

### Descrizione

In questa fase, dimostreremo come raccogliere dati dai social media utilizzando l'API di Twitter con la libreria `tweepy`. Tuttavia, per semplificare la dimostrazione e risparmiare tempo, utilizzeremo un file JSON precompilato con dati sintetici contenenti tweet simulati relativi al brand.

### Strumenti

- **Python**: Un linguaggio di programmazione versatile utilizzato per l'analisi dei dati.
- **Libreria tweepy**: Una libreria Python per interagire con l'API di Twitter.
- **File JSON**: `tweets_data.json` contenente tweet grezzi pronti per la fase di pre-elaborazione.

### Procedura

1. **Configurazione dell'API di Twitter**:
   - Registrate un'app su [Twitter Developer](https://developer.twitter.com/) per ottenere le chiavi API.
   - Configurate `tweepy` con le vostre chiavi API.

2. **Raccolta dei Dati**:
   - Utilizzate uno script Python per raccogliere tweet relativi al brand.
   - Salvate i tweet in un file JSON per facilitarne l'analisi.

3. **Ottimizzazione**:
   - Per questa dimostrazione, utilizzeremo un file JSON precompilato con dati sintetici per evitare complicazioni tecniche.

### Output

- **File JSON**: `tweets_data.json` contenente tweet grezzi, pronto per la fase di pre-elaborazione.

## 3.3. Pre-elaborazione dei Dati

### Descrizione

La pre-elaborazione dei dati è fondamentale per garantire che i dati siano puliti e strutturati per l'analisi. In questa fase, procederemo con:

- **Rimozione di link, hashtag, emoji e simboli speciali**: Pulire il testo dai caratteri non necessari.
- **Tokenizzazione**: Suddividere il testo in parole o frasi significative.
- **Rimozione delle stop word**: Eliminare parole comuni che non aggiungono valore all'analisi.

### Strumenti

- **Python**: Utilizzeremo Python per eseguire la pre-elaborazione.
- **Librerie**:
  - `pandas`: Per la manipolazione dei dati.
  - `re`: Per le operazioni di espressioni regolari.
  - `nltk`: Per il trattamento del linguaggio naturale.

### Procedura

1. **Caricamento dei Dati**:
   - Importate il file `tweets_data.json` utilizzando `pandas`.

2. **Pulizia del Testo**:
   - Utilizzate `re` per rimuovere link, hashtag, emoji e simboli speciali.

3. **Tokenizzazione e Rimozione delle Stop Word**:
   - Suddividete il testo in token (parole) e rimuovete le stop word utilizzando `nltk`.

### Output

- **File Pulito**: Testo strutturato e pronto per l’analisi.

## 3.4. Analisi del Sentiment: via ChatGPT

In questa sezione, esploreremo diversi metodi per eseguire l'analisi del sentiment utilizzando ChatGPT e modelli pre-addestrati di Hugging Face.

### 3.4.1. Utilizzo Diretto di ChatGPT (Senza API)

#### Descrizione

Questo metodo consiste nell'inserire manualmente i testi pre-elaborati nella console di ChatGPT per ottenere una classificazione dei sentimenti.

#### Strumenti

- **Console ChatGPT**: Interfaccia web di ChatGPT.

#### Procedura

1. **Preparazione dei Testi**:
   - Copiate i testi pre-elaborati dal file `03_tweets_dati_cleaned.json`.

2. **Analisi Manuale**:
   - Incollate uno o più testi nella console di ChatGPT.
   - Utilizzate un prompt specifico per richiedere l'analisi del sentiment (positivo, negativo, neutro).

3. **Annotazione dei Risultati**:
   - Annotate o salvate manualmente le classificazioni ottenute.

#### Output

- **Classificazione Manuale**: Sentimenti classificati per ciascun testo.

### 3.4.2.a. Analisi tramite API di ChatGPT con Interfaccia WebUI

#### Descrizione

Utilizzare l'interfaccia WebUI di ChatGPT per inviare dati e ricevere risposte formattate.

#### Procedura

1. **Preparazione dei Dati**:
   - Utilizzate il file `02_tweets_dati_sintetici.json` con i testi pre-elaborati.
   - Selezionate alcuni tweet da analizzare.

2. **Invio Dati tramite WebUI**:
   - Aprite l’interfaccia "OpenAI_WebUI".
   - Inserite manualmente il prompt verificato nella console.

3. **Ricezione e Annotazione dei Risultati**:
   - Copiate i risultati generati (JSON).
   - Salvate manualmente i risultati in un file.

#### Output Atteso

- **File JSON**: Contenente i campi `text`, `sentiment`, `explanation`, `date`.

### 3.4.2.b. Analisi tramite API di ChatGPT da Riga di Comando

#### Descrizione

Automatizzare l’analisi inviando i testi all’API di ChatGPT tramite uno script Python eseguito da riga di comando.

#### Procedura

1. **Preparazione del File di Richiesta**:
   - Create un file di testo (es. `3_4_GPT_request_sentiment_analysis_console.txt`).
   - Inserite nel file:
     - Il prompt standard per l’analisi del sentimento.
     - I dati da analizzare, copiati dal file `03_tweets_dati_cleaned.json`.

2. **Esecuzione dello Script**:
   - Aprite il terminale e navigate nella directory contenente lo script.
   - Lanciate lo script con il comando:
     ```bash
     python cli_app.py --input_file "3_4_GPT_request_sentiment_analysis_console.txt" --output_file "04_tweets_sentiment_analysis.txt"
     ```

3. **Risultato Atteso**:
   - **File di Output**: `04_tweets_sentiment_analysis.txt` contenente:
     - La risposta completa restituita dall’API.
     - Classificazione dei sentimenti per ciascun testo.
     - Spiegazioni per ogni classificazione.

#### Nota

1. Il contenuto del file di output dipenderà dalla precisione del prompt inserito. Se il prompt richiede un formato JSON, il risultato sarà strutturato.
2. Per ulteriori analisi o visualizzazioni, potrebbe essere necessario elaborare il file di output con uno script aggiuntivo per trasformarlo in un formato strutturato (es. JSON o CSV).

### 3.4.3. Utilizzo dei Modelli Pre-addestrati (Hugging Face)

#### Descrizione

Eseguire l'analisi dei sentimenti utilizzando un modello pre-addestrato della libreria `transformers` di Hugging Face. Questo approccio consente di automatizzare completamente il processo di classificazione, garantendo l'accuratezza per testi in lingua italiana.

#### Strumenti

- **Python**: Per eseguire lo script.
- **Libreria transformers di Hugging Face**: Per caricare e utilizzare modelli pre-addestrati.
- **Dataset pre-elaborato**: `03_tweets_dati_cleaned.json`, contenente i testi già puliti e strutturati.
- **Modelli pre-addestrati ottimizzati per l'italiano**:
  - `MilaNLProc/feel-it-italian-sentiment`
  - `neuraly/bert-base-italian-cased-sentiment`

#### Procedura

1. **Preparazione del Dataset**:
   - Utilizzate il file `03_tweets_dati_cleaned.json`, contenente i testi già puliti e strutturati.

2. **Esecuzione dello Script**:
   - Lanciate lo script Python preparato per l’analisi dei sentimenti:
     ```bash
     python sentiment_analysis_hf.py
     ```

3. **Risultati**:
   - I risultati saranno salvati in due file JSON:
     - `04_tweets_sentiment_analysis_feel_it.json`: Risultati ottenuti con il modello `MilaNLProc/feel-it-italian-sentiment`.
     - `04_tweets_sentiment_analysis_bert_italian.json`: Risultati ottenuti con il modello `neuraly/bert-base-italian-cased-sentiment`.

#### Nota

1. Lo script utilizza modelli ottimizzati per l'analisi del sentiment in italiano.
2. Prima di eseguire lo script, verificare che:
   - Tutte le dipendenze (come `transformers` e `torch`) siano installate.
   - La versione della libreria `transformers` sia compatibile con i modelli selezionati.
3. La selezione del dispositivo (GPU o CPU) avviene automaticamente. Se disponibile, la GPU migliorerà significativamente i tempi di esecuzione.

## 3.5. Analisi dei Risultati e Visualizzazioni Grafiche

### Descrizione

Questo passaggio si concentra sull'analisi dei dati elaborati dai modelli di sentiment analysis e sulla loro rappresentazione visiva. L'obiettivo è interpretare i risultati in modo chiaro e intuitivo, evidenziando i principali trend e distribuzioni emersi dall'analisi.

### Strumenti

- **Python**: Per l’elaborazione dei dati e la creazione delle visualizzazioni.
- **Librerie principali**:
  - `pandas`: Per manipolare i dati.
  - `matplotlib` e `seaborn`: Per creare grafici.
  - `wordcloud`: Per generare le word cloud.
  - `json`: Per leggere i file di input.

### Input Atteso

- **File JSON**: Contenente i risultati dell'analisi del sentiment generata da uno specifico modello.
  - **Esempio**: `./output_data/04_tweets_sentiment_analysis_bert_italian.json`

### Output Generato

- **Cartella di Visualizzazione**: Tutti i grafici saranno salvati in una sottocartella specifica, ad esempio: `./visualizations/YYYYMMDD_HHMMSS/`
- **Grafici Principali**:
  1. **Distribuzione dei sentimenti**: `sentiment_distribution.png`
     - **Descrizione**: Mostra la distribuzione totale dei sentimenti (positivo, negativo, neutro) basandosi sul dataset.
     - **Utilità**: Fornisce un’idea chiara della prevalenza di ciascun tipo di sentimento.
  
  2. **Distribuzione temporale**: `temporal_distribution.png`
     - **Descrizione**: Analizza l’evoluzione dei sentimenti nel tempo.
     - **Utilità**: Identifica pattern o anomalie temporali che potrebbero essere correlate a eventi specifici.
  
  3. **Word cloud per sentimenti**:
     - `wordcloud_positive.png`
     - `wordcloud_negative.png`
     - `wordcloud_neutral.png`
     - **Descrizione**: Evidenzia le parole più frequenti associate a ciascun tipo di sentimento.
     - **Utilità**: Fornisce insight sulle parole chiave per ogni emozione.
  
  4. **Distribuzione delle probabilità di sentimento**: `sentiment_probabilities.png`
     - **Descrizione**: Mostra la distribuzione dei punteggi di confidenza dei modelli per ciascun sentimento.
     - **Utilità**: Valuta quanto i modelli siano sicuri delle loro classificazioni.
  
  5. **Parole più comuni (Top-10)**: `top10_words_bert_italian.png`
     - **Descrizione**: Mostra le 10 parole più frequenti nel dataset, associate ai sentimenti.
     - **Utilità**: Identifica temi principali o termini ricorrenti nei dati.
  
  6. **Parole più impattanti per ciascun sentimento**:
     - `most_impactful_words_positive_bert_italian.png`
     - `most_impactful_words_negative_bert_italian.png`
     - `most_impactful_words_neutral_bert_italian.png`
     - **Descrizione**: Visualizza le parole con il punteggio di rilevanza più alto per ogni tipo di sentimento.
     - **Utilità**: Evidenzia quali parole contribuiscono maggiormente alla classificazione dei sentimenti, basandosi sui punteggi del modello.
  
  7. **Analisi delle tendenze dei sentimenti**: `sentiment_trend_analysis_bert_italian.png`
     - **Descrizione**: Esplora tendenze nei sentimenti (positivo, negativo, neutro) con un focus sull'andamento temporale.
     - **Utilità**: Aiuta a identificare momenti critici o cambiamenti significativi nei sentimenti degli utenti.
  
  8. **Tabella riassuntiva dei sentimenti**: `sentiment_summary_bert_italian.csv`
     - **Descrizione**: Fornisce un riepilogo quantitativo dei sentimenti (conteggio per positivo, negativo, neutro).
     - **Utilità**: Permette di esportare i risultati per un'ulteriore analisi o reportistica.

### Procedura

1. **Preparazione dell'Ambiente**:
   - Assicurarsi che il file JSON di input sia disponibile nella cartella `./output_data`.
   - Verificare che le librerie richieste siano installate.

2. **Esecuzione dello Script**:
   - Avviare lo script con il comando:
     ```bash
     python 3_5_sentiment_analysis_visualization.py "./output_data/04_tweets_sentiment_analysis_bert_italian.json"
     ```

3. **Output Generato**:
   - I grafici saranno salvati in una nuova cartella all’interno di `./visualizations/` con timestamp (ad esempio, `20250122_234230/`).

4. **Interpretazione dei Risultati**:
   - Esaminare i grafici e i dati esportati per comprendere le distribuzioni e i trend.
   - Utilizzare i risultati per presentazioni, report o strategie di miglioramento.

## Conclusione

In questo modulo abbiamo visto come raccogliere, pre-elaborare e analizzare i sentimenti degli utenti sui social media utilizzando diversi strumenti e metodologie. L'obiettivo è utilizzare queste informazioni per prendere decisioni informate che migliorino le strategie di marketing e la gestione della reputazione del brand nel settore della moda.

Ricordate che la collaborazione con i data scientist è fondamentale per tradurre le vostre intuizioni di marketing in requisiti tecnici che possono essere implementati efficacemente. Continuate a esplorare e sperimentare con i dati per scoprire nuove opportunità di crescita e miglioramento.

---

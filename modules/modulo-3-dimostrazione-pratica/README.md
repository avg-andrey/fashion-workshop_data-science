# Modulo 3: Dimostrazione Pratica del Caso d'Uso Selezionato

## Introduzione

**Modulo 3: Dimostrazione Pratica del Caso d'Uso Selezionato**. In questo modulo, metteremo in pratica quanto appreso nei moduli precedenti attraverso un caso d'uso concreto: l'analisi dei sentimenti degli utenti sui social media relativi a un brand specifico. Questo esercizio vi aiuterà a comprendere come utilizzare i dati di sentiment analysis per migliorare le strategie di marketing e gestire la reputazione online.


---

## 3.1. Scenario e Obiettivo

**Scenario**: Immaginiamo di lavorare per un brand di moda fittizio, “FashionX”. Negli ultimi mesi, alcuni manager hanno notato un calo di vendite e temono che ci siano opinioni negative in rete. Vogliono capire **cosa** i clienti stiano dicendo su Twitter e **come** questi commenti influiscano sulla reputazione del marchio.

**Obiettivo**: Raccogliere una serie di tweet pubblici che menzionano “FashionX”, pulirli e analizzarli per determinare se il sentiment prevalente sia positivo, negativo o neutro. Quindi, interpretare i risultati per prendere decisioni di marketing.

---

## 3.2. Ruolo dell’Analista: Domande di Business

Prima di passare alla parte tecnica, **l’analista** discute con il team marketing e customer care per definire:

1. **Periodo di analisi**: “Quali tweet consideriamo (ultime 2 settimane, ultimo mese, ecc.)?”
2. **Lingua/fonte**: “Dobbiamo filtrare solo tweet in italiano? O includiamo anche inglese, spagnolo?”
3. **KPI**: “Cosa misuriamo? Percentuale di tweet negativi? Principali parole chiave utilizzate?”
4. **Obiettivo finale**: “Vogliamo usare questi dati per ricalibrare la strategia social? O per informare il team prodotto su eventuali difetti segnalati dai clienti?”

> In questa fase, **l’analista** traduce le richieste di business in **specifiche** per il team di data science (es. “raccolta di tweet contenenti #FashionX negli ultimi 30 giorni, in italiano, con analisi di sentiment e parole più menzionate”).

---

## 3.3. Flusso di Lavoro

## 3.4. Raccolta dei Dati (Esempio con Twitter API)

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

## 3.5. Pre-elaborazione dei Dati

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

## 3.6. Analisi del Sentiment: via ChatGPT

In questa sezione, esploreremo diversi metodi per eseguire l'analisi del sentiment utilizzando ChatGPT e modelli pre-addestrati di Hugging Face.

### 3.6.1. Utilizzo Diretto di ChatGPT (Senza API)

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

### 3.6.2.a. Analisi tramite API di ChatGPT con Interfaccia WebUI

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

### 3.6.2.b. Analisi tramite API di ChatGPT da Riga di Comando

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

### 3.6.3. Utilizzo dei Modelli Pre-addestrati (Hugging Face)

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

## 3.7. Analisi dei Risultati e Visualizzazioni Grafiche

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

## Struttura del Workshop

Il workshop è suddiviso in sette parti principali:

1. [Home](/README.md)

2. [Modulo 1: Introduzione](/modules/modulo-1-introduzione/README.md)
   - [1.1. Obiettivi del Workshop](/modules/modulo-1-introduzione/README.md#11-obiettivi-del-workshop)
   - [1.2. L'importanza di Big Data e AI Analytics nella moda](/modules/modulo-1-introduzione/README.md#12-limportanza-di-big-data-e-ai-analytics-nella-moda)
   - [1.3. Sfide Reali e Ruolo dell’Analista](/modules/modulo-1-introduzione/README.md#13-sfide-reali-e-ruolo-dellanalista)

3. [Modulo 2: I Use-Case principali nel FashionTech](/modules/modulo-2-use-case-principali/README.md)
   - [2.1. Spiegazione delle Tecnologie (per i più curiosi)](/modules/modulo-2-use-case-principali/README.md#21-spiegazione-delle-tecnologie-per-i-piu-curiosi)
   - [2.2. Macro-Use-Case in Fashion Tech](/modules/modulo-2-use-case-principali/README.md#22-macro-use-case-in-fashion-tech)
     - [Use Case 1: Analisi delle Tendenze di Moda](/modules/modulo-2-use-case-principali/README.md#use-case-1-analisi-delle-tendenze-di-moda)
     - [Use Case 2: Gestione della Catena di Approvvigionamento](/modules/modulo-2-use-case-principali/README.md#use-case-2-gestione-della-catena-di-approvvigionamento)
     - [Use Case 3: Personalizzazione delle Offerte](/modules/modulo-2-use-case-principali/README.md#use-case-3-personalizzazione-delle-offerte)
     - [Use Case 4: Sentiment Analysis del Brand](/modules/modulo-2-use-case-principali/README.md#use-case-4-sentiment-analysis-del-brand)
     - [Use Case 5: Previsione delle Vendite](/modules/modulo-2-use-case-principali/README.md#use-case-5-previsione-delle-vendite)
   - [2.3. Ruoli di Big Data e Modelli di Machine Learning](/modules/modulo-2-use-case-principali/README.md#23-ruoli-di-big-data-e-modelli-di-machine-learning)
     - [2.3.1. Big Data: Raccolta, Archiviazione e Pre-Elaborazione dei Dati](/modules/modulo-2-use-case-principali/README.md#231-big-data-raccolta-archiviazione-e-pre-elaborazione-dei-dati)
     - [2.3.2. Modelli di Machine Learning: Estrarre Insight dai Dati](/modules/modulo-2-use-case-principali/README.md#232-modelli-di-machine-learning-estrarre-insight-dai-dati)
     - [2.3.3. Sinergia tra Big Data e Machine Learning](/modules/modulo-2-use-case-principali/README.md#233-sinergia-tra-big-data-e-machine-learning)
     - [2.3.4. Fattori Critici di Successo](/modules/modulo-2-use-case-principali/README.md#234-fattori-critici-di-successo)

4. [Modulo 3: Dimostrazione Pratica del Caso d'Uso Selezionato](/modules/modulo-3-dimostrazione-pratica/README.md)
   - [3.1. Scenario e Obiettivo](/modules/modulo-3-dimostrazione-pratica/README.md#31-scenario-e-obiettivo)
   - [3.2. Ruolo dell’Analista: Domande di Business](/modules/modulo-3-dimostrazione-pratica/README.md#32-ruolo-dellanalista-domande-di-business)
   - [3.3. Flusso di Lavoro](/modules/modulo-3-dimostrazione-pratica/README.md#33-flusso-di-lavoro)
   - [3.4. Raccolta dei Dati (Esempio con Twitter API)](/modules/modulo-3-dimostrazione-pratica/README.md#34-raccolta-dei-dati-esempio-con-twitter-api)
   - [3.5. Pre-elaborazione dei Dati](/modules/modulo-3-dimostrazione-pratica/README.md#35-pre-elaborazione-dei-dati)
   - [3.6. Analisi del Sentiment: via ChatGPT](/modules/modulo-3-dimostrazione-pratica/README.md#36-analisi-del-sentiment-via-chatgpt)
     - [3.6.1. Utilizzo Diretto di ChatGPT (Senza API)](/modules/modulo-3-dimostrazione-pratica/README.md#361-utilizzo-diretto-di-chatgpt-senza-api)
     - [3.6.2.a. Analisi tramite API di ChatGPT con Interfaccia WebUI](/modules/modulo-3-dimostrazione-pratica/README.md#362a-analisi-tramite-api-di-chatgpt-con-interfaccia-webui)
     - [3.6.2.b. Analisi tramite API di ChatGPT da Riga di Comando](/modules/modulo-3-dimostrazione-pratica/README.md#362b-analisi-tramite-api-di-chatgpt-da-riga-di-comando)
     - [3.6.3. Utilizzo dei Modelli Pre-addestrati (Hugging Face)](/modules/modulo-3-dimostrazione-pratica/README.md#363-utilizzo-dei-modelli-pre-addestrati-hugging-face)
   - [3.7. Analisi dei Risultati e Visualizzazioni Grafiche](/modules/modulo-3-dimostrazione-pratica/README.md#37-analisi-dei-risultati-e-visualizzazioni-grafiche)

5. [Modulo 4: Follow-up per Scenario Realizzato](/modules/modulo-4-follow-up/README.md)
   - [4.1. Come Utilizzare i Dati di Sentiment Analysis nel Fashion Business](/modules/modulo-4-follow-up/README.md#41-come-utilizzare-i-dati-di-sentiment-analysis-nel-fashion-business)
   - [4.2. Real-World Challenges: Cosa può andare storto?](/modules/modulo-4-follow-up/README.md#42-real-world-challenges-cosa-puo-andare-storto)
   - [4.3. Cosa Fare se Non Abbiamo un Data Scientist Interno?](/modules/modulo-4-follow-up/README.md#43-cosa-fare-se-non-abbiamo-un-data-scientist-interno)
   - [4.4. Mini-Esercizio di Riflessione](/modules/modulo-4-follow-up/README.md#44-mini-esercizio-di-riflessione)
   - [4.5. Come Implementare le Strategie](/modules/modulo-4-follow-up/README.md#45-come-implementare-le-strategie)
   - [4.6. Best Practices](/modules/modulo-4-follow-up/README.md#46-best-practices)
   - [4.7. Risorse Utili](/modules/modulo-4-follow-up/README.md#47-risorse-utili)
   - [4.8. Ringraziamenti](/modules/modulo-4-follow-up/README.md#48-ringraziamenti)

6. [Modulo 5: Conclusione e Discussioni](/modules/modulo-5-conclusione-discussione/README.md)
   - [5.1. Riepilogo Finale](/modules/modulo-5-conclusione-discussione/README.md#51-riepilogo-finale)
   - [5.2. Oltre la Sentiment Analysis: Altri Possibili Sviluppi](/modules/modulo-5-conclusione-discussione/README.md#52-oltre-la-sentiment-analysis-altri-possibili-sviluppi)
   - [5.3. Ruolo dell’Analista: Punti di Forza e Criticità](/modules/modulo-5-conclusione-discussione/README.md#53-ruolo-dellanalista-punti-di-forza-e-criticità)
   - [5.4. Mini-Esercizi Non Tecnici](/modules/modulo-5-conclusione-discussione/README.md#54-mini-esercizi-non-tecnici)
   - [5.5. Risorse di Studio Autonomo](/modules/modulo-5-conclusione-discussione/README.md#55-risorse-di-studio-autonomo)
   - [5.6. Consigli per i Prossimi Passi](/modules/modulo-5-conclusione-discussione/README.md#56-consigli-per-i-prossimi-passi)
   - [5.7. Conclusioni](/modules/modulo-5-conclusione-discussione/README.md#57-conclusioni)

7. [Glossario](/modules/glossario/README.md)
   - [Machine Learning vs. Deep Learning vs. Neural Network](/modules/glossario/README.md#machine-learning-vs-deep-learning-vs-neural-network)
   - [Machine Learning Model (Modello di Machine Learning)](/modules/glossario/README.md#machine-learning-model-modello-di-machine-learning)
   - [Training (Addestramento)](/modules/glossario/README.md#training-addestramento)
   - [Inference (Inferenza)](/modules/glossario/README.md#inference-inferenza)
   - [Tecnologie e Strumenti](/modules/glossario/README.md#tecnologie-e-strumenti)
   - [Esempi Pratici](/modules/glossario/README.md#esempi-pratici)
   - [Statistica e Visualizzazione dei Dati](/modules/glossario/README.md#statistica-e-visualizzazione-dei-dati)
   - [Termini Aggiuntivi Utili](/modules/glossario/README.md#termini-aggiuntivi-utili)
   - [GLOSSARIO](/modules/glossario/README.md#glossario)

8. [Modulo Extra 1: Fashion Concept Graph](/modules/modulo-extra-1/README.md)
   - [8.1. Dataset e Contesto](/modules/modulo-extra-1/README.md#81-dataset-e-contesto)
   - [8.2. Due Approcci: Interattivo vs. Automatizzato](/modules/modulo-extra-1/README.md#82-due-approcci-interattivo-vs-automatizzato)
     - [8.2.1. Interattivo (Manuale)](/modules/modulo-extra-1/README.md#821-interattivo-manuale)
     - [8.2.2. Automatizzato (Python + AI/NLP)](/modules/modulo-extra-1/README.md#822-automatizzato-python-ai-nlp)
     - [8.2.3. Caratteristiche Estratte Automaticamente e Limiti](/modules/modulo-extra-1/README.md#823-caratteristiche-estratte-automaticamente-e-limiti)
   - [8.3. Fasi Principali del Progetto](/modules/modulo-extra-1/README.md#83-fasi-principali-del-progetto)
     - [8.3.1. Fase 0: Download e Setup Dataset](/modules/modulo-extra-1/README.md#831-fase-0-download-e-setup-dataset)
     - [8.3.2. Fase 1: Estrazione Tratti Visivi](/modules/modulo-extra-1/README.md#832-fase-1-estrazione-tratti-visivi)
     - [8.3.3. Fase 2: Contestualizzazione Culturale](/modules/modulo-extra-1/README.md#833-fase-2-contestualizzazione-culturale)
     - [8.3.4. Fase 3: Estrazione di Concetti Chiave (NLP)](/modules/modulo-extra-1/README.md#834-fase-3-estrazione-di-concetti-chiave-nlp)
     - [8.3.5. Fase 4: Costruzione del Grafo di Concetti](/modules/modulo-extra-1/README.md#835-fase-4-costruzione-del-grafo-di-concetti)
     - [8.3.6. Fase 5: Visualizzazione del Grafo](/modules/modulo-extra-1/README.md#836-fase-5-visualizzazione-del-grafo)
   - [8.4. Esempio di Utilizzo Manuale vs Automatizzato](/modules/modulo-extra-1/README.md#84-esempio-di-utilizzo-manuale-vs-automatizzato)
   - [8.5. Conclusioni](/modules/modulo-extra-1/README.md#85-conclusioni)
   
---
## Contatti

Per domande o suggerimenti, crea un *issue* in questo repository o contatta Andrey Golub ([@aVg](https://www.linkedin.com/in/andreygolub/)).

---

## Disclaimer

Questo materiale è destinato esclusivamente a fini educativi e formativi. Gli esempi di codice e dati forniti sono puramente dimostrativi e non devono essere utilizzati in ambienti di produzione senza le dovute verifiche e personalizzazioni.
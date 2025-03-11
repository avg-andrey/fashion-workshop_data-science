# Modulo Extra 1: Fashion Concept Graph – Analisi delle Immagini e Creazione di Grafi Semantici.

## Introduzione

**Obiettivo:** Dimostrare un flusso di lavoro completo in ambito Data Science per la moda, dall’estrazione di caratteristiche visive con l’AI alla costruzione di una rete semantica di concetti chiave.

---

## 8.1. Dataset e Contesto

- **Dataset:** Utilizziamo il *Women’s Fashion Image Dataset* di Kaggle (vedi README). Contiene immagini di abbigliamento femminile, con vari stili e colori.
- **Utilità:** Consente di analizzare colore, texture, silhouette, materiali, stili, con l’obiettivo di realizzare raccomandazioni, ricerche per simili o analisi di trend nella moda.

---

## 8.2. Due Approcci: Interattivo vs. Automatizzato

### 8.2.1. Interattivo (Manuale)
- Utile per piccoli dataset o prove rapide.
- **Processo:** L’utente inserisce un testo descrittivo, ChatGPT risponde con JSON, suggerimenti, descrizioni marketing, ecc.
- Richiede intervento umano per ogni immagine o gruppo di immagini.

### 8.2.2. Automatizzato (Python x AI + NLP)
- Gestisce dataset medio-grandi in modo coerente e ripetibile.
- **Pipeline:** Si possono programmare batch di analisi, archiviare i risultati in JSON e CSV.
- **Configurazione:** I parametri sono definiti nel file `graph_setup.json` per personalizzare filtri, layout dei grafi, ecc.

### 8.2.3. Caratteristiche Estratte Automaticamente e Limiti

| **Caratteristiche Estratte Automaticamente (AI + LLM)** | **Descrizione** |
|--------------------------------|----------------------------------------------------------------|
| **Caratteristiche cromatiche** | Palette di colori principali e secondari, bilanciamento cromatico (monocromatico, contrastato, pastello, ecc.) |
| **Composizione dell'immagine** | Tipo di inquadratura (primo piano, mezza figura, figura intera), orientamento (verticale, orizzontale), posizionamento del soggetto (centrato, asimmetrico) |
| **Scenografia e ambiente** | Tipo di sfondo (monocromatico, architettura, texture, natura), presenza di elementi scenografici, illuminazione (morbida, contrastata, silhouette) |
| **Analisi dello stile e delle forme** | Tipo di capo (abito, tailleur, blusa), silhouette (aderente, ampia, strutturata), materiali e texture visibili (trasparenze, pelle, superfici lucide), elementi decorativi (ricami, strass, drappeggi), stile generale (minimalista, architettonico, retrò) |
| **Generazione di descrizioni testuali** | Breve descrizione della scena, descrizione dettagliata degli elementi visivi, generazione automatica di tag basati sull’immagine |

| **Caratteristiche Derivate da AI + LLM (richiedono conoscenza esterna)** | **Descrizione** |
|--------------------------------|----------------------------------------------------------------|
| **Pattern e motivi decorativi** | Identificazione del tipo di motivo (floreale, geometrico, astratto), associazione con periodi storici o movimenti artistici (Art Deco, Barocco) |
| **Caratterizzazione avanzata dei tessuti** | Classificazione approssimativa del materiale (seta, velluto, lino), associazione con categorie note (es. “Chiffon” per un materiale trasparente e leggero) |
| **Tipologie di costruzione sartoriale** | Identificazione dello stile di taglio e lavorazione (es. “taglio a sbieco”, “drappeggio couture”), possibile correlazione con tecniche sartoriali specifiche (plissé Fortuny) |
| **Interpretazione e contesto culturale** | Possibile ispirazione stilistica basata su elementi visivi (es. kimono giapponese, toga romana), connessioni con icone della moda o epoche storiche |
| **Attribuzione stilistica basata su riferimenti noti** | Associazione con tendenze specifiche di designer (es. "architettura tessile" → Ferré, "decostruzione" → Margiela), collegamento con collezioni precedenti dello stesso brand se emergono elementi ricorrenti |

| **Caratteristiche Non Estratte Automaticamente (richiedono fonti esterne)** | **Descrizione** |
|--------------------------------|----------------------------------------------------------------|
| **Dati d’archivio e attribuzioni** | Nome del fotografo, luogo e data dello scatto, diritti di utilizzo dell'immagine |
| **Contesto della collezione e del brand** | Nome e concept della collezione, contesto storico della creazione del capo, fonti d’ispirazione del designer |
| **Materiali e produzione** | Tessuti utilizzati (se non chiaramente visibili), atelier di produzione del capo, fornitori di materiali e tecniche di lavorazione |
| **Collegamenti con l’archivio e documentazione** | Codice dello schizzo originale corrispondente, ubicazione di campioni di tessuto o cartamodelli, pubblicazioni su riviste legate all’immagine |

---

## 8.3. Fasi Principali del Progetto

### **8.3.1. Fase 0: Download e Setup Dataset**
- **Manuale:** Vai su Kaggle, scarica manualmente il dataset e spostalo in `./image-dataset`.
- **Automatizzato:**
  ```bash
  python 00_download_dataset.py
  ```

### **8.3.2. Fase 1: Estrazione Tratti Visivi**
- **Manuale:** Carica un’immagine in ChatGPT.
  - **Prompt:**
    ```
    Descrivi l'immagine caricata in modo strutturato. Il testo deve includere:
    - Descrizione della scena.
    - Colori principali.
    - Categoria del capo.
    - Materiali utilizzati.
    - Elementi di design.
    Rispondi direttamente con il testo, senza analisi, senza spiegazioni aggiuntive e senza codice.
    ```
  - **Risposta Attesa:**
    ```
    Scene Description: Donna con abito Anarkali, sfondo rimosso.
    Colori: Bianco con motivi blu elettrico.
    Materiali: Georgette per la dupatta, satin per la gonna.
    Elementi di Design: Rifiniture in perline, silhouette ampia.
    ```
- **Automatizzato:**
  ```bash
  python 01_extract_visual_features.py
  ```
  - Analizza tutte le immagini in `./image-dataset/`, genera `fashion_data.json` e `fashion_data.csv`.
  - Internamente, lo script invia richieste all’API di OpenAI GPT-4 Turbo per estrarre i campi desiderati.

### **8.3.3. Fase 2: Contestualizzazione Culturale**
- **Manuale:**
  - Prendi il testo generato nella Fase 1.
  - **Prompt:**
    ```
    Analizza il testo e descrivi le radici culturali e storiche dell’abito: se ha un’influenza etnica, se appartiene a un movimento di moda, ecc.
    ```
  - **Risposta Attesa:**
    ```
    Radici culturali e storiche: L'abito Anarkali ha origini nell'epoca Mughal (XVI-XVIII secolo), derivando il suo nome dalla leggendaria cortigiana Anarkali. Tradizionalmente associato alla nobiltà indiana, il suo design enfatizza fluidità e grazia.
    ```
- **Automatizzato:**
  ```bash
  python 02_gen_cultural_context.py
  ```

### **8.3.4. Fase 3: Estrazione di Concetti Chiave (NLP)**
- **Manuale:**
  - **Prompt:**
    ```
    Analizza i seguenti testi e identifica i concetti chiave più rilevanti. Restituisci un elenco di parole chiave separate da virgola, senza stop words e con almeno 3 caratteri.
    ```
  - **Risposta Attesa:**
    ```
    abito, Anarkali, dupatta, donna, selfie, velo, design, tessuto, bianco, blu, cuore, perline, silhouette, Mughal, tradizione, moda
    ```
- **Automatizzato:**
  ```bash
  python 03_extract_concepts_nlp.py
  ```

### **8.3.5. Fase 4: Costruzione del Grafo di Concetti**
- **Automatizzato:**
  ```bash
  python 04_build_graph_data.py
  ```

### **8.3.6. Fase 5: Visualizzazione del Grafo**
- **Automatizzato:**
  ```bash
  python 05_visualise_graph.py
  ```

---

## 8.4. Esempio di Utilizzo: Manuale vs Automatizzato  

### **Scenario:** Analisi di immagini di abiti floreali  

Tutti i materiali, inclusi dataset di immagini e script, si trovano nei seguenti percorsi:

📂 **Archivio delle immagini:**  
Il dataset di immagini per il test si trova nella cartella principale del repository:  
[`fashion-workshop_data-science/extra/Archivio-Photo`](../../extra/Archivio-Photo)  

📄 **Documentazione del modulo:**  
Per una guida dettagliata sul modulo (questa pagina) **"Extra 1: Fashion Concept Graph – Analisi delle Immagini e Creazione di Grafi Semantici"**, consultare il seguente documento:  
[`fashion-workshop_data-science/modules/modulo-extra-1/README.md`](../../modules/modulo-extra-1/README.md)  

📑 **Guida tecnica e istruzioni di implementazione:**  
Per le istruzioni tecniche relative al repository, alla configurazione del codice e all'esecuzione dell'esercizio pratico, fare riferimento a:  
[`fashion-workshop_data-science/extra/Archivio-Photo/README.md`](../../extra/Archivio-Photo/README.md)

#### **Metodo Manuale:**
1. Caricare ogni immagine in ChatGPT.
2. Estrarre JSON con descrizione, colori, materiali, elementi di design.
3. Copiare/incollare i risultati in Excel.
4. Chiedere a ChatGPT il contesto culturale.
5. Estrarre parole chiave e creare un file CSV manualmente.
6. Importare i dati in un software di visualizzazione grafi.

#### **Metodo Automatizzato:**
1. Inserire le immagini in `./image-dataset/`.
2. Eseguire gli script in sequenza:
   ```bash
   python 01_extract_visual_features.py 
   python 02_gen_cultural_context.py 
   python 03_extract_concepts_nlp.py 
   python 04_build_graph_data.py 
   python 05_visualise_graph.py 
   ```
3. Ottenere JSON e CSV finali, PNG/HTML con le reti di concetti.

---

## 8.5. Conclusioni

Questo modulo dimostra come i dati visivi possano essere arricchiti con AI e NLP per costruire mappe semantiche dei concetti di moda. 
- Il **metodo interattivo** è utile per piccole analisi rapide.
- Il **metodo automatizzato** è scalabile e replicabile per dataset più grandi.
- Per dettagli tecnici, consulta il `README.md`.

📌 **Buon apprendimento e buona sperimentazione con la Fashion Concept Graph!**

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
     - [8.2.2. Automatizzato (Python x AI + NLP)](/modules/modulo-extra-1/README.md#822-automatizzato-python-x-ai-nlp)
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
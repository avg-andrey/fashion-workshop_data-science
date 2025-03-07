
# Accesso ai Dati di Twitter con Tweepy

## Descrizione

`02_twitter_access_data.py` è uno demo script Python progettato per raccogliere dati da Twitter utilizzando l'API di Twitter. Lo script autentica l'utente, esegue ricerche basate su query specifiche, raccoglie tweet pertinenti e salva i dati raccolti in un file JSON. Questo strumento è utile per analisi di sentiment, monitoraggio di marchi, ricerca accademica e molto altro.

## Requisiti

- **Python 3.7+**
- **Librerie Python:**
  - `tweepy`
  - `json`
  - `logging`
  - `os`
  - `pathlib`



## Utilizzo

Esegui lo script tramite la riga di comando:

```bash
python 02_twitter_access_data.py
```

### Funzionamento dello Script

1. **Caricamento delle Credenziali:**

   Lo script carica le credenziali dall'apposito file di testo.

2. **Autenticazione all'API di Twitter:**

   Utilizza le credenziali caricate per autenticarsi all'API di Twitter.

3. **Definizione della Query di Ricerca:**

   La query di ricerca è definita all'interno dello script. Per impostazione predefinita, cerca tweet con l'hashtag `#MyBrandName` escludendo i retweet:

   ```python
   query = "#MyBrandName -filter:retweets"
   ```

   **Personalizzazione:** Puoi modificare questa query per adattarla alle tue esigenze.

4. **Raccolta dei Tweet:**

   Lo script raccoglie fino a 50 tweet che corrispondono alla query specificata.

5. **Salvataggio dei Dati:**

   I tweet raccolti vengono salvati in un file JSON chiamato `tweets_data.json` nella cartella `output`.

## Personalizzazione

- **Modifica della Query di Ricerca:**

  Apri lo script `02_twitter_access_data.py` e modifica la variabile `query` per cambiare i criteri di ricerca.

  ```python
  query = "#NuovoHashtag -filter:retweets"
  ```

- **Numero di Tweet da Raccogliere:**

  Modifica il parametro `count` nella funzione `collect_tweets` per cambiare il numero di tweet da raccogliere.

  ```python
  tweets = collect_tweets(api, query, count=100)  # Raccoglie 100 tweet
  ```

## Esempio

Esempio di esecuzione dello script:

```bash
python 02_twitter_access_data.py
```

**Output Atteso:**

- **Log di Informazioni:**

  ```plaintext
  INFO - 2025-01-24 10:00:00,000 - load_twitter_credentials: Credenziali caricate da /path/to/app/3_2_twitter_access_data.txt.
  INFO - 2025-01-24 10:00:01,000 - authenticate_to_twitter: Autenticazione completata con successo.
  INFO - 2025-01-24 10:00:02,000 - collect_tweets: Raccogliti 50 tweet per la query: '#MyBrandName -filter:retweets'.
  INFO - 2025-01-24 10:00:03,000 - save_to_json: Dati salvati nel file: tweets_data.json.
  ```

- **File di Output:**

  Un file JSON `tweets_data.json` contenente i tweet raccolti con i seguenti campi:

  ```json
  [
      {
          "text": "Esempio di tweet #MyBrandName",
          "date": "2025-01-24T10:00:00",
          "id": 1234567890,
          "author": "utente1"
      },
      ...
  ]
  ```

## Risoluzione dei Problemi

- **Errore di File delle Credenziali Non Trovato:**

  Assicurati che il file `3_2_twitter_access_data.txt` esista nel percorso corretto e che il percorso specificato nello script sia corretto.

- **Errore di Autorizzazione:**

  Verifica che le credenziali dell'API di Twitter siano corrette e che non siano scadute. Puoi rigenerare le chiavi dal [Developer Portal di Twitter](https://developer.twitter.com/).

- **Limiti di Richiesta Raggiunti:**

  Se raggiungi i limiti di richiesta dell'API di Twitter, lo script attenderà automaticamente fino a quando i limiti non saranno resettati grazie all'opzione `wait_on_rate_limit=True` nella configurazione dell'API.

---

**Nota:** Ricorda di mantenere le tue credenziali API di Twitter al sicuro e di non condividerle pubblicamente. Evita di commettere il file delle credenziali nei repository pubblici.


## 👨‍💻 Contatti

Per domande o suggerimenti, crea un *issue* in questo repository o contatta **Andrey Golub** [(@aVg)](https://www.linkedin.com/in/andreygolub/).

---

## ⚠️ Disclaimer

Questo materiale è destinato esclusivamente a fini educativi e formativi. Gli esempi di codice e dati forniti sono puramente dimostrativi e non devono essere utilizzati in ambienti di produzione senza le dovute verifiche e personalizzazioni.
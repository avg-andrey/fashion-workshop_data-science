# download_dataset.py

"""
Script: download_dataset.py

Descrizione:
Questo script scarica un dataset di immagini di moda da KaggleHub e ne restituisce il percorso locale.
È utilizzato come primo passo nella pipeline di elaborazione dei dati, garantendo che il dataset sia disponibile per le fasi successive.

-------------------------------------------------------
Funzionalità principali:
1. **Eliminazione della cache**: 
   - Rimuove la versione cache del dataset per forzare un nuovo download.
   - Utile quando si desidera scaricare la versione più recente dei dati.

2. **Download del dataset da KaggleHub**: 
   - Utilizza l'API `kagglehub` per scaricare il dataset specificato.
   - Verifica che il download sia riuscito controllando l'esistenza e il contenuto della cartella.

3. **Gestione degli errori**:
   - Segnala eventuali problemi di connessione, autenticazione o disponibilità dei file.
   - Verifica che il dataset contenga effettivamente dei file dopo il download.

-------------------------------------------------------
Struttura dei file scaricati:
- I file vengono salvati nella directory locale di KaggleHub: `~/.cache/kagglehub/datasets/{nome_dataset}/versions/latest/`
- Il percorso di output viene stampato nella console.

-------------------------------------------------------
Flusso di esecuzione:
1. **Definizione del nome del dataset**: `NOME_DATASET = "jainaru/womens-fashion-image-dataset"`
2. **Chiamata alla funzione `scarica_dataset()`**:
   - Cancella la cache del dataset.
   - Scarica i file nella directory di KaggleHub.
   - Verifica la presenza dei dati.
3. **Output**:
   - Stampa il percorso del dataset scaricato o segnala errori in caso di problemi.

-------------------------------------------------------
Prerequisiti:
- L'utente deve avere un account Kaggle configurato e le credenziali API accessibili.
- Il pacchetto `kagglehub` deve essere installato (`pip install kagglehub`).

Output:
- Stampa a console il percorso del dataset scaricato o eventuali errori.

Autore: [Inserisci il tuo nome]
Data: [Inserisci la data]
"""


import kagglehub
import os
import shutil

def cancella_cache(nome_dataset):
    """
    Elimina la cartella della cache per forzare un nuovo download.
    """
    cache_path = os.path.expanduser(f"~/.cache/kagglehub/datasets/{nome_dataset}/versions")
    if os.path.exists(cache_path):
        print(f"[INFO] Eliminazione della cache: {cache_path}")
        shutil.rmtree(cache_path)

def scarica_dataset(nome_dataset):
    """
    Scarica il dataset da KaggleHub e restituisce il percorso dei file.
    
    Parametri:
    nome_dataset (str): Nome del dataset su KaggleHub.
    
    Ritorna:
    str: Percorso dei file del dataset scaricato o None in caso di errore.
    """
    try:
        # Cancella la cache prima di scaricare
        cancella_cache(nome_dataset)
        
        print(f"[INFO] Download del dataset: {nome_dataset}")
        percorso = kagglehub.dataset_download(nome_dataset)
        
        if not percorso or not os.path.exists(percorso):
            raise FileNotFoundError("Il percorso del dataset non esiste o il download non è riuscito.")
        
        # Controlla se la cartella contiene effettivamente dei file
        if not os.listdir(percorso):
            raise FileNotFoundError("Il dataset risulta scaricato ma la cartella è vuota.")
        
        print(f"[SUCCESSO] Dataset scaricato con successo: {percorso}")
        return percorso
    
    except FileNotFoundError as e:
        print(f"[ERRORE] File non trovato: {e}")
    except Exception as e:
        print(f"[ERRORE] Si è verificato un errore durante il download: {e}")
    
    return None

if __name__ == "__main__":
    # Nome del dataset da scaricare
    NOME_DATASET = "jainaru/womens-fashion-image-dataset"
    
    # Scarica il dataset
    percorso_dataset = scarica_dataset(NOME_DATASET)
    
    # Se il download ha avuto successo, mostra il percorso
    if percorso_dataset:
        print("Percorso ai file del dataset:", percorso_dataset)

# 03_tweets_data_cleaning.py

import json
import re
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import os
import sys
from langdetect import detect, LangDetectException  # Per rilevare la lingua

# Configurazione del logging
def setup_logging():
    """
    Configura il sistema di logging per tracciare le operazioni dello script.
    
    Restituisce:
        logger (logging.Logger): Oggetto logger configurato.
    """
    logger = logging.getLogger('TweetDataCleaning')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler per la console con livello INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Handler per il file di log con livello DEBUG
    fh = logging.FileHandler('03_data_cleaning.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# Inizializzazione del logger
logger = setup_logging()

# Funzione per scaricare i dati NLTK necessari
def download_nltk_data():
    """
    Verifica la presenza dei dati NLTK necessari e li scarica se non sono presenti.
    """
    try:
        logger.info("download_nltk_data: Verifica della presenza dei dati NLTK necessari...")
        nltk.data.find('tokenizers/punkt')  # Verifica se 'punkt' è presente
        nltk.download('punkt_tab')  # Questo sembra un errore, probabilmente dovrebbe essere 'punkt'
        nltk.data.find('corpora/stopwords')  # Verifica se 'stopwords' è presente
        logger.info("download_nltk_data: I dati NLTK necessari sono già installati.")
    except LookupError as e:
        logger.warning("download_nltk_data: Dati NLTK necessari non trovati. Tentativo di download...")
        try:
            nltk.download('punkt')  # Scarica 'punkt' se non presente
            nltk.download('stopwords')  # Scarica 'stopwords' se non presente
            nltk.data.find('tokenizers/punkt')  # Verifica aggiuntiva dopo il download
            nltk.data.find('corpora/stopwords')  # Verifica aggiuntiva dopo il download
            logger.info("download_nltk_data: Dati NLTK scaricati con successo.")
        except Exception as e:
            logger.error(f"download_nltk_data: Errore durante il download o la verifica dei dati NLTK: {e}")
            sys.exit(1)

# Funzione per pulire il testo
def clean_text(text, custom_stopwords=None):
    """
    Pulisce il testo rimuovendo link, hashtag, menzioni, caratteri speciali e stop-words.
    
    Args:
        text (str): Il testo da pulire.
        custom_stopwords (set, optional): Stop-words personalizzate da aggiungere.
    
    Returns:
        str: Il testo pulito.
    """
    logger.debug("clean_text: Inizio della pulizia del testo")
    try:
        # Rimuove i link (es. http://example.com o www.example.com)
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
        logger.debug("Rimosso i link dal testo.")

        # Rimuove il simbolo "#" dai hashtag, lasciando le parole
        text = re.sub(r"#", '', text)
        logger.debug("Rimosso i simboli '#' dagli hashtag.")

        # Rimuove le menzioni (@username)
        text = re.sub(r"@\w+", '', text)
        logger.debug("Rimosse le menzioni (@username) dal testo.")

        # Rimuove tutti i caratteri speciali, mantenendo solo lettere, numeri e spazi
        text = re.sub(r"[^\w\s]", '', text)
        logger.debug("Rimossi i caratteri speciali dal testo.")

        # Converte tutto il testo in minuscolo
        text = text.lower()
        logger.debug("Convertito il testo in minuscolo.")

        # Rileva la lingua del testo
        try:
            lang = detect(text)
            logger.debug(f"clean_text: Lingua rilevata: {lang}")
        except LangDetectException:
            logger.warning("clean_text: Impossibile rilevare la lingua. Uso l'italiano come default.")
            lang = 'it'

        # Tokenizzazione
        tokens = word_tokenize(text)
        logger.debug(f"Tokenizzati {len(tokens)} parole.")

        # Caricamento delle stopwords standard
        if lang == 'it':
            stop_words = set(stopwords.words('italian'))
            logger.debug("Caricate le stop-words per l'italiano.")
        elif lang == 'en':
            stop_words = set(stopwords.words('english'))
            logger.debug("Caricate le stop-words per l'inglese.")
        else:
            logger.warning(f"clean_text: Lingua non supportata: {lang}. Uso l'italiano come fallback.")
            stop_words = set(stopwords.words('italian'))

        # Aggiunta delle stop-words personalizzate
        if custom_stopwords:
            stop_words.update(custom_stopwords)
            logger.debug("Aggiunte stop-words personalizzate.")

        # Calcolo del numero iniziale di token
        num_tokens_iniziali = len(tokens)

        # Rimozione delle stop-words
        cleaned_tokens = [word for word in tokens if word not in stop_words]
        logger.debug(f"Rimossi {num_tokens_iniziali - len(cleaned_tokens)} token come stop-words.")

        # Calcolo del numero di token rimanenti
        num_tokens_finali = len(cleaned_tokens)
        num_tokens_rimossi = num_tokens_iniziali - num_tokens_finali

        # Log dei risultati
        logger.info(
            f"clean_text: Pulizia completata. Token iniziali: {num_tokens_iniziali}, "
            f"Token rimossi: {num_tokens_rimossi}, Token finali: {num_tokens_finali}."
        )

        # Ricostruzione del testo pulito
        cleaned_text = ' '.join(cleaned_tokens)
        logger.debug("Ricostruito il testo pulito.")
        return cleaned_text
    except LookupError as e:
        logger.error(f"clean_text: Errore durante la pulizia del testo: {e}")
        logger.error("clean_text: Assicurati di aver scaricato i dati NLTK necessari.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"clean_text: Errore durante la pulizia del testo: {e}")
        return ""

# Funzione per caricare i dati da un file JSON
def load_json(file_path):
    """
    Carica i dati da un file JSON.
    
    Args:
        file_path (str): Il percorso del file JSON.
    
    Returns:
        list: Lista di record caricati dal file JSON.
    """
    logger.debug(f"load_json: Tentativo di caricare il file: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"File non trovato: {file_path}")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"load_json: Caricati {len(data)} record da {file_path}")
            return data
    except Exception as e:
        logger.error(f"load_json: Errore durante il caricamento del file {file_path}: {e}")
        return []

# Funzione per salvare i dati in un file JSON
def save_json(data, file_path):
    """
    Salva i dati in un file JSON.
    
    Args:
        data (list): Dati da salvare.
        file_path (str): Il percorso del file JSON di destinazione.
    """
    logger.debug(f"save_json: Tentativo di salvare i dati nel file: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info(f"save_json: Dati salvati con successo in {file_path}")
    except Exception as e:
        logger.error(f"save_json: Errore durante il salvataggio del file {file_path}: {e}")

# Funzione principale per la pre-elaborazione dei tweet
def preprocess_tweets(input_file, output_file, stop_words):
    """
    Pre-elabora i tweet caricati da un file JSON e salva i tweet puliti in un altro file JSON.
    
    Args:
        input_file (str): Percorso del file JSON di input contenente i tweet.
        output_file (str): Percorso del file JSON di output per i tweet puliti.
        stop_words (set): Insieme di stop-words da rimuovere dal testo.
    """
    logger.info("preprocess_tweets: Inizio del processo di pre-elaborazione dei tweet.")
    tweets = load_json(input_file)
    if not tweets:
        logger.warning("preprocess_tweets: Nessun dato da elaborare.")
        return

    cleaned_tweets = []
    for idx, tweet in enumerate(tweets, start=1):
        logger.info(f"preprocess_tweets: Elaborazione del tweet {idx}/{len(tweets)}")
        cleaned_text = clean_text(tweet.get("text", ""), stop_words)
        if cleaned_text:
            logger.info(f"preprocess_tweets: Tweet {idx} elaborato con successo.")
            cleaned_tweet = {
                "text": cleaned_text,
                "date": tweet.get("date", "")
            }
            cleaned_tweets.append(cleaned_tweet)
        else:
            logger.warning(f"preprocess_tweets: Il testo del tweet {idx} è vuoto dopo la pulizia.")

    save_json(cleaned_tweets, output_file)
    logger.info("preprocess_tweets: Processo di pre-elaborazione completato.")

# Funzione per contare i record in un file JSON
def count_records(file_path):
    """
    Conta il numero di record presenti in un file JSON.
    
    Args:
        file_path (str): Il percorso del file JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"count_records: Numero di record nel file: {len(data)}")
    except Exception as e:
        print(f"count_records: Errore: {e}")

# Funzione per aggiungere parole personalizzate alle stop-words
def add_custom_stopwords(custom_words):
    """
    Aggiunge parole personalizzate all'elenco delle stop-words per la lingua italiana.

    Args:
        custom_words (list): Lista di parole personalizzate da aggiungere alle stop-words.

    Returns:
        set: Insieme aggiornato di stop-words.

    Raises:
        ValueError: Se custom_words non è una lista o contiene elementi non stringa.
    """
    logger = logging.getLogger("custom_stopwords")
    logger.info("Inizio dell'aggiunta di stop-words personalizzate.")

    try:
        # Validazione input
        if not isinstance(custom_words, list):
            raise ValueError("Il parametro custom_words deve essere una lista.")
        if not all(isinstance(word, str) for word in custom_words):
            raise ValueError("Tutti gli elementi di custom_words devono essere stringhe.")

        # Carica le stop-words standard per l'italiano
        stop_words = set(stopwords.words('italian'))
        logger.info("Stop-words standard caricate con successo.")

        # Aggiunge le parole personalizzate
        logger.info(f"Parole personalizzate da aggiungere: {', '.join(custom_words)}")
        stop_words.update(custom_words)

        logger.info("Stop-words personalizzate aggiunte con successo.")
        return stop_words

    except ValueError as ve:
        logger.error(f"Errore di validazione: {ve}")
        raise

    except Exception as e:
        logger.error(f"Errore durante l'aggiunta di stop-words: {e}")
        sys.exit(1)

# Esecuzione del processo
if __name__ == "__main__":

    # Percorsi dei file di input e output
    input_file = "./input_data/02_tweets_dati_sintetici.json"
    output_file = "./output_data/03_tweets_dati_cleaned.json"
        
    logger.info("MAIN: Avvio dello script.")
    
    # Conta i record nel file di input
    count_records(input_file)

    # Mostra i percorsi di dati NLTK
    print(nltk.data.path)
    
    # Scarica i dati NLTK necessari
    download_nltk_data()

    # Aggiunge le custom stop-words
    custom_words = ["mybrandname", "altrotermine"]
    stop_words = add_custom_stopwords(custom_words)

    # Mostra le prime 10 stop-words come esempio (per log educativo)
    logger.info(f"MAIN: Prime 10 stop-words aggiornate: {list(stop_words)[:10]}")

    # Pre-elabora i tweet e salva i risultati
    preprocess_tweets(input_file, output_file, stop_words)

    logger.info("MAIN: Script terminato.")

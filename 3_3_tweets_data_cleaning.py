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
    logger = logging.getLogger('TweetDataCleaning')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler('03_data_cleaning.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

logger = setup_logging()

# Funzione per scaricare i dati NLTK necessari
def download_nltk_data():
    try:
        logger.info("download_nltk_data: Verifica della presenza dei dati NLTK necessari...")
        nltk.data.find('tokenizers/punkt')
        nltk.download('punkt_tab')
        nltk.data.find('corpora/stopwords')
        logger.info("download_nltk_data: I dati NLTK necessari sono già installati.")
    except LookupError as e:
        logger.warning("download_nltk_data: Dati NLTK necessari non trovati. Tentativo di download...")
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.data.find('tokenizers/punkt')  # Verifica aggiuntiva
            nltk.data.find('corpora/stopwords')
            logger.info("download_nltk_data: Dati NLTK scaricati con successo.")
        except Exception as e:
            logger.error(f"download_nltk_data: Errore durante il download o la verifica dei dati NLTK: {e}")
            sys.exit(1)

# Funzione per pulire il testo
def clean_text(text, custom_stopwords=None):
    logger.debug("clean_text: Inizio della pulizia del testo")
    try:
        # Rimuove i link (es. http://example.com o www.example.com)
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

        # Rimuove il simbolo "#" dai hashtag, lasciando le parole (es. "#great" → "great")
        text = re.sub(r"#", '', text)

        # Rimuove le menzioni (@username), che di solito non aggiungono valore semantico
        text = re.sub(r"@\w+", '', text)

        # Rimuove tutti i caratteri speciali, mantenendo solo lettere, numeri e spazi
        text = re.sub(r"[^\w\s]", '', text)

        # Converte tutto il testo in minuscolo per standardizzare l'analisi
        text = text.lower()

        # Rileva la lingua del testo
        try:
            lang = detect(text)
            logger.debug(f"clean_text: Lingua rilevata: {lang}")
        except LangDetectException:
            logger.warning("clean_text: Impossibile rilevare la lingua. Utilizzo dell'italiano come predefinito.")
            lang = 'it'

        # Tokenizzazione
        tokens = word_tokenize(text)

        # Caricamento delle stopwords standard e aggiunta di quelle personalizzate
        if lang == 'it':
            stop_words = set(stopwords.words('italian'))
        elif lang == 'en':
            stop_words = set(stopwords.words('english'))
        else:
            logger.warning(f"clean_text: Lingua non supportata: {lang}. Utilizzo dell'italiano come fallback.")
            stop_words = set(stopwords.words('italian'))

        # Aggiunta delle stop-words personalizzate, se fornite
        if custom_stopwords:
            #logger.info(f"clean_text: Aggiunta delle stop-words personalizzate: {', '.join(custom_stopwords)}")
            stop_words.update(custom_stopwords)

        # Rimozione delle stop-words
        cleaned_tokens = [word for word in tokens if word not in stop_words]

        # Ricostruzione del testo pulito
        cleaned_text = ' '.join(cleaned_tokens)
        logger.debug(f"clean_text: Testo pulito: {cleaned_text}")
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
    logger.debug(f"save_json: Tentativo di salvare i dati nel file: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info(f"save_json: Dati salvati con successo in {file_path}")
    except Exception as e:
        logger.error(f"save_json: Errore durante il salvataggio del file {file_path}: {e}")

# Funzione principale per la pre-elaborazione dei tweet
def preprocess_tweets(input_file, output_file, stop_words):
    logger.info("preprocess_tweets: Inizio del processo di pre-elaborazione dei tweet.")
    tweets = load_json(input_file)
    if not tweets:
        logger.warning("preprocess_tweets: Nessun dato da elaborare.")
        return

    cleaned_tweets = []
    for idx, tweet in enumerate(tweets, start=1):
        logger.debug(f"preprocess_tweets: Elaborazione del tweet {idx}/{len(tweets)}")
        cleaned_text = clean_text(tweet.get("text", ""), stop_words)
        if cleaned_text:
            cleaned_tweet = {
                "text": cleaned_text,
                "date": tweet.get("date", "")
            }
            cleaned_tweets.append(cleaned_tweet)
        else:
            logger.warning(f"preprocess_tweets: Tweet {idx} ha restituito un testo vuoto dopo la pulizia.")

    save_json(cleaned_tweets, output_file)
    logger.info("preprocess_tweets: Processo di pre-elaborazione completato.")


def count_records(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"count_records: Numero di record nel file: {len(data)}")
    except Exception as e:
        print(f"count_records: Errore: {e}")

# Funzione per aggiungere parole personalizzate alle stop-words
def add_custom_stopwords(custom_words):
    logger.info("add_custom_stopwords: Inizio dell'aggiunta di stop-words personalizzate.")
    try:
        # Carica le stop-words standard per l'italiano
        stop_words = set(stopwords.words('italian'))

        # Aggiunge le parole personalizzate
        logger.info(f"Parole aggiunte: {', '.join(custom_words)}")
        stop_words.update(custom_words)

        # Restituisce l'elenco aggiornato
        logger.info("add_custom_stopwords: Stop-words personalizzate aggiunte con successo.")
        return stop_words
    except Exception as e:
        logger.error(f"add_custom_stopwords: Errore durante l'aggiunta di stop-words: {e}")
        sys.exit(1)


# Esecuzione del processo
if __name__ == "__main__":
    logger.info("MAIN: Avvio dello script.")
    count_records("02_tweets_dati_sintetici.json")

    print(nltk.data.path)
    download_nltk_data()

    # Aggiunge le custom stop-words
    custom_words = {"mybrandname", "altrotermine"}
    stop_words = add_custom_stopwords(custom_words)

    # Mostra le prime 10 stop-words come esempio (per log educativo)
    logger.info(f"MAIN: Prime 10 stop-words aggiornate: {list(stop_words)[:10]}")

    input_file = "./input_data/02_tweets_dati_sintetici.json"
    output_file = "./output_data/03_tweets_dati_cleaned.json"
    preprocess_tweets(input_file, output_file, stop_words)

    logger.info("MAIN: Script terminato.")

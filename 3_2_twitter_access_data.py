# 02_twitter_access_data.py

import tweepy  # Libreria per interagire con l'API di Twitter
import json  # Libreria per la manipolazione di dati JSON
import logging  # Libreria per il logging delle operazioni
import os  # Libreria per interagire con il sistema operativo
from pathlib import Path  # Libreria per la gestione dei percorsi dei file

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,  # Livello dei log (INFO)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato dei messaggi di log
)
logger = logging.getLogger('TwitterAccessData')  # Creazione di un logger specifico


def load_twitter_credentials(file_path):
    """
    Carica le credenziali di accesso all'API di Twitter da un file.

    Args:
        file_path (str): Il percorso del file contenente le credenziali.

    Returns:
        dict: Dizionario contenente le chiavi delle credenziali.
    """
    credentials = {}  # Dizionario per memorizzare le credenziali
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Suddivide ogni riga in chiave e valore basandosi sul simbolo '='
                key, value = line.strip().split('=')
                credentials[key] = value  # Aggiunge la coppia chiave-valore al dizionario
        logger.info(f"load_twitter_credentials: Credenziali caricate da {file_path}.")
    except FileNotFoundError:
        logger.error(f"load_twitter_credentials: File non trovato: {file_path}.")
        raise
    except Exception as e:
        logger.error(f"load_twitter_credentials: Errore durante il caricamento delle credenziali: {e}.")
        raise
    return credentials


def authenticate_to_twitter(credentials):
    """
    Autentica l'applicazione all'API di Twitter utilizzando le credenziali fornite.

    Args:
        credentials (dict): Dizionario contenente le chiavi delle credenziali.

    Returns:
        tweepy.API: Oggetto API autenticato per interagire con Twitter.
    """
    try:
        # Configura l'autenticazione OAuth1 con le credenziali fornite
        auth = tweepy.OAuth1UserHandler(
            credentials["API_KEY"],
            credentials["API_SECRET_KEY"],
            credentials["ACCESS_TOKEN"],
            credentials["ACCESS_TOKEN_SECRET"]
        )
        # Crea un oggetto API con l'autenticazione e gestisce i limiti di richiesta
        api = tweepy.API(auth, wait_on_rate_limit=True)
        logger.info("authenticate_to_twitter: Autenticazione completata con successo.")
        return api
    except KeyError as e:
        logger.error(f"authenticate_to_twitter: Mancata chiave di credenziali: {e}.")
        raise
    except Exception as e:
        logger.error(f"authenticate_to_twitter: Errore durante l'autenticazione: {e}.")
        raise


def collect_tweets(api, query, count=50):
    """
    Raccoglie tweet basati su una query specifica.

    Args:
        api (tweepy.API): Oggetto API autenticato.
        query (str): Query di ricerca per i tweet.
        count (int, optional): Numero di tweet da raccogliere. Default è 50.

    Returns:
        list: Lista di dizionari contenenti i dati dei tweet raccolti.
    """
    tweets_data = []  # Lista per memorizzare i dati dei tweet
    try:
        # Utilizza Cursor per iterare sui tweet che soddisfano la query
        for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="it", tweet_mode="extended").items(count):
            tweets_data.append({
                "text": tweet.full_text,  # Testo completo del tweet
                "date": str(tweet.created_at),  # Data di creazione del tweet
                "id": tweet.id,  # ID del tweet
                "author": tweet.user.screen_name  # Nome utente dell'autore
            })
        logger.info(f"collect_tweets: Raccogliti {len(tweets_data)} tweet per la query: '{query}'.")
    except tweepy.errors.Unauthorized:
        logger.error("collect_tweets: Token non valido o scaduto. Controlla le tue credenziali.")
    except tweepy.TweepyException as e:
        logger.error(f"collect_tweets: Si è verificato un errore durante la raccolta dei tweet: {e}.")
    except Exception as e:
        logger.error(f"collect_tweets: Errore inaspettato durante la raccolta dei tweet: {e}.")
    return tweets_data


def save_to_json(data, output_file):
    """
    Salva i dati forniti in un file JSON.

    Args:
        data (list): Dati da salvare nel file JSON.
        output_file (str): Il percorso del file JSON di destinazione.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # Salva i dati con indentazione
        logger.info(f"save_to_json: Dati salvati nel file: {output_file}.")
    except IOError as e:
        logger.error(f"save_to_json: Errore durante il salvataggio del file: {e}.")


def main():
    """
    Processo principale per raccogliere i dati dei tweet e salvarli in un file JSON.
    """
    try:
        # Log della directory di lavoro corrente
        logger.info(f"main: Directory di lavoro corrente: {os.getcwd()}")

        # Determina il percorso del file delle credenziali relativo allo script
        script_dir = Path(__file__).parent  # Directory dello script
        filepath = (script_dir / "app" / "3_2_twitter_access_data.txt").resolve()  # Percorso completo del file delle credenziali

        logger.info(f"main: Percorso previsto del file delle credenziali: {filepath}")

        # Caricamento delle credenziali dal file
        credentials = load_twitter_credentials(filepath)

        # Autenticazione all'API di Twitter
        api = authenticate_to_twitter(credentials)

        # Definizione della query di ricerca per i tweet
        query = "#MyBrandName -filter:retweets"  # Cerca i tweet con l'hashtag #MyBrandName escludendo i retweet

        # Raccolta dei dati dei tweet
        logger.info("main: Raccolta dei tweet in corso...")
        tweets = collect_tweets(api, query, count=50)

        if tweets:
            logger.info(f"main: Raccogliti {len(tweets)} tweet.")
            # Definisce il percorso del file di output per i dati raccolti
            output_file = "tweets_data.json"
            # Salva i dati raccolti nel file JSON
            save_to_json(tweets, output_file)
        else:
            logger.warning("main: Nessun tweet è stato raccolto. I dati non sono stati salvati.")

    except FileNotFoundError as e:
        logger.error(f"main: File delle credenziali non trovato: {filepath}.")
        print(f"Errore: Il file delle credenziali non è stato trovato. Percorso previsto: {filepath}")
    except tweepy.errors.Unauthorized:
        logger.error("main: Errore di autorizzazione. Controlla le tue credenziali Twitter.")
        print("Errore di autorizzazione: Controlla le tue credenziali Twitter.")
    except Exception as e:
        logger.error(f"main: Si è verificato un errore inaspettato: {e}.")
        print(f"Si è verificato un errore inaspettato: {e}")


if __name__ == "__main__":
    main()

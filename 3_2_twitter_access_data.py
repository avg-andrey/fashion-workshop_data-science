# 02_twitter_access_data.py

import tweepy
import json
import logging
import os
from pathlib import Path


# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,  # Livello dei log
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato dei messaggi
)

# Funzione per caricare le credenziali di accesso da un file
def load_twitter_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = {}
        for line in file:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

# Configurazione dell'autenticazione all'API di Twitter
def authenticate_to_twitter(credentials):
    auth = tweepy.OAuth1UserHandler(
        credentials["API_KEY"],
        credentials["API_SECRET_KEY"],
        credentials["ACCESS_TOKEN"],
        credentials["ACCESS_TOKEN_SECRET"]
    )
    return tweepy.API(auth, wait_on_rate_limit=True)


# Funzione per raccogliere tweet
def collect_tweets(api, query, count=50):
    tweets_data = []
    try:
        for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="it", tweet_mode="extended").items(count):
            tweets_data.append({
                "text": tweet.full_text,
                "date": str(tweet.created_at),
                "id": tweet.id,
                "author": tweet.user.screen_name
            })
    except tweepy.errors.Unauthorized:
        print("Errore: Token non valido o scaduto. Controlla le tue credenziali.")
        return []
    except tweepy.TweepyException as e:
        print(f"Si è verificato un errore durante la raccolta dei tweet: {e}")
        return []
    return tweets_data

# Funzione per salvare i dati in un file JSON
def save_to_json(data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Dati salvati nel file: {output_file}")
    except IOError as e:
        print(f"Errore durante il salvataggio del file: {e}")

# Processo principale
def main():
    try:
        logging.info(f"Current working directory: {os.getcwd()}")
        # Caricamento delle credenziali
        script_dir = Path(__file__).parent
        filepath = (script_dir / "app" / "3_2_twitter_access_data.txt").resolve()

        logging.info(f"Expected credentials file path: {filepath}")
        credentials = load_twitter_credentials(filepath)
        
        # Autenticazione
        api = authenticate_to_twitter(credentials)
        
        # Query di ricerca
        query = "#MyBrandName -filter:retweets"  # Escludiamo i retweet
        
        # Raccolta dei dati
        print("Raccolta dei tweet in corso...")
        tweets = collect_tweets(api, query, count=50)
        if tweets:
            print(f"Sono stati raccolti {len(tweets)} tweet.")
            
            # Salvataggio dei dati in un file
            output_file = "tweets_data.json"
            save_to_json(tweets, output_file)
        else:
            print("Nessun tweet è stato raccolto. I dati non sono stati salvati.")

    except FileNotFoundError as e:
        logging.error(f"File delle credenziali non trovato: {filepath}")
        print(f"Errore: Il file delle credenziali non è stato trovato. Percorso previsto: {filepath}")
    except tweepy.errors.Unauthorized:
        print("Errore di autorizzazione: Controlla le tue credenziali Twitter.")
    except Exception as e:
        logging.error(f"Si è verificato un errore inaspettato: {e}")
        print(f"Si è verificato un errore inaspettato: {e}")


if __name__ == "__main__":
        main()

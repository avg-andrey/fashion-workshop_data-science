# 3_4_sentiment_analysis_hf.py

import json
import logging
import torch  # Importa torch per determinare il dispositivo (CPU o GPU)
from transformers import pipeline  # Importa la pipeline di HuggingFace per l'analisi del sentiment
import os
from collections import Counter  # Importa Counter per contare le occorrenze delle emozioni

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SentimentAnalysis')


def load_json(file_path):
    """
    Carica i dati da un file JSON.

    Args:
        file_path (str): Il percorso del file JSON da caricare.

    Returns:
        list: Lista di record caricati dal file JSON. Ritorna una lista vuota in caso di errore.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"load_json: Caricati {len(data)} record da {file_path}.")
            return data
    except Exception as e:
        logger.error(f"load_json: Errore durante il caricamento del file JSON: {e}")
        return []


def save_json(data, file_path):
    """
    Salva i dati in un file JSON.

    Args:
        data (list): Dati da salvare nel file JSON.
        file_path (str): Il percorso del file JSON di destinazione.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"save_json: Risultati salvati in {file_path}.")
    except Exception as e:
        logger.error(f"save_json: Errore durante il salvataggio del file JSON: {e}")


def sentiment_analysis(input_file, output_file, model_name, device):
    """
    Esegue l'analisi del sentiment sui dati caricati da un file JSON e salva i risultati.
    Inoltre, calcola e registra le statistiche dei tipi di emozioni rilevate.

    Args:
        input_file (str): Percorso del file JSON di input contenente i tweet puliti.
        output_file (str): Percorso del file JSON di output per i risultati dell'analisi del sentiment.
        model_name (str): Nome del modello pre-addestrato da utilizzare per l'analisi del sentiment.
        device (int): Dispositivo su cui caricare il modello (0 per GPU, -1 per CPU).
    """
    # Caricamento dei dati
    tweets = load_json(input_file)
    if not tweets:
        logger.error("sentiment_analysis: Nessun dato da analizzare. Uscita.")
        return

    # Inizializzazione del modello pre-addestrato
    try:
        logger.info(f"sentiment_analysis: Caricamento del modello pre-addestrato: {model_name}...")
        sentiment_pipeline = pipeline("sentiment-analysis", model=model_name, device=device)
        logger.info("sentiment_analysis: Modello caricato con successo.")
    except Exception as e:
        logger.error(f"sentiment_analysis: Errore durante il caricamento del modello {model_name}: {e}")
        return

    # Analisi dei sentimenti
    results = []  # Lista per memorizzare i risultati dell'analisi
    sentiment_counts = Counter()  # Contatore per le statistiche delle emozioni
    for idx, tweet in enumerate(tweets, start=1):
        tweet_text = tweet.get('text', '')
        logger.info(f"sentiment_analysis: Analisi del tweet {idx}/{len(tweets)}: {tweet_text}")
        try:
            # Esecuzione dell'analisi del sentiment sul testo del tweet
            analysis = sentiment_pipeline(tweet_text)[0]
            sentiment_label = analysis["label"].lower()  # Etichetta del sentiment (es. 'positive', 'negative')
            sentiment_score = round(analysis["score"], 4)  # Punteggio del sentiment

            # Log del risultato dell'analisi
            logger.info(f"sentiment_analysis: Risultato analisi: sentiment='{sentiment_label}', score={sentiment_score}")

            # Aggiunta dei risultati alla lista
            results.append({
                "text": tweet_text,
                "sentiment": sentiment_label,
                "score": sentiment_score,
                "date": tweet.get("date", "")  # Data del tweet, se disponibile
            })

            # Aggiornamento del contatore delle emozioni
            sentiment_counts[sentiment_label] += 1
        except Exception as e:
            logger.error(f"sentiment_analysis: Errore durante l'analisi del tweet: {e}")

    # Salvataggio dei risultati
    save_json(results, output_file)

    # Calcolo e registrazione delle statistiche delle emozioni
    total_analyzed = sum(sentiment_counts.values())
    if total_analyzed > 0:
        logger.info("sentiment_analysis: Statistiche delle emozioni rilevate:")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / total_analyzed) * 100
            logger.info(f"  - {sentiment.capitalize()}: {count} tweet ({percentage:.2f}%)")
    else:
        logger.warning("sentiment_analysis: Nessuna emozione rilevata per calcolare le statistiche.")


# Esecuzione dello script
if __name__ == "__main__":
    # Log della directory di lavoro corrente
    logger.info(f"Current working directory: {os.getcwd()}")

    # Percorso del file di input contenente i tweet puliti
    input_file = "./input_data/03_tweets_dati_cleaned.json"

    # Determina il dispositivo: GPU (0) se disponibile, altrimenti CPU (-1)
    if torch.cuda.is_available():
        device = 0  # Usa la prima GPU disponibile
        logger.info("MAIN: GPU rilevata. Il modello sarà caricato sulla GPU.")
    else:
        device = -1  # Usa la CPU
        logger.info("MAIN: GPU non rilevata. Il modello sarà caricato sulla CPU.")

    # Dizionario dei modelli da utilizzare con i rispettivi file di output
    models = {
        "MilaNLProc/feel-it-italian-sentiment": "./output_data/04_tweets_sentiment_analysis_feel_it.json",
        "neuraly/bert-base-italian-cased-sentiment": "./output_data/04_tweets_sentiment_analysis_bert_italian.json"
    }

    # Iterazione sui modelli e esecuzione dell'analisi del sentiment
    for model_name, output_file in models.items():
        logger.info(f"MAIN: Inizio analisi con il modello: {model_name}")
        sentiment_analysis(input_file, output_file, model_name, device)
        logger.info(f"MAIN: Analisi completata con il modello: {model_name}. Risultati salvati in {output_file}.")

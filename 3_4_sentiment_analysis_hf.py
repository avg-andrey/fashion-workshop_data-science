# 3_4_sentiment_analysis_hf.py

import json
import logging
import torch  # Importa torch per determinare il dispositivo
from transformers import pipeline

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SentimentAnalysis')

# Funzione per caricare i dati da un file JSON
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"load_json: Caricati {len(data)} record da {file_path}.")
            return data
    except Exception as e:
        logger.error(f"load_json: Errore durante il caricamento del file JSON: {e}")
        return []

# Funzione per salvare i risultati in un file JSON
def save_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"save_json: Risultati salvati in {file_path}.")
    except Exception as e:
        logger.error(f"save_json: Errore durante il salvataggio del file JSON: {e}")

# Funzione principale per l'analisi del sentiment
def sentiment_analysis(input_file, output_file, model_name, device):
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
    results = []
    for idx, tweet in enumerate(tweets, start=1):
        logger.info(f"sentiment_analysis: Analisi del tweet {idx}/{len(tweets)}: {tweet['text']}")
        try:
            analysis = sentiment_pipeline(tweet["text"])[0]
            sentiment_label = analysis["label"].lower()
            sentiment_score = round(analysis["score"], 4)
            
            # Log del risultato dell'analisi
            logger.info(f"sentiment_analysis: Risultato analisi: sentiment='{sentiment_label}', score={sentiment_score}")
            
            results.append({
                "text": tweet["text"],
                "sentiment": sentiment_label,
                "score": sentiment_score,
                "date": tweet.get("date", "")
            })
        except Exception as e:
            logger.error(f"sentiment_analysis: Errore durante l'analisi del tweet: {e}")

    # Salvataggio dei risultati
    save_json(results, output_file)

# Esecuzione dello script
if __name__ == "__main__":
    logging.info(f"Current working directory: {os.getcwd()}")
    
    input_file = "./input_data/03_tweets_dati_cleaned.json"

    # Determina il dispositivo: GPU (0) se disponibile, altrimenti CPU (-1)
    if torch.cuda.is_available():
        device = 0  # Usa la prima GPU
        logger.info("MAIN: GPU rilevata. Il modello sarà caricato sulla GPU.")
    else:
        device = -1  # Usa la CPU
        logger.info("MAIN: GPU non rilevata. Il modello sarà caricato sulla CPU.")

    # Modelli da utilizzare
    models = {
        "MilaNLProc/feel-it-italian-sentiment": "./output_data/04_tweets_sentiment_analysis_feel_it.json",
        "neuraly/bert-base-italian-cased-sentiment": "./output_data/04_tweets_sentiment_analysis_bert_italian.json"
    }

    for model_name, output_file in models.items():
        logger.info(f"MAIN: Inizio analisi con il modello: {model_name}")
        sentiment_analysis(input_file, output_file, model_name, device)
        logger.info(f"MAIN: Analisi completata con il modello: {model_name}. Risultati salvati in {output_file}.")

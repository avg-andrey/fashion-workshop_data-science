# cli_app_migrated.py

import logging
import sys
import os
from pathlib import Path
from openai import OpenAI
import threading

# Archiviazione sicura dei log
log_messages = []
log_lock = threading.Lock()

# Archiviazione sicura del conteggio dei token
token_counts = []
token_lock = threading.Lock()

class ListHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        with log_lock:
            log_messages.append(log_entry)
            # Limitazione della dimensione della lista dei log a 1000 messaggi
            if len(log_messages) > 1000:
                log_messages.pop(0)

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
handler = ListHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(handler)

# Lettura della chiave API da un file esterno
def load_api_key():
    try:
        # Determinare il percorso assoluto del file api_key.txt relativo allo script
        script_dir = Path(__file__).parent
        filepath = script_dir / "app" / "api_key.txt"
        with open(filepath, "r") as file:
            api_key = file.read().strip()
            return api_key
    except Exception as e:
        logging.error(f"Impossibile caricare la chiave API: {e}")
        sys.exit(1)

# Funzione per interagire con il modello ChatCompletion
def chat_with_model(client, prompt, model):
    try:
        logging.info(f"Invio richiesta al modello (Chat): {model}, prompt: {prompt}")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        logging.info(f"Risposta dal modello (Chat): {response}")

        # Estrazione dell'uso dei token
        total_tokens = response.usage.total_tokens
        with token_lock:
            token_counts.append(total_tokens)
            if len(token_counts) > 1000:
                token_counts.pop(0)

        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Errore durante la richiesta al modello (Chat): {e}")
        return f"Errore: {e}"

# Funzione per interagire con il modello Completion
def completion_with_model(client, prompt, model):
    try:
        logging.info(f"Invio richiesta al modello (Completion): {model}, prompt: {prompt}")
        response = client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=150
        )
        logging.info(f"Risposta dal modello (Completion): {response}")

        # Estrazione dell'uso dei token
        total_tokens = response.usage.total_tokens
        with token_lock:
            token_counts.append(total_tokens)
            if len(token_counts) > 1000:
                token_counts.pop(0)

        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Errore durante la richiesta al modello (Completion): {e}")
        return f"Errore: {e}"

# Funzione per ottenere la lista dei modelli disponibili
def get_available_model_names(client):
    try:
        logging.info("Richiesta della lista dei modelli disponibili...")
        models = client.models.list()
        model_names = [model.id for model in models.data]  # Accessing .data for model names
        logging.info(f"Lista dei modelli disponibili: {model_names}")
        return model_names
    except Exception as e:
        logging.error(f"Errore nell'ottenere la lista dei modelli: {e}")
        return []

# Funzione per leggere il prompt da un file
def read_prompt(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            prompt = file.read().strip()
            logging.info(f"Prompt letto dal file {filepath}.")
            return prompt
    except Exception as e:
        logging.error(f"Impossibile leggere il file del prompt {filepath}: {e}")
        sys.exit(1)

# Funzione per scrivere la risposta in un file
def write_response(response, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(response)
            logging.info(f"Risposta scritta nel file {filepath}.")
    except Exception as e:
        logging.error(f"Impossibile scrivere la risposta nel file {filepath}: {e}")
        sys.exit(1)

# Funzione principale CLI
def main(args):
    logging.info(f"Current working directory: {os.getcwd()}")

    # Caricamento della chiave API
    api_key = load_api_key()

    # Inizializzazione del client OpenAI
    client = OpenAI(api_key=api_key)

    # Ottenere la lista dei modelli disponibili
    available_models = get_available_model_names(client)
    if not available_models:
        logging.error("Nessun modello disponibile. Terminazione dell'esecuzione.")
        sys.exit(1)

    # Determinare il modello da utilizzare
    model = args.model if args.model else "gpt-3.5-turbo"
    if model not in available_models:
        logging.warning(f"Modello '{model}' non disponibile. Verrà utilizzato il modello predefinito.")
        model = available_models[0]

    logging.info(f"Modello utilizzato: {model}")

    # Leggere il prompt dal file
    prompt = read_prompt(args.input_file)

    # Determinare il tipo di modello e chiamare la funzione corrispondente
    if model.startswith("gpt-") and "turbo" in model:
        response = chat_with_model(client, prompt, model)
    elif model.startswith("gpt-") and ("instruct" in model or "text" in model):
        response = completion_with_model(client, prompt, model)
    else:
        logging.error(f"Il modello '{model}' non è supportato da questo script.")
        sys.exit(1)

    # Scrivere la risposta nel file
    write_response(response, args.output_file)

    # Inoltre: visualizzazione delle informazioni sui token
    total_tokens_used = sum(token_counts)
    logging.info(f"Numero totale di token utilizzati: {total_tokens_used}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Utility CLI per interagire con l'API di OpenAI.")
    parser.add_argument(
        "--input_file",
        type=str,
        default="gpt_request_sample.txt",
        help="Percorso del file con il prompt (predefinito: gpt_request_sample.txt)"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="gpt_request_output.txt",
        help="Percorso del file per salvare la risposta (predefinito: gpt_request_output.txt)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="ID del modello da utilizzare (predefinito: gpt-3.5-turbo)"
    )

    args = parser.parse_args()
    main(args)

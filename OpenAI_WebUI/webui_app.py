# webui_app.py

from flask import Flask, redirect
import gradio as gr
import threading
import asyncio
import openai
import logging
import plotly.graph_objs as go
from pathlib import Path
import sys

# Memoria thread-safe per i log
log_messages = []
log_lock = threading.Lock()

# Memoria thread-safe per il conteggio dei token
token_counts = []
token_lock = threading.Lock()

class ListHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        with log_lock:
            log_messages.append(log_entry)
            # Limita la dimensione della lista dei log a 1000 messaggi
            if len(log_messages) > 1000:
                log_messages.pop(0)

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
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
            openai.api_key = api_key
            logging.info("Chiave API caricata con successo dal file.")
            return api_key
    except Exception as e:
        logging.error(f"Impossibile caricare la chiave API: {e}")
        sys.exit(1)

# Chiamata alla funzione di caricamento della chiave API
load_api_key()

app = Flask(__name__)

# Funzione per comunicare con il modello OpenAI usando ChatCompletion
def chat_with_model(prompt, model):
    try:
        logging.info(f"Invio richiesta al modello (Chat): {model}, prompt: {prompt}")
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        logging.info(f"Risposta dal modello (Chat): {response}")

        # Estrazione del conteggio dei token
        total_tokens = response['usage']['total_tokens']
        with token_lock:
            token_counts.append(total_tokens)
            # Opzionalmente limita la dimensione di token_counts
            if len(token_counts) > 1000:
                token_counts.pop(0)

        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Errore durante la richiesta al modello OpenAI (Chat): {e}")
        return f"Errore: {e}"

# Funzione per comunicare con il modello OpenAI usando Completion
def completion_with_model(prompt, model):
    try:
        logging.info(f"Invio richiesta al modello (Completion): {model}, prompt: {prompt}")
        response = openai.Completion.create(
            model=model,
            prompt=prompt
        )
        logging.info(f"Risposta dal modello (Completion): {response}")

        # Estrazione del conteggio dei token
        total_tokens = response['usage']['total_tokens']
        with token_lock:
            token_counts.append(total_tokens)
            # Opzionalmente limita la dimensione di token_counts
            if len(token_counts) > 1000:
                token_counts.pop(0)

        return response['choices'][0]['text'].strip()
    except Exception as e:
        logging.error(f"Errore durante la richiesta al modello OpenAI (Completion): {e}")
        return f"Errore: {e}"

# Funzione per ottenere la lista dei modelli disponibili
def get_available_model_names():
    try:
        logging.info("Richiesta della lista dei modelli disponibili...")
        models = openai.Model.list()
        model_names = [model["id"] for model in models["data"]]
        logging.info(f"Lista dei modelli disponibili: {model_names}")
        return model_names
    except Exception as e:
        logging.error(f"Errore nel recupero della lista dei modelli: {e}")
        return []

# Funzione per ottenere i log
def get_logs(max_lines=100):
    """Restituisce le ultime linee di log in ordine inverso."""
    with log_lock:
        # Inverte la lista dei log e prende le ultime max_lines linee
        return "\n".join(reversed(log_messages[-max_lines:]))

# Funzione per generare il grafico dell'uso dei token
def get_token_plot():
    with token_lock:
        tokens = token_counts.copy()
    if not tokens:
        # Restituisce un grafico vuoto
        fig = go.Figure()
        fig.update_layout(
            title="Utilizzo dei Token nel Tempo",
            xaxis_title="Richiesta",
            yaxis_title="Token",
            xaxis=dict(tickmode='linear')
        )
        return fig
    x = list(range(1, len(tokens) + 1))
    y = tokens
    fig = go.Figure([go.Bar(x=x, y=y, marker_color='indigo')])
    fig.update_layout(
        title="Utilizzo dei Token nel Tempo",
        xaxis_title="Richiesta",
        yaxis_title="Token",
        xaxis=dict(tickmode='linear')
    )
    return fig

# Interfaccia Gradio
def interface_fn(prompt, model_id):
    try:
        if model_id.startswith("gpt-") and "turbo" in model_id:
            response_content = chat_with_model(prompt, model_id)
        elif model_id.startswith("gpt-") and "instruct" in model_id:
            response_content = completion_with_model(prompt, model_id)
        else:
            response_content = f"Il modello '{model_id}' non è supportato in questa interfaccia."
        
        # Genera il grafico dell'uso dei token
        plot_fig = get_token_plot()
        
        return response_content, plot_fig
    except Exception as e:
        logging.error(f"Errore in interface_fn: {e}")
        return f"Errore: {e}", get_token_plot()

# Funzione per aggiornare la lista dei modelli
def refresh_models():
    try:
        logging.info("Funzione refresh_models chiamata.")
        available_models = get_available_model_names()
        logging.info(f"Modelli disponibili dopo l'aggiornamento: {available_models}")

        # Determina il modello predefinito
        default_model = "gpt-3.5-turbo"
        if default_model in available_models:
            selected_model = default_model
            logging.info(f"Modello predefinito '{default_model}' trovato dopo l'aggiornamento.")
        elif available_models:
            selected_model = available_models[0]
            logging.info(f"Modello predefinito '{default_model}' non trovato. Impostato il primo modello disponibile: {selected_model}")
        else:
            selected_model = None
            logging.warning("La lista dei modelli è vuota dopo l'aggiornamento. Impossibile impostare un modello predefinito.")

        # Genera il grafico dell'uso dei token
        plot_fig = get_token_plot()

        return gr.Dropdown.update(choices=available_models, value=selected_model), get_logs(), plot_fig
    except Exception as e:
        logging.error(f"Errore nella funzione refresh_models: {e}")
        return gr.Dropdown.update(choices=[], value=None), get_logs(), get_token_plot()

with gr.Blocks() as demo:
    # Blocchi superiori: selezione del modello e invio delle richieste
    with gr.Row():
        model_dropdown = gr.Dropdown(choices=[], label="Seleziona Modello")
        refresh_button = gr.Button("Aggiorna Lista Modelli")

    with gr.Row():
        user_input = gr.Textbox(label="Il Tuo Prompt")
        submit_btn = gr.Button("Invia")

    with gr.Row():
        output = gr.Textbox(label="Risposta del Modello")

    # Blocchi inferiori: console dei log
    with gr.Row():
        log_output = gr.Textbox(label="Console dei Log", lines=20, interactive=False)
        refresh_log_btn = gr.Button("Aggiorna Log")

    # Nuovo blocco: Grafico dell'uso dei token
    with gr.Row():
        token_plot = gr.Plot(label="Grafico Utilizzo Token")

    # Assegna le funzioni ai pulsanti
    refresh_button.click(
        refresh_models, 
        inputs=[], 
        outputs=[model_dropdown, log_output, token_plot]
    )
    submit_btn.click(
        interface_fn, 
        inputs=[user_input, model_dropdown], 
        outputs=[output, token_plot]
    )
    refresh_log_btn.click(
        get_logs, 
        inputs=[], 
        outputs=log_output
    )

    # Inizializza i modelli disponibili e imposta il valore predefinito
    initial_models = get_available_model_names()
    logging.info(f"Modelli disponibili: {initial_models}")

    default_model = "gpt-3.5-turbo"
    if default_model in initial_models:
        selected_model = default_model
        logging.info(f"Modello predefinito '{default_model}' trovato.")
    elif initial_models:
        selected_model = initial_models[0]
        logging.info(f"Modello predefinito '{default_model}' non trovato. Impostato il primo modello disponibile: {selected_model}")
    else:
        selected_model = None
        logging.warning("La lista dei modelli è vuota. Impossibile impostare un modello predefinito.")

    # Aggiorna il Dropdown con il valore predefinito
    model_dropdown.update(choices=initial_models, value=selected_model)

    # Imposta i log nell'interfaccia
    log_output.value = get_logs()

    # Imposta il grafico dei token nell'interfaccia
    token_plot.update(get_token_plot())

# Esegui Gradio con un ciclo di eventi asyncio
def run_gradio():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.info("Avvio di Gradio...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

@app.route("/")
def home():
    logging.info("Reindirizzamento all'interfaccia Gradio.")
    return redirect("http://127.0.0.1:7860")

if __name__ == "__main__":
    logging.info("Avvio dell'applicazione Flask...")
    # Avvia Gradio in un thread separato
    threading.Thread(target=run_gradio, daemon=True).start()
    # Avvia Flask
    app.run(port=5000)

# webui_app.py

import os
from flask import Flask, redirect
import gradio as gr
import sys
import logging
import http.client
import threading
import asyncio
import traceback
import plotly.graph_objs as go
from pathlib import Path
from openai import OpenAI

# Enable HTTP request logging
http.client.HTTPConnection.debuglevel = 1

# Configure logging for HTTP requests
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("http.client").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("gradio").setLevel(logging.DEBUG)

# Output Gradio and Python information
print("Gradio version:", gr.__version__)
print("Gradio location:", gr.__file__)
print("Python version:", sys.version)
print("Python executable:", sys.executable)

# Thread-safe storage for logs
log_messages = []
log_lock = threading.Lock()

# Thread-safe storage for token counts
token_counts = []
token_lock = threading.Lock()

class ListHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        with log_lock:
            log_messages.append(log_entry)
            # Limit log size to 1000 messages
            if len(log_messages) > 1000:
                log_messages.pop(0)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
handler = ListHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(handler)

# Load API key from environment variable or external file
def load_api_key():
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Determine the absolute path to the api_key.txt file relative to the script
            script_dir = Path(__file__).parent
            filepath = script_dir / "app" / "api_key.txt"
            with open(filepath, "r") as file:
                api_key = file.read().strip()
        if not api_key:
            raise ValueError("API key is empty.")
        logging.info("API key successfully loaded.")
        return api_key
    except Exception as e:
        logging.error(f"Failed to load API key: {e}")
        sys.exit(1)

# Call the API key loading function
api_key = load_api_key()

# Initialize OpenAI client
try:
    client = OpenAI(
        api_key=api_key
    )
    logging.info("OpenAI client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI client: {e}")
    sys.exit(1)

app = Flask(__name__)

# Function to communicate with OpenAI's ChatCompletion
def chat_with_model(prompt, model):
    try:
        logging.info(f"Sending request to model (Chat): {model}, prompt: {prompt}")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        logging.info(f"Response from model (Chat): {response}")

        # Extract token count
        total_tokens = response.usage.total_tokens
        with token_lock:
            token_counts.append(total_tokens)
            if len(token_counts) > 1000:
                token_counts.pop(0)

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error during OpenAI Chat request: {e}")
        return f"Error: {e}"

# Function to communicate with OpenAI's Completion
def completion_with_model(prompt, model):
    try:
        logging.info(f"Sending request to model (Completion): {model}, prompt: {prompt}")
        response = client.completions.create(
            model=model,
            prompt=prompt
        )
        logging.info(f"Response from model (Completion): {response}")

        # Extract token count
        total_tokens = response.usage.total_tokens
        with token_lock:
            token_counts.append(total_tokens)
            if len(token_counts) > 1000:
                token_counts.pop(0)

        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error during OpenAI Completion request: {e}")
        return f"Error: {e}"

# Function to get the list of available models
def get_available_model_names():
    try:
        logging.info("Requesting list of available models...")
        models = client.models.list()
        model_names = [model.id for model in models.data]  # Make sure you use .data
        logging.info(f"Available models: {model_names}")
        return model_names
    except Exception as e:
        logging.error(f"Error fetching model list: {e}")
        return []

# Function to retrieve logs
def get_logs(max_lines=100):
    """Returns the latest log lines in reverse order."""
    with log_lock:
        return "\n".join(reversed(log_messages[-max_lines:]))

# Function to generate the token usage plot
def get_token_plot():
    with token_lock:
        tokens = token_counts.copy()
    if not tokens:
        fig = go.Figure()
        fig.update_layout(
            title="Token Usage Over Time",
            xaxis_title="Request",
            yaxis_title="Tokens",
            xaxis=dict(tickmode='linear')
        )
        return fig
    x = list(range(1, len(tokens) + 1))
    y = tokens
    fig = go.Figure([go.Bar(x=x, y=y, marker_color='indigo')])
    fig.update_layout(
        title="Token Usage Over Time",
        xaxis_title="Request",
        yaxis_title="Tokens",
        xaxis=dict(tickmode='linear')
    )
    return fig

# Gradio interface function
def interface_fn(prompt, model_id):
    try:
        if model_id.startswith("gpt-") and "turbo" in model_id:
            response_content = chat_with_model(prompt, model_id)
        elif model_id.startswith("gpt-") and "instruct" in model_id:
            response_content = completion_with_model(prompt, model_id)
        else:
            response_content = f"The model '{model_id}' is not supported in this interface."
        
        plot_fig = get_token_plot()
        
        return response_content, plot_fig
    except Exception as e:
        logging.error(f"Error in interface_fn: {e}")
        return f"Error: {e}", get_token_plot()

# Function to refresh the list of models
def refresh_models():
    try:
        logging.info("refresh_models function called.")
        available_models = get_available_model_names()
        logging.info(f"Available models after refresh: {available_models}")

        # Determine the default model
        default_model = "gpt-3.5-turbo"
        if default_model in available_models:
            selected_model = default_model
            logging.info(f"Default model '{default_model}' found after refresh.")
        elif available_models:
            selected_model = available_models[0]
            logging.info(f"Default model '{default_model}' not found. Set to first available model: {selected_model}")
        else:
            selected_model = None
            logging.warning("Model list is empty after refresh. Cannot set a default model.")

        plot_fig = get_token_plot()

        return (
            gr.update(choices=available_models, value=selected_model),  # Update Dropdown
            get_logs(),
            plot_fig
        )
    except Exception as e:
        logging.error(f"Error in refresh_models: {e}")
        return (
            gr.update(choices=[], value=None),  # Update Dropdown in case of error
            get_logs(),
            get_token_plot()
        )

with gr.Blocks() as demo:
    # Top section: model selection and prompt submission
    with gr.Row():
        initial_models = get_available_model_names()
        default_model = "gpt-3.5-turbo" if "gpt-3.5-turbo" in initial_models else (initial_models[0] if initial_models else None)

        model_dropdown = gr.Dropdown(choices=initial_models, value=default_model, label="Select Model")
        refresh_button = gr.Button("Refresh Model List")

    with gr.Row():
        user_input = gr.Textbox(label="Your Prompt")
        submit_btn = gr.Button("Submit")

    with gr.Row():
        output = gr.Textbox(label="Model Response")

    # Bottom section: log console and token chart
    with gr.Row():
        log_output = gr.Textbox(label="Log Console", lines=20, interactive=False, value=get_logs())
        refresh_log_btn = gr.Button("Refresh Logs")

    with gr.Row():
        token_plot = gr.Plot(label="Token Usage Chart")

    # Button functions
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

# Run Gradio
def run_gradio():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.info("Starting Gradio...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

if __name__ == "__main__":
    logging.info("Starting Flask application...")
    threading.Thread(target=run_gradio, daemon=True).start()
    app.run(port=5000)

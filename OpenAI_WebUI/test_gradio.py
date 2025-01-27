# test_gradio.py

import gradio as gr
import sys
import logging
import http.client
import traceback

# Configure global logging
logging.basicConfig(
    level=logging.DEBUG,  # Logging level: DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to console
    ],
)
logger = logging.getLogger()

# Enable HTTP request debugging
http.client.HTTPConnection.debuglevel = 1

# Logging for urllib3 (HTTP requests by Gradio)
logging.getLogger("http.client").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("gradio").setLevel(logging.DEBUG)

# Output Gradio and Python information
logger.debug(f"Gradio version: {gr.__version__}")
logger.debug(f"Gradio location: {gr.__file__}")
logger.debug(f"Python version: {sys.version}")
logger.debug(f"Python executable: {sys.executable}")

# Function with detailed logging
def greet(name):
    return f"Hello, {name}!"

# Create Gradio interface with debugging
try:
    with gr.Blocks() as demo:
        logger.debug("Initializing Gradio interface...")

        name_input = gr.Textbox(label="Your Name", placeholder="Enter your name here...")
        greet_button = gr.Button("Submit")
        output = gr.Textbox(label="Greeting")

        logger.debug("Setting up button click event...")
        greet_button.click(fn=greet, inputs=name_input, outputs=output)

    logger.debug("Launching Gradio app...")
    demo.launch(debug=True)  # Enable debug mode
except Exception as e:
    logger.critical(f"Critical error while launching the app: {traceback.format_exc()}")

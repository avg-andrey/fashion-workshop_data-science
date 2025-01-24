
# OpenAI_WebUI

A simple demo of OpenAI's API access via a WebUI, built using Flask and Gradio. This application allows users to interact with OpenAI models (e.g., GPT-3.5-turbo) and provides a visualization of token usage per request.

---

## Features

- **Interactive WebUI**: Easily interact with OpenAI's API via a Gradio-based user interface.
- **Model Selection**: Dynamically select from available OpenAI models.
- **Token Usage Visualization**: Track and visualize the number of tokens used for each request in a bar chart.
- **Log Console**: View logs of API interactions and debug information in real-time.
- **Flask Integration**: Redirects to Gradio from a Flask app for streamlined usage.

---

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key stored in a file named `api_key.txt`

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/OpenAI_WebUI.git
   cd OpenAI_WebUI
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your OpenAI API key:
   - Create a file named `api_key.txt` in the root directory.
   - Paste your OpenAI API key into this file.

4. Run the application:
   ```bash
   python webui_app.py
   ```

5. Access the WebUI:
   - Open your browser and navigate to `http://127.0.0.1:5000`.

---

## File Structure

```
OpenAI_WebUI/
├── /app/api_key.txt          # Your OpenAI API key (required)
├── webui_app.py         # Main application file
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Usage

1. **Run the App**:
   Start the application using `python webui_app.py`.

2. **Interact with OpenAI Models**:
   - Select an available model from the dropdown menu.
   - Enter your prompt in the text box.
   - View the response and associated token usage graph.

3. **Visualize Token Usage**:
   - The token usage graph updates with each new request.
   - Compare token counts across requests in a bar chart.

4. **Refresh Models or Logs**:
   - Use the "Refresh Models List" button to load the latest available models.
   - Use the "Refresh Logs" button to view updated logs.

---

## Dependencies

This project uses the following libraries:

- **Flask**: For backend routing.
- **Gradio**: For building the user interface.
- **Plotly**: For generating the token usage graph.
- **OpenAI**: For interacting with OpenAI's API.
- **Logging**: For real-time logging and debugging.

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## Notes

- Ensure the `api_key.txt` file is present and contains a valid OpenAI API key.
- The token usage graph may show a delay for very large requests due to API response times.
- This project is for demonstration purposes only and not intended for production use.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Thanks to OpenAI for their amazing APIs.
- This demo was created for educational purposes as part of a course on Python and API integrations.

---

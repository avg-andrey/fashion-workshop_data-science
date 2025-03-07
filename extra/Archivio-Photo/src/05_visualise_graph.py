# visualise_graph.py

"""
Script: visualise_graph.py

Descrizione:
Questo script genera visualizzazioni statiche e interattive di un grafo basato sui concetti estratti dal dataset sulla moda.
Il grafo rappresenta parole chiave come nodi e le loro connessioni come archi ponderati.
Le visualizzazioni aiutano ad analizzare le connessioni tra i termini attraverso diversi layout grafici.

-------------------------------------------------------
Tipologie di grafici generati:
1. **Grafici statici** (salvati in PNG):
   - `spring_layout`: Basato su forze repulsive tra i nodi, simula una disposizione fisica naturale.
   - `kamada_kawai_layout`: Ottimizza la disposizione dei nodi minimizzando la distanza tra quelli connessi.
   - `circular_layout`: Dispone i nodi in un cerchio, utile per evidenziare le connessioni.

2. **Grafico interattivo** (salvato in HTML con Pyvis):
   - Permette di esplorare il grafo con zoom e spostamenti dinamici.
   - Mostra informazioni su ogni nodo al passaggio del mouse.

-------------------------------------------------------
Struttura dei file di output:
- **PNG**: `output-data/graph-{layout}_{timestamp}.png` (grafici statici per ogni layout).
- **HTML**: `output-data/interactive_graph_{timestamp}.html` (grafico interattivo).

-------------------------------------------------------
Flusso di esecuzione:
1. **Caricamento dei dati**: Legge `graph-data.json` con parole chiave e relazioni.
2. **Costruzione del grafo**: Usa NetworkX per creare la struttura dei nodi e degli archi.
3. **Applicazione dei layout**:
   - Calcola posizioni dei nodi per ogni layout.
   - Registra la distanza media tra i nodi per analizzare la disposizione.
4. **Generazione delle visualizzazioni**:
   - Disegna e salva i grafici statici in PNG.
   - Crea un grafico interattivo con Pyvis e salva in HTML.

-------------------------------------------------------
Parametri configurabili (`config/graph_setup.json`):
- `"spring_layout"`: Configurazione del layout a molla (`k`, `seed`, `node_size_multiplier`, `edge_alpha`).
- `"kamada_kawai_layout"`: Configurazione del layout Kamada-Kawai (`scale`).
- `"circular_layout"`: Configurazione del layout circolare.
- `"interactive_graph"`: Configurazione del grafico interattivo (dimensioni, fisica, parametri del layout dinamico).

Prerequisiti:
- Il dataset `graph-data.json` deve essere stato generato precedentemente dallo script `build_graph_data.py`.
- Le librerie richieste (`networkx`, `matplotlib`, `pyvis`).

Output:
- PNG: Visualizzazioni statiche per ogni layout.
- HTML: Grafico interattivo navigabile.

Autore: [Inserisci il tuo nome]
Data: [Inserisci la data]
"""

import json
import logging
from pathlib import Path
import datetime
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

# Configurazione del logging (impostazione dei log)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Percorsi dei file (path settings)
INPUT_FILE = Path("input-data/graph-data.json")
OUTPUT_DIR = Path("output-data/")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SETTINGS_FILE = Path("config/graph_setup.json")

def load_settings(settings_path):
    """Carica le impostazioni dal file JSON."""
    try:
        with open(settings_path, "r", encoding="utf-8") as file:
            settings = json.load(file)
        logging.info(f"Impostazioni caricate da {settings_path}")
        return settings
    except Exception as e:
        logging.error(f"Errore nel caricamento delle impostazioni: {e}")
        return {}

def visualize_static_graph(settings):
    """
    Visualizza grafici statici dei concetti con diversi layout, utilizzando le impostazioni.
    I grafici vengono salvati come file PNG con timestamp nel nome.
    """
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            graph_data = json.load(file)
        keywords = graph_data.get("keywords", {})
        relations = graph_data.get("relations", [])
        logging.info(f"Caricate {len(keywords)} parole chiave e {len(relations)} relazioni.")

        # Costruzione del grafo usando NetworkX
        G = nx.Graph()
        for word, freq in keywords.items():
            G.add_node(word, size=freq)
        for rel in relations:
            w1, w2 = rel["words"]
            count = rel["count"]
            G.add_edge(w1, w2, weight=count)
        logging.info(f"Il grafo contiene {G.number_of_nodes()} nodi e {G.number_of_edges()} archi.")

        # Definizione dei layout da utilizzare
        layouts = {}
        for layout_name in ["spring_layout", "kamada_kawai_layout", "circular_layout"]:
            layout_settings = settings.get(layout_name, {})
            params = layout_settings.get("params", {})
            if layout_name == "spring_layout":
                layouts[layout_name] = nx.spring_layout(G, **params)
            elif layout_name == "kamada_kawai_layout":
                layouts[layout_name] = nx.kamada_kawai_layout(G, **params)
            elif layout_name == "circular_layout":
                layouts[layout_name] = nx.circular_layout(G, **params)

        # Calcolo e log della distanza media tra nodi per ogni layout
        for layout_name, pos in layouts.items():
            distances = []
            nodes = list(pos.keys())
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    x1, y1 = pos[nodes[i]]
                    x2, y2 = pos[nodes[j]]
                    dist = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
                    distances.append(dist)
            if distances:
                avg_distance = sum(distances) / len(distances)
                logging.debug(f"Layout {layout_name}: distanza media tra nodi = {avg_distance:.4f}")
            else:
                logging.debug(f"Layout {layout_name}: non ci sono nodi per calcolare la distanza.")

        # Creazione di timestamp per i nomi dei file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Visualizzazione e salvataggio dei grafici statici per ogni layout
        for layout_name, pos in layouts.items():
            layout_settings = settings.get(layout_name, {})
            figure_size = tuple(layout_settings.get("figure_size", [12, 12]))
            node_size_multiplier = layout_settings.get("node_size_multiplier", 100)
            edge_alpha = layout_settings.get("edge_alpha", 0.4)
            edge_width = layout_settings.get("edge_width", 1)
            font_size = layout_settings.get("font_size", 10)
            title_font_size = layout_settings.get("title_font_size", 14)
            dpi = layout_settings.get("dpi", 300)
            bbox_inches = layout_settings.get("bbox_inches", "tight")

            plt.figure(figsize=figure_size)
            plt.title(f"Grafico dei concetti ({layout_name})", fontsize=title_font_size)

            # Calcolo delle dimensioni dei nodi in base alla frequenza
            node_sizes = [G.nodes[n]["size"] * node_size_multiplier for n in G.nodes]
            nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="lightblue", edgecolors="black")
            nx.draw_networkx_edges(G, pos, alpha=edge_alpha, width=edge_width, edge_color="black")
            nx.draw_networkx_labels(G, pos, font_size=font_size, font_family="sans-serif")

            output_image_path = OUTPUT_DIR / f"graph-{layout_name}_{timestamp}.png"
            plt.savefig(output_image_path, dpi=dpi, bbox_inches=bbox_inches)
            plt.close()
            logging.info(f"Grafico statico salvato: {output_image_path}")

        return G

    except Exception as e:
        logging.error(f"Errore nella visualizzazione del grafico statico: {e}")


def calculate_node_size_pyvis(G, frequency, min_size=10, max_size=50):
    """
    Calcola la dimensione del nodo per Pyvis in base alla frequenza.
    """
    if not G.nodes:
        return min_size

    min_frequency = min(attr['size'] for _, attr in G.nodes(data=True))
    max_frequency = max(attr['size'] for _, attr in G.nodes(data=True))

    if max_frequency == min_frequency:
        return max_size

    normalized_frequency = (frequency - min_frequency) / (max_frequency - min_frequency)
    return min_size + (max_size - min_size) * normalized_frequency


def visualize_interactive_graph(G, settings):
    """
    Crea un grafico interattivo utilizzando Pyvis, applicando le impostazioni fornite.
    Il grafico interattivo viene salvato in formato HTML con timestamp nel nome.
    """
    interactive_settings = settings.get("interactive_graph", {})
    height = interactive_settings.get("height", "800px")
    width = interactive_settings.get("width", "100%")

    nt = Network(height=height, width=width, notebook=False, directed=False, cdn_resources="remote")

    # Aggiunta dei nodi con dimensioni normalizzate
    for node, attr in G.nodes(data=True):
        frequency = attr.get("size", 1)
        node_size = calculate_node_size_pyvis(G, frequency)
        label = f"{node}\n({frequency})"
        nt.add_node(node, label=label, title=f"Frequenza: {frequency}", size=node_size)

    # Aggiunta delle relazioni (archi)
    for source, target, attr in G.edges(data=True):
        weight = attr.get("weight", 1)
        nt.add_edge(source, target, value=weight, title=f"Peso: {weight}")

    if len(G.edges) == 0:
        logging.warning("ATTENZIONE: Il grafo non contiene relazioni. Verifica i dati in input.")

    # Impostazioni di fisica e pannello di configurazione
    physics_options = {
        "physics": {
            "enabled": True,
            "barnesHut": {
                "gravitationalConstant": -80000,
                "centralGravity": 0.3,
                "springLength": 200,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 1
            },
            "minVelocity": 0.75,
            "solver": "barnesHut",
            "stabilization": {"iterations": 150}
        },
        "configure": {
            "enabled": True,
            "filter": ["physics", "nodes", "edges"]
        },
        "height": height,
        "width": width
    }

    nt.set_options(json.dumps(physics_options))

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    interactive_output = OUTPUT_DIR / f"interactive_graph_{timestamp}.html"
    nt.save_graph(str(interactive_output))

    # Aggiunta di CSS e JS personalizzati per mostrare il pannello di controllo
    custom_css = """
    <style>
        body {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: flex-start;
            height: 100vh;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        #mynetwork {
            flex: 1 1 75%;
            height: 100vh;
            margin-right: 10px;
        }
        .vis-configuration-wrapper {
            flex: 1 1 25%;
            height: 100vh;
            overflow-y: auto;
            background: white;
            border-left: 1px solid #ccc;
            padding: 10px;
            z-index: 999;
        }
    </style>
    """
    custom_js = """
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var configWrapper = document.querySelector('.vis-configuration-wrapper');
            if (configWrapper) {
                document.body.appendChild(configWrapper);
            }
        });
    </script>
    """

    with open(interactive_output, "r", encoding="utf-8") as file:
        html_content = file.read()

    html_content = html_content.replace('</head>', f'{custom_css}</head>')
    html_content = html_content.replace('</body>', f'{custom_js}</body>')

    with open(interactive_output, "w", encoding="utf-8") as file:
        file.write(html_content)

    logging.info(f"Grafico interattivo salvato: {interactive_output}")


def main():
    settings = load_settings(SETTINGS_FILE)
    # Generazione dei grafici statici e ottenimento del grafo costruito G
    G = visualize_static_graph(settings)
    # Generazione del grafico interattivo basato sullo stesso grafo
    visualize_interactive_graph(G, settings)

if __name__ == "__main__":
    main()

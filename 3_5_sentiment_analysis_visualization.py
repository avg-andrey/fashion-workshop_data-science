# 3_5_sentiment_analysis_visualization.py

import json  # Libreria per la manipolazione di dati JSON
import logging  # Libreria per il logging delle operazioni
import os  # Libreria per interagire con il sistema operativo
import sys  # Libreria per interagire con il sistema (es. uscita dallo script)
from datetime import datetime  # Libreria per lavorare con date e orari
import argparse  # Libreria per gestire gli argomenti da linea di comando
import string  # Libreria per operazioni con stringhe e punteggiatura

import pandas as pd  # Libreria per la manipolazione e analisi dei dati
import matplotlib.pyplot as plt  # Libreria per la creazione di grafici
import seaborn as sns  # Libreria per la visualizzazione statistica dei dati
from wordcloud import WordCloud  # Libreria per la creazione di word cloud
from collections import Counter  # Libreria per il conteggio degli elementi
from sklearn.feature_extraction.text import TfidfVectorizer  # Libreria per l'estrazione di caratteristiche dai testi

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SentimentVisualization')  # Creazione di un logger specifico per la visualizzazione dei sentimenti


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
        logger.error(f"load_json: Errore durante il caricamento del file JSON {file_path}: {e}")
        return []


def convert_to_dataframe(data):
    """
    Converte una lista di dizionari in un DataFrame pandas.

    Args:
        data (list): Lista di dizionari contenenti i dati.

    Returns:
        pandas.DataFrame: DataFrame creato dai dati forniti. Ritorna un DataFrame vuoto in caso di errore.
    """
    try:
        df = pd.DataFrame(data)
        logger.info(f"convert_to_dataframe: Convertito in DataFrame con {df.shape[0]} righe e {df.shape[1]} colonne.")
        return df
    except Exception as e:
        logger.error(f"convert_to_dataframe: Errore durante la conversione in DataFrame: {e}")
        return pd.DataFrame()


def create_output_folder(base_folder_path):
    """
    Crea la cartella di output principale e una sottocartella temporanea con timestamp.

    Args:
        base_folder_path (str): Percorso della cartella di output principale.

    Returns:
        str: Percorso della sottocartella temporanea creata.

    Raises:
        SystemExit: Se si verifica un errore durante la creazione delle cartelle.
    """
    try:
        # Crea la cartella base se non esiste
        os.makedirs(base_folder_path, exist_ok=True)
        logger.info(f"create_output_folder: Cartella di output verificata o creata: {base_folder_path}.")

        # Crea una sottocartella con data e ora corrente
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_folder = os.path.join(base_folder_path, timestamp)
        os.makedirs(temp_folder, exist_ok=True)
        logger.info(f"create_output_folder: Sottocartella temporanea creata: {temp_folder}.")

        return temp_folder
    except Exception as e:
        logger.error(f"create_output_folder: Errore durante la creazione delle cartelle {base_folder_path}: {e}")
        sys.exit(1)


def extract_model_name(file_path):
    """
    Estrae il nome del modello dal nome del file.

    Args:
        file_path (str): Percorso del file JSON contenente i risultati dell'analisi del sentiment.

    Returns:
        str: Nome del modello estratto. Ritorna "unknown_model" se l'estrazione fallisce.
    """
    base_name = os.path.basename(file_path)
    # Esempio: "04_tweets_sentiment_analysis_feel_it.json" -> "feel_it"
    try:
        parts = base_name.split('_sentiment_analysis_')
        if len(parts) == 2:
            model_part = parts[1].split('.json')[0]
            return model_part
        else:
            return "unknown_model"
    except Exception as e:
        logger.error(f"extract_model_name: Errore nell'estrazione del nome del modello da {file_path}: {e}")
        return "unknown_model"


def plot_sentiment_distribution(df, output_folder, model_name):
    """
    Crea e salva un grafico a barre della distribuzione dei sentimenti.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti.
        output_folder (str): Percorso della cartella di output per salvare il grafico.
        model_name (str): Nome del modello per personalizzare il titolo del grafico.
    """
    try:
        sentiment_counts = df['sentiment'].value_counts()
        plt.figure(figsize=(8, 6))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='viridis')
        plt.title(f'Distribuzione dei Sentimenti - {model_name.capitalize()}')
        plt.xlabel('Sentimento')
        plt.ylabel('Conteggio')
        # Aggiunge il conteggio sopra ogni barra
        for index, value in enumerate(sentiment_counts.values):
            plt.text(index, value + max(sentiment_counts.values)*0.01, str(value), ha='center')
        output_filename = f'sentiment_distribution_{model_name}.png'
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path)
        plt.close()
        logger.info(f"plot_sentiment_distribution: Grafico salvato in {output_path}.")
    except Exception as e:
        logger.error(f"plot_sentiment_distribution: Errore nella creazione del grafico: {e}")


def plot_temporal_distribution(df, output_folder, model_name):
    """
    Crea e salva un grafico a linee della distribuzione temporale dei sentimenti.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti.
        output_folder (str): Percorso della cartella di output per salvare il grafico.
        model_name (str): Nome del modello per personalizzare il titolo del grafico.
    """
    try:
        df['date'] = pd.to_datetime(df['date'])
        temporal_counts = df.groupby(['date', 'sentiment']).size().reset_index(name='counts')
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=temporal_counts, x='date', y='counts', hue='sentiment', marker='o')
        plt.title(f'Distribuzione Temporale dei Sentimenti - {model_name.capitalize()}')
        plt.xlabel('Data')
        plt.ylabel('Conteggio')
        plt.legend(title='Sentimento')
        plt.tight_layout()
        output_filename = f'temporal_distribution_{model_name}.png'
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path)
        plt.close()
        logger.info(f"plot_temporal_distribution: Grafico salvato in {output_path}.")
    except Exception as e:
        logger.error(f"plot_temporal_distribution: Errore nella creazione del grafico: {e}")


def plot_wordclouds(df, output_folder, model_name):
    """
    Crea e salva word cloud per ciascun tipo di sentimento.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti.
        output_folder (str): Percorso della cartella di output per salvare le word cloud.
        model_name (str): Nome del modello per personalizzare il titolo delle word cloud.
    """
    try:
        sentiment_types = df['sentiment'].unique()
        for sentiment in sentiment_types:
            text = ' '.join(df[df['sentiment'] == sentiment]['text'].tolist())
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Parole Chiave Più Comuni - {sentiment.capitalize()} - {model_name.capitalize()}')
            output_filename = f'wordcloud_{sentiment}_{model_name}.png'
            output_path = os.path.join(output_folder, output_filename)
            plt.savefig(output_path)
            plt.close()
            logger.info(f"plot_wordclouds: Word cloud per '{sentiment}' salvata in {output_path}.")
    except Exception as e:
        logger.error(f"plot_wordclouds: Errore nella creazione delle word cloud: {e}")


def plot_sentiment_probabilities(df, output_folder, model_name):
    """
    Crea e salva un istogramma delle probabilità di sentiment.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti con i punteggi.
        output_folder (str): Percorso della cartella di output per salvare l'istogramma.
        model_name (str): Nome del modello per personalizzare il titolo dell'istogramma.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='score', hue='sentiment', bins=30, kde=True, alpha=0.6)
        plt.title(f'Distribuzione delle Probabilità di Sentiment - {model_name.capitalize()}')
        plt.xlabel('Punteggio di Confidenza')
        plt.ylabel('Frequenza')
        plt.legend(title='Sentimento')
        plt.tight_layout()
        output_filename = f'sentiment_probabilities_{model_name}.png'
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path)
        plt.close()
        logger.info(f"plot_sentiment_probabilities: Grafico salvato in {output_path}.")
    except Exception as e:
        logger.error(f"plot_sentiment_probabilities: Errore nella creazione del grafico: {e}")


def plot_geographical_distribution(df, output_folder, model_name):
    """
    Crea e salva un grafico della distribuzione geografica dei sentimenti, se i dati sono disponibili.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti con informazioni sulla località.
        output_folder (str): Percorso della cartella di output per salvare il grafico.
        model_name (str): Nome del modello per personalizzare il titolo del grafico.
    """
    try:
        if 'location' not in df.columns:
            logger.warning("plot_geographical_distribution: Dati geografici non disponibili. Grafico non creato.")
            return

        if df['location'].isnull().all():
            logger.warning("plot_geographical_distribution: Nessuna informazione geografica presente. Grafico non creato.")
            return

        # Aggrega i sentimenti per località
        geo_counts = df.groupby(['location', 'sentiment']).size().reset_index(name='counts')

        # Creazione del grafico a barre
        plt.figure(figsize=(12, 8))
        sns.barplot(data=geo_counts, x='location', y='counts', hue='sentiment', palette='viridis')
        plt.title(f'Distribuzione Geografica dei Sentimenti - {model_name.capitalize()}')
        plt.xlabel('Località')
        plt.ylabel('Conteggio')
        plt.xticks(rotation=45)
        plt.legend(title='Sentimento')
        plt.tight_layout()
        output_filename = f'geographical_distribution_{model_name}.png'
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path)
        plt.close()
        logger.info(f"plot_geographical_distribution: Grafico salvato in {output_path}.")
    except Exception as e:
        logger.error(f"plot_geographical_distribution: Errore nella creazione del grafico: {e}")


def export_summary_tables(df, output_folder, model_name):
    """
    Esporta tabelle riassuntive delle distribuzioni dei sentimenti in formato CSV.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti.
        output_folder (str): Percorso della cartella di output per salvare le tabelle.
        model_name (str): Nome del modello per personalizzare il nome del file CSV.
    """
    try:
        summary = df['sentiment'].value_counts().reset_index()
        summary.columns = ['sentiment', 'counts']
        output_filename = f'sentiment_summary_{model_name}.csv'
        output_path = os.path.join(output_folder, output_filename)
        summary.to_csv(output_path, index=False)
        logger.info(f"export_summary_tables: Tabella riassuntiva salvata in {output_path}.")
    except Exception as e:
        logger.error(f"export_summary_tables: Errore nell'esportazione della tabella riassuntiva: {e}")


def plot_top_words(df, output_folder, model_name):
    """
    Crea e salva un grafico delle top-10 parole più frequenti nei tweet.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti.
        output_folder (str): Percorso della cartella di output per salvare il grafico.
        model_name (str): Nome del modello per personalizzare il titolo del grafico.
    """
    try:
        # Unire tutti i testi in un'unica stringa
        all_text = ' '.join(df['text'].astype(str).tolist())

        # Rimuovere la punteggiatura
        translator = str.maketrans('', '', string.punctuation)
        all_text = all_text.translate(translator)

        # Tokenizzazione semplice: dividere per spazi
        words = all_text.lower().split()

        # Conteggio delle parole
        word_counts = Counter(words)

        # Ottenere le top-10 parole
        top_10 = word_counts.most_common(10)

        if not top_10:
            logger.warning("plot_top_words: Nessuna parola trovata per creare il grafico delle top-10 parole.")
            return

        # Separare parole e conteggi
        words, counts = zip(*top_10)

        # Creazione del grafico a barre
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(words), y=list(counts), palette='magma')
        plt.title(f'Top-10 Parole Più Frequenti - {model_name.capitalize()}')
        plt.xlabel('Parola')
        plt.ylabel('Frequenza')
        plt.xticks(rotation=45)
        plt.tight_layout()
        output_filename = f'top10_words_{model_name}.png'
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path)
        plt.close()
        logger.info(f"plot_top_words: Grafico delle top-10 parole salvato in {output_path}.")
    except Exception as e:
        logger.error(f"plot_top_words: Errore nella creazione del grafico delle top-10 parole: {e}")


def plot_most_impactful_words(df, output_folder, model_name, top_n=10):
    """
    Crea e salva un grafico delle parole più impattanti utilizzando l'analisi TF-IDF.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti.
        output_folder (str): Percorso della cartella di output per salvare i grafici.
        model_name (str): Nome del modello per personalizzare il titolo dei grafici.
        top_n (int, optional): Numero di parole impattanti da visualizzare. Default è 10.
    """
    try:
        # Separare i documenti per sentimento
        sentiments = df['sentiment'].unique()
        impactful_words = {}

        for sentiment in sentiments:
            subset = df[df['sentiment'] == sentiment]
            texts = subset['text'].tolist()

            # Inizializzare il vettorizzatore TF-IDF
            vectorizer = TfidfVectorizer(stop_words='english')  # Poiché i dati sono già puliti, possiamo evitare stopwords aggiuntive
            tfidf_matrix = vectorizer.fit_transform(texts)

            # Calcolare la media TF-IDF per ogni termine
            tfidf_mean = tfidf_matrix.mean(axis=0).A1
            terms = vectorizer.get_feature_names_out()
            tfidf_scores = dict(zip(terms, tfidf_mean))

            # Ordinare i termini per punteggio TF-IDF decrescente
            sorted_terms = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

            # Estrarre le top-N parole
            top_words = sorted_terms[:top_n]
            impactful_words[sentiment] = top_words

            # Preparare i dati per il grafico
            words, scores = zip(*top_words)

            # Creare il grafico a barre
            plt.figure(figsize=(10, 6))
            sns.barplot(x=list(words), y=list(scores), palette='coolwarm')
            plt.title(f'Parole Più Impattanti - {sentiment.capitalize()} - {model_name.capitalize()}')
            plt.xlabel('Parola')
            plt.ylabel('Punteggio TF-IDF')
            plt.xticks(rotation=45)
            plt.tight_layout()
            output_filename = f'most_impactful_words_{sentiment}_{model_name}.png'
            output_path = os.path.join(output_folder, output_filename)
            plt.savefig(output_path)
            plt.close()
            logger.info(f"plot_most_impactful_words: Grafico delle parole più impattanti per '{sentiment}' salvato in {output_path}.")

        # Opzionale: Salvare le parole impattanti in un file JSON
        impactful_words_path = os.path.join(output_folder, f'most_impactful_words_{model_name}.json')
        with open(impactful_words_path, 'w', encoding='utf-8') as f:
            json.dump(impactful_words, f, ensure_ascii=False, indent=4)
        logger.info(f"plot_most_impactful_words: Dati delle parole più impattanti salvati in {impactful_words_path}.")

    except Exception as e:
        logger.error(f"plot_most_impactful_words: Errore nell'analisi delle parole più impattanti: {e}")


def plot_sentiment_trend_analysis(df, output_folder, model_name, freq='M'):
    """
    Analizza e crea un grafico delle tendenze dei sentimenti nel tempo.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati dei sentimenti.
        output_folder (str): Percorso della cartella di output per salvare il grafico.
        model_name (str): Nome del modello per personalizzare il titolo del grafico.
        freq (str, optional): Frequenza di aggregazione ('W' per settimane, 'M' per mesi). Default è 'M'.
    """
    try:
        # Assicurarsi che la colonna 'date' sia di tipo datetime
        df['date'] = pd.to_datetime(df['date'])

        # Impostare la data come indice
        df.set_index('date', inplace=True)

        # Raggruppare i dati per la frequenza selezionata e sentimento
        sentiment_trend = df.groupby([pd.Grouper(freq=freq), 'sentiment']).size().reset_index(name='counts')

        # Normalizzare i dati per vedere le proporzioni
        total_counts = sentiment_trend.groupby('date')['counts'].transform('sum')
        sentiment_trend['percentage'] = (sentiment_trend['counts'] / total_counts) * 100

        # Ripristinare l'indice
        df.reset_index(inplace=True)

        # Creazione del grafico
        plt.figure(figsize=(14, 8))
        sns.lineplot(data=sentiment_trend, x='date', y='percentage', hue='sentiment', marker='o')
        plt.title(f'Andamento dei Sentimenti nel Tempo - {model_name.capitalize()}')
        plt.xlabel('Data')
        plt.ylabel('Percentuale (%)')
        plt.legend(title='Sentimento')
        plt.tight_layout()

        # Salvataggio del grafico
        output_filename = f'sentiment_trend_analysis_{model_name}.png'
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path)
        plt.close()
        logger.info(f"plot_sentiment_trend_analysis: Grafico delle tendenze dei sentimenti salvato in {output_path}.")

    except Exception as e:
        logger.error(f"plot_sentiment_trend_analysis: Errore nella creazione del grafico delle tendenze dei sentimenti: {e}")


def main(input_file):
    """
    Processo principale per l'analisi e la visualizzazione dei risultati dell'analisi del sentiment.

    Args:
        input_file (str): Percorso al file JSON di input contenente i risultati dell'analisi del sentiment.
    """
    try:
        # Verifica che il file di input esista
        if not os.path.isfile(input_file):
            logger.error(f"main: Il file di input {input_file} non esiste. Uscita.")
            sys.exit(1)

        # Cartella di output principale per i grafici e le tabelle
        base_output_folder = "./visualizations"
        # Crea la cartella di output temporanea con timestamp
        output_folder = create_output_folder(base_output_folder)

        # Estrazione del nome del modello dal nome del file
        model_name = extract_model_name(input_file)

        # Caricamento e conversione dei dati
        data = load_json(input_file)
        df = convert_to_dataframe(data)

        # Verifica se il DataFrame non è vuoto
        if df.empty:
            logger.error("main: Il DataFrame è vuoto. Uscita.")
            return

        # Creazione delle visualizzazioni
        plot_sentiment_distribution(df, output_folder, model_name)
        plot_temporal_distribution(df, output_folder, model_name)
        plot_wordclouds(df, output_folder, model_name)
        plot_sentiment_probabilities(df, output_folder, model_name)
        plot_geographical_distribution(df, output_folder, model_name)
        plot_top_words(df, output_folder, model_name)  # Grafico Top-10 Parole
        plot_most_impactful_words(df, output_folder, model_name)  # Analisi TF-IDF
        plot_sentiment_trend_analysis(df, output_folder, model_name, freq='M')  # Analisi Tendenze Sentimenti

        # Esportazione delle tabelle riassuntive
        export_summary_tables(df, output_folder, model_name)

        logger.info("MAIN: Analisi e visualizzazioni completate con successo.")
    except Exception as e:
        logger.error(f"main: Errore durante l'esecuzione del main: {e}")


# Esecuzione dello script
if __name__ == "__main__":
    # Configurazione degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Analisi dei risultati e visualizzazioni grafiche della sentiment analysis.')
    parser.add_argument('input_file', type=str, help='Percorso al file JSON di input contenente i risultati dell\'analisi del sentiment.')
    args = parser.parse_args()

    # Avvio del processo principale con il file di input specificato
    main(args.input_file)

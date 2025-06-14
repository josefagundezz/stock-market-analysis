# app.py (Versión 3.0 - Bilingüe)

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, timedelta

# --- 1. DICCIONARIO DE TEXTOS (ESPAÑOL E INGLÉS) ---
TEXTS = {
    'es': {
        'page_title': "Análisis de Acciones",
        'page_icon': "📈",
        'title': "Dashboard de Análisis de Acciones 📈",
        'description': "Esta aplicación interactiva te permite realizar un análisis técnico básico de cualquier acción. **Simplemente introduce el 'ticker' en la barra lateral.**",
        'sidebar_header': "Opciones de Análisis",
        'ticker_label': "Ticker de la Acción",
        'start_date_label': "Fecha de Inicio",
        'end_date_label': "Fecha de Fin",
        'help_header': "¿Qué es un Ticker?",
        'help_info': """
            Un 'ticker' es el símbolo único de una empresa en la bolsa.
            **Ejemplos Populares:**
            - **AAPL:** Apple
            - **GOOGL:** Google
            - **TSLA:** Tesla
            - **NVDA:** NVIDIA
            - **ECOPETROL.CL:** Ecopetrol
            - **BTC-USD:** Bitcoin
            """,
        'button_text': "Analizar Acción",
        'spinner_text': "Cargando datos para",
        'error_not_found': "No se encontraron datos para el ticker o el rango de fechas.",
        'error_download': "Ocurrió un error al descargar los datos:",
        'success_load': "Datos cargados correctamente.",
        'plot1_title': "Tendencia del Precio y Medias Móviles de",
        'plot1_ylabel': "Precio (USD)",
        'plot1_legend_close': "Precio de Cierre Ajustado",
        'plot1_legend_ma50': "Media Móvil 50 Días",
        'plot1_legend_ma200': "Media Móvil 200 Días",
        'plot2_subheader': "Análisis de Volatilidad",
        'plot2_title': "Distribución de Retornos Diarios de",
        'plot2_xlabel': "Retorno Diario",
        'info_start': 'Por favor, introduce un ticker y haz clic en "Analizar Acción".'
    },
    'en': {
        'page_title': "Stock Analysis",
        'page_icon': "📈",
        'title': "Stock Analysis Dashboard 📈",
        'description': "This interactive application allows you to perform basic technical analysis on any stock. **Simply enter the stock 'ticker' in the sidebar.**",
        'sidebar_header': "Analysis Options",
        'ticker_label': "Stock Ticker",
        'start_date_label': "Start Date",
        'end_date_label': "End Date",
        'help_header': "What is a Ticker?",
        'help_info': """
            A 'ticker' is the unique symbol for a company on the stock market.
            **Popular Examples:**
            - **AAPL:** Apple
            - **GOOGL:** Google
            - **TSLA:** Tesla
            - **NVDA:** NVIDIA
            - **ECOPETROL.CL:** Ecopetrol
            - **BTC-USD:** Bitcoin
            """,
        'button_text': "Analyze Stock",
        'spinner_text': "Loading data for",
        'error_not_found': "No data found for the selected ticker or date range.",
        'error_download': "An error occurred while downloading data:",
        'success_load': "Data loaded successfully.",
        'plot1_title': "Price Trend and Moving Averages for",
        'plot1_ylabel': "Price (USD)",
        'plot1_legend_close': "Adjusted Close Price",
        'plot1_legend_ma50': "50-Day Moving Average",
        'plot1_legend_ma200': "200-Day Moving Average",
        'plot2_subheader': "Volatility Analysis",
        'plot2_title': "Distribution of Daily Returns for",
        'plot2_xlabel': "Daily Return",
        'info_start': 'Please enter a ticker and click "Analyze Stock".'
    }
}

# --- 2. MANEJO DEL ESTADO DEL IDIOMA ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'en' # Inglés como idioma por defecto

# Función para cambiar de idioma
def toggle_language():
    st.session_state.lang = 'es' if st.session_state.lang == 'en' else 'en'

# Variable para el texto actual
texts = TEXTS[st.session_state.lang]

# --- Configuración de la Página ---
st.set_page_config(page_title=texts['page_title'], page_icon=texts['page_icon'], layout="wide")

# --- Botón para cambiar de idioma ---
st.button('Español / English', on_click=toggle_language)


# --- Título y Bienvenida ---
st.title(texts['title'])
st.markdown(texts['description'])

# --- Barra Lateral (Sidebar) ---
st.sidebar.header(texts['sidebar_header'])
ticker_symbol = st.sidebar.text_input(texts['ticker_label'], 'AAPL').upper()
today = date.today()
start_date = st.sidebar.date_input(texts['start_date_label'], today - timedelta(days=5*365))
end_date = st.sidebar.date_input(texts['end_date_label'], today)

st.sidebar.subheader(texts['help_header'])
st.sidebar.info(texts['help_info'])


# --- Lógica Principal ---
if st.sidebar.button(texts['button_text']):
    st.header(f'{texts["plot1_title"]} {ticker_symbol}')
    try:
        with st.spinner(f'{texts["spinner_text"]} {ticker_symbol}...'):
            stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=True)
        if stock_data.empty:
            st.error(texts['error_not_found'])
        else:
            st.success(texts['success_load'])
            stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
            stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
            stock_data['Daily Return'] = stock_data['Close'].pct_change()

            fig1, ax1 = plt.subplots(figsize=(16, 8))
            ax1.plot(stock_data['Close'], label=texts['plot1_legend_close'], alpha=0.8, color='dodgerblue')
            ax1.plot(stock_data['MA50'], label=texts['plot1_legend_ma50'], linestyle='--')
            ax1.plot(stock_data['MA200'], label=texts['plot1_legend_ma200'], linestyle='--')
            ax1.set_title(f'{texts["plot1_title"]} {ticker_symbol}', fontsize=16)
            ax1.set_ylabel(texts['plot1_ylabel'], fontsize=12)
            ax1.legend()
            ax1.grid(True)
            st.pyplot(fig1)

            st.subheader(texts['plot2_subheader'])
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            sns.histplot(stock_data['Daily Return'].dropna(), bins=50, kde=True, ax=ax2)
            ax2.set_title(f'{texts["plot2_title"]} {ticker_symbol}', fontsize=16)
            ax2.set_xlabel(texts['plot2_xlabel'], fontsize=12)
            st.pyplot(fig2)
    except Exception as e:
        st.error(f"{texts['error_download']} {e}")
else:
    st.info(texts['info_start'])
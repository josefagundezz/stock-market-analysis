# app.py
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, timedelta

# --- Configuración de la Página ---
st.set_page_config(page_title="Análisis de Acciones", page_icon="📈", layout="wide")

# --- Barra Lateral (Sidebar) ---
st.sidebar.header('Opciones de Usuario')

# Widget para el ticker de la acción
ticker_symbol = st.sidebar.text_input('Ticker de la Acción', 'AAPL').upper()

# Widgets para el rango de fechas
today = date.today()
#Ponemos por defecto desde hace 3 años hasta hoy
start_date = st.sidebar.date_input('Fecha de Inicio', today - timedelta(days=3*365))
end_date = st.sidebar.date_input('Fecha de Fin', today)

# Botón para ejecutar el análisis
if st.sidebar.button('Analizar Acción'):
    # --- Lógica Principal ---
    st.header(f'Análisis Técnico para {ticker_symbol}')

    # Descargar los datos
    try:
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=True)
        if stock_data.empty:
            st.error("No se encontraron datos para el ticker o el rango de fechas seleccionado. Por favor, verifica el ticker.")
            st.stop()
    except Exception as e:
        st.error(f"Ocurrió un error al descargar los datos: {e}")
        st.stop()

    # Calcular medias móviles
    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()

    # Calcular retornos diarios
    stock_data['Daily Return'] = stock_data['Close'].pct_change()

    # --- Creación del Dashboard ---
    st.subheader('Tendencia del Precio y Medias Móviles')
    fig1, ax1 = plt.subplots(figsize=(16, 8))
    ax1.plot(stock_data['Close'], label='Precio de Cierre Ajustado', alpha=0.8)
    ax1.plot(stock_data['MA50'], label='Media Móvil 50 Días', linestyle='--')
    ax1.plot(stock_data['MA200'], label='Media Móvil 200 Días', linestyle='--')
    ax1.set_title(f'Tendencia del Precio de {ticker_symbol}', fontsize=16)
    ax1.set_ylabel('Precio (USD)', fontsize=12)
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    st.subheader('Análisis de Volatilidad (Distribución de Retornos Diarios)')
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.histplot(stock_data['Daily Return'].dropna(), bins=50, kde=True, color='purple', ax=ax2)
    ax2.set_title(f'Distribución de Retornos Diarios de {ticker_symbol}', fontsize=16)
    ax2.set_xlabel('Retorno Diario', fontsize=12)
    st.pyplot(fig2)

else:
    st.info('Por favor, introduce un ticker y haz clic en "Analizar Acción".')
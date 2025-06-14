# app.py (Versión 2.0 - Mejorada)

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, timedelta

# --- Configuración de la Página ---
st.set_page_config(page_title="Análisis de Acciones", page_icon="📈", layout="wide")

# --- Título y Bienvenida ---
st.title('Dashboard de Análisis de Acciones 📈')
st.markdown("""
Esta aplicación interactiva te permite realizar un análisis técnico básico de cualquier acción que cotice en bolsa.
**Simplemente introduce el "ticker" de la acción en la barra lateral y selecciona un rango de fechas.**
""")


# --- Barra Lateral (Sidebar) ---
st.sidebar.header('Opciones de Análisis')

# Widget para el ticker de la acción, con un valor por defecto
ticker_symbol = st.sidebar.text_input('Ticker de la Acción', 'AAPL').upper()

# Widgets para el rango de fechas
today = date.today()
# Ponemos por defecto desde hace 5 años hasta hoy
start_date = st.sidebar.date_input('Fecha de Inicio', today - timedelta(days=5*365))
end_date = st.sidebar.date_input('Fecha de Fin', today)

# --- NUEVO: Sección de ayuda en la barra lateral ---
st.sidebar.subheader('¿Qué es un Ticker?')
st.sidebar.info("""
Un 'ticker' es el símbolo único que identifica a una empresa en la bolsa de valores.
**Ejemplos Populares:**
- **AAPL:** Apple Inc.
- **GOOGL:** Alphabet (Google)
- **MSFT:** Microsoft
- **TSLA:** Tesla, Inc.
- **AMZN:** Amazon
- **ECOPETROL.CL:** Ecopetrol (ejemplo Colombia)
""")


# --- LÓGICA MEJORADA: El código se ejecuta siempre, no espera a un botón ---

# Descargar los datos
try:
    # Mostramos un mensaje mientras se cargan los datos
    with st.spinner(f'Cargando datos para {ticker_symbol}...'):
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=True)
    
    if stock_data.empty:
        st.error("Error: No se encontraron datos para el ticker o el rango de fechas seleccionado. Por favor, verifica el ticker.")
    else:
        st.success(f"Datos para {ticker_symbol} cargados correctamente.")

        # Calcular medias móviles
        stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
        
        # Calcular retornos diarios
        stock_data['Daily Return'] = stock_data['Close'].pct_change()

        # --- Creación del Dashboard ---
        st.subheader('Tendencia del Precio y Medias Móviles')
        fig1, ax1 = plt.subplots(figsize=(16, 8))
        ax1.plot(stock_data['Close'], label='Precio de Cierre Ajustado', alpha=0.8, color='dodgerblue')
        ax1.plot(stock_data['MA50'], label='Media Móvil 50 Días', linestyle='--', color='orange')
        ax1.plot(stock_data['MA200'], label='Media Móvil 200 Días', linestyle='--', color='red')
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

except Exception as e:
    st.error(f"Ocurrió un error: {e}")
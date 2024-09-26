import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import openai

# Configuración de la página
st.set_page_config(page_title="Dashboard Financiero", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/edgroma04/TrabajoFinal/refs/heads/main/Datos_proyecto_corregido.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Calcular ratios
df['Ratio de Liquidez Corriente'] = df['Current_Assets'] / df['Current_Liabilities']
df['Ratio de Deuda a Patrimonio'] = (df['Short_Term_Debt'] + df['Long_Term_Debt']) / df['Equity']
df['Cobertura de Gastos Financieros'] = df['Total_Revenue'] / df['Financial_Expenses']

# Título del dashboard
st.title("Dashboard Financiero")

# Sección 1: Gráfica de barras apiladas por sector
st.header("Análisis por Sector")

sector_metrics = df.groupby('Industry')[['Ratio de Liquidez Corriente', 'Ratio de Deuda a Patrimonio', 'Cobertura de Gastos Financieros']].mean().reset_index()

fig_sector = go.Figure(data=[
    go.Bar(name='Ratio de Liquidez Corriente', x=sector_metrics['Industry'], y=sector_metrics['Ratio de Liquidez Corriente']),
    go.Bar(name='Ratio de Deuda a Patrimonio', x=sector_metrics['Industry'], y=sector_metrics['Ratio de Deuda a Patrimonio']),
    go.Bar(name='Cobertura de Gastos Financieros', x=sector_metrics['Industry'], y=sector_metrics['Cobertura de Gastos Financieros'])
])

fig_sector.update_layout(barmode='stack', title='Ratios Financieros por Sector')
st.plotly_chart(fig_sector, use_container_width=True)
# Instanciar el cliente de OpenAI
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai_api_key)

def obtener_respuesta(prompt):
  response = client.chat.completions.create(
      model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
      messages=[
          {"role": "system", "content": """
         Eres un inversionista que desea invertir en acciones # Instanciar el cliente de OpenAI
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai_api_key)

def obtener_respuesta(prompt):
  response = client.chat.completions.create(
      model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
      messages=[
          {"role": "system", "content": """
          Eres un financiero que trabaja para la aseguradora patito, eres experto en el área de solvencia,
          entonces vas a responder todo desde la perspectiva de la aseguradora. Contesta siempre en español
          en un máximo de 50 palabras.
          """}, #Solo podemos personalizar la parte de content
          {"role": "user", "content": prompt}
      ]
  )
  output = response.choices[0].message.content
  return output

prompt_user= st.text_area("Ingresa tu pregunta: ")

# Obtener la respuesta del modelo
output_modelo = obtener_respuesta(prompt_user)

# Mostrar la respuesta del modelo
st.write(output_modelo)
          """}, #Solo podemos personalizar la parte de content
          {"role": "user", "content": prompt}
      ]
  )
  output = response.choices[0].message.content
  return output

prompt_user= st.text_area("Ingresa tu pregunta: ")

# Obtener la respuesta del modelo
output_modelo = obtener_respuesta(prompt_user)

# Mostrar la respuesta del modelo
st.write(output_modelo)

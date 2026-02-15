import streamlit as st
import pandas as pd
import plotly_express as px

# -----------------------------
# Cargar datos
# -----------------------------
df = pd.read_csv("sleepdata.csv")

# -----------------------------
# Encabezado
# -----------------------------
st.header("Screen Time, Sleep and Stress Dashboard")

st.write("Esta aplicación permite explorar la relación entre el tiempo de pantalla, las horas de sueño y el nivel de estrés.")

# -----------------------------
# Botón Histograma
# -----------------------------
hist_button = st.button("Construir histograma de horas de sueño")

if hist_button:
    st.write("Distribución de las horas de sueño")

    fig = px.histogram(
        df,
        x="Sleep_Hours",
        nbins=30,
        title="Distribución de Horas de Sueño"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Botón Scatter Plot
# -----------------------------
scatter_button = st.button("Construir gráfico de dispersión")

if scatter_button:
    st.write("Relación entre uso diario del teléfono y horas de sueño")

    fig = px.scatter(
        df,
        x="Daily_Phone_Hours",
        y="Sleep_Hours",
        color="Stress_Level",
        title="Daily Phone Hours vs Sleep Hours"
    )

    st.plotly_chart(fig, use_container_width=True)

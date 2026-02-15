import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================================
# Configuración general
# ==========================================================

PAGE_TITLE = "Dashboard - Sueño y uso de los dispositivos moviles"
DATA_FILE = "sleepdata.csv"

NUMERIC_COLUMNS = [
    "Daily_Phone_Hours",
    "Social_Media_Hours",
    "Sleep_Hours",
    "Work_Productivity_Score",
    "Caffeine_Intake_Cups",
    "Weekend_Screen_Time_Hours"
]


# ==========================================================
# Carga de datos
# ==========================================================

@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """Carga el dataset desde un archivo CSV."""
    return pd.read_csv(filepath)


# ==========================================================
# Filtros
# ==========================================================

def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    """Crea filtros en la barra lateral y devuelve el dataframe filtrado."""

    st.sidebar.header("🔎 Filtros")

    selected_gender = st.sidebar.multiselect(
        "Género",
        options=data["Gender"].unique(),
        default=data["Gender"].unique()
    )

    selected_occupation = st.sidebar.multiselect(
        "Ocupación",
        options=data["Occupation"].unique(),
        default=data["Occupation"].unique()
    )

    selected_device = st.sidebar.multiselect(
        "Tipo de dispositivo",
        options=data["Device_Type"].unique(),
        default=data["Device_Type"].unique()
    )

    age_range = st.sidebar.slider(
        "Rango de Edad",
        int(data["Age"].min()),
        int(data["Age"].max()),
        (int(data["Age"].min()), int(data["Age"].max()))
    )

    selected_stress = st.sidebar.multiselect(
        "Nivel de Estrés",
        options=data["Stress_Level"].unique(),
        default=data["Stress_Level"].unique()
    )

    filtered_data = data[
        (data["Gender"].isin(selected_gender)) &
        (data["Occupation"].isin(selected_occupation)) &
        (data["Device_Type"].isin(selected_device)) &
        (data["Age"].between(age_range[0], age_range[1])) &
        (data["Stress_Level"].isin(selected_stress))
    ]

    return filtered_data


# ==========================================================
# Métricas
# ==========================================================

def display_metrics(data: pd.DataFrame) -> None:
    """Muestra métricas principales del dataset filtrado."""

    st.subheader("📌 Indicadores Generales")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Promedio Horas de Sueño", round(
        data["Sleep_Hours"].mean(), 2))
    col2.metric("Promedio Uso Diario Teléfono", round(
        data["Daily_Phone_Hours"].mean(), 2))
    col3.metric("Promedio Nivel Estrés", round(data["Stress_Level"].mean(), 2))
    col4.metric("Promedio Productividad", round(
        data["Work_Productivity_Score"].mean(), 2))


# ==========================================================
# Visualizaciones
# ==========================================================

def display_histogram(data: pd.DataFrame) -> None:
    """Muestra histograma de horas de sueño."""

    st.subheader("📈 Distribución de Horas de Sueño")

    fig = px.histogram(
        data,
        x="Sleep_Hours",
        color="Stress_Level",
        nbins=30,
        title="Distribución de Horas de Sueño"
    )

    st.plotly_chart(fig, use_container_width=True)


def display_scatter_plot(data: pd.DataFrame) -> None:
    """Muestra gráfico de dispersión dinámico."""

    st.subheader("📉 Análisis Relacional")

    x_axis = st.selectbox("Selecciona variable eje X", NUMERIC_COLUMNS)
    y_axis = st.selectbox("Selecciona variable eje Y",
                          NUMERIC_COLUMNS, index=2)

    fig = px.scatter(
        data,
        x=x_axis,
        y=y_axis,
        color="Stress_Level",
        size="App_Usage_Count",
        hover_data=data.columns,
        title=f"{x_axis} vs {y_axis}"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# Aplicación principal
# ==========================================================

def main() -> None:
    """Función principal de la aplicación."""

    st.set_page_config(page_title=PAGE_TITLE, layout="wide")

    st.title("📊 Screen Time, Sleep & Stress Analysis Dashboard")
    st.markdown(
        "Explora cómo el uso del teléfono, redes sociales y otros factores "
        "influyen en las horas de sueño y el nivel de estrés."
    )

    data = load_data(DATA_FILE)
    filtered_data = apply_filters(data)

    display_metrics(filtered_data)
    display_histogram(filtered_data)
    display_scatter_plot(filtered_data)


if __name__ == "__main__":
    main()

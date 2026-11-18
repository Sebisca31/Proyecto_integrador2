
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="IA y estudiantes",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ¿La IA está ayudando a los estudiantes?")
st.write(
    "Análisis del uso de inteligencia artificial, "
    "rendimiento académico y dependencia tecnológica."
)

archivo = st.file_uploader(
    "Carga el dataset CSV",
    type=["csv"]
)

if archivo is not None:

    datos = pd.read_csv(archivo)
    datos.columns = datos.columns.str.strip()

    st.success("Dataset cargado correctamente")

    st.sidebar.header("Configuración de variables")

    st.sidebar.write("Selecciona las columnas correspondientes.")

    def buscar_columnas(palabras):
        return [
            c for c in datos.columns
            if any(p in c.lower() for p in palabras)
        ]

    def selector(nombre, palabras):
        opciones = buscar_columnas(palabras)
        if not opciones:
            return None
        return st.sidebar.selectbox(nombre, opciones)

    col_uso = selector(
        "Frecuencia de uso de IA",
        ["frequency", "frecuencia", "usage"]
    )

    col_herramienta = selector(
        "Herramienta de IA",
        ["tool", "herramienta", "platform"]
    )

    col_motivo = selector(
        "Motivo de uso",
        ["purpose", "motivo", "reason"]
    )

    col_rendimiento = selector(
        "Rendimiento académico",
        ["gpa", "grade", "score", "nota", "academic"]
    )

    col_horas = selector(
        "Horas de estudio",
        ["study", "estudio"]
    )

    col_confianza = selector(
        "Confianza o dependencia",
        ["depend", "trust", "confianza"]
    )

    st.divider()

    st.header("1. Resumen general")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total de estudiantes", len(datos))

    if col_uso:
        c2.metric(
            "Categorías de uso",
            datos[col_uso].nunique()
        )

    if col_herramienta:
        c3.metric(
            "Herramientas utilizadas",
            datos[col_herramienta].nunique()
        )

    st.subheader("Vista general del dataset")
    st.dataframe(datos.head(10), use_container_width=True)

    st.divider()

    st.header("2. ¿Cómo utilizan la IA?")

    if col_herramienta:
        st.subheader("Herramientas más utilizadas")
        st.bar_chart(datos[col_herramienta].value_counts())

    if col_motivo:
        st.subheader("Principales motivos de uso")
        st.bar_chart(datos[col_motivo].value_counts())

    if col_uso:
        st.subheader("Frecuencia de utilización")
        st.bar_chart(datos[col_uso].value_counts())

    st.divider()

    st.header("3. IA y rendimiento académico")

    if col_rendimiento:
        rendimiento = pd.to_numeric(
            datos[col_rendimiento],
            errors="coerce"
        ).dropna()

        if len(rendimiento) > 0:
            c1, c2, c3 = st.columns(3)

            c1.metric("Promedio", round(np.mean(rendimiento), 2))
            c2.metric("Mediana", round(np.median(rendimiento), 2))
            c3.metric("Desviación estándar",
                      round(np.std(rendimiento), 2))

    if col_uso and col_rendimiento:
        temporal = datos[[col_uso, col_rendimiento]].copy()
        temporal[col_rendimiento] = pd.to_numeric(
            temporal[col_rendimiento],
            errors="coerce"
        )
        temporal = temporal.dropna()

        if not temporal.empty:
            st.subheader("Rendimiento según frecuencia de uso")
            comparacion = temporal.groupby(col_uso)[
                col_rendimiento
            ].mean()

            st.bar_chart(comparacion)

    st.divider()

    st.header("4. Confianza y dependencia")

    if col_confianza:
        st.subheader("Distribución de confianza o dependencia")
        st.bar_chart(datos[col_confianza].value_counts())

    st.divider()

    st.header("5. Exploración de datos")

    columnas = st.multiselect(
        "Selecciona las variables que deseas visualizar",
        datos.columns.tolist(),
        default=datos.columns.tolist()[:5]
    )

    st.dataframe(
        datos[columnas],
        use_container_width=True
    )

    csv = datos.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Descargar dataset",
        csv,
        "datos_analizados.csv",
        "text/csv"
    )

else:
    st.info("Carga el archivo CSV para comenzar el análisis.")
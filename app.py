import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Cargar los archivos Excel
file_path_facultades = "./FACUL123.xlsx"
file_path_carreras = "./CARRERAS.xlsx"

df_facultades = pd.read_excel(file_path_facultades, sheet_name='Hoja1')
df_carreras = pd.read_excel(file_path_carreras)

# Función para filtrar el DataFrame según los filtros seleccionados
def filtrar_datos(region, financiamiento, facultad):
    df_filtrado = df_facultades.copy()
    
    if region != "Todos":
        df_filtrado = df_filtrado[df_filtrado["REGION"] == region]
    if financiamiento != "Todos":
        df_filtrado = df_filtrado[df_filtrado["FINANCIAMIENTO"] == financiamiento]
    if facultad != "Todos":
        df_filtrado = df_filtrado[df_filtrado["FACULTAD UDLA"] == facultad]
    
    return df_filtrado

# Función para actualizar el gráfico de participación por facultad
def actualizar_grafico(df_filtrado):
    if df_filtrado.empty:
        st.write("No hay datos para mostrar con los filtros seleccionados.")
        return
    
    df_agrupado = df_filtrado.groupby(['Instituto', 'AÑO'])['Participación'].sum().unstack().fillna(0)
    df_agrupado = df_agrupado * 100
    
    institutos = df_agrupado.index
    años = df_agrupado.columns
    
    bar_width = 0.2
    indices = np.arange(len(institutos))
    colors = plt.get_cmap('Blues')(np.linspace(0.3, 0.8, len(años)))
    
    fig, ax = plt.subplots(figsize=(18, 10))
    
    for i, año in enumerate(años):
        ax.bar(indices + i * bar_width, df_agrupado[año], bar_width, label=f"Año {año}", color=colors[i])
    
    ax.set_xlabel('Universidad')
    ax.set_ylabel('Participación por facultad (%)')
    ax.set_title('Participación por Facultad por Año (%)')
    
    for i, año in enumerate(años):
        for j, valor in enumerate(df_agrupado[año]):
            if valor > 0:
                ax.text(indices[j] + i * bar_width, valor + 0.2, f'{valor:.0f}%', ha='center', va='bottom', fontsize=9)
    
    ax.set_xticks(indices + bar_width)
    ax.set_xticklabels(institutos, rotation=45, ha='right')
    
    for tick in ax.get_xticklabels():
        if 'UNIVERSIDAD DE LAS AMERICAS' in tick.get_text().upper():
            tick.set_fontweight('bold')
    
    ax.legend()
    st.pyplot(fig)

# Función para actualizar el gráfico según la carrera seleccionada
def actualizar_grafico_por_carrera(df_filtrado, carrera):
    if df_filtrado.empty:
        st.write("No hay datos para mostrar con los filtros seleccionados.")
        return
    
    df_agrupado = df_filtrado.groupby(['Instituto', 'AÑO'])['Participación'].sum().unstack().fillna(0)
    df_agrupado = df_agrupado * 100
    
    institutos = df_agrupado.index
    años = df_agrupado.columns
    
    bar_width = 0.2
    indices = np.arange(len(institutos))
    colors = plt.get_cmap('Blues')(np.linspace(0.3, 0.8, len(años)))
    
    fig, ax = plt.subplots(figsize=(18, 10))
    
    for i, año in enumerate(años):
        ax.bar(indices + i * bar_width, df_agrupado[año], bar_width, label=f"Año {año}", color=colors[i])
    
    ax.set_xlabel('Universidad')
    ax.set_ylabel(f'Participación en {carrera} (%)')
    ax.set_title(f'Participación por Universidad en {carrera} por Año (%)')
    
    for i, año in enumerate(años):
        for j, valor in enumerate(df_agrupado[año]):
            if valor > 0:
                ax.text(indices[j] + i * bar_width, valor + 0.2, f'{valor:.0f}%', ha='center', va='bottom', fontsize=9)
    
    ax.set_xticks(indices + bar_width)
    ax.set_xticklabels(institutos, rotation=45, ha='right')
    
    for tick in ax.get_xticklabels():
        if 'UNIVERSIDAD DE LAS AMERICAS' in tick.get_text().upper():
            tick.set_fontweight('bold')
    
    ax.legend()
    st.pyplot(fig)

# Streamlit UI
st.title('Análisis de Participación por Facultad y Año')

# Filtros
regiones = ["Todos"] + sorted(df_facultades["REGION"].unique().tolist())
financiamientos = ["Todos"] + sorted(df_facultades["FINANCIAMIENTO"].unique().tolist())
facultades = ["Todos"] + sorted(df_facultades["FACULTAD UDLA"].unique().tolist())

region = st.selectbox("Región:", regiones)
financiamiento = st.selectbox("Financiamiento:", financiamientos)
facultad = st.selectbox("Facultad:", facultades)

# Filtrar los datos
df_filtrado = filtrar_datos(region, financiamiento, facultad)

# Mostrar gráfico de participación por facultad
if not df_filtrado.empty:
    actualizar_grafico(df_filtrado)
else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")

# Mostrar botones de carrera
if facultad != "Todos":
    carreras = df_carreras[df_carreras["FACULTAD UDLA"] == facultad]["CARRERA UDLA"].unique()
    
    carrera_seleccionada = st.radio("Selecciona una carrera:", carreras)
    
    if carrera_seleccionada:
        df_filtrado_carrera = df_carreras[
            (df_carreras['REGION'] == region) &
            (df_carreras['FINANCIAMIENTO'] == financiamiento) &
            (df_carreras['FACULTAD UDLA'] == facultad) &
            (df_carreras['CARRERA UDLA'] == carrera_seleccionada)
        ]
        
        actualizar_grafico_por_carrera(df_filtrado_carrera, carrera_seleccionada)

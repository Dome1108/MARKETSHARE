import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Cargar los archivos Excel
file_path_facultades = r"C:\Users\domenica.villalva.01\OneDrive - Universidad de Las Américas\FACUL123.xlsx"
file_path_carreras = r"C:\Users\domenica.villalva.01\Downloads\CARRERAS.xlsx"

df_facultades = pd.read_excel(file_path_facultades, sheet_name='Hoja1')
df_carreras = pd.read_excel(file_path_carreras)

# Función para filtrar el DataFrame según los filtros seleccionados
def filtrar_datos(region, financiamiento, facultad):
    df_filtrado = df_facultades.copy()
    
    # Aplicar los filtros seleccionados
    if region != "Todos":
        df_filtrado = df_filtrado[df_filtrado["REGION"] == region]
    if financiamiento != "Todos":
        df_filtrado = df_filtrado[df_filtrado["FINANCIAMIENTO"] == financiamiento]  # Usar los valores exactos: "PÚBLICA", "PRIVADA"
    if facultad != "Todos":
        df_filtrado = df_filtrado[df_filtrado["FACULTAD UDLA"] == facultad]
    
    return df_filtrado

# Función para actualizar el gráfico de participación por facultad
def actualizar_grafico(df_filtrado):
    # Agrupar por Instituto y Año
    df_agrupado = df_filtrado.groupby(['Instituto', 'AÑO'])['Participación por facultad'].sum().unstack().fillna(0)
    
    # Convertir a porcentaje
    df_agrupado = df_agrupado * 100
    
    institutos = df_agrupado.index
    años = df_agrupado.columns
    
    bar_width = 0.2  # Ajustamos el ancho de las barras para dejar más espacio
    indices = np.arange(len(institutos))
    colors = plt.get_cmap('Blues')(np.linspace(0.3, 0.8, len(años)))  # Escala de colores azules
    
    plt.figure(figsize=(18, 10))  # Ajustar el tamaño del gráfico
    
    # Dibujar barras para cada año con colores en escala de azul
    for i, año in enumerate(años):
        plt.bar(indices + i * bar_width, df_agrupado[año], bar_width, label=f"Año {año}", color=colors[i])
    
    plt.xlabel('Universidad')
    plt.ylabel('Participación por facultad (%)')
    plt.title('Participación por Facultad por Año (%)')

    # Colocar las etiquetas de porcentaje encima de las barras
    for i, año in enumerate(años):
        for j, valor in enumerate(df_agrupado[año]):
            if valor > 0:  # Mostrar solo si el valor es mayor a 0
                plt.text(indices[j] + i * bar_width, valor + 0.2, f'{valor:.0f}%', ha='center', va='bottom', fontsize=9)
    
    # Ajustar las etiquetas de las universidades en el eje X
    plt.xticks(indices + bar_width, institutos, rotation=45, ha='right')  # Ajustar rotación y alineación
    
    # Poner en negritas la Universidad de las Américas
    for tick in plt.gca().get_xticklabels():
        if 'UNIVERSIDAD DE LAS AMERICAS' in tick.get_text().upper():
            tick.set_fontweight('bold')
    
    plt.legend()
    plt.tight_layout(pad=3)  # Ajustar el gráfico para evitar superposición con los bordes
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)  # Más espacio para el eje X
    st.pyplot(plt)

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

# Mostrar gráfico si hay datos
if not df_filtrado.empty:
    actualizar_grafico(df_filtrado)
else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")



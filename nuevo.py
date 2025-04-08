import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(
    page_title="Visualizador de Datos",
    layout="wide"
)

# Título principal
st.title("Visualizador Dinámico de Datos")
st.markdown("Esta aplicación permite visualizar datos según los parámetros que selecciones.")

# Sidebar con controles
st.sidebar.header("Controles de Datos")

# Sliders para seleccionar valores
valor1 = st.sidebar.slider("Valor 1", 0, 100, 25, help="Selecciona el primer valor")
valor2 = st.sidebar.slider("Valor 2", 0, 100, 50, help="Selecciona el segundo valor") 
valor3 = st.sidebar.slider("Valor 3", 0, 100, 75, help="Selecciona el tercer valor")
valor4 = st.sidebar.slider("Valor 4", 0, 100, 60, help="Selecciona el cuarto valor")

# Lista de valores para usar en gráficos
valores = [valor1, valor2, valor3, valor4]
etiquetas = ["Categoría A", "Categoría B", "Categoría C", "Categoría D"]

# Generamos algunos datos adicionales para gráficos más complejos
x = np.arange(len(etiquetas))
y = np.array(valores)

# Selector del tipo de gráfico
st.sidebar.header("Tipo de Visualización")
tipo_grafico = st.sidebar.selectbox(
    "Selecciona el tipo de gráfico",
    ["Gráfico de Barras", "Gráfico de Líneas", "Gráfico Circular"]
)

# Contenedor principal para la visualización
st.header(f"Visualización: {tipo_grafico}")

# Crear y mostrar el gráfico seleccionado
fig, ax = plt.figure(figsize=(10, 6)), plt.axes()

if tipo_grafico == "Gráfico de Barras":
    # Gráfico de barras con colores personalizados
    bars = ax.bar(x, y, width=0.6)
    
    # Añadir colores diferentes a cada barra
    colors = ['#4285F4', '#DB4437', '#F4B400', '#0F9D58']
    for i, bar in enumerate(bars):
        bar.set_color(colors[i % len(colors)])
    
    # Añadir etiquetas de datos
    for i, v in enumerate(valores):
        ax.text(i, v + 2, str(v), ha='center', fontweight='bold')
    
    ax.set_ylabel('Valores')
    ax.set_title('Comparación de valores por categoría')
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

elif tipo_grafico == "Gráfico de Líneas":
    # Crear datos adicionales para una línea más interesante
    # Añadimos algunos puntos intermedios para suavizar la línea
    x_detallado = np.linspace(0, len(valores) - 1, 100)
    y_suavizado = np.interp(x_detallado, range(len(valores)), valores)
    
    # Trazar la línea principal
    ax.plot(x_detallado, y_suavizado, color='#4285F4', linewidth=3)
    
    # Añadir marcadores en los puntos de datos originales
    ax.scatter(x, y, color='#DB4437', s=100, zorder=5)
    
    # Añadir etiquetas a los puntos
    for i, v in enumerate(valores):
        ax.text(i, v + 2, str(v), ha='center', fontweight='bold')
    
    ax.set_ylabel('Valores')
    ax.set_title('Tendencia de valores por categoría')
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Añadir área sombreada bajo la línea
    ax.fill_between(x_detallado, y_suavizado, alpha=0.2, color='#4285F4')

elif tipo_grafico == "Gráfico Circular":
    # Crear gráfico circular (pie)
    # Solo mostraremos valores positivos
    valores_positivos = [max(0, v) for v in valores]
    
    # Ajustar colores y propiedades
    colors = ['#4285F4', '#DB4437', '#F4B400', '#0F9D58']
    
    # Destacar la sección más grande
    explode = [0] * len(valores)
    indice_max = valores.index(max(valores))
    explode[indice_max] = 0.1
    
    wedges, texts, autotexts = ax.pie(
        valores_positivos, 
        explode=explode,
        labels=etiquetas, 
        autopct='%1.1f%%',
        shadow=True, 
        startangle=90,
        colors=colors
    )
    
    # Personalizar textos
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title('Distribución proporcional de valores')
    # Asegurar que el círculo se vea como un círculo
    ax.axis('equal')

# Ajustes finales del gráfico
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Sección adicional con datos en tabla
st.header("Datos Utilizados")
df = pd.DataFrame({
    'Categoría': etiquetas,
    'Valor': valores
})
st.table(df)

# Información adicional
st.markdown("---")
st.markdown("""
### Información sobre el gráfico
- Los valores mostrados son los seleccionados mediante los sliders.
- Puedes cambiar el tipo de visualización en cualquier momento.
- La tabla muestra los datos exactos utilizados para el gráfico.
""")

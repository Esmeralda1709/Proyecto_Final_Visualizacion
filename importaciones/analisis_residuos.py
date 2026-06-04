from nltk import ngrams
from collections import Counter
import matplotlib.pyplot as plt

def obtener_ngrams(texto, n):
    tokens = texto.split()
    return list(ngrams(tokens, n))

def generar_ngrams(corpus, top=15):
    unigramas = []
    bigramas = []
    trigramas = []
    
    for i in corpus:
        unigramas.extend(obtener_ngrams(i, 1))
        bigramas.extend(obtener_ngrams(i, 2))
        trigramas.extend(obtener_ngrams(i, 3))
    
    frecuencia_unigramas = Counter(unigramas).most_common(top)
    frecuencia_bigramas = Counter(bigramas).most_common(top)
    frecuencia_trigramas = Counter(trigramas).most_common(top)
    
    return frecuencia_unigramas, frecuencia_bigramas, frecuencia_trigramas

def graficar_ngrams(frecuencias, titulo, paleta):
    etiquetas = [' '.join(ng) for ng, _ in frecuencias]
    valores = [freq for _, freq in frecuencias]
    
    # Usamos subplots para poder retornar la figura a Streamlit
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Interceptamos la paleta personalizada
    if isinstance(paleta, list):
        colores = [paleta[i % len(paleta)] for i in range(len(etiquetas))]
    elif isinstance(paleta, str) and paleta.lower() == 'okabe-ito':
        paleta_okabe = ['#000000', '#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
        colores = [paleta_okabe[i % len(paleta_okabe)] for i in range(len(etiquetas))]
    else:
        colores = plt.cm.get_cmap(paleta)(range(len(etiquetas)))
    
    ax.bar(etiquetas, valores, color=colores)

    plt.xticks(rotation=45, ha="right") 
    ax.set_title(titulo)
    plt.tight_layout(pad=3.0)
    
    return fig

def hacer_graficos(comentarios_outliers, titulo, paleta='viridis'):
    # Ya no llamamos a outliers() aquí, usamos los que nos mandan
    uni, bi, tri = generar_ngrams(comentarios_outliers)

    fig1 = graficar_ngrams(uni, "Unigramas - " + titulo, paleta)
    fig2 = graficar_ngrams(bi, "Bigramas - " + titulo, paleta)
    fig3 = graficar_ngrams(tri, "Trigramas - " + titulo, paleta)
    
    # Retornamos las figuras para que el dashboard las dibuje
    return fig1, fig2, fig3
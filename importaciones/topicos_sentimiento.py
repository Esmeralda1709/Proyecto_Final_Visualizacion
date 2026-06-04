from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def modelar_topicos(comentarios, n_topicos=2, n_palabras=10):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(comentarios)
    lda = LatentDirichletAllocation(n_components=n_topicos, random_state=42)
    distribucion = lda.fit_transform(X)

    palabras = vectorizer.get_feature_names_out()
    resultados = []
    for idx, topic in enumerate(lda.components_):
        # Palabras clave del tópico
        top_words = [palabras[i] for i in topic.argsort()[-n_palabras:]]
        # comentario más representativo (máxima probabilidad en este tópico)
        rep_idx = np.argmax(distribucion[:, idx])
        comentario_rep = comentarios[rep_idx]
        resultados.append((idx, top_words, comentario_rep))
    return resultados


def frecuencia_palabras(comentarios):
    texto = " ".join(comentarios)
    wc = WordCloud(width=800, height=400, background_color="white").generate(texto)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def topicos_por_sentimiento(corpus, tipo, idioma="es", umbral=5):
    # Ya no llamamos a sentimientos aquí, usamos el corpus que nos pasan
    print(f"\n--- Comentarios {tipo} ---")
    lista_resultados = []
    
    if len(corpus) >= umbral:
        topicos = modelar_topicos(corpus) # Asumimos que modelar_topicos existe en tu archivo
        for idx, palabras, comentario in topicos:
            print(f"Tópico {idx}: {', '.join(palabras)}")
            print(f"Comentario representativo: {comentario}\n")
            lista_resultados.append({
                    "ID": "Frecuencia",
                    "Palabras Clave": ", ".join(palabras),
                    "Comentario Representativo": f"Apariciones: {comentario}"
                })
    else:
        print(f"Muy pocos comentarios {tipo}, usando frecuencia de palabras...")
        frecuencia_palabras(corpus)
        frecuencias = frecuencia_palabras(corpus)
        if frecuencias:
            for palabra, cantidad in frecuencias:
                lista_resultados.append({
                    "ID": "Frecuencia",
                    "Palabras Clave": palabra,
                    "Comentario Representativo": f"Apariciones: {cantidad}"
                })
                
    topicos_encontrados = pd.DataFrame(lista_resultados)
    return topicos_encontrados

from sentence_transformers import SentenceTransformer, util
import plotly.express as px
import pandas as pd

def filtro_semantico(corpus, paleta='viridis', umbral=0.40, top_n=5):
    """
    Análisis del concepto 'precio/valor/costo':
    - Identifica comentarios relacionados (similitud >= umbral).
    - Genera scatter plot interactivo con hover/clic.
    - Muestra un reporte con los top N comentarios más cercanos.
    """

    # Modelo multilingüe para similitud semántica
    modelo = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    # Concepto objetivo
    concepto_objetivo = "precio costo valor económico dinero caro barato pago"

    # Embeddings
    embeddings_corpus = modelo.encode(corpus, convert_to_tensor=True)
    embedding_concepto = modelo.encode(concepto_objetivo, convert_to_tensor=True)

    # Similitud coseno
    similitudes = util.cos_sim(embedding_concepto, embeddings_corpus)[0].cpu().numpy()

    # Clasificación
    comentarios_precio = [doc for doc, score in zip(corpus, similitudes) if score >= umbral]
    comentarios_otros = [doc for doc, score in zip(corpus, similitudes) if score < umbral]

    # Top N más cercanos
    top_indices = similitudes.argsort()[-top_n:][::-1]
    top_comentarios = [(corpus[i], similitudes[i]) for i in top_indices]

    # Scatter plot interactivo
    df = pd.DataFrame({
        "comentario": corpus,
        "similitud": similitudes,
        "relacionado": ["Relacionado" if s >= umbral else "No relacionado" for s in similitudes]
    })
    
    # para la paleta de color
    if isinstance(paleta, list):
        # Si recibe nuestra lista personalizada Okabe-Ito
        secuencia_colores = paleta
    elif isinstance(paleta, str) and paleta.lower() == 'plotly3':
        secuencia_colores = px.colors.sequential.Plotly3
    elif isinstance(paleta, str):
        # Si recibe textos como 'viridis' o 'plasma'
        secuencia_colores = getattr(px.colors.sequential, paleta.capitalize(), px.colors.sequential.Viridis)
    else:
        secuencia_colores = px.colors.sequential.Viridis

    fig = px.scatter(
        df,
        x=range(len(corpus)),
        y="similitud",
        color="relacionado",
        color_discrete_sequence=secuencia_colores, 
        hover_data=["comentario"],
        title="Relación de comentarios con el concepto Precio/Valor/Costo"
    )
    fig.show()

    # Reporte
    print("\n--- Reporte de análisis Precio/Valor/Costo ---")
    print(f"Comentarios relacionados: {len(comentarios_precio)}")
    print(f"Comentarios no relacionados: {len(comentarios_otros)}\n")

    print(f"Top {top_n} comentarios más cercanos al concepto:")
    for comentario, score in top_comentarios:
        print(f"- ({score:.3f}) {comentario}")

    return comentarios_precio, comentarios_otros, top_comentarios, fig #retorno el fig para el dashboard

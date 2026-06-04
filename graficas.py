"""
PALETA APTA: 

Black (#000000)

Orange (#E69F00)

Sky BLue (#56B4E9)

Bluish Green (#009E73)

Yellow (#F0E442)

Blue (#0072B2)

Vermillion (#D55E00)

Reddish Purple (#CC79A7)
    
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import pickle 
import os     

# Importaciones de modulos
from importaciones.limpiar_palabras import preprocessing_text
from importaciones.Isolation_forest import outliers
from importaciones.analisis_sentimiento import sentimientos
from importaciones.analisis_pv import filtro_semantico
from importaciones.analisis_residuos import hacer_graficos
# from importaciones.Filtro_inicial_bertopic import llamada_bertopic_visualizaciones
from importaciones.Filtro_inicial import llamada_bertopic
from importaciones.topicos_sentimiento import topicos_por_sentimiento

# Configuración de la página
st.set_page_config(page_title="Dashboard de Percepción Turística", layout="wide")
st.title("Análisis de Percepción Turística")
st.markdown("Procesamiento de Lenguaje Natural para evaluación de destinos turísticos en México.")

# --- LÓGICA DE CARGA AUTOMÁTICA ---
if os.path.exists("datos_dashboard.pkl"):
    # Si el archivo existe, lo leemos instantáneamente
    with open("datos_dashboard.pkl", "rb") as archivo:
        datos = pickle.load(archivo)
        
    st.success("Datos procesados cargados desde la terminal.")
    
    # Extraemos las variables del diccionario
    paleta_activa = datos["paleta_activa"]
    corpus_limpio = datos["corpus_limpio"]
    normales = datos["normales"]
    atipicos = datos["atipicos"]
    positivos = datos["positivos"]
    negativos = datos["negativos"]
    out_pos = datos["out_pos"]
    out_neg = datos["out_neg"]
    topicos_pos = datos["topicos_pos"]
    topicos_neg = datos["topicos_neg"]
    top_n = datos["top_n"]
    fig_pv = datos["fig_pv"]
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Anomalías y N-gramas", "Sentimientos", "Outliers por Sentimiento", "Precio y Valor"])
    
    # --- TAB 1: OUTLIERS GLOBALES ---
    with tab1:
        st.subheader("Análisis de anomalías textuales (Isolation Forest)")
        # Como hacer_graficos solo dibuja, se ejecuta rapidísimo
        fig_uni, fig_bi, fig_tri = hacer_graficos(corpus_limpio, titulo="Globales", paleta=paleta_activa)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.pyplot(fig_uni)
        with col2: st.pyplot(fig_bi)
        with col3: st.pyplot(fig_tri)

    # --- TAB 2: SENTIMIENTOS Y TÓPICOS ---
    with tab2:
        st.subheader("Clasificación de Polaridad y Tópicos Principales")
        
        # Gráfica de pastel generada al instante
        df_sent = pd.DataFrame({
            "Sentimiento": ["Positivos", "Negativos"],
            "Cantidad": [len(positivos), len(negativos)]
        })
        fig_sent = px.pie(
            df_sent, values='Cantidad', names='Sentimiento', 
            color_discrete_sequence=paleta_activa if isinstance(paleta_activa, list) else px.colors.qualitative.Set1
        )
        st.plotly_chart(fig_sent, use_container_width=True)
        
        st.divider()
        st.markdown("Tópicos Principales por Sentimiento")
        
        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.success("🟢 Tópicos Positivos")
            st.dataframe(topicos_pos, use_container_width=True)
            
        with col_neg:
            st.error("🔴 Tópicos Negativos")
            st.dataframe(topicos_neg, use_container_width=True)

    # --- TAB 3: RUIDO BERTOPIC ---
    with tab3:
        st.subheader("Ruido y Outliers descubiertos por BERTopic")
        
        st.write("### N-gramas Atípicos: Comentarios Positivos")
        # Los outliers de bertopic (out_pos) ya vienen calculados de main.py
        fig_up, fig_bp, fig_tp = hacer_graficos(out_pos, titulo="Positivos", paleta=paleta_activa)
        col1, col2, col3 = st.columns(3)
        with col1: st.pyplot(fig_up)
        with col2: st.pyplot(fig_bp)
        with col3: st.pyplot(fig_tp)
        
        st.divider() 
        
        st.write("### N-gramas Atípicos: Comentarios Negativos")
        fig_un, fig_bn, fig_tn = hacer_graficos(out_neg, titulo="Negativos", paleta=paleta_activa)
        col4, col5, col6 = st.columns(3)
        with col4: st.pyplot(fig_un)
        with col5: st.pyplot(fig_bn)
        with col6: st.pyplot(fig_tn)

    # --- TAB 4: PRECIO Y VALOR ---
    with tab4:
        st.subheader("Filtro Semántico: Precio, Costo y Valor")
        
        # Mostramos la gráfica de Plotly que ya venía armada desde main.py
        st.plotly_chart(fig_pv, use_container_width=True)
        
        st.write("**Top comentarios con mayor carga económica:**")
        for comentario, score in top_n:
            st.markdown(f"- *(Score: {score:.3f})* {comentario}")

else:
    # --- MODO MANUAL ---
    st.info("No se detectó un análisis previo. Por favor, sube un archivo.")

    # --- Subir archivo ---
    st.sidebar.header("Dataset para Analisis")
    archivo_subido = st.sidebar.file_uploader("Sube el dataset (CSV o Excel)", type=["csv", "xlsx", "xls"])

    if archivo_subido is not None:
        
        # Lectura del archivo 
        if archivo_subido.name.endswith('.csv'):
            # hacemos un try catcch para poder leerlo con diferente encoding (ya me dio error xd)
            try:
                # con encoding utf-8-sig
                df = pd.read_csv(archivo_subido, encoding='utf-8-sig') 
            except UnicodeDecodeError:
                # si hay error usa latin-1
                archivo_subido.seek(0) 
                df = pd.read_csv(archivo_subido, encoding='latin-1')
        else:
            # aca si es excel no hay problema de encoding
            df = pd.read_excel(archivo_subido)
            
        columnas_disponibles = df.columns.tolist()
        
        columna_interes = st.sidebar.selectbox("Columna a analizar:", columnas_disponibles)
        idioma = st.sidebar.selectbox("Idioma del corpus:", ["es", "en", "fr"])
        
        # Selector de paleta de colores
        opcion_paleta = st.sidebar.selectbox(
            "Paleta de colores:", 
            ["Okabe-Ito (Personalizada)", "viridis", "plasma", "plotly3"]
        )
        
        # Asignación de la lista de hexadecimales
        if opcion_paleta == "Okabe-Ito (Personalizada)":
            # Colores
            paleta_activa = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
        else:
            paleta_activa = opcion_paleta

        st.write("### Vista previa de los datos")
        st.dataframe(df[[columna_interes]].head())

        # ejecucion completa
        if st.button("Ejecutar Análisis Completo", use_container_width=True):
            
            # Extracción de la columna y eliminación de nulos
            corpus = df[columna_interes].dropna()
            
            # LIMPIEZA
            with st.spinner('Limpiando y normalizando el texto...'):
                corpus_limpio = preprocessing_text(corpus.tolist(), idioma=idioma, use_lemma=True)
                st.success(f"Se limpiaron {len(corpus_limpio)} comentarios con éxito.")
            
            # Creación de pestañas para organizar la información visual
            tab1, tab2, tab3, tab4 = st.tabs(["Anomalías y N-gramas", "Sentimientos", "Outliers por Sentimiento", "Precio y Valor"])
            
            # ANALISIS DE OUTLIERS
            with tab1:
                st.subheader("Análisis de anomalías textuales (Isolation Forest)")
                normales, atipicos = outliers(corpus_limpio)
                
                # Llamamos a la función adaptada para que retorne las figuras
                fig_uni, fig_bi, fig_tri = hacer_graficos(corpus_limpio, titulo="Globales", paleta=paleta_activa)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.pyplot(fig_uni)
                with col2:
                    st.pyplot(fig_bi)
                with col3:
                    st.pyplot(fig_tri)

            # SENTIMIENTOS
            with tab2:
                st.subheader("Clasificación de Polaridad")
                with st.spinner('Ejecutando modelos transformer de clasificación...'):
                    positivos, negativos = sentimientos(normales, idioma)
                    
                    df_sent = pd.DataFrame({
                        "Sentimiento": ["Positivos", "Negativos"],
                        "Cantidad": [len(positivos), len(negativos)]
                    })
                    
                    fig_sent = px.pie(
                        df_sent, 
                        values='Cantidad', 
                        names='Sentimiento', 
                        color_discrete_sequence=paleta_activa if isinstance(paleta_activa, list) else px.colors.qualitative.Set1
                    )
                    
                    st.plotly_chart(fig_sent, use_container_width=True)
                
                # --- Extracción y visualización de Tópicos ---
                st.divider() # Línea divisoria visual
                st.markdown("Tópicos Principales por Sentimiento")
                
                with st.spinner('Extrayendo tópicos principales de cada polaridad...'):
                    
                    # Llamamos a la función de tópicos. 
                    topicos_pos = topicos_por_sentimiento(positivos, tipo="positivos", idioma=idioma)
                    topicos_neg = topicos_por_sentimiento(negativos, tipo="negativos", idioma=idioma)
                    
                    # Dividimos la pantalla en 2 columnas para comparar
                    col_pos, col_neg = st.columns(2)
                    
                    with col_pos:
                        st.success("🟢 Tópicos Positivos")
                        # Dependiendo de lo que retorne tu función, usamos st.dataframe o st.write
                        if isinstance(topicos_pos, pd.DataFrame):
                            st.dataframe(topicos_pos, use_container_width=True)
                        else:
                            st.write(topicos_pos) # Si devuelve una lista, texto o diccionario
                            
                    with col_neg:
                        st.error("🔴 Tópicos Negativos")
                        # Dependiendo de lo que retorne tu función, usamos st.dataframe o st.write
                        if isinstance(topicos_neg, pd.DataFrame):
                            st.dataframe(topicos_neg, use_container_width=True)
                        else:
                            st.write(topicos_neg)
                    
            # --- OUTLIERS BERTOPIC ---
            with tab3:
                st.subheader("Ruido y Outliers descubiertos por BERTopic")
                with st.spinner('Procesando tópicos latentes...'):
                    # Llamamos a tu nueva lógica
                    out_pos = llamada_bertopic(positivos)
                    out_neg = llamada_bertopic(negativos)
                    
                    st.write("### N-gramas Atípicos: Comentarios Positivos")
                    fig_up, fig_bp, fig_tp = hacer_graficos(out_pos, titulo="Positivos", paleta=paleta_activa)
                    col1, col2, col3 = st.columns(3)
                    with col1: st.pyplot(fig_up)
                    with col2: st.pyplot(fig_bp)
                    with col3: st.pyplot(fig_tp)
                    
                    st.divider() # Línea divisoria
                    
                    st.write("### N-gramas Atípicos: Comentarios Negativos")
                    fig_un, fig_bn, fig_tn = hacer_graficos(out_neg, titulo="Negativos", paleta=paleta_activa)
                    col4, col5, col6 = st.columns(3)
                    with col4: st.pyplot(fig_un)
                    with col5: st.pyplot(fig_bn)
                    with col6: st.pyplot(fig_tn)

            # ANALISIS PRECIO VALOR
            with tab4:
                st.subheader("Filtro Semántico: Precio, Costo y Valor")
                with st.spinner('Calculando distancia coseno de embeddings...'):
                    precio, otros, top_n, fig_pv = filtro_semantico(normales, paleta=paleta_activa)
                    
                    st.plotly_chart(fig_pv, use_container_width=True)
                    
                    st.write("**Top 5 comentarios con mayor carga económica:**")
                    for comentario, score in top_n:
                        st.markdown(f"- *(Score: {score:.3f})* {comentario}")
    else:
        st.info("Por favor, sube un archivo en la barra lateral para comenzar la evaluación.")
import argparse
import subprocess
import pickle #para guardar los resultados
# Importaciones desde la carpeta 'importaciones'
from importaciones.Filtro_inicial import llamada_bertopic
from importaciones.leer_archivo import leer_archivos
from importaciones.limpiar_palabras import preprocessing_text
from importaciones.Isolation_forest import outliers
from importaciones.analisis_sentimiento import sentimientos
from importaciones.topicos_sentimiento import topicos_por_sentimiento
from importaciones.analisis_pv import filtro_semantico
from importaciones.analisis_residuos import hacer_graficos

def main():
    # 1. Configuración de parámetros obligatorios (CLI)
    parser = argparse.ArgumentParser(description="Analizador de Comentarios Turísticos")
    parser.add_argument("--ruta", required=True, help="Ruta del archivo CSV/Excel")
    parser.add_argument("--columna", required=True, help="Nombre de la columna a analizar")
    parser.add_argument("--idioma", required=True, help="Idioma (es, en, fr)")
    parser.add_argument("--titulo", required=True, help="Título del reporte")
    parser.add_argument("--paleta", required=True, help="Paleta de colores (ej. viridis, plasma)")
    parser.add_argument("--lemma", help="Usar lematizacion? (True, False)")
    parser.add_argument("--stem", help="Usar stemming? (True, False)")

    args = parser.parse_args()

    print(f"\n--- Iniciando: {args.titulo} ---")
    
    if args.paleta.lower() == 'okabe-ito':
        paleta = ['#000000', '#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
    else:
        paleta = args.paleta

    # 2. Flujo de procesamiento
    # Carga
    print("leyendo archivo")
    corpus = leer_archivos(args.ruta, args.columna)
    if corpus is None:
        print("Error crítico: No se pudo leer el archivo. Abortando.")
        return
    
    # Limpieza
    print("limpiando")
    corpus_limpio = preprocessing_text(corpus.tolist(), idioma=args.idioma,use_lemma=args.lemma, use_stem=args.stem)
    
    # Análisis de Outliers y N-gramas (Pasa paleta)
    print("graficas")
    #hacer_graficos(corpus_limpio, paleta=args.paleta)
    normales, atipicos = outliers(corpus_limpio)
    hacer_graficos(atipicos, titulo="Outliers", paleta=paleta)
    
    
    
    # Análisis de Sentimientos
    print("Sentimientos")
    positivos, negativos = sentimientos(normales, args.idioma)
    # para el modelado.
    out_pos = llamada_bertopic(positivos)
    out_neg = llamada_bertopic(negativos) 
    
    # Modelado de Tópicos (Apartado 5)
    print("\n--- Modelado de Tópicos ---")
    topicos_por_sentimiento(positivos, tipo="positivos", idioma=args.idioma)
    topicos_por_sentimiento(negativos, tipo="negativos", idioma=args.idioma)
    topicos_pos = topicos_por_sentimiento(positivos, tipo="positivos", idioma=args.idioma)
    topicos_neg = topicos_por_sentimiento(negativos, tipo="negativos", idioma=args.idioma)
    
    # Análisis Precio/Valor/Costo (Apartado 7 - Pasa paleta)
    print("\n--- Análisis Precio/Valor/Costo ---")
    filtro_semantico(normales, paleta=paleta)
    precio, otros, top_n, fig_pv = filtro_semantico(normales, paleta=paleta)

    print(f"\nProceso '{args.titulo}' finalizado con éxito.")
    
    # --- Para abrir Streamlit al finalizar ---
    print("Guardando resultados para el dashboard...")
 
    # diccionario con los datos
    datos_exportar = {
        "idioma": args.idioma,
        "paleta_activa": paleta,
        "corpus_limpio": corpus_limpio,
        "normales": normales,
        "atipicos": atipicos,
        "positivos": positivos,
        "negativos": negativos,
        "out_pos": out_pos,
        "out_neg": out_neg,
        "topicos_pos": topicos_pos,
        "topicos_neg": topicos_neg,
        "precio": precio,
        "otros": otros,
        "top_n": top_n,
        "fig_pv": fig_pv # Plotly sí permite guardar sus figuras directamente
    }
    
    # Guardamos el diccionario en un archivo físico
    with open("datos_dashboard.pkl", "wb") as archivo:
        pickle.dump(datos_exportar, archivo)
    
    
    print("\nIniciando el dashboard...")
    
    # Esto simula correr "streamlit run graficas.py" en consola
    try:
        subprocess.run(["streamlit", "run", "graficas.py"])
    except Exception as e:
        print(f"Error al intentar abrir Streamlit: {e}")

if __name__ == "__main__":
    main()

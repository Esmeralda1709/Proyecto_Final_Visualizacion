from bertopic import BERTopic
import pandas as pd


def llamada_bertopic(df, idioma='multilingual', min_samples = 15, reduccion_muestras = 5, umbral=120):
	"""
		esta funcióm dados los parametros usara un modelo BERT, este tomara los comentarios y regresara un embeding
	:param df: columna del dataframe LIMPIO(sin acentos y stopwords) para el modelo
	:param idioma: idioma en el qeu estan los cometarios, se dejara 'multilingual' por defecto, ete funcionara(en teoria) independiete del idioma
	:param min_samples: minimo de muestras que habra por topico, se deja 15 por defecto
	:param reduccion_muestras: si llega a pasar al siguiente nivel, este dira cuantas muestras menos se usaran, se deja 5 por defecto
	:param umbral: numero de comentarios minimo en el que se seguiran considerando muchos, se deja por defecto 120
	:return: lista de los valores que quedaron como ruido(outliers) se regrasara el original
	"""
	if isinstance(df, pd.DataFrame):
		comentarios = df.dropna().tolist()
	elif isinstance(df, list):
		comentarios = [doc for doc in df if pd.notna(doc)]
	else:
		comentarios = pd.Series(df).dropna().tolist()
	
	if min_samples <= 0:
		print('numero minimo de muestras no aceptado')
		return comentarios

	#se supondra que la lista vendra con los comentarios nsuficientes para entrar al modelo BERT, opor lo que se dejara el comprobante de ello para despues
	modelo = BERTopic(language=idioma, min_topic_size=min_samples)
	temas, _ = modelo.fit_transform(comentarios)
	info_docs_1 = modelo.get_document_info(comentarios)
	comentarios_ruido = info_docs_1[info_docs_1["Topic"] == -1]['Document'].tolist()
	#aqui se gradficara el conjunto de temas, accediendo a los clusteres formados en info_temas, ignorando el '-1', se accede con info_temas['Topic', 'Count', 'Name']
	if len(comentarios_ruido) > umbral:
		print("aun hay suficientes comentarios, se volvera a crear un modelo para tratar de clasificarlo nuevamente")
		return llamada_bertopic(df = comentarios_ruido, idioma = idioma, min_samples=min_samples-reduccion_muestras, reduccion_muestras=reduccion_muestras)
	else:
		return comentarios_ruido

from transformers import pipeline
import torch
import streamlit as st

@st.cache_data # guarda en cache los datos pq tarda mucho en ejecutar
def sentimientos(corpus, idioma):
	if idioma == 'multilingual':
		modelo_sentiment = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
	elif idioma == 'spanish' or idioma == 'es':
		modelo_sentiment = "pysentimiento/robertuito-sentiment-analysis"
	else:
		modelo_sentiment = "distilbert-base-uncased-finetuned-sst-2-english"
	
	analizador = pipeline("sentiment-analysis", model=modelo_sentiment, truncation=True, max_length=512)
	
	resultados = analizador(corpus, truncation=True, max_length=128)
	
	positivos = []
	negativos = []
	
	for doc, label in zip(corpus, resultados):
		if label['label'].upper() in ['NEGATIVE', 'NEG']:
			negativos.append(doc)
		else:
			#si es que llegan a existor neutros se mandan a positivos
			positivos.append(doc)
	
	return positivos, negativos

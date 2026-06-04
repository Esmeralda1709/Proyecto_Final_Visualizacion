from sklearn.ensemble import IsolationForest
from sentence_transformers import SentenceTransformer

def outliers(corpus, contaminacion = 0.05):
	modelo_embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
	embeddings = modelo_embedder.encode(corpus)
	
	detector = IsolationForest(contamination=contaminacion, random_state=42)
	predicciones = detector.fit_predict(embeddings)
	
	comentarios_normales = []
	comentarios_outliers = []
	
	for doc, pred in zip(corpus, predicciones):
		if pred < 0:
			comentarios_outliers.append(doc)
		else:
			comentarios_normales.append(doc)
	
	return comentarios_normales, comentarios_outliers

import pandas as pd

def leer_archivos(ruta, columna_interes, tipo='.csv', hoja=0, separador=None):
	"""
	lee el archivo de entrada de comentarios
	:param ruta: ruita del archivo
	:param tipo: tipo del archivo subido(csv, txt, etc). solo se dejaran 3: csv, txt y excel, en caso de excel se debera de especificar la hoja que se quiere analizar
	:param columna_interes: columan queb se va a analizar
	:return: el datafr5ame seccionado por la columna de interes
	"""
	tipo_limpio = tipo.lower().replace('.', '').strip()
	
	try:
		if tipo_limpio in ['csv', 'txt']:
			try:
				# con encoding utf-8-sig
				df = pd.read_csv(ruta, sep=separador, engine='python' if separador is None else None, encoding='utf-8-sig')
			except UnicodeDecodeError:
				# si hay error usa latin-1
				df = pd.read_csv(ruta, sep=separador, engine='python' if separador is None else None, encoding='latin-1')
    
		elif tipo_limpio in ['excel', 'xlsx', 'xls']:
			df = pd.read_excel(ruta, sheet_name=hoja)
		
		else:
			raise ValueError(f"Tipo de archivo '{tipo}' no soportado.")
		
		if columna_interes not in df.columns:
			raise KeyError(f"La columna '{columna_interes}' no existe. Columnas encontradas: {list(df.columns)}")
		
		return df[columna_interes]
	
	except Exception as e:
		print(f"Error al procesar el archivo: {e}")
		return None

import re
import spacy
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

# --- Descargar recursos ---
nltk.download('stopwords')

def accent(word):
    # Agregamos caracteres especiales del francés si es necesario
    return word.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('à', 'a').replace('è', 'e').replace('ê', 'e').replace('î', 'i').replace('ô', 'o').replace('û', 'u').replace('ç', 'c')

def pal_vacias(texto, s_sw):
    palabras = texto.split()
    filtradas = [p for p in palabras if p not in s_sw]
    return " ".join(filtradas)

def lematizacion(texto, nlp):
    doc = nlp(texto)
    return " ".join(token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space)

def stemming(texto, stemmer):
    tokens = texto.split()
    return " ".join([stemmer.stem(token) for token in tokens])

def limpiar_texto(doc):
    doc = re.sub(r"http\S+|www\S+", "", doc)
    doc = re.sub(r"[^\w\s]", " ", doc)
    return doc

def preprocessing_text(corpus, idioma='es', use_lemma=False, use_stem=False):
    # Configuración según el idioma
    if idioma == "es":
        nlp = spacy.load("es_core_news_sm")
        stemmer = SnowballStemmer("spanish")
        s_sw = set(stopwords.words("spanish"))
    elif idioma == "en":
        nlp = spacy.load("en_core_web_sm")
        stemmer = SnowballStemmer("english")
        s_sw = set(stopwords.words("english"))
    elif idioma == "fr":
        nlp = spacy.load("fr_core_news_sm")
        stemmer = SnowballStemmer("french")
        s_sw = set(stopwords.words("french"))
    else:
        raise ValueError(f"Idioma no soportado: {idioma}")

    processed = []
    
    for doc in corpus:
        doc = limpiar_texto(doc)
        doc = accent(doc.lower())
        
        # Expresión regular ajustada para incluir caracteres latinos básicos del francés
        tokens = re.findall(r'[a-zñüàâçéèêëîïôûùÿ]+', doc)
        tokens = [w for w in tokens if 3 <= len(w) <= 20]

        text = pal_vacias(" ".join(tokens), s_sw)

        if use_lemma:
            text = lematizacion(text, nlp)
        if use_stem:
            text = stemming(text, stemmer)

        processed.append(text)

    return processed

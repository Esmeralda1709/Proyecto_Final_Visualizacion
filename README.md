# 🏖️ Analizador de Comentarios Turísticos Multilingüe

## 📖 Descripción

Este proyecto desarrolla una herramienta en Python para el análisis automatizado de comentarios turísticos almacenados en archivos CSV.

La aplicación implementa técnicas de Procesamiento de Lenguaje Natural (PLN) para limpiar y analizar texto, determinar el sentimiento de los comentarios, identificar temas recurrentes mediante modelado de tópicos y generar visualizaciones interactivas que facilitan la interpretación de los resultados.

Todo el procesamiento se realiza localmente, sin depender de APIs externas.

---

## 🎯 Objetivo

Desarrollar una solución autónoma capaz de:

- Procesar comentarios turísticos en distintos idiomas.
- Realizar limpieza y normalización de texto.
- Aplicar técnicas de stemming y/o lematización.
- Analizar sentimientos de los usuarios.
- Identificar tópicos relevantes dentro de los comentarios.
- Generar visualizaciones interactivas para facilitar la exploración de resultados.
- Facilitar su ejecución desde la línea de comandos.

---

## 🌎 Idiomas Soportados

El sistema puede procesar comentarios en:

- Español (`es`)
- Inglés (`en`)
- Francés (`fr`)

Cada idioma utiliza sus correspondientes listas de stopwords para mejorar la calidad del procesamiento del texto.

---

## ⚙️ Funcionalidades

### Limpieza y preprocesamiento

- Conversión de texto a minúsculas.
- Eliminación de caracteres especiales.
- Eliminación de stopwords.
- Tokenización.
- Normalización de texto.
- Stemming (opcional).
- Lematización (opcional).

### Análisis de sentimientos

El sistema clasifica automáticamente los comentarios en dos categorías:

- Positivo 😊
- Negativo ☹️

Los comentarios neutralesson considerados comentarios positivos.

### Modelado de tópicos

Detección automática de temas frecuentes presentes en los comentarios turísticos.

### Visualización interactiva

Generación de gráficas y reportes interactivos para explorar:

- Distribución de sentimientos.
- Frecuencia de palabras.
- Nubes de palabras.
- Principales tópicos detectados.
- Estadísticas descriptivas.

---

## 🛠️ Tecnologías Utilizadas

- Python 3.10
- Pandas
- NumPy
- NLTK
- SpaCy
- Scikit-Learn
- Gensim
- Plotly
- Matplotlib

---

## 📂 Estructura del Proyecto

```text
Proyecto_Final_Visualizacion/
│
├── Archivos/
├── importaciones/
├── graficas.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Esmeralda1709/Proyecto_Final_Visualizacion.git
```

### 2. Entrar al directorio

```bash
cd Proyecto_Final_Visualizacion
```

### 3. Crear entorno de Conda

```bash
conda create -n pipeline_turismo python=3.10
```

### 4. Activar el entorno

```bash
conda activate pipeline_turismo
```

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📚 Descarga de Recursos Adicionales

### NLTK

Es necesario descargar las stopwords utilizadas por el sistema:

```python
import nltk

nltk.download('stopwords')
```

Las listas de palabras vacías utilizadas corresponden a:

- Español
- Inglés
- Francés

### SpaCy

Si se desea utilizar lematización, es necesario instalar los modelos de lenguaje correspondientes.

#### Español

```bash
python -m spacy download es_core_news_sm
```

#### Inglés

```bash
python -m spacy download en_core_web_sm
```

#### Francés

```bash
python -m spacy download fr_core_news_sm
```

Los modelos cargados por el sistema son:

```python
spacy.load("es_core_news_sm")
spacy.load("en_core_web_sm")
spacy.load("fr_core_news_sm")
```
---



## ▶️ Ejecución

El programa se ejecuta desde la línea de comandos mediante argumentos:

```bash
python main.py \
--ruta " [Lugar y nombre de la ubicacion del archivo que deseas analizar] " \
--columna " [Nombre de la columna de tu archivo que contiene los comentarios] " \
--idioma " [Idioma en el cual estan todos o la mayoria de los comentarios] "\
--titulo " [Titulo que le quieras dar al analisis] " \
--paleta " [Paleta de color que va a tener] " \
--lemma [True si lo quieres usar / False si no lo quieres usar]
--stem [True si lo quieres usar / False si no lo quieres usar]
```

### Parámetros

| Parámetro | Descripción |
|------------|------------|
| `--ruta` | Ruta al archivo CSV |
| `--columna` | Nombre de la columna que contiene los comentarios |
| `--idioma` | Idioma de los comentarios (`es`, `en`, `fr`) |
| `--titulo` | Título utilizado en los reportes y visualizaciones |
| `--paleta` | Paleta de colores para las gráficas |
| `--lemma` | Activa o desactiva la lematización (`True` o `False`) |
| `--stem` | Activa el stemming (`True` o `False`) |

---

### Ejemplos

Sin stemming ni lematización:

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito"
```

Con lematización:

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito" --lemma True
```

Con stemming:

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito" --stem True
```

Con lematización y stemming:

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito" --lemma True --stem True
```

---

## ⏱️ Tiempo de Procesamiento

El tiempo de ejecución depende del tamaño del conjunto de datos.

Como referencia:

- Archivos pequeños: 20-30 minutos.
- Archivos medianos: 45 minutos a 1 hora.
- Archivos grandes: más de 1 hora.

El modelado de tópicos y el procesamiento lingüístico suelen ser las etapas más demandantes computacionalmente.

---

## 📊 Resultados

Al finalizar el procesamiento, el sistema abrirá automáticamente una interfaz interactiva en el navegador.

Desde ella será posible explorar:

- N-gramas de las anomalias de los comentarios.
- Distribución de comentarios positivos y negativos.
- Tópicos principales de los comentarios positivos y negativos.
- Comentario representativo de esos tópicos
- N-gramas de las anomalias de los comentarios positivos y negativos.
- Grafica de la relación de comentarios con el concepto de Precio/Valor/Costo.
- Top 5 de comentarios con mayor carga económica.


Esto permite al usuario navegar e interpretar fácilmente los resultados obtenidos.

---

> ⚠️ **Importante**
>
> El tiempo de procesamiento puede superar los 30 minutos para conjuntos de datos grandes, especialmente cuando se utilizan técnicas de modelado de tópicos, lematización o stemming.
>
> Se recomienda no cerrar la terminal durante la ejecución del análisis.

---

## 👩‍💻 Autor

**ANGEL RAFAEL LOPEZ HERNANDEZ**
**JESSICA ALMENDRA CERVERA MARTINEZ**
**ESMERALDA ABIGAIL RUIZ VAZQUEZ**

Proyecto desarrollado con fines académicos para la materia de Visualización y Análisis de Datos.

---

## 📜 Licencia

Este proyecto tiene fines educativos y académicos.

# 🏖️ Analizador de Comentarios Turísticos Multilingüe

## 📖 Descripción

Este proyecto consiste en una herramienta desarrollada en Python para el análisis automatizado de comentarios turísticos almacenados en archivos CSV.

La aplicación emplea técnicas de Procesamiento de Lenguaje Natural (PLN) para realizar la limpieza y normalización de texto, análisis de sentimientos, detección de tópicos y generación de visualizaciones interactivas. Todo el procesamiento se ejecuta localmente, sin depender de APIs o servicios externos.

El objetivo es proporcionar una solución reproducible y fácil de utilizar para explorar grandes volúmenes de opiniones turísticas y obtener información relevante sobre la percepción de los usuarios.

---

## 🎯 Objetivos

* Procesar comentarios turísticos en múltiples idiomas.
* Realizar tareas de limpieza y normalización de texto.
* Aplicar técnicas opcionales de stemming y/o lematización.
* Clasificar comentarios según su sentimiento.
* Identificar los principales tópicos presentes en los comentarios.
* Detectar patrones y anomalías lingüísticas mediante análisis de n-gramas.
* Analizar la presencia de conceptos relacionados con precio, valor y costo.
* Generar visualizaciones interactivas que faciliten la exploración de resultados.
* Permitir la ejecución completa desde la línea de comandos.

---

## 🌎 Idiomas Soportados

El sistema puede procesar comentarios escritos en:

* Español (`es`)
* Inglés (`en`)
* Francés (`fr`)

Para cada idioma se utilizan listas específicas de stopwords y recursos lingüísticos adaptados al procesamiento del texto.

---

## ⚙️ Funcionalidades

### Limpieza y preprocesamiento

* Conversión de texto a minúsculas.
* Eliminación de caracteres especiales.
* Eliminación de stopwords.
* Tokenización.
* Normalización de texto.
* Stemming (opcional).
* Lematización (opcional).

### Análisis de sentimientos

Los comentarios son clasificados en dos categorías:

* Positivos 😊
* Negativos ☹️

Los comentarios neutrales son incorporados a la categoría positiva para efectos del análisis.

### Modelado de tópicos

Detección automática de temas recurrentes dentro de los comentarios mediante técnicas de modelado de tópicos.

### Visualización interactiva

Generación de gráficos y reportes interactivos que permiten explorar los resultados de manera dinámica.

---

## 🛠️ Tecnologías Utilizadas

* Python 3.10
* Pandas
* NumPy
* NLTK
* SpaCy
* Scikit-Learn
* Gensim
* Plotly
* Matplotlib

---

## 📂 Estructura del Proyecto

```text
Proyecto_Final_Visualizacion/
│
├── Archivos/
    ├── comentarios.csv
    ├── huatulco-T_unido.csv
    ├── lapaz-T_unido.csv
    ├── pv-T_unido.csv
    ├── rm-T_unido.csv
    └── rn-T_unido.csv
├── importaciones/
    ├── Filtro_inicial.py
    ├── Insolation_forest.py
    ├── analisis_pv.py
    ├── analisis_residuos.py
    ├── analisis_sentimiento.py
    ├── leer_archivo.py
    ├── limpiar_palabras.py
    └── topicos_sentimiento.py
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

### 2. Acceder al directorio

```bash
cd Proyecto_Final_Visualizacion
```

### 3. Crear el entorno virtual con Conda

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

## 📚 Recursos Adicionales

### SpaCy

Si se desea utilizar lematización, deberán instalarse los modelos correspondientes:

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

Modelos utilizados:

```python
spacy.load("es_core_news_sm")
spacy.load("en_core_web_sm")
spacy.load("fr_core_news_sm")
```

---

## ▶️ Ejecución

La ejecución se realiza desde la línea de comandos mediante los siguientes parámetros:

```bash
python main.py \
--ruta "[Ruta del archivo CSV]" \
--columna "[Nombre de la columna que contiene los comentarios]" \
--idioma "[es | en | fr]" \
--titulo "[Título del análisis]" \
--paleta "[Nombre de la paleta de colores]" \
--lemma [True | False] \
--stem [True | False]
```

### Parámetros disponibles

| Parámetro   | Descripción                                        |
| ----------- | -------------------------------------------------- |
| `--ruta`    | Ruta del archivo CSV a analizar                    |
| `--columna` | Columna que contiene los comentarios               |
| `--idioma`  | Idioma predominante de los comentarios             |
| `--titulo`  | Título mostrado en los resultados                  |
| `--paleta`  | Paleta de colores utilizada en las visualizaciones |
| `--lemma`   | Activa o desactiva la lematización                 |
| `--stem`    | Activa o desactiva el stemming                     |

### Ejemplos

**Sin stemming ni lematización**

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito"
```

**Con lematización**

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito" --lemma True
```

**Con stemming**

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito" --stem True
```

**Con lematización y stemming**

```bash
python main.py --ruta "Archivos/rn-T_unido.csv" --columna "Comentario" --idioma "es" --titulo "Analisis" --paleta "okabe-ito" --lemma True --stem True
```

---

## ⏱️ Tiempo de Procesamiento

El tiempo de ejecución depende principalmente del tamaño del conjunto de datos y de los recursos disponibles en el equipo.

Como referencia:

* Archivos pequeños: 20 a 30 minutos.
* Archivos medianos: 45 minutos a 1 hora.
* Archivos grandes: más de 1 hora.

Las etapas de modelado de tópicos y procesamiento lingüístico suelen representar la mayor parte del tiempo de ejecución.

---

## 📊 Resultados Generados

Al finalizar el procesamiento, el sistema abrirá automáticamente una interfaz interactiva en el navegador para la exploración de resultados.

Entre los elementos generados se incluyen:

* N-gramas asociados a anomalías detectadas en los comentarios.
* Distribución de comentarios positivos y negativos.
* Principales tópicos encontrados en comentarios positivos.
* Principales tópicos encontrados en comentarios negativos.
* Comentarios representativos para cada tópico identificado.
* N-gramas asociados específicamente a comentarios positivos y negativos.
* Análisis de la relación entre los comentarios y conceptos económicos como precio, valor y costo.
* Top 5 de comentarios con mayor carga económica.

---

> ⚠️ **Importante**
>
> El tiempo de procesamiento puede superar una hora cuando se analizan conjuntos de datos grandes o cuando se habilitan técnicas adicionales como lematización y stemming.
>
> Durante la ejecución se recomienda no cerrar la terminal ni interrumpir el proceso.

---

## 👩‍💻 Autores

* Angel Rafael López Hernández
* Jessica Almendra Cervera Martínez
* Esmeralda Abigail Ruiz Vázquez

Proyecto desarrollado con fines académicos para la materia de **Visualización y Análisis de Datos**.

---

## 📜 Licencia

Este proyecto fue desarrollado con fines educativos y académicos.

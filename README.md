# Ciencia de Datos Aplicada al Fútbol
### Modelado de Acciones y Métricas Avanzadas de Rendimiento
#### DiploDatos 2026 · Mentoría · FaMAF — Universidad Nacional de Córdoba

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Jupyter-Notebooks-orange?style=flat-square&logo=jupyter" />
  <img src="https://img.shields.io/badge/Dataset-Wyscout%202017%2F18-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Framework-VAEP%20%7C%20xT-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?style=flat-square" />
</p>

---

## Descripción

Este proyecto aplica técnicas modernas de **ciencia de datos y aprendizaje automático** al análisis del fútbol profesional, usando datos reales de eventos de partido de la temporada 2017/18 provistos por **Wyscout**.

Recorremos un flujo completo de data science — desde la ingesta y exploración de datos hasta el modelado supervisado y no supervisado — con foco en producir métricas accionables para la evaluación objetiva del rendimiento de jugadores y equipos.

El proyecto sigue los estándares actuales de la industria y la academia, implementando los frameworks **VAEP** (Decroos et al., 2019), **xT** (Singh, 2019) y la representación **SPADL**, que son hoy referencia en los departamentos de análisis de los principales clubes europeos.

---

## Objetivo

Construir un pipeline reproducible y documentado que permita:

- Transformar datos crudos de eventos de partido en representaciones estructuradas aptas para modelado
- Estimar el **valor individual de cada acción** sobre el césped mediante aprendizaje supervisado
- Identificar **perfiles y roles de juego** mediante técnicas de clustering y reducción de dimensionalidad
- Generar **rankings, visualizaciones y herramientas de scouting** basados en evidencia cuantitativa

---

## Preguntas que exploramos

> *"El fútbol es un deporte lleno de incertidumbre. Sin embargo, los datos nos permiten minimizar el impacto del azar y revelar la verdadera capacidad de equipos y jugadores."*

A lo largo del proyecto buscamos responder:

- ¿Desde qué zonas del campo se generan más oportunidades de gol, y cómo varía esto entre ligas?
- ¿Cuánto vale un pase progresivo comparado con un regate en el área? ¿Y una recuperación defensiva?
- ¿Qué jugadores crean más valor real ajustado por posesión, independientemente de si marcaron o no?
- ¿Existen perfiles de juego universales que se repitan entre ligas, o cada competición tiene sus propios arquetipos?
- ¿Puede un modelo encontrar reemplazantes funcionales para un jugador dado, basándose solo en su comportamiento en el campo?
- ¿Qué tan correlacionados están xT y VAEP? ¿Cuándo divergen y qué nos dice esa divergencia sobre un jugador?
- ¿Qué features tienen mayor impacto en la probabilidad de que una acción derive en gol?

---

## Dataset

Los datos provienen de **Wyscout**, una de las principales compañías de datos deportivos, y fueron publicados bajo licencia **CC BY 4.0**.

| Dimensión | Detalle |
|---|---|
| **Temporada** | 2017/18 |
| **Competiciones** | Premier League · La Liga · Serie A · Bundesliga · Ligue 1 · Euro 2016 · Mundial 2018 |
| **Equipos** | 142 |
| **Partidos** | 1.941 |
| **Jugadores únicos** | 4.299 |
| **Eventos de juego** | 3.251.294 |
| **Formato original** | JSON (Wyscout API schema) |
| **Formato procesado** | Parquet (optimizado, columnar) |

Cada evento contiene: coordenadas de inicio y fin de la acción (sistema 0–100), tipo de evento, sub-tipo, jugador, equipo, minuto, período y etiquetas de resultado. El dataset cubre la **totalidad de acciones** de cada partido — tiros, pases, regates, duelos, recuperaciones, faltas y más.

El formato **Parquet** se usa en los notebooks para una carga hasta 10× más rápida respecto al JSON original y un consumo de memoria reducido en más del 60%.

Los datos se pueden descargar desde: [mega.nz/folder/dpIxiYrZ#CBR9Igt4hgLuknBqEPYXeA](https://mega.nz/folder/dpIxiYrZ#CBR9Igt4hgLuknBqEPYXeA)

---

## Estructura del repositorio

```
.
├── data/
│   ├──events/
│   │   ├──events_England.parquet
│   │   ├──events_European_Championship.parquet
│   │   ├──events_France.parquet
│   │   ├──events_Germany.parquet
│   │   ├──events_Italy.parquet
│   │   ├──events_Spain.parquet
│   │   └──events_World_Cup.parquet
│   ├──matches/
│   │   ├──matches_England.json
│   │   ├──matches_European_Championship.json
│   │   ├──matches_France.json
│   │   ├──matches_Germany.json
│   │   ├──matches_Italy.json
│   │   ├──matches_Spain.json
│   │   └──matches_World_Cup.json
│   ├──coaches.json
│   ├──competitions.json
│   ├──eventid2name.csv
│   ├──players.json
│   ├──referees.json
│   ├──tags2name.csv
│   └──teams.json
│
├── notebooks/
│   ├── P1_Analisis_Visualizacion.ipynb      # Hito 1: EDA + Visualizaciones
│   ├── P2_EDA_Curacion_SPADL.ipynb          # Hito 2: Curación + SPADL
│   └── P3_Supervisado_NoSupervisado.ipynb   # Hito 3: ML supervisado + clustering
│
├── requirements.txt
└── README.md
```

---

## Hitos del proyecto

### Práctico 1 — Análisis y Visualización
Exploración visual del dataset completo. Construcción de shot maps, heat maps de densidad, redes de pases y radares de jugadores. Implementación de un modelo baseline de **Expected Goals (xG)** con regresión logística.

### Práctico 2 — Exploración y Curación de Datos
Análisis riguroso de calidad de datos, detección de outliers y valores faltantes. Conversión del formato Wyscout al estándar **SPADL** usando `socceraction`. Feature engineering contextual y normalización por posición y minutos jugados.

### Práctico 3 — Aprendizaje Supervisado y No Supervisado
Implementación completa de **xT** (grilla iterativa) y **VAEP** (XGBoost + LightGBM con validación cruzada por partido). Explicabilidad con **SHAP**. Clustering con K-Means, visualización con **UMAP** y sistema de scouting por similitud coseno.

### Video de presentación final de mentoría

### Jornadas Presentación de mentorías

---

## Stack tecnológico

```python
# Datos y transformación
pandas · numpy · pyarrow · socceraction

# Visualización
mplsoccer · matplotlib · seaborn · plotly

# Machine Learning
scikit-learn · xgboost · lightgbm · shap

# Reducción dimensional
umap-learn · scipy
```

---

## Referencias académicas

- Decroos, T., Bransen, L., Van Haaren, J., & Davis, J. (2019). **Actions Speak Louder than Goals: Valuing Player Actions in Football.** *KDD 2019.*
- Van Roy, M., Robberechts, P., Yang, W. C., De Raedt, L., & Davis, J. (2020). **Valuing on-the-ball actions in soccer: a critical comparison of XT and VAEP.** *AAAI Workshop.*
- Singh, K. (2019). **Introducing Expected Threat.** *Statsbomb Blog.*

---

## Instalación

```bash
git clone https://github.com/guillealonso/futbol-ciencia-datos-2026.git
cd futbol-ciencia-datos-2026
pip install -r requirements.txt
```

Descargá los datos desde el enlace indicado y ya podés correr los notebooks en orden.

---

## Sobre el proyecto

Este trabajo forma parte de la **Diplomatura en Ciencia de Datos, Aprendizaje Automático y sus Aplicaciones** (DiploDatos) de la **Facultad de Matemática, Astronomía, Física y Computación** de la **Universidad Nacional de Córdoba**, Argentina.

---

<p align="center">
  <strong>Guillermo Alonso</strong><br>
  📧 <a href="mailto:ing.guillermoalonso@gmail.com">ing.guillermoalonso@gmail.com</a><br>
  DiploDatos 2026 · FaMAF · UNC
</p>

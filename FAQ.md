# ❓ Preguntas frecuentes (FAQ)

Bienvenido a la sección de Preguntas Frecuentes del repositorio. Haz clic en cada pregunta para ver la respuesta.

---

## Parquet

<details>
<summary><b>¿Por qué convertimos los datos de Wyscout de JSON a Parquet? ¿Cómo se hace y es un estándar?</b></summary>

Convertimos a Parquet principalmente por eficiencia de almacenamiento y velocidad de lectura. Parquet es un formato columnar que comprime y serializa datos de forma más compacta que JSON, por lo que es habitual usarlo cuando los datasets son grandes o se quieren realizar lecturas selectivas.

Ejemplo sencillo con pandas:

```python
import pandas as pd
df = pd.read_json("events.json", lines=True)
df.to_parquet("events.parquet", index=False)
# y para leer:
df = pd.read_parquet("events.parquet")
```

No es obligatorio usar Parquet, pero es muy común en proyectos de datos por su rendimiento y compatibilidad con herramientas de análisis.

</details>

## Etiquetado (tagging)

<details>
<summary><b>¿Cómo se etiquetan los eventos en Wyscout y otras empresas? ¿Existe un estándar como SPADL?</b></summary>

El etiquetado suele hacerse mediante aplicaciones (tablets o software) donde un operador marca los eventos viendo el video. Las etiquetas son configurables según las necesidades del proveedor o del proyecto.

SPADL es un ejemplo de formato estandarizado para representar acciones de fútbol y facilita comparar o integrar datos de distintos proveedores. No es el único formato, pero sí uno de los más usados en la comunidad académica/práctica. Algunas empresas complementan el etiquetado manual con técnicas de visión por computadora para extraer información adicional a partir del video.

</details>

## Normalización de métricas

<details>
<summary><b>¿A qué se refiere normalizar métricas? ¿Tiene relación con features/características?</b></summary>

Normalizar significa llevar valores a una escala comparable. Las métricas pueden ser características (features) y, para poder compararlas o combinarlas, muchas veces las escalamos.

Ejemplos frecuentes:
- Normalizar por tiempo de juego (por 90 minutos):

	- Si un jugador tiene 10 goles en 900 minutos jugados, su tasa por 90 minutos es 10 / (900/90) = 1.0 goles/90'.
	- Si otro tiene 10 goles en 450 minutos, su tasa es 10 / (450/90) = 2.0 goles/90'.

- Escalados estadísticos: `min-max` o `z-score` cuando las features tienen rangos muy distintos.

La normalización se usa tanto para análisis descriptivo como para modelos que requieren features en la misma escala.

</details>

## Feature engineering (TP1)

<details>
<summary><b>¿Todas las características del notebook del TP1 son producto de feature engineering?</b></summary>

No todas las columnas provienen de feature engineering. En general distinguimos:

- Features crudas: columnas que vienen directamente del dataset (por ejemplo `eventType`, `teamId`, `playerId`).
- Features creadas: métricas derivadas combinando o transformando columnas originales (por ejemplo `pases_completados`, `porcentaje_pases`, `xG_total`, `minutos_jugados` o métricas normalizadas por 90 minutos).

Muchas de las métricas útiles del TP1 se obtienen mediante feature engineering sobre los datos originales.

</details>

---


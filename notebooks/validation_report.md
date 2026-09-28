# Informe de Validación del Dataset
> Generado: 2026-09-21 12:54:12  
> Archivo: `notebooks/spadl_curado_PL_2017.parquet`  
> Validador: `validate_dataset.py` v1.0.0

---

## Resultado general

### ✅ PASSED

El dataset cumple todos los requisitos contractuales para ejecutar P3.

| Métrica | Valor |
|---|---|
| Total de checks | 39 |
| ✅ Passed | 38 |
| ⚠️ Warnings | 1 |
| ❌ Failed | 0 |

---

## Detalle por categoría

### Archivo

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Archivo Parquet existe | notebooks/spadl_curado_PL_2017.parquet |

### Volumen

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Cantidad mínima de acciones | 474,866 filas (mínimo requerido: 50,000) |

### Schema

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Columna 'game_id' | dtype=int64 (esperado: int) |
| ✅ PASSED | Columna 'period_id' | dtype=int64 (esperado: int) |
| ✅ PASSED | Columna 'time_seconds' | dtype=float64 (esperado: float) |
| ✅ PASSED | Columna 'team_id' | dtype=int64 (esperado: int) |
| ✅ PASSED | Columna 'player_id' | dtype=int64 (esperado: int) |
| ✅ PASSED | Columna 'start_x' | dtype=float64 (esperado: float) |
| ✅ PASSED | Columna 'start_y' | dtype=float64 (esperado: float) |
| ✅ PASSED | Columna 'end_x' | dtype=float64 (esperado: float) |
| ✅ PASSED | Columna 'end_y' | dtype=float64 (esperado: float) |
| ✅ PASSED | Columna 'action_type_id' | dtype=int64 (esperado: int) |
| ✅ PASSED | Columna 'type_name' | dtype=object (esperado: object) |
| ✅ PASSED | Columna 'bodypart_id' | dtype=int64 (esperado: int) |
| ✅ PASSED | Columna 'bodypart_name' | dtype=object (esperado: object) |
| ✅ PASSED | Columna 'result_id' | dtype=int64 (esperado: int) |
| ✅ PASSED | Columna 'result_name' | dtype=object (esperado: object) |

### Calidad

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Nulos en 'game_id' | Sin valores nulos |
| ✅ PASSED | Nulos en 'player_id' | Sin valores nulos |
| ✅ PASSED | Nulos en 'team_id' | Sin valores nulos |
| ✅ PASSED | Nulos en 'start_x' | Sin valores nulos |
| ✅ PASSED | Nulos en 'start_y' | Sin valores nulos |
| ✅ PASSED | Nulos en 'type_name' | Sin valores nulos |
| ✅ PASSED | Nulos en 'result_name' | Sin valores nulos |
| ✅ PASSED | Sin duplicados exactos | 0 filas duplicadas detectadas |

### Coordenadas

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Rango coordenada 'start_x' | 0 valores fuera de [0.0, 105.0] (0.0000%) |
| ✅ PASSED | Rango coordenada 'start_y' | 0 valores fuera de [0.0, 68.0] (0.0000%) |
| ✅ PASSED | Rango coordenada 'end_x' | 0 valores fuera de [0.0, 105.0] (0.0000%) |
| ✅ PASSED | Rango coordenada 'end_y' | 0 valores fuera de [0.0, 68.0] (0.0000%) |

### Categorías

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Valores de 'type_name' | Tipos ausentes (puede ser normal): {'keeper_pick_up', 'freekick_shot', 'keeper_claim', 'keeper_punch', 'penalty_shot', 'non_action', 'bad_touch'} |
| ✅ PASSED | Valores de 'result_name' | Tipos ausentes (puede ser normal): {'red_card', 'yellow_card'} |
| ✅ PASSED | Valores de 'bodypart_name' | Todos los valores en Partes del cuerpo SPADL son válidos |
| ✅ PASSED | Valores de 'period_id' | 0 valores fuera de {1, 2, 3, 4, 5} |

### Cobertura

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Partidos únicos | 380 (mínimo: 200) |
| ✅ PASSED | Jugadores únicos | 557 (mínimo: 300) |
| ✅ PASSED | Tipos de acción únicos | 18 tipos presentes (mínimo: 12) |
| ⚠️ WARNING | Distribución de acciones por partido | Media: 1250 | P1: 1018 | P99: 1493 | Partidos atípicos: 8 |

### P3-Específico

| Estado | Check | Detalle |
|---|---|---|
| ✅ PASSED | Tiros presentes (shot/penalty/freekick) | 1.80% de acciones son tiros (mínimo: 0.5%) |
| ✅ PASSED | Orden temporal dentro de períodos | 0 inversiones temporales (0.0000%) |

---

## ⚠️ Warnings — revisar antes de continuar

- **Distribución de acciones por partido** (Cobertura): Media: 1250 | P1: 1018 | P99: 1493 | Partidos atípicos: 8
  - 📄 *Ver análisis detallado, fixture y justificación táctica en:* **[analisis_partidos_atipicos.md](./analisis_partidos_atipicos.md)**

---

## 🎯 Conclusión final

### Estado: **APROBADO PARA PRÁCTICO 3 (P3)**

1. **Cumplimiento Contractual:** El dataset cumple satisfactoriamente con **38 de 39 checks** (0 fallas críticas), superando los requerimientos de schema (`action_type_id`, tipos de datos), volumen, calidad (0 nulos críticos, 0 duplicados exactos, 0 inversiones temporales) y cobertura.
2. **Evaluación de Warnings:** Las advertencias estadísticas (como la distribución por partido) corresponden a la variabilidad empírica natural de los estilos de juego reales y han sido analizadas en detalle sin detectarse corrupción ni truncamiento de datos.
3. **Dictamen:** El dataset cuenta con la calidad, integridad y consistencia requeridas para el entrenamiento de modelos de valoración de acciones en el Práctico 3.

---

## Contexto del contrato

Este informe verifica el contrato definido en `DATASET_CARD.md`.
Los umbrales aplicados son:

| Parámetro | Umbral |
|---|---|
| `max_missing_pct` | `2.0` |
| `max_missing_pct_warn` | `0.5` |
| `min_actions` | `50000` |
| `min_games` | `200` |
| `min_players` | `300` |
| `min_action_types` | `12` |
| `max_coord_outlier_pct` | `0.1` |
| `min_shots_pct` | `0.5` |
| `max_time_anomaly_pct` | `0.5` |

---

*DiploDatos 2026 · Mentoría: Ciencia de Datos Aplicada al Fútbol · FaMAF, UNC*
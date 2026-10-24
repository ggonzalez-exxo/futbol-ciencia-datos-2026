# Tareas para continuar el proyecto

> Proyecto: **Ciencia de Datos Aplicada al Fútbol — DiploDatos 2026**.
> Este archivo es el backlog de continuación: video final, HyperFrames,
> Kdenlive, audio, QA y mejoras opcionales del proyecto de datos.

## Fechas críticas

| Fecha | Entregable |
|---|---|
| **26/10/2026** | Video de presentación final de mentoría |
| **04–05/12/2026** | Presentación de mentorías |

> Faltan pocos días para el video. La estrategia es **no bloquear la entrega
> con el rediseño HyperFrames**: si una pieza no queda mejor que la versión
> matplotlib, se usa la versión anterior como fallback.

## Prioridades

- **P0** — imprescindible para el video del 26/10.
- **P1** — mejora importante, hacer si hay margen.
- **P2** — post-entrega o presentación de diciembre.

---

## A. Video final (P0)

- [ ] Cerrar el guión definitivo (`guion_video_final.md`) y congelar la VO.
- [ ] Grabar la voz en off por escena (Audacity), un WAV por escena.
- [ ] Normalizar la VO a −16 LUFS / picos −3 dB.
- [ ] Elegir la jugada recurrente y conseguir el clip (con derechos de uso).
- [ ] Conseguir 10–15 clips de b-roll de fútbol.
- [ ] Elegir música y 3–5 SFX.
- [ ] Armar el master en Kdenlive (V1 footage, V2 gráficos, A1 VO, A2 música, A3 ambiente).
- [ ] Exportar H.264 1080p30, CRF 20, audio AAC 192 kbps.
- [ ] Revisar en celular y en proyector antes de entregar.

## B. HyperFrames — rediseño estético (P0/P1)

- [x] Contador rediseñado (grafito + marfil + ámbar, sin grid).
- [x] Revisar el contador con `check` + `snapshot`.
- [x] Rediseñar `xt.html`:
  - cancha más grande, líneas claras, viridis;
  - panel derecho sin tarjeta;
  - sin grid de fondo.
- [x] Rediseñar `heatmap.html`:
  - viridis + blur/clipPath para suavizar;
  - revelar por opacidad (sin agujeros negros);
  - stats simples.
- [x] Rediseñar `umap.html`:
  - puntos más grandes, layout ajustado;
  - etiquetas con línea guía, sin pills;
  - sin grid.
- [x] `check --json` verde en las 4.
- [x] Render `--quality looks` del master (y de las 4 piezas individuales en `video/animaciones/`).
- [ ] Comparar con las versiones matplotlib y decidir ganador por pieza.
- [ ] (P1) Sumar capítulos entre TP1/TP2/TP3 y lower thirds.
- [ ] (P1) Evaluar shot map animado, red de pases y radares como piezas extra.
- [ ] (P2) Explorar el bloque `count-up`/`number-wheel` del registry para el contador, si aporta.

## C. Kdenlive (P0)

- [x] Instalar `cli-anything-kdenlive` en `.venv-kdenlive`.
- [x] Smoke test: MLT con 2 clips y 2 guías; validado con melt 7.36.1 (queda abrirlo en Kdenlive GUI).
- [x] Definir `video/edl.json`:
  - escenas, assets, pistas, in/out, guías;
  - guías en los límites del guión (0:50 / 2:00 / 3:30 / 6:30 / 9:00 / 10:20 / 12:00);
  - piezas HF individuales en V2 (no hace falta cortar el master).
- [x] Builder `video/scripts/build_kdenlive_timeline.py`:
  - duraciones con `ffprobe`;
  - API core de la CLI (en proceso, `.venv-kdenlive`);
  - guarda `video/kdenlive/proyecto.json` y exporta MLT validado con melt.
- [ ] Montar el timeline y pulir en la GUI:
  - transiciones, títulos, color, audio.
- [ ] Render final desde Kdenlive.

## D. Audio y VO (P0)

- [ ] Grabar y editar la VO.
- [ ] Música: 1–2 tracks; ducking bajo la VO.
- [ ] SFX: impactos de corte, whoosh de transición, ambiente de partido.
- [ ] Mezcla final: VO clara, música −22 dB bajo voz, ambiente −28 dB.
- [ ] (P1) Subtítulos: usar `captions-overlay` si se queman.

## E. Assets y gráficos (P1)

- [ ] Revisar `video/graficos/manifest.csv` y descartar figuras que no se usan.
- [ ] Exportar los gráficos que falten con fondo transparente cuando corresponda.
- [ ] Rehacer el shot map / red de pases / radares si se animan.
- [ ] Preparar placas de título y placa final con QR al repo.
- [ ] Unificar tipografía y paleta entre PNGs y piezas HyperFrames.

## F. QA y entrega (P0)

- [ ] Verificar duración total (~12–13 min) y ritmo.
- [ ] Verificar sincronía VO–imagen en cada escena.
- [ ] Verificar legibilidad de textos en celular.
- [ ] Verificar niveles de audio y ausencia de clipping.
- [ ] Verificar que no haya frames negros, textos cortados ni artefactos.
- [ ] Export final y copia de respaldo.
- [ ] Entregar en el aula virtual antes del 26/10.

## G. Repo y documentación (P1)

- [ ] Agregar `video/hyperframes/.hyperframes/` al `.gitignore`.
- [ ] Decidir qué MP4 se versionan (¿solo el master final?).
- [ ] Actualizar `video/README.md` con el flujo HyperFrames definitivo.
- [ ] Actualizar `README.md` raíz con la sección del video final.
- [ ] Documentar el pipeline: datos → JSON → HyperFrames → master → Kdenlive.
- [ ] Arreglar el `.venv` roto o documentar el uso de `.venv-video`.

## H. Presentación de diciembre (P2)

- [ ] Armar una versión de deck (puede reutilizar los PNGs y frames del video).
- [ ] Preparar guion de exposición de 10–15 min.
- [ ] Ensayar la demo del sistema de scouting.
- [ ] Preparar respuestas a preguntas frecuentes (xG vs xT vs VAEP, límites, datos).

## I. Mejoras opcionales del proyecto de datos (P2)

- [ ] Incorporar minutos jugados reales (hoy “p90” es por partido).
- [ ] Completar las 5 ligas (hoy el foco es España, Inglaterra e Italia).
- [ ] Calibrar xG (Platt scaling / isotónica) y comparar con el baseline.
- [ ] Probar features nuevas para VAEP (presión, contexto, marcador).
- [ ] Validar la estabilidad de clusters con distintas semillas y k.
- [ ] Documentar limitaciones: xT y arqueros, VAEP y minutos, sesgo de anotación.
- [ ] Publicar un notebook de reproducción end-to-end.

---

## Plan de 72 horas (23–26/10)

### Día 1 — 23/10
- [ ] Terminar el rediseño de xT, heatmap y UMAP.
- [ ] `check` + `snapshot` + master render.
- [ ] Grabar la VO completa.

### Día 2 — 24/10
- [ ] Elegir clips de b-roll y la jugada recurrente.
- [ ] Montar el timeline en Kdenlive (estructura + VO).
- [ ] Música y SFX.

### Día 3 — 25/10
- [ ] Pulido: transiciones, títulos, color, audio.
- [ ] QA en celular/proyector.
- [ ] Export final.

### Día 4 — 26/10
- [ ] Entrega y backup.
- [ ] (Si algo falla) usar los MP4 de matplotlib como fallback.

---

## Riesgos

| Riesgo | Mitigación |
|---|---|
| El rediseño HyperFrames no convence a tiempo | Usar los MP4 de matplotlib ya generados |
| La CLI de Kdenlive no abre bien el MLT | Smoke test temprano; si falla, montar a mano en la GUI |
| La VO se retrasa | Grabar por escena y montar en paralelo |
| Faltan clips de fútbol | Priorizar la jugada recurrente y reducir b-roll |
| El master HyperFrames es mudo | El audio entra en Kdenlive; no es bloqueante |

## Definición de “video terminado”

- Duración entre 12 y 13 minutos.
- VO sincronizada y audible.
- Las 4 piezas de datos se ven al menos tan bien como las versiones matplotlib.
- Sin errores de texto, frames negros ni desincronización.
- Export 1080p30 reproducible.
- Archivo entregado antes del 26/10.

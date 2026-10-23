# Siguientes pasos — conversación de video

> Estado al 2026-10-23. Este archivo es el traspaso corto de la conversación:
> qué quedó hecho, qué se estaba cambiando y qué conviene hacer ahora.

## Estado actual

### Commits

- `b3a4b58` — estructura del video + animaciones base (matplotlib/ffmpeg).
- `7f525a2` — proyecto HyperFrames con 4 composiciones (contador, xT, heatmap VAEP, UMAP).

### Infraestructura verificada

- **Node 22.23.4** instalado con `nvm` (HyperFrames exige ≥22).
- **HyperFrames CLI 0.8.189** funcionando. `usage --json` responde `unknown` (harness no soportado), pero renderiza.
- **Kdenlive 25.12.3** y **melt 7.36.1** instalados.
- **`cli-anything-kdenlive` 1.0.0** probado en un venv temporal (`/tmp/opencode/kdenliveenv`), no instalado en el repo.
- El `.venv` original está roto (apunta a Python 3.12 inexistente). Para datos/video usar `.venv-video` o el venv temporal de pruebas.

### Assets existentes

- `video/animaciones/`:
  - `esc00_contador_eventos.mp4`, `esc05_xt_grilla.mp4`, `esc05_heatmap_vaep.mp4`, `esc05_umap_clusters.mp4` (matplotlib, primera versión).
  - `hf_datos_4piezas.mp4` (master HyperFrames, 17 s, estética vieja).
- `video/graficos/` — 60 figuras extraídas de los notebooks.
- `video/hyperframes/` — proyecto HyperFrames con `index.html` y 4 composiciones.

### Problema abierto

Las 4 piezas HyperFrames **no convencen estéticamente**: se leen como un dashboard
tech (verde neón, grids, tarjetas, mucho aire). Gustaban más las primeras
(matplotlib): más limpias, científicas, con viridis y cancha de mplsoccer.

**Decisión tomada:** rediseñar con una estética editorial:
- Fondo grafito `#0B0E11` / `#0C0F12`.
- Texto marfil `#F2F4F3`, secundario `#93A0A8`.
- Acento ámbar `#F2B544` (reemplaza el verde neón).
- Datos con **viridis**.
- Sin grid de fondo, sin tarjetas con borde/sombra, sin pills.
- Tipografía más grande y en sentence case.

**Hecho:** `compositions/counter.html` ya fue reescrito con esta paleta (sin commitear).
**Pendiente:** rehacer `xt.html`, `heatmap.html` y `umap.html`.

---

## Checklist inmediato

### 1. Terminar el rediseño HyperFrames

- [x] Revisar el contador rediseñado (`counter.html`) con `check` y `snapshot`.
- [x] Rediseñar `xt.html`:
  - cancha más grande (~1300×842), líneas claras, viridis;
  - panel derecho sin tarjeta (iteración, Δmax, colorbar);
  - sin grid de fondo.
- [x] Rediseñar `heatmap.html`:
  - usar viridis y **suavizar las celdas** (`filter: blur` + `clipPath`);
  - revelar por opacidad, no ocultando celdas (evitar los “agujeros” negros);
  - títulos/stats simples, sin tarjetas.
- [x] Rediseñar `umap.html`:
  - puntos más grandes, layout más ajustado;
  - etiquetas de cluster y de Messi/CR con línea guía, sin pills;
  - sin grid de fondo.
- [x] `check --json` verde en las 4 (0 errores, 0 warnings).
- [x] `snapshot` de cada pieza y revisar frames (verificado por análisis de píxeles: viridis activo en xT/heatmap, clusters con paleta nueva en UMAP; ojo: `assets/data/umap.js` trae colores viejos, la composición ahora fuerza la paleta editorial).
- [ ] Render `--quality looks` del master.

### 2. Validar contra las versiones anteriores

- [ ] Comparar frame a frame con `esc00_contador_eventos.mp4`, `esc05_xt_grilla.mp4`, `esc05_heatmap_vaep.mp4`, `esc05_umap_clusters.mp4`.
- [ ] Si el heatmap reconstruido sigue sin gustar, usar los **PNG originales de VAEP** como asset y animar un reveal suave.
- [ ] Confirmar duración y orden del master: 3,2 / 4,2 / 4,2 / 5,4 s.

### 3. Pasar a Kdenlive

- [ ] Instalar `cli-anything-kdenlive` en un entorno del repo (`.venv-kdenlive`).
- [ ] Smoke test: MLT de 30 s con 2 clips y 2 guías, abrirlo en Kdenlive 25.12.3.
- [ ] Escribir `video/edl.json` con escenas, assets, pistas, in/out y guías.
- [ ] Builder `video/scripts/build_kdenlive_timeline.py`:
  - `ffprobe` para duraciones;
  - API core de la CLI (no invocaciones separadas: el estado no persiste);
  - exportar JSON + MLT.
- [ ] Montar en Kdenlive: V1 footage, V2 gráficos, A1 VO, A2 música, A3 ambiente.
- [ ] Cortar el master HyperFrames en 3,2 / 7,4 / 11,6 s.

### 4. Audio y VO

- [ ] Grabar VO por escena (Audacity), normalizar a −16 LUFS.
- [ ] Música y SFX; ducking manual en Kdenlive.
- [ ] Subtítulos (si se decide): usar la doctrina de `captions-overlay`.

### 5. Higiene del repo

- [ ] Agregar `video/hyperframes/.hyperframes/` al `.gitignore` (artefactos de check/snapshot no deberían versionarse).
- [ ] Decidir si se commitean `hf_counter.mp4`, `hf_counter_root.mp4` y `hf_datos_4piezas.mp4` o solo el master final.
- [ ] Commit del rediseño cuando esté aprobado.

---

## Comandos útiles

```bash
# Node 22
export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 22

# Datos para HyperFrames
/tmp/opencode/videoenv/bin/python video/scripts/export_hf_data.py

# HyperFrames (usar la versión pinneada; `npx hyperframes` choca con el package local)
cd video/hyperframes
npx --yes hyperframes@0.8.189 check --json
npx --yes hyperframes@0.8.189 snapshot --at 2,5,10,16
npx --yes hyperframes@0.8.189 render --quality looks -o ../animaciones/hf_datos_4piezas.mp4

# Kdenlive CLI (temporal)
/tmp/opencode/kdenliveenv/bin/cli-anything-kdenlive --help
```

## Decisiones abiertas

1. ¿Heatmap HyperFrames reconstruido con viridis + blur, o PNG original de VAEP animado?
2. ¿UMAP con etiquetas sobre el plot o leyenda lateral?
3. ¿Se mantiene el master HyperFrames único (se corta en Kdenlive) o se renderiza pieza por pieza?
4. ¿Los MP4 de matplotlib quedan como fallback o se descartan?

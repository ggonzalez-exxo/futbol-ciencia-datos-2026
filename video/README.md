# Video final — assets y generación automática

Esta carpeta contiene todo lo necesario para armar el video del guión
[`guion_video_final.md`](../guion_video_final.md) en Kdenlive.

```
video/
├── footage/          # clips de fútbol (b-roll, jugadas)
├── graficos/         # figuras exportadas de los notebooks (PNG)
│   ├── esc03/        # TP1
│   ├── esc04/        # TP2
│   ├── esc05/        # TP3
│   ├── otros/        # figuras no mapeadas a una escena
│   └── manifest.csv  # inventario de figuras extraídas
├── animaciones/      # MP4 generados por generar_animaciones.py
├── voz/              # grabaciones de voz en off
├── musica/           # música y SFX
├── titulos/          # placas y títulos
└── scripts/
    ├── extraer_figuras.py
    ├── generar_animaciones.py
    └── requirements.txt
```

---

## 1. Preparar el entorno

> El `.venv` original del repo fue creado con Python 3.12 y puede no funcionar
> si el sistema ya no tiene ese intérprete. Para el video conviene un entorno
> aparte.

Con `uv` (recomendado, ya está instalado en este equipo):

```bash
cd futbol-ciencia-datos-2026
uv venv --python 3.12 .venv-video
uv pip install --python .venv-video/bin/python -r video/scripts/requirements.txt
```

Alternativa con `venv`:

```bash
python3.12 -m venv .venv-video
source .venv-video/bin/activate
pip install -r video/scripts/requirements.txt
```

También necesitás **ffmpeg** (Kdenlive ya lo usa). Verificá con:

```bash
ffmpeg -version
```

---

## 2. Generar las figuras y animaciones

Ejecutá siempre en este orden:

```bash
# 1) Extrae las 60 figuras incrustadas en los notebooks
.venv-video/bin/python video/scripts/extraer_figuras.py

# 2) Genera las animaciones (contador, xT, heat maps VAEP y UMAP)
.venv-video/bin/python video/scripts/generar_animaciones.py
```

O en un solo paso (crea las figuras y las animaciones):

```bash
bash video/scripts/generar_todo.sh
```

La segunda corrida tarda unos **2–4 minutos** (el UMAP ~20 s y el renderizado
el resto). Al terminar, `video/animaciones/` contiene:

| Archivo | Escena | Duración | Qué muestra |
|---|---|---|---|
| `esc00_contador_eventos.mp4` | 0 | 3,0 s | Contador 0 → 3.251.294 eventos |
| `esc05_xt_grilla.mp4` | 5a | 3,8 s | Grilla xT 16×12 iterando hasta converger |
| `esc05_heatmap_vaep.mp4` | 5a | 3,8 s | Messi vs Cristiano: VAEP por zona iluminándose |
| `esc05_umap_clusters.mp4` | 5b | 4,3 s | 1.201 jugadores apareciendo por arquetipo |

Además se generan estos PNG de referencia:

- `video/graficos/esc05/esc05_xt_grilla_final.png`
- `video/graficos/esc05/esc05_heatmap_vaep_messi_final.png`
- `video/graficos/esc05/esc05_umap_final.png`
- `video/animaciones/umap_embedding.csv` (coordenadas UMAP por jugador)

### Version HyperFrames (recomendada)

Las 4 animaciones también existen como **composiciones HyperFrames** en
`video/hyperframes/` — HTML + GSAP, vectores más nítidos y mejor motion:

```bash
cd video/hyperframes
npm run check                       # lint + runtime + layout + contrast
npx hyperframes snapshot --at 2,5,10,16   # ver frames antes de renderizar
npm run render                      # master con las 4 piezas (17 s)
```

- `compositions/counter.html` — contador 0 → 3.251.294 (3,2 s)
- `compositions/xt.html` — grilla xT iterando (4,2 s)
- `compositions/heatmap.html` — Messi vs Cristiano, VAEP por zona (4,2 s)
- `compositions/umap.html` — 1.201 jugadores por arquetipo (5,4 s)

Los datos se regeneran con `video/scripts/export_hf_data.py` (escribe
`assets/data/*.js`); el master se renderiza a `video/animaciones/hf_datos_4piezas.mp4`
y en Kdenlive se corta en los límites de escena. Estos MP4 reemplazan a los
generados con matplotlib; los umbrates de escena están en el guión.

Para generar solo una parte:

```bash
.venv-video/bin/python video/scripts/generar_animaciones.py --solo xt
.venv-video/bin/python video/scripts/generar_animaciones.py --solo heatmap
.venv-video/bin/python video/scripts/generar_animaciones.py --solo umap,contador
```

---

## 3. Importar en Kdenlive

1. **Nuevo proyecto** → perfil **1920×1080, 30 fps**.
2. Arrastrá `video/animaciones/` y `video/graficos/` al **Project Bin**.
3. Armá las pistas como en el guión:

| Pista | Contenido |
|---|---|
| V2 | gráficos PNG, animaciones superpuestas |
| V1 | clips de fútbol (b-roll y jugada recurrente) |
| A1 | voz en off |
| A2 | música |
| A3 | sonido ambiente / SFX |

4. Las animaciones ya vienen a 1920×1080 y con el mismo fondo oscuro
   (`#0E1116`): podés ponerlas en V1 (pantalla completa) o en V2.
5. Los PNG de los notebooks tienen **fondo blanco**. Si los usás como overlay,
   podés:
   - dejarlos como “tarjetas” sobre el video, o
   - aplicar **Chroma Key / Color to Alpha** con blanco para volverlos
     transparentes.

### Mapa rápido de assets por escena

- **Escena 0:** `esc00_contador_eventos.mp4` + b-roll de goles.
- **Escena 3 (TP1):** `graficos/esc03/*` (shot maps, heat maps, red de pases,
  radares, pressing).
- **Escena 4 (TP2):** `graficos/esc04/*` (heatmap de eventos, distribución
  temporal, features, sesgo posicional) + la jugada recurrente.
- **Escena 5 (TP3):** `esc05_xt_grilla.mp4`, `esc05_heatmap_vaep.mp4`,
  `esc05_umap_clusters.mp4` y `graficos/esc05/*` (SHAP, clusters, scouting).
- **Escena 6:** la jugada recurrente y la placa final.

---

## 4. Cómo se generó cada animación

- **Contador:** composición con PIL; no depende de datos.
- **Grilla xT:** se recalcula desde `notebooks/spadl_curado_PL_2017.parquet`
  con una grilla 16×12. La escala coincide con la del notebook P3 (puede haber
  diferencias mínimas por la definición de “movimiento”).
- **Heat maps VAEP:** se parte de la figura real exportada por P3
  (`graficos/esc05/esc05_heatmap_vaep_messi_cr_dybala.png`), se recortan los
  paneles de Messi y Cristiano y se revelan las celdas de menor a mayor
  intensidad. No es un dato recalculado: es la figura VAEP del notebook.
- **UMAP:** se reconstruyen los vectores de jugador (proporciones de tipos de
  acción + `vaep_p90`, `off_total`, `def_total`) desde el parquet y el CSV de
  rankings, y se corre UMAP. Los colores usan las etiquetas de cluster
  guardadas en `rankings_jugadores_PL_2017.csv`. La reconstrucción reproduce
  los clusters del notebook con un ARI ≈ 0,98.

---

## 5. Personalización

En `scripts/generar_animaciones.py`:

- `PLAYERS_HEATMAP`: nombres y métricas que aparecen bajo cada heat map.
- `PANEL_BOXES`: recortes de los paneles dentro de la figura de 3 mapas.
  Si cambiás la figura de origen, ajustá estas fracciones.
- `CLUSTER_NAMES` y `CLUSTER_COLORS`: nombres y colores de los arquetipos.
- `stars`: jugadores que se anotan en el UMAP y su offset.
- `W, H`, `FPS`: resolución y velocidad.
- `--solo`: para regenerar solo una animación.

En `scripts/extraer_figuras.py`:

- `ALIASES`: mapea celdas de notebook a nombres amigables y escenas.
- `NOTEBOOKS`: rutas de los notebooks.

---

## 6. Problemas frecuentes

- **`ffmpeg: command not found`:** instalalo con el gestor de paquetes del
  sistema (`sudo apt install ffmpeg` en Ubuntu/Debian).
- **`ModuleNotFoundError: pandas` / `umap`:** estás usando el intérprete
  equivocado. Asegurate de ejecutar con `.venv-video/bin/python` o de activar
  el entorno.
- **El UMAP tarda o falla:** la primera ejecución compila numba; puede tardar
  un poco más. Si vuelve a fallar, probá `--solo xt` y `--solo umap` por
  separado.
- **Los frames no coinciden de tamaño:** el script fuerza 1920×1080 con
  `savefig.bbox = "standard"`. Si modificás el guardado, no uses
  `bbox_inches="tight"` en animaciones.
- **La figura VAEP no aparece:** corré primero `extraer_figuras.py`; el
  archivo esperado es
  `video/graficos/esc05/esc05_heatmap_vaep_messi_cr_dybala.png`.

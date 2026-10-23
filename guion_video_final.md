# Guión — Video final de mentoría
**"Contar el partido sin verlo"**

## Concepto narrativo

Hilo conductor: al principio planteamos una pregunta incómoda —*¿se puede entender un partido de fútbol sin verlo?*— y la respondemos recorriendo las tres etapas. Recurso clave: **una jugada recurrente** (un gol que elegís en video) que aparece tres veces en el video y cada vez la miramos con otra lente: primero con xG, después con SPADL y features, finalmente con VAEP. El espectador ve cómo la misma jugada se va "iluminando" con datos.

Duración objetivo: **~13 minutos**.
Tono: documental deportivo, ritmo ágil, música con tensión creciente.
Voz en off: una sola voz (o dos alternando: una más analítica, una más narrativa).

---

## Mapa de tiempos

| # | Escena | Duración | Acumulado |
|---|---|---|---|
| 0 | Cold open / gancho | 0:50 | 0:50 |
| 1 | Intro mentoría + equipo + objetivo | 1:10 | 2:00 |
| 2 | El dataset: Wyscout | 1:30 | 3:30 |
| 3 | TP1 — Mirar el juego | 3:00 | 6:30 |
| 4 | TP2 — Limpiar, entender, estandarizar | 2:30 | 9:00 |
| 5 | TP3 — Valorar y agrupar | 3:00 | 12:00 |
| 6 | Cierre: la jugada, contada | 1:00 | 13:00 |

---

## ESCENA 0 — Cold open (0:00 – 0:50)

**VISUAL**
Montaje rápido de goles reales (b-roll con derechos libres o clips propios): disparos, atajadas, festejos. Cada 2–3 segundos un corte. Sobre las imágenes, un contador animado de eventos sube hasta **3.251.294**. La música sube y de golpe se corta a negro.

**VOZ EN OFF**
> "Cada temporada, un solo partido de fútbol genera miles de acciones. Pases, quites, remates, duelos. La mayoría pasan desapercibidos. Y sin embargo, cada una deja un rastro. Una posición. Un tiempo. Un resultado."

**EN PANTALLA** (texto que aparece tipo máquina de escribir)
> 3.251.294 eventos · 1.941 partidos · 4.299 jugadores

**GOLPE:** pantalla en negro, una sola frase.

**VOZ EN OFF**
> "¿Y si pudiéramos contar la historia de un partido… sin verlo?"

**AUDIO:** música que corta en seco (silencio de 1 s) en la frase final.

---

## ESCENA 1 — Intro: quiénes somos y qué buscamos (0:50 – 2:00)

**VISUAL**
Placa de presentación con el logo de DiploDatos 2026 · FaMAF · UNC. Nombres y foto/avatar de cada integrante (aparecen uno por uno con un corte al ritmo de la música). Fondo sutil: un campo de fútbol dibujado con puntos y flechas que se van trazando.

**VOZ EN OFF**
> "Somos [Integrante 1], [Integrante 2] y [Integrante 3]. Como parte de la mentoría *Ciencia de Datos Aplicada al Fútbol*, de la Diplomatura en Ciencia de Datos de FaMAF, nos propusimos aplicar aprendizaje automático al fútbol profesional, con datos reales de una temporada completa."

> "Nuestro objetivo fue recorrer el flujo completo de data science: desde la limpieza de datos crudos hasta modelos capaces de valorar cada acción de un partido y encontrar jugadores parecidos entre sí."

**EN PANTALLA**
> Objetivo: transformar eventos crudos → métricas accionables.
> Frameworks de referencia: **VAEP** · **xT** · **SPADL**

**NOTA DE PRODUCCIÓN:** acá entra el primer momento "videíto de fútbol": 4–5 s de un clip genérico de fútbol mientras habla la voz en off de la introducción, para no arrancar con puro texto.

---

## ESCENA 2 — El dataset: Wyscout (2:00 – 3:30)

**VISUAL**
Animación de archivos JSON abriéndose y transformándose en tablas (JSON → Parquet). Un mapa de Europa con las ligas encendidas.

**VOZ EN OFF**
> "Los datos provienen de Wyscout, uno de los principales proveedores de datos deportivos del mundo, publicados con licencia abierta. Son eventos de la temporada 2017/18: cada pase, cada remate, cada duelo, con coordenadas de inicio y fin."

**EN PANTALLA** (datos del proyecto, aparecen sincronizados)
> Premier League · La Liga · Serie A · Bundesliga · Ligue 1 · Euro 2016 · Mundial 2018
> 142 equipos · 1.941 partidos · 4.299 jugadores únicos
> Coordenadas en sistema 0–100

**VOZ EN OFF**
> "Para trabajar, convertimos los JSON originales a Parquet: en nuestros notebooks pasamos de 1.9 millones de eventos cargando hasta 10 veces más rápido y consumiendo la mitad de memoria. Nuestro foco principal fueron **España, Inglaterra e Italia**: casi 500.000 eventos por liga."

**VISUAL:** gráfico animado de barras por liga (Italy 496k, England 483k, Spain 474k).

**NOTA DE PRODUCCIÓN:** si querés el dato "3.251.294" del cold open, aclarar en off que ese es el total del dataset completo y que se trabajó con el subconjunto de tres ligas.

---

## ESCENA 3 — TP1: Mirar el juego (3:30 – 6:30)

### 3a. xG — la primera pregunta (3:30 – 4:20)

**VISUAL**
Un tiro se congela en pantalla y desde el punto de disparo se traza un cono hacia el arco. Aparece un número: la probabilidad de gol. Repetir con 3 tiros de zonas distintas.

**VOZ EN OFF**
> "Empezamos por la pregunta más básica: ¿qué tan probable era que ese remate terminara en gol? Implementamos un modelo de **Expected Goals** con regresión logística, entrenado sobre más de 8.000 tiros de La Liga."

**EN PANTALLA**
> Modelo xG: AUC 0.78 ± 0.01
> xG total de la liga: **911,4** · Goles reales: **912**

**VOZ EN OFF**
> "El resultado es llamativo: el modelo estimó 911 goles esperados donde hubo 912 reales. Casi perfecto. Eso nos dio confianza en la métrica."

### 3b. Shot maps (4:20 – 4:50)

**VISUAL**
Shot map animado de La Liga: cada tiro aparece como un punto, los goles en otro color. Luego, transición a comparación lado a lado **Barcelona vs Real Madrid**.

**VOZ EN OFF**
> "Con esos datos construimos shot maps. La comparación es elocuente: el Real Madrid tiró más —631 remates contra 502— pero el Barcelona convirtió el 17,3% contra el 12,8%. Más tiros no siempre es mejor."

### 3c. Heat maps y pressing (4:50 – 5:25)

**VISUAL**
Heat maps de densidad de acciones superpuestos. Después, mapa de recuperaciones: Barcelona y Eibar iluminados en campo rival.

**VOZ EN OFF**
> "Los mapas de calor muestran dónde vive el juego. Y una pregunta nos llevó a medir el pressing: ¿presionar alto va con estar arriba en la tabla? La respuesta nos sorprendió: Barcelona recuperó el 56% de las pelotas en campo rival… y Eibar, que terminó a mitad de tabla, el 56,2%. **Presionar alto es un estilo, no un nivel.**"

### 3d. Redes de pases y radares (5:25 – 6:10)

**VISUAL**
Red de pases animada: nodos que son jugadores, aristas que se engrosan según los pases. Destacar el par Trigueros–Rodri.

**VOZ EN OFF**
> "Las redes de pases dibujan el sistema de un equipo. La conexión más usada de toda la temporada fue Trigueros–Rodri, del Villarreal: 620 pases entre ambos. Y con radares por percentil comparamos jugadores por posición: Isco apareció como un mediocampista por encima del percentil 90 en las cuatro variables que medimos."

**NOTA DE PRODUCCIÓN:** esta escena es la ideal para un **split de video + gráfico**: en un lado el clip real de una posesión del Villarreal, en el otro el nodo encendido en la red.

---

## ESCENA 4 — TP2: Limpiar, entender, estandarizar (6:30 – 9:00)

### 4a. La jugada, ahora en SPADL (6:30 – 7:15)

**VISUAL:** retoma **la jugada recurrente** del video. Sobre el clip congelado, se superponen las etiquetas del formato SPADL: tipo de acción, parte del cuerpo, resultado, coordenada.

**VOZ EN OFF**
> "Volvemos a nuestra jugada, pero ahora con otra mirada. ¿Cómo hacemos comparable una acción de Messi con una de un defensor de la Serie A? Con un lenguaje común: **SPADL**. Un formato estándar que describe cada acción como un vector."

**EN PANTALLA**
> game_id · period_id · time_seconds · team_id · player_id · start_x/y · end_x/y · tipo · parte del cuerpo · resultado

**VOZ EN OFF**
> "Convertimos 1.9 millones de eventos a 1.454.478 acciones SPADL estandarizadas."

### 4b. Curación: lo que encontramos (7:15 – 8:00)

**VISUAL:** dashboard de validación en pantalla (del `validation_report.md`), resaltando 38/39 checks aprobados.

**VOZ EN OFF**
> "Antes de modelar, auditamos todo. ¿Valores faltantes? Ninguno. ¿Coordenadas fuera de rango? Un solo evento en un millón novecientos mil, que eliminamos. ¿Duplicados? Ochenta y seis, depurados. El dataset final pasó 38 de 39 controles."

> "Y aprendimos algo que suele pasarse por alto: los eventos en los bordes del campo no son errores de carga — son saques de banda, córners y tiros libres. Conservarlos fue una decisión, no un descuido."

### 4c. El hallazgo: la zona y la construcción (8:00 – 9:00)

**VISUAL:** gráfico animado del área dividida en zonas, con la tasa de conversión encendida por zona: Centro_Area **18,4%**, bandas **~6%**, fuera del área **~2–4%**.

**VOZ EN OFF**
> "Con las acciones ya limpias, construimos features propias. La primera: la zona del remate. El gradiente es limpísimo: desde el centro del área se convierte al 18,4%. Desde las bandas del área, al 6%. Tres veces menos."

**VISUAL:** gráfico de barras: tiros sin construcción previa **12%** de conversión; con 6 o más pases, **8,1%**.

**VOZ EN OFF**
> "La segunda nos dejó pensando: medimos el largo de la construcción previa a cada tiro. Y encontramos que **los tiros sin construcción previa convierten más** —12%— que los de posesión larga —8%—. Contraintuitivo, pero consistente: muchas veces el gol llega tras una recuperación o un rebote, no después de veinte pases."

> "Y cerramos con una advertencia metodológica: los datos están sesgados por posición. Un delantero registra un 35% menos de acciones que un mediocampista. Si uno mira números crudos, mide dónde juega el jugador, no lo bueno que es. Por eso normalizamos por 90 minutos y por percentil dentro de cada posición: así Messi aparece en el percentil 98,6 de remates… comparado solo contra delanteros."

**NOTA DE PRODUCCIÓN:** este es el mejor punto para insertar un clip real de un **gol de contraataque** y explicar en off por qué convierte más que una jugada elaborada.

---

## ESCENA 5 — TP3: Valorar y agrupar (9:00 – 11:40)

### 5a. xT y VAEP (9:00 – 10:20)

**VISUAL:** el campo se divide en una grilla animada 16×12; cada celda se colorea según "amenaza". La animación corre ~10 iteraciones hasta estabilizarse. Luego, aparecen dos probabilidades en pantalla.

**VOZ EN OFF**
> "Acá llegamos al corazón del proyecto. Primero, **Expected Threat**: el campo se divide en zonas y a cada una se le asigna un valor de peligro, que se propaga iterativamente. Un pase desde tu área al medio campo ya aumenta la amenaza."

**EN PANTALLA**
> xT: grilla 16×12 · converge en ~10 iteraciones

> "Después, **VAEP**: en lugar de valuar solo el movimiento del balón, entrenamos dos modelos de machine learning que estiman, para cada acción, cuánto sube la probabilidad de que nuestro equipo convierta… y cuánto sube la de que el rival convierta."

**EN PANTALLA**
> VAEP = ΔP(anotar) − ΔP(conceder)
> XGBoost: P(score) AUC 0.774 | P(concede) AUC 0.743

**VOZ EN OFF**
> "VAEP tiene una ventaja sobre xT: premia también el trabajo defensivo. Lo comprobamos: la correlación entre ambas métricas es moderada, 0,41. Cuando divergen, están mostrando facetas distintas del mismo jugador."

**VISUAL:** ranking animado. Messi arriba, luego Salah, Cristiano, Coutinho.

**VOZ EN OFF**
> "El ranking de la temporada: Messi primero, con 0,97 de VAEP por partido. Detrás, Salah, Cristiano Ronaldo, Coutinho. Un detalle: Messi genera peligro de mil maneras —pases, regates, remates—; Cristiano, casi exclusivamente rematando. Los datos distinguen estilos que a simple vista se confunden."

**VISUAL:** mapas de calor de VAEP de **L. Messi** y **Cristiano Ronaldo**, lado a lado. Las celdas se van iluminando progresivamente siguiendo la escala del heat map (de frío a caliente), como si el mapa se "encendiera"; al final quedan los dos mapas completos.

**VOZ EN OFF**
> "Antes de seguir, un control: probamos XGBoost y LightGBM y el ranking salió casi idéntico —correlación 0,985—. La elección del algoritmo no cambiaba la historia; lo que la cambia es *dónde* genera peligro cada jugador."

> "Messi enciende el borde del área y la zona derecha, con diagonales hacia adentro. Cristiano enciende casi solo el área, del centro a la derecha. La misma métrica, dos mapas de calor distintos: dos formas de entender el ataque."

**EN PANTALLA**
> VAEP por zona · Messi 0,97 vs Cristiano 0,58 VAEP/partido
> Acciones top (p95+): 138 vs 60

### 5b. Clustering y scouting (10:20 – 11:45)

**VISUAL:** cuatro fichas aparecen una por una, cada una con su color, cantidad de jugadores, posiciones dominantes y jugadores de ejemplo; luego colapsan en la nube de puntos UMAP: 1.201 jugadores agrupados en 4 colores.

**VOZ EN OFF**
> "Y nos preguntamos: ¿hay arquetipos de jugador? Usando clustering, **K-Means** eligió cuatro perfiles óptimos sobre 1.201 jugadores. K-Means no los nombra: los leímos nosotros mirando cómo se compone cada grupo."

> "Cluster 0 —322 jugadores—: los finalizadores. 219 delanteros, pocas acciones en toda la temporada (unas 600) y xT bajo; viven del remate. Agüero, Kane, Icardi, Aubameyang."

> "Cluster 1 —629, el más grande—: defensores y volantes de contención. 392 defensores y 229 mediocampistas, mucho pase y el único grupo con VAEP defensivo positivo. Marcelo y Koulibaly son su cara más valiosa."

> "Cluster 2 —80—: los arqueros. 79 de los 80. Su xT alto es un artefacto: el modelo premia el pase corto desde el área."

> "Cluster 3 —170—: los creadores. Mediocampistas y delanteros de élite, los que más acciones acumulan y el mayor VAEP medio, 0,215. Messi, Salah, Cristiano, Coutinho, Dybala."

**EN PANTALLA** (fichas)
> **0 · Finalizadores** (n=322) · 219 FW · VAEP 0,11
> **1 · Defensores/volantes** (n=629) · 392 DF · VAEP 0,15
> **2 · Arqueros** (n=80) · 79 GK · xT inflado
> **3 · Creadores** (n=170) · 118 MD · VAEP 0,22

**NOTA DE PRODUCCIÓN:** las cifras salen de cruzar `rankings_jugadores_PL_2017.csv` (columna `cluster`) con las posiciones de `players.json`. Los nombres de los arquetipos ("Finalizadores", etc.) son una lectura descriptiva nuestra, no salen de K-Means. Verificar los n exactos al momento de graficar; los valores de VAEP son medianas.

**VOZ EN OFF**
> "Y lo más interesante: al compararlos entre ligas, los mismos cuatro arquetipos aparecen casi idénticos en España, Italia e Inglaterra."

**EN PANTALLA**
> Proporciones por liga casi iguales — el arquetipo no depende de la liga

**VOZ EN OFF**
> "Los perfiles de juego son universales. Lo que no encaja en el molde son los individuos: Messi, Icardi, Kane. La diferencia relevante está en el jugador, no en la liga."

**VISUAL:** sistema de scouting en pantalla: buscamos reemplazante de Iniesta. Aparecen los 5 más similares.

**VOZ EN OFF**
> "Con eso construimos un sistema de scouting. Le pedimos un reemplazante funcional para Iniesta, que se iba del Barcelona. El más parecido por estilo fue Kovačić, pero rendía la mitad. El sistema encontró a Modrić y a Allan como alternativas: jugadores de perfil similar que, además, sumaban más valor. Eso es scouting basado en evidencia."

### 5c. SHAP: por qué el modelo decide (11:45 – 12:00)

**VISUAL:** gráfico SHAP animado, resaltando la variable que baja la probabilidad.

**VOZ EN OFF**
> "Y abrimos la caja negra con **SHAP**: si el tiro viene precedido de una acción fallida, el modelo baja la probabilidad de gol. Tiene lógica futbolera. El modelo, en el fondo, entendió el juego."

---

## ESCENA 6 — Cierre: la jugada, contada (12:00 – 13:00)

**VISUAL:** por última vez, **la jugada recurrente** en video, completa y sin pausas. La música baja. Aparecen, uno por uno, los datos que la describen: xG, zona, valor VAEP, probabilidad de gol.

**VOZ EN OFF**
> "Al principio nos preguntamos si se podía contar un partido sin verlo. Mirá esta jugada. Sabemos desde qué zona salió. Sabemos cuánto aumentó la probabilidad de gol. Sabemos qué jugador la generó. Sabemos si podría haberla hecho mejor otro. Y todo eso, sin mirar el video."

> "No reemplazamos el ojo del analista. Le damos una capa más: la evidencia de **3 millones de acciones** que cuentan lo que el ojo no siempre ve."

**VISUAL:** placa final con logo DiploDatos, mentoría, integrantes, repositorio y agradecimientos.

**VOZ EN OFF**
> "Esto fue nuestro recorrido: explorar, limpiar, modelar y, sobre todo, transformar datos en decisiones. Gracias."

**EN PANTALLA**
> github.com/guillealonso/futbol-ciencia-datos-2026
> DiploDatos 2026 · FaMAF · UNC

**AUDIO:** la música cierra en un acorde y baja a silencio.

---

## Checklist de assets a producir

| Asset | Escena | Cómo obtenerlo |
|---|---|---|
| 10–15 clips de fútbol (b-roll) | 0, 1, 4, 6 | Banco de video libre o clips propios |
| Contador animado 3.251.294 | 0 | Animación en After Effects / CapCut / plantilla |
| Geometría de tiro + cono xG | 3a | Rehacer desde el notebook P1 (mplsoccer) exportado a PNG |
| Shot map Barcelona vs Real Madrid | 3b | Ya existe en P1 |
| Heat map de recoveries | 3c | Ya existe en P1 |
| Red de pases animada | 3d | Exportar el gráfico de P1 y animar aparición de aristas |
| Etiquetas SPADL sobre la jugada | 4a | Overlay en editor sobre el clip congelado |
| Grilla xT iterando 10 veces | 5a | Exportar tsx de la grilla desde P3 |
| Ranking animado VAEP | 5a | Gráfico de barras animado (bar chart race) |
| Heat maps VAEP Messi vs Cristiano | 5a | Exportar de P3 e iluminar celdas por escala (animación) |
| Fichas de los 4 clusters | 5b | Diseño propio con n, posiciones y ejemplos (datos abajo) |
| Nube UMAP | 5b | Ya existe en P3 |
| Panel de scouting de Iniesta | 5b | Ya existe en P3 |
| Placa final + QR al repo | 6 | Diseño simple |

---

## Notas de dirección

- **Ritmo:** las escenas 3 y 5 son las más densas. No acumular más de dos gráficos por minuto de voz en off.
- **Regla del dato loco:** un solo número impactante por escena (912 vs 911,4 · 18,4% · 56,2% · 0,985 · 4 arquetipos). El resto queda como texto en pantalla.
- **Truco de continuidad:** la jugada recurrente debe ser *el mismo clip exacto* las tres veces, con distinto overlay. Ver sección **"El truco de continuidad"** más abajo.
- **Si necesitás bajar a ~7 minutos:** recortá 3b (shot maps), 4b (curación detallada) y 5c (SHAP), y fusioná 5a y 5b.

---

## El truco de continuidad — la jugada que se repite

### Por qué funciona

El video no se divide en tres bloques independientes (TP1, TP2, TP3), sino que **vuelve tres veces al mismo lugar**. Eso genera dos efectos:

1. **El espectador aprende acumulativamente.** La primera vez ve un gol. La segunda entiende que ese gol tiene una estructura de datos. La tercera entiende cuánto valió y por qué. Es el efecto "estribillo": cada repetición agrega una capa sin perder el ancla.
2. **Sensación de descubrimiento, no de clase.** No decimos "ahora vamos a explicar VAEP". Decimos "volvamos a esta jugada", y el espectador siente que algo nuevo se revela sobre algo que ya conocía.

La regla de oro: **mismo clip, misma angulación, mismo encuadre. Solo cambia la capa de datos y la voz.**

### Cómo elegir la jugada

Criterios, en orden de importancia:

- **Es un gol o una ocasión clarísima** (necesitás que el espectador entienda de un vistazo que "eso valía").
- **Tiene, al menos, dos o tres acciones encadenadas** (pase → conducción → remate, o recuperación → pase filtrado → definición). Una jugada de una sola acción no permite mostrar la evolución de la amenaza.
- **Preferentemente de un jugador que aparece en los rankings del TP3** (Messi, Salah, Cristiano, De Bruyne, Coutinho). Así el cierre reutiliza su VAEP real y no inventa.
- **Con buena calidad de imagen y sin logos de transmisión que estorben.**
- **Que el remate final caiga en una zona identificable** (idealmente *Centro_Area*, la de mayor conversión: 18,4%).

Sugerencia práctica: buscá en el dataset `rankings_jugadores_PL_2017.csv` o en el parquet las acciones de mayor `vaep_value` de la temporada, y elegí el clip de video de una de ellas. Así la jugada que el espectador ve es literalmente una de las más valiosas que encontró el modelo.

### Cómo preparar el clip

- Recortá **6–8 segundos** desde el inicio de la posesión relevante.
- Armá **dos versiones**:
  - **Versión A (completa):** corre normal, con sonido ambiente del partido. Es la que se usa en las escenas 4a y 6.
  - **Versión B (congelada):** la misma, pero con **freeze-frame** en el instante previo al remate o en la definición. Es la que se usa para superponer overlays en la escena 4a.
- Anotá las coordenadas reales de la jugada (start_x/start_y, end_x/end_y) y el `player_id`. Los vas a necesitar para cuadrar el overlay con la geometría de la cancha.
- Si el video está en pantalla fija, dibujá la cancha encima respetando la orientación (Wyscout normaliza a un solo sentido: el equipo que ataca va siempre de izquierda a derecha). Esto es clave para que el gráfico y el video hablen el mismo idioma.

### Las tres apariciones

| | Escena | Duración | Imagen | Overlay | Frase ancla en off |
|---|---|---|---|---|---|
| **1ª** | 4a — SPADL | 6–8 s | Clip completo, luego freeze en el contacto | Cajas etiquetando cada acción: tipo, parte del cuerpo, resultado, coordenada | "…volvemos a nuestra jugada" |
| **2ª** | 4c — Features | 8–10 s | Solo el tramo final, más lento | Zona del remate iluminada + número de conversión (ej. 18,4%) y `build_up_length` | "…esta jugada tiene una zona y una construcción" |
| **3ª** | 5a — VAEP | 6–8 s | Clip completo pero pausado en cámara lenta | Flechas de valor acumulándose; el `vaep_value` del remate encendido al final | "…y ahora sabemos cuánto valió cada toque" |
| **Cierre** | 6 — Cierre | 8–10 s | Clip completo, velocidad normal, sin cortes | Datos apareciendo uno por uno sobre la imagen | "Mirá esta jugada": xG · zona · VAEP · probabilidad |

**Total de pantalla para la jugada: ~40 s repartidos en todo el video.** Es poco, pero es lo que sostiene el hilo.

### Cómo evitar que canse

- **Cambiá la duración y el ritmo de cada aparición:** la primera es rápida, la tercera en cámara lenta, la del cierre en velocidad real. Nunca dos veces igual.
- **Cambiá qué se resalta:** 1ª aparición → todas las acciones por igual; 2ª → solo la zona; 3ª → solo el toque decisivo. El ojo enfoca distinto aunque el clip sea el mismo.
- **No repitas la misma frase.** El ancla verbal cambia: "volvemos a esta jugada" → "esta misma jugada" → "ahora ya sabemos" → "mirá esta jugada".
- **Nunca la muestres dos veces seguidas.** Siempre hay al menos una escena de por medio.

### Ejemplo trabajado (a completar con tu clip)

Supongamos que la jugada elegida es un gol de Messi (perfil zurdo que arranca desde la derecha, el patrón que apareció en los mapas de calor del TP3).

| Aparición | Lo que ve el espectador |
|---|---|
| 1ª (SPADL) | El clip corre; se congela en el pase previo. Etiquetas: `pass` · pie izquierdo · success · (52, 18) → (78, 30) y luego `shot` · Centro_Area |
| 2ª (Features) | Solo el remate. Se ilumina la franja central del área con **18,4%** y aparece "`build_up_length` = 2": dos pases antes del gol |
| 3ª (VAEP) | Cámara lenta. Cada toque suma: el pase aporta un delta pequeño, el remate aporta el salto grande. El `vaep_value` del disparo se enciende |
| Cierre | El gol completo, limpio, con los cuatro datos apareciendo en secuencia: xG 0,xx · Centro_Area · VAEP +0,xx · jugador: L. Messi (0,97 VAEP/90) |

El remate final ya lo tenés caracterizado por los datos del proyecto. Cerrás así el círculo: el espectador reconoce la jugada que vio al principio, pero ahora sabe leerla.

### Detalles técnicos de montaje

- **Encuadre idéntico:** no cambies el recorte entre apariciones. Si zooméas, que sea el mismo zoom la segunda y tercera vez.
- **Marca de agua de posición:** si querés, un pequeño punto que indique el balón, siempre en el mismo estilo.
- **Sincronía con la cancha:** superponé la cancha de `mplsoccer` translúcida sobre el video para que la coordenada caiga exactamente donde está el balón. Ese "match" entre video y gráfico es lo que da el golpe de efecto.
- **Sonido:** en la primera y última aparición, dejá el sonido ambiente del partido (gol, hinchada). Las apariciones intermedias van con música. El contraste refuerza "esto es el mismo momento, lo miramos distinto".
- **Si la jugada no es de Messi:** elegí cualquier goleador del top VAEP. El guión funciona igual; solo cambiá el nombre y las cifras del recuadro de cierre.

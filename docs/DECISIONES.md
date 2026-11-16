# Registro de decisiones

**Regla:** toda decisión que afecte a más de una persona se anota aquí. Si no está aquí, no existe.

| Fecha | Decisión | Dueño | Alternativas consideradas | Razón |
|---|---|---|---|---|
| 2026-11-14 | Público objetivo: 8–12 años | CD | 6–8, 12–15, público general | Es la edad con más curiosidad y capacidad de lectura autónoma |
| 2026-11-14 | Stack: Streamlit | BE | Flask, HTML/CSS/JS, Java | Prioridad: terminar y desplegar rápido con lo que ya saben |
| 2026-11-14 | 10 piezas en el MVP | CD | 6, 14, 20 | Permite profundidad narrativa sin sacrificar cobertura |
| 2026-11-14 | Tres zonas: Luna, Marte, espacio profundo | CD | Solo Luna, solo Marte | Cubre el brief completo y da un recorrido narrativo |
| 2026-11-14 | Datos estáticos + live con respaldo | BE | Solo estático, solo live | El live es el gancho; el estático garantiza la demo |
| 2026-11-14 | Taxonomía de 5 estados | CD | 3 estados, 8 estados | Simple para niños, suficiente para contar historias |
| 2026-11-14 | Un dueño por archivo | Todos | Todos editan todo | Evita conflictos de merge |
| 2026-11-14 | BE es merge captain | Todos | Rotativo | Una sola persona controla la integración |
| 2026-11-14 | Code freeze en T+38 | Todos | T+42 | Deja 6 horas para ensayo y entrega |
| 2026-11-14 | Cierre del pitch: hito de un día luz de Voyager 1 | CD | Cierre genérico | Es un evento real y cercano (18 nov 2026) |
| 2026-11-14 | Investigación llena `contenido/fichas.csv` y backend genera `data/artifacts.json` | BE + CD | Investigación escribe el JSON a mano | Evita errores de sintaxis en un equipo sin experiencia técnica |
| 2026-11-14 | Una guía única en Word (`docs/Guia_Equipo.docx`) como documento de trabajo diario | Todos | Los ocho documentos de `docs/` por separado | El equipo se perdía entre documentos; la guía tiene un paso a paso por rol |
| 2026-11-14 | Paleta oficial de NASA Space Apps en tema oscuro: Deep Blue `#07173F` de fondo, Electric `#0042A6` y Neon Blue `#0960E1` en bloques, Neon Yellow `#EAFE07` solo como acento | FE | Paleta clara actual; azules inventados | Es la identidad documentada en la Brand Guide (jun 2026) y el amarillo como acento respeta la regla 60-30-10 |
| 2026-11-14 | Tipografía Exo 2 (títulos) + Overpass (texto), empaquetadas en `static/fonts/` | FE | Fira Sans oficial; Orbitron; Alvaro Wide | Exo 2 da el aire espacial que pidió el equipo, Overpass mantiene legibilidad y las dos son OFL; «Alvaro Wide» no existe y «Alvaro» es solo uso personal |
| 2026-11-14 | Las fuentes se sirven desde `static/` con `server.enableStaticServing`, no desde un CDN | FE + BE | Google Fonts por URL | Streamlit solo publica `./static`; sin red la app debe verse igual |
| 2026-11-14 | Encabezado «Menú» y encabezados temáticos por sección con CSS propio | FE | Fotos de fondo por sección | La guía de marca pide no poner texto encima de fotografías; el patrón de estrellas es CSS y pesa 0 KB |
| 2026-11-14 | Sin 3D real (WebGL/Three.js) por ahora | FE | Three.js o componente propio | Pesaría más de 600 KB, rompe «sin librerías nuevas» y castiga el celular; se prefieren esferas y fondos con CSS |
| 2026-11-15 | Los títulos pasan de Exo 2 a **Orbitron** (OFL, subset latin, 11.8 KB); Overpass se mantiene para el texto | FE | Exo 2; Michroma; Audiowide | Orbitron tiene formas geométricas de instrumento espacial y conserva la legibilidad en tamaños pequeños; se empaqueta local igual que Overpass |
| 2026-11-15 | Encabezados de Luna, Marte, espacio profundo y En vivo usan fotos reales de NSSDCA con una capa de degradado para el contraste | FE | Gradientes CSS; fotos de JPL; imágenes generadas | El usuario pidió imágenes realistas del archivo NSSDCA; la capa oscura mantiene el texto en AA y el crédito va visible bajo la descripción |
| 2026-11-15 | El menú lateral sube a 1.5 rem el rótulo «MENÚ» y a 1.08 rem los enlaces | FE | Menú actual de 0.8 rem | El menú se leía muy pequeño en el celular y en el proyector del pitch |
| 2026-11-15 | `client.toolbarMode = "minimal"`: la app no ofrece fondo claro/oscuro | FE + BE | Ocultar el menú solo con CSS | La identidad es oscura por diseño; `minimal` quita el menú de desarrollador y el selector de tema sin romper el botón de la barra lateral |
| 2026-11-15 | `.block-container` reserva 4.75 rem arriba (60 px del header + 1 rem) en escritorio y celular | FE | Bajar el `z-index` del header; ocultar el header | El header de Streamlit es absoluto y tapaba el borde superior del hero y la etiqueta de estado de la ficha |
| 2026-11-15 | El encabezado de inicio usa la ilustración de Marte, la Luna y la Tierra que aportó el equipo (`inicio_tres_mundos.jpg`), con el mismo recorte 1200 × 675 y el mismo degradado que los demás héroes | FE | Patrón de estrellas CSS; foto del NSSDCA | El usuario pidió cambiar la portada por esa imagen; los tres mundos resumen el recorrido de la app y el degradado mantiene el texto en AA |
| 2026-11-15 | El enlace junto a cada título copia la dirección completa y no navega: el clic se intercepta con JavaScript propio y muestra un aviso «Enlace copiado» | FE | Dejar el ancla nativa de Streamlit; ocultar el símbolo | Streamlit 1.67 solo enlaza al hash y provoca un salto; el equipo necesita compartir la sección sin perder la posición. Sin librerías ni red |
| 2026-11-15 | Los botones de regreso usan iconos Material locales: `arrow_back` para «Volver a…» y `keyboard_double_arrow_left` para «Volver al inicio» | FE | Emojis 🏠 y de zona; flechas tipográficas | Los emojis cambian de forma según el sistema; los iconos vienen empaquetados con Streamlit y se leen igual en todos los equipos |
| 2026-11-15 | El encabezado del Quiz usa `PIA01341 · Solar System Montage Updated` (NASA/JPL) | FE | Montajes del NSSDCA; gradiente CSS actual | El NSSDCA solo tiene mosaicos técnicos del Voyager con etiquetas impresas, y las reglas prohíben texto incrustado; PIA01341 viene de la misma fuente que los globos del selector, no lleva rótulos y deja los gigantes a la derecha, donde el degradado aclara |
| 2026-11-15 | La Tierra del selector solar se dibuja con degradados CSS (océano, continentes, casquete, terminador y anillo de atmósfera) y sin rótulo; el Sol pierde el texto y gana halo | FE | Foto real recortada; seguir mostrando «Tierra» y «Sol» | A 65 px el texto era lo único que identificaba la esfera; la silueta con continentes la hace reconocible sin ocupar espacio y mantiene la escena como dibujo, sin imágenes extra |
| 2026-11-15 | El Quiz ya no lleva el destello `✦` y su tarjeta usa un padding propio | FE | Dejar el destello; quitar también la sombra del contorno | El usuario lo señaló como decorativo y sobrante; al quitarlo la tarjeta encoge y el hueco superior se cierra con un padding menor solo para `quiz_inicio`, sin tocar el bloque de las fichas |
| 2026-11-15 | El mapa de Marte pasa a disco ortográfico rojo, con el meridiano 10° E al centro y Spirit e InSight en la fila «Al otro lado de Marte» | FE | Mapa ecuatóreo en color; dos discos con una segunda vista; globo PIA00407 tal cual | El usuario pidió un diseño como el de la Luna con los colores del planeta. Los cinco sitios abarcan 209° de longitud y ningún hemisferio muestra más de tres, así que la fila inferior cuenta el resto. Se reproyecta el mapa ya validado y se toma la paleta de PIA00407 para no depender de coordenadas de cámara sin documentar |
| 2026-11-15 | Los marcadores de los mapas cambian el texto por la ilustración de cada pieza (`static/img/marcadores/{id}.png`), pintada por CSS sobre un panel translúcido; sin tocar `mapa.py` | FE | PNG dentro del botón con `st.image`; componente HTML propio; dejar el texto | `st.button` no acepta imágenes y un componente propio rompe «sin librerías nuevas»; con CSS el texto queda oculto pero accesible (tooltip de `help` y nombre accesible intactos) y los tests de Python siguen igual. Ilustraciones aportadas por el equipo, fondo plano removido y menos de 300 KB cada una |
| 2026-11-16 | La app pasa a `st.navigation` de una sola página: `app.py` es el punto de entrada, la portada vive en `pages/0_Inicio.py` y las vistas cambian sin recargar el documento | FE | Navegación multipágina clásica; router propio con componentes | La multipágina recargaba el documento en cada clic: el contenido colapsaba a 900 px, crecía en 3–4 pasos (CLS ≈ 0,60) y el scroll saltaba. `st.navigation` conserva el documento, la hoja de estilos y el estado del navegador |
| 2026-11-16 | La hoja de estilos se instala una vez en `<head>` (`#fe1-estilos`) y se restaura desde `sessionStorage`; el movimiento vive en `components/movimiento.py` y respeta `prefers-reduced-motion` | FE | Reinyectar 30 KB de CSS en cada página; animaciones repartidas por página | Reanalizar el CSS en cada rerun provocaba repintados y parpadeo; un solo módulo de movimiento evita duplicar guiones y el revelado solo oculta lo que empieza bajo la pantalla, nunca lo visible |
| 2026-11-16 | En el celular el menú se cierra solo al elegir una sección | FE | Dejar el menú abierto como hace `st.navigation`; ocultar el menú con CSS | El overlay tapaba el contenido elegido y obligaba a un toque extra; el guion detecta el ancho y pulsa el botón de colapsar después de navegar |
| 2026-11-16 | Las animaciones se pueden encender en una pestaña con `?movimiento=completo` (y apagar con `?movimiento=normal`); la elección se guarda en `sessionStorage` | FE | Ignorar siempre `prefers-reduced-motion`; cambiar la configuración de animaciones de Windows | Windows puede tener las animaciones apagadas (`MinAnimate = 0`), lo que en Brave equivale a `prefers-reduced-motion: reduce` y apaga el movimiento por accesibilidad. El modo demo es opt-in, dura solo esa pestaña y permite enseñar la interfaz sin alterar el sistema de nadie |
| 2026-11-16 | La hoja de estilos no puede contener el carácter `<` | FE | Comentarios con etiquetas HTML dentro del CSS | El CSS viaja dentro de un `<script>` inline y el saneador de HTML descarta el bloque entero si encuentra una etiqueta: la app se quedó sin estilos por un comentario con `<html>`. Hay una prueba que lo impide |

---

## Fase 2 — 2026-11-15

- FE: inicio usa un selector solar ilustrado con CSS local y botones Streamlit
  para Luna, Marte y espacio profundo; tamaños y distancias no están a escala.
- FE: «Ver ficha» ofrece una vista previa textual mediante `help` nativo.
  El clic conserva el recorrido existente y funciona en pantallas táctiles.
- FE: mantener mapas 2D con 10 horas restantes. El reemplazo 3D exige nuevas
  coordenadas y comunicación de selección con Python; estimación y condiciones
  en [VIABILIDAD_3D.md](VIABILIDAD_3D.md).
- FE: los globos del selector usan fotos locales de NASA (Luna Galileo, Marte
  Viking) y la nebulosa de Orión como fondo decorativo, no como ubicación real
  de las Voyager. Créditos en [static/README.md](../static/README.md).
- FE: las preguntas de cada ficha se agrupan en un bloque con borde amarillo
  neón; «Ver ficha» y las opciones del quiz cambian a ese mismo amarillo con
  texto Deep Blue al pasar el cursor o recibir foco, para mantener el contraste.
- FE: el quiz pasa a 30 preguntas sacadas de las 10 fichas y sus fuentes, con
  menú previo, una pregunta por pantalla, avance al responder, orden y opciones
  mezclados en cada partida. El récord vive en la sesión, no en un servidor.

## Cómo agregar una decisión

1. Escribe la fecha.
2. Describe la decisión en una frase.
3. Indica quién es el dueño.
4. Anota al menos una alternativa que se descartó.
5. Explica la razón en una frase.

Si la decisión cambia el contrato de datos, actualiza también [CONTRATO_DATOS.md](CONTRATO_DATOS.md).

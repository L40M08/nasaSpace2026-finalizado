# `components/` — piezas visuales reutilizables

**Dueño:** Frontend.
Aquí vive lo que se repite en varias pantallas. No hay lógica de datos.

---

## Qué va aquí

| Archivo | Qué aporta |
|---|---|
| `ui.py` | `aplicar_estilos()` instala la hoja en `<head>` y `encabezado()` |
| `movimiento.py` | Guion de entrada de página, revelado al scroll y barra de progreso |
| `tarjeta.py` | Tarjeta de una pieza con imagen, estado y botón |
| `mapa.py` | Fondo de zona y marcadores encima, en sus coordenadas |
| `zonas.py` | Página común de las tres zonas |
| `__init__.py` | Marca la carpeta como paquete de Python |

## Formato y convenciones

- **Python** (`.py`), funciones pequeñas que reciben datos y pintan.
- Una función pública por responsabilidad; nombres en español.
- Los componentes **no abren el dataset ni llaman a la API**: reciben `pieza`,
  `piezas` o `posiciones` ya cargadas. Solo pueden comprobar si existe un asset
  estático, nunca leer su contenido.
- El estilo va en `assets/styles.css`, no en líneas `style="..."` sueltas.
  La única excepción son las coordenadas de los marcadores: `mapa.py` genera
  un `<style>` mínimo con `left`/`top`, porque salen de `posiciones.json` y
  cambian con cada zona.
- Todo el movimiento vive en `movimiento.py`. Las clases que ocultan contenido
  (`fe1-revelar`) solo las pone el guion: sin JavaScript la página se ve
  completa, y con `prefers-reduced-motion` no se anima nada.
- Para demos con las animaciones de Windows apagadas existe
  `?movimiento=completo`: enciende el movimiento en esa pestaña aunque el
  sistema pida movimiento reducido; `?movimiento=normal` lo apaga.
- Usar las clases `fe1-*` que ya existen (`.fe1-hero`, `.fe1-badge`, etc.).

## Reglas

- Si un componente se usa una sola vez, se queda en su página.
- Si una página crece más de ~150 líneas, se parte en un componente.
- No agregar librerías nuevas sin avisar a backend.
- Todo texto visible se escribe para un niño de 8 a 12 años.

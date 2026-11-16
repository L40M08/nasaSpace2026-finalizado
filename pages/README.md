# `pages/` — una pantalla por archivo

**Dueño:** Frontend.
`app.py` declara cada archivo con `st.Page(...)` dentro de `st.navigation`, que
arma el menú lateral y cambia de vista sin recargar el documento.

---

## Qué va aquí

| Archivo | Pantalla |
|---|---|
| `0_Inicio.py` | Portada: métricas, selector solar y piezas destacadas |
| `1_Luna.py` | Mapa y fichas de la Luna |
| `2_Marte.py` | Mapa y fichas de Marte |
| `3_Espacio_profundo.py` | Mapa y fichas del espacio profundo |
| `4_En_vivo.py` | Panel con distancia y tiempo de luz |
| `5_Quiz.py` | Quiz de 30 preguntas |
| `6_Fuentes.py` | Fuentes de cada pieza y enlaces oficiales |
| `7_Ficha.py` | Ficha completa de la pieza elegida (oculta del menú) |

## Formato y convenciones

- **Python** (`.py`), una pantalla por archivo.
- El nombre empieza con número y guion bajo: `8_Mi_pagina.py`. Así se controla
  el orden del menú. Toda página nueva se registra en `app.py`; si no se
  registra, no existe para `st.navigation`.
- Los estilos y el movimiento los instala `app.py` una sola vez: ninguna página
  llama a `aplicar_estilos()`.
- Los datos se piden a `core` (`datos`, `vivo`, `formato`). **Nunca** se abre un
  JSON a mano ni se importa `requests`.
- La pieza elegida viaja en `st.session_state["pieza_sel"]`; para cambiar de
  pantalla se usa `st.switch_page("pages/7_Ficha.py")`.
- Para volver a la portada: `st.page_link("pages/0_Inicio.py", ...)`. Bajo
  `st.navigation`, `st.page_link("app.py")` lanza `StreamlitPageNotFoundError`.

## Reglas

- No dejar una pantalla en blanco: siempre un mensaje amable si faltan datos.
- No duplicar lógica entre páginas: si se repite, va a `components/`.
- No cambiar nombres de campos del dataset desde aquí.
- Toda página nueva se agrega a la guía Word (`scripts/generar_guia_word.py`).
- Probar en celular (ancho de 390 px) antes de abrir el PR: el menú debe cerrarse
  solo al elegir una sección.

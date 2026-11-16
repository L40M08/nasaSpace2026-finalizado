"""Página de inicio de «¿Dónde está ahora?».

Dueño: Frontend.
Aquí no hay lógica de datos: se usa `core.datos` y se pinta.

`app.py` es el punto de entrada y dibuja el menú; esta página solo pinta el
contenido de la portada.
"""

from __future__ import annotations

import streamlit as st

from components.sistema_solar import sistema_solar
from components.tarjeta import tarjeta
from components.ui import encabezado
from core import datos

st.set_page_config(
    page_title="¿Dónde está ahora?",
    page_icon="🚀",
    layout="wide",
)

encabezado(
    "¿Dónde está ahora?",
    "Un viaje por las máquinas que la NASA dejó en la Luna, en Marte y en el "
    "espacio profundo. Todavía están ahí. Algunas siguen hablando.",
    variante="inicio",
    grande=True,
)

piezas = datos.cargar_piezas()

if not piezas:
    st.warning(
        "Todavía no hay datos cargados. Backend debe generar `data/artifacts.json` "
        "con `python scripts/fichas_a_json.py`."
    )
    st.stop()

zonas = datos.contar_por_zona(piezas)
columnas = st.columns(4)
columnas[0].metric("Piezas en total", len(piezas))
columnas[1].metric("En la Luna", zonas["luna"])
columnas[2].metric("En Marte", zonas["marte"])
columnas[3].metric("En el espacio profundo", zonas["espacio_profundo"])

sistema_solar()

st.subheader("Algunas de las piezas")

destacadas = [pieza for pieza in piezas if pieza.get("estado") == "activo"][:3]
if not destacadas:
    destacadas = piezas[:3]

for pieza in destacadas:
    tarjeta(pieza)

st.divider()
st.caption(
    "Proyecto del NASA Space Apps Challenge 2026. Datos de NASA, NSSDCA y JPL. "
    "No está afiliado a NASA."
)

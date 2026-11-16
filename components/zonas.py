"""Página común de las tres zonas.

Dueño: Frontend.

Las páginas `1_Luna.py`, `2_Marte.py` y `3_Espacio_profundo.py` solo llaman a
`pagina_zona()` para no repetir el mismo código tres veces.
"""

from __future__ import annotations

import streamlit as st

from components.mapa import mapa_zona
from components.tarjeta import tarjeta
from components.ui import encabezado
from core import datos

SIN_PIEZAS = (
    "Todavía no hay piezas en esta zona. Investigación debe llenarlas en "
    "`contenido/fichas.csv` y backend debe ejecutar `python scripts/fichas_a_json.py`."
)


def pagina_zona(zona: str, titulo: str, descripcion: str, icono: str) -> None:
    st.set_page_config(
        page_title=f"{titulo} — ¿Dónde está ahora?",
        page_icon=icono,
        layout="wide",
    )
    encabezado(titulo, descripcion, variante=zona.replace("_", "-"))

    piezas = datos.por_zona(datos.cargar_piezas(), zona)

    if not piezas:
        st.info(SIN_PIEZAS)
        st.page_link("pages/0_Inicio.py", label="Volver al inicio", icon=":material/keyboard_double_arrow_left:")
        return

    mapa_zona(zona, piezas, datos.cargar_posiciones())

    st.subheader("Las fichas de esta zona")
    for pieza in piezas:
        tarjeta(pieza)

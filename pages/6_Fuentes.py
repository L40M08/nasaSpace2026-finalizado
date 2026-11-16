"""Página de fuentes. Dueño: Frontend.

Muestra de dónde salió cada dato. Es la página que revisa el jurado cuando
pregunta «¿y eso de dónde lo sacaron?».
"""

from __future__ import annotations

import streamlit as st

from components.ui import encabezado
from core import datos

ENLACES_OFICIALES = [
    ("Reto de NASA Space Apps 2026", "https://www.spaceappschallenge.org/2026/challenges/nasas-discarded-equipment-storytelling/"),
    ("NSSDCA — catálogo de naves", "https://nssdc.gsfc.nasa.gov/nmc/"),
    ("NASA Science — misiones", "https://science.nasa.gov/science-missions/"),
    ("NASA Images", "https://images.nasa.gov"),
    ("JPL Horizons", "https://ssd.jpl.nasa.gov/horizons/"),
    ("NASA Space Place en español", "https://spaceplace.nasa.gov/sp/"),
]

st.set_page_config(
    page_title="Fuentes — ¿Dónde está ahora?",
    page_icon="📚",
    layout="wide",
)
encabezado(
    "Fuentes",
    "Cada dato de la app se puede rastrear a una página oficial de NASA. "
    "Si algo no está aquí, no debería estar en la app.",
    variante="fuentes",
)

piezas = datos.cargar_piezas()

if not piezas:
    st.info("Todavía no hay fuentes porque no hay piezas cargadas.")
    st.stop()

for pieza in piezas:
    st.subheader(pieza.get("nombre", "Pieza"))
    fuentes = pieza.get("fuentes") or []

    if not fuentes:
        st.warning(
            "Esta ficha no tiene fuentes. Investigación debe agregarlas en "
            "`contenido/fichas.csv`."
        )
    else:
        for fuente in fuentes:
            titulo = fuente.get("titulo") or "Fuente sin título"
            url = fuente.get("url") or ""
            consultado = fuente.get("consultado") or ""
            if url:
                st.markdown(f"- [{titulo}]({url}) — consultado el {consultado}")
            else:
                st.markdown(f"- {titulo} — consultado el {consultado}")

    st.caption(
        f"Imagen: {pieza.get('credito_imagen', 'sin crédito')} · "
        f"Revisó: {pieza.get('revisor', 'pendiente')}"
    )
    st.divider()

st.subheader("Enlaces oficiales del proyecto")
for titulo, url in ENLACES_OFICIALES:
    st.markdown(f"- [{titulo}]({url})")

st.page_link("pages/0_Inicio.py", label="Volver al inicio", icon=":material/keyboard_double_arrow_left:")

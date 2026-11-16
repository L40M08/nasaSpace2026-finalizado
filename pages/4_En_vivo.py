"""Panel de datos en vivo. Dueño: Frontend.

No llama a internet: `core.vivo` ya se encarga de la API, el respaldo y la
caché. Aquí solo se pinta.
"""

from __future__ import annotations

import streamlit as st

from components.ui import encabezado
from core import datos, formato, vivo

ESTADOS = {
    "ok": "En vivo",
    "stale": "Último dato guardado",
    "error": "Sin dato",
}

st.set_page_config(
    page_title="En vivo — ¿Dónde está ahora?",
    page_icon="📡",
    layout="wide",
)
encabezado(
    "En vivo",
    "Cuánto han viajado estas naves y cuánto tarda su señal en llegar a la "
    "Tierra. El dato se calcula con JPL Horizons.",
    variante="vivo",
)

piezas = datos.cargar_piezas()
conectadas = [pieza for pieza in piezas if pieza.get("horizons_id")]

if not conectadas:
    st.info(
        "Ninguna pieza tiene `horizons_id`. Backend debe agregarlo solo a las "
        "naves del espacio profundo."
    )
    st.stop()

panel = vivo.datos_en_vivo(piezas)

aviso = vivo.aviso_panel(panel)
if aviso:
    st.info(aviso)
elif panel.get("source"):
    st.caption(
        f"Fuente: {panel['source']} · actualizado "
        f"{formato.antiguedad_texto(panel.get('generated_at'))}"
    )

for pieza in conectadas:
    objeto = vivo.objeto(panel, pieza.get("id", ""))

    st.subheader(pieza.get("nombre", "Pieza"))
    columnas = st.columns(3)
    columnas[0].metric(
        "Distancia a la Tierra",
        formato.distancia_texto(objeto.get("distance_km")),
    )
    columnas[1].metric(
        "La señal tarda",
        formato.tiempo_luz_texto(objeto.get("light_time_s")),
    )
    columnas[2].metric(
        "Estado del dato",
        ESTADOS.get(objeto.get("status", "error"), "Sin dato"),
    )

    st.caption(pieza.get("ubicacion_texto", ""))
    st.divider()

st.page_link("pages/0_Inicio.py", label="Volver al inicio", icon=":material/keyboard_double_arrow_left:")

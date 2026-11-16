"""Punto de entrada de «¿Dónde está ahora?».

Dueño: Frontend.

La app usa `st.navigation`: una sola página real (`app.py`) que cambia de
vista sin recargar el documento. Eso evita el parpadeo y el salto de scroll
que produce la navegación multipágina clásica, y permite que la hoja de
estilos y el JavaScript vivan una sola vez en el documento.
"""

from __future__ import annotations

import streamlit as st

from components.ui import aplicar_estilos

st.set_page_config(
    page_title="¿Dónde está ahora?",
    page_icon="🚀",
    layout="wide",
)

# Los estilos se inyectan en <head> una sola vez por sesión. Al cambiar de
# vista no se vuelven a analizar 30 KB de CSS ni se reordena el contenido.
aplicar_estilos()

PAGINAS = [
    st.Page("pages/0_Inicio.py", title="Inicio", icon="🚀", default=True),
    st.Page("pages/1_Luna.py", title="La Luna", icon="🌕"),
    st.Page("pages/2_Marte.py", title="Marte", icon="🔴"),
    st.Page("pages/3_Espacio_profundo.py", title="Espacio profundo", icon="🌌"),
    st.Page("pages/4_En_vivo.py", title="En vivo", icon="📡"),
    st.Page("pages/5_Quiz.py", title="Quiz", icon="🧠"),
    st.Page("pages/6_Fuentes.py", title="Fuentes", icon="📚"),
    # La ficha solo tiene sentido con una pieza elegida: no ocupa un lugar
    # en el menú, pero sigue disponible para `st.switch_page`.
    st.Page("pages/7_Ficha.py", title="Ficha", icon="🛰️", visibility="hidden"),
]

st.navigation(PAGINAS).run()

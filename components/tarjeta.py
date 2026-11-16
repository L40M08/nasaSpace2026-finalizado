"""Tarjeta reutilizable de una pieza.

Dueño: Frontend.
Se usa en el inicio, en las tres zonas y en los resultados del quiz.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent


def tarjeta(pieza: dict[str, Any], *, mostrar_boton: bool = True) -> None:
    """Pinta una pieza. Si la imagen no existe, muestra un marcador de posición."""
    clave = str(pieza.get("id") or "pieza")
    with st.container(border=True, key=f"tarjeta_{clave}"):
        imagen, texto = st.columns([1, 2.4])

        with imagen:
            ruta = RAIZ / str(pieza.get("imagen", ""))
            if pieza.get("imagen") and ruta.exists():
                st.image(str(ruta))
            else:
                st.markdown(
                    '<div class="fe1-sin-imagen">📷<br><small>Imagen pendiente</small></div>',
                    unsafe_allow_html=True,
                )

        with texto:
            estado = pieza.get("estado", "perdido")
            st.markdown(
                f'<span class="fe1-badge fe1-badge--{estado}">'
                f'{pieza.get("etiqueta_estado", "Sin estado")}</span>',
                unsafe_allow_html=True,
            )
            st.subheader(pieza.get("nombre", "Sin nombre"))
            st.caption(f"«{pieza.get('apodo', '')}»")
            st.write(pieza.get("ubicacion_texto", ""))

            if mostrar_boton:
                historia = pieza.get("historia") or {}
                resumen = str(historia.get("que_es") or "Explora la historia de esta máquina.")
                vista_previa = (
                    f"**{pieza.get('nombre', 'Pieza')}**\n\n"
                    f"{resumen}\n\n"
                    f"**Ahora:** {pieza.get('ubicacion_texto', 'Ubicación por confirmar')}"
                )
                if st.button(
                    "Ver ficha",
                    key=f"ver_{pieza.get('id')}",
                    help=vista_previa,
                ):
                    st.session_state["pieza_sel"] = pieza.get("id")
                    st.switch_page("pages/7_Ficha.py")

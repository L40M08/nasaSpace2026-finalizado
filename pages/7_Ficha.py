"""Ficha completa de una pieza. Dueño: Frontend.

Se llega aquí desde una tarjeta o desde un marcador del mapa. La pieza elegida
viaja en `st.session_state["pieza_sel"]`.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from core import datos, formato, vivo

RAIZ = Path(__file__).resolve().parent.parent

ZONA_A_PAGINA = {
    "luna": ("pages/1_Luna.py", "La Luna"),
    "marte": ("pages/2_Marte.py", "Marte"),
    "espacio_profundo": ("pages/3_Espacio_profundo.py", "Espacio profundo"),
}

BLOQUES = [
    ("que_es", "¿Qué es?"),
    ("por_que", "¿Por qué la enviamos?"),
    ("descubrimiento", "¿Qué descubrió?"),
    ("ahora", "¿Dónde está ahora?"),
    ("dato_curioso", "Un dato curioso"),
]

st.set_page_config(
    page_title="Ficha — ¿Dónde está ahora?",
    page_icon="🛰️",
    layout="wide",
)

pieza_id = st.session_state.get("pieza_sel")
pieza = datos.buscar(datos.cargar_piezas(), pieza_id) if pieza_id else None

if pieza is None:
    st.title("Todavía no elegiste una pieza")
    st.write(
        "Entra a una zona, toca una tarjeta o un marcador del mapa, y la ficha "
        "completa aparece aquí."
    )
    columnas = st.columns(3)
    with columnas[0]:
        st.page_link("pages/1_Luna.py", label="La Luna", icon="🌕")
    with columnas[1]:
        st.page_link("pages/2_Marte.py", label="Marte", icon="🔴")
    with columnas[2]:
        st.page_link("pages/3_Espacio_profundo.py", label="Espacio profundo", icon="🌌")
    st.page_link("pages/0_Inicio.py", label="Volver al inicio", icon=":material/keyboard_double_arrow_left:")
    st.stop()

zona = pieza.get("zona", "")
pagina_zona, nombre_zona = ZONA_A_PAGINA.get(
    zona, ("pages/0_Inicio.py", "Inicio")
)

with st.container(key="ficha_cabecera"):
    st.markdown(
        f'<span class="fe1-badge fe1-badge--{pieza.get("estado", "perdido")}">'
        f'{pieza.get("etiqueta_estado", "Sin estado")}</span>',
        unsafe_allow_html=True,
    )
    st.title(pieza.get("nombre", "Pieza sin nombre"))
    st.caption(f"«{pieza.get('apodo', '')}»")

imagen, resumen = st.columns([1.1, 1.6])

with imagen:
    ruta = RAIZ / str(pieza.get("imagen", ""))
    if pieza.get("imagen") and ruta.is_file():
        st.image(str(ruta))
        st.caption(f"Imagen: {pieza.get('credito_imagen', 'sin crédito')}")
    else:
        st.markdown(
            '<div class="fe1-sin-imagen">📷<br><small>Imagen pendiente</small></div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Investigación debe guardar la imagen en `assets/img/` con el nombre "
            "que dice el CSV."
        )

with resumen:
    st.write(pieza.get("ubicacion_texto", ""))
    st.markdown(
        f"**Lanzamiento:** {formato.fecha_texto(pieza.get('lanzamiento'))}  \n"
        f"**Misión:** {pieza.get('mision', 'sin dato')}  \n"
        f"**Agencia:** {pieza.get('agencia', 'sin dato')}  \n"
        f"**Zona:** {nombre_zona}"
    )

    if pieza.get("horizons_id"):
        panel = vivo.datos_en_vivo(datos.cargar_piezas())
        objeto = vivo.objeto(panel, pieza.get("id", ""))
        st.metric(
            "Distancia a la Tierra",
            formato.distancia_texto(objeto.get("distance_km")),
        )
        st.metric(
            "La señal tarda",
            formato.tiempo_luz_texto(objeto.get("light_time_s")),
        )
        aviso = vivo.aviso_panel(panel)
        if aviso:
            st.caption(aviso)
    elif pieza.get("distancia_actual"):
        st.info(pieza["distancia_actual"])

st.divider()

historia = pieza.get("historia") or {}
with st.container(key="historia_ficha"):
    for clave, titulo in BLOQUES:
        texto = historia.get(clave)
        if texto:
            with st.container(key=f"ficha_bloque_{clave}"):
                st.subheader(titulo)
                st.write(texto)

st.divider()

with st.container(key="ficha_fuentes"):
    st.subheader("Fuentes")
    fuentes = pieza.get("fuentes") or []
    if not fuentes:
        st.warning("Esta ficha todavía no tiene fuentes registradas.")
    for fuente in fuentes:
        titulo = fuente.get("titulo") or "Fuente sin título"
        url = fuente.get("url") or ""
        if url:
            st.markdown(f"- [{titulo}]({url})")
        else:
            st.markdown(f"- {titulo}")

st.caption(
    f"Revisó: {pieza.get('revisor', 'pendiente')} · "
    f"Verificado el {pieza.get('fecha_verificacion', 'sin fecha')}"
)

st.divider()
st.page_link(
    pagina_zona,
    label=f"Volver a {nombre_zona}",
    icon=":material/arrow_back:",
)
st.page_link("pages/0_Inicio.py", label="Volver al inicio", icon=":material/keyboard_double_arrow_left:")

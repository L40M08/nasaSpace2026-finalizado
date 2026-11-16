"""Quiz de 30 preguntas, una por pantalla, con fuentes del dataset."""

import streamlit as st

from components.ui import encabezado
from core import datos, quiz

st.set_page_config(page_title="Quiz — ¿Dónde está ahora?", page_icon="🧠", layout="wide")
encabezado(
    "Quiz",
    "Pon a prueba tu curiosidad con 30 preguntas sobre las máquinas exploradoras.",
    variante="quiz",
)

preguntas = quiz.construir_preguntas(datos.cargar_piezas())
if len(preguntas) != 30:
    st.info("Necesitamos las 10 fichas y sus fuentes para preparar las 30 preguntas.")
    st.stop()

st.session_state.setdefault("quiz_mejor", 0)


def iniciar():
    st.session_state["quiz_partida"] = quiz.nueva_partida(preguntas)


def elegir(partida_id, indice, respuesta):
    partida = st.session_state.get("quiz_partida")
    if partida and quiz.responder(partida, partida_id, indice, respuesta):
        if len(partida["respuestas"]) == len(partida["preguntas"]):
            st.session_state["quiz_mejor"] = max(
                st.session_state["quiz_mejor"], partida["aciertos"]
            )


def menu():
    st.session_state.pop("quiz_partida", None)


partida = st.session_state.get("quiz_partida")
if partida is None:
    with st.container(key="quiz_inicio"):
        st.subheader("¿Estás listo?")
        st.metric("Mejor puntuación de esta sesión", f"{st.session_state['quiz_mejor']} / 30")
        st.write("30 preguntas · 1 punto por acierto · Sin límite de tiempo")
        st.write(
            "Elige una respuesta y pasarás a la siguiente pregunta. "
            "Al terminar podrás revisar las respuestas y sus fuentes."
        )
        st.button("Iniciar quiz", key="quiz_iniciar", type="primary", on_click=iniciar)
        st.caption("Cada partida mezcla las preguntas y las opciones. Tu récord dura esta sesión.")
elif len(partida["respuestas"]) < len(partida["preguntas"]):
    indice = len(partida["respuestas"])
    pregunta = partida["preguntas"][indice]
    with st.container(key="quiz_progreso"):
        st.progress(indice / 30, text=f"Pregunta {indice + 1} de 30")
    if indice:
        anterior = partida["preguntas"][indice - 1]
        if partida["respuestas"][-1] == anterior["correcta"]:
            with st.container(key="quiz_feedback_ok"):
                st.success("¡Respuesta anterior correcta!")
        else:
            with st.container(key="quiz_feedback_ko"):
                st.info(f"Respuesta anterior: {anterior['correcta']}")
    with st.container(key="quiz_pregunta"):
        st.subheader(pregunta["pregunta"], anchor=False)
        st.caption("Elige una respuesta. Avanzarás automáticamente.")
        columnas = st.columns(2)
        for numero, opcion in enumerate(pregunta["opciones"]):
            with columnas[numero % 2]:
                st.button(
                    f"{'ABCD'[numero]}. {opcion}",
                    key=f"quiz_opcion_{partida['id']}_{indice}_{numero}",
                    width="stretch",
                    on_click=elegir,
                    args=(partida["id"], indice, opcion),
                )
    st.caption(f"Aciertos: {partida['aciertos']} · Puedes salir y volver durante esta sesión.")
else:
    st.subheader("¡Misión completada!")
    izquierda, derecha = st.columns(2)
    izquierda.metric("Tu puntuación", f"{partida['aciertos']} / 30")
    derecha.metric("Mejor puntuación de esta sesión", f"{st.session_state['quiz_mejor']} / 30")
    st.write("Cada intento es una oportunidad para descubrir algo nuevo.")
    st.button("Volver al menú", key="quiz_menu", on_click=menu, type="primary")
    with st.expander("Revisa tus respuestas y las fuentes"):
        for numero, (pregunta, respuesta) in enumerate(
            zip(partida["preguntas"], partida["respuestas"]), start=1
        ):
            st.markdown(f"**{numero}. {pregunta['pregunta']}**")
            st.write(f"Tu respuesta: {respuesta}")
            st.write(f"Respuesta correcta: {pregunta['correcta']}")
            st.write(pregunta["explicacion"])
            for fuente in pregunta["fuentes"]:
                st.markdown(f"[{fuente['titulo']}]({fuente['url']})")
            st.divider()

st.page_link("pages/0_Inicio.py", label="Volver al inicio", icon=":material/keyboard_double_arrow_left:")

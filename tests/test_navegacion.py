"""Pruebas de la navegación de una sola página y del movimiento de la interfaz.

La app dejó de ser multipágina clásica: `app.py` es el único punto de entrada y
`st.navigation` cambia de vista sin recargar el documento. Estas pruebas fijan
ese contrato y los ganchos de animación para que no se rompan sin avisar.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parent.parent
APP = RAIZ / "app.py"
PAGES = RAIZ / "pages"
UI = RAIZ / "components" / "ui.py"
MOVIMIENTO = RAIZ / "components" / "movimiento.py"


def paginas_registradas() -> set[str]:
    """Rutas de las páginas declaradas en `st.Page(...)` dentro de `app.py`."""
    return set(re.findall(r'st\.Page\(\s*"([^"]+)"', APP.read_text(encoding="utf-8")))


def test_la_app_es_una_sola_pagina_con_st_navigation() -> None:
    codigo = APP.read_text(encoding="utf-8")
    assert "st.navigation(" in codigo
    assert 'st.Page("pages/0_Inicio.py"' in codigo
    assert "default=True" in codigo


def test_la_ficha_sigue_disponible_pero_fuera_del_menu() -> None:
    codigo = APP.read_text(encoding="utf-8")
    assert 'st.Page("pages/7_Ficha.py"' in codigo
    assert 'visibility="hidden"' in codigo


def test_la_portada_vive_en_pages_y_es_el_inicio() -> None:
    inicio = PAGES / "0_Inicio.py"
    assert inicio.is_file()
    codigo = inicio.read_text(encoding="utf-8")
    assert "¿Dónde está ahora?" in codigo
    assert "sistema_solar()" in codigo
    assert "tarjeta(" in codigo


def test_todas_las_paginas_registradas_existen() -> None:
    registradas = paginas_registradas()
    assert registradas, "app.py no registra ninguna página"
    faltan = sorted(ruta for ruta in registradas if not (RAIZ / ruta).is_file())
    assert not faltan, f"Páginas registradas que no existen: {faltan}"


def test_los_enlaces_apuntan_solo_a_paginas_registradas() -> None:
    destinos: set[str] = set()
    archivos = [APP, *PAGES.glob("*.py"), *(RAIZ / "components").glob("*.py")]
    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8")
        destinos |= set(re.findall(r'st\.page_link\(\s*"([^"]+)"', texto))
    assert destinos, "No se encontró ningún st.page_link"
    # `st.page_link("app.py")` falla bajo st.navigation: la portada es una página.
    assert "app.py" not in destinos
    assert destinos <= paginas_registradas(), destinos - paginas_registradas()


def test_solo_el_punto_de_entrada_instala_los_estilos() -> None:
    assert "aplicar_estilos()" in APP.read_text(encoding="utf-8")
    for pagina in PAGES.glob("*.py"):
        texto = pagina.read_text(encoding="utf-8")
        assert "aplicar_estilos" not in texto, f"{pagina.name} vuelve a inyectar el CSS"


def test_la_portada_abre_sin_excepciones() -> None:
    app = AppTest.from_file("../app.py").run()
    assert not app.exception
    assert {m.label for m in app.metric} == {
        "Piezas en total",
        "En la Luna",
        "En Marte",
        "En el espacio profundo",
    }
    assert "Algunas de las piezas" in [s.value for s in app.subheader]


def test_el_movimiento_esta_en_un_solo_modulo() -> None:
    texto = MOVIMIENTO.read_text(encoding="utf-8")
    for gancho in (
        "fe1-entrando",
        "fe1-menu-entra",
        "fe1-revelar",
        "fe1-revelado",
        "fe1-progreso",
        "IntersectionObserver",
    ):
        assert gancho in texto, f"Falta el gancho {gancho}"


def test_el_movimiento_respeta_menos_movimiento() -> None:
    texto = MOVIMIENTO.read_text(encoding="utf-8")
    assert "prefers-reduced-motion: reduce" in texto
    # Sin JavaScript o con movimiento reducido no se oculta nada: la clase que
    # esconde bloques solo la añade el guion, nunca el HTML de la página.
    assert 'classList.add("fe1-revelar")' in texto
    assert "if (!observador || MENOS.matches) return;" in texto


def test_el_revelado_no_oculta_lo_que_ya_se_ve() -> None:
    texto = MOVIMIENTO.read_text(encoding="utf-8")
    # Solo se anima lo que empieza por debajo del área visible; un bloque
    # parcialmente visible no debe parpadear.
    assert "if (caja.top < alto) return;" in texto


def test_el_menu_movil_se_cierra_al_navegar() -> None:
    texto = MOVIMIENTO.read_text(encoding="utf-8")
    assert "cerrarMenuEstrecho" in texto
    assert "max-width: 760px" in texto
    assert "stSidebarCollapseButton" in texto


def test_la_hoja_se_instala_en_head_una_sola_vez() -> None:
    texto = UI.read_text(encoding="utf-8")
    assert 'hoja.id = "fe1-estilos"' in texto
    assert "document.head.appendChild(hoja)" in texto
    assert "sessionStorage" in texto
    assert 'st.session_state.get("_fe1_estilos")' in texto


@pytest.mark.parametrize(
    "clave",
    ["quiz_progreso", "quiz_feedback_ok", "quiz_feedback_ko"],
)
def test_el_quiz_expone_las_claves_de_movimiento(clave: str) -> None:
    texto = (PAGES / "5_Quiz.py").read_text(encoding="utf-8")
    assert f'key="{clave}"' in texto

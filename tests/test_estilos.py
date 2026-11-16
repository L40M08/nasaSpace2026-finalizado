"""Pruebas de la identidad visual y de las fuentes locales."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
CSS = RAIZ / "assets" / "styles.css"
CONFIG = RAIZ / ".streamlit" / "config.toml"
FUENTES = RAIZ / "static" / "fonts"
ENCABEZADOS = RAIZ / "static" / "img" / "encabezados"

FAMILIAS = {
    "Orbitron": FUENTES / "orbitron-latin.woff2",
    "Overpass": FUENTES / "overpass-latin.woff2",
}

FONDOS = (
    "luna_apollo17.jpg",
    "marte_viking1.jpg",
    "espacio_voyager.jpg",
    "vivo_apollo8.jpg",
    "quiz_sistema_solar.jpg",
    "inicio_tres_mundos.jpg",
)


@pytest.fixture(scope="module")
def css() -> str:
    return CSS.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def config() -> dict:
    with CONFIG.open("rb") as archivo:
        return tomllib.load(archivo)


@pytest.mark.parametrize("familia,archivo", FAMILIAS.items())
def test_la_fuente_existe_y_pesa_menos_de_60_kb(familia: str, archivo: Path) -> None:
    assert archivo.is_file(), f"Falta la fuente {familia}: {archivo}"
    assert 0 < archivo.stat().st_size < 60 * 1024


@pytest.mark.parametrize(
    "licencia",
    ["OFL-Orbitron.txt", "OFL-Overpass.txt"],
)
def test_la_licencia_ofl_esta_empaquetada(licencia: str) -> None:
    archivo = FUENTES / licencia
    assert archivo.is_file()
    assert "SIL OPEN FONT LICENSE" in archivo.read_text(encoding="utf-8").upper()


def test_el_css_no_pide_nada_por_internet(css: str) -> None:
    assert "http://" not in css
    assert "https://" not in css


def test_el_css_declara_las_dos_familias_locales(css: str) -> None:
    assert '@font-face' in css
    assert "/app/static/fonts/orbitron-latin.woff2" in css
    assert "/app/static/fonts/overpass-latin.woff2" in css
    assert 'font-family: "Orbitron"' in css
    assert 'font-family: "Overpass"' in css


def test_el_css_usa_la_paleta_oficial(css: str) -> None:
    for color in ("#07173f", "#0042a6", "#0960e1", "#2e96f5", "#e43700", "#eafe07"):
        assert color in css.lower()


def test_el_css_reserva_espacio_para_la_barra_superior(css: str) -> None:
    # El header de Streamlit mide 60 px y es absoluto: sin colchón tapa el
    # encabezado y la etiqueta de la ficha.
    assert "padding-top: 4.75rem" in css


def test_el_css_usa_fotos_reales_en_los_seis_encabezados(css: str) -> None:
    for fondo in FONDOS:
        assert f"/app/static/img/encabezados/{fondo}" in css


@pytest.mark.parametrize("nombre", FONDOS)
def test_los_fondos_son_horizontales_y_pesan_menos_de_300_kb(nombre: str) -> None:
    archivo = ENCABEZADOS / nombre
    assert archivo.is_file(), f"Falta el fondo {nombre}"
    assert 0 < archivo.stat().st_size < 300 * 1024
    with Image.open(archivo) as imagen:
        assert imagen.size == (1200, 675)


def test_el_css_tiene_foco_visible_y_movimiento_reducido(css: str) -> None:
    assert ":focus-visible" in css
    assert "prefers-reduced-motion" in css
    assert "min-height: 2.7rem" in css


def test_el_css_trae_las_animaciones_de_la_interfaz(css: str) -> None:
    for clave in (
        "fe1-entrada-pagina",
        "fe1-menu-entra",
        "fe1-acierto",
        "fe1-fallo",
        "fe1-revelar",
        "fe1-progreso",
    ):
        assert clave in css, f"Falta la animación {clave}"


def test_el_revelado_solo_oculta_mientras_el_guion_lo_pide(css: str) -> None:
    # La clase `fe1-revelar` la pone JavaScript; sin ella el contenido se ve.
    oculto = re.search(r"\.fe1-revelar \{(.*?)\}", css, re.S)
    assert oculto and "opacity: 0" in oculto.group(1)
    visible = re.search(r"\.fe1-revelar\.fe1-revelado \{(.*?)\}", css, re.S)
    assert visible and "opacity: 1" in visible.group(1)


def test_el_movimiento_reducido_anula_animaciones(css: str) -> None:
    bloque = css[css.index("prefers-reduced-motion: reduce") :]
    assert "animation-duration: 0.001ms !important" in bloque
    assert "transition-duration: 0.001ms !important" in bloque


def test_el_modo_demo_escapa_del_movimiento_reducido(css: str) -> None:
    # `?movimiento=completo` pone la clase en <html>; el bloque de movimiento
    # reducido no debe alcanzarla.
    assert "html:not(.fe1-movimiento-forzado) *," in css
    assert "html:not(.fe1-movimiento-forzado) *::before," in css
    assert "html:not(.fe1-movimiento-forzado) *::after" in css


def test_el_css_no_rompe_el_guion_que_lo_instala(css: str) -> None:
    # La hoja viaja dentro de un <script> inline. Un `<` literal en un
    # comentario (por ejemplo `<html>`) hace que el saneador de HTML descarte
    # el bloque entero y la app se quede sin estilos.
    assert "<" not in css


def test_las_tarjetas_y_los_mapas_reservan_su_espacio(css: str) -> None:
    # Streamlit 1.67 ya no usa `stVerticalBlockBorderWrapper` para los
    # contenedores con borde: la clave de la tarjeta es el selector vigente.
    assert '[class*="st-key-tarjeta_"]' in css
    assert "aspect-ratio: 4 / 3" in css
    assert "aspect-ratio: 1600 / 764" in css


def test_el_aviso_de_enlace_copiado_es_legible(css: str) -> None:
    # El aviso flota sobre el contenido: fondo Deep Blue, texto blanco y
    # borde del amarillo oficial para que se vea sin depender del tema.
    assert ".fe1-aviso-ancla" in css
    assert "position: fixed" in css
    assert "var(--fe1-deep)" in css
    assert "var(--fe1-white)" in css


def test_las_metricas_muestran_el_texto_completo(css: str) -> None:
    # Streamlit recorta con puntos suspensivos; «25 893 millones de km» y
    # «23 horas 59 minutos» deben poder bajar a dos líneas.
    assert '[data-testid="stMetricValue"] [data-testid="stMarkdownContainer"]' in css
    assert '[data-testid="stMetricLabel"] [data-testid="stMarkdownContainer"]' in css
    assert "white-space: normal" in css
    assert "text-overflow: clip" in css


def test_los_botones_de_regreso_usan_iconos_locales() -> None:
    paginas = [
        RAIZ / "pages" / "4_En_vivo.py",
        RAIZ / "pages" / "5_Quiz.py",
        RAIZ / "pages" / "6_Fuentes.py",
        RAIZ / "pages" / "7_Ficha.py",
        RAIZ / "components" / "zonas.py",
    ]
    texto = "\n".join(pagina.read_text(encoding="utf-8") for pagina in paginas)
    assert 'icon=":material/keyboard_double_arrow_left:"' in texto
    assert 'icon=":material/arrow_back:"' in texto
    assert "🏠" not in texto


def test_el_css_trae_los_encabezados_tematicos(css: str) -> None:
    for variante in (
        "luna",
        "marte",
        "espacio-profundo",
        "vivo",
        "quiz",
        "fuentes",
        "inicio",
    ):
        assert f".fe1-hero--{variante}" in css


def test_la_barra_lateral_dice_menu(css: str) -> None:
    assert '[data-testid="stSidebarNav"]::before' in css
    assert 'content: "Menú"' in css
    # Letra grande para el rótulo y para los enlaces.
    assert "font-size: 1.5rem" in css
    assert "font-size: 1.08rem" in css


def test_el_tema_es_oscuro_y_oficial(config: dict) -> None:
    tema = config["theme"]
    assert tema["base"] == "dark"
    assert tema["backgroundColor"].lower() == "#07173f"
    assert tema["primaryColor"].lower() == "#eafe07"
    assert tema["textColor"].lower() == "#eaf0ff"


def test_el_tema_carga_las_dos_familias_locales(config: dict) -> None:
    tema = config["theme"]
    assert "Orbitron" in tema["headingFont"]
    assert "Overpass" in tema["font"]

    familias = {fuente["family"]: fuente for fuente in tema["fontFaces"]}
    assert set(familias) == {"Orbitron", "Overpass"}
    for fuente in familias.values():
        assert fuente["url"].startswith("app/static/fonts/")
        assert fuente["url"].endswith(".woff2")


def test_la_app_no_muestra_el_selector_de_tema(config: dict, css: str) -> None:
    # `minimal` deja solo las opciones que declara la app: sin menú de
    # desarrollador ni selector de fondo claro/oscuro. La CSS lo refuerza.
    assert config["client"]["toolbarMode"] == "minimal"
    assert '[data-testid="stMainMenu"]' in css
    assert "display: none" in css


def test_el_servidor_sirve_los_archivos_estaticos(config: dict) -> None:
    assert config["server"]["enableStaticServing"] is True


def _luminancia(color: str) -> float:
    """Luminancia relativa WCAG de un color hexadecimal."""
    valor = color.lstrip("#")
    canales = [int(valor[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lineales = [
        canal / 12.92 if canal <= 0.04045 else ((canal + 0.055) / 1.055) ** 2.4
        for canal in canales
    ]
    return 0.2126 * lineales[0] + 0.7152 * lineales[1] + 0.0722 * lineales[2]


def _contraste(texto: str, fondo: str) -> float:
    alto, bajo = sorted((_luminancia(texto), _luminancia(fondo)), reverse=True)
    return (alto + 0.05) / (bajo + 0.05)


@pytest.mark.parametrize(
    "texto,fondo",
    [
        ("#EAF0FF", "#07173F"),  # texto principal sobre Deep Blue
        ("#B9C8E8", "#0A2258"),  # texto suave sobre superficie
        ("#93A7CE", "#07173F"),  # texto tenue sobre fondo
        ("#EAFE07", "#07173F"),  # acento sobre Deep Blue
        ("#07173F", "#EAFE07"),  # botón primario
        ("#FFFFFF", "#0042A6"),  # blanco sobre Electric Blue
        ("#07173F", "#2E96F5"),  # texto oscuro sobre Blue Yonder
    ],
)
def test_el_contraste_cumple_aa(texto: str, fondo: str) -> None:
    assert _contraste(texto, fondo) >= 4.5

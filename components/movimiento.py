"""Movimiento de la interfaz: transiciones, revelado y barra de progreso.

Dueño: Frontend.

Todo el movimiento vive en un solo lugar y se apoya en dos reglas:

1. **Nada de contenido invisible sin JavaScript.** Las clases que ocultan un
   bloque (`fe1-revelar`) las pone el propio guion cuando ya puede observar el
   elemento. Si el navegador no ejecuta JavaScript, la página se ve completa.
2. **`prefers-reduced-motion` manda.** Si la persona pidió menos movimiento,
   no se añaden clases de animación y lo que ya estaba oculto se muestra de
   inmediato.
"""

from __future__ import annotations

# El guion se ejecuta una sola vez por documento. Streamlit vuelve a inyectarlo
# en cada rerun, así que la primera línea corta si ya está instalado.
MOVIMIENTO = """
<script>
(() => {
  if (window.__fe1Movimiento) return;
  window.__fe1Movimiento = true;

  const MENOS = window.matchMedia("(prefers-reduced-motion: reduce)");
  const ESTRECHO = window.matchMedia("(max-width: 760px)");
  const main = () => document.querySelector('[data-testid="stMain"]');
  const hero = () => document.querySelector('[data-testid="stMain"] .fe1-hero');

  /* --- 1. Entrada de página -------------------------------------------- */

  let firma = "";
  let temporizadorEntrada = 0;

  function entrada() {
    const contenedor = main();
    if (!contenedor || MENOS.matches) return;
    contenedor.classList.remove("fe1-entrando");
    void contenedor.offsetWidth;
    contenedor.classList.add("fe1-entrando");
    window.clearTimeout(temporizadorEntrada);
    temporizadorEntrada = window.setTimeout(
      () => contenedor.classList.remove("fe1-entrando"),
      760
    );
  }

  /* --- 2. Menú lateral -------------------------------------------------- */

  function menu() {
    const lista = document.querySelector('[data-testid="stSidebarNavItems"]');
    if (!lista || MENOS.matches) return;
    lista.classList.remove("fe1-menu-entra");
    void lista.offsetWidth;
    lista.classList.add("fe1-menu-entra");
  }

  /* En el móvil el menú es una capa que tapa el contenido. Streamlit no lo
     cierra al cambiar de vista dentro de `st.navigation`, así que lo cerramos
     nosotros después de navegar: si no, la sección elegida queda debajo. */
  function cerrarMenuEstrecho() {
    if (!ESTRECHO.matches) return;
    const lateral = document.querySelector('[data-testid="stSidebar"]');
    if (!lateral || lateral.getAttribute("data-collapsed") !== "false") return;
    const boton = document.querySelector(
      '[data-testid="stSidebarCollapseButton"] button'
    );
    if (boton) boton.click();
  }

  /* --- 3. Revelado al hacer scroll -------------------------------------- */

  const SELECTORES = [
    '[class*="st-key-tarjeta_"]',
    '[data-testid="stVerticalBlockBorderWrapper"]',
    '[data-testid="stMetric"]',
    '[data-testid="stAlert"]',
    '[class*="st-key-mapa_"]',
    '[class*="st-key-ficha_"]',
    '[class*="st-key-quiz_feedback_"]',
    '[data-testid="stExpander"]'
  ];

  const observador =
    "IntersectionObserver" in window
      ? new IntersectionObserver(
          (entradas) => {
            const visibles = entradas.filter((e) => e.isIntersecting);
            visibles.forEach((e, i) => {
              e.target.style.transitionDelay = Math.min(i, 6) * 65 + "ms";
              e.target.classList.add("fe1-revelado");
              observador.unobserve(e.target);
            });
          },
          { threshold: 0.08, rootMargin: "0px 0px -6% 0px" }
        )
      : null;

  const vistos = new WeakSet();
  let ultimoBarrido = 0;

  function preparar() {
    if (!observador || MENOS.matches) return;
    const ahora = performance.now();
    if (ahora - ultimoBarrido < 120) return;
    ultimoBarrido = ahora;

    const alto = window.innerHeight;
    for (const selector of SELECTORES) {
      document.querySelectorAll(selector).forEach((el) => {
        if (vistos.has(el)) return;
        vistos.add(el);
        if (el.classList.contains("fe1-revelado")) return;
        if (el.classList.contains("fe1-revelar")) return;
        if (el.querySelector(".fe1-revelar")) return;

        const caja = el.getBoundingClientRect();
        if (caja.height < 24) return;
        // Lo que ya se ve, aunque sea un poco, no se oculta: aparecería un
        // parpadeo. Solo se anima lo que empieza por debajo de la pantalla.
        if (caja.top < alto) return;

        el.classList.add("fe1-revelar");
        observador.observe(el);
      });
    }
  }

  /* --- 4. Barra de progreso de lectura ---------------------------------- */

  let barra = document.getElementById("fe1-progreso");
  if (!barra) {
    barra = document.createElement("div");
    barra.id = "fe1-progreso";
    barra.setAttribute("aria-hidden", "true");
    document.body.appendChild(barra);
  }

  function progreso() {
    const contenedor = main();
    if (!contenedor) return;
    const recorrido = contenedor.scrollHeight - contenedor.clientHeight;
    const avance = recorrido > 80 ? contenedor.scrollTop / recorrido : 0;
    barra.style.transform = "scaleX(" + avance + ")";
    barra.classList.toggle("fe1-progreso--visible", avance > 0.01);
  }

  function engancharScroll() {
    const contenedor = main();
    if (!contenedor || contenedor.dataset.fe1Scroll) return;
    contenedor.dataset.fe1Scroll = "1";
    contenedor.addEventListener("scroll", progreso, { passive: true });
  }

  /* --- 5. Cambio de vista ----------------------------------------------- */

  let pendiente = false;
  let temporizadorCambio = 0;

  function revisar() {
    if (pendiente) return;
    pendiente = true;
    window.requestAnimationFrame(() => {
      pendiente = false;

      const titulo = hero() ? hero().querySelector("h1") : null;
      const actual =
        location.pathname + "|" + (titulo ? titulo.textContent.trim() : "");
      if (actual !== firma) {
        firma = actual;
        // Al cambiar de vista el DOM puede mostrar todavía el título anterior
        // con la URL nueva. 90 ms alcanzan para que llegue el título bueno y
        // la entrada se anime una sola vez.
        window.clearTimeout(temporizadorCambio);
        temporizadorCambio = window.setTimeout(() => {
          entrada();
          if (ESTRECHO.matches) cerrarMenuEstrecho();
          else menu();
        }, 90);
      }

      engancharScroll();
      progreso();
      preparar();
    });
  }

  let barraLateralObservada = null;
  function observarMenu() {
    const lateral = document.querySelector('[data-testid="stSidebar"]');
    if (!lateral || lateral === barraLateralObservada) return;
    barraLateralObservada = lateral;
    new MutationObserver(() => {
      if (lateral.getAttribute("data-collapsed") === "false") menu();
    }).observe(lateral, { attributes: true, attributeFilter: ["data-collapsed"] });
  }

  new MutationObserver(revisar).observe(document.body, {
    childList: true,
    subtree: true
  });
  window.addEventListener("popstate", revisar);
  window.addEventListener("resize", progreso, { passive: true });

  if (MENOS.addEventListener) {
    MENOS.addEventListener("change", (evento) => {
      if (evento.matches) {
        document
          .querySelectorAll(".fe1-revelar")
          .forEach((el) => el.classList.add("fe1-revelado"));
      }
    });
  }

  revisar();
  observarMenu();
})();
</script>
"""

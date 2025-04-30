// menu.js
function loadMenu() {
    const menuHTML = `
        <nav>
            <ul>
                <li><a href="index.html">Inicio</a></li>
                <li><a href="indexestrategias.html">Estrategias</a></li>
                <li><a href="quienes-somos.html">Quiénes Somos</a></li>
                <li><a href="servicios.html">Servicios</a></li>
                <li><a href="franquicias.html">Franquicias</a></li>
                <li><a href="novedades.html">Novedades</a></li>
                <li><a href="contacto.html">Contacto</a></li>
                <li><a href="miembros.html">Miembros</a></li>
                <li><a href="planes.html">Planes</a></li>
                <li><a href="cargar-noticias.html">Cargar Noticias</a></li>
            </ul>
        </nav>
    `;

    // Inserta el menú en el elemento con id="main-nav"
    document.getElementById("main-nav").innerHTML = menuHTML;
}

// Ejecuta la función cuando la página cargue
document.addEventListener("DOMContentLoaded", loadMenu);
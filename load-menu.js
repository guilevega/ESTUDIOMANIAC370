// load-menus.js
function loadHeaderMenu() {
    fetch('header-menu.html')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el menú del encabezado: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("header-nav").innerHTML = data;
        })
        .catch(error => {
            console.error('Error al cargar el menú del encabezado:', error);
            document.getElementById("header-nav").innerHTML = '<p>Error al cargar el menú del encabezado.</p>';
        });
}

function loadRightSidebarMenu() {
    fetch('right-sidebar-menu.html')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el menú de la barra lateral derecha: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("right-sidebar").innerHTML = data;
        })
        .catch(error => {
            console.error('Error al cargar el menú de la barra lateral derecha:', error);
            document.getElementById("right-sidebar").innerHTML = '<p>Error al cargar el menú de la barra lateral derecha.</p>';
        });
}

function loadLeftSidebarMenu() {
    // Determinar qué archivo cargar según la página actual
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const leftSidebarFile = currentPage === 'impuestos-nacionales.html' ? 'left-sidebar-impuestos.html' : 'left-sidebar-menu.html';

    fetch(leftSidebarFile)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el menú de la barra lateral izquierda: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("left-sidebar").innerHTML = data;
        })
        .catch(error => {
            console.error('Error al cargar el menú de la barra lateral izquierda:', error);
            document.getElementById("left-sidebar").innerHTML = '<p>Error al cargar el menú de la barra lateral izquierda.</p>';
        });
}

document.addEventListener("DOMContentLoaded", () => {
    loadHeaderMenu();
    loadRightSidebarMenu();
    loadLeftSidebarMenu();
});
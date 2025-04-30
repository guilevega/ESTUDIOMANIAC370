// Mostrar/Ocultar el menú desplegable al hacer clic
document.addEventListener('DOMContentLoaded', function () {
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownBtn.addEventListener('click', function () {
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    // Cerrar el menú si se hace clic fuera de él
    document.addEventListener('click', function (event) {
        if (!dropdownBtn.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.style.display = 'none';
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    // Obtener todos los títulos (h1) que actuarán como botones
    const titles = document.querySelectorAll('section h1');

    titles.forEach(title => {
        // Obtener el ID de la sección para determinar a qué página redirigir
        const sectionId = title.parentElement.id;
        let targetPage = '';

        // Mapear el ID de la sección a la página correspondiente
        switch (sectionId) {
            case 'inicio':
                targetPage = 'index.html';
                break;
            case 'quienes-somos':
                targetPage = 'quienes-somos.html';
                break;
            case 'servicios':
                targetPage = 'servicios.html';
                break;
            case 'franquicias':
                targetPage = 'franquicias.html';
                break;
            case 'novedades':
                targetPage = 'novedades.html';
                break;
            case 'contacto':
                targetPage = 'contacto.html';
                break;
            case 'miembros':
                targetPage = 'miembros.html';
                break;
            case 'planes':
                targetPage = 'planes.html';
                break;
            default:
                targetPage = 'index.html';
        }

        // Agregar evento de doble clic para redirigir
        title.addEventListener('dblclick', function () {
            window.location.href = targetPage;
        });
    });
});
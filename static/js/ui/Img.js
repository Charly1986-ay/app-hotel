/**
 * Crea un elemento HTML <img> seguro con atributos obligatorios de accesibilidad.
 * @param {string} src - La ruta de la imagen (ej: '/static/img/room-1.jpg' o una URL).
 * @param {string} alt - Descripción de la imagen para accesibilidad y SEO (ej: 'Habitación Suite Matrimonial').
 * @param {string|null} classProperty - Una o más clases CSS opcionales (ej: 'img-fluid rounded').
 * @returns {HTMLImageElement} El elemento img listo para ser insertado en el DOM.
 */
export const createImg = (src, alt, classProperty = null) => {
    const img = document.createElement('img');
    
    // Atributos esenciales y seguros
    img.src = src;
    img.alt = alt;

    // Clases de diseño opcionales
    if (classProperty) {
        img.className = classProperty;
    }

    return img;
};
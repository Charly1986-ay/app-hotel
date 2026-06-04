/**
 * Crea un elemento HTML <button> atómico con ícono y propiedades opcionales.
 * @param {string} text - El texto plano que llevará el botón.
 * @param {string|null} iconClass - Clase de FontAwesome para el ícono (opcional).
 * @param {string|null} classProperty - Una o más clases CSS de diseño (opcional).
 * @param {string|null} idProperty - ID único para el botón (opcional).
 * @param {function|null} onClick - Función callback para el evento click (opcional).
 * @returns {HTMLButtonElement} El elemento botón listo para el DOM.
 */
export function createButton(
    text, 
    iconClass = null, 
    classProperty = null, 
    idProperty = null, 
    onClick = null
) 
{
    const btn = document.createElement('button');

    // 1. Si hay ícono, lo fabricamos de forma nativa y segura
    if (iconClass) {
        const icon = document.createElement('i');
        icon.className = iconClass;
        btn.appendChild(icon);
        btn.append(' '); // Espacio en blanco
    }

    // 2. Inyectamos el texto plano (Cero HTML sucio)
    btn.append(text);

    // 3. Atributos opcionales de estructura y diseño
    if (classProperty) {
        btn.className = classProperty;
    }

    if (idProperty) {
        btn.id = idProperty;
    }

    // 4. Evento interactivo opcional
    if (onClick) {
        btn.addEventListener('click', onClick);
    }

    return btn;
}
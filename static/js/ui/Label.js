/**
 * Crea un elemento Label con ícono opcional y clase de diseño opcional.
 * @param {string} inputId - El ID del input enlazado.
 * @param {string} text - El texto plano del label.
 * @param {string|null} iconClass - Clase de FontAwesome para el ícono (opcional).
 * @param {string|null} className - Clase CSS para el diseño del label (opcional).
 */
export function createLabel(inputId, text, iconClass = null, className = null) {
    const label = document.createElement('label');
    label.htmlFor = inputId;

    // 1. Si nos pasaron un ícono, lo fabricamos y lo metemos primero
    if (iconClass) {
        const icon = document.createElement('i');
        icon.className = iconClass;
        label.appendChild(icon);
        
        // Añadimos un espacio en blanco para que el texto no quede pegado al ícono
        label.appendChild(document.createTextNode(' '));
    }

    // 2. Metemos el texto del label (Ahora usamos textContent de forma segura)
    const textNode = document.createTextNode(text);
    label.appendChild(textNode);

    // 3. Clase opcional para el diseño del label
    if (className) {
        label.className = className;
    }

    return label;
}
/**
 * Crea un elemento HTML <span> genérico con texto y un ícono opcional.
 * @param {string|null} classProperty - Una o más clases CSS separadas por espacios (ej: 'policy-item text-danger').
 * @param {string|HTMLElement} text - El texto plano o el nodo que irá dentro del span.
 * @param {string|null} [iconClass=null] - Opcional. La clase de FontAwesome para el ícono (ej: 'fa-solid fa-clock').
 * @returns {HTMLSpanElement} El elemento span completamente estructurado y listo para usar.
 */
export function createSpan(classProperty, text, iconClass = null) {
    const span = document.createElement('span');
    
    // Usamos className para permitir múltiples clases con espacios sin errores
    if (classProperty) {
        span.className = classProperty;
    }

    if (iconClass) {
        const icon = document.createElement('i');
        icon.className = iconClass; 
        span.appendChild(icon);
        span.append(' ');
    }

    span.append(text);
    return span;
}
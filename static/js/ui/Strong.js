/**
 * Crea un elemento de texto resaltado (strong) puro.
 * @param {string} text - El texto que irá en negrita.
 * @param {string|null} classProperty - Clase CSS opcional.
 */
export const createStrong = (text, classProperty = null) => {
    const strong = document.createElement('strong');
    strong.textContent = text; // Seguro y rápido

    if (classProperty) {
        strong.className = classProperty;
    }

    return strong;
};
/**
 * Crea un input HTML configurable.
 *
 * @param {Object} options
 * @param {string} options.type - Tipo de input (text, email, password, etc.)
 * @param {string} options.name - Nombre del input
 * @param {string} [options.idProperty] - ID opcional del input
 * @param {string} [options.classProperty] - Clases CSS separadas por espacio
 * @param {string} [options.value] - Valor inicial opcional
 * @returns {HTMLInputElement}
 */
export function createInput({
    type = 'text',
    name,
    idProperty,
    classProperty,
    value = ''
}) {
    const input = document.createElement('input');

    input.type = type;
    input.name = name;

    if (idProperty) {
        input.id = idProperty;
    }

    if (classProperty) {
        input.classList.add(...classProperty.split(' '));
    }

    if (value) {
        input.value = value;
    }

    return input;
}
/**
 * Crea un elemento HTML input de tipo date de forma dinámica.
 * @param {string} name - El atributo 'name' para el input.
 * @param {string|null} [valueDefault=null] - El valor inicial. Usa 'today' para la fecha actual o un string en formato 'YYYY-MM-DD'.
 * @param {string|null} [idProperty=null] - El atributo 'id' único para el input. Si es null, no se asignará.
 * @param {string|null} [classProperty=null] - Las clases CSS para el input (separadas por espacios). Si es null, no se asignará.
 * @returns {HTMLInputElement} El elemento input configurado.
 */
export function createInputDate(name, valueDefault = null, idProperty = null, classProperty = null) {
    const input = document.createElement('input');
    input.type = 'date';
    input.name = name;

    if (idProperty !== null) {
        input.id = idProperty;
    }

    if (classProperty !== null) {
        input.className = classProperty;
    }

    if (valueDefault === 'today') {
        const hoy = new Date();
        const año = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, '0');
        const dia = String(hoy.getDate()).padStart(2, '0');
        input.value = `${año}-${mes}-${dia}`;
    } else if (valueDefault !== null) {
        input.value = valueDefault;
    }

    return input;
}
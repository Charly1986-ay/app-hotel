/**
 * Crea un elemento HTML <button> atómico con ícono y propiedades opcionales.  
 * @param {string|null} classProperty - Una o más clases CSS de diseño (opcional).
 * @param {string|null} idProperty - ID único para el botón (opcional). 
 * @returns {HTMLButtonElement} El elemento botón listo para el DOM.
 */
export function createArticle(classProperty = null, idProperty = null) {
    const article = document.createElement('article');

    if (classProperty != null) {
        article.className = classProperty;
    }

    if (idProperty) {
        article.id = idProperty;
    }

    return article;
}
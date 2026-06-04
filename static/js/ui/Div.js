export function createDiv(classCss, content = '') {
    const div = document.createElement('div');
    
    // Asignamos la clase de estilo
    div.className = classCss;
    
    // Si el contenido es texto o HTML, lo agregamos directamente
    if (typeof content === 'string') {
        div.innerHTML = content;
    } 
    // Si lo que le pasamos es otro elemento ya creado del DOM (como un botón), lo añadimos como hijo
    else if (content instanceof HTMLElement) {
        div.appendChild(content);
    }
    
    return div;
}
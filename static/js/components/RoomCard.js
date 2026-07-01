// 1. Diccionario de traducción para los Tipos de Habitación
const TypeRoomTranslation = {
    'standard': 'Estándar',
    'executive': 'Ejecutiva',
    'suite': 'Suite'
};

// 2. Diccionario de traducción y asignación de clases para los Estados
const StatusRoomConfig = {
    'available': { text: 'Disponible', className: 'available' },
    'occupied': { text: 'Ocupada', className: 'occupied' },
    'pending_cleaning': { text: 'Limp. Pendiente', className: 'pending-cleaning' },
    'maintenance': { text: 'Mantenimiento', className: 'maintenance' }
};

/**
 * UI Component: RoomCard
 * Generates a reusable room card element using translation dictionaries.
 * @param {Object} room - The room data from FastAPI ({id, status, type_room, ...})
 * @param {Function} onClickCallback - The business logic function to execute on click
 * @returns {HTMLElement} The configured room card DOM element
 */
export function createRoomCard(room, onClickCallback) {
    const roomCard = document.createElement('div');
    
    // Obtener la configuración del estado de forma segura (fallback si no existe)
    const statusConfig = StatusRoomConfig[room.status] || { text: room.status, className: 'unknown' };
    const translatedType = TypeRoomTranslation[room.type_room] || 'Estándar';
    const displayRoomNumber = room.id || "N/A";

    // 🎨 Aplicamos las clases CSS estrictas organizadas (ej: 'room-card' y 'available')
    roomCard.classList.add('room-card', statusConfig.className);
    roomCard.setAttribute('data-room-number', displayRoomNumber);
    
    // Estructura interna enriquecida con el tipo de habitación traducido
    roomCard.innerHTML = `
        <div class="room-card-number">${displayRoomNumber}</div>
        <div class="room-card-type">${translatedType}</div>
        <span class="room-status-label">${statusConfig.text}</span>
    `;
    
    // Enlace polimórfico del evento Click
    roomCard.addEventListener('click', () => {
        if (typeof onClickCallback === 'function') {
            onClickCallback(displayRoomNumber, room.status);
        }
    });
    
    return roomCard;
}
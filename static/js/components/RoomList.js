// RoomList.js
import { createRoomAvailable } from './ArticleRoomAvailable.js';

export function renderRooms(rooms) {
    // Buscamos el contenedor del catálogo en tu HTML real (ajusta el ID si es otro)
    const container = document.querySelector('.rooms-list');
    if (!container) return;

    // 1. Limpiamos búsquedas anteriores
    container.innerHTML = '';

    if (rooms.length === 0) {
        container.innerHTML = '<p class="empty-msg">No hay habitaciones disponibles para los criterios seleccionados.</p>';
        return;
    }

    // 2. Iteramos las habitaciones filtradas que mandó index.js
    rooms.forEach(room => {
        // Mapeamos las propiedades de tu JSON interno a los parámetros que pide tu función
        const roomArticle = createRoomAvailable(
            room.image || 'default.jpg',        // imageName
            room.type_room,                     // txtRoomTypeSpan
            room.price,                         // textSpanPrice
            room.max_capacity,                  // maxCapacity (ajusta según tus llaves del JSON)
            room.bed_count,                     // badCount
            room.id                             // dataRoomId
        );

        // 3. Inyectamos el elemento del DOM real creado por tu fábrica
        container.appendChild(roomArticle);
    });
}
import { createSidebar } from '../components/Sidebar.js'; 
import { BookingServices } from '../services/BookingServices.js';
import { RoomFilterServices } from '../services/RoomFilterService.js';
import { renderRooms } from '../components/RoomList.js'; 
import { initBookingEvents } from '../events/bookingEvent.js';

document.addEventListener('DOMContentLoaded', () => {    
    const bookingForm = createSidebar();
    
    bookingForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Frena la recarga de la página
        initBookingEvents();
        
        // Extraemos las fechas seleccionadas por el usuario
        const checkIn = document.querySelector('#checkin').value;
        const checkOut = document.querySelector('#checkout').value;


        // =======================================================
        //      CONTROL PREVENTIVO DE FECHAS EN EL CLIENTE
        // =======================================================
        if (checkIn >= checkOut) {
            alert(`Introduzca una fecha válida. La fecha de entrada debe ser menor a la de salida.`);
            return; // Freno de mano: detiene la ejecución aquí mismo
        }


        // =======================================================
        //      ÚNICO VIAJE AL SERVIDOR POR BÚSQUEDA (Asíncrono)
        // =======================================================
        //  Obtenemos la respuesta cruda (el paquete de correo)
        const responseFromServer = await BookingServices.getRoomAvailable(checkIn, checkOut);

        // Abrimos el paquete y extraemos el Array de habitaciones
        const rooms = await responseFromServer.json();

        // Control de salida rápida si el hotel está 100% lleno en esas fechas
        if (!rooms || rooms.length === 0) {
            alert(`Lo sentimos, no tenemos habitaciones disponibles para estas fechas.`);
            renderRooms([]); // Limpiamos las tarjetas de la pantalla
            return; // Freno de mano
        } 

        
        // =======================================================
        //      RECOLECCIÓN EN TIEMPO REAL DEL DOM (Fase 2)
        // =======================================================
        // Buscamos las filas vivas en la interfaz (pueden ser 1, 2 o 3)
        const roomRows = document.querySelectorAll('.room-row');
        
        // Mapeamos las filas para construir nuestro array de demandas puro
        const MaxCapacity = Array.from(roomRows).map(row => {            
            const adultInput = row.querySelector('.adults input') || row.querySelector('input[name="adults"]');
            const childrenInput = row.querySelector('.children input') || row.querySelector('input[name="children"]');
            
            return {
                adult: adultInput ? parseInt(adultInput.value, 10) || 1 : 1, // Por regla, mínimo 1 adulto
                children: childrenInput ? parseInt(childrenInput.value, 10) || 0 : 0
            };
        });


        // =======================================================
        //      FILTRADO EN FRONTEND CON FALLBACK DE NEGOCIO
        // =======================================================
        // Ejecutamos tu filtro matemático (Síncrono, súper veloz en memoria RAM)
        let roomsToRender = RoomFilterServices.filter(rooms, MaxCapacity);
                
        if (roomsToRender.length === 0 && rooms.length > 0) {
            alert("No encontramos habitaciones individuales que cumplan con la capacidad solicitada de pasajeros. Sin embargo, te mostramos todas nuestras opciones disponibles para que consideres reservar varias habitaciones.");
            
            // Reemplazamos el array vacío por todas las habitaciones del backend
            roomsToRender = rooms; 
        }

        
        // =======================================================
        //          PINTAR LA INTERFAZ VISUAL
        // =======================================================
        // Le pasamos el resultado final (filtrado o el fallback total) al componente
        renderRooms(roomsToRender);
    });
});
import { createDiv } from '../ui/Div.js';
import { createButton } from '../ui/Button.js';
import { createLabel } from '../ui/Label.js';
import { createInputDate } from '../ui/InputDate.js';
import { createSpan } from '../ui/Span.js';
import { createStrong } from '../ui/Strong.js';
import { createRoomRow } from './RoomRow.js'; // Nota: Saqué createSpinner si no lo usás directo acá

export function createSidebar() {
    const divSidebar = document.querySelector('#sidebar-container');
    
    // Si por alguna razón el contenedor no existe en el HTML, frenamos para evitar crasheos
    if (!divSidebar) {
        console.error("No se encontró el contenedor #sidebar-container en el DOM.");
        return;
    }

    // Políticas del hotel
    const divHotelPolice = createDiv('hotel-policies');
    divSidebar.appendChild(divHotelPolice);

    const policySpanIn = createSpan('', 'Check-in: ', 'fa-solid fa-clock-rotate-left');
    policySpanIn.append(createStrong('12:00 p.m.'));
    divHotelPolice.appendChild(policySpanIn);

    const policySpanOut = createSpan('', 'Check-out: ', 'fa-solid fa-clock');
    policySpanOut.append(createStrong('10:00 a.m.'));
    divHotelPolice.appendChild(policySpanOut);

    // Formulario principal
    const form = document.createElement('form');
    form.className = 'booking-form';

    // Grupo Fecha de Entrada
    const divGroup1 = createDiv('form-group');
    form.appendChild(divGroup1);

    const labelIn = createLabel('checkin', 'Fecha de Entrada', 'fa-solid fa-calendar-import');
    const inputIn = createInputDate('checkin', 'today', 'checkin', 'form-input');
    divGroup1.appendChild(labelIn);
    divGroup1.appendChild(inputIn);

    // Grupo Fecha de Salida
    const divGroup2 = createDiv('form-group');
    form.appendChild(divGroup2);

    const labelOut = createLabel('checkout', 'Fecha de Salida', 'fa-solid fa-calendar-export');
    const inputOut = createInputDate('checkout', 'today', 'checkout', 'form-input');
    divGroup2.appendChild(labelOut);
    divGroup2.appendChild(inputOut);

    // Título de habitaciones
    const divGroup3 = createDiv('form-group');
    form.appendChild(divGroup3);

    const labelRoom = createLabel('room', 'Habitaciones', 'fa-solid fa-bed', 'form-label');
    divGroup3.appendChild(labelRoom);

    // Contenedor dinámico de filas
    const divRoomsContainer = createDiv('rooms-container');
    form.appendChild(divRoomsContainer);

    const configAdults = { min: 1, max: 5, default: 1 };
    const configChildren = { min: 0, max: 5, default: 0 };    

    // 1. Cargar primera habitación por defecto (canDelete = false)
    divRoomsContainer.appendChild(createRoomRow(false, configAdults, configChildren));

    // 2. Función para añadir más filas de habitaciones
    const handleAddRoom = () => {
        const cantidadActual = divRoomsContainer.querySelectorAll('.room-row').length;
        
        // Si ya hay 3, no hacemos nada (Freno de mano por seguridad)
        if (cantidadActual >= 3) return;

        divRoomsContainer.appendChild(createRoomRow(true, configAdults, configChildren));
    };

    // 3. Botón "+ Añadir Habitación"
    const btnAddRoom = createButton(
        'Añadir Habitación',          
        'fa-solid fa-plus',             
        'btn btn-outline',            
        'btn-add-room',                 
        handleAddRoom                   
    );    
    btnAddRoom.type = 'button'; // <-- IMPORTANTE: Que no sea submit
    form.appendChild(btnAddRoom);

    // 4. El verdadero botón de Buscar (Submit)
    const btnSearchRooms = createButton(
        'Buscar Disponibilidad',
        'fa-solid fa-magnifying-glass',
        'btn btn-primary',
        'btn-search-rooms'
    );
    btnSearchRooms.type = 'submit'; // <-- Este es el que dispara el formulario
    form.appendChild(btnSearchRooms);
   
    divSidebar.appendChild(form);
    return form;
}
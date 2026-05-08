let countRoom = 1;
const MAX_ROOMS = 2;

const roomContainer = document.querySelector('.rooms-container');
const btnAddRoom = document.querySelector('#btn-add-room');

// Inicializa fechas al cargar la página
window.addEventListener('load', () => {
    setDefaultDate();
});

// Botón para agregar habitación
btnAddRoom.addEventListener('click', () => {
    if (countRoom < MAX_ROOMS) {
        countRoom++;
        loadRoom();

        if (countRoom >= MAX_ROOMS) {
            btnAddRoom.disabled = true;
        }
    }
});

// Función para setear fechas por defecto
function setDefaultDate() {
    const checkIn = document.querySelector('#checkin');
    const checkOut = document.querySelector('#checkout');

    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');

    checkIn.value = `${year}-${month}-${day}`;
    checkOut.value = `${year}-${month}-${day}`;
}

// Función para cargar una habitación nueva
function loadRoom() {
    const divRoomRow = document.createElement('div');
    divRoomRow.classList.add('room-row');

    divRoomRow.innerHTML = `
        <div class="room-header">
            <span class="room-title">Habitación ${countRoom}</span>
            ${countRoom > 1 ? `<button type="button" class="btn-delete-icon">
                <i class="fa fa-trash"></i>
            </button>` : ''}
        </div>

        <div class="room-spinners">
            <!-- Adultos -->
            <div class="guest-spinner-group">
                <span class="spinner-label">Adultos</span>
                <div class="spinner-base">
                    <button type="button" class="btn spinner-btn dec-btn">-</button>
                    <input type="text" name="rooms[${countRoom}][adults]" class="spinner-input" value="1" readonly>
                    <button type="button" class="btn spinner-btn inc-btn">+</button>
                </div>
            </div>

            <!-- Niños -->
            <div class="guest-spinner-group">
                <span class="spinner-label">Niños</span>
                <div class="spinner-base">
                    <button type="button" class="btn spinner-btn dec-btn">-</button>
                    <input type="text" name="rooms[${countRoom}][children]" class="spinner-input" value="0" readonly>
                    <button type="button" class="btn spinner-btn inc-btn">+</button>
                </div>
            </div>
        </div>
    `;

    // Agrega listener solo si existe el botón eliminar
    const btnDelete = divRoomRow.querySelector('.btn-delete-icon');
    if (btnDelete) {
        btnDelete.addEventListener('click', () => {
            divRoomRow.remove();
            countRoom = 1;
            btnAddRoom.disabled = false;
        });
    }

    roomContainer.appendChild(divRoomRow);
}
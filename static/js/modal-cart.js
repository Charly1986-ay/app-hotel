const deleteRoom = (index) => {
    let roomsStorage = JSON.parse(localStorage.getItem('rooms'));

    // Eliminar room del indice
    roomsStorage.splice(index, 1);

    // Actualizar el array del localStorage
    localStorage.setItem('rooms', JSON.stringify(roomsStorage));

    // Mostrar el listado
    showCart();
}

const showCart = () => {
    const rooms = document.querySelector('#cartItems');
    rooms.innerHTML = '';

    let roomsStorage = JSON.parse(localStorage.getItem('rooms')) || [];

    if (roomsStorage.length === 0) {
        rooms.innerHTML = 'No hay habitaciones seleccionadas.';
        return false;
    }

    roomsStorage.forEach((room, index) => {
        let divItem = document.createElement('div');
        divItem.classList.add('cartItem');

        divItem.dataset.roomType = room.roomType;
        divItem.dataset.price = room.price;

        divItem.innerHTML = `
            <span class="room-type">${room.roomType}</span>        
            <span class="cart-price-room">${room.price}</span>            
        `;

        const btnDelete = document.createElement('button');    
        
        btnDelete.innerHTML = '<i class="fa-solid fa-trash"></i>';
        
        btnDelete.addEventListener('click', () => deleteRoom(index)); 

        divItem.appendChild(btnDelete);        

        rooms.appendChild(divItem);
    });

    updateTotal();

    return true;
}


const updateTotal = () => {
    let roomsStorage = JSON.parse(localStorage.getItem('rooms'));
    let total = 0;

    roomsStorage.forEach(room => {
        total += room.price;
    });

    document.querySelector('#itemsTotal').textContent = `
        Total: ${total} USD
    `;
}


const saveRoom = (priceStr, roomType, roomId) => {
    let price = parseInt(priceStr);
    let id = parseInt(roomId);

    if (isNaN(price) || price <= 0) {
        console.log("No es un número válido");
        return
    }

    if (isNaN(id) || id <= 0) {
        console.log("No es un número válido");
        return
    }

    let roomObject = {
        roomId: id,
        roomType: roomType,
        price: price,
    }

    console.log(roomObject)

    // Sacar todas las habitaciones guardadas
    let roomsStorage = JSON.parse(localStorage.getItem('rooms'));

    if (!roomsStorage) {
        // No hay habitaciones guardadas
        roomsStorage = [];
    }
    roomsStorage.push(roomObject);

    // Almacenamos en el localstorage
    localStorage.setItem('rooms', JSON.stringify(roomsStorage));

    showCart();

    return true;
}


window.addEventListener('load', (event) => {
    // cargamos las habitaciones
    showCart();

    const btnBookings = document.querySelectorAll('.btn-booking');    

    btnBookings.forEach(btn => {
        btn.addEventListener('click', (event) => {
            // Obtiene el article contenedor del botón
            const divArticle = event.target.closest('article');

            let room = divArticle.querySelector('.room-badge').textContent;

            let priceStr = divArticle.querySelector('.price-amount').textContent.substring(4);
            
            const roomId = btn.dataset.roomId;
            
            saveRoom(priceStr, room, roomId);
        });
    });
}); 
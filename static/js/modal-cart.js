document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       MODAL
    ========================= */

    const modal = document.getElementById("modalRooms");
    const openCart = document.getElementById("openCart");
    const closeBtn = document.querySelector(".close");

    function openModal() {
        if (!modal) return;
        modal.style.display = "block";
    }

    function closeModal() {
        if (!modal) return;
        modal.style.display = "none";
    }

    /* BOTÓN CARRO (HEADER) */
    if (openCart) {
        openCart.addEventListener("click", (e) => {
            e.preventDefault();
            showCart();   // refresca antes de abrir
            openModal();
        });
    }

    /* BOTÓN CERRAR */
    if (closeBtn) {
        closeBtn.addEventListener("click", closeModal);
    }

    /* CLICK FUERA */
    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });


    /* =========================
        CARRITO (TU LÓGICA)
    ========================= */

    const deleteRoom = (index) => {
        let roomsStorage = JSON.parse(localStorage.getItem('rooms')) || [];

        roomsStorage.splice(index, 1);

        localStorage.setItem('rooms', JSON.stringify(roomsStorage));

        showCart();
    };

    const showCart = () => {
        const rooms = document.querySelector('#cartItems');
        if (!rooms) return;

        rooms.innerHTML = '';

        let roomsStorage = JSON.parse(localStorage.getItem('rooms')) || [];

        if (roomsStorage.length === 0) {
            rooms.innerHTML = 'No hay habitaciones seleccionadas.';
            updateTotal();
            return false;
        }

        roomsStorage.forEach((room, index) => {

            let divItem = document.createElement('div');
            divItem.classList.add('cart-item'); // FIX CSS

            divItem.innerHTML = `
                <span class="room-type">${room.roomType}</span>
                <span class="cart-price-room">${room.price} USD</span>
            `;

            const btnDelete = document.createElement('button');
            btnDelete.innerHTML = '<i class="fa-solid fa-trash"></i>';
            //btnDelete.classList.add('remove-item');

            btnDelete.addEventListener('click', () => deleteRoom(index));

            divItem.appendChild(btnDelete);
            rooms.appendChild(divItem);
        });

        updateTotal();
        return true;
    };

    const getTotal = () => {
        let roomsStorage = JSON.parse(localStorage.getItem('rooms')) || [];

        let total = 0;

        roomsStorage.forEach(room => {
            total += Number(room.price);
        });

        return total;
    }

    const updateTotal = () => {
        let total = getTotal();

        const totalEl = document.querySelector('#itemsTotal');

        if (totalEl) {
            totalEl.textContent = `Total: ${total} USD`;
        }
    };

    const saveRoom = (priceStr, roomType, roomId) => {

        let price = parseInt(priceStr);
        let id = parseInt(roomId);

        if (isNaN(price) || price <= 0) return;
        if (isNaN(id) || id <= 0) return;

        let roomObject = {
            roomId: id,
            roomType: roomType,
            price: price,
        };

        let roomsStorage = JSON.parse(localStorage.getItem('rooms')) || [];

        roomsStorage.push(roomObject);

        localStorage.setItem('rooms', JSON.stringify(roomsStorage));

        showCart();
        openModal(); // abre modal al reservar
    };


    /* =========================
       BOTONES RESERVA
    ========================= */

    const btnBookings = document.querySelectorAll('.btn-booking');

    btnBookings.forEach(btn => {
        btn.addEventListener('click', (event) => {

            const divArticle = event.target.closest('article');

            let room = divArticle.querySelector('.room-badge').textContent;

            let priceStr = divArticle
                .querySelector('.price-amount')
                .textContent
                .substring(4);

            const roomId = btn.dataset.roomId;

            saveRoom(priceStr, room, roomId);
        });
    });

    const btnCartPayment = document.querySelector('#btn-cart-payment');
    btnCartPayment.addEventListener('click', (event) => {        
        closeModal();
        
        let checkin = document.querySelector('#checkin').value;
        let checkout = document.querySelector('#checkout').value;
        let total = getTotal();

        let objBooking = {
            checkin,
            checkout,
            total
        };

        localStorage.setItem('booking', JSON.stringify(objBooking));
        window.location = '/payment';
    });


    /* =========================
       INIT
    ========================= */

    showCart();

});
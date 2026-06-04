import { ModalCart } from "../components/ModalCart.js";
import { CartStorageServices } from "../services/CartStorageServices.js";


export const initCartEvent = () => {

    document.addEventListener("click", (e) => {
        if (e.target.closest("#openCart")) {
            ModalCart.open();
            return;
        }

        if (e.target.closest(".close")) {
            ModalCart.close();
            return;
        }

        if (e.target.closest('#btn-cart-payment')) {
            const checkin = document.querySelector('#checkin').value;
            const checkout = document.querySelector('#checkout').value;

            if (checkin >= checkout) {
                alert('Fecha de ingreso no puede ser mayor o igual al de salida');
                return;
            }

            CartStorageServices.setBooking(checkin, checkout);
            window.location.href = "/payment";
            return;
        }
    });
};
import { ModalCart } from "../components/ModalCart.js";
import { CartStorageServices } from "../services/CartStorageServices.js";
import { authRequire } from '../utils/session.js';


export const initCartEvent = () => {

    document.addEventListener("click", async (e) => {
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

            // 1. Validamos fechas primero (así no hacemos trabajar al backend si las fechas están mal)
            if (checkin >= checkout) {
                alert('Fecha de ingreso no puede ser mayor o igual al de salida');
                return;
            }

            // 2. 💾 GUARDADO PREVENTIVO: La reserva queda a salvo en el localStorage
            CartStorageServices.setBooking(checkin, checkout);

            // 🌟 PASO 0: Validar autenticación antes de redireccionar a la pasarela
            const isAuthenticated = await authRequire();
            
            // Si authRequire devolvió false (y adentro ya manejó el desvío al login), frenamos el código aquí
            if (!isAuthenticated) {
                // Dejamos la migaja de pan para saber a dónde regresar tras el login exitoso
                localStorage.setItem('redirect_after_login', '/payment');
                window.location.href = "/auth/login"; // Desvío manual por si authRequire no lo hace automáticamente
                return;
            }

            // 3. Si pasó el authRequire con éxito, va directo a pagar
            window.location.href = "/api/payment";
            return;
        }
    });
};
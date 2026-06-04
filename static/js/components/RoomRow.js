import { createDiv } from '../ui/Div.js';
import { createButton } from '../ui/Button.js';
import { createSpinner } from '../ui/Spinner.js';

/** * Creates a room row with independent guest configuration spinners.
 * @param {boolean} canDelete - Flag to render a remove button.
 * @param {Object} adultsConfig - Limits for adult guests { min, max, defaultValue }
 * @param {Object} childrenConfig - Limits for child guests { min, max, defaultValue }
 */
export function createRoomRow(
    canDelete = false, 
    adultsConfig = { min: 1, max: 5, defaultValue: 1 }, 
    childrenConfig = { min: 0, max: 5, defaultValue: 0 }
) {    
    const roomRow = createDiv('room-row');

    // 1. Header & Actions
    const roomHeader = createDiv('room-header');
    if (canDelete) {
        const btnDelete = createButton('', 'fa-solid fa-trash-can', 'btn-delete-icon', null, () => {
            roomRow.remove();
        });
        btnDelete.type = 'button';
        roomHeader.appendChild(btnDelete);
    }

    // 2. Guest Spinners Container
    const roomSpinners = createDiv('room-spinners');

    // --- Adults Spinner Group ---
    const guestGroupAdults = createDiv('guest-spinner-group');
    const labelAdults = document.createElement('span');
    labelAdults.className = 'spinner-label';
    labelAdults.textContent = 'Adults';
    
    const currentAdultsDefault = adultsConfig?.defaultValue ?? 1;
    const spinnerAdults = createSpinner('adults', adultsConfig.min, adultsConfig.max, currentAdultsDefault); 
    guestGroupAdults.append(labelAdults, spinnerAdults);

    // --- Children Spinner Group ---
    const guestGroupChildren = createDiv('guest-spinner-group');
    const labelChildren = document.createElement('span');
    labelChildren.className = 'spinner-label';
    labelChildren.textContent = 'Children';
    
    const currentChildrenDefault = childrenConfig?.defaultValue ?? 0;
    const spinnerChildren = createSpinner('children', childrenConfig.min, childrenConfig.max, currentChildrenDefault); 
    guestGroupChildren.append(labelChildren, spinnerChildren);

    // --- LÓGICA DE CONTROL: FORZAR RETROCESO EN EL SPINNER ---
    const inputAdults = spinnerAdults.querySelector('input');
    const inputChildren = spinnerChildren.querySelector('input');

    if (inputAdults && inputChildren) {
        const MAX_TOTAL = 5;
        let ultimoSpinnerTocado = null;

        // Detectamos cuál de los dos contenedores de spinner recibió el clic
        spinnerAdults.addEventListener('click', () => { ultimoSpinnerTocado = spinnerAdults; });
        spinnerChildren.addEventListener('click', () => { ultimoSpinnerTocado = spinnerChildren; });

        const verificarYSimularMenos = () => {
            const adults = parseInt(inputAdults.value, 10) || 1;
            const children = parseInt(inputChildren.value, 10) || 0;

            // Si se pasaron de 5 (dio 6)
            if (adults + children > MAX_TOTAL) {
                
                alert("El máximo permitido es de 5 personas por habitación. Si son más huéspedes, por favor añade una nueva habitación.");

                if (ultimoSpinnerTocado) {
                    // Buscamos el botón de restar (-) de ese spinner específico.
                    // Busca por clase (ej: .btn-minus) o asume que es el primer botón del contenedor.
                    const btnMinus = ultimoSpinnerTocado.querySelector('.btn-minus') || 
                                     ultimoSpinnerTocado.querySelector('button:first-of-type') ||
                                     ultimoSpinnerTocado.querySelector('button');

                    // Si encontramos el botón de restar del spinner, le hacemos un clic fantasma
                    if (btnMinus) {
                        btnMinus.click(); 
                    }
                }
            }
        };

        // Escuchamos el click global en la fila con un delay para que tu spinner sume primero,
        // y si se pasa, nuestro código lo obliga inmediatamente a restar.
        roomRow.addEventListener('click', () => {
            setTimeout(verificarYSimularMenos, 15);
        });
    }

    // Assembly
    roomSpinners.append(guestGroupAdults, guestGroupChildren);
    roomRow.append(roomHeader, roomSpinners);

    return roomRow;
}
import { createDiv } from './Div.js';
import { createButton } from './Button.js';

export function createSpinner(idInput, min = 0, max = 10, defaultValue = 0) {
    // 1. Contenedor principal (Tu Div)
    const spinnerContainer = createDiv('spinner-container');

    // 2. 🔥 SOLUCIÓN 1: Input 100% OCULTO (type='hidden') para que no dibuje flechas extras del navegador
    const inputHidden = document.createElement('input');
    inputHidden.type = 'hidden'; 
    inputHidden.name = idInput;
    inputHidden.id = idInput;
    inputHidden.value = defaultValue;

    // 3. 🌟 SOLUCIÓN 2: Creamos el SPAN de forma nativa limpia para evitar que tu 'createSpan' duplique etiquetas
    const numberDisplay = document.createElement('span');
    numberDisplay.id = `spinner-display-${idInput}`;
    numberDisplay.className = 'spinner-display';
    numberDisplay.textContent = defaultValue; // Asigna el número limpiamente

    // 4. Botón Menos (Tu Button)
    const btnMinus = createButton('', 'fa-solid fa-minus', 'spinner-btn decrement', `btn-minus-${idInput}`);
    btnMinus.type = 'button';      

    // 5. Botón Más (Tu Button)
    const btnPlus = createButton('', 'fa-solid fa-plus', 'spinner-btn increment', `btn-plus-${idInput}`);
    btnPlus.type = 'button';

    // --- 🕹️ LÓGICA INTERACTIVA ---
    btnMinus.addEventListener('click', () => {
        let currentValue = parseInt(inputHidden.value);
        if (currentValue > min) {
            currentValue--;
            inputHidden.value = currentValue;
            numberDisplay.textContent = currentValue; 
        }
    });

    btnPlus.addEventListener('click', () => {
        let currentValue = parseInt(inputHidden.value);
        if (currentValue < max) {
            currentValue++;
            inputHidden.value = currentValue;
            numberDisplay.textContent = currentValue;
        }
    });

    // --- 🧱 LAYOUT ASSEMBLY ---
    // Orden exacto: Botón [-] , Número en el medio , Botón [+] e Input oculto al final
    spinnerContainer.append(btnMinus, numberDisplay, btnPlus, inputHidden);

    return spinnerContainer;
}
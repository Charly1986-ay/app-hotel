// components/PaymentForm.js
import { createDiv } from '../ui/Div.js';
import { createLabel } from '../ui/Label.js';
import { createInput } from '../ui/Input.js';
import { createButton } from '../ui/Button.js';

export function createPaymentForm() {
    const divWrapper = document.querySelector('#payment-container');
    if (!divWrapper) return null;

    // Tarjeta contenedora principal
    const divCard = createDiv('auth-card');
    divWrapper.appendChild(divCard);

    // Encabezado
    const divHeader = createDiv('auth-header');
    divHeader.innerHTML = `<h2>Pago Seguro</h2><p>Ingrese los datos de su tarjeta</p>`;
    divCard.appendChild(divHeader);

    // Formulario
    const form = document.createElement('form');
    form.className = 'auth-form';
    form.id = 'paymentForm';
    divCard.appendChild(form);

    // Grupo Titular
    const divGroup1 = createDiv('form-group');
    const labelHolder = createLabel('cardHolder', 'Nombre del titular');
    const inputHolder = createInput('text', 'cardHolder', 'cardHolder', 'cardHolder', 'Juan Pérez');
    inputHolder.required = true;
    divGroup1.appendChild(labelHolder);
    divGroup1.appendChild(inputHolder);
    form.appendChild(divGroup1);

    // Grupo Contenedor de Stripe
    const divGroup2 = createDiv('form-group');
    const labelCard = createLabel('card-element', 'Datos de la tarjeta (Número, Vencimiento y CVC)');
    
    // Contenedor físico donde Stripe va a inyectar sus inputs
    const stripeContainer = createDiv('');
    stripeContainer.id = 'card-element';
    stripeContainer.style.cssText = "padding: 10px; border: 1px solid #ccc; border-radius: 4px; background: white;";
    
    divGroup2.appendChild(labelCard);
    divGroup2.appendChild(stripeContainer);
    form.appendChild(divGroup2);

    // Botón de Submit (Lo creamos vacío o con texto genérico)
    const btnSubmit = createButton('Cargando...', 'fa-solid fa-credit-card', 'btn-submit');
    btnSubmit.type = 'submit';
    form.appendChild(btnSubmit);

    // Al final, devolvemos las referencias que el "manejador de eventos" va a necesitar
    return {
        form: form,
        submitBtn: btnSubmit,
        cardElementId: '#card-element'
    };
}
import { createDiv } from '../ui/Div.js';
import { createSpan } from '../ui/Span.js';
import { createButton } from '../ui/Button.js';

export function createCartItem(roomType, price, index, onDeleteCallback) {
    const divItem = createDiv('cart-item');

    const spanType = createSpan('room-type', roomType, null);
    const spanPrice = createSpan('cart-price-room', `${price} USD`, null);
    const btnDelete = createButton('', 'fa-solid fa-trash', 'remove-item', null, null);

    btnDelete.addEventListener('click', () => onDeleteCallback(index));

    divItem.appendChild(spanType);
    divItem.appendChild(spanPrice);
    divItem.appendChild(btnDelete);

    return divItem;
}
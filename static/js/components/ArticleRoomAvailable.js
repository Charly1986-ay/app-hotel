import { createArticle } from '../ui/Article.js';
import { createDiv } from '../ui/Div.js';
import { createImg } from '../ui/Img.js';
import { createSpan } from '../ui/Span.js';
import { createButton } from '../ui/Button.js';

export function createRoomAvailable(
    imageName, 
    txtRoomTypeSpan, 
    textSpanPrice,
    maxCapacity = 0, 
    bedCount = 0, 
    dataRoomId = 0
){
    // Creamos el article
    const article = createArticle('hotel-post', null);

    // 🌟 Añadimos todos los data-attributes
    article.dataset.roomId = dataRoomId;
    article.dataset.roomName = txtRoomTypeSpan;
    article.dataset.price = textSpanPrice;
    article.dataset.maxCapacity = maxCapacity;
    article.dataset.bedCount = bedCount;

    // DIV IMAGE
    const divRoomImg = createDiv('room-image');
    article.appendChild(divRoomImg);

    const textAltImg = txtRoomTypeSpan.toUpperCase();
    const srcImg = `static/img/${imageName}`;
    const image = createImg(srcImg, textAltImg); 
    const spanRoomBodage = createSpan('room-badge', `${textAltImg}`, null);
    divRoomImg.appendChild(image);
    divRoomImg.appendChild(spanRoomBodage);

    // DIV ROOM PRICE
    const divRoomPrice = createDiv('room-price');
    article.appendChild(divRoomPrice);

    const spanPriceAmout = createSpan('price-amount', `USD ${textSpanPrice}`, null);
    const spanPriceRoom = createSpan('price-night', '/ noche', null);    
    divRoomPrice.appendChild(spanPriceAmout);
    divRoomPrice.appendChild(spanPriceRoom);

    // DIV ROOM CAPACITY
    const divRoomCapacity = createDiv('room-capacity');
    article.appendChild(divRoomCapacity);

    const spanMaxCapacity = createSpan(
        'max-capacity', 
        `${maxCapacity}`, 
        'fa-solid fa-person'
    );
    const spanBedCount = createSpan(
        'bed-count', 
        `${bedCount}`,
        'fa-solid fa-bed'
    );    
    divRoomCapacity.appendChild(spanMaxCapacity);
    divRoomCapacity.appendChild(spanBedCount);    

    // DIV ROOM BUTTONS
    const divRoomButtons = createDiv('room-buttons');
    article.appendChild(divRoomButtons);

    const buttonViewDetails = createButton(
        'Ver Detalles', 
        null, 
        'btn btn-outline', 
        null, 
        null
    );
    const buttonBooking = createButton(
        'Reservar Ahora', 
        null, 
        'btn btn-outline btn-booking', 
        null, 
        null
    );
    // Ya no necesitamos data en el botón, lo leemos del article
    divRoomButtons.appendChild(buttonViewDetails);
    divRoomButtons.appendChild(buttonBooking);

    return article;
}
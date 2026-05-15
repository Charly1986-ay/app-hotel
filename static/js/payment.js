// ======================================
// ELEMENTOS
// ======================================

const paymentForm =
    document.getElementById('paymentForm');

const cardNumber =
    document.getElementById('cardNumber');

const expiryDate =
    document.getElementById('expiryDate');

const successMsg =
    document.getElementById('successMsg');

// ======================================
// FORMATO TARJETA
// ======================================

cardNumber.addEventListener('input', (e) => {

    let value = e.target.value;

    value = value
        .replace(/\D/g, '')
        .substring(0, 16);

    const groups =
        value.match(/.{1,4}/g);

    e.target.value =
        groups
            ? groups.join(' ')
            : '';

});

// ======================================
// FORMATO FECHA
// ======================================

expiryDate.addEventListener('input', (e) => {

    let value = e.target.value;

    value = value
        .replace(/\D/g, '')
        .substring(0, 4);

    if (value.length >= 3) {

        value =
            value.substring(0, 2)
            + '/'
            + value.substring(2);

    }

    e.target.value = value;

});

// ======================================
// SUBMIT
// ======================================

paymentForm.addEventListener('submit', (e) => {

    e.preventDefault();

    successMsg.style.display = 'block';

    successMsg.innerHTML =
        'Pago procesado correctamente';

});
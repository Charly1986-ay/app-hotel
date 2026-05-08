let checkIn = document.querySelector('#checkin');
let checkOut = document.querySelector('#checkout');

const currentDate = new Date();

let year = currentDate.getFullYear();
let month = currentDate.getMonth() + 1;
let day = currentDate.getDate();

if (month < 10) month = '0' + month;
if (day < 10) day = '0' + day;

checkIn.value = `${year}-${month}-${day}`;
checkOut.value = `${year}-${month}-${day}`;

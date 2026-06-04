import { initCartEvent } from "./events/cartEvent.js";


document.addEventListener("DOMContentLoaded", () => {
    initCartEvent();
    
    // =========================
    // MENU MOBILE
    // =========================
    const menuToggle = document.querySelector("#mobile-menu");
    const navList = document.querySelector("#nav-list");

    if (menuToggle && navList) {
        menuToggle.addEventListener("click", () => {
            navList.classList.toggle("active");
        });
    }
});
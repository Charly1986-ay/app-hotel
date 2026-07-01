import { RoomServices } from '../services/RoomServices.js';
import { createRoomCard } from '../components/RoomCard.js';
import { RoomEventHandlers } from '../events/roomEvent.js';

// Elementos del DOM - Tus Pestañas Macro Originales
const macroTabs = document.querySelectorAll('.tabs-menu .tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');

// Elementos del DOM - Internos de Habitaciones
const gridContainer = document.getElementById('roomsGridContainer');
const statusButtons = document.querySelectorAll('.status-filters .status-btn');
const addRoomBtn = document.getElementById('addRoomBtn');

// Estado de la aplicación
let currentFilter = 'all';
let pollingInterval = null;
const POLLING_TIME = 15000;

/**
 * Peticiona y renderiza la grilla de habitaciones
 */
async function fetchAndRenderRooms() {
    const activeRoomsPanel = document.getElementById('tab-rooms');
    if (!gridContainer || !activeRoomsPanel.classList.contains('is-active')) return;
    
    const rooms = await RoomServices.listRooms(currentFilter);
    gridContainer.innerHTML = ""; 

    if (!rooms || rooms.length === 0) {
        gridContainer.innerHTML = `
            <div class="empty-state">
                <p>No hay habitaciones en estado <strong>${currentFilter.replace('_', ' ')}</strong>.</p>
            </div>
        `;
        return;
    }

    rooms.forEach(room => {
        const roomCardElement = createRoomCard(room, RoomEventHandlers.onCardClick);
        gridContainer.appendChild(roomCardElement);
    });

    console.log(`[Sync] Grilla [Filtro: ${currentFilter}] - ${new Date().toLocaleTimeString()}`);
}

/**
 * Control del Polling
 */
function startPolling() {
    if (!pollingInterval) {
        pollingInterval = setInterval(fetchAndRenderRooms, POLLING_TIME);
        console.log("[Sync] Polling reactivado.");
    }
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
        console.log("[Sync] Polling pausado.");
    }
}

/**
 * Navegación de tus pestañas originales usando data-target e is-active
 */
function setupNavigationTabs() {
    macroTabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            const targetId = e.currentTarget.getAttribute('data-target');
            
            // 1. Alternar estado activo en los botones de tu menú
            macroTabs.forEach(t => t.classList.remove('is-active'));
            e.currentTarget.classList.add('is-active');
            
            // 2. Alternar visibilidad en tus paneles originales
            tabPanels.forEach(panel => panel.classList.remove('is-active'));
            const targetPanel = document.querySelector(targetId);
            if (targetPanel) targetPanel.classList.add('is-active');
            
            // 3. Control inteligente del Polling según el panel visible
            if (targetId === '#tab-rooms') {
                fetchAndRenderRooms();
                startPolling();
            } else {
                stopPolling();
            }
        });
    });
}

/**
 * Filtros de estado internos (.status-btn)
 */
function setupStatusFilters() {
    statusButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            const targetFilter = e.currentTarget.getAttribute('data-status') || 'all';
            if (currentFilter === targetFilter) return;
            
            statusButtons.forEach(btn => btn.classList.remove('is-active'));
            e.currentTarget.classList.add('is-active');
            
            currentFilter = targetFilter;
            await fetchAndRenderRooms();
        });
    });
}

/**
 * Botón Añadir Habitación
 */
function setupActionButtons() {
    if (!addRoomBtn) return;
    addRoomBtn.addEventListener('click', () => {
        console.log("[Acción] Abrir formulario para crear una nueva habitación");
        alert("Aquí abriremos el modal de creación.");
    });
}

/**
 * Inicialización
 */
function initDashboard() {
    console.log("Inicializando Panel del Supervisor...");
    fetchAndRenderRooms();
    setupNavigationTabs();
    setupStatusFilters();
    setupActionButtons();
    startPolling();
}

window.addEventListener('beforeunload', stopPolling);
document.addEventListener('DOMContentLoaded', initDashboard);
/**
 * Event Handler: Room Interactions
 * Defines what happens when users interact with room components.
 */
export const RoomEventHandlers = {
    /**
     * Handle the click event on a room card (Polymorphic callback)
     * @param {string|number} roomNumber 
     * @param {string} currentStatus 
     */
    onCardClick(roomNumber, currentStatus) {
        console.log(`[Event Dispatched] Room: ${roomNumber} | Status: ${currentStatus}`);
        // Más adelante, aquí decidiremos si abrir un modal, lanzar un fetch, etc.
    }
};
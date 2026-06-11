export const BookingServices = {

    createBooking: async (stripeToken, booking) => {
        try {
            const response = await fetch("/api/payment", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    token: stripeToken,
                    booking: booking // Aquí ya viajan las fechas, el total y los room_ids
                })
            });

            return response;

        } catch (error) {
            console.error("Error crítico en el servicio:", error);
            throw error;
        }
    },

    getRoomAvailable: async (checkIn, checkOut) => {
        try {            
            const queryParams = new URLSearchParams({ 
                checkin: checkIn, 
                checkout: checkOut 
            }).toString();

            const response = await fetch(`/api/rooms?${queryParams}`, {
                method: 'GET',
                credentials: 'include'
            });

            return response;
        } catch (error) {
            console.error("Error al procesar la estadia: ", error);
            throw error;
        }
    }
}
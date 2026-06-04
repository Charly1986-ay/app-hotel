export const CartStorageServices = {
    getRooms() {
        return JSON.parse(localStorage.getItem('rooms') || '[]');
    },

    saveRoom(id, roomType, price) {
        if (isNaN(price) || price <= 0 || isNaN(id) || id <= 0) return false;

        const rooms = this.getRooms();
        rooms.push({ roomId: id, roomType, price });

        localStorage.setItem('rooms', JSON.stringify(rooms));
        return true;
    },

    deleteRoom(index) {
        const rooms = this.getRooms();
        rooms.splice(index, 1);
        localStorage.setItem('rooms', JSON.stringify(rooms));
    },

    getTotal() {
        let total = 0;

        this.getRooms().forEach(room => {
            total += Number(room.price);
        });

        return total;
    },

    setBooking(checkin, checkout) {
        localStorage.setItem(
            'booking',
            JSON.stringify({
                checkin,
                checkout,
                total: this.getTotal()
            })
        );
    },

    getBooking() {
        return JSON.parse(localStorage.getItem('booking') || '{}');
    }
};
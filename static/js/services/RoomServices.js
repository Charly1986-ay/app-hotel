export const RoomServices = {

    listRooms: async (status = 'all') => {
        const url = `/admin/supervisor/rooms/list?q=${encodeURIComponent(status)}`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            });

            if (!response.ok) {
                return [];
            }

            const data = await response.json();

            // 💡 Extraemos la propiedad exacta que envía FastAPI
            return data.rooms_list || [];
        } catch (error) {
            return [];
        }
    }
}
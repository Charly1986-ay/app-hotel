/**
 * Filtra las habitaciones del backend según el desglose de huéspedes de los spinners.
 * @param {Array} roomsJson - El JSON todas las habitaciones.
 * @param {Array} ArrayMaxPerson - El array de spinners: [{ adult: X, children: Y }].
 * @returns {Array} - Las habitaciones que pasaron el filtro.
 */
export const RoomFilterServices = {

    filter: (roomsJson, ArrayMaxPerson) => { 

        const capacityProperty = 'capacity';

        // 1. Inyectamos de forma dinámica la propiedad 'capacity' sumando los huéspedes
        ArrayMaxPerson.forEach(bed => {
            let capacity = bed.adult + bed.children;
            bed[capacityProperty] = capacity;
            //console.log(bed);
        });

        let roomAvailable = [];

        // 2. Buscamos qué habitaciones del backend cubren las necesidades
        roomsJson.forEach(room => {
            // Evaluamos si esta habitación sirve para AL MENOS UNA de las demandas solicitadas
            // Usamos .some() para evitar duplicar la habitación si coincide con varias filas
            const satisfiesAnyDemand = ArrayMaxPerson.some(bed => room.max_capacity >= bed.capacity);

            if (satisfiesAnyDemand) {
                //console.log(room)
                roomAvailable.push(room);
            }
        });

        // 3. Regla de resguardo: Si ninguna cumplió la condición, mostramos todas
        if (roomAvailable.length === 0) {
            roomAvailable = roomsJson;
        }

        return roomAvailable;
    }
}
from datetime import date


BOOKINGS = [
    {
        'check_in': date(2026, 4, 24),
        'check_out': date(2026, 5, 3),
        'user_id': 1,
        'room_id': 1,  # 🌟 Agregado: ID de la habitación para la relación M2M
        'status': 'confirmed'
    },    
    {
        'check_in': date(2026, 4, 24),
        'check_out': date(2026, 5, 3),
        'user_id': 2,
        'room_id': 2,  # 🌟 Agregado
        'status': 'confirmed'
    },
    {
        'check_in': date(2026, 5, 3),
        'check_out': date(2026, 5, 10),
        'user_id': 3,
        'room_id': 1,  # 🌟 Agregado
        'status': 'confirmed'
    },
    {
        'check_in': date(2026, 5, 3),
        'check_out': date(2026, 5, 10),
        'user_id': 4,
        'room_id': 3,  # 🌟 Agregado
        'status': 'confirmed'
    }
]
import asyncio  # <--- Importante para ejecutar corrutinas
import typer

from app.seeds.service import run_all, run_users, run_rooms, run_booking, run_supplies

app = typer.Typer(help='Seeds: users, rooms, bookings, supplies')


@app.command("all")
def all_():
    # asyncio.run crea el bucle de eventos, ejecuta la función asíncrona y lo cierra
    asyncio.run(run_all())
    typer.secho("🌱 Todos los seeds creados exitosamente", fg=typer.colors.GREEN, bold=True)


@app.command("users")
def users():
    asyncio.run(run_users())
    typer.secho("👤 Usuarios cargados", fg=typer.colors.WHITE)


@app.command("rooms")
def rooms():
    asyncio.run(run_rooms())
    typer.secho("🏨 Habitaciones cargadas", fg=typer.colors.CYAN)


@app.command("booking")
def bookings():
    asyncio.run(run_booking())
    typer.secho("📅 Reservas cargadas", fg=typer.colors.BLUE)


@app.command("supplies")
def supplies():
    asyncio.run(run_supplies())
    typer.secho("📦 Insumos cargados", fg=typer.colors.YELLOW)  # Corregido "cargadas" -> "cargados"


if __name__ == "__main__":
    app()
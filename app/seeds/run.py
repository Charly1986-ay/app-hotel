import asyncio  # <--- Importante para ejecutar corrutinas
import typer

from app.seeds.service import run_all, run_users, run_rooms, run_booking

app = typer.Typer(help='Seeds: users, rooms, bookings')


@app.command("all")
def all_():
    # asyncio.run crea el bucle de eventos, ejecuta la función asíncrona y lo cierra
    asyncio.run(run_all())
    typer.echo("Todos los seeds creados")


@app.command("users")
def users():
    asyncio.run(run_users())
    typer.echo("Usuarios cargados")


@app.command("rooms")
def rooms():
    asyncio.run(run_rooms())
    typer.echo("Habitaciones cargadas")


@app.command("booking")
def bookings():
    asyncio.run(run_booking())
    typer.echo("Reservas cargadas")


if __name__ == "__main__":
    app()
import typer

from app.seeds.service import run_all, run_users, run_rooms

app = typer.Typer(help='Seeds: users, rooms')


@app.command("all")
def all_():
    run_all()
    typer.echo("Todos los seeds creados")


@app.command("users")
def users():
    run_users()
    typer.echo("Usuarios cargados")


@app.command("categories")
def rooms():
    run_rooms()
    typer.echo("Habitaciones cargadas")
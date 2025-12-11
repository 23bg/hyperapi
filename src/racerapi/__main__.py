import typer

from racerapi.commands.new_project import new_project
from racerapi.commands.start_dev import start_dev
from racerapi.commands.generate.resource import generate_resource
from racerapi.commands.help import help
from racerapi.commands.doctor_cmd import doctor_cmd

app = typer.Typer(help="RacerAPI CLI - FastAPI project generator")

#
# Existing Commands
#


@app.command()
def new(name: str):
    """Create a new RacerAPI project."""
    return new_project(name=name)


@app.command()
def generate(kind: str, name: str):
    """Generate new resources (modules)."""
    return generate_resource(kind=kind, name=name)


@app.command()
def dev():
    """Start development server with reload."""
    return start_dev()


#
# Newly Added Placeholder Commands
#


@app.command()
def start():
    """Start production server."""
    typer.echo("[start] Production server command not implemented yet.")
    pass


@app.command()
def build():
    """Build project (e.g., compile assets, prepare dist)."""
    typer.echo("[build] Build command not implemented yet.")
    pass


@app.command()
def doctor():
    return doctor_cmd()


@app.command()
def format():
    """Format code (black, isort, ruff)."""
    typer.echo("[format] Code formatting command not implemented yet.")
    pass


@app.command()
def lint():
    """Run linter checks."""
    typer.echo("[lint] Lint command not implemented yet.")
    pass


@app.command()
def test():
    """Run unit tests."""
    typer.echo("[test] Test command not implemented yet.")
    pass


@app.command()
def init():
    """Initialize RacerAPI into an existing folder."""
    typer.echo("[init] Init command not implemented yet.")
    pass


@app.command(
    name="--version",
)
def version():
    """Show RacerAPI version."""
    typer.echo("RacerAPI v0.0.1")
    pass


@app.command(name="help")
def help_cmd():
    return help()


def main():
    app()


if __name__ == "__main__":
    main()

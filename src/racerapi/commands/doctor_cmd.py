import typer
from pathlib import Path


def doctor_cmd():
    """
    Diagnose RacerAPI project structure and report missing folders, templates,
    modules, or configuration issues.
    """

    typer.echo("")
    typer.secho("RacerAPI System Doctor", bold=True)
    typer.echo("-----------------------------------")
    typer.echo("")

    project_root = Path(".")
    required_paths = {
        "app folder": project_root / "app",
        "modules folder": project_root / "app" / "modules",
        "main.py": project_root / "main.py",
        "templates folder": project_root / "racerapi" / "templates",
        "project template": project_root / "racerapi" / "templates" / "project",
        "resource template": project_root / "racerapi" / "templates" / "resource",
    }

    typer.secho("Project Structure:", bold=True)
    for name, path in required_paths.items():
        if path.exists():
            typer.secho(f"  ✓ {name:20} OK", fg="green")
        else:
            typer.secho(f"  ✗ {name:20} MISSING", fg="red")
    typer.echo("")

    typer.secho("Environment Checks:", bold=True)
    try:
        import uvicorn

        typer.secho("  ✓ uvicorn installed", fg="green")
    except ImportError:
        typer.secho("  ✗ uvicorn NOT installed", fg="red")

    try:
        import fastapi

        typer.secho("  ✓ fastapi installed", fg="green")
    except ImportError:
        typer.secho("  ✗ fastapi NOT installed", fg="red")

    typer.echo("")

    typer.secho("Status:", bold=True)
    typer.echo(
        "  Review missing items above. Fix required paths to ensure project works correctly."
    )
    typer.echo("")

    typer.secho("Tip:", bold=True)
    typer.echo("  Use 'racerapi new <name>' to create a fully valid project template.")
    typer.echo("")

from pathlib import Path
from racerapi.utils.copy_tree import copy_tree
import typer


BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
PROJECT_TEMPLATE_DIR = TEMPLATES_DIR / "project"
RESOURCE_TEMPLATE_DIR = TEMPLATES_DIR / "resource"


def generate_resource(kind: str, name: str):
    kind = kind.lower()
    name = name.lower()

    if kind != "resource":
        typer.echo("Only 'resource' generator is supported for now.")
        raise typer.Exit(1)

    if not RESOURCE_TEMPLATE_DIR.exists():
        typer.echo(
            f"[ERROR] Resource template directory not found: {RESOURCE_TEMPLATE_DIR}"
        )
        raise typer.Exit(1)

    module_path = Path("app/modules") / name

    if module_path.exists():
        typer.echo(f"Module '{name}' already exists.")
        raise typer.Exit(1)

    typer.echo(f"Generating resource '{name}'...")
    copy_tree(
        RESOURCE_TEMPLATE_DIR,
        module_path,
        {
            "resource_name": name,
            "class_name": name.capitalize(),
        },
    )
    typer.echo("✅ Resource generated")

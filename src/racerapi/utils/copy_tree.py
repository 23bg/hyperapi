from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
PROJECT_TEMPLATE_DIR = TEMPLATES_DIR / "project"
RESOURCE_TEMPLATE_DIR = TEMPLATES_DIR / "resource"


def copy_tree(src: Path, dest: Path, context: dict):
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        target = dest / rel

        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        content = path.read_text(encoding="utf-8")
        for key, value in context.items():
            content = content.replace(f"{{{{ {key} }}}}", value)

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

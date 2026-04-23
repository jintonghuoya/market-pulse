"""Report engine — fill templates with analysis results."""

from pathlib import Path
from datetime import date

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "reports"


def render_markdown(template_name, context, output_name=None):
    """Render a Markdown report template.

    Args:
        template_name: Template file name in templates/.
        context: Dict of values to fill into the template.
        output_name: Output file name. None = auto-generate.

    Returns:
        Path to generated report.
    """
    tpl_path = TEMPLATE_DIR / template_name
    if not tpl_path.exists():
        raise FileNotFoundError(f"Template not found: {tpl_path}")

    text = tpl_path.read_text()
    for key, value in context.items():
        text = text.replace(f"{{{{{key}}}}}", str(value))

    if output_name is None:
        output_name = f"report_{date.today().isoformat()}.md"

    out_path = OUTPUT_DIR / output_name
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text)
    return out_path

from jinja2 import Template
from src.models import JobInfo
import os

def render_markdown(job_info: JobInfo, template_str: str) -> str:
    """Renders job information into a Markdown string using a Jinja2 template."""
    template = Template(template_str)
    return template.render(job_info.model_dump())

def save_markdown(content: str, filepath: str):
    """Saves the Markdown content to a file."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

"""Report renderers for InferDoctor."""

from inferdoctor.reporters.console import render_console, render_dashboard
from inferdoctor.reporters.json_reporter import render_json
from inferdoctor.reporters.markdown import render_markdown

__all__ = ["render_console", "render_dashboard", "render_json", "render_markdown"]

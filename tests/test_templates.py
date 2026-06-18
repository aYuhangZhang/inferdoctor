import py_compile
import subprocess
import sys

from inferdoctor.core.templates import (
    compose_template_names,
    create_compose_project,
    create_template_project,
    render_compose_create_summary,
    get_template,
    render_template_detail,
    render_template_list,
    render_template_registry,
)


def test_template_catalog_contains_customer_service():
    template = get_template("customer-service")

    assert template.title == "Customer Service Chatbot"
    assert "OpenAI-compatible" in template.required_stack[0]


def test_template_renderers_are_human_readable():
    assert "InferDoctor Local AI App Templates" in render_template_list()
    assert "Restaurant Ordering Assistant" in render_template_detail("restaurant-ordering")


def test_create_customer_service_template(tmp_path):
    written = create_template_project("customer-service", str(tmp_path))

    assert str(tmp_path / "README.md") in written
    app = (tmp_path / "app.py").read_text(encoding="utf-8")
    faq = (tmp_path / "data" / "faq.md").read_text(encoding="utf-8")
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert (tmp_path / "prompts" / "system_prompt.md").exists()
    assert (tmp_path / "troubleshooting.md").exists()
    assert (tmp_path / ".env.example").exists()
    assert "read_env_file" in app
    assert "read_simple_config" in app
    assert "Billing" in faq
    assert "Warranty" in faq
    assert "Ollama OpenAI-compatible" in readme
    assert "LM Studio" in readme
    assert "vLLM" in readme
    assert "SGLang" in readme
    assert "Xinference" in readme
    assert "inferdoctor template validate ." in readme
    assert "inferdoctor template smoke-test ." in readme
    assert "Expected File Tree" in readme
    py_compile.compile(str(tmp_path / "app.py"), doraise=True)
    help_result = subprocess.run([sys.executable, str(tmp_path / "app.py"), "--help"], capture_output=True, text=True, check=True)
    assert "--check-config" in help_result.stdout
    assert "--dry-run" in help_result.stdout
    dry_run = subprocess.run([sys.executable, str(tmp_path / "app.py"), "--dry-run"], capture_output=True, text=True, check=True)
    assert "Dry run: no endpoint call was made" in dry_run.stdout
    assert "Local AI starter configured" in app
    assert "A live endpoint call happens only after you send a message" in app
    assert "KeyboardInterrupt" in app
    assert "--dry-run" in help_result.stdout
    check_result = subprocess.run([sys.executable, str(tmp_path / "app.py"), "--check-config"], capture_output=True, text=True, check=True)
    assert "No endpoint call was made" in check_result.stdout
    dry_run = subprocess.run([sys.executable, str(tmp_path / "app.py"), "--dry-run"], capture_output=True, text=True, check=True)
    assert "Dry run: no endpoint call was made" in dry_run.stdout
    assert "Context preview" in dry_run.stdout


def test_create_restaurant_template(tmp_path):
    create_template_project("restaurant-ordering", str(tmp_path))

    menu = (tmp_path / "data" / "menu.yaml").read_text(encoding="utf-8")
    policies = (tmp_path / "data" / "policies.md").read_text(encoding="utf-8")
    assert (tmp_path / "prompts" / "system_prompt.md").exists()
    assert (tmp_path / "examples" / "sample_orders.md").exists()
    assert (tmp_path / "troubleshooting.md").exists()
    assert "Classic Ramen" in menu
    assert "Miso Ramen" in menu
    assert "Gyoza" in menu
    assert "allergies" in policies
    assert "payment" in policies
    py_compile.compile(str(tmp_path / "app.py"), doraise=True)
    help_result = subprocess.run([sys.executable, str(tmp_path / "app.py"), "--help"], capture_output=True, text=True, check=True)
    assert "--check-config" in help_result.stdout


def test_create_local_doc_qa_template(tmp_path):
    create_template_project("local-doc-qa", str(tmp_path))

    assert (tmp_path / "ingest.py").exists()
    assert (tmp_path / "query.py").exists()
    assert (tmp_path / ".env.example").exists()
    assert (tmp_path / "troubleshooting.md").exists()
    assert "keyword" in (tmp_path / "config.yaml").read_text(encoding="utf-8")
    assert "Top local context matches" in (tmp_path / "query.py").read_text(encoding="utf-8")
    assert "OpenAI-compatible endpoint" in (tmp_path / "docs" / "sample.md").read_text(encoding="utf-8")
    py_compile.compile(str(tmp_path / "ingest.py"), doraise=True)
    py_compile.compile(str(tmp_path / "query.py"), doraise=True)
    ingest_help = subprocess.run([sys.executable, str(tmp_path / "ingest.py"), "--help"], capture_output=True, text=True, check=True)
    query_help = subprocess.run([sys.executable, str(tmp_path / "query.py"), "--help"], capture_output=True, text=True, check=True)
    assert "Markdown files" in ingest_help.stdout
    assert "keyword index" in query_help.stdout
    assert "--dry-run" in query_help.stdout
    assert "--check-config" in query_help.stdout
    query_config = subprocess.run([sys.executable, str(tmp_path / "query.py"), "--check-config"], capture_output=True, text=True, check=True)
    assert "No endpoint call was made" in query_config.stdout
    query_dry_run = subprocess.run([sys.executable, str(tmp_path / "query.py"), "--dry-run"], capture_output=True, text=True, check=True)
    assert "Dry run: no endpoint call was made" in query_dry_run.stdout



def test_create_compose_template_customer_service(tmp_path):
    written = create_compose_project("customer-service", str(tmp_path))

    assert str(tmp_path / "docker-compose.yml") in written
    compose = (tmp_path / "docker-compose.yml").read_text(encoding="utf-8")
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    summary = render_compose_create_summary("customer-service", str(tmp_path), written)
    assert "python:3.12-slim" in compose
    assert "host.docker.internal" in compose
    assert "did not pull images" in readme
    assert "Docker Compose Files Created" in summary


def test_create_compose_template_open_webui(tmp_path):
    create_compose_project("open-webui", str(tmp_path))

    compose = (tmp_path / "docker-compose.yml").read_text(encoding="utf-8")
    assert "open-webui" in compose
    assert "3000:8080" in compose
    assert "local-placeholder" in (tmp_path / ".env.example").read_text(encoding="utf-8")
    assert "open-webui" in compose_template_names()



def test_template_registry_renderer():
    rendered = render_template_registry()

    assert "InferDoctor Template Registry" in rendered
    assert "built-in templates" in rendered
    assert "No remote template execution" in rendered

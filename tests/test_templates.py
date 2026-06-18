from inferdoctor.core.templates import (
    create_template_project,
    get_template,
    render_template_detail,
    render_template_list,
)


def test_template_catalog_contains_customer_service():
    template = get_template("customer-service")

    assert template.title == "Customer Service Chatbot"
    assert "OpenAI-compatible" in template.required_stack[0]


def test_template_renderers_are_human_readable():
    assert "InferDoctor Local AI Templates" in render_template_list()
    assert "Restaurant Ordering Assistant" in render_template_detail("restaurant-ordering")


def test_create_customer_service_template(tmp_path):
    written = create_template_project("customer-service", str(tmp_path))

    assert str(tmp_path / "README.md") in written
    assert (tmp_path / "app.py").read_text(encoding="utf-8").startswith("from __future__")
    faq = (tmp_path / "data" / "faq.md").read_text(encoding="utf-8")
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "Standard shipping" in faq
    assert "Warranty" in faq
    assert "Troubleshooting" in readme


def test_create_restaurant_template(tmp_path):
    create_template_project("restaurant-ordering", str(tmp_path))

    menu = (tmp_path / "data" / "menu.yaml").read_text(encoding="utf-8")
    policies = (tmp_path / "data" / "policies.md").read_text(encoding="utf-8")
    assert "Classic Ramen" in menu
    assert "Miso Ramen" in menu
    assert "allergies" in policies
    assert "payment" in policies


def test_create_local_doc_qa_template(tmp_path):
    create_template_project("local-doc-qa", str(tmp_path))

    assert (tmp_path / "ingest.py").exists()
    assert (tmp_path / "query.py").exists()
    assert "keyword" in (tmp_path / "config.yaml").read_text(encoding="utf-8")
    assert "Top local context matches" in (tmp_path / "query.py").read_text(encoding="utf-8")

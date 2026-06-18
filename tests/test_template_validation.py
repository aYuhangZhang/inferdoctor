from inferdoctor.core.template_validation import (
    render_template_validation,
    validate_template_project,
)
from inferdoctor.core.templates import create_template_project


def test_validate_customer_service_template_passes(tmp_path):
    create_template_project("customer-service", str(tmp_path))

    report = validate_template_project(str(tmp_path))
    rendered = render_template_validation(report)

    assert report.status == "PASS"
    assert report.template_type == "customer-service"
    assert "InferDoctor Template Validation" in rendered
    assert "No obvious secrets" in rendered
    assert "python app.py" in rendered


def test_validate_local_doc_qa_template_passes(tmp_path):
    create_template_project("local-doc-qa", str(tmp_path))

    report = validate_template_project(str(tmp_path))

    assert report.status == "PASS"
    assert report.template_type == "local-doc-qa"
    assert "python ingest.py && python query.py" in render_template_validation(report)


def test_validate_missing_template_directory_fails(tmp_path):
    report = validate_template_project(str(tmp_path / "missing"))

    assert report.status == "FAIL"
    assert report.template_type == "missing"


def test_validate_missing_required_file_fails(tmp_path):
    create_template_project("restaurant-ordering", str(tmp_path))
    (tmp_path / "config.yaml").unlink()

    report = validate_template_project(str(tmp_path))

    assert report.status == "FAIL"
    assert any(item.name == "config.yaml" and item.status == "FAIL" for item in report.items)


def test_validate_warns_on_secret_like_values(tmp_path):
    create_template_project("customer-service", str(tmp_path))
    (tmp_path / ".env").write_text("LOCAL_AI_TOKEN=abcdefghijklmnopqrstuvwxyz\n", encoding="utf-8")

    report = validate_template_project(str(tmp_path))

    assert report.status == "WARN"
    assert any(item.name == "secret scan" and item.status == "WARN" for item in report.items)

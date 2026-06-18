from inferdoctor.core.template_validation import (
    render_template_smoke_test,
    render_template_validation,
    smoke_test_template_project,
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
    assert "Project Readiness: 100 / 100" in rendered
    assert report.readiness_score == 100
    assert "python app.py" in rendered


def test_validate_local_doc_qa_template_passes(tmp_path):
    create_template_project("local-doc-qa", str(tmp_path))

    report = validate_template_project(str(tmp_path))

    assert report.status == "PASS"
    assert report.template_type == "local-doc-qa"
    rendered = render_template_validation(report)
    assert "python query.py --dry-run" in rendered
    assert "inferdoctor template smoke-test" in rendered


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


def test_validate_missing_customer_sample_data_fails_but_keeps_type(tmp_path):
    create_template_project("customer-service", str(tmp_path))
    (tmp_path / "data" / "faq.md").unlink()

    report = validate_template_project(str(tmp_path))
    rendered = render_template_validation(report)

    assert report.template_type == "customer-service"
    assert report.status == "FAIL"
    assert "Missing data/faq.md" in rendered
    assert "python app.py --dry-run" in rendered
    assert "inferdoctor template smoke-test" in rendered


def test_validate_missing_env_example_and_endpoint_fails(tmp_path):
    create_template_project("local-doc-qa", str(tmp_path))
    (tmp_path / ".env.example").unlink()
    (tmp_path / "config.yaml").write_text("model: local-model\n", encoding="utf-8")

    report = validate_template_project(str(tmp_path))

    assert report.status == "FAIL"
    assert any(item.name == ".env.example" and item.status == "FAIL" for item in report.items)
    assert any(item.name == "endpoint config" and item.status == "FAIL" for item in report.items)


def test_validate_unknown_layout_reports_entrypoint_and_sample_data(tmp_path):
    (tmp_path / "README.md").write_text("# My App\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("", encoding="utf-8")
    (tmp_path / "config.yaml").write_text("endpoint: http://127.0.0.1:8000/v1\n", encoding="utf-8")
    (tmp_path / ".env.example").write_text("LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1\n", encoding="utf-8")

    report = validate_template_project(str(tmp_path))
    rendered = render_template_validation(report)

    assert report.template_type == "unknown"
    assert report.status == "FAIL"
    assert "No app.py, query.py, or ingest.py found" in rendered
    assert "inferdoctor template list" in rendered


def test_smoke_test_customer_service_template_passes(tmp_path):
    create_template_project("customer-service", str(tmp_path))

    report = smoke_test_template_project(str(tmp_path))
    rendered = render_template_smoke_test(report)

    assert report.status == "PASS"
    assert report.template_type == "customer-service"
    assert "InferDoctor Template Smoke Test" in rendered
    assert "Project Readiness: 100 / 100" in rendered
    assert report.readiness_score == 100
    assert "python app.py --dry-run" in rendered
    assert "do not install dependencies" in rendered


def test_smoke_test_local_doc_qa_template_passes(tmp_path):
    create_template_project("local-doc-qa", str(tmp_path))

    report = smoke_test_template_project(str(tmp_path))
    rendered = render_template_smoke_test(report)

    assert report.status == "PASS"
    assert report.template_type == "local-doc-qa"
    assert "python query.py --dry-run" in rendered
    assert "python query.py --check-config" in rendered


def test_smoke_test_missing_entrypoint_fails(tmp_path):
    create_template_project("customer-service", str(tmp_path))
    (tmp_path / "app.py").unlink()

    report = smoke_test_template_project(str(tmp_path))
    rendered = render_template_smoke_test(report)

    assert report.status == "FAIL"
    assert "Missing app.py" in rendered


def test_smoke_test_unknown_template_fails(tmp_path):
    (tmp_path / "README.md").write_text("# Unknown\n", encoding="utf-8")

    report = smoke_test_template_project(str(tmp_path))

    assert report.status == "FAIL"
    assert report.template_type == "unknown"



def test_template_readiness_score_drops_for_missing_files(tmp_path):
    create_template_project("customer-service", str(tmp_path))
    (tmp_path / "data" / "faq.md").unlink()

    report = validate_template_project(str(tmp_path))
    rendered = render_template_validation(report)

    assert report.readiness_score < 100
    assert "Project Readiness:" in rendered

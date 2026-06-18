from inferdoctor.core.stack_plan import (
    build_stack_bootstrap_plan,
    build_stack_plan,
    render_stack_bootstrap_plan,
    render_stack_plan,
)


def test_stack_plan_customer_service_with_vram():
    plan = build_stack_plan(goal="customer-service", preference="easiest", vram_gib=24)
    rendered = render_stack_plan(plan)

    assert plan.recommendation.template == "customer-service"
    assert plan.recommendation.vram_gib == 24
    assert "InferDoctor Local AI Stack Plan" in rendered
    assert "inferdoctor template validate ./customer-service-demo" in rendered
    assert "Required components:" in rendered
    assert "Use-case fit:" in rendered


def test_stack_plan_document_qa_easiest():
    plan = build_stack_plan(goal="document-qa", preference="easiest")
    rendered = render_stack_plan(plan)

    assert plan.recommendation.template == "local-doc-qa"
    assert "Local Markdown documents" in rendered
    assert "Dify for a fuller RAG app" in rendered


def test_stack_bootstrap_customer_service_dry_run():
    plan = build_stack_bootstrap_plan(goal="customer-service", preference="easiest", vram_gib=24)
    rendered = render_stack_bootstrap_plan(plan)

    assert plan.recommendation.template == "customer-service"
    assert "InferDoctor Stack Bootstrap Plan (Dry Run)" in rendered
    assert "inferdoctor template smoke-test ./customer-service-demo" in rendered
    assert "python app.py --dry-run" in rendered
    assert "InferDoctor will not do automatically" in rendered
    assert "Download models" in rendered


def test_stack_bootstrap_document_qa_dry_run():
    plan = build_stack_bootstrap_plan(goal="document-qa", preference="easiest")
    rendered = render_stack_bootstrap_plan(plan)

    assert plan.recommendation.template == "local-doc-qa"
    assert "python query.py --dry-run" in rendered
    assert "python query.py --check-config" in rendered

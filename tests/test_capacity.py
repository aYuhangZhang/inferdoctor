from inferdoctor.core.capacity import (
    CapacityHardware,
    CapacityRequest,
    estimate_capacity,
    estimate_model_memory_gib,
    infer_vram_from_gpu_name,
    parse_model_size_b,
    render_capacity,
)


def test_capacity_estimate_for_24_gib_vram_marks_7b_likely_ok():
    rows = estimate_capacity(
        CapacityHardware(
            architecture="x86_64",
            total_ram_gib=32,
            available_ram_gib=20,
            vram_gib=24,
            gpu_name="Example GPU",
        )
    )

    by_workload = {row.workload: row for row in rows}
    assert by_workload["7B/8B quantized models"].readiness == "LIKELY OK"
    assert by_workload["vLLM FP16 serving"].readiness == "LIKELY OK"
    assert by_workload["Use case: customer service"].readiness == "LIKELY OK"
    assert by_workload["Use case: GPU optimized serving"].readiness == "LIKELY OK"


def test_capacity_estimate_for_low_memory_is_conservative():
    rows = estimate_capacity(
        CapacityHardware(
            architecture="x86_64",
            total_ram_gib=8,
            available_ram_gib=4,
            vram_gib=None,
        )
    )

    by_workload = {row.workload: row for row in rows}
    assert by_workload["32B quantized models"].readiness == "UNLIKELY"
    assert by_workload["vLLM FP16 serving"].readiness == "UNLIKELY"
    assert by_workload["Use case: local API"].readiness == "NOT RECOMMENDED"


def test_render_capacity_supports_manual_vram_override():
    output = render_capacity(vram_gib=24, gpu_name="Manual GPU")

    assert "InferDoctor Capacity Preview" in output
    assert "24.0 GiB (override)" in output
    assert "Manual GPU" in output
    assert "rough heuristics, not benchmarks" in output


def test_gpu_name_can_infer_common_vram():
    assert infer_vram_from_gpu_name("RTX 3090") == 24.0
    assert infer_vram_from_gpu_name("RTX 3060 12GB") == 12.0


def test_model_size_parser_accepts_b_suffix():
    assert parse_model_size_b("14b") == 14.0
    assert parse_model_size_b("32") == 32.0


def test_requested_model_estimate_uses_quant_and_runtime():
    hardware = CapacityHardware(
        architecture="x86_64",
        total_ram_gib=64,
        available_ram_gib=48,
        vram_gib=24,
        gpu_name="RTX 3090",
    )

    rows = estimate_capacity(hardware, CapacityRequest(model_size_b=14, quant="q4", runtime="ollama"))

    assert rows[0].workload == "Requested 14B Q4 on ollama"
    assert rows[0].readiness == "LIKELY OK"
    assert estimate_model_memory_gib(14, "q8", "vllm") > estimate_model_memory_gib(14, "q4", "ollama")


def test_render_capacity_supports_gpu_profile_and_request():
    output = render_capacity(gpu_name="RTX 3090", model_size_b="14b", quant="q4", runtime="ollama")

    assert "24.0 GiB (GPU profile heuristic)" in output
    assert "Requested estimate:" in output
    assert "Requested 14B Q4 on ollam" in output

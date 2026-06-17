from inferdoctor.core.capacity import CapacityHardware, estimate_capacity, render_capacity


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


def test_render_capacity_supports_manual_vram_override():
    output = render_capacity(vram_gib=24, gpu_name="Manual GPU")

    assert "InferDoctor Capacity Preview" in output
    assert "24.0 GiB (override)" in output
    assert "Manual GPU" in output
    assert "rough heuristics, not benchmarks" in output

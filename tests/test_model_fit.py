from inferdoctor.core.model_fit import estimate_model_fit, render_model_fit


def test_model_fit_marks_14b_q4_on_24gib_likely():
    result = estimate_model_fit("14b", quant="q4", vram_gib=24)

    assert result.fit == "LIKELY FITS"
    assert result.estimated_memory_gib > 0


def test_model_fit_marks_32b_q4_on_24gib_conservative():
    result = estimate_model_fit("32b", quant="q4", runtime="vllm", vram_gib=24)

    assert result.fit in {"MAYBE", "UNLIKELY"}
    assert "InferDoctor Model Fit Advisor" in render_model_fit(result)

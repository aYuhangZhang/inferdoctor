from inferdoctor.checkers.endpoint import EndpointChecker


class VLLMChecker(EndpointChecker):
    name = "vllm"
    endpoint_name = "vllm"
    probe_path = "models"
    service_label = "vLLM-compatible"
    offline_suggestions = [
        "Start the vLLM OpenAI-compatible server or update endpoints.vllm.",
        "No action is needed if vLLM is not used on this machine.",
    ]

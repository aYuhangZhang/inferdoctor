from inferdoctor.checkers.openai_compatible import OpenAICompatibleChecker


class VLLMChecker(OpenAICompatibleChecker):
    name = "vllm"
    endpoint_name = "vllm"
    service_label = "vLLM"

from inferdoctor.checkers.openai_compatible import OpenAICompatibleChecker


class SGLangChecker(OpenAICompatibleChecker):
    name = "sglang"
    endpoint_name = "sglang"
    service_label = "SGLang"

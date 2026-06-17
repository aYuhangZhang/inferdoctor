from inferdoctor.checkers.openai_compatible import OpenAICompatibleChecker


class LMStudioChecker(OpenAICompatibleChecker):
    name = "lmstudio"
    endpoint_name = "lmstudio"
    service_label = "LM Studio"

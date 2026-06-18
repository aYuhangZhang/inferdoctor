from inferdoctor.checkers.openai_compatible import OpenAICompatibleChecker


class LlamaCppChecker(OpenAICompatibleChecker):
    name = "llamacpp"
    endpoint_name = "llamacpp"
    service_label = "llama.cpp"

from inferdoctor.checkers.endpoint import EndpointChecker


class OpenWebUIChecker(EndpointChecker):
    name = "openwebui"
    endpoint_name = "openwebui"
    probe_path = ""
    service_label = "Open WebUI"
    offline_suggestions = [
        "Open WebUI is optional. Add endpoints.openwebui to inferdoctor.yaml if you want to diagnose it.",
        "If Open WebUI is running, check its host port mapping, usually http://127.0.0.1:3000.",
    ]

from inferdoctor.checkers.endpoint import EndpointChecker


class DifyChecker(EndpointChecker):
    name = "dify"
    endpoint_name = "dify"
    probe_path = ""
    service_label = "Dify"
    offline_suggestions = [
        "Dify is optional. Add endpoints.dify to inferdoctor.yaml if you want to diagnose Dify connectivity.",
        "If Dify is running, check its service status and container port mappings.",
    ]

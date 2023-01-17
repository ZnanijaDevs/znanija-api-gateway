from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def generate_custom_openapi(app: FastAPI):
    """Generate the OpenAPI schema of the app"""
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        servers=[
            {"url": "https://tools.br-helper.com"},
            {"url": "http://localhost:8040"}
        ],
    )

    schema["tags"] = []
    schema["security"] = {"basicAuth": []}
    schema["components"].update({
        "securitySchemes": {
            "basicAuth": {
                "type": "http",
                "scheme": "basic"
            }
        }
    })

    for path, path_endpoint in schema["paths"].items():
        tag = ".".join(path.split("/")[1:3])

        schema["tags"].append({"name": tag})

        updated_endpoint = path_endpoint
        for method, route_by_method in updated_endpoint.items():
            parameters = []
            for parameter in route_by_method["parameters"]:
                if parameter["name"] != "authorization":
                    parameters.append(parameter)

            route_by_method["parameters"] = parameters
            route_by_method["tags"] = [tag]

            updated_endpoint[method] = route_by_method

        schema["paths"][path] = updated_endpoint

    return schema

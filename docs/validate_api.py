#!/usr/bin/env python3
"""Validate public API scope, examples, and blank published credentials offline."""

import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from openapi_spec_validator import validate

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "content/assets"
METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


def normalized(path):
    return re.sub(r"\{\{[^}]+\}\}|\{[^}]+\}", "{}", path)


def main():
    spec = yaml.safe_load((ASSETS / "adios-public.openapi.yaml").read_text())
    validate(spec)
    operations = {(method.upper(), normalized(path)): operation
                  for path, item in spec["paths"].items()
                  for method, operation in item.items() if method in METHODS}
    expected = set()
    for name in ["adios-api.postman_collection.json", "adios-mcp-discovery.postman_collection.json"]:
        collection = json.loads((ASSETS / name).read_text())
        groups = collection["item"]
        items = [item for group in groups for item in group["item"]] if "item" in groups[0] else groups
        for item in items:
            request = item["request"]
            path = "/" + "/".join(request["url"]["path"])
            key = (request["method"], normalized(path))
            assert key not in expected, f"Duplicate public operation: {key}"
            expected.add(key)
            operation = operations[key]
            public = request.get("auth", {}).get("type") == "noauth"
            assert bool(operation["security"]) != public, key
            tenant = [param for param in operation["parameters"] if param["in"] == "header" and param["name"] == "X-Tenant-ID"]
            assert bool(tenant) != public, key
            assert not any(param["in"] == "header" and param["name"] == "team_id" for param in operation["parameters"]), key
    assert set(operations) == expected, "Public OpenAPI and reviewed Postman scope differ"
    assert spec["servers"] == [{"url": "https://api.adios.dev", "description": "Production"}]
    assert operations[("DELETE", "/v1/workload/{}")]["responses"].keys() == {"200"}
    assert operations[("DELETE", "/v1/object_bucket/{}/object")]["responses"].keys() == {"204"}
    assert "application/octet-stream" in operations[("PUT", "/v1/object_bucket/{}/object")]["requestBody"]["content"]
    tree_path = next(param for param in operations[("GET", "/v1/workspace/{}/tree")]["parameters"] if param["name"] == "path")
    assert not tree_path["required"] and tree_path["schema"]["default"] == "."
    async_build = next(param for param in operations[("POST", "/v1/workload/{}/build")]["parameters"] if param["name"] == "async")
    assert not async_build["required"] and async_build["schema"]["type"] == "boolean"
    examples = 0
    for key, operation in operations.items():
        contents = [operation.get("requestBody", {}).get("content", {})]
        contents.extend(response.get("content", {}) for response in operation["responses"].values())
        for content in contents:
            for payload in content.values():
                if "example" not in payload or "schema" not in payload:
                    continue
                wrapper = {**spec, "$ref": "#/$defs/payload", "$defs": {"payload": payload["schema"]}}
                Draft202012Validator(wrapper).validate(payload["example"])
                examples += 1
    for path in ASSETS.glob("*.postman_environment.json"):
        for value in json.loads(path.read_text())["values"]:
            if value["key"] == "access_token" or value["key"].endswith("_id"):
                assert value["value"] == "", f"Published private value: {path.name}: {value['key']}"
    provenance = json.loads((ROOT / "api-provenance.json").read_text())
    assert provenance["publicOperations"] == len(operations)
    print(f"Validated OpenAPI 3.1, {len(operations)} reviewed operations, {examples} schema-compatible examples, and blank environment credentials.")


if __name__ == "__main__":
    main()

import json

from jsonschema import validate

def validate_schema(response_data,schema_path):
    with open(schema_path, "r", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)

    validate(
        instance=response_data,
        schema=schema
    )

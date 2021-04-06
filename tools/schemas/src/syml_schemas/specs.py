from jsonschema import RefResolver
from openapi_schema_validator import validate
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename


class Spec:

    def __init__(self, path: str):
        self.path = path
        self.body, self.url = read_from_filename(path)
        self.ref_resolver = RefResolver.from_schema(self.body)

    def validate(self):
        validate_spec(self.body, self.url)

    def validate_definition(self, definition: dict, schema_name: str):
        validate(
            definition,
            self.body['components']['schemas'][schema_name],
            resolver=self.ref_resolver,
        )

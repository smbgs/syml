import yaml

from syml_schemas.specs import Spec


class Definition:

    schema_name = None

    def __init__(self, spec: Spec, path: str):
        self.spec = spec
        self.path = path

        with open(path, 'r') as def_file:
            self.body = yaml.load(def_file, Loader=yaml.SafeLoader)

    def validate(self):
        self.spec.validate_definition(self.body, self.schema_name)


class SchemaDefinition(Definition):
    schema_name = 'Schema'

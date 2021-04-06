from unittest import TestCase

from syml_core import TOOLS_ROOT, SYML_ROOT
from syml_schemas.definitions import SchemaDefinition
from syml_schemas.specs import Spec


class TestYaml(TestCase):

    spec_path = TOOLS_ROOT / 'schemas/specs/v1.schema.openapi.yml'
    samples_path = SYML_ROOT / 'docs/samples/tpc-h/yaml/'

    # def runTest(self):
    #     validator = Validator(self.spec_path)
    #     validated = validator.validate_spec()
    #     print(validated)

    def test_spec_loading(self):
        spec = Spec(str(self.spec_path))
        self.assertEqual(spec.body.get('openapi'), '3.1.0')
        self.assertEqual(spec.url, 'file://' + str(self.spec_path))

    def test_spec_validation(self):
        spec = Spec(str(self.spec_path))
        spec.validate()

    def test_spec_definition_validation(self):
        spec = Spec(str(self.spec_path))

        for path in self.samples_path.iterdir():
            for schema_path in path.iterdir():
                print('validating', schema_path)
                schema_def = SchemaDefinition(spec, schema_path)
                schema_def.validate()


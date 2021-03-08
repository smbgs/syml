import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename
from openapi_schema_validator import validate


class Validator:

    def __init__(self, spec_path):
        self.spec_dict, self.spec_url = read_from_filename(spec_path)

    def validate_spec(self):
        return validate_spec(self.spec_dict, self.spec_url)

    def validate_definition(self, def_path):
        with open(def_path, 'r') as def_file:
            def_object = yaml.load(def_file)
            validate(def_object, self.spec_dict)


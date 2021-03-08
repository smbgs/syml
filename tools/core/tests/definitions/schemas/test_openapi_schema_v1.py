import os
from pathlib import Path
from unittest import TestCase

from syml_core.validation.openapi import Validator


class TestYaml(TestCase):

    base_dir = str(
        (
            Path(os.path.realpath(__file__)).parent
            / '..' / '..' / '..' / '..' / '..'
        ).resolve()
    )

    spec_path = 'tools/syml-core/definitions/schemas/v1.schema.openapi.yml'
    samples_path = ['docs/samples/tpc-h/yaml/*.yml']

    def runTest(self):
        validator = Validator()

        # Validating the specification itself
        validator.load_spec(self.spec_path)

        validator.validate_spec()

        # TODO: validate the samples



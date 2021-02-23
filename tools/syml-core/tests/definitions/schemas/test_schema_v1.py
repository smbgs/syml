import os
from pathlib import Path

from yamale import YamaleTestCase


class TestYaml(YamaleTestCase):

    base_dir = str(
        (
            Path(os.path.realpath(__file__)).parent
            / '..' / '..' / '..' / '..' / '..'
        ).resolve()
    )

    schema = 'tools/syml-core/definitions/schemas/v1.yamale.yml'
    yaml = ['docs/samples/tpc-h/yaml/*.yml']

    def runTest(self):
        self.assertTrue(self.validate())


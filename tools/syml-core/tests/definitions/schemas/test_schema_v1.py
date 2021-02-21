import os
from pathlib import Path

from yamale import YamaleTestCase


class TestYaml(YamaleTestCase):
    base_dir = str((Path(os.path.realpath(__file__)).parent / '..' / '..' / '..' / '..' / '..').absolute())

    schema = 'tools/syml-core/definitions/schemas/v1.yamale.yml'
    #yaml = 'docs2/samples/tpc-h/yam2l/.yml'
    yaml = ['docs/samples/tpc-h/yaml/*.yml']
    #yaml = ['data-*.yaml', 'some_data.yaml']

    def runTest(self):
        self.assertTrue(self.validate())

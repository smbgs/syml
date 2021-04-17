import ast
import unittest
from pathlib import Path

from syml_core.codegen.clients import generate_clients_module
from syml_core.meta.loader import MetaLoader


class CodegenTestCase(unittest.TestCase):

    def test_codegen_from_manifest(self):

        meta = MetaLoader.from_path(Path(__file__).parent / 'stub' / 'service.syml.meta.yml')

        module = generate_clients_module({'test-service': prov.actions for prov in meta.spec.provides})

        print(ast.unparse(module))

        self.assertIsNotNone(module)


if __name__ == '__main__':
    unittest.main()

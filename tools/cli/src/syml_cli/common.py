import typing
from pathlib import Path

SYML_ROOT_PATH = (Path(__file__).parent / '..' / '..' / '..').resolve()

SYML_CORE_PATH = SYML_ROOT_PATH / 'core'
SYML_CLI_PATH = SYML_ROOT_PATH / 'cli'


class SymlCLI:
    pass


class SymlServiceBasedCLI(SymlCLI):

    def __init__(self):
        self.clients = [v for v in self.__dict__.values()
                        if hasattr(v, 'finalize')]

    def finalize(self):
        for c in self.clients:
            c.finalize()


class SymlProfileBasedCLI:

    def __init__(self, profile_name='default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._profile = profile_name

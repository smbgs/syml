import typing
from pathlib import Path

SYML_ROOT_PATH = (Path(__file__).parent / '..' / '..' / '..').resolve()

SYML_CORE_PATH = SYML_ROOT_PATH / 'core'
SYML_CLI_PATH = SYML_ROOT_PATH / 'cli'


class SymlCLI:
    pass


class SymlServiceBasedCLI(SymlCLI):

    _to_finalize = []

    def __init__(self):
        SymlServiceBasedCLI._to_finalize.append(self)

    def _finalize(self):
        for c in self.__dict__.values():
            if hasattr(c, 'finalize'):
                c.finalize()

    @classmethod
    def _finalize_all(cls):
        for it in cls._to_finalize:
            it._finalize()


class SymlProfileBasedCLI:

    def __init__(self, profile_name='default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._profile = profile_name

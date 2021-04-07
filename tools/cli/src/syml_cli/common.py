from rich.console import Console


class SymlServiceBasedCLI:

    _to_finalize = []

    def __init__(self):
        SymlServiceBasedCLI._to_finalize.append(self)
        self.console = Console()

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

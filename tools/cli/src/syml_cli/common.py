from syml_core.rich.components import SymlConsole


class SymlServiceBasedCLI:

    def __init__(self):
        self.console = SymlConsole()


class SymlProfileBasedCLI:

    def __init__(self, profile_name='default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._profile = profile_name

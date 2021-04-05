from syml_cli.clients.db_reverser import SymlDBReverserClient
from syml_cli.clients.profiles import SymlProfileClient
from syml_cli.common import SymlServiceBasedCLI


class SymlSystemCLI(SymlServiceBasedCLI):
    """
    Manages the local SYML services so that CLI can work more quickly
    """

    def __init__(self):
        super().__init__()

    def up(self):
        """
        Starts all Syml services locally
        """
        SymlProfileClient().start_local_server()
        SymlDBReverserClient().start_local_server()

    def down(self):
        """
        Stops all Syml services locally
        """


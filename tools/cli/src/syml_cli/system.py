from syml_cli.clients import Clients
from syml_cli.common import SymlServiceBasedCLI
from syml_core.service_base.client import ServiceClient


class SymlSystemCLI(SymlServiceBasedCLI):
    """
    Manages the local SYML services so that CLI can work more quickly
    """

    def up(self):
        """
        Starts all Syml services locally
        """
        client: ServiceClient
        for client in vars(Clients).values():
            if isinstance(client, ServiceClient):
                client.start_local_server()

        self.console.input("Running... press enter to exit!")

    def down(self):
        """
        Stops all Syml services locally
        """

    def check_rust(self):
        self.console.print(Clients.rust_core.sync_command('test'))


if __name__ == '__main__':
    SymlSystemCLI().up()

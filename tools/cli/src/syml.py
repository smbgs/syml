import logging

import fire

from syml_cli.common import SymlProfileBasedCLI, SymlServiceBasedCLI

if __name__ == '__main__':

    from syml_cli.system import SymlSystemCLI
    from syml_cli.db_reverser import SymlDBReverserCLI
    from syml_cli.profiles import SymlProfilesCLI

    class SymlDBCLI(SymlProfileBasedCLI, SymlServiceBasedCLI):
        """
        Syml projects related to database interaction are grouped here
        """

        def __init__(self, profile_name):
            super().__init__(profile_name)
            self.reverse = SymlDBReverserCLI()


    class SymlCommandLineInterface(SymlServiceBasedCLI):
        """
        Syml Command Line Interfaces integrates all other Syml projects into a
        powerful system that can be used in terminal or as a part of DevOps
        process
        """

        profile: SymlProfilesCLI
        db: SymlDBCLI
        system: SymlSystemCLI

        def __init__(self, p='default', debug=False):
            super().__init__()
            if debug:
                logging.getLogger().setLevel(logging.DEBUG)
            self._profile_name = p
            self.system = SymlSystemCLI()
            self.profile = SymlProfilesCLI()
            self.db = SymlDBCLI(self._profile_name)

        def info(self):
            yield 'info'
            # TODO: implement this


    fire.Fire(SymlCommandLineInterface, name='syml')
    SymlServiceBasedCLI._finalize_all()

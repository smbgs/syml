import sys

import fire

from syml_cli.common import SYML_CORE_PATH, SymlProfileBasedCLI

if __name__ == '__main__':


    # TODO: in binary package mode this should be different
    # Adding core library to python path
    sys.path.insert(0, str(SYML_CORE_PATH / 'src'))

    from syml_cli.db_reverser import SymlDBReverserCLI
    from syml_cli.profiles import SymlProfilesCLI

    class SymlDBCLI(SymlProfileBasedCLI):
        """
        Syml projects related to database interaction are grouped here
        """

        def __init__(self, profile_name):
            super().__init__(profile_name)
            self.reverse = SymlDBReverserCLI()

        def finalize(self):
            self.reverse.finalize()

    class SymlCommandLineInterface:
        """
        Syml Command Line Interfaces integrates all other Syml projects into a
        powerful system that can be used in terminal or as a part of DevOps
        process
        """

        profile: SymlProfilesCLI
        db: SymlDBCLI

        def __init__(self, p='default'):
            self._profile_name = p
            SymlCommandLineInterface.profile = SymlProfilesCLI()
            SymlCommandLineInterface.db = SymlDBCLI(self._profile_name)

        def info(self):
            yield 'info'
            # TODO: implement this

        @classmethod
        def finalize(cls):
            cls.profile.finalize()
            cls.db.finalize()


    fire.Fire(SymlCommandLineInterface, name='syml')
    SymlCommandLineInterface.finalize()

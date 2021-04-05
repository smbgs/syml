import sys

from syml_cli.common import SYML_CORE_PATH

if __name__ == '__main__':
    # TODO: in binary package mode this should be different
    sys.path.insert(0, str(SYML_CORE_PATH / 'src'))

    from syml_cli.service.profiles import SymlProfileService

    service = SymlProfileService()
    service.unix_serve()

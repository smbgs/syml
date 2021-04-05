from pathlib import Path

import sys

if __name__ == '__main__':
    # TODO: in binary package mode this should be different

    # TODO: we need to reduce this boilerplate code
    SYML_ROOT_PATH = (Path(__file__).parent / '..' / '..').resolve()
    SYML_CORE_PATH = SYML_ROOT_PATH / 'core'
    sys.path.insert(0, str(SYML_CORE_PATH / 'src'))

    from syml_db_reverser.service.db_reverser import SymlDBReverserService

    service = SymlDBReverserService()
    service.unix_serve()

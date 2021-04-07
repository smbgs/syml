from syml_db_reverser.service.db_reverser import SymlDBReverserService

if __name__ == '__main__':
    service = SymlDBReverserService()
    service.unix_serve()

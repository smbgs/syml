if __name__ == '__main__':
    from syml_db_reverser.service.db_reverser import SymlDBReverserService

    service = SymlDBReverserService()
    service.unix_serve()

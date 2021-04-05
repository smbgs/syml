
if __name__ == '__main__':
    from syml_cli.service.profiles import SymlProfileService

    service = SymlProfileService()
    service.unix_serve()

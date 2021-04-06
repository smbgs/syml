if __name__ == '__main__':

    from syml_schemas.service.schemas import SymlSchemasService

    service = SymlSchemasService()
    service.unix_serve()

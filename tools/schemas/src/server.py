from syml_schemas.service.schemas import SymlSchemasService

if __name__ == '__main__':
    service = SymlSchemasService()
    service.unix_serve()

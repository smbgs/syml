import ast

p = ast.parse("""
from syml_core.service_base.client import ServiceClient, ClientsList


class ProfilesClient(ServiceClient):
    pass


class SchemasClient(ServiceClient):

    # TODO: response
    def get(self, path, validate):
        return self.command(name='get', args=dict(
            path=path,
            validate=validate,
        ))

    def validate(self, path):
        return self.command(name='get', args=dict(
            path=path,
        ))


class Clients(ClientsList):

    profiles = ProfilesClient('profiles')
    db_reverser = ServiceClient('db-reverser')
    schemas = SchemasClient('schemas')
    rust_codegen = ServiceClient('rust-codegen')
    go_parquet = ServiceClient('go-parquet')
""")

if __name__ == '__main__':
    print(ast.dump(p, indent=4))



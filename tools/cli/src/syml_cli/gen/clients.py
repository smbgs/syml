from syml_core.service_base.client import ServiceClient, ClientsList


class Clients(ClientsList):

    profiles = ServiceClient('profiles')
    db_reverser = ServiceClient('db-reverser')
    schemas = ServiceClient('schemas')
    rust_codegen = ServiceClient('rust-codegen')
    go_parquet = ServiceClient('go-parquet')



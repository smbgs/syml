from syml_core.service_base.client import ServiceClient


class Clients:

    profiles = ServiceClient('profiles')
    db_reverser = ServiceClient('db-reverser')
    schemas = ServiceClient('schemas')
    rust_codegen = ServiceClient('rust-codegen')
    go_core = ServiceClient('go_core', uri='~/.syml/sockets/test-go-socket.sock')

    @classmethod
    def finalize_all(cls):
        for client in vars(cls).values():
            if hasattr(client, 'finalize'):
                client.finalize()


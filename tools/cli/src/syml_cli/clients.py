from syml_core.service_base.client import ServiceClient


class Clients:

    profiles = ServiceClient('profiles')
    db_reverser = ServiceClient('db-reverser')
    schemas = ServiceClient('schemas')

    @classmethod
    def finalize_all(cls):
        for client in vars(cls).values():
            if hasattr(client, 'finalize'):
                client.finalize()


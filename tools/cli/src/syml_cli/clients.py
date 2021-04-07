from syml_core.service_base.client import ServiceClient


class Clients:

    profiles = ServiceClient('profiles')
    db_reverser = ServiceClient('db-reverser')
    schemas = ServiceClient('schemas')


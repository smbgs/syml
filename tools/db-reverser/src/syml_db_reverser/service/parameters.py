from dataclasses import dataclass


@dataclass
class ReverseUsingAlchemy:
    connection_string: str
    schemas: str
    objects_names: str
    objects_types: str

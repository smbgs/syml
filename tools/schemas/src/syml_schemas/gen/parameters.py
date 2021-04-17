from dataclasses import dataclass


@dataclass
class GetSchemaParams:
    path: str
    validate: bool = False


@dataclass
class ValidateSchemaParams:
    path: str

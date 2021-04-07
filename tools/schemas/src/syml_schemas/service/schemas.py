from jsonschema import ValidationError

from syml_core import TOOLS_ROOT
from syml_core.service_base.base import LocalServiceBase
from syml_core.service_base.protocol import SymlServiceCommand, \
    SymlServiceResponse
from .parameters import ValidateSchemaParams
from ..definitions import SchemaDefinition
from ..specs import Spec


class SymlSchemasService(LocalServiceBase):

    spec_path = TOOLS_ROOT / 'schemas/specs/v1.schema.openapi.yml'

    def __init__(self):
        super().__init__('schemas')
        self.spec = Spec(self.spec_path)

    async def cmd_validate(self, cmd: SymlServiceCommand[ValidateSchemaParams]):
        path = cmd.args.path

        definition = SchemaDefinition(self.spec, path)

        try:
            definition.validate()
        except ValidationError as e:
            return SymlServiceResponse(
                data=dict(
                    message=e.message,
                    validator=e.validator,
                    validator_value=e.validator_value,
                    absolute_path=list(e.absolute_path),
                    instance=e.instance,
                    definition=definition.body,
                ),
                errors=[
                    dict(message="validation failed {file}", file=path)
                ]
            )

        return SymlServiceResponse(
            data={'status': 'ok'},
            info=[
                dict(message="validated {file}", file=path)
            ]
        )

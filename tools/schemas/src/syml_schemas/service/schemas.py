from jsonschema import ValidationError

from syml_core import TOOLS_ROOT
from syml_core.service_base.base import LocalServiceBase
from syml_core.service_base.protocol import SymlServiceCommand, \
    SymlServiceResponse
from syml_schemas.gen.parameters import ValidateSchemaParams, GetSchemaParams
from ..definitions import SchemaDefinition
from ..specs import Spec


class SymlSchemasService(LocalServiceBase):
    spec_path = TOOLS_ROOT / 'schemas/specs/v1.schema.openapi.yml'

    def __init__(self):
        super().__init__('schemas')
        self.spec = Spec(self.spec_path)

    async def cmd_get(self, cmd: SymlServiceCommand[GetSchemaParams]):
        path = cmd.args.path
        validate = cmd.args.validate

        definition = SchemaDefinition(self.spec, path)
        return SymlServiceResponse.merge(
            definition=SymlServiceResponse(
                data=definition.body,
                info=[
                    dict(message="loaded ${file}", file=definition.path)
                ]
            ),
            validation=self.validate(definition) if validate else None,
        )

    async def cmd_validate(self, cmd: SymlServiceCommand[ValidateSchemaParams]):
        path = cmd.args.path

        definition = SchemaDefinition(self.spec, path)
        return self.validate(definition)

    @staticmethod
    def validate(definition: SchemaDefinition):
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
                ),
                errors=[
                    dict(
                        message="validation failed ${file}",
                        file=definition.path
                    )
                ]
            )

        return SymlServiceResponse(
            data={'status': 'ok'},
            info=[
                dict(message="validated ${file}", file=definition.path)
            ]
        )

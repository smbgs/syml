from syml_core.service_base.local import LocalServiceBase


class SymlDBReverserService(LocalServiceBase):

    def __init__(self):
        # TODO: this should not be a service, probably?
        super().__init__('db-reverser')

    async def cmd_alchemy(
        self,
        connection_string,
        schemas,
        objects_names,
        objects_types
    ):
        return dict(
            connection_string=connection_string,
            schemas=schemas,
            objects_names=objects_names,
            objects_types=objects_types,
        )
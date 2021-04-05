from pathlib import Path

from syml_core.service_base.local import LocalServiceBase


class SymlProfileService(LocalServiceBase):

    DEFAULT_PROFILES_STORAGE_PATH = '~/.syml/profiles/'
    DEFAULT_PROFILE_NAME = 'default'

    def __init__(self):
        super().__init__('profiles')

    async def ensure(self):
        default_path = \
            Path(self.DEFAULT_PROFILES_STORAGE_PATH) \
            / self.DEFAULT_PROFILE_NAME

        if not default_path.exists():
            await self.cmd_create(self.DEFAULT_PROFILE_NAME)

    async def cmd_list(self):
        # TODO: implement
        await self.ensure()
        return ['test1', 'test2', 'test3']

    async def cmd_create(self, profile_name: str, base=None):
        # TODO: implement
        pass

    async def cmd_delete(self, profile_name: str, confirm=False):
        raise NotImplementedError

    async def cmd_alias(self, profile_name: str, alias_name, alias_val=None):
        raise NotImplementedError

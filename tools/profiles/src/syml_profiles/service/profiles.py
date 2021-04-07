from datetime import datetime
from pathlib import Path

import yaml

from syml_core.service_base.base import LocalServiceBase
from syml_core.service_base.protocol import SymlServiceResponse, \
    SymlServiceCommand
from .parameters import CreateProfile, DeleteProfile, ProfileSetAlias


class SymlProfileService(LocalServiceBase):

    DEFAULT_PROFILES_STORAGE_PATH = Path('~/.syml/profiles/').expanduser()
    DEFAULT_PROFILE_NAME = 'default'
    DEFAULT_BASE = '@profiles/default/'

    PROFILE_FILENAME = 'profile.yaml'

    def __init__(self):
        super().__init__('profiles')

    async def cmd_list(self):
        await self.ensure()

        items = []
        for d in self.DEFAULT_PROFILES_STORAGE_PATH.iterdir():
            # TODO: more specific data
            profile_manifest = self.load_profile_manifest(d.name)
            item = dict(
                name=d.name,
                meta=dict(
                    created_at=profile_manifest.get('created_at'),
                    updated_at=profile_manifest.get('updated_at'),
                )
            )

            items.append(item)

        return SymlServiceResponse(
            data=dict(
                items=items
            )
        )

    async def cmd_create(self, cmd: SymlServiceCommand[CreateProfile]):

        base = cmd.args.base
        profile_name = cmd.args.profile_name

        use_default = base is None

        if base is None:
            base = self.DEFAULT_BASE

        base = str(base).replace(
            '@profiles', str(self.DEFAULT_PROFILES_STORAGE_PATH)
        )

        base = Path(base).expanduser().resolve()
        base_profile_manifest_path = base / self.PROFILE_FILENAME

        if base_profile_manifest_path.exists():
            with open(str(base_profile_manifest_path), 'r') as f:
                base_profile_manifest = yaml.load(f, Loader=yaml.SafeLoader)
        elif use_default:
            base_profile_manifest = dict(
                aliases={},
                areas={},
                # TODO: better defaults
            )
            self.store_profile_manifest(profile_name, base_profile_manifest)
        else:
            return SymlServiceResponse(errors=[
                dict(
                    message='unable to find base {base} for profile {profile}',
                    base=base,
                    profile=profile_name
                )
            ])

        return self.store_profile_manifest(profile_name, base_profile_manifest)

    async def cmd_delete(self, cmd: SymlServiceCommand[DeleteProfile]):
        raise NotImplementedError

    async def cmd_alias(self, cmd: SymlServiceCommand[ProfileSetAlias]):

        profile_name = cmd.args.profile_name
        alias_name = cmd.args.alias_name
        alias_val = cmd.args.alias_val

        manifest = self.load_profile_manifest(profile_name)

        if isinstance(manifest, SymlServiceResponse):
            return manifest

        aliases = manifest.get('aliases')
        if alias_val is not None:
            aliases[alias_name] = alias_val
        else:
            if alias_name in aliases:
                del aliases[alias_name]
            else:
                return SymlServiceResponse(
                    errors=[
                        dict(
                            message="unable to find the alias {alias}",
                            alias=alias_name,
                        )
                    ]
                )

        return SymlServiceResponse(
            info=[
                dict(
                    message="alias {alias} set to {value}",
                    alias=alias_name,
                    value=alias_val,
                )
                if alias_val is not None else
                dict(
                    message="alias {alias} deleted",
                    alias=alias_name,
                )
            ]
        ).combined_with(
            self.store_profile_manifest(profile_name, manifest)
        )

    async def ensure(self):
        default_path = self.resolve_profile_path(self.DEFAULT_PROFILE_NAME)
        if not default_path.exists():
            await self.cmd_create(
                SymlServiceCommand(
                    args=CreateProfile(profile_name=self.DEFAULT_PROFILE_NAME)
                )
            )

    def resolve_profile_path(self, profile_name):
        return Path(self.DEFAULT_PROFILES_STORAGE_PATH / profile_name)

    def resolve_profile_manifest_path(self, profile_name):
        return self.resolve_profile_path(profile_name) / self.PROFILE_FILENAME

    def load_profile_manifest(self, name):

        path = self.resolve_profile_manifest_path(name)

        if path.exists():
            with open(str(path), 'r') as f:
                return yaml.load(f, Loader=yaml.SafeLoader)
        else:
            return SymlServiceResponse(errors=[
                dict(
                    message='unable to find profile {profile} '
                            'in the path {path}',
                    profile=name,
                    path=str(path),
                )
            ])

    def store_profile_manifest(self, name, body):

        path = self.resolve_profile_manifest_path(name)

        is_new = 'created_at' not in body

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(path), 'w') as profile_file:
            yaml.dump({
                **body,
                'created_at': body.get('created_at', datetime.now()),
                'updated_at': datetime.now(),
            }, profile_file)

        # TODO: error handling

        return SymlServiceResponse(
            data=body,
            info=[
                dict(
                    message=
                    'profile {profile} created'
                    if is_new else
                    'profile {profile} updated',
                    profile=name,
                )
            ]
        )


if __name__ == '__main__':
    service = SymlProfileService()
    service.unix_serve()

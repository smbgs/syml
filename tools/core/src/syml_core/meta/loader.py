import typing
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class MetaSpec:
    name: str
    desc: str


@dataclass
class SpecProvidesItemSpec:
    interface: typing.Optional[str]


@dataclass
class SpecRequiresItemSpec:
    runtime: typing.Optional[str]
    service: typing.Optional[str]


@dataclass
class SpecSpec:
    provides: typing.List[SpecProvidesItemSpec]
    requires: typing.List[SpecRequiresItemSpec]


@dataclass
class Service:
    name: str


class MetaLoader:

    body: dict

    apiVersion: str

    meta: MetaSpec
    spec: SpecSpec

    services: typing.Dict[str, Service]

    def __init__(self, path: Path):
        """
        Loads the meta manifest from path
        :param path:
        """
        # TODO: make this work not only with local files, possibly urllib?
        with open(path, 'r') as def_file:
            self.body = yaml.load(def_file, Loader=yaml.SafeLoader)
            self.apiVersion = self.body.get('apiSpec')
            self.meta = MetaSpec(**self.body.get('meta'))
            self.spec = SpecSpec(**self.body.get('spec'))

            for requires in self.spec.requires:
                if requires.service:
                    self.services[requires.service] = Service(name=requires.service)
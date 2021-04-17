import copy
from typing import *
from dataclasses import dataclass
from pathlib import Path
import yaml
from marshmallow_dataclass import class_schema
from mergedeep import merge


@dataclass
class MetaSpec:
    name: str
    desc: str


@dataclass
class ActionSpec:
    name: str
    args: Dict[str, str]


@dataclass
class ActionGroupSpec:
    group: str
    actions: List[Union[
        ActionSpec,
        'ActionGroupSpec',
    ]]


@dataclass
class InterfaceSpec:
    type: str
    actions: List[Union[
        ActionSpec,
        'ActionGroupSpec',
    ]]


@dataclass
class ProvidesSpec:
    interfaces: Optional[List[InterfaceSpec]]
    features: Optional[List[str]]


@dataclass
class RequiresSpec:
    runtimes: Optional[List[str]]
    services: Optional[List[str]]
    tools: Optional[List[str]]


@dataclass
class SpecSpec:
    provides: Optional[ProvidesSpec]
    requires: Optional[RequiresSpec]
    overrides: Optional[Dict[str, dict]]


class MetaLoader:
    _body: dict

    apiVersion: str
    meta: MetaSpec
    spec: SpecSpec

    def __init__(self, body: dict):
        """
        Loads the meta manifest from path
        :param path:
        """
        self._body = body

        self.apiVersion = self._body.get('apiSpec')

        self.meta = class_schema(MetaSpec)().load(self._body.get('meta'))
        self.spec = class_schema(SpecSpec)().load(self._body.get('spec'))

    @classmethod
    def from_path(cls, path: Path):
        # TODO: make this work not only with local files, possibly urllib?
        with open(path, 'r') as def_file:
            return cls(yaml.load(def_file, Loader=yaml.SafeLoader))

    def with_override(self, override_name: str):
        body = copy.deepcopy(self._body)
        if self.spec.overrides:
            override = self.spec.overrides.get(override_name)
            # TODO: handle missing override profile
            if override:
                merge(body, override)
        return MetaLoader(body)

import json
import typing
from dataclasses import dataclass
from uuid import uuid4

Shape = typing.List[typing.Union[str, typing.List]]
T = typing.TypeVar('T')


def shape_data(data: typing.Dict, shape: Shape = None):
    if shape is None:
        shape = data.keys()

    result = {}
    for field in shape:
        if type(field) == str:
            result[field] = data.get(field)
        else:
            result[field[0]] = shape_data(data.get(field), field[1:])

    return result


class Serializable(dataclass):

    @classmethod
    def parse(cls, data: typing.Union[str, bytes]):
        return cls(**json.loads(data))

    def jsonb(self) -> bytes:
        return json.dumps(
            self.json(),
            default=lambda o: o.json() if hasattr(o, 'json') else str(o)
        ).encode()


@dataclass
class SymlServiceCommand(typing.Generic[T], Serializable):
    cid: str
    name: str
    args: T
    shape: Shape
    info: bool
    errors: bool

    def __init__(
        self,
        name: str = None,
        args: T = None,
        shape: Shape = None,
        info=True,
        errors=True,
        cid: str = None,
    ):
        self.name = name
        self.cid = cid or uuid4().hex
        self.args = args
        self.shape = shape
        self.info = info
        self.errors = errors

    def json(self):
        # TODO: we can do better
        return self.__dict__


@dataclass
class SymlServiceResponse(Serializable):
    data: typing.Dict
    errors: typing.List[typing.Dict]
    info: typing.List[typing.Dict]
    rid: str
    cid: str

    def __init__(
        self,
        data: typing.Dict = None,
        errors: typing.List[typing.Dict] = None,
        info: typing.List[typing.Dict] = None,
        rid: str = None,
        command: SymlServiceCommand = None,
    ):
        self.data = data
        self.errors = errors
        self.info = info
        self.rid = rid or uuid4().hex
        self.command = command

    def json(self):
        response = dict()
        if self.errors and self.command and self.command.errors:
            response['errors'] = self.errors

        if self.info and self.command and self.command.info:
            response['info'] = self.info

        if self.data:
            if self.command and self.command.shape:
                response['data'] = shape_data(self.data, self.command.shape)
            else:
                response['data'] = self.data

        if self.command:
            response['cid'] = self.command.cid

        if self.rid:
            response['rid'] = self.rid

        return response

    def combined_with(self, response: 'SymlServiceResponse'):
        return SymlServiceResponse(
            data=response.data,
            errors=(self.errors or []) + (response.errors or []),
            info=(self.info or []) + (response.info or [])
        )


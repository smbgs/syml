import typing
import json
from dataclasses import dataclass


@dataclass
class SymlServiceResponse:
    data: typing.Dict
    errors: typing.List[typing.Dict]
    info: typing.List[typing.Dict]

    def  __init__(
        self,
        data: typing.Dict = None,
        errors: typing.List[typing.Dict] = None,
        info: typing.List[typing.Dict] = None,
    ):
        self.data = data
        self.errors = errors
        self.info = info

    def json(self):
        response = dict()
        if self.errors:
            response['errors'] = self.errors

        if self.data:
            response['data'] = self.data

        if self.info:
            response['info'] = self.info

        return response

    def combined_with(self, response: 'SymlServiceResponse'):
        return SymlServiceResponse(
            data=response.data,
            errors=(self.errors or []) + (response.errors or []),
            info=(self.info or []) + (response.info or [])
        )

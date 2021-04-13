import typing
import ast

from syml_core.meta.loader import Service


def generate_clients_ast(services: typing.List[Service]):
    module = ast.Module()
    clients_class = ast.ClassDef()
    module.body.append(clients_class)
    ast.ImportFrom(
        module='syml_core.service_base.client',
        names=['ServiceClient']
    )

    for service in services:
        clients_class.body.append(ast.Assign(
            target=ast.Name(id=service.name, ctx=ast.Store()),
            value=ast.Call(
                func=ast.Name(id='ServiceClient', ctx=ast.Load())
            )
        ))

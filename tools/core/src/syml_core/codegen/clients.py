import typing
from ast import *

from syml_core.meta.loader import ActionSpec


def generate_clients_module(services: typing.Dict[str, typing.List[ActionSpec]]):

    client_class_names = {
        service_name: ''.join(
             it.capitalize() for it in service_name.replace('_', '-').split('-')
        ) + 'Client' for service_name in services.keys()
    }

    return Module(
        type_ignores=[],
        body=[
            ImportFrom(
                module='syml_core.service_base.client',
                names=[
                    alias(name='ServiceClient'),
                    alias(name='ClientsList')
                ],
                level=0,
            ),
            *[ClassDef(
                name=client_class_names[service_name],
                bases=[Name(id='ServiceClient', ctx=Load())],
                decorator_list=[],
                keywords=[],
                body=[
                    FunctionDef(
                        name=action_spec.name,
                        decorator_list=[],
                        lineno=None,
                        args=arguments(
                            posonlyargs=[],
                            args=[
                                arg(arg='self'),
                                *[
                                    arg(arg=argument_name)
                                    for argument_name, argument in action_spec.args.items()
                                ],
                            ],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[
                            Return(
                                value=Call(
                                    func=Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr='command',
                                        ctx=Load()
                                    ),
                                    args=[],
                                    keywords=[
                                        keyword(
                                            arg='name',
                                            value=Constant(value=action_spec.name)
                                        ),
                                        keyword(
                                            arg='args',
                                            value=Call(
                                                func=Name(id='dict', ctx=Load()),
                                                args=[],
                                                keywords=[
                                                    keyword(
                                                        arg=argument_name,
                                                        value=Name(id=argument_name, ctx=Load())
                                                    ) for argument_name, argument in action_spec.args.items()
                                                ]
                                            )
                                        )
                                    ]
                                )
                            )
                        ]
                    ) for action_spec in actions
                ],
            ) for service_name, actions in services.items()],
            ClassDef(
                name='Clients',
                bases=[Name(id='ClientsList', ctx=Load())],
                decorator_list=[],
                keywords=[],
                body=[
                    Assign(
                        targets=[Name(id=service_name.replace('-', '_'), ctx=Store())],
                        lineno=None,
                        value=Call(
                            func=Name(id=client_class_names[service_name], ctx=Load()),
                            args=[Constant(value=service_name)],
                            keywords={},
                        )
                    ) for service_name in services.keys()
                ],
            )
        ],
    )

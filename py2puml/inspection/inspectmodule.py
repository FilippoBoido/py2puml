import inspect
import types
from typing import Dict, Iterable, List, Type
from types import ModuleType

from dataclasses import is_dataclass
from enum import Enum
from inspect import getmembers, isclass

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectclass import inspect_dataclass_type, inspect_class_type
from py2puml.inspection.inspectenum import inspect_enum_type
from py2puml.inspection.inspectnamedtuple import inspect_namedtuple_type


class FoundInParentException(Exception):
    pass


def filter_domain_definitions(module: ModuleType, root_module_name: str) -> Iterable[Type]:
    for definition_key in dir(module):
        definition_type = getattr(module, definition_key)
        if isclass(definition_type):
            definition_members = getmembers(definition_type)
            definition_module_member = next((
                member for member in definition_members
                # ensures that the type belongs to the module being parsed
                if member[0] == '__module__' and member[1].startswith(root_module_name)
            ), None)
            if definition_module_member is not None:
                yield definition_type


def inspect_domain_definition(
        definition_type: Type,
        root_module_name: str,
        domain_items_by_fqn: Dict[str, UmlItem],
        domain_relations: List[UmlRelation],
        hide_inherited_methods,
        hide_private_methods,
        hide_private_attributes
):
    definition_type_fqn = f'{definition_type.__module__}.{definition_type.__name__}'
    if definition_type_fqn not in domain_items_by_fqn:
        inspection = inspect.getclasstree(inspect.getmro(definition_type))
        search_list = []

        def recursive_search(tree_list):
            for list_element in tree_list:
                if type(list_element) is type([]):
                    recursive_search(list_element)
                    continue
                search_list.append(list_element[0])

        recursive_search(inspection)

        inspection = inspect.getmembers(definition_type)

        methods = []
        for member_name, member_data in inspection:
            try:
                if type(member_data) is types.FunctionType \
                        and not member_name.startswith('__') \
                        and not member_name.endswith('__')\
                        and not (member_name.startswith('_') and hide_private_methods):
                    if hide_inherited_methods:
                        try:
                            for element in search_list[:-1:]:
                                parent_inspection = inspect.getmembers(element)
                                for parent_member_name, parent_member_data in parent_inspection:
                                    if parent_member_name == member_name:
                                        raise FoundInParentException
                        except FoundInParentException:
                            continue

                    methods.append('  ' + member_name + '()\n')
            except TypeError:
                pass
        if issubclass(definition_type, Enum):
            inspect_enum_type(definition_type, definition_type_fqn, domain_items_by_fqn)
        elif getattr(definition_type, '_fields', None) is not None:
            inspect_namedtuple_type(definition_type, definition_type_fqn, domain_items_by_fqn)
        elif is_dataclass(definition_type):
            inspect_dataclass_type(
                definition_type, definition_type_fqn,
                root_module_name, domain_items_by_fqn, domain_relations
            )
        else:
            inspect_class_type(
                definition_type, definition_type_fqn,
                root_module_name, domain_items_by_fqn, domain_relations, methods,
                hide_private_attributes
            )


def inspect_module(
        domain_item_module: ModuleType,
        root_module_name: str,
        domain_items_by_fqn: Dict[str, UmlItem],
        domain_relations: List[UmlRelation],
        hide_inherited_methods,
        hide_private_methods,
        hide_private_attributes
):
    # processes only the definitions declared or imported within the given root module
    for definition_type in filter_domain_definitions(domain_item_module, root_module_name):
        inspect_domain_definition(
            definition_type,
            root_module_name,
            domain_items_by_fqn,
            domain_relations,
            hide_inherited_methods,
            hide_private_methods,
            hide_private_attributes)

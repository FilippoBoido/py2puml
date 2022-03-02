from typing import Dict, List, Iterable
from types import ModuleType
from pkgutil import walk_packages
from importlib import import_module

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectmodule import inspect_module
from py2puml.exportpuml import to_puml_content


def py2puml(
        domain_path: str,
        domain_module: str,
        hide_inherited_methods=True,
        hide_private_methods=True,
        hide_private_attributes=True) -> Iterable[str]:

    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    for _, name, is_pkg in walk_packages([domain_path], f'{domain_module}.'):
        if not is_pkg:

            domain_item_module: ModuleType = import_module(name)
            inspect_module(
                domain_item_module,
                domain_module,
                domain_items_by_fqn,
                domain_relations,
                hide_inherited_methods,
                hide_private_methods,
                hide_private_attributes
            )
    content = to_puml_content(domain_items_by_fqn.values(), domain_relations)
    return content

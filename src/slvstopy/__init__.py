from python_solvespace import SolverSystem, Entity
from typing import List, TextIO, Dict, Tuple

from slvstopy.constants import VERSION_STRING
from slvstopy.repositories import ConstraintRepository, EntityRepository
from slvstopy.services import ConstraintService, EntityService
from slvstopy.utils import set_in_dict


def load_from_filepath(path: str) -> Tuple[SolverSystem, Dict[str, Entity]]:
    with open(path, encoding="utf8", errors="ignore") as f:
        lines = _read_lines_from_file(f)

    return load(lines)


def load(file_lines: List[str]) -> Tuple[SolverSystem, Dict[str, Entity]]:
    entity_definitions, constraint_definitions = _parse_elements(file_lines)

    sys = SolverSystem()
    entity_repository = EntityRepository(system=sys)
    entity_service = EntityService(entity_repository=entity_repository)
    entity_service.construct_entities(entity_definitions)

    constraint_repository = ConstraintRepository(system=sys)
    constraint_service = ConstraintService(
        constraint_repository=constraint_repository, entity_repository=entity_repository
    )
    constraint_service.construct_constraints(constraint_definitions)

    return sys, entity_repository.entities


def _read_lines_from_file(handle: TextIO) -> List[str]:
    return handle.read().splitlines()


def _parse_elements(file_lines: List[str]):
    sv: dict = {}
    entities = []
    constraints = []

    for line in file_lines:
        if line == "":
            continue

        if "=" in line:
            split = line.split("=")
            key = split[0]
            val = split[1]
            set_in_dict(sv, key.split("."), val)
        elif line == "AddGroup":
            continue
        elif line == "AddParam":
            continue
        elif line == "AddEntity":
            entities.append(sv.get("Entity"))
            sv = {}
            continue
        elif line == "AddRequest":
            continue
        elif line == "AddConstraint":
            constraints.append(sv.get("Constraint"))
            sv = {}
            continue
        elif line == "AddStyle":
            continue
        elif line == VERSION_STRING:
            continue
        elif any(
            line.startswith(typ)
            for typ in [
                "Triangle ",
                "Surface ",
                "SCtrl ",
                "TrimBy ",
                "Curve ",
                "CCtrl ",
                "CurvePt ",
            ]
        ) or any(line == typ for typ in ["AddSurface", "AddCurve"]):
            continue

    return entities, constraints

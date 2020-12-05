from python_solvespace import SolverSystem, Entity
from typing import List, TextIO, Dict, Tuple

from slvstopy.constants import VERSION_STRING
from slvstopy.repositories import ConstraintRepository, EntityRepository
from slvstopy.services import ConstraintService, EntityService
from slvstopy.utils import set_in_dict


class Slvstopy:
    """
    A SolverSystem can only solve once. This helper class exists solely to
    generate new systems.
    """

    def __init__(self, file_path: str = "", file_handle: TextIO = None):
        if file_path:
            with open(file_path, encoding="utf8", errors="ignore") as f:
                lines = self._read_lines_from_file(f)
        else:
            lines = self._read_lines_from_file(f)

        self.entity_definition, self.constraint_definition = self._parse_elements(lines)

    def generate_system(self) -> Tuple[SolverSystem, Dict[str, Entity]]:
        return self._generate_system(self.entity_definition, self.constraint_definition)

    def _generate_system(
        self, entity_definition: List[Dict], constraint_definition: List[Dict],
    ) -> Tuple[SolverSystem, Dict[str, Entity]]:
        sys = SolverSystem()
        entity_repository = EntityRepository(system=sys)
        entity_service = EntityService(entity_repository=entity_repository)
        constraint_repository = ConstraintRepository(system=sys)
        constraint_service = ConstraintService(
            constraint_repository=constraint_repository,
            entity_repository=entity_repository,
        )

        # Assumption: first nine entities are reference entities
        reference_entity_definition = entity_definition[0:9]
        mechanism_entity_definition = entity_definition[9:]

        entity_service.construct_entities(reference_entity_definition)
        entity_service.set_group_number(entity_service.get_group_number() + 1)
        entity_service.construct_entities(mechanism_entity_definition)

        constraint_service.construct_constraints(constraint_definition)

        return sys, entity_repository.entities

    def _read_lines_from_file(self, handle: TextIO) -> List[str]:
        return handle.read().splitlines()

    def _parse_elements(self, file_lines: List[str]) -> Tuple[List, List]:
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

from typing import Dict, Any

from python_solvespace import Entity

from slvstopy.constants import EntityType, ConstraintType
from slvstopy.repositories import EntityRepository, ConstraintRepository
from slvstopy.utils import get_in_dict


class EntityService(object):
    def __init__(
        self, entity_repository=EntityRepository(),
    ):
        self.entity_repository = entity_repository

    def construct_entities(self, entity_definition_list):
        for entity_definition in entity_definition_list:
            self.construct_entity(entity_definition, entity_definition_list)

    def construct_entity(self, entity_definition, entity_definition_list):
        entity_type = int(entity_definition["type"])
        entity_id = entity_definition["h"]["v"]

        if (
            entity_type == EntityType.POINT_IN_3D
            or entity_type == EntityType.POINT_N_COPY
        ):
            act_point = self._validate_actpoint(entity_definition)
            return self.entity_repository.get_or_create_point_in_3d(
                entity_id, act_point["x"], act_point["y"], act_point["z"],
            )
        elif entity_type == EntityType.POINT_IN_2D:
            wp = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["workplane"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )

            act_point = self._validate_actpoint(entity_definition)
            return self.entity_repository.get_or_create_point_in_2d(
                entity_id, act_point["x"], act_point["y"], wp,
            )
        elif (
            entity_type == EntityType.NORMAL_IN_3D
            or entity_type == EntityType.NORMAL_N_COPY
        ):
            act_normal = self._validate_actnormal(entity_definition)
            return self.entity_repository.get_or_create_normal_in_3d(
                entity_id,
                act_normal["vx"],
                act_normal["vy"],
                act_normal["vz"],
                act_normal["w"],
            )
        elif entity_type == EntityType.NORMAL_IN_2D:
            workplane = (
                self.construct_entity(
                    self._get_entity_definition_by_id(
                        entity_definition["workplane"]["v"], entity_definition_list
                    ),
                    entity_definition_list,
                )
                if "workplane" in entity_definition
                else None
            )
            return self.entity_repository.get_or_create_normal_in_2d(
                entity_id, workplane
            )
        elif entity_type == EntityType.DISTANCE:
            act_distance = float(entity_definition["actDistance"])
            workplane = (
                self.construct_entity(
                    self._get_entity_definition_by_id(
                        entity_definition["workplane"]["v"], entity_definition_list
                    ),
                    entity_definition_list,
                )
                if "workplane" in entity_definition
                else None
            )
            return self.entity_repository.get_or_create_distance(
                entity_id, act_distance, workplane
            )
        elif entity_type == EntityType.WORKPLANE:
            point = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["point[0]"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )
            normal = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["normal"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )
            entity = self.entity_repository.get_or_create_workplane(
                entity_id, point, normal
            )

            # TODO: Proper support for groups. Workaround for default reference group.
            group_number = self.entity_repository.get_group_number()
            self.entity_repository.set_group_number(group_number + 1)

            return entity
        elif entity_type == EntityType.LINE_SEGMENT:
            first_point = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["point[0]"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )
            second_point = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["point[1]"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )
            workplane = (
                self.construct_entity(
                    self._get_entity_definition_by_id(
                        entity_definition["workplane"]["v"], entity_definition_list
                    ),
                    entity_definition_list,
                )
                if "workplane" in entity_definition
                else None
            )
            return self.entity_repository.get_or_create_line_segment(
                entity_id, first_point, second_point, workplane
            )
        elif entity_type == EntityType.CIRCLE:
            # WARNING: only 2D circles are supported by python-solvespace
            point = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["point[0]"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )
            normal = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["normal"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )
            distance = self.construct_entity(
                self._get_entity_definition_by_id(
                    entity_definition["distance"]["v"], entity_definition_list
                ),
                entity_definition_list,
            )
            workplane = (
                self.construct_entity(
                    self._get_entity_definition_by_id(
                        entity_definition["workplane"]["v"], entity_definition_list
                    ),
                    entity_definition_list,
                )
                if "workplane" in entity_definition
                else None
            )
            return self.entity_repository.get_or_create_circle(
                entity_id, normal, point, distance, workplane
            )
        else:
            raise NotImplementedError(
                f"Entity type {EntityType(entity_type).name} is not supported"
            )

    def _get_entity_definition_by_id(self, entity_id, entity_definition_list):
        return next(
            entity for entity in entity_definition_list if entity["h"]["v"] == entity_id
        )

    def _validate_actpoint(self, entity_definition: Dict[str, Any]) -> Dict[str, float]:
        act_point = get_in_dict(entity_definition, "actPoint")
        act_point = act_point if act_point is not None else {}

        x = act_point.get("x", "0")
        y = act_point.get("y", "0")
        z = act_point.get("z", "0")

        return {"x": float(x), "y": float(y), "z": float(z)}

    def _validate_actnormal(
        self, entity_definition: Dict[str, Any]
    ) -> Dict[str, float]:
        act_normal = get_in_dict(entity_definition, "actNormal")
        act_normal = act_normal if act_normal is not None else {}

        vx = act_normal.get("vx", "0")
        vy = act_normal.get("vy", "0")
        vz = act_normal.get("vz", "0")
        w = act_normal.get("w", "0")

        return {"vx": float(vx), "vy": float(vy), "vz": float(vz), "w": float(w)}


class ConstraintService(object):
    def __init__(
        self,
        constraint_repository=ConstraintRepository(),
        entity_repository=EntityRepository(),
    ):
        self.constraint_repository = constraint_repository
        self.entity_repository = entity_repository

    def construct_constraints(self, constraint_definition_list):
        for constraint_definition in constraint_definition_list:
            self.construct_constraint(constraint_definition)

    def construct_constraint(self, constraint_definition):
        constraint_type = ConstraintType(int(constraint_definition["type"]))

        # TODO: Most of the constraint definitions are the same. Get rid of the
        # repetitive boilerplate.
        if constraint_type == ConstraintType.POINTS_COINCIDENT:
            point_a = self.entity_repository.get(constraint_definition["ptA"]["v"])
            point_b = self.entity_repository.get(constraint_definition["ptB"]["v"])
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_points_coincident(
                point_a, point_b, workplane
            )
        elif constraint_type == ConstraintType.PT_PT_DISTANCE:
            point_a = self.entity_repository.get(constraint_definition["ptA"]["v"])
            point_b = self.entity_repository.get(constraint_definition["ptB"]["v"])
            value = (
                float(constraint_definition["valA"])
                if constraint_definition.get("valA")
                else 0.0
            )
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_pt_pt_distance(
                point_a, point_b, value, workplane
            )
        elif (
            constraint_type == ConstraintType.PT_PLANE_DISTANCE
            or constraint_type == ConstraintType.PT_LINE_DISTANCE
        ):
            point_a = self.entity_repository.get(constraint_definition["ptA"]["v"])
            plane = self.entity_repository.get(constraint_definition["entityA"]["v"])
            value = (
                float(constraint_definition["valA"])
                if constraint_definition.get("valA")
                else 0.0
            )
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_pt_plane_distance(
                point_a, plane, value, workplane
            )
        elif constraint_type == ConstraintType.PT_LINE_DISTANCE:
            point_a = self.entity_repository.get(constraint_definition["ptA"]["v"])
            plane = self.entity_repository.get(constraint_definition["entityA"]["v"])
            value = (
                float(constraint_definition["valA"])
                if constraint_definition.get("valA")
                else 0.0
            )
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_pt_line_distance(
                point_a, plane, value, workplane
            )
        elif constraint_type == ConstraintType.PT_ON_LINE:
            point_a = self.entity_repository.get(constraint_definition["ptA"]["v"])
            line = self.entity_repository.get(constraint_definition["entityA"]["v"])
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_pt_on_line(point_a, line, workplane)
        elif constraint_type == ConstraintType.EQUAL_LENGTH_LINES:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            entity_b = self.entity_repository.get(constraint_definition["entityB"]["v"])
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_equal_length_lines(
                entity_a, entity_b, workplane
            )
        elif constraint_type == ConstraintType.AT_MIDPOINT:
            point_a = self.entity_repository.get(constraint_definition["ptA"]["v"])
            line = self.entity_repository.get(constraint_definition["entityA"]["v"])
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_at_midpoint(point_a, line, workplane)
        elif constraint_type == ConstraintType.HORIZONTAL:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            workplane = self.entity_repository.get(
                constraint_definition["workplane"]["v"]
            )
            self.constraint_repository.add_horizontal(entity_a, workplane)
        elif constraint_type == ConstraintType.VERTICAL:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            workplane = self.entity_repository.get(
                constraint_definition["workplane"]["v"]
            )
            self.constraint_repository.add_vertical(entity_a, workplane)
        elif constraint_type == ConstraintType.DIAMETER:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            value = (
                float(constraint_definition["valA"])
                if constraint_definition.get("valA")
                else 0.0
            )
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_diameter(entity_a, value, workplane)
        elif constraint_type == ConstraintType.ANGLE:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            entity_b = self.entity_repository.get(constraint_definition["entityB"]["v"])
            value = (
                float(constraint_definition["valA"])
                if constraint_definition.get("valA")
                else 0.0
            )
            inverse = bool(int(constraint_definition["other"]))
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_angle(
                entity_a, entity_b, value, workplane, inverse
            )
        elif constraint_type == ConstraintType.PARALLEL:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            entity_b = self.entity_repository.get(constraint_definition["entityB"]["v"])
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_parallel(entity_a, entity_b, workplane)
        elif constraint_type == ConstraintType.PERPENDICULAR:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            entity_b = self.entity_repository.get(constraint_definition["entityB"]["v"])
            inverse = bool(int(constraint_definition["other"]))
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_perpendicular(
                entity_a, entity_b, workplane, inverse
            )
        elif constraint_type == ConstraintType.EQUAL_RADIUS:
            entity_a = self.entity_repository.get(constraint_definition["entityA"]["v"])
            entity_b = self.entity_repository.get(constraint_definition["entityB"]["v"])
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_equal_radius(entity_a, entity_b, workplane)
        elif constraint_type == ConstraintType.WHERE_DRAGGED:
            point_a = self.entity_repository.get(constraint_definition["ptA"]["v"])
            workplane = (
                self.entity_repository.get(constraint_definition["workplane"]["v"])
                if constraint_definition.get("workplane", {}).get("v")
                else Entity.FREE_IN_3D
            )
            self.constraint_repository.add_where_dragged(point_a, workplane)
        else:
            constraint_name = ConstraintType(constraint_type).name
            raise NotImplementedError(
                f"Constraint type {constraint_name} is not supported"
            )

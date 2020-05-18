from typing import Optional, Dict, Any

from python_solvespace import SolverSystem, Constraint, Entity


class EntityNotFoundException(Exception):
    pass


class EntityRepository(object):
    def __init__(self, system: SolverSystem = SolverSystem()):
        self.system: SolverSystem = system
        self.entities: Dict[str, Any] = {}
        self._group_number = 0

    def get(self, entity_id: str) -> Entity:
        try:
            entity = self.entities[entity_id]
        except KeyError:
            raise EntityNotFoundException
        return entity

    def add(self, entity_id: str, entity: Entity) -> None:
        self.entities[entity_id] = entity

    def get_or_create_point_in_3d(
        self, entity_id: str, x: float, y: float, z: float
    ) -> Entity:
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_point_in_3d(entity_id, x, y, z)
        return entity

    def create_point_in_3d(
        self, entity_id: str, x: float, y: float, z: float
    ) -> Entity:
        entity = self.system.add_point_3d(x, y, z)
        self.add(entity_id, entity)
        return entity

    def get_or_create_point_in_2d(
        self, entity_id: str, u: float, v: float, wp: Entity
    ) -> Entity:
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_point_in_2d(entity_id, u, v, wp)
        return entity

    def create_point_in_2d(
        self, entity_id: str, u: float, v: float, wp: Entity
    ) -> Entity:
        entity = self.system.add_point_2d(u, v, wp)
        self.add(entity_id, entity)
        return entity

    def get_or_create_normal_in_3d(
        self, entity_id: str, qw: float, qx: float, qy: float, qz: float
    ) -> Entity:
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_normal_in_3d(entity_id, qw, qx, qy, qz)
        return entity

    def create_normal_in_3d(
        self, entity_id: str, qw: float, qx: float, qy: float, qz: float
    ) -> Entity:
        entity = self.system.add_normal_3d(qw, qx, qy, qz)
        self.add(entity_id, entity)
        return entity

    def get_or_create_normal_in_2d(self, entity_id: str, wp: Entity) -> Entity:
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_normal_in_2d(entity_id, wp)
        return entity

    def create_normal_in_2d(self, entity_id: str, wp: Entity) -> Entity:
        entity = self.system.add_normal_2d(wp)
        self.add(entity_id, entity)
        return entity

    def get_or_create_distance(self, entity_id: str, d: float, wp: Entity) -> Entity:
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_distance(entity_id, d, wp)
        return entity

    def create_distance(
        self, entity_id: str, d: float, wp: Entity = Entity.FREE_IN_3D
    ) -> Entity:
        entity = self.system.add_distance(d, wp)
        self.add(entity_id, entity)
        return entity

    def get_or_create_workplane(
        self, entity_id: str, origin: Entity, nm: Entity
    ) -> Entity:
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_workplane(entity_id, origin, nm)
        return entity

    def create_workplane(self, entity_id: str, origin: Entity, nm: Entity) -> Entity:
        entity = self.system.add_work_plane(origin, nm)
        self.add(entity_id, entity)
        self._group_number += 1
        self.system.set_group(self._group_number)
        return entity

    def get_or_create_line_segment(
        self, entity_id: str, p1: Entity, p2: Entity, wp: Optional[Entity] = None
    ) -> Entity:
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_line_segment(entity_id, p1, p2, wp)
        return entity

    def create_line_segment(
        self, entity_id: str, p1: Entity, p2: Entity, wp: Optional[Entity] = None
    ) -> Entity:
        entity = (
            self.system.add_line_2d(p1, p2, wp)
            if wp
            else self.system.add_line_3d(p1, p2)
        )
        self.add(entity_id, entity)
        return entity

    def get_or_create_cubic(
        self, entity_id: str, p1: Entity, p2: Entity, p3: Entity, p4: Entity, wp: Entity
    ):
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_cubic(entity_id, p1, p2, p3, p4, wp)
        return entity

    def create_cubic(
        self, entity_id: str, p1: Entity, p2: Entity, p3: Entity, p4: Entity, wp: Entity
    ):
        entity = self.system.add_cubic(p1, p2, p3, p4, wp)
        self.add(entity_id, entity)
        return entity

    def get_or_create_circle(
        self, entity_id: str, nm: Entity, ct: Entity, radius: Entity, wp: Entity
    ):
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_circle(entity_id, nm, ct, radius, wp)
        return entity

    def create_circle(
        self, entity_id: str, nm: Entity, ct: Entity, radius: Entity, wp: Entity,
    ):
        entity = self.system.add_circle(nm, ct, radius, wp)
        self.add(entity_id, entity)
        return entity

    def get_or_create_arc_of_circle(
        self,
        entity_id: str,
        nm: Entity,
        ct: Entity,
        start: Entity,
        end: Entity,
        wp: Entity,
    ):
        try:
            entity = self.get(entity_id)
        except EntityNotFoundException:
            entity = self.create_arc_of_circle(entity_id, nm, ct, start, end, wp)
        return entity

    def create_arc_of_circle(
        self,
        entity_id: str,
        nm: Entity,
        ct: Entity,
        start: Entity,
        end: Entity,
        wp: Entity,
    ):
        entity = self.system.add_arc(nm, ct, start, end, wp)
        self.add(entity_id, entity)
        return entity


class ConstraintRepository(object):
    def __init__(self, system: SolverSystem = SolverSystem()):
        self.system: SolverSystem = system

    def add_points_coincident(
        self, point_a: Entity, point_b: Entity, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        self.system.coincident(point_a, point_b, wp)

    def add_pt_pt_distance(
        self, e1: Entity, e2: Entity, value: float, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        self.system.distance(e1, e2, value, wp)

    def add_pt_plane_distance(
        self,
        point: Entity,
        workplane: Entity,
        value: float,
        wp: Entity = Entity.FREE_IN_3D,
    ) -> None:
        if wp == Entity.FREE_IN_3D:
            self.system.distance(point, workplane, value, wp)
        else:
            # python-solvespace does not support constraining a 2d point to
            # another workplane. Solvespace UI allows this type of contraint.
            raise NotImplementedError(
                "Constraint type PT_PLANE_DISTANCE must be on a workplane of \
                type Entity.FREE_IN_3D"
            )

    def add_pt_line_distance(
        self, e1: Entity, e2: Entity, value: float, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        self.system.distance(e1, e2, value, wp)

    def add_pt_face_distance(self):
        raise NotImplementedError

    def add_proj_pt_distance(self, e1: Entity, e2: Entity, value: float) -> None:
        raise NotImplementedError

    def add_pt_in_plane(self):
        raise NotImplementedError

    def add_pt_on_line(
        self, point: Entity, line: Entity, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        self.system.coincident(point, line, wp)

    def add_pt_on_face(self):
        raise NotImplementedError

    def add_equal_length_lines(
        self, e1: Entity, e2: Entity, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        self.system.equal(e1, e2, wp)

    def add_length_ratio(self):
        raise NotImplementedError

    def add_eq_len_pt_line_d(self):
        raise NotImplementedError

    def add_eq_pt_line_d(self):
        raise NotImplementedError

    def add_equal_angle(self):
        raise NotImplementedError

    def add_equal_line_arc_len(
        self, e1: Entity, e2: Entity, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        raise NotImplementedError

    def add_length_difference(self):
        raise NotImplementedError

    def add_symmetric(self):
        raise NotImplementedError

    def add_symmetric_horiz(self):
        raise NotImplementedError

    def add_symmetric_vert(self):
        raise NotImplementedError

    def add_symmetric_line(self):
        raise NotImplementedError

    def add_at_midpoint(
        self, point: Entity, line: Entity, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        self.system.midpoint(point, line, wp)

    def add_horizontal(self, line: Entity, wp: Entity) -> None:
        self.system.horizontal(line, wp)

    def add_vertical(self, e1: Entity, wp: Entity) -> None:
        self.system.vertical(e1, wp)

    def add_diameter(self, e1: Entity, value: float, wp: Entity) -> None:
        self.system.diameter(e1, value, wp)

    def add_pt_on_circle(self):
        raise NotImplementedError

    def add_same_orientation(self):
        raise NotImplementedError

    def add_angle(
        self, e1: Entity, e2: Entity, value: float, wp: Entity, inverse: bool = False
    ) -> None:
        if wp == Entity.FREE_IN_3D:
            raise NotImplementedError("Workplane cannot be Entity.FREE_IN_3D")
        self.system.angle(e1, e2, value, wp, inverse)

    def add_parallel(
        self, e1: Entity, e2: Entity, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        if wp == Entity.FREE_IN_3D:
            # This causes Python to crash. Avoid.
            raise NotImplementedError("Workplane cannot be Entity.FREE_IN_3D")
        self.system.parallel(e1, e2, wp)

    def add_perpendicular(
        self,
        e1: Entity,
        e2: Entity,
        wp: Entity = Entity.FREE_IN_3D,
        inverse: bool = False,
    ) -> None:
        # Bypass validation introduced by SovlerSystem.perpendicular as the
        # constraint in 3D works fine in the SolveSpace API.
        self.system.add_constraint(
            Constraint.PERPENDICULAR,
            wp,
            0.0,
            Entity.NONE,
            Entity.NONE,
            e1,
            e2,
            Entity.NONE,
            Entity.NONE,
            inverse,
        )

    def add_arc_line_tangent(self):
        raise NotImplementedError

    def add_cubic_line_tangent(self):
        raise NotImplementedError

    def add_curve_curve_tangent(self):
        raise NotImplementedError

    def add_equal_radius(
        self, e1: Entity, e2: Entity, wp: Entity = Entity.FREE_IN_3D
    ) -> None:
        self.system.equal(e1, e2, wp)

    def add_where_dragged(self, e1: Entity, wp: Entity = Entity.FREE_IN_3D) -> None:
        self.system.dragged(e1, wp)

    def add_comment(self):
        raise NotImplementedError

import pytest
import math

from pymatrix import dot, cross, matrix as pymatrix
from python_solvespace import SolverSystem, ResultFlag, quaternion_n
from slvstopy.repositories import ConstraintRepository, EntityRepository
from slvstopy.services import ConstraintService

from utils import matrix, compute_distance


class TestConstraintService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.system = SolverSystem()
        self.constraint_repository = ConstraintRepository(system=self.system)
        self.entity_repository = EntityRepository(system=self.system)
        self.constraint_service = ConstraintService(
            constraint_repository=self.constraint_repository,
            entity_repository=self.entity_repository,
        )

    def test_points_coincident_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 0.0, 0.0, 0.0, 1.0
        )
        workplane = self.entity_repository.create_workplane("00000000", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "00000001", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "00000002", 1.0, 1.0, workplane
        )

        constraint_definition = {
            "type": "20",
            "ptA": {"v": "00000001"},
            "ptB": {"v": "00000002"},
            "workplane": {"v": "00000000"},
        }

        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        assert result == ResultFlag.OKAY
        assert self.system.params(point_a.params) == self.system.params(point_b.params)

    def test_points_coincident_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("00000001", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("00000002", 1.0, 1.0, 1.0)

        constraint_definition = {
            "type": "20",
            "ptA": {"v": "00000001"},
            "ptB": {"v": "00000002"},
        }

        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        assert result == ResultFlag.OKAY
        assert self.system.params(point_a.params) == self.system.params(point_b.params)

    def test_pt_pt_distance_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 0.0, 0.0, 0.0, 1.0
        )
        workplane = self.entity_repository.create_workplane("00000000", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "00000001", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "00000002", 1.0, 1.0, workplane
        )

        constraint_definition = {
            "type": "30",
            "ptA": {"v": "00000001"},
            "ptB": {"v": "00000002"},
            "valA": "1",
            "workplane": {"v": "00000000"},
        }

        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        coordinates_a = self.system.params(point_a.params)
        coordinates_b = self.system.params(point_b.params)

        vector = matrix(coordinates_b) - matrix(coordinates_a)
        distance = compute_distance(vector)

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1.0)

    def test_pt_pt_distance_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("00000001", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("00000002", 1.0, 1.0, 1.0)

        constraint_definition = {
            "type": "30",
            "ptA": {"v": "00000001"},
            "ptB": {"v": "00000002"},
            "valA": "1",
        }

        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        coordinates_a = self.system.params(point_a.params)
        coordinates_b = self.system.params(point_b.params)

        vector = matrix(coordinates_b) - matrix(coordinates_a)
        distance = compute_distance(vector)

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1.0)

    def test_pt_plane_distance_in_3d(self):
        origin = self.entity_repository.create_point_in_3d("00000000", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "00000001", 1.0, 0.0, 0.0, 0.0
        )
        self.entity_repository.create_workplane("00000002", origin, normal)
        point = self.entity_repository.create_point_in_3d("00000003", 1.0, 1.0, 1.0)

        constraint_definition = {
            "type": "31",
            "ptA": {"v": "00000003"},
            "entityA": {"v": "00000002"},
            "valA": "1",
        }

        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        normal_quaternion = self.system.params(normal.params)
        normal_coordinates = quaternion_n(*normal_quaternion)
        origin_coordinates = self.system.params(origin.params)
        point_coordinates = self.system.params(point.params)

        dist_vector = matrix(point_coordinates) - matrix(origin_coordinates)
        norm_vector = matrix(normal_coordinates)

        distance = dot(dist_vector, norm_vector)

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1.0)

    def test_pt_line_distance_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 100.0, 100.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", -100.0, -100.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )
        point = self.entity_repository.create_point_in_2d("99999996", -1, 1, workplane)

        constraint_definition = {
            "type": "32",
            "ptA": {"v": "99999996"},
            "entityA": {"v": "99999995"},
            "valA": "1",
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        direction_vector = (point_b - point_a).dir()
        point_vector = point - point_a
        distance = pymatrix([point_vector[0], direction_vector[0]]).det()

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1)

    def test_pt_line_distance_in_3d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        self.entity_repository.create_workplane("99999992", origin, normal)
        point = self.entity_repository.create_point_in_3d("99999993", 1.0, 1.0, 1.0)

        constraint_definition = {
            "type": "32",
            "ptA": {"v": "99999993"},
            "entityA": {"v": "99999992"},
            "valA": "1",
        }
        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        normal_quaternion = self.system.params(normal.params)
        normal_coordinates = quaternion_n(*normal_quaternion)
        origin_coordinates = self.system.params(origin.params)
        point_coordinates = self.system.params(point.params)

        dist_vector = matrix(point_coordinates) - matrix(origin_coordinates)
        norm_vector = matrix(normal_coordinates)

        distance = dot(dist_vector, norm_vector)

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1.0)

    def test_pt_on_line_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 1.0, 1.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )
        point = self.entity_repository.create_point_in_2d(
            "99999996", -1.0, -2.0, workplane
        )

        constraint_definition = {
            "type": "42",
            "ptA": {"v": "99999996"},
            "entityA": {"v": "99999995"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        direction_vector = (point_b - point_a).dir()
        point_vector = point - point_a
        distance = pymatrix([point_vector[0], direction_vector[0]]).det()

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(0)

    def test_pt_on_line_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d(
            "99999991", 10.0, 10.0, 10.0
        )
        self.entity_repository.create_line_segment("99999992", point_a, point_b)
        point = self.entity_repository.create_point_in_3d("99999993", -1.0, -2.0, -3.0)

        constraint_definition = {
            "type": "42",
            "ptA": {"v": "99999993"},
            "entityA": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        direction_vector = (point_b - point_a).dir()
        point_vector = point - point_a
        distance = compute_distance(
            cross(point_vector.trans(), direction_vector.trans())
        )

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(0)

    def test_equal_length_lines_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        center = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_a = self.entity_repository.create_point_in_2d(
            "99999994", 2.0, 2.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999995", 3.0, 3.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999996", center, point_a, workplane
        )
        self.entity_repository.create_line_segment(
            "99999997", center, point_b, workplane
        )

        constraint_definition = {
            "type": "50",
            "entityA": {"v": "99999996"},
            "entityB": {"v": "99999997"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(origin)
        result = self.system.solve()

        center = matrix(self.system.params(center.params))
        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        vector_a = point_a - center
        vector_b = point_b - center
        distance_a = compute_distance(vector_a)
        distance_b = compute_distance(vector_b)

        assert result == ResultFlag.OKAY
        assert distance_a == pytest.approx(distance_b)

    def test_equal_length_lines_in_3d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_a = self.entity_repository.create_point_in_3d("99999991", 2.0, 2.0, 2.0)
        point_b = self.entity_repository.create_point_in_3d("99999992", 3.0, 3.0, 3.0)
        self.entity_repository.create_line_segment("99999993", origin, point_a)
        self.entity_repository.create_line_segment("99999994", origin, point_b)

        constraint_definition = {
            "type": "50",
            "entityA": {"v": "99999993"},
            "entityB": {"v": "99999994"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(origin)
        result = self.system.solve()

        origin = matrix(self.system.params(origin.params))
        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        vector_a = point_a - origin
        vector_b = point_b - origin
        distance_a = compute_distance(vector_a)
        distance_b = compute_distance(vector_b)

        assert result == ResultFlag.OKAY
        assert distance_a == pytest.approx(distance_b)

    def test_at_midpoint_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", -1.0, -1.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 1.0, 1.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )
        point = self.entity_repository.create_point_in_2d(
            "99999996", 5.0, 5.0, workplane
        )

        constraint_definition = {
            "type": "70",
            "ptA": {"v": "99999996"},
            "entityA": {"v": "99999995"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        distance_a = compute_distance(point - point_a)
        distance_b = compute_distance(point - point_b)

        assert result == ResultFlag.OKAY
        assert distance_a == pytest.approx(distance_b)

    def test_at_midpoint_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d(
            "99999990", -1.0, -1.0, -1.0
        )
        point_b = self.entity_repository.create_point_in_3d("99999991", 1.0, 1.0, 1.0)
        self.entity_repository.create_line_segment("99999992", point_a, point_b)
        point = self.entity_repository.create_point_in_3d("99999993", 5.0, 5.0, 5.0)

        constraint_definition = {
            "type": "70",
            "ptA": {"v": "99999993"},
            "entityA": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        distance_a = compute_distance(point - point_a)
        distance_b = compute_distance(point - point_b)

        assert result == ResultFlag.OKAY
        assert distance_a == pytest.approx(distance_b)

    def test_horizontal(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 1.0, 1.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )

        constraint_definition = {
            "type": "80",
            "entityA": {"v": "99999995"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a, workplane)
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] != pytest.approx(0)
        assert point_b[1] == pytest.approx(0)

    def test_vertical(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 1.0, 1.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )

        constraint_definition = {
            "type": "81",
            "entityA": {"v": "99999995"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a, workplane)
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] == pytest.approx(0)
        assert point_b[1] != pytest.approx(0)

    def test_diameter(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        centre = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        radius = self.entity_repository.create_distance("99999994", 100, workplane)
        self.entity_repository.create_circle(
            "99999995", normal, centre, radius, workplane
        )

        constraint_definition = {
            "type": "90",
            "entityA": {"v": "99999995"},
            "valA": "50",
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        radius = self.system.params(radius.params)

        assert result == ResultFlag.OKAY
        assert radius[0] == pytest.approx(25)

    def test_angle(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 1.0, 0.0, workplane
        )
        point_c = self.entity_repository.create_point_in_2d(
            "99999995", 1.0, 2.0, workplane
        )
        line_b = self.entity_repository.create_line_segment(
            "99999996", point_a, point_b, workplane
        )
        self.entity_repository.create_line_segment(
            "99999997", point_a, point_c, workplane
        )

        constraint_definition = {
            "type": "120",
            "entityA": {"v": "99999996"},
            "entityB": {"v": "99999997"},
            "valA": "45",
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a, workplane)
        self.constraint_repository.add_horizontal(line_b, workplane)
        self.constraint_repository.add_pt_pt_distance(point_a, point_c, 1, workplane)

        result = self.system.solve()
        point_c = self.system.params(point_c.params)

        assert result == ResultFlag.OKAY
        assert point_c[0] == pytest.approx(1.0 / math.sqrt(2))
        assert point_c[1] == pytest.approx(1.0 / math.sqrt(2))

    def test_parallel_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 5.0, 0.0, workplane
        )
        point_c = self.entity_repository.create_point_in_2d(
            "99999995", 0.0, 5.0, workplane
        )
        point_d = self.entity_repository.create_point_in_2d(
            "99999996", 5.0, 10.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999997", point_a, point_b, workplane
        )
        self.entity_repository.create_line_segment(
            "99999998", point_c, point_d, workplane
        )

        constraint_definition = {
            "type": "121",
            "entityA": {"v": "99999997"},
            "entityB": {"v": "99999998"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point_c = matrix(self.system.params(point_c.params))
        point_d = matrix(self.system.params(point_d.params))

        vector_ab = (point_b - point_a).dir()
        vector_cd = (point_d - point_c).dir()

        assert result == ResultFlag.OKAY
        assert vector_ab[0][0] == pytest.approx(vector_cd[0][0])
        assert vector_ab[0][1] == pytest.approx(vector_cd[0][1])

    def test_perpendicular_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 5.0, 0.0, workplane
        )
        point_c = self.entity_repository.create_point_in_2d(
            "99999995", 0.0, 5.0, workplane
        )
        point_d = self.entity_repository.create_point_in_2d(
            "99999996", 5.0, 10.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999997", point_a, point_b, workplane
        )
        self.entity_repository.create_line_segment(
            "99999998", point_c, point_d, workplane
        )

        constraint_definition = {
            "type": "122",
            "entityA": {"v": "99999997"},
            "entityB": {"v": "99999998"},
            "workplane": {"v": "99999992"},
            "other": "0",
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point_c = matrix(self.system.params(point_c.params))
        point_d = matrix(self.system.params(point_d.params))

        vector_ab = (point_b - point_a).dir()
        vector_cd = (point_d - point_c).dir()
        dot_product = dot(vector_ab, vector_cd)

        assert result == ResultFlag.OKAY
        assert compute_distance(vector_ab) > 0
        assert compute_distance(vector_cd) > 0
        assert dot_product == pytest.approx(0)

    def test_perpendicular_in_2d_inverse(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 5.0, 0.0, workplane
        )
        point_c = self.entity_repository.create_point_in_2d(
            "99999995", 0.0, 5.0, workplane
        )
        point_d = self.entity_repository.create_point_in_2d(
            "99999996", 5.0, 10.0, workplane
        )
        self.entity_repository.create_line_segment(
            "99999997", point_a, point_b, workplane
        )
        self.entity_repository.create_line_segment(
            "99999998", point_c, point_d, workplane
        )

        constraint_definition = {
            "type": "122",
            "entityA": {"v": "99999997"},
            "entityB": {"v": "99999998"},
            "workplane": {"v": "99999992"},
            "other": "1",
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point_c = matrix(self.system.params(point_c.params))
        point_d = matrix(self.system.params(point_d.params))

        vector_ab = (point_b - point_a).dir()
        vector_cd = (point_d - point_c).dir()
        dot_product = dot(vector_ab, vector_cd)

        assert result == ResultFlag.OKAY
        assert compute_distance(vector_ab) > 0
        assert compute_distance(vector_cd) > 0
        assert dot_product == pytest.approx(0)

    def test_perpendicular_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 5.0, 0.0, 1.0)
        point_c = self.entity_repository.create_point_in_3d("99999992", 0.0, 5.0, 0.0)
        point_d = self.entity_repository.create_point_in_3d("99999993", 0.0, 0.0, -2.0)
        self.entity_repository.create_line_segment("99999994", point_a, point_b)
        self.entity_repository.create_line_segment("99999995", point_c, point_d)

        constraint_definition = {
            "type": "122",
            "entityA": {"v": "99999994"},
            "entityB": {"v": "99999995"},
            "other": "0",
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point_c = matrix(self.system.params(point_c.params))
        point_d = matrix(self.system.params(point_d.params))

        vector_ab = point_b - point_a
        vector_cd = point_d - point_c
        dot_product = dot(vector_ab, vector_cd)

        assert result == ResultFlag.OKAY
        assert compute_distance(vector_ab) > 0
        assert compute_distance(vector_cd) > 0
        assert dot_product == pytest.approx(0)

    def test_perpendicular_in_3d_inverse(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 5.0, 0.0, 1.0)
        point_c = self.entity_repository.create_point_in_3d("99999992", 0.0, 5.0, 0.0)
        point_d = self.entity_repository.create_point_in_3d("99999993", 0.0, 0.0, -2.0)
        self.entity_repository.create_line_segment("99999994", point_a, point_b)
        self.entity_repository.create_line_segment("99999995", point_c, point_d)

        constraint_definition = {
            "type": "122",
            "entityA": {"v": "99999994"},
            "entityB": {"v": "99999995"},
            "other": "1",
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point_c = matrix(self.system.params(point_c.params))
        point_d = matrix(self.system.params(point_d.params))

        vector_ab = point_b - point_a
        vector_cd = point_d - point_c
        dot_product = dot(vector_ab, vector_cd)

        assert result == ResultFlag.OKAY
        assert compute_distance(vector_ab) > 0
        assert compute_distance(vector_cd) > 0
        assert dot_product == pytest.approx(0)

    def test_equal_radius_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 0.0, 0.0, 0.0, 1.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        centre = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        radius_a = self.entity_repository.create_distance("99999994", 75, workplane)
        self.entity_repository.create_circle(
            "99999995", normal, centre, radius_a, workplane
        )
        radius_b = self.entity_repository.create_distance("99999996", 25, workplane)
        self.entity_repository.create_circle(
            "99999997", normal, centre, radius_b, workplane
        )

        constraint_definition = {
            "type": "130",
            "entityA": {"v": "99999995"},
            "entityB": {"v": "99999997"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        result = self.system.solve()

        radius_a = self.system.params(radius_a.params)
        radius_b = self.system.params(radius_b.params)

        assert result == ResultFlag.OKAY
        assert radius_a == radius_b

    def test_where_dragged_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999994", 1.0, 1.0, workplane
        )

        constraint_definition = {
            "type": "200",
            "ptA": {"v": "99999994"},
            "workplane": {"v": "99999992"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a, workplane)
        self.system.set_params(point_b.params, (1.0, 0.0))
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] == pytest.approx(1)
        assert point_b[1] == pytest.approx(0)

    def test_where_dragged_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 1.0, 1.0, 1.0)

        constraint_definition = {
            "type": "200",
            "ptA": {"v": "99999991"},
        }
        self.constraint_service.construct_constraint(constraint_definition)
        self.constraint_repository.add_where_dragged(point_a)
        self.system.set_params(point_b.params, (2.0, 2.0, 2.0))
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] == pytest.approx(2)
        assert point_b[1] == pytest.approx(2)
        assert point_b[2] == pytest.approx(2)

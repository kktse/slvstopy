import math
import pytest

from pymatrix import dot, cross, matrix as pymatrix
from python_solvespace import SolverSystem, ResultFlag, quaternion_n
from slvstopy.repositories import ConstraintRepository, EntityRepository

from utils import matrix, compute_distance


class TestConstraintRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.system = SolverSystem()
        self.constraint_repository = ConstraintRepository(system=self.system)
        self.entity_repository = EntityRepository(system=self.system)

    def test_add_points_coincident_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 0.0, 0.0, 0.0, 1.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999993", 1.0, 1.0, workplane
        )

        self.constraint_repository.add_points_coincident(point_a, point_b, workplane)
        result = self.system.solve()

        assert result == ResultFlag.OKAY
        assert self.system.params(point_a.params) == self.system.params(point_b.params)

    def test_add_points_coincident_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 1.0, 1.0, 1.0)

        self.constraint_repository.add_points_coincident(point_a, point_b)
        result = self.system.solve()

        assert result == ResultFlag.OKAY
        assert self.system.params(point_a.params) == self.system.params(point_b.params)

    def test_add_pt_pt_distance_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 0.0, 0.0, 0.0, 1.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point_a = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        point_b = self.entity_repository.create_point_in_2d(
            "99999993", 1.0, 1.0, workplane
        )

        self.constraint_repository.add_pt_pt_distance(point_a, point_b, 1.0, workplane)
        result = self.system.solve()

        coordinates_a = self.system.params(point_a.params)
        coordinates_b = self.system.params(point_b.params)

        vector = matrix(coordinates_b) - matrix(coordinates_a)
        distance = compute_distance(vector)

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1.0)

    def test_add_pt_pt_distance_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 1.0, 1.0, 1.0)

        self.constraint_repository.add_pt_pt_distance(point_a, point_b, 1.0)
        result = self.system.solve()

        coordinates_a = self.system.params(point_a.params)
        coordinates_b = self.system.params(point_b.params)

        vector = matrix(coordinates_b) - matrix(coordinates_a)
        distance = compute_distance(vector)

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1.0)

    def test_add_pt_plane_distance_in_3d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        point = self.entity_repository.create_point_in_3d("99999993", 1.0, 1.0, 1.0)

        self.constraint_repository.add_pt_plane_distance(point, workplane, 1.0)
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

    def test_add_pt_line_distance_in_2d(self):
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
        line = self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )
        point = self.entity_repository.create_point_in_2d("99999996", -1, 1, workplane)

        self.constraint_repository.add_pt_line_distance(point, line, 1)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        direction_vector = (point_b - point_a).dir()
        point_vector = point - point_a
        distance = pymatrix([point_vector[0], direction_vector[0]]).det()

        assert result == ResultFlag.OKAY
        assert distance == pytest.approx(1)

    def test_add_pt_line_distance_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 10.0, 10.0)
        point_b = self.entity_repository.create_point_in_3d(
            "99999991", 0.0, -10.0, -10.0
        )
        line = self.entity_repository.create_line_segment("99999992", point_a, point_b)
        point = self.entity_repository.create_point_in_3d("99999993", 5.0, 0.0, 0.0)

        self.constraint_repository.add_pt_line_distance(point, line, 1.0)
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
        line = self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )
        point = self.entity_repository.create_point_in_2d(
            "99999996", -1.0, -2.0, workplane
        )

        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_pt_on_line(point, line, workplane)
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
        line = self.entity_repository.create_line_segment("99999992", point_a, point_b)
        point = self.entity_repository.create_point_in_3d("99999993", -1.0, -2.0, -3.0)

        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        self.constraint_repository.add_pt_on_line(point, line)
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

    def test_add_equal_length_lines_in_2d(self):
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
        line_a = self.entity_repository.create_line_segment(
            "99999996", center, point_a, workplane
        )
        line_b = self.entity_repository.create_line_segment(
            "99999997", center, point_b, workplane
        )

        self.constraint_repository.add_where_dragged(origin)
        self.constraint_repository.add_equal_length_lines(line_a, line_b)
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

    def test_add_equal_length_lines_in_3d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_a = self.entity_repository.create_point_in_3d("99999991", 2.0, 2.0, 2.0)
        point_b = self.entity_repository.create_point_in_3d("99999992", 3.0, 3.0, 3.0)
        line_a = self.entity_repository.create_line_segment("99999993", origin, point_a)
        line_b = self.entity_repository.create_line_segment("99999994", origin, point_b)

        self.constraint_repository.add_where_dragged(origin)
        self.constraint_repository.add_equal_length_lines(line_a, line_b)
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

    def test_add_at_midpoint_in_2d(self):
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
        line = self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )
        point = self.entity_repository.create_point_in_2d(
            "99999996", 5.0, 5.0, workplane
        )

        self.constraint_repository.add_at_midpoint(point, line, workplane)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        distance_a = compute_distance(point - point_a)
        distance_b = compute_distance(point - point_b)

        assert result == ResultFlag.OKAY
        assert distance_a == pytest.approx(distance_b)

    def test_add_at_midpoint_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d(
            "99999990", -1.0, -1.0, -1.0
        )
        point_b = self.entity_repository.create_point_in_3d("99999991", 1.0, 1.0, 1.0)
        line = self.entity_repository.create_line_segment("99999992", point_a, point_b)
        point = self.entity_repository.create_point_in_3d("99999993", 5.0, 5.0, 5.0)

        self.constraint_repository.add_at_midpoint(point, line)
        result = self.system.solve()

        point_a = matrix(self.system.params(point_a.params))
        point_b = matrix(self.system.params(point_b.params))
        point = matrix(self.system.params(point.params))

        distance_a = compute_distance(point - point_a)
        distance_b = compute_distance(point - point_b)

        assert result == ResultFlag.OKAY
        assert distance_a == pytest.approx(distance_b)

    def test_add_horizontal(self):
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
        line = self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )

        self.constraint_repository.add_where_dragged(point_a, workplane)
        self.constraint_repository.add_horizontal(line, workplane)
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] != pytest.approx(0)
        assert point_b[1] == pytest.approx(0)

    def test_add_vertical(self):
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
        line = self.entity_repository.create_line_segment(
            "99999995", point_a, point_b, workplane
        )

        self.constraint_repository.add_where_dragged(point_a, workplane)
        self.constraint_repository.add_vertical(line, workplane)
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] == pytest.approx(0)
        assert point_b[1] != pytest.approx(0)

    def test_add_diameter(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 1.0, 0.0, 0.0, 0.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        centre = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        radius = self.entity_repository.create_distance("99999994", 100, workplane)
        circle = self.entity_repository.create_circle(
            "99999995", normal, centre, radius, workplane
        )

        self.constraint_repository.add_diameter(circle, 50, workplane)
        result = self.system.solve()

        radius = self.system.params(radius.params)

        assert result == ResultFlag.OKAY
        assert radius[0] == pytest.approx(25)

    def test_add_angle(self):
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
        line_c = self.entity_repository.create_line_segment(
            "99999997", point_a, point_c, workplane
        )

        self.constraint_repository.add_where_dragged(point_a, workplane)
        self.constraint_repository.add_horizontal(line_b, workplane)
        self.constraint_repository.add_pt_pt_distance(point_a, point_c, 1, workplane)
        self.constraint_repository.add_angle(line_b, line_c, 45, workplane)

        result = self.system.solve()
        point_c = self.system.params(point_c.params)

        assert result == ResultFlag.OKAY
        assert point_c[0] == pytest.approx(1.0 / math.sqrt(2))
        assert point_c[1] == pytest.approx(1.0 / math.sqrt(2))

    def test_add_angle__inverse(self):
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
        line_c = self.entity_repository.create_line_segment(
            "99999997", point_a, point_c, workplane
        )

        self.constraint_repository.add_where_dragged(point_a, workplane)
        self.constraint_repository.add_horizontal(line_b, workplane)
        self.constraint_repository.add_pt_pt_distance(point_a, point_c, 1, workplane)
        self.constraint_repository.add_angle(
            line_b, line_c, 45, workplane, inverse=True
        )
        result = self.system.solve()

        point_c = self.system.params(point_c.params)

        assert result == ResultFlag.OKAY
        assert point_c[0] == pytest.approx(-1.0 / math.sqrt(2))
        assert point_c[1] == pytest.approx(1.0 / math.sqrt(2))

    def test_add_parallel_in_2d(self):
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
        line_a = self.entity_repository.create_line_segment(
            "99999997", point_a, point_b, workplane
        )
        line_b = self.entity_repository.create_line_segment(
            "99999998", point_c, point_d, workplane
        )
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        self.constraint_repository.add_parallel(line_a, line_b, workplane)
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

    def test_add_perpendicular_in_2d(self):
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
        line_a = self.entity_repository.create_line_segment(
            "99999997", point_a, point_b, workplane
        )
        line_b = self.entity_repository.create_line_segment(
            "99999998", point_c, point_d, workplane
        )
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        self.constraint_repository.add_perpendicular(line_a, line_b, workplane)
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

    def test_add_perpendicular_in_2d_inverse(self):
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
        line_a = self.entity_repository.create_line_segment(
            "99999997", point_a, point_b, workplane
        )
        line_b = self.entity_repository.create_line_segment(
            "99999998", point_c, point_d, workplane
        )
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        self.constraint_repository.add_perpendicular(
            line_a, line_b, workplane, inverse=True
        )
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

    def test_add_perpendicular_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 5.0, 0.0, 1.0)
        point_c = self.entity_repository.create_point_in_3d("99999992", 0.0, 5.0, 0.0)
        point_d = self.entity_repository.create_point_in_3d("99999993", 0.0, 0.0, -2.0)
        line_a = self.entity_repository.create_line_segment(
            "99999994", point_a, point_b
        )
        line_b = self.entity_repository.create_line_segment(
            "99999995", point_c, point_d
        )
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        self.constraint_repository.add_perpendicular(line_a, line_b)
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

    def test_add_perpendicular_in_3d_inverse(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 5.0, 0.0, 1.0)
        point_c = self.entity_repository.create_point_in_3d("99999992", 0.0, 5.0, 0.0)
        point_d = self.entity_repository.create_point_in_3d("99999993", 0.0, 0.0, -2.0)
        line_a = self.entity_repository.create_line_segment(
            "99999994", point_a, point_b
        )
        line_b = self.entity_repository.create_line_segment(
            "99999994", point_c, point_d
        )
        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        self.constraint_repository.add_perpendicular(line_a, line_b, inverse=True)
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

    def test_add_equal_radius_in_2d(self):
        origin = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.entity_repository.create_normal_in_3d(
            "99999991", 0.0, 0.0, 0.0, 1.0
        )
        workplane = self.entity_repository.create_workplane("99999992", origin, normal)
        centre = self.entity_repository.create_point_in_2d(
            "99999993", 0.0, 0.0, workplane
        )
        radius_a = self.entity_repository.create_distance("99999994", 75, workplane)
        circle_a = self.entity_repository.create_circle(
            "99999995", normal, centre, radius_a, workplane
        )
        radius_b = self.entity_repository.create_distance("99999996", 25, workplane)
        circle_b = self.entity_repository.create_circle(
            "99999997", normal, centre, radius_b, workplane
        )

        self.constraint_repository.add_equal_radius(circle_a, circle_b, workplane)
        result = self.system.solve()

        radius_a = self.system.params(radius_a.params)
        radius_b = self.system.params(radius_b.params)

        assert result == ResultFlag.OKAY
        assert radius_a == radius_b

    def test_add_where_dragged_in_2d(self):
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

        self.constraint_repository.add_where_dragged(point_a, workplane)
        self.constraint_repository.add_where_dragged(point_b, workplane)
        self.system.set_params(point_b.params, (1.0, 0.0))
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] == pytest.approx(1)
        assert point_b[1] == pytest.approx(0)

    def test_add_where_dragged_in_3d(self):
        point_a = self.entity_repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        point_b = self.entity_repository.create_point_in_3d("99999991", 1.0, 1.0, 1.0)

        self.constraint_repository.add_where_dragged(point_a)
        self.constraint_repository.add_where_dragged(point_b)
        self.system.set_params(point_b.params, (2.0, 2.0, 2.0))
        result = self.system.solve()

        point_b = self.system.params(point_b.params)

        assert result == ResultFlag.OKAY
        assert point_b[0] == pytest.approx(2)
        assert point_b[1] == pytest.approx(2)
        assert point_b[2] == pytest.approx(2)

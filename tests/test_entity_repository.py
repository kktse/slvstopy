import pytest

from python_solvespace import SolverSystem
from slvstopy.repositories import EntityRepository


class TestEntityRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.system = SolverSystem()
        self.repository = EntityRepository(system=self.system)
        self.entity_id = "00000001"

    def test_create_point_in_3d(self):
        coordinates = (1.0, 1.0, 1.0)
        entity = self.repository.create_point_in_3d(self.entity_id, *coordinates)
        assert self.system.params(entity.params) == coordinates
        assert self.repository.get(self.entity_id) == entity

    def test_create_point_in_2d(self):
        coordinates = (1.0, 2.0)

        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", 0.0, 0.0, 0.0, 1.0)
        workplane = self.repository.create_workplane("99999992", origin, normal)
        entity = self.repository.create_point_in_2d(
            self.entity_id, *coordinates, workplane
        )
        assert self.system.params(entity.params) == coordinates
        assert self.repository.get(self.entity_id) == entity

    def test_create_normal_in_3d(self):
        quaternion = (0.5, 0.5, 0.5, 0.5)
        entity = self.repository.create_normal_in_3d(self.entity_id, *quaternion)
        assert self.system.params(entity.params) == quaternion
        assert self.repository.get(self.entity_id) == entity

    def test_create_normal_in_2d(self):
        quaternion = (0.5, 0.5, 0.5, 0.5)

        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", *quaternion)
        workplane = self.repository.create_workplane("99999991", origin, normal)
        entity = self.repository.create_normal_in_2d(self.entity_id, workplane)
        assert entity.is_normal_2d()
        assert self.repository.get(self.entity_id) == entity

    def test_create_distance(self):
        distance = (1.0,)

        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", 0.0, 0.0, 0.0, 1.0)
        workplane = self.repository.create_workplane("99999992", origin, normal)
        entity = self.repository.create_distance(self.entity_id, *distance, workplane)
        assert self.system.params(entity.params) == distance
        assert self.repository.get(self.entity_id) == entity

    def test_create_workplane(self):
        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", 0.0, 0.0, 0.0, 1.0)
        entity = self.repository.create_workplane(self.entity_id, origin, normal)
        assert entity.is_work_plane()
        assert self.repository.get(self.entity_id) == entity

    def test_create_3d_line_segment(self):
        first_coordinate = (-1.0, -1.0, -1.0)
        second_coordinate = (1.0, 1.0, 1.0)

        first_point = self.repository.create_point_in_3d("99999990", *first_coordinate)
        second_point = self.repository.create_point_in_3d(
            "99999991", *second_coordinate
        )
        entity = self.repository.create_line_segment(
            self.entity_id, first_point, second_point,
        )
        assert entity.is_line()
        assert entity.is_line_3d()
        assert self.repository.get(self.entity_id) == entity

    def test_create_2d_line_segment(self):
        first_coordinate = (-1.0, -1.0)
        second_coordinate = (1.0, 1.0)

        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", 0.0, 0.0, 0.0, 1.0)
        workplane = self.repository.create_workplane("99999992", origin, normal)

        first_point = self.repository.create_point_in_2d(
            "99999993", *first_coordinate, workplane
        )
        second_point = self.repository.create_point_in_2d(
            "99999994", *second_coordinate, workplane
        )
        entity = self.repository.create_line_segment(
            self.entity_id, first_point, second_point, workplane
        )
        assert entity.is_line()
        assert entity.is_line_2d()
        assert self.repository.get(self.entity_id) == entity

    def test_create_cubic(self):
        first_coordinate = (0.0, 0.0)
        second_coordinate = (1.0, 1.0)
        third_coordinate = (2.0, 1.0)
        fourth_coordinate = (3.0, 0.0)

        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", 0.0, 0.0, 0.0, 1.0)
        workplane = self.repository.create_workplane("99999992", origin, normal)

        first_point = self.repository.create_point_in_2d(
            "99999993", *first_coordinate, workplane
        )
        second_point = self.repository.create_point_in_2d(
            "99999994", *second_coordinate, workplane
        )
        third_point = self.repository.create_point_in_2d(
            "99999995", *third_coordinate, workplane
        )
        fourth_point = self.repository.create_point_in_2d(
            "99999996", *fourth_coordinate, workplane
        )

        entity = self.repository.create_cubic(
            self.entity_id,
            first_point,
            second_point,
            third_point,
            fourth_point,
            workplane,
        )

        assert entity.is_cubic()
        assert self.repository.get(self.entity_id) == entity

    def test_create_circle(self):
        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", 0.0, 0.0, 0.0, 1.0)
        workplane = self.repository.create_workplane("99999992", origin, normal)
        centre = self.repository.create_point_in_2d("99999993", 0.0, 0.0, workplane)
        radius = self.repository.create_distance("99999994", 100, workplane)
        entity = self.repository.create_circle(
            self.entity_id, normal, centre, radius, workplane
        )
        assert entity.is_circle()
        assert self.repository.get(self.entity_id) == entity

    def test_create_arc_of_circle(self):
        origin = self.repository.create_point_in_3d("99999990", 0.0, 0.0, 0.0)
        normal = self.repository.create_normal_in_3d("99999991", 0.0, 0.0, 0.0, 1.0)
        workplane = self.repository.create_workplane("99999992", origin, normal)
        centre = self.repository.create_point_in_2d("99999993", 0.0, 0.0, workplane)
        start = self.repository.create_point_in_2d("99999994", 1.0, 0.0, workplane)
        end = self.repository.create_point_in_2d("99999995", 0.0, 1.0, workplane)
        entity = self.repository.create_arc_of_circle(
            self.entity_id, normal, centre, start, end, workplane
        )
        assert entity.is_arc()
        assert self.repository.get(self.entity_id) == entity

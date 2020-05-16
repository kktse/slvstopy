import pytest
from unittest.mock import Mock

from python_solvespace import SolverSystem
from slvstopy.repositories import EntityRepository
from slvstopy.services import EntityService

from factories import (
    workplane_definition_factory,
    point_in_3d_definition_factory,
    point_in_2d_definition_factory,
)


class TestEntityRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.system = SolverSystem()
        self.repository = Mock(wraps=EntityRepository(system=self.system))
        self.service = EntityService(entity_repository=self.repository)
        self.entity_id = "00000001"

    def test_create_point_in_3d__success(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "2000",
            "actPoint": {"x": "1.0", "y": "1.0", "z": "1.0"},
        }
        entity_list = [entity_definition]

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (1.0, 1.0, 1.0)

    def test_create_point_in_3d__partial_point_defaults_to_zero(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "2000",
            "actPoint": {"x": "1.0"},
        }
        entity_list = [entity_definition]

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (1.0, 0.0, 0.0)

    def test_create_point_in_3d__undefined_point_defaults_to_zero(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "2000",
        }
        entity_list = [entity_definition]

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (0.0, 0.0, 0.0)

    def test_create_point_in_2d__success(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "2001",
            "workplane": {"v": "99999990"},
            "actPoint": {"x": "1.0", "y": "1.0"},
        }
        entity_list = [entity_definition] + workplane_definition_factory()

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (1.0, 1.0)

    def test_create_point_in_2d__undefined_point_defaults_to_zero(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "2001",
            "workplane": {"v": "99999990"},
        }
        entity_list = [entity_definition] + workplane_definition_factory()

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (0.0, 0.0)

    def test_create_normal_in_3d__success(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "3000",
            "point[0]": {"v": "99999990"},
            "actNormal": {"w": "0.5", "vx": "0.5", "vy": "0.5", "vz": "0.5"},
        }
        entity_list = [entity_definition] + point_in_3d_definition_factory()

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (0.5, 0.5, 0.5, 0.5)

    def test_create_normal_in_3d__partial_normal_defaults_to_zero(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "3000",
            "point[0]": {"v": "99999990"},
            "actNormal": {"vx": "1.0"},
        }
        entity_list = [entity_definition] + point_in_3d_definition_factory()

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (1.0, 0.0, 0.0, 0.0)

    def test_create_normal_in_3d__undefined_normal_defaults_to_zero(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "3000",
            "point[0]": {"v": "99999990"},
        }
        entity_list = [entity_definition] + point_in_3d_definition_factory()

        entity = self.service.construct_entity(entity_definition, entity_list)

        assert entity == self.repository.get(self.entity_id)
        assert self.system.params(entity.params) == (0.0, 0.0, 0.0, 0.0)

    def test_create_workplane__success(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "10000",
            "point[0]": {"v": "99999991"},
            "normal": {"v": "99999992"},
        }
        point_definition = {"h": {"v": "99999991"}, "type": "2000"}
        normal_definition = {
            "h": {"v": "99999992"},
            "type": "3000",
            "point[0]": {"v": "99999991"},
            "actNormal": {"w": "1.0"},
        }

        entity_list = [entity_definition, point_definition, normal_definition]

        entity = self.service.construct_entity(entity_definition, entity_list)
        point = self.repository.get("99999991")
        normal = self.repository.get("99999992")

        assert entity == self.repository.get(self.entity_id)
        self.repository.get_or_create_workplane.assert_called_with(
            self.entity_id, point, normal
        )

    def test_create_line_segment__in_3d__success(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "11000",
            "point[0]": {"v": "99999991"},
            "point[1]": {"v": "99999992"},
        }
        points_definition = point_in_3d_definition_factory(
            hv="99999991"
        ) + point_in_3d_definition_factory(hv="99999992", x="1.0", y="1.0", z="1.0")

        entity_list = [entity_definition] + points_definition

        entity = self.service.construct_entity(entity_definition, entity_list)
        first_point = self.repository.get("99999991")
        second_point = self.repository.get("99999992")

        assert entity == self.repository.get(self.entity_id)
        self.repository.get_or_create_line_segment.assert_called_with(
            self.entity_id, first_point, second_point, None
        )

    def test_create_line_segment__in_2d__success(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "11000",
            "point[0]": {"v": "99999999"},
            "point[1]": {"v": "99999998"},
            "workplane": {"v": "99999990"},
        }
        workplane_definition = workplane_definition_factory()
        points_definition = point_in_2d_definition_factory(
            hv="99999999", workplane="99999990"
        ) + point_in_2d_definition_factory(
            hv="99999998", x="1.0", y="1.0", workplane="99999990"
        )

        entity_list = [entity_definition] + workplane_definition + points_definition

        entity = self.service.construct_entity(entity_definition, entity_list)
        workplane = self.repository.get("99999990")
        first_point = self.repository.get("99999999")
        second_point = self.repository.get("99999998")

        assert entity == self.repository.get(self.entity_id)
        self.repository.get_or_create_line_segment.assert_called_with(
            self.entity_id, first_point, second_point, workplane
        )

    def test_create_circle__in_2d__success(self):
        entity_definition = {
            "h": {"v": self.entity_id},
            "type": "13000",
            "point[0]": {"v": "99999997"},
            "normal": {"v": "99999992"},
            "distance": {"v": "99999998"},
            "workplane": {"v": "99999990"},
        }
        workplane_definition = workplane_definition_factory()
        point_definition = {
            "h": {"v": "99999997"},
            "type": "2001",
            "workplane": {"v": "99999990"},
            "actPoint": {"x": "1.0", "y": "1.0"},
        }
        distance_definition = {
            "h": {"v": "99999998"},
            "type": "4000",
            "workplane": {"v": "99999990"},
            "actDistance": "10.0",
        }
        entity_list = [
            entity_definition,
            distance_definition,
            point_definition,
        ] + workplane_definition

        entity = self.service.construct_entity(entity_definition, entity_list)
        workplane = self.repository.get("99999990")
        point = self.repository.get("99999997")
        normal = self.repository.get("99999992")
        distance = self.repository.get("99999998")

        assert entity == self.repository.get(self.entity_id)
        self.repository.get_or_create_circle.assert_called_with(
            self.entity_id, normal, point, distance, workplane
        )

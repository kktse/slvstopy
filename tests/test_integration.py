import pytest

from python_solvespace import ResultFlag
from slvstopy import Slvstopy


class TestCrankRocker:
    def test_load_success(self):
        system_factory = Slvstopy(file_path="tests/files/crank_rocker.slvs")
        system, entities = system_factory.generate_system()
        point = entities.get("00070000")
        coordinates = system.params(point.params)
        result = system.solve()

        assert result == ResultFlag.OKAY
        assert coordinates[0] == pytest.approx(39.54852)
        assert coordinates[1] == pytest.approx(61.91009)


class TestInvolute:
    def test_load_success(self):
        system_factory = Slvstopy(file_path="tests/files/involute.slvs")
        system, entities = system_factory.generate_system()
        point = entities.get("00050000")
        coordinates = system.params(point.params)
        result = system.solve()

        assert result == ResultFlag.OKAY
        assert coordinates[0] == pytest.approx(12.62467, rel=1.5e-5)
        assert coordinates[1] == pytest.approx(1.51746, rel=1.5e-5)

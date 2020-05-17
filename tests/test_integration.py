import pytest

from python_solvespace import ResultFlag
from slvstopy import load_from_filepath


class TestCrankRocker:
    def test_load_succes(self):
        system, entities = load_from_filepath("tests/files/crank_rocker.slvs")
        point = entities.get("00070000")
        coordinates = system.params(point.params)
        result = system.solve()

        assert result == ResultFlag.OKAY
        assert coordinates[0] == pytest.approx(39.54852)
        assert coordinates[1] == pytest.approx(61.91009)


class TestInvolute:
    def test_load_succes(self):
        system, entities = load_from_filepath("tests/files/involute.slvs")
        point = entities.get("00050000")
        coordinates = system.params(point.params)
        result = system.solve()

        assert result == ResultFlag.OKAY
        assert coordinates[0] == pytest.approx(12.62467, rel=1.5e-5)
        assert coordinates[1] == pytest.approx(1.51746, rel=1.5e-5)

import pytest

from service import isilon_service

service = isilon_service.IsilonService()


def test_mock_data():
    assert service.Info(None, None).message == "Isilon data tbd"

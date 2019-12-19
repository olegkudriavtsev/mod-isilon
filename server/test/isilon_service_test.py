import unittest

from service import isilon_service
service = isilon_service.IsilonService()


class MyTestCase(unittest.TestCase):
    def test_mock_data_returned(self):
        self.assertEqual("Isilon data tbd", service.Info(None, None).message)


if __name__ == '__main__':
    unittest.main()

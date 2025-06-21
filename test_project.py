import unittest
from models import Package, Driver, Route
from utils import save_data, load_data
import timeit

class TestProject(unittest.TestCase):

    def test_package_creation(self):
        pkg = Package(1, "Jan", "Anna", 3.5)
        self.assertEqual(pkg.sender, "Jan")
        self.assertEqual(pkg.receiver, "Anna")
        self.assertGreater(pkg.weight, 0)

    def test_driver_creation(self):
        drv = Driver(1, "Tomasz", "Renault")
        self.assertEqual(drv.name, "Tomasz")
        self.assertIn("Renault", drv.vehicle)

    def test_route_estimate(self):
        pkg1 = Package(1, "A", "B", 2)
        pkg2 = Package(2, "C", "D", 3)
        driver = Driver(1, "X", "Fiat")
        route = Route("R1", driver, [pkg1, pkg2])
        self.assertEqual(route.estimate_time_minutes(), 50)

    def test_save_and_load(self):
        data = {
            "packages": [{"id": 1, "sender": "Jan", "receiver": "Ola", "weight": 2.0}],
            "drivers": [{"id": 1, "name": "Kuba", "vehicle": "Opel"}]
        }
        save_data(data, "test_data.json")
        loaded = load_data("test_data.json")
        self.assertEqual(loaded["packages"][0]["receiver"], "Ola")

    def test_speed_estimation_function(self):
        stmt = "sum([x for x in range(1000)])"
        exec_time = timeit.timeit(stmt, number=100)
        self.assertLess(exec_time, 1)

if __name__ == '__main__':
    unittest.main()

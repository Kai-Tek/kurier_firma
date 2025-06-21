import json
class Package:
    def __init__(self, package_id, sender, receiver, weight):
        self.package_id = package_id
        self.sender = sender
        self.receiver = receiver
        self.weight = weight

    def __str__(self):
        return f"Package {self.package_id} from {self.sender} to {self.receiver}, weight: {self.weight}kg"


class Driver:
    def __init__(self, driver_id, name, vehicle):
        self.driver_id = driver_id
        self.name = name
        self.vehicle = vehicle

    def __str__(self):
        return f"Driver {self.name} (ID: {self.driver_id}) - Vehicle: {self.vehicle}"


class Route:
    def __init__(self, route_id, driver, packages):
        self.route_id = route_id
        self.driver = driver
        self.packages = packages  # lista obiektów Package

    def __str__(self):
        return f"Route {self.route_id} with driver {self.driver.name}, {len(self.packages)} packages"

    def save_to_txt(self, filename):
        try:
            with open(filename, "w") as f:
                f.write(str(self) + "\n")
                for pkg in self.packages:
                    f.write(str(pkg) + "\n")
            print(f"Dane zapisane do pliku {filename}")
        except Exception as e:
            print(f"Błąd zapisu do pliku txt: {e}")

    def save_to_json(self, filename):
        try:
            data = {
                "route_id": self.route_id,
                "driver": {
                    "id": self.driver.driver_id,
                    "name": self.driver.name,
                    "vehicle": self.driver.vehicle
                },
                "packages": [
                    {
                        "id": pkg.package_id,
                        "sender": pkg.sender,
                        "receiver": pkg.receiver,
                        "weight": pkg.weight
                    } for pkg in self.packages
                ]
            }
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Dane zapisane do pliku {filename}")
        except Exception as e:
            print(f"Błąd zapisu do pliku JSON: {e}")

    def estimate_time_minutes(self):
        times = list(map(lambda pkg: pkg.weight * 10, self.packages))
        return sum(times)

class ExpressPackage(Package):
    def __init__(self, package_id, sender, receiver, weight, priority_level):
        super().__init__(package_id, sender, receiver, weight)
        self.priority_level = priority_level  # np. "wysoki", "niski"

    def __str__(self):
        return f"ExpressPackage {self.package_id} ({self.priority_level}) from {self.sender} to {self.receiver}, weight: {self.weight}kg"

def recursive_weight_sum(packages, index=0):
    if index >= len(packages):
        return 0
    return packages[index].weight + recursive_weight_sum(packages, index + 1)

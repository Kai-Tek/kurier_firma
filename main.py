from models import Package, Driver, Route, recursive_weight_sum
from utils import load_data, save_all
from functools import reduce
import matplotlib.pyplot as plt

print("Testy podstawowe:")
try:
    assert isinstance([], list)
    print("Listy działają")
except AssertionError:
    print("Błąd listy")

try:
    bad_pkg = Package(99, "X", "Y", -1.0)
    assert bad_pkg.weight >= 0, "Waga nie może być ujemna!"
except AssertionError as e:
    print(f"Test błędnej paczki: {e}")

# Wczytywanie danych z data.json - obsługa różnych nazw kluczy
data = load_data()
packages = [Package(
    p.get("id") or p.get("package_id"),
    p["sender"],
    p["receiver"],
    p["weight"]
) for p in data["packages"]]

drivers = [Driver(
    d.get("id") or d.get("driver_id"),
    d["name"],
    d["vehicle"]
) for d in data["drivers"]]

routes = []

def show_menu():
    print("\n=== MENU ===")
    print("1. Dodaj paczkę")
    print("2. Dodaj kierowcę")
    print("3. Stwórz trasę")
    print("4. Zapisz trasę do plików")
    print("5. Wyświetl wszystkie trasy")
    print("6. Statystyki paczek (set, tuple, dict, filter, reduce)")
    print("7. Zmień dane paczki (po ID)")
    print("8. Wyszukaj paczkę (po ID lub odbiorcy)")
    print("9. Wygeneruj wykres: liczba paczek na trasę")
    print("0. Wyjście")

while True:
    show_menu()
    choice = input("Wybierz opcję: ")

    if choice == "1":
        try:
            pid = int(input("ID paczki: "))
            sender = input("Nadawca: ")
            receiver = input("Odbiorca: ")
            weight = float(input("Waga (kg): "))
            assert weight >= 0, "Waga nie może być ujemna!"
            pkg = Package(pid, sender, receiver, weight)
            packages.append(pkg)
            print("Paczka dodana.")
            save_all(packages, drivers)
        except Exception as e:
            print(f"Błąd dodawania paczki: {e}")

    elif choice == "2":
        try:
            did = int(input("ID kierowcy: "))
            name = input("Imię kierowcy: ")
            vehicle = input("Pojazd: ")
            drv = Driver(did, name, vehicle)
            drivers.append(drv)
            print("Kierowca dodany.")
            save_all(packages, drivers)
        except Exception as e:
            print(f"Błąd dodawania kierowcy: {e}")

    elif choice == "3":
        if not packages or not drivers:
            print("Dodaj najpierw paczki i kierowcę.")
            continue
        route_id = input("ID trasy: ")
        print("Dostępni kierowcy:")
        for i, d in enumerate(drivers):
            print(f"{i}: {d.name}")
        try:
            d_idx = int(input("Wybierz kierowcę (nr): "))
            route = Route(route_id, drivers[d_idx], packages[:])  # wszystkie paczki
            routes.append(route)
            print("Trasa utworzona.")
        except Exception as e:
            print(f"Błąd tworzenia trasy: {e}")

    elif choice == "4":
        for route in routes:
            route.save_to_txt(f"trasa_{route.route_id}.txt")
            route.save_to_json(f"trasa_{route.route_id}.json")

    elif choice == "5":
        for r in routes:
            print(r)
            print(f"Szacowany czas: {r.estimate_time_minutes()} min")

    elif choice == "6":
        print("\nStatystyki paczek:")

        # dict - paczki po nadawcy
        paczki_po_nadawcy = {}
        for pkg in packages:
            paczki_po_nadawcy.setdefault(pkg.sender, []).append(pkg)
        for nadawca, lista in paczki_po_nadawcy.items():
            print(f"{nadawca}: {len(lista)} paczek")

        # set - unikalni nadawcy
        unikalni_nadawcy = set(pkg.sender for pkg in packages)
        print("Unikalni nadawcy:", unikalni_nadawcy)

        # tuple - wagi paczek
        wagi = tuple(pkg.weight for pkg in packages)
        print("Wagi paczek (tuple):", wagi)

        # rekurencja
        print("Całkowita waga paczek (rekurencyjnie):", recursive_weight_sum(packages), "kg")

        # filter
        try:
            prog = float(input("Pokaż paczki powyżej wagi (kg): "))
            ciezkie_paczki = list(filter(lambda p: p.weight > prog, packages))
            print(f"Paczki powyżej {prog} kg:")
            for p in ciezkie_paczki:
                print(" -", p)
        except:
            print("Nieprawidłowa waga.")

        # reduce
        waga_reduce = reduce(lambda acc, p: acc + p.weight, packages, 0)
        print("Całkowita waga paczek (reduce):", waga_reduce, "kg")

    elif choice == "7":
        try:
            pid = int(input("Podaj ID paczki do edycji: "))
            found = next((p for p in packages if p.package_id == pid), None)
            if found:
                print("Obecne dane:", found)
                found.sender = input("Nowy nadawca: ")
                found.receiver = input("Nowy odbiorca: ")
                found.weight = float(input("Nowa waga (kg): "))
                print("Dane paczki zaktualizowane.")
                save_all(packages, drivers)
            else:
                print("Nie znaleziono paczki o takim ID.")
        except Exception as e:
            print(f"Błąd edycji paczki: {e}")

    elif choice == "8":
        kryterium = input("Szukaj po (id/odbiorca): ").strip().lower()
        if kryterium == "id":
            try:
                pid = int(input("Podaj ID paczki: "))
                result = [p for p in packages if p.package_id == pid]
            except:
                result = []
        elif kryterium == "odbiorca":
            nazwa = input("Podaj nazwisko lub nazwę odbiorcy: ").lower()
            result = [p for p in packages if nazwa in p.receiver.lower()]
        else:
            print("Nieznane kryterium.")
            result = []

        if result:
            print("Znalezione paczki:")
            for p in result:
                print(" -", p)
        else:
            print("Brak wyników.")

    elif choice == "9":
        if not routes:
            print("Brak tras do pokazania.")
            continue

        labels = [r.route_id for r in routes]
        values = [len(r.packages) for r in routes]

        plt.figure(figsize=(6, 4))
        plt.bar(labels, values, color="skyblue")
        plt.title("Liczba paczek na trasę")
        plt.xlabel("ID trasy")
        plt.ylabel("Liczba paczek")
        plt.tight_layout()

        plt.savefig("wykres_paczki_na_trase.png")
        print("Wykres zapisany do pliku: wykres_paczki_na_trase.png")
        plt.show()

    elif choice == "0":
        print("Zamykanie programu.")
        break

    else:
        print("Nieznana opcja.")
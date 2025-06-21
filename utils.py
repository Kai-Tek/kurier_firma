import json

def load_data(filename="data.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Plik data.json nie istnieje. Tworzę pustą bazę.")
        return {"packages": [], "drivers": []}
    except Exception as e:
        print(f"Błąd wczytywania danych: {e}")
        return {"packages": [], "drivers": []}

def save_data(data, filename="data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Dane zapisane do {filename}")
    except Exception as e:
        print(f"Błąd zapisu danych: {e}")

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"Wywołano funkcję: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_action
def save_all(packages, drivers):
    save_data({
        "packages": [vars(p) for p in packages],
        "drivers": [vars(d) for d in drivers]
    })

